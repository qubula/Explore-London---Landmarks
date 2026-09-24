"""
generate_receipt_batch.py

Generates a batch of visual thermal-printer receipts for ~30 different,
real London journeys, using the live planner (Google Directions + Static
Maps APIs) so each receipt reflects an actual route, duration and set of
landmarks.

Output: Receipt_Batch_30/<NN>_<start>_to_<end>.png
"""

import os
import re
import time

from dotenv import load_dotenv
load_dotenv()

from App.planner import plan_route
from App.receipt_generator import generate_visual_receipt

OUTPUT_DIR = "Receipt_Batch_30"

# (start, end, mode, tour_type)
# mode: "1" = Fastest, "2" = Scenic Auto
JOURNEYS = [
    ("King's Cross Station, London", "Waterloo Station, London", "2", "all"),
    ("Paddington Station, London", "Liverpool Street Station, London", "2", "architecture"),
    ("Victoria Station, London", "Tower Hill, London", "2", "royal"),
    ("Camden Town, London", "Notting Hill Gate, London", "1", "all"),
    ("Vauxhall, London", "Pimlico, London", "2", "all"),
    ("British Museum, London", "Natural History Museum, London", "2", "all"),
    ("Buckingham Palace, London", "Westminster Abbey, London", "1", "royal"),
    ("Tower of London", "Borough Market, London", "2", "all"),
    ("Westminster Abbey, London", "St Paul's Cathedral, London", "2", "religious"),
    ("Hyde Park Corner, London", "Kensington Palace, London", "2", "all"),
    ("St Paul's Cathedral, London", "Tate Modern, London", "1", "all"),
    ("Covent Garden, London", "Somerset House, London", "1", "all"),
    ("Shoreditch High Street, London", "Liverpool Street Station, London", "1", "all"),
    ("Regent's Park, London", "Camden Market, London", "2", "all"),
    ("London Bridge Station, London", "Tower Bridge, London", "1", "all"),
    ("Marble Arch, London", "Oxford Circus, London", "1", "all"),
    ("Stratford, London", "Hackney, London", "1", "all"),
    ("Holborn Station, London", "Covent Garden, London", "1", "all"),
    ("South Kensington Station, London", "Hyde Park, London", "2", "all"),
    ("Bank Station, London", "Tower of London", "1", "architecture"),
    ("Notting Hill Gate, London", "Paddington Station, London", "1", "all"),
    ("Westminster Station, London", "Buckingham Palace, London", "1", "royal"),
    ("Angel, Islington, London", "King's Cross Station, London", "2", "all"),
    ("Whitechapel, London", "Tower Hill, London", "2", "all"),
    ("Peckham, London", "Brixton, London", "1", "all"),
    ("Liverpool Street Station, London", "Spitalfields Market, London", "1", "all"),
    ("Baker Street Station, London", "Regent's Park, London", "1", "all"),
    ("Clapham Common, London", "Brixton, London", "1", "all"),
    ("Hampstead Heath, London", "Camden Town, London", "2", "all"),
    ("Temple, London", "St Paul's Cathedral, London", "2", "religious"),
]


def slugify(text: str) -> str:
    text = text.split(",")[0]  # drop ", London" etc.
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_")
    return text


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    results = []

    for i, (start, end, mode, tour_type) in enumerate(JOURNEYS, 1):
        label = f"{i:02d}_{slugify(start)}_to_{slugify(end)}"
        print(f"[{i:02d}/{len(JOURNEYS)}] {start} -> {end}  (mode={mode}, theme={tour_type})")

        try:
            result = plan_route(start=start, end=end, mode=mode, tour_type=tour_type)

            receipt_path = generate_visual_receipt(
                landmarks=result["landmarks"],
                tour_type=result["tour_type"],
                route_mode=result["mode"],
                start_location=start,
                end_location=end,
                journey_time=f"{int(round(result['chosen_eta']))} min",
                route_points=result["route_points"],
            )

            final_path = os.path.join(OUTPUT_DIR, f"{label}.png")
            os.replace(receipt_path, final_path)

            print(f"    -> {final_path}  ({len(result['landmarks'])} landmarks, "
                  f"{result['chosen_eta']:.1f} min)")
            results.append((label, len(result["landmarks"]), result["chosen_eta"]))

        except Exception as e:
            print(f"    !! FAILED: {e}")
            results.append((label, None, None))

        time.sleep(0.4)  # be gentle on the API

    print()
    print("=" * 60)
    print(f"Done. {sum(1 for r in results if r[1] is not None)}/{len(JOURNEYS)} receipts generated.")
    empty = [r[0] for r in results if r[1] == 0]
    failed = [r[0] for r in results if r[1] is None]
    if empty:
        print(f"Receipts with no landmarks ({len(empty)}): {', '.join(empty)}")
    if failed:
        print(f"Failed ({len(failed)}): {', '.join(failed)}")


if __name__ == "__main__":
    main()
