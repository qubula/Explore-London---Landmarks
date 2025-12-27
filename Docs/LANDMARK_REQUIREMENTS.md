# Landmark Creation Requirements

## Overview
This document explains how landmarks are determined, scored, filtered, and selected for the Alfie tour guide system.

---

## 1. Basic Landmark Requirements

### Minimum Data Required
Every landmark in the system must have:
- **Name**: Landmark identifier (e.g., "Tower Bridge")
- **Coordinates**: Latitude and longitude (lat/lng or lat/lon)
- **Script**: Conversational tour guide description (50-100 words)

### Optional but Valuable Data
- **Wikipedia context**: Historical information for script generation
- **Google Places data**: Ratings, reviews, boost scores
- **Address**: For user reference
- **Type**: Category (museum, palace, bridge, etc.)

---

## 2. Landmark Scoring System

Landmarks are scored based on **category** + **popularity boost** to determine their importance.

### Category-Based Scores (from `App/landmarks.py`)

Scores are additive - landmarks can match multiple categories:

| Category | Score | Keywords | Examples |
|----------|-------|----------|----------|
| **Palaces/Castles** | +60 | "palace", "castle" | Buckingham Palace, Kensington Palace |
| **Major Churches** | +55 | "cathedral", "abbey", "minster", "basilica" | Westminster Abbey, St Paul's Cathedral |
| **Museums/Galleries** | +50 | "museum", "gallery", "library" | British Museum, National Gallery |
| **Monuments** | +35 | "statue", "memorial", "monument", "column" | Nelson's Column, Tower Hill Memorial |
| **Important Squares** | +35 | Special list only | Trafalgar Square, Leicester Square |
| **Bridges/Towers** | +30 | "bridge", "tower", "wheel", "eye", "shard" | Tower Bridge, London Eye |
| **Parks/Gardens** | +25 | "park", "garden", "gardens" | Hyde Park, Kew Gardens |
| **Generic Squares** | +5 | "square" (not on important list) | Minor squares |
| **Fallback** | +5 | Any landmark with a name | Generic landmarks |

### Popularity Boost Scores (from `App/config.py`)

Generated from **Google Places API** data (Dec 4, 2025 - 238 API calls, $7.62 cost)

Based on real visitor ratings and review counts:

| Boost Range | Number of Landmarks | Examples |
|-------------|---------------------|----------|
| **50-56** (Top Tier) | 16 landmarks | Tower Bridge (56), British Museum (54), St Paul's (54) |
| **40-49** (Major) | 12 landmarks | Buckingham Palace (50), Trafalgar Square (51) |
| **30-39** (Important) | 8 landmarks | National Army Museum (37), Kew Palace (34) |
| **20-29** (Notable) | 22 landmarks | BT Tower (23), Garden Museum (19) |
| **10-19** (Minor) | 26 landmarks | Tower Hill Memorial (15), Brunel Museum (13) |
| **0-9** (Small) | 16 landmarks | Islington Museum (7), Fashion Museum (0) |

**Total landmarks with boost scores**: 100 most popular from Google Places

---

## 3. Grand Landmark Criteria

Not all 1,327 landmarks are "grand" landmarks. To be considered **grand**, a landmark must:

### Keyword Matching (from `App/landmarks.py:87-101`)

Must contain at least ONE of these keywords:
- "museum"
- "cathedral"
- "palace"
- "abbey"
- "gallery"
- "bridge"
- "tower"
- "square"
- "buckingham"
- "big ben"
- "parliament"
- "st paul"
- "trafalgar"

### Square Exception Rule
If landmark contains "square", it MUST be on the **Important Squares List**:
- Trafalgar Square
- Parliament Square
- Leicester Square
- Berkeley Square
- Soho Square

*Generic squares are excluded from grand landmarks.*

---

## 4. Complete Scoring Examples

Let's see how real landmarks are scored:

### Example 1: Tower Bridge
```
Category Score:
  • "bridge" → +30
  • "tower" → +30 (but doesn't count twice - already +30 from bridge)

Popularity Boost:
  • "tower bridge" → +56 (Google Places boost)

TOTAL SCORE: 30 + 56 = 86 points
```

