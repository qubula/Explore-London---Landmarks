"""
Landmark Categorization Engine for Tour Types

This module provides functions to filter and score landmarks based on tour types.
Uses keyword matching against landmark names and Wikipedia summaries.
"""

import re

from App.tour_types import TOUR_TYPES, get_tour_type_config
from App.landmarks import score_grand_landmark


def extract_years(text):
    """Extract 4-digit years from text (1000-2099)."""
    years = re.findall(r'\b(1[0-9]{3}|20[0-9]{2})\b', text)
    return [int(y) for y in years]


def categorize_landmark(landmark, tour_type_config):
    """
    Determine if landmark matches a tour type based on keywords.

    Args:
        landmark: Landmark dict with 'name' and 'summary' fields
        tour_type_config: Tour type configuration dict from TOUR_TYPES

    Returns:
        tuple: (matches: bool, score: int)
               - matches: True if landmark matches tour type criteria
               - score: Combined base + boost score (0 if doesn't match)
    """
    name = landmark.get("name", "").lower()
    summary = landmark.get("summary", "").lower()
    combined_text = f"{name} {summary}"

    # Check if any keyword matches (with word boundaries)
    matches_keyword = any(
        re.search(r'\b' + re.escape(keyword) + r'\b', combined_text)
        for keyword in tour_type_config["keywords"]
    )

    # Check if any exclude keyword matches (with word boundaries)
    has_exclude = any(
        re.search(r'\b' + re.escape(keyword) + r'\b', combined_text)
        for keyword in tour_type_config["exclude_keywords"]
    )

    if has_exclude:
        return False, 0

    if not matches_keyword:
        return False, 0

    # Temporal validation for era-specific tours
    if tour_type_config.get("strict_dates"):
        era_range = tour_type_config.get("era_range")
        if era_range:
            years = extract_years(summary)
            # If we find dates that contradict the era, exclude
            for year in years:
                if year < era_range[0] or year > era_range[1]:
                    return False, 0  # Temporal mismatch - exclude

    # Calculate boost score
    base_score = score_grand_landmark(landmark)  # From existing system

    boost_score = 0
    for keyword, bonus in tour_type_config.get("boost_keywords", {}).items():
        # Use word boundaries for boost keywords too
        if re.search(r'\b' + re.escape(keyword) + r'\b', name):
            boost_score += bonus

    total_score = base_score + boost_score

    # Check minimum score threshold
    if total_score < tour_type_config["min_score"]:
        return False, 0

    return True, total_score


def get_landmarks_for_tour_type(tour_type: str, all_landmarks):
    """
    Filter and score landmarks for a specific tour type.

    Args:
        tour_type: Tour type key (e.g., "architecture", "historical")
        all_landmarks: List of all landmark dicts

    Returns:
        List of (landmark, score) tuples sorted by score descending
    """
    config = get_tour_type_config(tour_type)

    # Special case: "all" returns everything with existing scores
    if not config["keywords"]:
        return [(lm, score_grand_landmark(lm)) for lm in all_landmarks]

    # Filter and score
    matching = []
    for lm in all_landmarks:
        matches, score = categorize_landmark(lm, config)
        if matches:
            matching.append((lm, score))

    # Sort by score descending
    matching.sort(key=lambda x: x[1], reverse=True)

    return matching


def score_landmark_for_tour_type(landmark, tour_type: str):
    """
    Score a single landmark for a specific tour type.
    Convenience function for quick scoring without full filtering.

    Args:
        landmark: Landmark dict
        tour_type: Tour type key

    Returns:
        int: Score (0 if doesn't match tour type)
    """
    if tour_type == "all":
        return score_grand_landmark(landmark)

    config = get_tour_type_config(tour_type)
    matches, score = categorize_landmark(landmark, config)

    return score if matches else 0


def count_landmarks_by_tour_type(all_landmarks):
    """
    Count how many landmarks match each tour type.
    Useful for debugging and verification.

    Args:
        all_landmarks: List of all landmark dicts

    Returns:
        dict: {tour_type: count} for all tour types
    """
    counts = {}

    for tour_type in TOUR_TYPES.keys():
        if tour_type == "all":
            counts[tour_type] = len(all_landmarks)
            continue

        matching = get_landmarks_for_tour_type(tour_type, all_landmarks)
        counts[tour_type] = len(matching)

    return counts
