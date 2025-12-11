from dotenv import load_dotenv
load_dotenv()

from App.planner import plan_route
from App.landmarks import grand_landmarks_near_route
from App.config import MAX_SCENIC_SELECT_CHOICES
from App.tour_types import TOUR_TYPES


def main():
    print("\n🚕 WELCOME TO THE ALFIE ROUTE PICKER\n")

    # 1️⃣ Tour Type Selection
    print("Choose Tour Type:")
    tour_options = list(TOUR_TYPES.items())
    for i, (key, config) in enumerate(tour_options, start=1):
        print(f"  {i}. {config['icon']}  {config['name']}")

    tour_choice = input("\nYour choice (1-9, or press Enter for All Landmarks): ").strip()
    if tour_choice.isdigit() and 1 <= int(tour_choice) <= len(tour_options):
        tour_type = tour_options[int(tour_choice) - 1][0]
        tour_name = tour_options[int(tour_choice) - 1][1]["name"]
    else:
        tour_type = "all"
        tour_name = "All Landmarks"

    print(f"✅ Selected: {tour_name}\n")

    # 2️⃣ Ask the user for start and end
    start = input("Start location: ").strip()
    end = input("Destination: ").strip()

    # 3️⃣ Get the baseline fastest route once
    fastest_result = plan_route(start, end, "1", tour_type=tour_type)
    fastest_eta = fastest_result["fastest_eta"]
    baseline_points = fastest_result["route_points"]

    # 4️⃣ Pre-calc Scenic Auto so we can show its ETA in the menu
    try:
        scenic_preview = plan_route(start, end, "2", tour_type=tour_type)
        scenic_eta = scenic_preview["chosen_eta"]
        scenic_diff = scenic_preview["difference"]
        scenic_label = f"{scenic_eta:.1f} min ({scenic_diff:+.1f} min vs fastest)"
    except Exception as e:
        print(f"\n[Warning] Could not pre-calculate Scenic Auto route: {e}")
        scenic_preview = None
        scenic_label = "ETA unavailable"

    # 5️⃣ Pre-calc grand landmarks near the fastest route (for Scenic Select menu)
    nearest_grand = grand_landmarks_near_route(baseline_points, tour_type=tour_type)

    # 4️⃣ Show menu WITH times
    print("\nChoose route mode:")
    print(f"1 → Fastest route ({fastest_eta:.1f} min)")
    print(f"2 → Scenic Auto (extra landmarks) [{scenic_label}]")
    print(
        f"3 → Scenic Select (choose up to {MAX_SCENIC_SELECT_CHOICES} big landmarks)"
    )

    mode = input("\nSelect 1 / 2 / 3: ").strip()
    chosen_indexes = None

    # 5️⃣ Scenic Select landmark picker
    if mode == "3":
        print("\n🏛  GRAND LANDMARKS YOU CAN CHOOSE:")
        for i, lm in enumerate(nearest_grand, start=1):
            print(f"{i}. {lm['name']}")

        raw = input(
            f"\nChoose up to {MAX_SCENIC_SELECT_CHOICES} numbers (comma-separated): "
        )
        if raw.strip():
            nums = [int(x) - 1 for x in raw.split(",") if x.strip().isdigit()]
            chosen_indexes = nums[:MAX_SCENIC_SELECT_CHOICES]

    # 6️⃣ Compute the FINAL route, based on confirmed mode

    if mode == "1":
        # Fastest: reuse the result we already computed
        result = fastest_result
    elif mode == "2":
        # Scenic Auto: reuse preview if available, otherwise recompute once
        if scenic_preview is not None:
            result = scenic_preview
        else:
            result = plan_route(start, end, "2", tour_type=tour_type)
    elif mode == "3":
        # Scenic Select: needs the chosen landmark indexes
        result = plan_route(start, end, "3", chosen_indexes, tour_type=tour_type)
    else:
        print("Invalid choice → defaulting to fastest.")
        result = fastest_result

    # 7️⃣ Print time summary
    print("\n==== 🕒 ROUTE TIME SUMMARY ====")
    print(f"Mode: {result['mode']}")
    if result.get("tour_type") and result["tour_type"] != "all":
        print(f"Tour Type: {tour_name}")
    print(f"Fastest ETA: {result['fastest_eta']:.1f} min")
    print(f"Chosen ETA:  {result['chosen_eta']:.1f} min")
    print(f"Difference:  {result['difference']:+.1f} min")

    # 8️⃣ Print landmarks
    print("\n==== 🚕 LANDMARKS YOU'LL PASS ====")
    print("--------------------------------")
    if not result["landmarks"]:
        print("No landmarks found for this route.")
    else:
        for lm in result["landmarks"]:
            print(
                f"\n➡️  {lm['name']} "
                f"({lm['side']} side, {lm['distance_m']:.1f}m away)"
            )
            if lm.get("script"):
                print(lm["script"])


if __name__ == "__main__":
    main()
