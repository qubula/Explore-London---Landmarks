"""
One-time script to categorize all 1,327 landmarks and save results.

This creates cached category assignments for fast filtering.
Run this script whenever:
- Adding a new tour type
- Modifying tour type keywords
- Updating landmark data

Usage:
    python3 App/precompute_tour_categories.py
"""

import json
from pathlib import Path
from App.tour_types import TOUR_TYPES
from App.categorize_landmarks import get_landmarks_for_tour_type


def precompute_all_categories():
    """
    Categorize all landmarks for all tour types.
    Save to Data/tour_categories.json for fast lookup.
    """
    print("=" * 70)
    print("PRECOMPUTING TOUR CATEGORIES")
    print("=" * 70)
    print()

    # Load all landmarks
    landmarks_file = Path("Data/final_landmarks_v6.2_Big.json")
    print(f"Loading landmarks from: {landmarks_file}")

    with open(landmarks_file, 'r', encoding='utf-8') as f:
        all_landmarks = json.load(f)

    print(f"✅ Loaded {len(all_landmarks)} landmarks")
    print()

    categories = {}

    # Categorize for each tour type (except "all")
    for tour_type, config in TOUR_TYPES.items():
        if tour_type == "all":
            continue

        print(f"📍 Categorizing for: {config['icon']} {config['name']}")

        matching = get_landmarks_for_tour_type(tour_type, all_landmarks)

        categories[tour_type] = {
            "count": len(matching),
            "name": config["name"],
            "icon": config["icon"],
            "color": config["color"],
            "landmarks": [
                {
                    "name": lm[0]["name"],
                    "lat": lm[0]["lat"],
                    "lng": lm[0]["lng"],
                    "score": lm[1]
                }
                for lm in matching[:200]  # Top 200 per category
            ]
        }

        print(f"   Found {len(matching)} landmarks")
        if matching:
            print(f"   Top 5: {', '.join([lm[0]['name'] for lm in matching[:5]])}")
        print()

    # Save results
    output_file = Path("Data/tour_categories.json")
    print(f"💾 Saving results to: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(categories, f, indent=2)

    print()
    print("=" * 70)
    print("✅ CATEGORIZATION COMPLETE!")
    print("=" * 70)
    print()

    # Print summary
    print("SUMMARY:")
    total_categorized = sum(cat["count"] for cat in categories.values())
    print(f"  Total landmarks: {len(all_landmarks)}")
    print(f"  Total categorizations: {total_categorized}")
    print()

    print("COUNTS BY TOUR TYPE:")
    for tour_type, data in sorted(categories.items(), key=lambda x: x[1]["count"], reverse=True):
        icon = data["icon"]
        name = data["name"]
        count = data["count"]
        pct = (count / len(all_landmarks)) * 100
        print(f"  {icon} {name:25s}: {count:4d} landmarks ({pct:5.1f}%)")
    print()

    # Warnings
    print("WARNINGS:")
    low_count_types = [
        (data["name"], data["count"])
        for data in categories.values()
        if data["count"] < 50
    ]

    if low_count_types:
        print("  ⚠️ Tour types with <50 landmarks:")
        for name, count in low_count_types:
            print(f"     - {name}: {count} landmarks")
        print("  Consider adjusting min_score or adding more keywords")
    else:
        print("  ✅ All tour types have sufficient landmarks (≥50)")

    print()


if __name__ == "__main__":
    precompute_all_categories()
