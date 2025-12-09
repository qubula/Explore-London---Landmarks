"""
Landmark helpers for the Alfie route picker:
- scoring "grand" landmarks
- filtering to grand landmarks
- finding grand landmarks near a route
"""

from App.route_landmark_finder import (
    landmarks,
    get_visibility_radius,
    closest_route_point_index,
)
from App.config import (
    IMPORTANT_SQUARES,
    MAX_GRAND_MENU_ITEMS,
    GRAND_LANDMARK_RADIUS_M,
    BIG_NAME_BOOST,
)


# -------------------------------------
# 1. Scoring for “Grand Landmarks”
# -------------------------------------
def score_grand_landmark(lm):
    """
    Return a numeric importance score for a landmark.
    Higher = more “grand” / iconic.
    """
    name = lm.get("name", "") or ""
    lower = name.lower()

    score = 0

    # --- 1. Category-based scores ---

    # Palaces / castles
    if "palace" in lower or "castle" in lower:
        score += 60

    # Major churches: cathedral / abbey / minster
    if any(k in lower for k in ("cathedral", "abbey", "minster", "basilica")):
        score += 55

    # Museums, galleries, libraries
    if any(k in lower for k in ("museum", "gallery", "library")):
        score += 50

    # Major monuments / statues
    if any(k in lower for k in ("statue", "memorial", "monument", "column")):
        score += 35

    # Bridges / towers / wheels
    if any(k in lower for k in ("bridge", "tower", "wheel", "eye", "shard")):
        score += 30

    # Parks and gardens
    if any(k in lower for k in (" park", "park ", " garden", " gardens")):
        score += 25

    # Squares — use IMPORTANT_SQUARES from config
    if "square" in lower:
        if lower.strip() in IMPORTANT_SQUARES:
            score += 35
        else:
            score += 5    # minor bump for generic squares

    # --- 2. Big-name boost (popular landmarks from Google Places API) ---
    for key, bonus in BIG_NAME_BOOST.items():
        if key in lower:
            score += bonus

    # --- 3. Fallback ---
    if score == 0 and len(name) > 0:
        score = 5

    return score


# -------------------------------------
# 2. List all GRAND landmarks in the DB
# -------------------------------------
def list_grand_landmarks():
    """
    These are big, iconic landmarks that are worth detouring for.
    We detect them based on keywords in their names.
    """
    grand_keywords = [
        "museum",
        "cathedral",
        "palace",
        "abbey",
        "gallery",
        "bridge",
        "tower",
        "square",
        "buckingham",
        "big ben",
        "parliament",
        "st paul",
        "trafalgar",
    ]

    important_squares_lower = [s.lower() for s in IMPORTANT_SQUARES]

    grand = []
    for lm in landmarks():  # Lazy load landmarks
        raw_name = lm.get("name", "")
        name = raw_name.lower()

        # Only consider things that match our "grand" keywords
        if not any(k in name for k in grand_keywords):
            continue

        # If it's a square, only keep it if it's on our important list
        if "square" in name and name not in important_squares_lower:
            continue

        grand.append(lm)

    # sort by importance (highest score first), then name
    grand.sort(key=lambda x: (-score_grand_landmark(x), x["name"]))

    return grand


# -------------------------------------
# 3. Grand landmarks near a specific route
# -------------------------------------
def get_route_bounds(route_points, buffer_km=1.0):
    """
    Get min/max lat/lon bounding box for a route with buffer.

    Args:
        route_points: List of (lat, lon) tuples
        buffer_km: Buffer distance in kilometers beyond route bounds

    Returns:
        Dictionary with min_lat, max_lat, min_lon, max_lon
    """
    lats = [p[0] for p in route_points]
    lons = [p[1] for p in route_points]

    # At London's latitude (~51°N), 1 degree ≈ 111km for latitude
    # For longitude at 51°N: 1 degree ≈ 69km (cos(51°) × 111km)
    # So we use different conversion factors for lat/lon
    lat_buffer_deg = buffer_km / 111.0  # ~0.009 degrees per km
    lon_buffer_deg = buffer_km / 69.0   # ~0.014 degrees per km at London's latitude

    return {
        "min_lat": min(lats) - lat_buffer_deg,
        "max_lat": max(lats) + lat_buffer_deg,
        "min_lon": min(lons) - lon_buffer_deg,
        "max_lon": max(lons) + lon_buffer_deg,
    }


def grand_landmarks_near_route(
    route_points,
    max_items: int = MAX_GRAND_MENU_ITEMS,
    radius_m: float = GRAND_LANDMARK_RADIUS_M,
):
    """
    Returns up to `max_items` grand landmarks that lie within `radius_m`
    of the given route.

    OPTIMIZATION: Uses geographic bounds pre-filtering to avoid checking
    all landmarks. Only landmarks within 1km of route bounds are considered.
    """
    grand = list_grand_landmarks()

    # OPTIMIZATION: Calculate bounding box for quick filtering
    bounds = get_route_bounds(route_points, buffer_km=1.0)

    nearby = []
    for lm in grand:
        # Get landmark coordinates
        lat = lm.get("lat")
        lon = lm.get("lng") or lm.get("lon")

        if lat is None or lon is None:
            continue

        # OPTIMIZATION: Quick bounds check before expensive distance calculation
        # This filters out ~90% of landmarks immediately
        if not (bounds["min_lat"] <= lat <= bounds["max_lat"] and
                bounds["min_lon"] <= lon <= bounds["max_lon"]):
            continue

        # Now do the expensive distance calculation only for candidates
        idx, dist = closest_route_point_index(lm, route_points)
        if dist <= radius_m:
            nearby.append((idx, lm))

    # Sort by distance along route, not alphabetically
    nearby.sort(key=lambda pair: pair[0])

    # Only keep the landmark objects
    return [lm for _, lm in nearby[:max_items]]
