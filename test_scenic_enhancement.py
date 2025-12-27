"""
Test script for scenic auto mode enhancement.

Tests that tour-specific detour factors are working correctly:
- Victorian tour (29 landmarks): 2.5x factor, 9 min max
- Religious tour (37 landmarks): 2.2x factor, 8 min max
- All tour (1,327 landmarks): 1.4x factor, 3 min max

Usage:
    python3 test_scenic_enhancement.py
"""

import sys
sys.path.append('.')

from App.planner import scenic_auto_route

def test_scenic_detours():
    """Test scenic auto with different tour types"""

    # Test coordinates (Camden Town to Tower Bridge)
    start = "51.5392,-0.1426"  # Camden Town
    end = "51.5055,-0.0754"    # Tower Bridge

    print("=" * 80)
    print("SCENIC AUTO MODE ENHANCEMENT TEST")
    print("=" * 80)
    print()
    print(f"Route: Camden Town → Tower Bridge")
    print()

    test_cases = [
        ("all", "All Landmarks (1,327 total)", "1.4x factor, 3 min max"),
        ("victorian", "Victorian Tour (29 landmarks)", "2.5x factor, 9 min max"),
        ("religious", "Religious Tour (37 landmarks)", "2.2x factor, 8 min max"),
    ]

    for tour_type, description, expected in test_cases:
        print(f"\n{'─' * 80}")
        print(f"Tour Type: {description}")
        print(f"Expected:  {expected}")
        print(f"{'─' * 80}")

        try:
            result = scenic_auto_route(start, end, tour_type=tour_type)

            duration_min = result["duration_min"]
            landmark_count = len(result.get("landmarks", []))

            print(f"✅ Success!")
            print(f"   Duration: {duration_min:.1f} minutes")
            print(f"   Landmarks: {landmark_count}")

            if landmark_count > 0:
                print(f"   Landmarks found:")
                for i, lm in enumerate(result["landmarks"][:5], 1):  # Show first 5
                    print(f"      {i}. {lm['name']}")
                if landmark_count > 5:
                    print(f"      ... and {landmark_count - 5} more")
            else:
                print(f"   ⚠️  No landmarks found")

        except Exception as e:
            print(f"❌ Error: {e}")

    print(f"\n{'=' * 80}")
    print("TEST COMPLETE")
    print(f"{'=' * 80}\n")

    print("\nExpected Improvements:")
    print("  - Victorian tour: Should show MORE landmarks than before (target: 3-5)")
    print("  - Religious tour: Should show MORE landmarks than before (target: 3-4)")
    print("  - All tour: Should maintain similar performance (5-7 landmarks)")
    print()


if __name__ == "__main__":
    test_scenic_detours()
