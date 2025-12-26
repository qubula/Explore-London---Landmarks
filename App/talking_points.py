"""
Dynamic Tour-Specific Script Selection

Selects appropriate landmark scripts based on tour type using LLM-generated talking points.
"""

import json
from pathlib import Path
from typing import Dict, Optional

# Global cache for talking points (loaded at startup)
TALKING_POINTS_CACHE: Dict[str, Dict] = {}


def load_talking_points():
    """Load LLM-generated talking points from Data/landmark_tags.json"""
    global TALKING_POINTS_CACHE

    tags_file = Path("Data/landmark_tags.json")

    if not tags_file.exists():
        print("⚠️  Warning: Data/landmark_tags.json not found. Using fallback scripts.")
        return

    try:
        with open(tags_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            TALKING_POINTS_CACHE = data.get('tags', {})

        print(f"✅ Loaded talking points for {len(TALKING_POINTS_CACHE)} landmarks")

    except Exception as e:
        print(f"❌ Error loading talking points: {e}")
        TALKING_POINTS_CACHE = {}


def get_tour_specific_script(landmark: Dict, tour_type: str = "all") -> str:
    """
    Get tour-type-specific script for a landmark.

    Strategy:
    - For "all" tour type: Use generic script only
    - For themed tours: Prepend theme-specific talking point to generic script

    Priority for talking point selection:
    1. Talking point for the specific tour_type
    2. Talking point for the primary_tag
    3. No talking point (use generic script only)

    Args:
        landmark: Landmark dict with 'name' and 'script' fields
        tour_type: Tour type key (e.g., "architecture", "victorian")

    Returns:
        str: Theme-specific talking point + generic script, or just generic script
    """
    name = landmark.get("name", "")
    generic_script = landmark.get("script", "")

    # If tour_type is "all", use generic script only
    if tour_type == "all":
        return generic_script

    # Check if talking points exist for this landmark
    if name not in TALKING_POINTS_CACHE:
        return generic_script

    landmark_data = TALKING_POINTS_CACHE[name]
    talking_points = landmark_data.get("talking_points", {})

    talking_point = None

    # Priority 1: Tour-specific talking point
    if tour_type in talking_points:
        talking_point = talking_points[tour_type]
    # Priority 2: Primary tag talking point
    elif landmark_data.get("primary_tag") in talking_points:
        talking_point = talking_points[landmark_data.get("primary_tag")]

    # If we have a talking point, prepend it to the generic script
    if talking_point:
        return f"{talking_point} {generic_script}"

    # Priority 3: Fallback to generic script only
    return generic_script


def get_talking_point_coverage_stats() -> Dict:
    """
    Get statistics about talking point coverage.
    Useful for debugging and validation.

    Returns:
        Dict with coverage statistics
    """
    if not TALKING_POINTS_CACHE:
        return {"error": "No talking points loaded"}

    total_landmarks = len(TALKING_POINTS_CACHE)

    # Count talking points per tour type
    tour_type_coverage = {}
    tour_types = ["architecture", "historical", "royal", "museums_galleries",
                  "parks_gardens", "religious", "modern", "victorian"]

    for tour_type in tour_types:
        count = sum(
            1 for lm_data in TALKING_POINTS_CACHE.values()
            if tour_type in lm_data.get("talking_points", {})
        )
        tour_type_coverage[tour_type] = {
            "count": count,
            "percentage": round(count / total_landmarks * 100, 1)
        }

    return {
        "total_landmarks": total_landmarks,
        "coverage_by_tour_type": tour_type_coverage
    }
