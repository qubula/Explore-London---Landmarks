# Alfie - London Tour Guide System Architecture

## Overview
An AI-powered audio tour guide that narrates London landmarks in the voice of a conversational London cabbie named "Alfie". The system combines multiple APIs to create 99 unique, naturally-spoken landmark descriptions.

---

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA COLLECTION PHASE                            │
└─────────────────────────────────────────────────────────────────────────┘

1. OpenStreetMap API
   └─> Downloaded 1000+ London landmarks with coordinates
       • Museums, palaces, bridges, monuments, parks
       • Geographic data (lat/lon)
       • Basic metadata

2. Wikipedia API
   └─> Enriched landmarks with historical context
       • First paragraph of Wikipedia articles
       • Historical dates and significance
       • Cultural context

3. Google Places API
   └─> Added visitor data and popularity metrics
       • User ratings (1-5 stars)
       • Number of reviews
       • Boost score (Google's internal popularity metric)
       • Used to rank "Top 100" landmarks

┌─────────────────────────────────────────────────────────────────────────┐
│                      CONTENT GENERATION PHASE                            │
└─────────────────────────────────────────────────────────────────────────┘

4. OpenAI GPT-4 API (Script Writing)
   └─> Generated conversational tour scripts
       • Input: Landmark name + Wikipedia context + location data
       • Prompt: 
              
"You are Alfie, a friendly London black cab driver.

Speak as if you’re chatting to a passenger in the cab. They may not know London well.

For the landmark below, say:

- 3–4 sentences of natural spoken English (around 60–80 words).
- First sentence: clearly say what the place is and roughly where it is in London. (This is important as you can't assume the passenger knows any context )
- - Whenever natural, start the sentence with "'The' + (landmark name)" instead of filler words like “Right,” or “Alright,”.
- Then give ONE surprising or less obvious detail that even many Londoners might not know.
  This could be a strange origin, a big change over time, a scandal, a legend, or an odd fact.
- Keep the tone warm, confident and a bit cheeky, but easy to understand for non-native speakers.
- A little British flavour is fine (“posh”, “bit of a glow-up”), but avoid heavy slang.
- Do not use stock phrases like “cheeky twist”, “funny thing is”, or “not bad, eh?”.
- End on a complete, satisfying thought, like something you’d say just as the cab drives past.

Landmark name: "{landmark_name}"

Source information:
\"\"\"{wiki_text[:2000]}\"\"\"

Now give ONE short spoken paragraph in Alfie’s voice (no bullet points, no headings)."
       • Output: 50-100 word conversational scripts
       • Tone: Informal, storytelling, with local character
       • Example: "Right, so Tower Bridge... built in the 1890s..."

   • Result: 1000+ unique scripts stored in final_landmarks_v6.2_Big.json

┌─────────────────────────────────────────────────────────────────────────┐
│                        VOICE DEVELOPMENT PHASE                           │
└─────────────────────────────────────────────────────────────────────────┘

5. Voice Testing & Refinement (ElevenLabs)

   Test 1: Pre-made Voices
   ├─> Tested "Adam" vs "George"
   └─> Selected George (more British, mature)

   Test 2: Fine-tuning (9 variations)
   ├─> Varied stability (0.30-0.40)
   ├─> Varied similarity boost (0.75-0.85)
   ├─> Varied style (0.50-0.70)
   └─> Selected: stability=0.35, similarity=0.80, style=0.60

   Test 3: Natural Storytelling (6 variations)
   └─> Problem: Voice sounded "read from script"
   └─> Solution: Added pauses, line breaks, ellipses
   └─> Lowered stability for variation

   Test 4: Ultra-Natural Mix (8 variations)
   └─> Combined low stability (0.20-0.30) with high style (0.70-0.82)
   └─> Goal: Varying speed, tone, and timing

   Test 5: Custom Voice Creation
   └─> Created "Alfie" - custom trained voice in ElevenLabs
       • Voice ID: LPRLepQnqpzvBlsHyfyS
       • Based on sample recordings
       • Tuned for London cabbie character

   FINAL SETTINGS:
   ├─> Voice: Custom "Alfie"
   ├─> Stability: 0.24 (lots of variation)
   ├─> Similarity Boost: 0.79 (maintains character)
   └─> Style: 0.76 (high expressiveness)

┌─────────────────────────────────────────────────────────────────────────┐
│                       AUDIO GENERATION PHASE                             │
└─────────────────────────────────────────────────────────────────────────┘

6. Script Enhancement (Python)
   └─> add_natural_pauses() function
       • Replaced ", and" with "... and" (thinking pauses)
       • Added line breaks between sentences
       • Paragraph breaks every 2-3 sentences
       • Result: More natural conversational flow

7. ElevenLabs TTS API (Audio Generation)
   └─> Generated 99 MP3 files (1 failed)
       • Model: eleven_turbo_v2_5
       • Format: MP3, mono, 22.05kHz, 64kbps
       • Average length: 26 seconds per landmark
       • Total: ~43 minutes of audio
       • Cost: ~$1.10 (100 scripts × 370 chars avg)

   Output: exhibition_audio/ folder
   ├─> 001_tower_bridge.mp3
   ├─> 002_buckingham_palace.mp3
   ├─> ...
   └─> 100_national_gallery.mp3

┌─────────────────────────────────────────────────────────────────────────┐
│                         AUDIO PROCESSING PHASE                           │
└─────────────────────────────────────────────────────────────────────────┘

8. FFmpeg Audio Concatenation
   └─> Combined 99 files with 8-second silence breaks
       • Created 8s silence MP3 file
       • Built concat filelist (audio → silence → audio...)
       • Generated exhibition_loop.mp3 (36 MB, 48:56 duration)
       • Re-encoded for compatibility: exhibition_loop_compatible.mp3 (45 MB)
       • Designed for infinite loop playback

┌─────────────────────────────────────────────────────────────────────────┐
│                        VISUALIZATION PHASE                               │
└─────────────────────────────────────────────────────────────────────────┘

9. Voice Visualizer (HTML5 Canvas + Web Audio API)
   └─> alfie_visualizer.html
       • Organic pulsating sphere reacting to voice
       • 12-point blob with Bezier curves for smoothness
       • Analyzes mid-range frequencies (speech)
       • Fast opening (35%), slow closing (15%) = mouth-like movement
       • Hidden progress bar for seeking/timeline control
       • Keyboard controls (Space = play/pause, Arrows = seek)
       • Black background with glowing blue gradient

   Technical Details:
   ├─> fftSize: 512 (high resolution for word detection)
   ├─> smoothingTimeConstant: 0.2 (snappy response)
   ├─> Size variation: baseRadius + audioLevel * 120
   └─> Particles spawn during high audio (audioLevel > 0.3)

┌─────────────────────────────────────────────────────────────────────────┐
│                          FINAL OUTPUT FILES                              │
└─────────────────────────────────────────────────────────────────────────┘

Core Files:
├─> Data/final_landmarks_v6.2_Big.json (500+ landmarks with scripts)
├─> App/generate_all_exhibition_audio.py (production generation script)
├─> App/exhibition_audio/ (99 individual MP3 files)
├─> App/exhibition_loop_compatible.mp3 (48-minute looping audio)
├─> App/alfie_visualizer.html (interactive voice visualizer)
└─> App/combine_with_ffmpeg.sh (audio concatenation script)

Archive:
└─> Archive - Voice Development/ (all test files and iterations)
```

---

## Key Technologies Used

| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| **OpenStreetMap API** | Landmark discovery | Free, comprehensive geographic data |
| **Wikipedia API** | Historical context | Rich, curated content for storytelling |
| **Google Places API** | Popularity ranking | Real visitor data for selecting "Top 100" |
| **OpenAI GPT-4** | Script generation | Natural language, context-aware writing |
| **ElevenLabs TTS** | Voice synthesis | Best quality, custom voices, fine-tuning |
| **FFmpeg** | Audio processing | Industry-standard, reliable concatenation |
| **Web Audio API** | Real-time analysis | Built-in browser API for frequency data |
| **Canvas 2D** | Visualization | Hardware-accelerated graphics |

---

## Data Flow Summary

```
OSM Data → Wikipedia Context → GPT-4 Scripts → ElevenLabs Voice → MP3 Files → Combined Loop
   ↓            ↓                   ↓               ↓                ↓            ↓
  500+        Added           Conversational    Custom "Alfie"    99 files   48-min loop
landmarks    history          cabbie tone         ultra-natural   @26s each  + visualizer
```

---

## Development Timeline

1. **Data Collection** (V1-V3): Gathered landmarks from OSM, Wikipedia, Google
2. **Script Generation** (V4-V6): Refined GPT-4 prompts for cabbie character
3. **Voice Testing** (Dec 10, 2024): 30+ voice variations tested
4. **Custom Voice** (Dec 10): Created "Alfie" in ElevenLabs
5. **Mass Generation** (Dec 10): Generated 99 landmark audio files
6. **Audio Processing** (Dec 10): Combined into exhibition loop
7. **Visualization** (Dec 10): Built interactive voice visualizer

---

## Landmark Selection & Scoring System

### Total Dataset
- **1,327 landmarks** with complete scripts
- All sourced from OpenStreetMap with Wikipedia enrichment
- 100% have GPT-4 generated conversational scripts
- Average script length: 370 characters (~65 words)
- Script range: 170-498 characters

### Scoring Algorithm

Landmarks are scored using a **two-tier system**:

#### 1. Category-Based Scores (from `App/landmarks.py`)

| Category | Score | Keywords | Examples |
|----------|-------|----------|----------|
| **Palaces/Castles** | +60 | "palace", "castle" | Buckingham Palace, Kensington Palace |
| **Major Churches** | +55 | "cathedral", "abbey", "minster", "basilica" | Westminster Abbey, St Paul's Cathedral |
| **Museums/Galleries** | +50 | "museum", "gallery", "library" | British Museum, National Gallery |
| **Monuments** | +35 | "statue", "memorial", "monument", "column" | Nelson's Column, Tower Hill Memorial |
| **Important Squares** | +35 | Trafalgar, Parliament, Leicester, Berkeley, Soho | Trafalgar Square |
| **Bridges/Towers** | +30 | "bridge", "tower", "wheel", "eye", "shard" | Tower Bridge, London Eye |
| **Parks/Gardens** | +25 | "park", "garden", "gardens" | Hyde Park, Kew Gardens |

#### 2. Popularity Boost Scores (from Google Places API)

Generated from real visitor data (238 API calls, $7.62, Dec 4 2025):

| Boost Range | Count | Examples |
|-------------|-------|----------|
| **50-56** (Top Tier) | 16 | Tower Bridge (56), British Museum (54), St Paul's (54) |
| **40-49** (Major) | 12 | Buckingham Palace (50), Trafalgar Square (51) |
| **30-39** (Important) | 8 | National Army Museum (37), Kew Palace (34) |
| **20-29** (Notable) | 22 | BT Tower (23), Garden Museum (19) |
| **10-19** (Minor) | 26 | Tower Hill Memorial (15), Brunel Museum (13) |
| **0-9** (Small) | 16 | Islington Museum (7), Fashion Museum (0) |

### Example Score Calculations

**Tower Bridge**: 30 (bridge) + 56 (popularity) = **86 points**
**British Museum**: 50 (museum) + 54 (popularity) = **104 points**
**Buckingham Palace**: 60 (palace) + 50 (popularity) = **110 points**
**Hyde Park**: 25 (park) + 0 (no boost) = **25 points**

### Grand Landmark Criteria

To be considered **"grand"** (for route planning), a landmark must:
1. Match grand keywords: museum, cathedral, palace, abbey, gallery, bridge, tower, square, buckingham, big ben, parliament, st paul, trafalgar
2. If it's a square: must be on Important Squares list (generic squares excluded)
3. Result: ~500-600 grand landmarks from 1,327 total

### Exhibition Audio Selection (Top 99)

For exhibition audio, simplified keyword scoring was used:

```python
boost_keywords = {
    "palace": 60, "museum": 50, "cathedral": 55, "abbey": 55,
    "tower": 40, "bridge": 35, "gallery": 50, "church": 30,
    "buckingham": 100, "big ben": 100, "tower of london": 90,
    "st paul": 80, "westminster": 75, "trafalgar": 70,
    "london eye": 65, "british museum": 90, "hyde park": 50,
    "national gallery": 80, "tate": 60, "royal": 45
}
```

**Selection Process**:
1. Filter landmarks with complete scripts (1,327 qualify)
2. Score based on keyword boosts (additive scoring)
3. Prioritize iconic landmarks (Buckingham: 160 pts, Big Ben: 100 pts)
4. Sort by score descending
5. Take top 100
6. Generate audio (1 failed → 99 total)

### Geographic Filtering (Route-Based Selection)

For route planning, landmarks are also filtered by proximity:

- **Default radius**: 600 meters from route
- **Optimization**: Bounding box pre-filter (filters ~90% before distance calculation)
- **Max landmarks per route**: 8 grand landmarks
- **Sorting**: By distance along route (not by score)

---

## Voice Naturalness Techniques

**Script Enhancement**:
- Line breaks after sentences → natural pauses
- Ellipses before conjunctions → thinking pauses
- Paragraph breaks every 2 sentences → breathing room

**Voice Settings**:
- **Low Stability (0.24)**: Varies pitch/speed/tone between words
- **High Similarity (0.79)**: Maintains Alfie's character
- **High Style (0.76)**: Adds emotional expressiveness

**Result**: Sounds like spontaneous storytelling, not reading a script

---

## Exhibition Use Cases

### 1. ESP32 Hardware Device (Original Plan)
- Upload exhibition_loop_compatible.mp3 to SD card
- Play on infinite loop with speaker
- Standalone audio installation

### 2. Laptop Presentation (Current)
- Open alfie_visualizer.html in browser
- Load exhibition_loop_compatible.mp3
- Visual + audio experience with timeline control
- Present to exhibition visitors

### 3. Future: GPS-Triggered Mobile App
- Store all 99 individual MP3 files
- Trigger playback when near landmark (20m radius)
- Real walking tour experience

---

## File Size & Performance

**Individual Files**:
- 99 files × ~200 KB = ~20 MB total
- Format: MP3, mono, 22.05kHz, 64kbps
- Average duration: 26 seconds

**Combined Loop**:
- exhibition_loop.mp3: 36 MB (concatenated)
- exhibition_loop_compatible.mp3: 45 MB (re-encoded)
- Duration: 48:56 (48 minutes 56 seconds)
- 99 landmarks + 98 × 8-second pauses

**Visualizer Performance**:
- 60 FPS animation loop
- Real-time FFT analysis (512 bins)
- Canvas size: Full screen (responsive)
- Memory usage: ~50 MB

---

## Cost Breakdown

| Service | Usage | Cost |
|---------|-------|------|
| OpenStreetMap API | 500+ queries | Free |
| Wikipedia API | 500+ queries | Free |
| Google Places API | ~$200 credit used | Free (trial) |
| OpenAI GPT-4 | 500 scripts × 300 tokens | ~$3.00 |
| ElevenLabs | Custom voice + 100 scripts | $5/month + $1.10 |
| **Total** | **Initial development** | **~$9.10** |

---

## Character Development: "Alfie"

**Personality**:
- London black cab driver
- Friendly, conversational, knowledgeable
- Uses informal language ("right, so...", "see that there...")
- Tells stories like a local, not a tour guide

**Voice Characteristics**:
- British accent (London)
- Male, mature (40s-50s)
- Warm, engaging tone
- Varying speed and pitch (natural speech)

**Example Script**:
```
"Right, so Tower Bridge... built in the 1890s, this one.
Took eight years to finish... and yeah, it still opens up
for tall ships. Pretty impressive engineering for back then,
if you ask me. The towers? Neo-Gothic style... very Victorian."
```

---

## Technical Challenges Solved

1. **Voice sounded scripted**
   - Solution: Added pauses, reduced stability, increased style

2. **Visualizer had angular artifacts**
   - Solution: Increased points to 12, used Bezier curves

3. **Sphere didn't react to words**
   - Solution: Higher FFT resolution, less smoothing, asymmetric response

4. **Progress bar too thin to grab**
   - Solution: Larger click area, scrubber handle, hover effects

5. **Old voice files mixed in**
   - Solution: Cleaned up folders, regenerated with consistent voice

6. **Playback stopping on loop**
   - Solution: Re-encoded with consistent parameters

---

## Future Enhancements

**Potential Features**:
- [ ] GPS-triggered mobile app with real-time playback
- [ ] User-selectable routes (historical, modern, royal, etc.)
- [ ] Multi-language support (translate scripts, new voices)
- [ ] Interactive map showing current landmark
- [ ] Voice customization (choose different characters)
- [ ] Offline mode with downloaded audio
- [ ] Integration with public transport routes

**Hardware Ideas**:
- [ ] ESP32 exhibition device with speaker
- [ ] Solar-powered outdoor installation
- [ ] Interactive kiosk with touchscreen map
- [ ] Bluetooth beacon triggers for proximity

---

## Project Structure

```
V4/
├── Data/
│   └── final_landmarks_v6.2_Big.json      # 500+ landmarks with scripts
├── App/
│   ├── generate_all_exhibition_audio.py   # Production generation script
│   ├── combine_with_ffmpeg.sh             # Audio concatenation
│   ├── alfie_visualizer.html              # Voice visualizer
│   ├── exhibition_audio/                  # 99 individual MP3 files
│   ├── exhibition_loop.mp3                # Combined loop (36 MB)
│   ├── exhibition_loop_compatible.mp3     # Re-encoded (45 MB)
│   └── Archive - Voice Development/       # All test iterations
│       ├── Voice Test Results/
│       ├── Old Test Scripts/
│       └── README.md
└── SYSTEM_ARCHITECTURE.md                 # This file
```

---

## Credits

**Data Sources**:
- OpenStreetMap contributors
- Wikipedia editors
- Google Places user reviews

**APIs & Services**:
- OpenAI (GPT-4 for script generation)
- ElevenLabs (custom voice synthesis)
- Google Maps Platform (Places API)

**Development**:
- Concept & Voice Development: Kuba Jarzebski
- Technical Implementation: Claude (Anthropic)
- Voice Character: "Alfie" (custom ElevenLabs voice)

---

## License & Usage

**Data**: OpenStreetMap data © OpenStreetMap contributors (ODbL)
**Scripts**: GPT-4 generated content (check OpenAI terms)
**Voice**: Custom ElevenLabs voice (personal use, check terms for commercial)
**Code**: Available for educational/portfolio use

---

## Development Log

### December 11, 2024 - Themed Tour Types Feature

**Context & User Feedback:**
After deploying the initial version with 3 route modes (Fastest, Scenic Auto, Scenic Select), received user feedback requesting the ability to filter tours by theme. Users wanted focused experiences like "Architecture Tour" or "Historical Tour" rather than seeing all landmarks.

**Requirements Gathered:**
- 8 themed tour types: Architecture, Historical, Royal, Museums & Galleries, Parks & Gardens, Religious Heritage, Modern London, Victorian Era
- Strict filtering (only show matching landmarks)
- Quality control: 3-5 best landmarks per journey for themed tours
- Must work with ALL 3 existing route modes
- Extensible system for adding new tour types
- No manual tagging required (use existing 1,327 landmark database)

**Design Challenge:**
How to categorize 1,327 landmarks into themed tours without manual tagging?

**Solution Approach:**
Implemented keyword-based auto-categorization with two-tier scoring system:
1. **Base Score**: From existing `score_grand_landmark()` function (palaces=60, museums=50, etc.)
2. **Boost Score**: Tour-specific keyword bonuses (e.g., "Tower Bridge" gets +100 in Architecture Tour)
3. **Minimum Thresholds**: Each tour type has min_score requirement (20-40) for quality control
4. **Exclude Keywords**: Prevent false matches (e.g., exclude "museum" from Architecture Tour)

**Implementation Steps:**

**Phase 1: Configuration & Categorization Engine (Created 3 new files)**

1. **Created App/tour_types.py** - Single source of truth
   - Defined 9 tour types (8 themed + "All Landmarks" default)
   - Each config contains:
     - `keywords`: List for matching landmark names/summaries
     - `exclude_keywords`: Filter out mismatches
     - `min_score`: Quality threshold (20-40)
     - `boost_keywords`: Dict of keyword→bonus points
     - `icon`, `color`, `description`: UI metadata

   Example for Architecture Tour:
   ```python
   "architecture": {
       "keywords": ["bridge", "tower", "building", "palace", "cathedral", ...],
       "exclude_keywords": ["museum", "gallery", "park"],
       "min_score": 30,
       "boost_keywords": {
           "tower bridge": 100,
           "st paul": 90,
           "big ben": 100
       }
   }
   ```

2. **Created App/categorize_landmarks.py** - Categorization engine
   - `categorize_landmark()`: Matches landmark against tour type keywords
     - Checks name + Wikipedia summary for keyword matches
     - Applies exclude keywords filter
     - Calculates base_score + boost_score
     - Returns (matches: bool, score: int)

   - `get_landmarks_for_tour_type()`: Filters entire dataset
     - Returns list of (landmark, score) tuples
     - Sorted by score descending (best matches first)
     - Special case: "all" tour type returns everything

   - `score_landmark_for_tour_type()`: Quick single-landmark scoring

3. **Created App/precompute_tour_categories.py** - One-time categorization script
   - Categorizes all 1,327 landmarks for all 8 tour types
   - Saves results to Data/tour_categories.json (112KB cache file)
   - Prints summary statistics and warnings

   **Run Results:**
   ```
   ✅ All 8 tour types have sufficient landmarks (76-199 each)
   📊 Total categorizations: 864

   Distribution:
   - Historical Tour: 199 landmarks (15.0%)
   - Parks & Gardens: 155 landmarks (11.7%)
   - Modern London: 94 landmarks (7.1%)
   - Victorian Era: 92 landmarks (6.9%)
   - Religious Heritage: 90 landmarks (6.8%)
   - Royal Tour: 79 landmarks (6.0%)
   - Museums & Galleries: 79 landmarks (6.0%)
   - Architecture Tour: 76 landmarks (5.7%)
   ```

**Phase 2: Backend Integration (Modified 3 core files)**

4. **Modified App/planner.py** - Added tour_type parameter throughout
   - Updated `limit_landmarks_by_duration()`:
     - For "all" tours: Dynamic calculation (0.5 landmarks/minute)
     - For themed tours: Fixed limits for quality control
       - <15 min: 3 landmarks max
       - 15-30 min: 4 landmarks max
       - >30 min: 5 landmarks max

   - Updated `scenic_auto_route()`: Pass tour_type to landmark filtering
   - Updated `scenic_select_route()`: Filter grand landmarks by tour type
   - Updated `extract_landmarks()`: Pre-filter by tour type before visibility check
     ```python
     if tour_type != "all":
         filtered = get_landmarks_for_tour_type(tour_type, all_landmarks)
         landmark_list = [lm[0] for lm in filtered]
     ```

   - Updated main `plan_route()` API:
     - Added `tour_type: str = "all"` parameter
     - Thread tour_type through all route mode branches
     - Include tour_type in return dict

5. **Modified App/landmarks.py** - Tour type support for grand landmarks
   - Updated `list_grand_landmarks(tour_type="all")`:
     - Filter by tour type BEFORE applying grand keyword filtering
     - Two-stage filtering: tour type → grand keywords

   - Updated `grand_landmarks_near_route(tour_type="all")`:
     - Used for Scenic Select landmark menu
     - Ensures menu only shows tour-type-matching landmarks

6. **Modified App/config.py** - Added tour type settings
   - `TOUR_TYPE_MAX_LANDMARKS`: Dict defining max landmarks per tour type
   - `TOUR_TYPE_COLORS`: UI colors for each tour type (for future map markers)

**Phase 3: UI Integration (Modified 3 interface files)**

7. **Modified templates/index.html** - Added tour type selector
   - Added dropdown selector with all 9 tour types
   - Positioned before route mode selection
   - Uses size="9" to show all options at once (no scrolling)
   - Preserved monospace font for consistency
   - Display selected tour type in route summary
   - Pass tour_type to live audio tour link

8. **Modified server.py** - FastAPI backend changes
   - Added `tour_type: str = Form("all")` parameter
   - Thread tour_type through all 3 route modes:
     - Mode 1 (Fastest): `plan_route(start, end, "1", tour_type=tour_type)`
     - Mode 2 (Scenic Auto): Same pattern
     - Mode 3 (Scenic Select): Filter grand landmarks by tour type
   - Updated `/track` endpoint to accept and use tour_type parameter

9. **Modified App/choose_route.py** - CLI interface
   - Added tour type selection menu at start:
     ```
     Choose Tour Type:
       1. 🗺️  All Landmarks
       2. 🏛️  Architecture Tour
       3. 📜 Historical Tour
       [...]
     ```
   - Parse user choice (1-9 or Enter for default)
   - Pass tour_type to all plan_route() calls
   - Display selected tour type in route summary

**Phase 4: Testing & Verification**

10. **Created test_tour_types.py** - Automated test script
    - Tests 4 tour types on same route (King's Cross → London Bridge)
    - Verifies filtering works correctly
    - Prints landmark counts and names for inspection

    **Test Results (26-minute route):**
    - All Landmarks: 12 landmarks
    - Architecture Tour: 3 landmarks (✅ strict filtering working)
      - Saint Nicholas Cole Abbey
      - Southwark Cathedral
      - London Bridge Experience
    - Historical Tour: 4 landmarks
    - Royal Tour: 1 landmark

    **Validation:** Themed tours showing 3-4 landmarks as intended (vs 12 for "all")

**Technical Achievements:**

1. **Zero Manual Tagging**: All 1,327 landmarks auto-categorized using keyword matching
2. **Performance**: Precomputed categories cached in JSON (instant filtering)
3. **Extensibility**: Adding new tour type = 3 steps:
   - Add definition to tour_types.py
   - Run precompute script
   - Add to UI dropdowns
4. **Backward Compatible**: "All Landmarks" preserves original behavior
5. **Quality Controlled**: Minimum score thresholds ensure only good matches

**Files Created:**
- App/tour_types.py (215 lines)
- App/categorize_landmarks.py (137 lines)
- App/precompute_tour_categories.py (122 lines)
- Data/tour_categories.json (112 KB, 864 categorizations)
- test_tour_types.py (68 lines)

**Files Modified:**
- App/planner.py: +80 lines (tour_type parameter threading)
- App/landmarks.py: +30 lines (tour type filtering)
- App/config.py: +32 lines (tour type settings)
- templates/index.html: +25 lines (dropdown selector)
- server.py: +15 lines (tour_type parameter handling)
- App/choose_route.py: +25 lines (CLI menu)

**Key Learnings:**

1. **Keyword-based categorization is sufficient**: Don't need ML/NLP for this use case
2. **Two-tier scoring works well**: Base score + boost score gives good quality control
3. **Precomputation prevents runtime overhead**: No performance impact from filtering
4. **Exclude keywords are critical**: Prevent false positives (e.g., "Natural History Museum" shouldn't match Architecture Tour)
5. **Fixed landmark limits for themed tours**: Better UX than dynamic calculation (users expect 3-5 focused landmarks, not 12)

**User Impact:**
- Users can now get curated experiences focused on their interests
- Reduces cognitive overload (3-5 relevant landmarks vs 12 mixed)
- Makes tours more educational (themed context vs random landmarks)
- Preserves flexibility (can still choose "All Landmarks" for classic experience)

**Next Steps for Future Enhancement:**
- Add tour type colors to map markers
- Allow multiple tour type selection (e.g., "Architecture + Historical")
- A/B test fixed limits vs percentage-based limits
- Add "Popular Tours" section showing most-selected tour types
- Consider adding more niche tour types (Literary London, Film Locations, etc.)

---

*Generated: December 11, 2024*
*Project: London Tour Guide - Alfie*
*Version: V4 (Exhibition Ready)*
*Last Updated: December 11, 2024 - Tour Types Feature*
