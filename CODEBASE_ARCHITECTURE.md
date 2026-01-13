# PassingBy Codebase Architecture Diagram

## Complete File Structure & Purposes

Copy this diagram into [Mermaid Live Editor](https://mermaid.live/) to visualize.

---

%%{init: {'theme':'base','themeVariables':{'fontFamily':'IBM Plex Mono, monospace','fontSize':'16px','primaryTextColor':'#000000'}}}%%
graph TB
    subgraph Production["PRODUCTION SERVER"]
        SERVER[server.py<br/>FastAPI web server<br/>Routes + API endpoints]
    end

    subgraph Core["CORE ROUTING ENGINE"]
        PLANNER[planner.py<br/>Main route planning logic<br/>3 modes: Fastest/Scenic/Select]
        LANDMARKS[landmarks.py<br/>Scoring & filtering<br/>Grand landmark selection]
        ROUTE_FINDER[route_landmark_finder.py<br/>Find landmarks near route<br/>Distance calculations]
    end

    subgraph Config["CONFIGURATION"]
        CONFIG[config.py<br/>App settings & constants<br/>API keys, thresholds]
        TOUR_TYPES[tour_types.py<br/>Tour type definitions<br/>9 themes with keywords]
    end

    subgraph DataGeneration["DATA GENERATION SCRIPTS"]
        BUILD[build_landmarks_v3.py<br/>Scrape OSM + Wikipedia<br/>Create landmark database]
        CATEGORIZE[categorize_landmarks.py<br/>Tag landmarks by category<br/>Palace, Museum, etc.]
        PRECOMPUTE[precompute_tour_categories.py<br/>Pre-filter landmarks<br/>By tour type]
        LLM_TAGGER[llm_tagger.py<br/>GPT-4 content generation<br/>Tour-specific scripts]
        TALKING_POINTS[talking_points.py<br/>Load AI-generated scripts<br/>Landmark narration]
        GENERATE_BIG[generate_big_names.py<br/>Identify iconic landmarks<br/>Scoring boost list]
        SCRAPE_IMAGES[scrape_landmark_images.py<br/>Fetch images from APIs<br/>Pexels + Unsplash]
    end

    subgraph Frontend["MOBILE WEB APP - HTML"]
        INDEX[index.html<br/>Landing page<br/>Start location input]
        DESTINATION[destination.html<br/>Destination page<br/>End location input]
        ROUTE_MODE[route_mode.html<br/>Mode selection<br/>Fastest vs Scenic]
        TOUR_TYPE_PAGE[tour_type.html<br/>Tour type selector<br/>9 themed options]
        TOUR_PAGE[tour.html<br/>Active tour page<br/>Map + GPS + Cards]
    end

    subgraph JavaScript["JAVASCRIPT LOGIC"]
        TOUR_LOGIC[tour_logic.js<br/>GPS tracking loop<br/>Landmark detection]
        TOUR_SELECTION[tour_selection.js<br/>Tour type API calls<br/>Availability check]
    end

    %% Production connections
    SERVER --> PLANNER
    SERVER --> LANDMARKS
    SERVER --> CONFIG
    SERVER --> TOUR_TYPES
    SERVER --> INDEX
    SERVER --> DESTINATION
    SERVER --> ROUTE_MODE
    SERVER --> TOUR_TYPE_PAGE
    SERVER --> TOUR_PAGE

    %% Core engine connections
    PLANNER --> LANDMARKS
    PLANNER --> ROUTE_FINDER
    PLANNER --> TOUR_TYPES
    PLANNER --> TALKING_POINTS
    LANDMARKS --> ROUTE_FINDER
    LANDMARKS --> CONFIG

    %% Frontend connections
    INDEX --> DESTINATION
    DESTINATION --> ROUTE_MODE
    ROUTE_MODE --> TOUR_TYPE_PAGE
    TOUR_TYPE_PAGE --> TOUR_PAGE
    TOUR_PAGE --> TOUR_LOGIC
    TOUR_TYPE_PAGE --> TOUR_SELECTION

    %% Data generation flow
    BUILD --> CATEGORIZE
    CATEGORIZE --> PRECOMPUTE
    PRECOMPUTE --> TOUR_TYPES
    LLM_TAGGER --> TALKING_POINTS
    GENERATE_BIG --> LANDMARKS
    SCRAPE_IMAGES --> TOUR_PAGE

    %% Styling
    style SERVER fill:#000,stroke:#000,stroke-width:3px,color:#FFF
    style PLANNER fill:#000,stroke:#000,stroke-width:2px,color:#FFF
    style TOUR_PAGE fill:#000,stroke:#000,stroke-width:2px,color:#FFF

    style LANDMARKS fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style ROUTE_FINDER fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style CONFIG fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style TOUR_TYPES fill:#FFF,stroke:#000,stroke-width:2px,color:#000

    style BUILD fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style CATEGORIZE fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style PRECOMPUTE fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style LLM_TAGGER fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style TALKING_POINTS fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style GENERATE_BIG fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style SCRAPE_IMAGES fill:#FFF,stroke:#000,stroke-width:2px,color:#000

    style INDEX fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style DESTINATION fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style ROUTE_MODE fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style TOUR_TYPE_PAGE fill:#FFF,stroke:#000,stroke-width:2px,color:#000

    style TOUR_LOGIC fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style TOUR_SELECTION fill:#FFF,stroke:#000,stroke-width:2px,color:#000

---

## File Purpose Summary

### Production Server
| File | Purpose |
|------|---------|
| **server.py** | FastAPI web server - handles all HTTP routes, serves HTML pages, provides API endpoints for route planning and tour availability |

### Core Routing Engine
| File | Purpose |
|------|---------|
| **planner.py** | Main routing logic - implements 3 modes (Fastest, Scenic Auto, Scenic Select), calls Google Directions API, filters landmarks |
| **landmarks.py** | Landmark scoring & filtering - calculates "grand" scores, ranks landmarks by importance, selects top N for scenic routes |
| **route_landmark_finder.py** | Proximity detection - finds landmarks within radius of route, calculates distances using Haversine formula |

### Configuration
| File | Purpose |
|------|---------|
| **config.py** | App-wide settings - API keys, radius thresholds, score minimums, visibility distances |
| **tour_types.py** | Tour type definitions - 9 themes (Architecture, Historical, Royal, etc.) with keywords, icons, descriptions |

### Data Generation Scripts (Run Once)
| File | Purpose |
|------|---------|
| **build_landmarks_v3.py** | Scrapes OpenStreetMap + Wikipedia - creates initial landmark database (1,327 POIs) |
| **categorize_landmarks.py** | Tags landmarks by type - Palace, Cathedral, Museum, Bridge, Park, etc. |
| **precompute_tour_categories.py** | Pre-filters landmarks - creates tour-specific subsets, speeds up runtime queries |
| **llm_tagger.py** | GPT-4 script generation - creates conversational 60-80 word narration for each landmark |
| **talking_points.py** | Script loader - loads AI-generated talking points, serves them to tour pages |
| **generate_big_names.py** | Identifies iconic landmarks - creates boost list (Tower of London, Big Ben, etc.) |
| **scrape_landmark_images.py** | Fetches landmark photos - queries Pexels & Unsplash APIs, saves image URLs |
| **generate_all_exhibition_audio.py** | TTS audio generation - converts scripts to speech using ElevenLabs API (planned feature) |

### Mobile Web App - HTML Pages
| File | Purpose |
|------|---------|
| **index.html** | Landing page - welcome screen, start location autocomplete |
| **destination.html** | Destination page - end location autocomplete, route preview |
| **route_mode.html** | Mode selection - choose Fastest or Scenic route |
| **tour_type.html** | Tour type selector - 9 themed tour cards, availability checking |
| **tour.html** | Active tour page - Google Maps display, GPS tracking, landmark cards with 3D flip |

### JavaScript Frontend Logic
| File | Purpose |
|------|---------|
| **tour_logic.js** | GPS tracking loop - watches position every 3 seconds, detects proximity (120m), triggers landmark cards |
| **tour_selection.js** | Tour availability - calls `/api/check-tour-availability`, grays out unavailable tour types |

### Testing Scripts
| File | Purpose |
|------|---------|
| **test_waypoint_routing.py** | Tests route planning - validates Google Directions API waypoint optimization |
| **test_scenic_enhancement.py** | Tests scenic routing - verifies landmark selection logic, detour calculations |
| **validate_tour_categories.py** | Validates tour data - checks keyword coverage, ensures all categories have landmarks |

### Helper Tools (Development)
| File | Purpose |
|------|---------|
| **choose_route.py** | CLI route picker - command-line interface for testing route planning without web UI |
| **alfie_visualizer.html** | Map visualization - debugging tool to visualize landmark locations and coverage |

---

## Execution Flow

### User Journey (Production)
```
1. User opens app → index.html
2. Enters start location → destination.html
3. Chooses route mode → route_mode.html
4. Selects tour type → tour_type.html (calls /api/check-tour-availability)
5. Starts tour → tour.html (calls /api/plan-route)
6. GPS tracking begins → tour_logic.js (detects landmarks, shows cards)
```

### Data Pipeline (One-Time Setup)
```
1. build_landmarks_v3.py → Scrapes 1,327 landmarks
2. categorize_landmarks.py → Tags by type (Palace, Museum, etc.)
3. generate_big_names.py → Identifies 50 iconic landmarks
4. llm_tagger.py → Generates AI scripts for all landmarks
5. scrape_landmark_images.py → Fetches photos from APIs
6. precompute_tour_categories.py → Pre-filters by tour type
7. Data ready → server.py serves to users
```

### API Request Flow (Runtime)
```
User clicks "Start Tour"
  ↓
tour_type.html → /api/plan-route
  ↓
server.py → planner.py
  ↓
planner.py → Google Directions API (route)
  ↓
planner.py → landmarks.py (filter & score)
  ↓
landmarks.py → route_landmark_finder.py (proximity)
  ↓
planner.py → talking_points.py (load scripts)
  ↓
Response: {route, landmarks, polyline}
  ↓
tour.html displays map
  ↓
tour_logic.js starts GPS tracking
```

---

## Key Design Patterns

### Separation of Concerns
- **server.py**: HTTP layer only (routes, requests, responses)
- **planner.py**: Business logic (route optimization, mode selection)
- **landmarks.py**: Data layer (scoring, filtering, ranking)

### Configuration as Code
- **tour_types.py**: Single source of truth for all tour themes
- **config.py**: Centralized constants (no magic numbers in code)

### Build vs Runtime
- **Build scripts** (run once): Generate landmark database, AI scripts, images
- **Runtime scripts** (run per request): Filter landmarks, plan routes, serve data

### Frontend State Management
- **localStorage**: Persists user selections across pages (start, end, mode, tour type)
- **sessionStorage**: Prevents reload loops, tracks error states
- **URL parameters**: Alternative state passing (legacy, mostly replaced)

---

## Technologies Used

### Backend
- **Python 3.14**: Core language
- **FastAPI**: Web framework
- **requests**: HTTP client for external APIs
- **polyline**: Google route encoding/decoding

### Frontend
- **Vanilla JavaScript**: No frameworks (lightweight, fast)
- **Google Maps JavaScript API**: Map display, markers, routing
- **Swiper.js**: Card carousel UI
- **CSS Grid + Flexbox**: Responsive layouts

### External APIs
- **Google Directions API**: Route calculation
- **Google Places API**: Autocomplete, location data
- **OpenStreetMap Overpass**: Landmark scraping
- **Wikipedia API**: Landmark descriptions
- **OpenAI GPT-4**: Script generation
- **Pexels + Unsplash**: Landmark images
- **ElevenLabs**: TTS audio (planned)

### Deployment
- **Railway.app**: Cloud hosting
- **GitHub**: Version control + auto-deploy
- **Environment variables**: API keys via .env file

---

## File Count Summary

- **Python scripts**: 15 files
- **HTML pages**: 5 files
- **JavaScript files**: 2 files
- **Config files**: 2 files
- **Test files**: 5 files
- **Total codebase**: ~30 files (excluding venv, tests, archive)

---

## How to Use This Diagram

1. Copy the Mermaid code above (from `%%{init:` to the last `style` line)
2. Paste into [Mermaid Live Editor](https://mermaid.live/)
3. Export as SVG or PNG for your portfolio presentation
4. Font will be IBM Plex Mono, black & white styling
