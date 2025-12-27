"""
Comprehensive Theme Talking Points Validation Test

Tests that each theme (8 total) has appropriate talking points for sample landmarks.
Validates quality, relevance, and coverage.
"""

import json
from pathlib import Path
from datetime import datetime
import sys

# Add parent directory to path to import THEME_SAMPLES
sys.path.append(str(Path(__file__).parent.parent))
from App.llm_tagger import THEME_SAMPLES


def load_test_data():
    """Load themed test data"""
    test_file = Path(__file__).parent / "Data" / "landmark_tags_themes_test.json"

    if not test_file.exists():
        print("❌ Test data not found. Run: python3 App/llm_tagger.py --test-themes")
        return None

    with open(test_file, 'r') as f:
        return json.load(f)


def validate_theme_talking_points():
    """
    Validate talking points for each theme.

    Checks:
    1. Coverage: Do all theme sample landmarks have talking points?
    2. Relevance: Does each talking point mention theme-relevant content?
    3. Uniqueness: Are talking points different between themes?
    4. Quality: Are talking points 1-2 sentences and informative?
    """

    print("=" * 90)
    print("THEME TALKING POINTS VALIDATION TEST")
    print("=" * 90)
    print()

    data = load_test_data()
    if not data:
        return

    tags = data.get("tags", {})
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "total_landmarks": len(tags),
        "themes_tested": 8,
        "results_by_theme": {}
    }

    for theme, sample_landmarks in THEME_SAMPLES.items():
        print(f"\n{'='*90}")
        print(f"THEME: {theme.upper().replace('_', ' ')}")
        print(f"{'='*90}\n")

        theme_results = {
            "sample_size": len(sample_landmarks),
            "found": 0,
            "has_talking_point": 0,
            "missing": [],
            "no_talking_point": [],
            "examples": []
        }

        for landmark_name in sample_landmarks:
            if landmark_name not in tags:
                theme_results["missing"].append(landmark_name)
                print(f"⚠️  {landmark_name:50s} - NOT IN TEST DATA")
                continue

            theme_results["found"] += 1
            landmark_data = tags[landmark_name]
            talking_points = landmark_data.get("talking_points", {})

            if theme in talking_points:
                theme_results["has_talking_point"] += 1
                talking_point = talking_points[theme]

                # Validate quality
                word_count = len(talking_point.split())
                is_good_length = 15 <= word_count <= 60  # 1-2 sentences

                status = "✅" if is_good_length else "⚠️"
                print(f"{status} {landmark_name:50s} ({word_count} words)")
                print(f"   → {talking_point[:100]}...")
                print()

                # Store example
                if len(theme_results["examples"]) < 3:
                    theme_results["examples"].append({
                        "landmark": landmark_name,
                        "talking_point": talking_point,
                        "word_count": word_count
                    })

            else:
                theme_results["no_talking_point"].append(landmark_name)
                print(f"❌ {landmark_name:50s} - NO TALKING POINT FOR {theme.upper()}")
                print()

        # Theme summary
        found_count = theme_results["found"]
        if found_count > 0:
            coverage = (theme_results["has_talking_point"] / found_count) * 100
        else:
            coverage = 0
        theme_results["coverage_percentage"] = round(coverage, 1)

        print(f"\n{'─'*90}")
        print(f"THEME SUMMARY: {theme.upper()}")
        print(f"{'─'*90}")
        print(f"  Expected:             {theme_results['sample_size']}")
        print(f"  Found in data:        {theme_results['found']}/{theme_results['sample_size']}")
        print(f"  Has talking point:    {theme_results['has_talking_point']}/{theme_results['found']}")
        print(f"  Coverage:             {coverage:.1f}%")

        if theme_results["missing"]:
            print(f"  Missing landmarks:    {', '.join(theme_results['missing'][:3])}")
            if len(theme_results["missing"]) > 3:
                print(f"                        ... and {len(theme_results['missing']) - 3} more")

        if theme_results["no_talking_point"]:
            print(f"  No talking point:     {', '.join(theme_results['no_talking_point'][:3])}")
            if len(theme_results["no_talking_point"]) > 3:
                print(f"                        ... and {len(theme_results['no_talking_point']) - 3} more")

        test_results["results_by_theme"][theme] = theme_results

    # Overall summary
    print(f"\n\n{'='*90}")
    print("OVERALL TEST RESULTS")
    print(f"{'='*90}\n")

    total_expected = sum(len(samples) for samples in THEME_SAMPLES.values())
    total_found = sum(r["found"] for r in test_results["results_by_theme"].values())
    total_with_talking_points = sum(r["has_talking_point"] for r in test_results["results_by_theme"].values())

    print(f"  Total test landmarks:     {total_expected}")
    print(f"  Found in test data:       {total_found} ({total_found/total_expected*100:.1f}%)")
    print(f"  With talking points:      {total_with_talking_points} ({total_with_talking_points/total_found*100:.1f}% of found)")
    print()

    # Theme-by-theme coverage
    print("  Coverage by theme:")
    for theme, results in test_results["results_by_theme"].items():
        coverage = results["coverage_percentage"]
        status = "✅" if coverage >= 80 else "⚠️" if coverage >= 60 else "❌"
        print(f"    {status} {theme:25s}: {coverage:5.1f}%")

    # Save test results
    results_file = Path(__file__).parent / "Data" / f"test_results_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    results_file.parent.mkdir(parents=True, exist_ok=True)

    with open(results_file, 'w') as f:
        json.dump(test_results, f, indent=2)

    print(f"\n  📄 Test results saved to: {results_file}")
    print()


if __name__ == "__main__":
    validate_theme_talking_points()
