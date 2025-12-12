"""
Tour Type Definitions for Alfie London Tour Guide

This is the SINGLE SOURCE OF TRUTH for all tour type configurations.
Each tour type defines:
- Keywords for matching landmarks
- Exclude keywords for filtering out mismatches
- Minimum score threshold
- Boost keywords for extra scoring
- UI metadata (icon, color, description)

To add a new tour type: Add a new entry to TOUR_TYPES dict and re-run
precompute_tour_categories.py
"""

TOUR_TYPES = {
    "all": {
        "name": "All Landmarks",
        "description": "Classic Alfie tour - all London landmarks",
        "icon": "🗺️",
        "keywords": [],  # Empty = match everything
        "exclude_keywords": [],
        "min_score": 30,  # Large pool (1327 landmarks) - high selectivity for quality
        "boost_keywords": {},
        "color": "#6B7280"
    },

    "architecture": {
        "name": "Architecture Tour",
        "description": "Iconic buildings, bridges, and architectural marvels",
        "icon": "🏛️",
        "keywords": [
            "bridge", "tower", "building", "palace", "cathedral", "church",
            "abbey", "basilica", "archway", "gate", "hall",
            "opera house", "railway station", "train station",
            "shard", "gherkin", "walkie talkie",
            "skyscraper", "monument", "dome", "spire", "clocktower",
            "estate", "housing estate", "modernist", "brutalist", "georgian", "tudor"
        ],
        "exclude_keywords": [
            "museum", "gallery",
            # Don't exclude "park" - too broad (excludes estates near parks)
            "theatre", "playhouse", "theater"  # Exclude performance venues
        ],
        "min_score": 10,  # Small pool (76 landmarks) - light filtering for quality
        "boost_keywords": {
            "tower bridge": 100,
            "st paul": 90,
            "westminster abbey": 85,
            "big ben": 100,
            "shard": 80,
            "elizabeth tower": 95,
            "gherkin": 75,
            "walkie talkie": 70,
            # Boost for housing estates and architectural styles
            "estate": 10,
            "housing": 5,
            "modernist": 10,
            "brutalist": 10,
            "georgian": 10,
            "tudor": 10
        },
        "color": "#EF4444"
    },

    "historical": {
        "name": "Historical Tour",
        "description": "Museums, monuments, and historical sites",
        "icon": "📜",
        "keywords": [
            "museum", "memorial", "monument", "castle", "fort", "tower",
            "historic", "heritage", "ancient", "historic building", "ancient site",
            "battle", "war memorial",
            "imperial", "national", "british", "london museum", "history",
            "churchill", "war rooms", "bunker"
        ],
        "exclude_keywords": [
            "modern architecture", "contemporary architecture",
            "theatre", "playhouse", "theater"  # Exclude performance venues
        ],
        "min_score": 15,  # Medium pool (200 landmarks) - moderate filtering for quality
        "boost_keywords": {
            "british museum": 100,
            "tower of london": 95,
            "imperial war museum": 80,
            "churchill war rooms": 75,
            "war memorial": 60,
            "monument": 55
        },
        "color": "#8B4513"
    },

    "royal": {
        "name": "Royal Tour",
        "description": "Palaces, royal parks, and ceremonial sites",
        "icon": "👑",
        "keywords": [
            "palace", "royal", "king", "queen", "crown", "throne",
            "buckingham", "kensington", "windsor", "hampton court",
            "st james", "clarence house", "royal mews", "guards",
            "ceremonial", "coronation", "monarch", "sovereign",
            "state", "majesty"
        ],
        "exclude_keywords": [
            "theatre", "playhouse", "theater"  # Exclude performance venues
        ],
        "min_score": 5,  # Small pool (57 landmarks) - minimal filtering to preserve options
        "boost_keywords": {
            "buckingham palace": 100,
            "kensington palace": 90,
            "st james's palace": 85,
            "tower of london": 80,
            "royal mews": 75,
            "royal albert hall": 70
        },
        "color": "#9333EA"
    },

    "museums_galleries": {
        "name": "Museums & Galleries",
        "description": "Art galleries, museums, and cultural institutions",
        "icon": "🎨",
        "keywords": [
            "museum", "gallery", "art", "exhibition", "collection",
            "tate", "national gallery", "victoria and albert", "v&a",
            "british museum", "science museum", "natural history",
            "portrait gallery", "courtauld", "saatchi", "whitechapel",
            "serpentine", "barbican"
        ],
        "exclude_keywords": [
            "memorial", "monument", "war",
            "theatre", "playhouse", "theater"  # Exclude performance venues
        ],
        "min_score": 10,  # Small pool (73 landmarks) - light filtering for quality
        "boost_keywords": {
            "british museum": 100,
            "national gallery": 95,
            "tate modern": 90,
            "victoria and albert": 90,
            "natural history museum": 85,
            "science museum": 80,
            "portrait gallery": 75
        },
        "color": "#06B6D4"
    },

    "parks_gardens": {
        "name": "Parks & Gardens",
        "description": "Green spaces, royal parks, and botanical gardens",
        "icon": "🌳",
        "keywords": [
            "park", "garden", "gardens", "green", "common", "heath",
            "hyde park", "regent", "kew", "richmond", "st james's park",
            "botanical", "arboretum", "nature reserve", "wood",
            "forest", "meadow"
        ],
        "exclude_keywords": [
            "museum", "palace", "bridge", "gallery",
            "theatre", "playhouse", "theater"  # Exclude performance venues
        ],
        "min_score": 0,  # Tiny pool (15 landmarks) - keywords only, no score threshold
        "boost_keywords": {
            "hyde park": 85,
            "kew gardens": 90,
            "regent's park": 80,
            "richmond park": 75,
            "st james's park": 70,
            "green park": 65
        },
        "color": "#10B981"
    },

    "religious": {
        "name": "Religious Heritage",
        "description": "Cathedrals, churches, abbeys, and religious sites",
        "icon": "⛪",
        "keywords": [
            "cathedral", "church", "abbey", "basilica",
            "chapel", "temple", "synagogue", "mosque", "monastery",
            "st paul", "westminster abbey", "southwark cathedral",
            "york minster", "beverly minster",  # Specific minsters only
            "religious", "holy", "sacred", "priest", "bishop"
        ],
        "exclude_keywords": [
            "museum",
            "theatre", "playhouse", "theater",  # Exclude performance venues
            "palace theatre", "victoria palace"  # Specific exclusions
        ],
        "min_score": 5,  # Small pool (37 landmarks) - minimal filtering to include smaller churches
        "boost_keywords": {
            "st paul's cathedral": 100,
            "westminster abbey": 100,
            "southwark cathedral": 70,
            "westminster cathedral": 65,
            "temple church": 60
        },
        "color": "#F59E0B"
    },

    "modern": {
        "name": "Modern London",
        "description": "Contemporary architecture and 21st century landmarks",
        "icon": "🏙️",
        "keywords": [
            "shard", "gherkin", "walkie talkie", "cheese grater",
            "canary wharf", "millennium", "london eye", "o2", "wembley",
            "modern architecture", "contemporary architecture",
            "2000s", "2010s", "2020s",
            "skyscraper", "high-rise"
        ],
        "exclude_keywords": [
            "victorian", "georgian", "medieval", "tudor", "19th century",
            "theatre", "playhouse", "theater"  # Exclude performance venues unless explicitly modern
        ],
        "min_score": 5,  # Small pool (41 landmarks) - minimal filtering to preserve modern sites
        "boost_keywords": {
            "the shard": 100,
            "london eye": 95,
            "millennium bridge": 80,
            "o2 arena": 70,
            "gherkin": 85,
            "canary wharf": 75
        },
        "era_range": (2000, 2100),
        "strict_dates": True,
        "color": "#3B82F6"
    },

    "victorian": {
        "name": "Victorian Era",
        "description": "19th century landmarks and Victorian architecture",
        "icon": "🎩",
        "keywords": [
            "victorian", "19th century", "1800s", "1850", "1860", "1870",
            "1880", "1890", "gothic revival", "tower bridge", "albert",
            "crystal palace", "railway", "railway station", "train station",
            "industrial", "iron", "steel", "brick"
        ],
        "exclude_keywords": [
            "modern architecture", "contemporary architecture",
            "theatre", "playhouse", "theater"  # Exclude performance venues unless explicitly Victorian
        ],
        "min_score": 5,  # Small pool (29 landmarks) - minimal filtering to preserve Victorian sites
        "boost_keywords": {
            "tower bridge": 95,
            "victoria and albert museum": 90,
            "natural history museum": 85,
            "royal albert hall": 80,
            "st pancras": 75,
            "paddington station": 70
        },
        "era_range": (1837, 1901),
        "strict_dates": True,
        "color": "#EC4899"
    }
}


def get_tour_type_config(tour_type: str):
    """
    Get configuration for a specific tour type.
    Returns 'all' config if tour_type not found.
    """
    return TOUR_TYPES.get(tour_type, TOUR_TYPES["all"])


def list_tour_types():
    """
    Get list of all available tour types.
    Returns list of (key, name, description, icon) tuples.
    """
    return [
        (key, config["name"], config["description"], config["icon"])
        for key, config in TOUR_TYPES.items()
    ]
