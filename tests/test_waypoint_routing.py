"""
Test script for Option B: Enhanced Scenic Auto with Smart Waypoints

Tests that waypoint-based routing is working correctly:
- Victorian tour (29 landmarks): Should select waypoints, 5-9 min detour, 3-5 landmarks
- Religious tour (37 landmarks): Should select waypoints, 5-8 min detour, 3-4 landmarks
- All tour (1,327 landmarks): Should maintain current performance (3 min detour, 5-7 landmarks)

Usage:
    python3 tests/test_waypoint_routing.py
"""

import sys
sys.path.append('.')

from App.planner import plan_route

def test_waypoint_routing():
    """Test scenic auto with waypoint routing for different tour types"""

    # Test coordinates (Camden Town to Tower Bridge)
    start = "51.5392,-0.1426"  # Camden Town
    end = "51.5055,-0.0754"    # Tower Bridge

    print("=" * 80)
    print("WAYPOINT ROUTING TEST (OPTION B)")
    print("=" * 80)
    print()
    print(f"Route: Camden Town → Tower Bridge")
    print()

    test_cases = [
        ("victorian", "Victorian Tour (29 landmarks)", "2.5x factor, 9 min max", 3, 5),
        ("religious", "Religious Tour (37 landmarks)", "2.2x factor, 8 min max", 3, 4),
        ("all", "All Landmarks (1,327 total)", "1.4x factor, 5 min max", 5, 10),
    ]

    for tour_type, description, config, min_expected, max_expected in test_cases:
        print(f"\n{'─' * 80}")
        print(f"Tour Type: {description}")
        print(f"Config:    {config}")
        print(f"Expected:  {min_expected}-{max_expected} landmarks")
        print(f"{'─' * 80}")

        try:
            # Run scenic auto (mode "2")
            result = plan_route(start, end, "2", tour_type=tour_type)

            # Extract results
            fastest_min = result["fastest_eta"]
            chosen_min = result["chosen_eta"]
            diff_min = result["difference"]
            landmark_count = len(result.get("landmarks", []))
            metadata = result.get("metadata", {})

            routing_mode = metadata.get("mode", "unknown")
            waypoints = metadata.get("waypoints", [])
            score = metadata.get("score", 0)

            print(f"\n✅ Success!")
            print(f"   Routing Mode: {routing_mode}")
            print(f"   Fastest:      {fastest_min:.1f} min")
            print(f"   Scenic:       {chosen_min:.1f} min")
            print(f"   Detour:       +{diff_min:.1f} min")
            print(f"   Landmarks:    {landmark_count}")
            print(f"   Score:        {score}")

            if waypoints:
                print(f"\n   Waypoints Used ({len(waypoints)}):")
                for i, wp in enumerate(waypoints, 1):
                    print(f"      {i}. {wp['name']} ({wp['lat']:.4f}, {wp['lng']:.4f})")
            else:
                print(f"\n   No waypoints used (alternatives route selected)")

            if landmark_count > 0:
                print(f"\n   Landmarks Found:")
                for i, lm in enumerate(result["landmarks"][:5], 1):  # Show first 5
                    print(f"      {i}. {lm['name']} ({lm['side']})")
                if landmark_count > 5:
                    print(f"      ... and {landmark_count - 5} more")
            else:
                print(f"\n   ⚠️  No landmarks found")

            # Validation
            print(f"\n   Validation:")
            if min_expected <= landmark_count <= max_expected:
                print(f"      ✅ Landmark count within expected range ({min_expected}-{max_expected})")
            else:
                print(f"      ⚠️  Landmark count outside expected range (got {landmark_count}, expected {min_expected}-{max_expected})")

            if tour_type in ["victorian", "religious"]:
                # Themed tours should use longer detours
                if diff_min >= 3.0:
                    print(f"      ✅ Detour time is good (+{diff_min:.1f} min >= 3 min)")
                else:
                    print(f"      ⚠️  Detour time is low (+{diff_min:.1f} min < 3 min)")
            else:
                # All tour should keep detours reasonable (up to 5 min)
                if diff_min <= 5.5:
                    print(f"      ✅ Detour time is reasonable (+{diff_min:.1f} min <= 5.5 min)")
                else:
                    print(f"      ⚠️  Detour time is high (+{diff_min:.1f} min > 5.5 min)")

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'=' * 80}")
    print("TEST COMPLETE")
    print(f"{'=' * 80}\n")

    print("\nExpected Improvements from Option B:")
    print("  - Victorian tour: Should show MORE landmarks with waypoint routing (3-5)")
    print("  - Religious tour: Should show MORE landmarks with waypoint routing (3-4)")
    print("  - All tour: With 5-min budget, should benefit from waypoint routing (5-10 landmarks)")
    print("  - Waypoints should be visible in metadata when selected")
    print()


if __name__ == "__main__":
    test_waypoint_routing()
