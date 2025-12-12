"""
Tour Category Validation Tool

This script analyzes tour categorization results and detects common error patterns:
- Substring matches (keywords matching in middle of words)
- Temporal mismatches (wrong era landmarks)
- Word boundary issues
- Unexpected category overlaps

Usage:
    python3 App/validate_tour_categories.py                    # Full report
    python3 App/validate_tour_categories.py --tour=victorian   # Specific tour
    python3 App/validate_tour_categories.py --verbose          # Detailed output
"""

import json
import re
import sys
from collections import defaultdict

from App.tour_types import TOUR_TYPES, get_tour_type_config
from App.categorize_landmarks import categorize_landmark
from App.landmarks import score_grand_landmark


# Tour era date ranges for temporal validation
TOUR_ERA_DATES = {
    "victorian": (1837, 1901),
    "modern": (2000, 2100),
    # Other tours don't have strict date ranges
}

# Incompatible tour type pairs
INCOMPATIBLE_PAIRS = [
    ("modern", "victorian"),
    ("modern", "19th century"),
]


def load_landmarks():
    """Load all landmarks from JSON file."""
    with open('Data/final_landmarks_v6.2_Big.json', 'r') as f:
        return json.load(f)


def extract_years_from_text(text):
    """Extract 4-digit years from text using regex."""
    # Match years from 1000-2099
    years = re.findall(r'\b(1[0-9]{3}|20[0-9]{2})\b', text)
    return [int(y) for y in years]


def detect_substring_matches(all_landmarks):
    """
    Find keywords matching in the middle of words (not at word boundaries).

    Returns:
        List of dicts with: {
            'landmark': landmark dict,
            'tour_type': str,
            'keyword': str,
            'context': str (surrounding text),
            'score': int
        }
    """
    print("\n🔍 DETECTING SUBSTRING MATCHES...")
    issues = []

    for tour_type, config in TOUR_TYPES.items():
        if tour_type == "all" or not config["keywords"]:
            continue

        for landmark in all_landmarks:
            name = landmark.get("name", "").lower()
            summary = landmark.get("summary", "").lower()
            combined_text = f"{name} {summary}"

            # Check each keyword
            for keyword in config["keywords"]:
                # Does it match as substring?
                if keyword in combined_text:
                    # Check if it matches as whole word
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                    if not re.search(pattern, combined_text):
                        # Find context (50 chars before and after)
                        idx = combined_text.find(keyword)
                        start = max(0, idx - 50)
                        end = min(len(combined_text), idx + len(keyword) + 50)
                        context = combined_text[start:end]

                        # Get the score
                        matches, score = categorize_landmark(landmark, config)

                        if matches:  # Only report if it actually got categorized
                            issues.append({
                                'landmark': landmark,
                                'tour_type': tour_type,
                                'keyword': keyword,
                                'context': context,
                                'score': score
                            })

    print(f"   Found {len(issues)} substring match issues")
    return issues


def detect_temporal_mismatches(all_landmarks):
    """
    Find landmarks with dates that contradict the tour era.

    Returns:
        List of dicts with: {
            'landmark': landmark dict,
            'tour_type': str,
            'found_year': int,
            'era_range': tuple (start, end),
            'score': int
        }
    """
    print("\n📅 DETECTING TEMPORAL MISMATCHES...")
    issues = []

    for tour_type, era_range in TOUR_ERA_DATES.items():
        config = get_tour_type_config(tour_type)

        for landmark in all_landmarks:
            matches, score = categorize_landmark(landmark, config)

            if matches:
                # Extract years from summary
                summary = landmark.get("summary", "")
                years = extract_years_from_text(summary)

                # Check if any year falls outside the era
                for year in years:
                    if year < era_range[0] or year > era_range[1]:
                        issues.append({
                            'landmark': landmark,
                            'tour_type': tour_type,
                            'found_year': year,
                            'era_range': era_range,
                            'score': score
                        })
                        break  # One mismatch per landmark is enough

    print(f"   Found {len(issues)} temporal mismatch issues")
    return issues