### Example 2: British Museum
```
Category Score:
  • "museum" → +50

Popularity Boost:
  • "british museum" → +54 (Google Places boost)

TOTAL SCORE: 50 + 54 = 104 points
```

### Example 3: Buckingham Palace
```
Category Score:
  • "palace" → +60

Popularity Boost:
  • "buckingham palace" → +50 (Google Places boost)

TOTAL SCORE: 60 + 50 = 110 points
```

### Example 4: Hyde Park
```
Category Score:
  • "park" → +25

Popularity Boost:
  • No boost score (not in top 100)

TOTAL SCORE: 25 points
```

### Example 5: Small Museum (e.g., Brunel Museum)
```
Category Score:
  • "museum" → +50

Popularity Boost:
  • "brunel museum" → +13 (Google Places boost)

TOTAL SCORE: 50 + 13 = 63 points
```

---

## 5. Landmark Selection for Exhibition Audio

For the **exhibition audio** (99 files generated), landmarks are selected using:

### Selection Algorithm (from `App/generate_all_exhibition_audio.py:78-98`)

```python
def score_landmark(lm):
    name = lm.get("name", "").lower()
    score = 0

    boost_keywords = {
        "palace": 60, "museum": 50, "cathedral": 55, "abbey": 55,
        "tower": 40, "bridge": 35, "gallery": 50, "church": 30,
        "buckingham": 100, "big ben": 100, "tower of london": 90,
        "st paul": 80, "westminster": 75, "trafalgar": 70,
        "london eye": 65, "british museum": 90, "hyde park": 50,
        "national gallery": 80, "tate": 60, "royal": 45
    }

    for keyword, points in boost_keywords.items():
        if keyword in name:
            score += points

    return score
```

### Steps:
1. **Filter**: Only landmarks with scripts (all 1,327 qualify)
2. **Score**: Apply keyword-based scoring
3. **Sort**: Highest score first
4. **Take**: Top 100 landmarks
5. **Generate**: Create audio with Alfie voice (1 failed → 99 total)

### Top Exhibition Landmarks (by keyword score)

| Landmark | Keywords Matched | Total Score |
|----------|------------------|-------------|
| Buckingham Palace | "buckingham" (100) + "palace" (60) | 160 |
| Big Ben | "big ben" (100) | 100 |
| Tower of London | "tower of london" (90) + "tower" (40) | 130 |
| British Museum | "british museum" (90) + "museum" (50) | 140 |
| St Paul's Cathedral | "st paul" (80) + "cathedral" (55) | 135 |
| Westminster Abbey | "westminster" (75) + "abbey" (55) | 130 |
| National Gallery | "national gallery" (80) + "gallery" (50) | 130 |
| Trafalgar Square | "trafalgar" (70) | 70 |
| Tower Bridge | "tower" (40) + "bridge" (35) | 75 |
| London Eye | "london eye" (65) | 65 |

---

## 6. Geographic Filtering

For **route-based landmark selection** (not exhibition), landmarks are also filtered by:

### Proximity Requirements (from `App/landmarks.py:157-198`)

- **Default radius**: 600 meters from route
- **Bounding box optimization**: Pre-filters landmarks within 1km of route bounds
  - Filters out ~90% of landmarks before expensive distance calculations
  - Uses lat/lon degree conversions:
    - Latitude: 1 degree ≈ 111 km
    - Longitude at London (51°N): 1 degree ≈ 69 km

### Route Landmark Selection Process:
1. Calculate route bounding box with 1km buffer
2. Quick bounds check: `min_lat ≤ lat ≤ max_lat` and `min_lon ≤ lon ≤ max_lon`
3. Expensive distance calculation only for candidates
4. Keep landmarks within 600m of route
5. Sort by distance along route (not score)
6. Return top 8 grand landmarks (`MAX_GRAND_MENU_ITEMS`)

---

## 7. Data Sources and Generation

### OpenStreetMap
- **Purpose**: Initial landmark discovery
- **Data**: 1000+ landmarks with coordinates
- **Filters**: Buildings, monuments, public structures in London

