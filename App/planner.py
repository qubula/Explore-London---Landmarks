"""
planner.py

The core routing logic for the Alfie Tour Guide:
- fastest route
- scenic auto route
- scenic select route
- generating the final route summary

This file provides one clean API function:

    plan_route(start, end, mode, chosen_landmarks=None)

so that the CLI, GUI, or web interface can all use
the same internal logic.
"""

import requests
import polyline
import json
import os

from App.talking_points import get_tour_specific_script, load_talking_points
from App.tour_types import TOUR_TYPES

# Load talking points at module startup
load_talking_points()

# Load landmark images mapping
LANDMARK_IMAGES = {}
try:
    images_path = os.path.join(os.path.dirname(__file__), "..", "Data", "landmark_images.json")
    with open(images_path, "r", encoding="utf-8") as f:
        LANDMARK_IMAGES = json.load(f)
except FileNotFoundError:
    print("Warning: landmark_images.json not found, images will not be available")
except json.JSONDecodeError:
    print("Warning: landmark_images.json is invalid JSON")

def limit_landmarks_by_duration(
    landmarks: list,
    duration_min: float,
    max_per_minute: float = 0.5,
    tour_type: str = "all",
) -> list:
    """
    Thin down the list of landmarks so that we show at most
    `max_per_minute` landmarks per minute of route.

    For themed tours (tour_type != "all"), uses stricter fixed limits:
    - <15 min: 3 landmarks max
    - 15-30 min: 4 landmarks max
    - >30 min: 5 landmarks max

    For "all" tours, uses dynamic calculation (max_per_minute).

    We keep the most important landmarks (using score_grand_landmark)
    but preserve their order along the route.
    """
    if not landmarks or duration_min <= 0:
        return landmarks

    # Determine maximum count based on tour type
    if tour_type == "all":
        # Dynamic calculation for "all" tours
        max_count = max(1, int(duration_min * max_per_minute))
    else:
        # Fixed limits for themed tours (stricter quality control)
        if duration_min < 15:
            max_count = 3
        elif duration_min < 30:
            max_count = 4
        else:
            max_count = 5

    # Already under the limit? Nothing to do.
    if len(landmarks) <= max_count:
        return landmarks

    # Attach a score to each landmark (importance)
    scored = []
    for idx, lm in enumerate(landmarks):
        try:
            score = lm.get("score")
        except AttributeError:
            score = None

        if score is None:
            # Use our existing scoring logic from landmarks.py
            score = score_grand_landmark(lm)

        scored.append((score, idx, lm))

    # Sort by score descending (most important first)
    scored.sort(key=lambda x: x[0], reverse=True)

    # Pick the top N by importance…
    top = scored[:max_count]
    # …but return them in route order (by original index)
    top.sort(key=lambda x: x[1])

    return [lm for _, _, lm in top]

from App.route_landmark_finder import (
    landmarks,
    get_visibility_radius,
    closest_route_point_index,
    landmark_side_of_route,
    cluster_landmarks,
)

from App.landmarks import (
    score_grand_landmark,
    list_grand_landmarks,
    grand_landmarks_near_route,
)

from App.config import MAX_SCENIC_SELECT_CHOICES

import os
GOOGLE_API_KEY = os.getenv("GOOGLE_DIRECTIONS_KEY")


# -----------------------------------------------------
# 1. Basic Google route helpers
# -----------------------------------------------------
def get_route_and_duration(start: str, end: str):
    """Return (list_of_points, duration_seconds) for fastest route."""
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": start,
        "destination": end,
        "mode": "driving",
        "key": GOOGLE_API_KEY,
    }

    r = requests.get(url, params=params)
    data = r.json()

    if data.get("status") != "OK":
        raise RuntimeError(f"Google Directions error: {data.get('status')}")

    route = data["routes"][0]
    poly = route["overview_polyline"]["points"]
    points = polyline.decode(poly)
    duration_sec = route["legs"][0]["duration"]["value"]

    return points, duration_sec


def get_fastest_route(start: str, end: str):
    """Convenience wrapper returning ONLY the points."""
    pts, _ = get_route_and_duration(start, end)
    return pts