def analyze_word_boundaries(all_landmarks):
    """
    Test how many matches would change if word boundaries were enforced.

    Returns:
        Dict with: {
            'tour_type': {
                'current_count': int,
                'with_boundaries_count': int,
                'would_lose': list of landmark names
            }
        }
    """
    print("\n🔤 ANALYZING WORD BOUNDARY IMPACT...")
    results = {}

    for tour_type, config in TOUR_TYPES.items():
        if tour_type == "all" or not config["keywords"]:
            continue

        current_matches = []
        boundary_matches = []

        for landmark in all_landmarks:
            name = landmark.get("name", "").lower()
            summary = landmark.get("summary", "").lower()
            combined_text = f"{name} {summary}"

            # Current substring matching
            matches_current = any(keyword in combined_text for keyword in config["keywords"])
            exclude_current = any(keyword in combined_text for keyword in config["exclude_keywords"])

            if matches_current and not exclude_current:
                current_matches.append(landmark)

            # Word boundary matching
            matches_boundary = any(
                re.search(r'\b' + re.escape(keyword) + r'\b', combined_text)
                for keyword in config["keywords"]
            )
            exclude_boundary = any(
                re.search(r'\b' + re.escape(keyword) + r'\b', combined_text)
                for keyword in config["exclude_keywords"]
            )

            if matches_boundary and not exclude_boundary:
                boundary_matches.append(landmark)

        # Find landmarks that would be lost
        current_names = {lm['name'] for lm in current_matches}
        boundary_names = {lm['name'] for lm in boundary_matches}
        would_lose = current_names - boundary_names

        results[tour_type] = {
            'current_count': len(current_matches),
            'with_boundaries_count': len(boundary_matches),
            'would_lose': sorted(list(would_lose))
        }

    total_would_lose = sum(len(r['would_lose']) for r in results.values())
    print(f"   {total_would_lose} total landmarks would be removed with word boundaries")
    return results


def find_unexpected_overlaps(all_landmarks):
    """
    Find landmarks categorized in incompatible tour types.

    Returns:
        List of dicts with: {
            'landmark': landmark dict,
            'conflicting_tours': list of tour_type strings,
            'keywords_matched': dict {tour_type: [keywords]}
        }
    """
    print("\n⚠️  DETECTING UNEXPECTED CATEGORY OVERLAPS...")
    issues = []

    # Build categorization map
    landmark_tours = defaultdict(list)
    landmark_keywords = defaultdict(dict)

    for landmark in all_landmarks:
        for tour_type, config in TOUR_TYPES.items():
            if tour_type == "all":
                continue

            matches, score = categorize_landmark(landmark, config)
            if matches:
                landmark_tours[landmark['name']].append(tour_type)

                # Find which keywords matched
                name = landmark.get("name", "").lower()
                summary = landmark.get("summary", "").lower()
                combined_text = f"{name} {summary}"

                matched_keywords = [
                    kw for kw in config["keywords"]
                    if kw in combined_text
                ]
                landmark_keywords[landmark['name']][tour_type] = matched_keywords

    # Check for incompatible pairs
    for landmark in all_landmarks:
        lm_name = landmark['name']
        tours = landmark_tours.get(lm_name, [])

        for tour1, tour2 in INCOMPATIBLE_PAIRS:
            if tour1 in tours and tour2 in tours:
                issues.append({
                    'landmark': landmark,
                    'conflicting_tours': [tour1, tour2],
                    'keywords_matched': landmark_keywords[lm_name]
                })
                break  # One conflict per landmark is enough

    print(f"   Found {len(issues)} unexpected overlaps")
    return issues


