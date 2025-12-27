"""
Quick test script for tour types feature
Tests Architecture Tour with a sample route
"""
from dotenv import load_dotenv
load_dotenv()

from App.planner import plan_route
from App.tour_types import TOUR_TYPES

def test_architecture_tour():
    """Test Architecture Tour from King's Cross to London Bridge"""
    print("=" * 70)
    print("TESTING TOUR TYPES FEATURE")
    print("=" * 70)
    print()

    start = "King's Cross Station, London"
    end = "London Bridge Station, London"

    print(f"Route: {start} → {end}")
    print()

    # Test 1: All Landmarks (baseline)
    print("1️⃣  Testing 'All Landmarks' tour...")
    result_all = plan_route(start, end, "1", tour_type="all")
    print(f"   ✅ Landmarks found: {len(result_all['landmarks'])}")
    print(f"   Duration: {result_all['chosen_eta']:.1f} min")
    print()

    # Test 2: Architecture Tour
    print("2️⃣  Testing 'Architecture Tour'...")
    result_arch = plan_route(start, end, "1", tour_type="architecture")
    print(f"   ✅ Landmarks found: {len(result_arch['landmarks'])}")
    print(f"   Duration: {result_arch['chosen_eta']:.1f} min")

    if result_arch['landmarks']:
        print("   Landmarks:")
        for lm in result_arch['landmarks']:
            print(f"      - {lm['name']}")
    print()

    # Test 3: Historical Tour
    print("3️⃣  Testing 'Historical Tour'...")
    result_hist = plan_route(start, end, "1", tour_type="historical")
    print(f"   ✅ Landmarks found: {len(result_hist['landmarks'])}")
    print(f"   Duration: {result_hist['chosen_eta']:.1f} min")

    if result_hist['landmarks']:
        print("   Landmarks:")
        for lm in result_hist['landmarks']:
            print(f"      - {lm['name']}")
    print()

    # Test 4: Royal Tour
    print("4️⃣  Testing 'Royal Tour'...")
    result_royal = plan_route(start, end, "1", tour_type="royal")
    print(f"   ✅ Landmarks found: {len(result_royal['landmarks'])}")
    print(f"   Duration: {result_royal['chosen_eta']:.1f} min")

    if result_royal['landmarks']:
        print("   Landmarks:")
        for lm in result_royal['landmarks']:
            print(f"      - {lm['name']}")
    print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"All Landmarks:      {len(result_all['landmarks'])} landmarks")
    print(f"Architecture Tour:  {len(result_arch['landmarks'])} landmarks")
    print(f"Historical Tour:    {len(result_hist['landmarks'])} landmarks")
    print(f"Royal Tour:         {len(result_royal['landmarks'])} landmarks")
    print()
    print("✅ All tests completed successfully!")
    print()

if __name__ == "__main__":
    test_architecture_tour()