# -----------------------------------------------------
# 2. Scenic Auto – choose best alternative route
# -----------------------------------------------------
def scenic_auto_route(start: str, end: str, tour_type: str = "all"):
    """
    Evaluate Google's alternative routes and pick the one
    with the highest weighted grand-landmark visibility score.

    Also respects a maximum detour factor so we don't pick
    insanely long routes compared to the fastest option.

    Args:
        start: Starting location
        end: Ending location
        tour_type: Tour type filter (e.g., "architecture", "historical", "all")

    Returns: (best_points, fastest_sec, scenic_sec)
    """
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": start,
        "destination": end,
        "mode": "driving",
        "alternatives": "true",
        "key": GOOGLE_API_KEY,
    }

    r = requests.get(url, params=params)
    data = r.json()
    if data.get("status") != "OK":
        raise RuntimeError(f"Google Directions failed: {data.get('status')}")

    routes = data.get("routes", [])
    if not routes:
        raise RuntimeError("No routes returned from Google.")

    # Find the actual fastest option (by duration)
    fastest_sec = min(route["legs"][0]["duration"]["value"] for route in routes)

    # Get tour-type-specific detour allowance
    tour_config = TOUR_TYPES.get(tour_type, TOUR_TYPES["all"])
    max_detour_factor = tour_config.get("max_detour_factor", 1.4)
    max_detour_minutes = tour_config.get("max_detour_minutes", 3)

    # Calculate max allowed time with both factor and absolute limits
    max_by_factor = fastest_sec * max_detour_factor
    max_by_minutes = fastest_sec + (max_detour_minutes * 60)
    max_allowed_sec = min(max_by_factor, max_by_minutes)

    best_route_points = None
    best_scenic_sec = None
    best_score = -1

    grand = list_grand_landmarks(tour_type=tour_type)

    for route in routes:
        poly = route["overview_polyline"]["points"]
        pts = polyline.decode(poly)

        duration = route["legs"][0]["duration"]["value"]

        # Skip routes that exceed our detour cap
        if duration > max_allowed_sec:
            continue

        # Weighted scenic score
        score = 0
        for lm in grand:
            radius = get_visibility_radius(lm)
            idx, dist = closest_route_point_index(lm, pts)
            if dist <= radius:
                score += score_grand_landmark(lm)

        if score > best_score:
            best_score = score
            best_route_points = pts
            best_scenic_sec = duration

    # If no scenic route passed the detour cap, just use the fastest route
    if best_route_points is None:
        # Pick the actual fastest route from the API routes
        best_fastest_route = min(
            routes, key=lambda rt: rt["legs"][0]["duration"]["value"]
        )
        poly = best_fastest_route["overview_polyline"]["points"]
        best_route_points = polyline.decode(poly)
        best_scenic_sec = fastest_sec

    return best_route_points, fastest_sec, best_scenic_sec

# -----------------------------------------------------
# 3. Scenic Select – user-chosen grand landmarks
# -----------------------------------------------------
def scenic_select_route(start: str, end: str, chosen_landmarks, tour_type: str = "all"):
    """
    Build a scenic route:
        start → lm1 → lm2 → ... → end

    Args:
        start: Starting location
        end: Ending location
        chosen_landmarks: LIST OF LANDMARK DICTS selected by user
        tour_type: Tour type (used for metadata, routing is via chosen landmarks)

    Returns: (points, fastest_sec, scenic_sec)
    """
    # Baseline fastest duration
    _, fastest_sec = get_route_and_duration(start, end)

    all_points = []
    scenic_sec_total = 0
    last = start

    for lm in chosen_landmarks:
        mid = f"{lm['lat']},{lm['lng']}"
        leg_points, leg_sec = get_route_and_duration(last, mid)
        scenic_sec_total += leg_sec

        # Append, avoiding duplicate joints
        if all_points:
            all_points.extend(leg_points[1:])
        else:
            all_points.extend(leg_points)

        last = mid

    # Final leg
    final_points, final_sec = get_route_and_duration(last, end)
    scenic_sec_total += final_sec

    if all_points:
        all_points.extend(final_points[1:])
    else:
        all_points.extend(final_points)

    return all_points, fastest_sec, scenic_sec_total