def generate_report(substring_issues, temporal_issues, boundary_analysis, overlap_issues, verbose=False):
    """Generate and print comprehensive validation report."""

    print("\n" + "=" * 70)
    print("TOUR CATEGORY VALIDATION REPORT")
    print("=" * 70)

    # 1. Substring Match Issues
    print("\n📍 SUBSTRING MATCH ISSUES")
    print("-" * 70)
    if substring_issues:
        # Group by tour type
        by_tour = defaultdict(list)
        for issue in substring_issues:
            by_tour[issue['tour_type']].append(issue)

        for tour_type in sorted(by_tour.keys()):
            issues = by_tour[tour_type]
            tour_config = get_tour_type_config(tour_type)
            print(f"\n{tour_config['icon']} {tour_config['name']}: {len(issues)} issues")

            if verbose:
                for issue in issues[:5]:  # Show top 5
                    print(f"   ❌ {issue['landmark']['name']}")
                    print(f"      Keyword: '{issue['keyword']}'")
                    print(f"      Context: ...{issue['context']}...")
                    print(f"      Score: {issue['score']}")
                if len(issues) > 5:
                    print(f"   ... and {len(issues) - 5} more")
    else:
        print("✅ No substring match issues found!")

    # 2. Temporal Mismatch Issues
    print("\n\n📅 TEMPORAL MISMATCH ISSUES")
    print("-" * 70)
    if temporal_issues:
        for issue in temporal_issues:
            tour_config = get_tour_type_config(issue['tour_type'])
            era_start, era_end = issue['era_range']
            print(f"\n❌ {issue['landmark']['name']}")
            print(f"   Tour: {tour_config['icon']} {tour_config['name']} ({era_start}-{era_end})")
            print(f"   Found year: {issue['found_year']}")
            print(f"   Difference: {issue['found_year'] - era_end} years too {'recent' if issue['found_year'] > era_end else 'old'}")
            print(f"   Score: {issue['score']}")
    else:
        print("✅ No temporal mismatch issues found!")

    # 3. Word Boundary Analysis
    print("\n\n🔤 WORD BOUNDARY IMPACT ANALYSIS")
    print("-" * 70)
    print("Shows how many landmarks would be removed if word boundaries were enforced:\n")

    for tour_type in sorted(boundary_analysis.keys()):
        analysis = boundary_analysis[tour_type]
        tour_config = get_tour_type_config(tour_type)

        current = analysis['current_count']
        with_boundaries = analysis['with_boundaries_count']
        diff = current - with_boundaries

        if diff > 0:
            print(f"{tour_config['icon']} {tour_config['name']}:")
            print(f"   Current: {current} landmarks")
            print(f"   With word boundaries: {with_boundaries} landmarks")
            print(f"   Would remove: {diff} landmarks")

            if verbose and analysis['would_lose']:
                print(f"   Examples:")
                for name in analysis['would_lose'][:3]:
                    print(f"      - {name}")
                if len(analysis['would_lose']) > 3:
                    print(f"      ... and {len(analysis['would_lose']) - 3} more")
            print()

    # 4. Unexpected Overlaps
    print("\n⚠️  UNEXPECTED CATEGORY OVERLAPS")
    print("-" * 70)
    if overlap_issues:
        for issue in overlap_issues:
            print(f"\n❌ {issue['landmark']['name']}")
            print(f"   Conflicting tours: {', '.join(issue['conflicting_tours'])}")
            if verbose:
                print(f"   Matched keywords:")
                for tour, keywords in issue['keywords_matched'].items():
                    if tour in issue['conflicting_tours']:
                        print(f"      {tour}: {', '.join(keywords)}")
    else:
        print("✅ No unexpected overlaps found!")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Substring matches: {len(substring_issues)}")
    print(f"Temporal mismatches: {len(temporal_issues)}")
    print(f"Unexpected overlaps: {len(overlap_issues)}")

    total_boundary_impact = sum(
        a['current_count'] - a['with_boundaries_count']
        for a in boundary_analysis.values()
    )
    print(f"Landmarks that would be removed with word boundaries: {total_boundary_impact}")

    total_issues = len(substring_issues) + len(temporal_issues) + len(overlap_issues)
    print(f"\n🔍 Total issues detected: {total_issues}")
    print("=" * 70 + "\n")


def save_report_to_file(substring_issues, temporal_issues, boundary_analysis, overlap_issues):
    """Save validation results to JSON file."""
    output = {
        'substring_matches': [
            {
                'landmark_name': issue['landmark']['name'],
                'tour_type': issue['tour_type'],
                'keyword': issue['keyword'],
                'context': issue['context'],
                'score': issue['score']
            }
            for issue in substring_issues
        ],
        'temporal_mismatches': [
            {
                'landmark_name': issue['landmark']['name'],
                'tour_type': issue['tour_type'],
                'found_year': issue['found_year'],
                'era_range': issue['era_range'],
                'score': issue['score']
            }
            for issue in temporal_issues
        ],
        'word_boundary_analysis': boundary_analysis,
        'unexpected_overlaps': [
            {
                'landmark_name': issue['landmark']['name'],
                'conflicting_tours': issue['conflicting_tours'],
                'keywords_matched': issue['keywords_matched']
            }
            for issue in overlap_issues
        ]
    }

    with open('Data/validation_issues.json', 'w') as f:
        json.dump(output, f, indent=2)

    print("💾 Report saved to Data/validation_issues.json")


def main():
    """Main validation routine."""
    import argparse

    parser = argparse.ArgumentParser(description='Validate tour categorization quality')
    parser.add_argument('--tour', help='Validate specific tour type only')
    parser.add_argument('--verbose', action='store_true', help='Show detailed output')
    args = parser.parse_args()

    print("=" * 70)
    print("TOUR CATEGORY VALIDATION TOOL")
    print("=" * 70)

    # Load landmarks
    print("\n📂 Loading landmarks...")
    all_landmarks = load_landmarks()
    print(f"   Loaded {len(all_landmarks)} landmarks")

    # Run validation checks
    substring_issues = detect_substring_matches(all_landmarks)
    temporal_issues = detect_temporal_mismatches(all_landmarks)
    boundary_analysis = analyze_word_boundaries(all_landmarks)
    overlap_issues = find_unexpected_overlaps(all_landmarks)

    # Generate report
    generate_report(
        substring_issues,
        temporal_issues,
        boundary_analysis,
        overlap_issues,
        verbose=args.verbose
    )

    # Save to file
    save_report_to_file(
        substring_issues,
        temporal_issues,
        boundary_analysis,
        overlap_issues
    )


if __name__ == "__main__":
    main()