### Wikipedia API
- **Purpose**: Historical context for script generation
- **Data**: First paragraph of Wikipedia articles
- **Usage**: Provides facts for GPT-4 to write scripts

### Google Places API
- **Purpose**: Popularity ranking
- **Data**: User ratings, review counts, boost scores
- **Cost**: $7.62 for 238 API calls (Dec 4, 2025)
- **Result**: Top 100 popular landmarks identified

### OpenAI GPT-4 API
- **Purpose**: Script generation
- **Input**: Landmark name + Wikipedia context
- **Output**: 50-100 word conversational scripts
- **Character**: "Alfie" the London cabbie
- **Cost**: ~$3.00 for 1,327 scripts

### ElevenLabs TTS API
- **Purpose**: Voice synthesis
- **Voice**: Custom "Alfie" (ID: LPRLepQnqpzvBlsHyfyS)
- **Settings**: stability=0.24, similarity=0.79, style=0.76
- **Cost**: $1.10 for 99 audio files

---

## 8. Quality Requirements

### Script Requirements
All 1,327 landmarks have scripts that meet:
- **Length**: 170-498 characters (avg: 370)
- **Word count**: ~50-100 words
- **Duration**: ~26 seconds when spoken
- **Tone**: Conversational, warm, cheeky
- **Structure**:
  - First sentence: What it is + where it is
  - Middle: 1 surprising/less-obvious detail
  - End: Complete satisfying thought
- **Audience**: Non-native English speakers friendly
- **Voice**: Alfie the London cabbie character

### Audio Requirements (for generated files)
- **Format**: MP3
- **Channels**: Mono
- **Sample rate**: 22.05 kHz
- **Bitrate**: 64 kbps
- **Size**: ~200 KB per file
- **Quality**: Clear speech, natural pauses

---

## 9. Landmark Distribution

Out of **1,327 total landmarks**:

### By Category (estimated)
- Museums/Galleries: ~400 (30%)
- Churches/Cathedrals: ~250 (19%)
- Palaces/Historic Buildings: ~150 (11%)
- Parks/Gardens: ~200 (15%)
- Bridges/Towers: ~100 (8%)
- Monuments/Statues: ~150 (11%)
- Other: ~77 (6%)

### By Importance Level
- **Grand Landmarks**: ~500-600 (match grand keywords)
- **Exhibition-Ready (Top 99)**: 99 (highest keyword scores)
- **Route Landmarks**: All 1,327 (filtered by proximity at runtime)

---

## 10. Summary: Requirements Checklist

To be included in the Alfie tour guide system, a landmark must:

- [ ] **Have a name** (any landmark in London)
- [ ] **Have coordinates** (lat/lng from OpenStreetMap)
- [ ] **Have a script** (generated by GPT-4 from Wikipedia)
- [ ] **Meet minimum quality** (170+ characters, conversational tone)

To be a **Grand Landmark**:
- [ ] Contains grand keywords (museum, palace, cathedral, etc.)
- [ ] If square: must be on Important Squares list

To be in **Top 99 Exhibition Audio**:
- [ ] High keyword-based score (palace=60, museum=50, etc.)
- [ ] Iconic/popular name (Buckingham, Big Ben, Tower Bridge)
- [ ] Has complete script and audio generated successfully

To appear in **Route Planning**:
- [ ] Within 600m of route
- [ ] Matches grand landmark criteria
- [ ] In top 8 by distance along route

---

## 11. Future Considerations

### Potential Additions
- User-contributed landmarks
- Seasonal/temporary landmarks (exhibitions, events)
- Hidden gems (low scores but interesting)
- Themed routes (royal, dark history, modern, etc.)

### Potential Improvements
- Real-time Google Places API scoring (update boost scores)
- User ratings/favorites (personalized scoring)
- Time-based scoring (less crowded alternatives)
- Accessibility scoring (wheelchair access, etc.)

---

*Last Updated: December 11, 2024*
*Total Landmarks: 1,327*
*Grand Landmarks: ~500-600*
*Exhibition Audio: 99*