# -----------------------------------------------------
# 4. Landmark extraction for any route
# -----------------------------------------------------
def extract_landmarks(route_points, tour_type: str = "all"):
    """
    Return all visible landmarks for a given polyline route.

    Args:
        route_points: List of (lat, lon) tuples defining the route
        tour_type: Tour type filter (e.g., "architecture", "historical", "all")

    Returns:
        List of landmark dicts with visibility and side information
    """
    from App.categorize_landmarks import get_landmarks_for_tour_type

    # Get filtered landmarks by tour type
    all_landmarks = list(landmarks())  # Lazy load all landmarks
    if tour_type != "all":
        filtered = get_landmarks_for_tour_type(tour_type, all_landmarks)
        landmark_list = [lm[0] for lm in filtered]  # Extract landmark objects
    else:
        landmark_list = all_landmarks

    visible = []

    for lm in landmark_list:
        radius = get_visibility_radius(lm)
        idx, dist = closest_route_point_index(lm, route_points)
        if dist <= radius:
            side = landmark_side_of_route(lm, route_points, idx)
            landmark_name = lm["name"]
            visible.append(
                {
                    "name": landmark_name,
                    "lat": lm["lat"],
                    "lng": lm["lng"],
                    "script": get_tour_specific_script(lm, tour_type),
                    "distance_m": dist,
                    "side": side,
                    "route_index": idx,
                    "radius_m": radius,
                    "image_url": LANDMARK_IMAGES.get(landmark_name),
                }
            )

    visible.sort(key=lambda l: l["route_index"])
    visible = cluster_landmarks(visible)

    # Filter out landmarks without tour-specific talking points
    # This ensures landmarks only appear on tours where they have relevant educational content
    if tour_type != "all":
        from App.talking_points import TALKING_POINTS_CACHE
        visible = [
            lm for lm in visible
            if lm["name"] in TALKING_POINTS_CACHE and
               (tour_type in TALKING_POINTS_CACHE[lm["name"]].get("talking_points", {}) or
                TALKING_POINTS_CACHE[lm["name"]].get("primary_tag") == tour_type)
        ]

    return visible


# -----------------------------------------------------
# 5. The main API: plan_route()
# -----------------------------------------------------

def plan_route(start: str, end: str, mode: str, chosen_landmark_indexes=None, tour_type: str = "all"):
    """
    The single clean API entry point.

    Args:
        start: Starting location (address or coords)
        end: Ending location (address or coords)
        mode: Route mode ("1"=fastest, "2"=scenic auto, "3"=scenic select)
        chosen_landmark_indexes: List of indexes for scenic select mode
        tour_type: Tour type filter (e.g., "architecture", "historical", "all")

    Returns:
        Structured dict for UI/CLI/GUI:
        {
            "mode": "...",
            "tour_type": "...",
            "fastest_eta": float_minutes,
            "chosen_eta": float_minutes,
            "difference": float_minutes,
            "landmarks": [...],
            "route_points": [...],
        }
    """

    # Always compute baseline first
    baseline_points, baseline_fastest_sec = get_route_and_duration(start, end)

    # Fastest mode
    if mode == "1":
        route_points = baseline_points
        actual_sec = baseline_fastest_sec
        mode_name = "Fastest"

    # Scenic Auto
    elif mode == "2":
        scenic_points, _, scenic_sec = scenic_auto_route(start, end, tour_type=tour_type)
        route_points = scenic_points
        actual_sec = scenic_sec
        mode_name = "Scenic Auto"

    # Scenic Select
    elif mode == "3":
        # We expect chosen_landmark_indexes from the UI/CLI
        base_pts, _ = get_route_and_duration(start, end)
        all_grand = grand_landmarks_near_route(base_pts, tour_type=tour_type)

        chosen = [
            all_grand[i]
            for i in chosen_landmark_indexes
            if 0 <= i < len(all_grand)
        ]
        chosen = chosen[:MAX_SCENIC_SELECT_CHOICES]

        route_points, _, scenic_sec = scenic_select_route(start, end, chosen, tour_type=tour_type)
        actual_sec = scenic_sec
        mode_name = "Scenic Select"

    else:
        raise ValueError("Unknown mode")

    # Landmarks along chosen route (filtered by tour type)
    lm_results = extract_landmarks(route_points, tour_type=tour_type)

    # Final times in minutes
    fastest_min = baseline_fastest_sec / 60.0
    actual_min = actual_sec / 60.0
    diff_min = actual_min - fastest_min

    # Limit landmark density based on route duration and tour type
    lm_results = limit_landmarks_by_duration(lm_results, actual_min, tour_type=tour_type)

    return {
        "mode": mode_name,
        "tour_type": tour_type,
        "fastest_eta": fastest_min,
        "chosen_eta": actual_min,
        "difference": diff_min,
        "landmarks": lm_results,
        "route_points": route_points,
    }
