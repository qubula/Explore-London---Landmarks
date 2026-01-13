# Detailed Technical Diagrams - Self-Explanatory for External Reviewers

**Font**: IBM Plex Mono
**Colors**: Black & White only
**Approach**: Every component clearly labeled with its function

**Copy Instructions**: Copy from the diagram start (e.g., `graph TB`) to the end, WITHOUT the ```mermaid wrapper

---

## 1. System Architecture - Complete Data Flow

graph TB
    subgraph "User Interface Layer - Mobile Browser"
        A[Mobile Web Application<br/>Progressive Web App<br/>HTML5 + JavaScript]
        B[Real-time GPS Tracking<br/>Browser Geolocation API<br/>Updates every 3 seconds]
        C[Interactive Google Maps<br/>Displays route and markers<br/>Custom dark theme styling]
    end

    subgraph "Client-Side Logic - JavaScript"
        D[Location Input System<br/>Google Places Autocomplete<br/>Geocodes addresses to coordinates]
        E[Route Visualization Engine<br/>Renders walking path on map<br/>Decodes compressed polyline data]
        F[Landmark Card Interface<br/>3D flip animation cards<br/>Shows images and AI scripts]
    end

    subgraph "Backend API - Python FastAPI Server"
        G[Route Planning Endpoint<br/>/api/plan-route<br/>Receives start/end coordinates]
        H[Tour Availability Checker<br/>/api/check-tour-availability<br/>Filters landmarks by route]
        I[Route Optimization Algorithm<br/>Balances scenic value vs time<br/>Selects waypoints intelligently]
    end

    subgraph "External Services - Third Party APIs"
        J[Google Maps Directions API<br/>Calculates walking routes<br/>Returns compressed polyline]
        K[Google Places API<br/>Location search and geocoding<br/>Autocomplete suggestions]
        L[OpenAI GPT-4 API<br/>Generated landmark scripts<br/>Used offline for data prep]
    end

    subgraph "Data Storage - JSON Files"
        M[Landmark Database<br/>1,327 London POIs<br/>Coordinates, names, descriptions<br/>1.8MB JSON file]
        N[Tour Category Mappings<br/>Keyword-based filtering<br/>Architecture, Historical, etc.<br/>Precomputed cache]
        O[AI-Generated Scripts<br/>Tour-specific talking points<br/>60-80 word narratives<br/>1.2MB JSON file]
    end

    D --> K
    A --> B
    A --> G
    G --> I
    I --> J
    I --> M
    I --> N
    H --> M
    M --> O
    J --> E
    E --> C
    B --> F
    G --> A

    style A fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style G fill:#FFF,stroke:#000,stroke-width:3px,color:#000
    style M fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style J fill:#FFF,stroke:#000,stroke-width:2px,color:#000

---

## 2. User Journey - Complete Step-by-Step Flow

flowchart TD
    Start([User Opens App<br/>Landing Page Loads]) --> A[Step 1: Enter Start Location<br/>Uses Google Places Autocomplete<br/>or Current GPS Location]

    A --> B[Step 2: Enter Destination<br/>Searches London locations<br/>Saves to localStorage]

    B --> C[Step 3: Choose Route Mode<br/>Fastest: Direct route only<br/>Scenic: Adds landmark detours]

    C --> D{Is Scenic<br/>Mode Selected?}

    D -->|Yes - User wants landmarks| E[Step 4: Select Tour Theme<br/>Architecture, Historical, Royal<br/>9 themed options available]

    D -->|No - Fastest route only| F[Skip Tour Selection<br/>Default to All Landmarks<br/>Proceed to routing]

    E --> G[API Call: Check Availability<br/>Backend tests each tour type<br/>Counts available landmarks]

    G --> H[Gray Out Unavailable Tours<br/>Tours with ≤1 landmark disabled<br/>Shows No landmarks message]

    H --> I[User Confirms Tour Choice<br/>Saves selection to localStorage<br/>Proceeds to route planning]

    I --> J[API Call: Plan Route<br/>POST to /api/plan-route<br/>Sends start, end, mode, type]

    F --> J

    J --> K[Backend Processes Request<br/>Calls Google Directions API<br/>Applies optimization algorithm]

    K --> L[Response: Route Data<br/>Polyline: Compressed route path<br/>Landmarks: 3-5 curated POIs<br/>ETAs: Fastest vs chosen time]

    L --> M[Display Active Tour Map<br/>Render route polyline on map<br/>Add landmark markers<br/>Initialize landmark cards]

    M --> N[Start GPS Tracking Loop<br/>Request browser geolocation<br/>watchPosition every 3 seconds]

    N --> O[Update User Position<br/>Blue marker moves on map<br/>Calculate distance to landmarks]

    O --> P{User Within<br/>Landmark Radius?<br/>Default: 120 meters}

    P -->|Yes - Trigger proximity alert| Q[Display Landmark Card<br/>Flip card animation<br/>Show image and AI script<br/>Mark as visited]

    P -->|No - Keep tracking| O

    Q --> R{More Unvisited<br/>Landmarks Ahead?}

    R -->|Yes| O
    R -->|No| End([Journey Complete<br/>All landmarks visited<br/>Destination reached])

    style Start fill:#000,stroke:#000,stroke-width:2px,color:#FFF
    style D fill:#FFF,stroke:#000,stroke-width:3px,color:#000
    style J fill:#FFF,stroke:#000,stroke-width:3px,color:#000
    style P fill:#FFF,stroke:#000,stroke-width:3px,color:#000
    style End fill:#000,stroke:#000,stroke-width:2px,color:#FFF

---

## 3. Route Optimization - Three Algorithm Modes Explained

graph TB
    subgraph Mode1["MODE 1: FASTEST ROUTE - No Detours"]
        A1[Input: Start and End Coordinates] --> B1[Google Directions API Call<br/>Request: Walking directions<br/>Output: Direct A→B route]
        B1 --> C1[Extract Visible Landmarks<br/>Find POIs within 600m of route<br/>No route modification]
        C1 --> D1[Dynamic Filtering<br/>Limit to 0.5 landmarks per minute<br/>Quality control for journey length]
        D1 --> E1[Output: Fastest Route<br/>Same duration as Google Maps<br/>Some ambient landmarks visible]
    end

    subgraph Mode2["MODE 2: SCENIC AUTO - AI-Optimized Detours"]
        A2[Input: Start, End, Tour Type<br/>e.g., Architecture theme] --> B2[Step 1: Get Baseline Route<br/>Calculate fastest path first<br/>Establish time budget]

        B2 --> C2[Step 2: Find Grand Landmarks<br/>Search within 1km of route<br/>Filter by tour type keywords<br/>e.g., bridge, tower, palace]

        C2 --> D2[Step 3: Rank by Importance<br/>Score = Category + Popularity<br/>Palace: 60, Cathedral: 55, etc.<br/>Google Places boost: 0-56]

        D2 --> E2[Step 4: Select Top N Waypoints<br/>Choose 3-5 highest scored<br/>Fit within +10 min time budget<br/>Balance scenic value vs time]

        E2 --> F2[Step 5: Re-route with Waypoints<br/>Google Directions: A→LM1→LM2→LM3→B<br/>Optimize waypoint order for efficiency]

        F2 --> G2[Output: Optimized Scenic Route<br/>Adds ~5-10 minutes to journey<br/>Passes by top landmarks<br/>Curated experience]
    end

    subgraph Mode3["MODE 3: SCENIC SELECT - User-Customized Route"]
        A3[Input: Start and End] --> B3[Step 1: Find Nearby Landmarks<br/>Search grand landmarks near route<br/>Return top 8 by importance score]

        B3 --> C3[Step 2: Display Selection Menu<br/>User sees dropdown with 8 options<br/>Each shows name and description<br/>User picks up to 3 landmarks]

        C3 --> D3[Step 3: User Confirms Choices<br/>e.g., Tower Bridge, St Paul's, Tate<br/>Order preserved as selected]

        D3 --> E3[Step 4: Build Custom Route<br/>Google Directions with user waypoints<br/>A→User Choice 1→Choice 2→Choice 3→B]

        E3 --> F3[Output: Personalized Route<br/>Variable time added 5-20 min<br/>User controls experience<br/>Maximum flexibility]
    end

    style B1 fill:#FFF,stroke:#000,stroke-width:2px
    style F2 fill:#FFF,stroke:#000,stroke-width:3px
    style E3 fill:#FFF,stroke:#000,stroke-width:2px

---

## 4. Landmark Scoring Algorithm - Decision Tree

graph TD
    A[Input: Single Landmark<br/>Name, Category, Coordinates] --> B[Step 1: Identify Category<br/>Check landmark type from name<br/>palace, cathedral, museum, bridge, park]

    B --> C{Category<br/>Classification}

    C -->|Contains: palace, castle| D[Category Score: +60 points<br/>Highest tier for royal buildings<br/>e.g., Buckingham Palace]

    C -->|Contains: cathedral, abbey| E[Category Score: +55 points<br/>Major religious landmarks<br/>e.g., Westminster Abbey]

    C -->|Contains: museum, gallery| F[Category Score: +50 points<br/>Cultural institutions<br/>e.g., British Museum]

    C -->|Contains: monument, memorial| G[Category Score: +40 points<br/>Historical markers<br/>e.g., Nelson's Column]

    C -->|Contains: bridge| H[Category Score: +30 points<br/>Iconic river crossings<br/>e.g., Tower Bridge]

    C -->|Contains: park, garden| I[Category Score: +25 points<br/>Green spaces and squares<br/>e.g., Hyde Park]

    D --> J[Step 2: Apply Popularity Boost<br/>Check Google Places data<br/>Tourist attraction rating]
    E --> J
    F --> J
    G --> J
    H --> J
    I --> J

    J --> K{Is landmark in<br/>BIG_NAME_BOOST<br/>dictionary?<br/>120+ famous locations}

    K -->|Yes - Highly popular| L[Add Boost: +10 to +56 points<br/>Tower Bridge: +56<br/>British Museum: +54<br/>Westminster Abbey: +53]

    K -->|No - Standard landmark| M[Add Boost: +0 points<br/>Lesser-known POIs<br/>Local interest only]

    L --> N[Calculate Final Score<br/>Total = Category + Boost<br/>Range: 0-116 points]
    M --> N

    N --> O[Example Calculations:<br/>Buckingham Palace: 60+50=110<br/>Tower Bridge: 30+56=86<br/>Small Church: 55+0=55]

    O --> P{Score ≥<br/>Minimum Threshold?<br/>Varies by tour type<br/>Usually 30-50 points}

    P -->|Yes - Meets quality bar| Q[Include in Tour Database<br/>Added to available landmarks<br/>Visible to users]

    P -->|No - Too obscure| R[Exclude from Results<br/>Filtered out during planning<br/>Not shown to users]

    Q --> S[Output: Ranked Landmark<br/>Stored with final score<br/>Used for sorting and selection]
    R --> S

    style C fill:#FFF,stroke:#000,stroke-width:3px,color:#000
    style K fill:#FFF,stroke:#000,stroke-width:3px,color:#000
    style P fill:#FFF,stroke:#000,stroke-width:3px,color:#000
    style Q fill:#000,stroke:#000,stroke-width:2px,color:#FFF
    style R fill:#FFF,stroke:#000,stroke-width:2px,color:#000

---

## 5. Data Pipeline - From Collection to Production

graph LR
    subgraph "Stage 1: Raw Data Collection"
        A1[OpenStreetMap Overpass API<br/>Query: All POIs in London<br/>Returns: 2,000+ locations]
        A2[Wikipedia API<br/>Fetch: Description summaries<br/>~200 word excerpts per POI]
        A3[Google Places API<br/>Get: Popularity ratings<br/>Tourist attraction scores]
    end

    subgraph "Stage 2: Data Merging and Cleaning"
        B1[Merge Three Data Sources<br/>Match by name and coordinates<br/>Deduplicate entries]
        B1 --> B2[Quality Filter Application<br/>Remove: Closed venues, duplicates<br/>Result: 1,327 valid landmarks]
        B2 --> B3[Calculate Importance Scores<br/>Category scoring + popularity boost<br/>Range: 0-116 points per landmark]
        B3 --> B4[Classify Landmark Types<br/>Region: Large areas parks<br/>Building: Museums, palaces<br/>Object: Statues, plaques]
    end

    subgraph "Stage 3: AI Content Generation"
        C1[OpenAI GPT-4 API Batch Request<br/>Prompt: Write 60-80 word script<br/>Conversational tour guide style]
        C1 --> C2[Generate Base Scripts<br/>1,327 general descriptions<br/>Interesting facts and history]
        C2 --> C3[LLM Categorization Tagging<br/>Analyze each landmark content<br/>Assign: Architecture, Historical, etc.]
        C3 --> C4[Create Tour-Specific Scripts<br/>Generate themed talking points<br/>9 tour types × 1,327 landmarks]
    end

    subgraph "Stage 4: Database Files Creation"
        D1[Combine All Processed Data<br/>Merge coordinates, scores, scripts]
        D1 --> D2[final_landmarks_v6.2_Big.json<br/>Size: 1.8 MB<br/>Contains: All 1,327 POIs with data]
        D1 --> D3[landmark_tags.json<br/>Size: 1.2 MB<br/>Contains: Tour-specific scripts]
        D1 --> D4[tour_categories.json<br/>Size: 155 KB<br/>Contains: Precomputed type mappings]
    end

    subgraph "Stage 5: Deployment Pipeline"
        E1[Git Commit and Push<br/>Push to GitHub repository<br/>Trigger: Railway CI/CD webhook]
        E1 --> E2[Railway Auto-Deploy<br/>Detects new commit<br/>Rebuilds container image]
        E2 --> E3[FastAPI Server Start<br/>Lazy-load JSON files<br/>Initialize API endpoints]
        E3 --> E4[Live Production Application<br/>Accessible via public URL<br/>Serves user requests]
    end

    A1 --> B1
    A2 --> B1
    A3 --> B1
    B4 --> C1
    C4 --> D1
    D2 --> E1
    D3 --> E1
    D4 --> E1

    style A1 fill:#FFF,stroke:#000,stroke-width:2px
    style C1 fill:#FFF,stroke:#000,stroke-width:2px
    style D2 fill:#FFF,stroke:#000,stroke-width:3px
    style E4 fill:#000,stroke:#000,stroke-width:2px,color:#FFF

---

## 6. Real-Time GPS Tracking - Sequence Diagram

sequenceDiagram
    participant User as User Device<br/>Smartphone Browser
    participant App as Frontend JavaScript<br/>tour_logic.js
    participant GPS as Browser Geolocation API<br/>navigator.geolocation
    participant Map as Google Maps Display<br/>Interactive Map Component

    User->>App: Clicks Start Tour Button<br/>Loads /mobile/tour page
    App->>App: Parse Route Data from API<br/>Decode polyline coordinates
    App->>Map: Initialize Google Maps<br/>Set center, zoom, style
    App->>Map: Draw Route Polyline<br/>Render walking path in cream color
    App->>Map: Add Landmark Markers<br/>Place SVG pins at POI coordinates

    App->>GPS: Request Continuous Tracking<br/>watchPosition enableHighAccuracy:true
    GPS-->>User: Permission Dialog<br/>Allow PassingBy to access location?
    User-->>GPS: Grant Permission<br/>User clicks Allow

    loop GPS Update Loop - Every 3 Seconds
        GPS->>App: Position Update Callback<br/>Latitude, Longitude, Accuracy
        App->>App: Calculate Distance to Landmarks<br/>Haversine formula in meters
        App->>Map: Update Blue User Marker<br/>Animate to new position
        App->>Map: Center Map on User<br/>Keep user marker visible

        alt User Within Trigger Radius
            Note over App: Distance ≤ 120m<br/>Default proximity threshold
            App->>App: Mark Landmark as Visited<br/>Update visited[] array
            App->>Map: Animate to Landmark Card<br/>Swiper.js slideTo index
            App->>User: Display Card Content<br/>Show image, name, AI script
            App->>User: Update Status Badge<br/>You're here! notification
        else User Still Far from Landmark
            Note over App: Distance > 120m<br/>Not yet triggered
            App->>User: Update Distance Display<br/>Show: 500m away
            App->>Map: Keep Current View<br/>No card change
        end
    end

    User->>Map: Manually Taps Landmark Marker<br/>User clicks POI on map
    Map->>App: Marker Click Event<br/>Pass landmark index
    App->>App: Jump to Card Index<br/>Swiper.slideTo index
    App->>User: Show Selected Landmark<br/>Display that specific card

    User->>App: Reaches Final Destination<br/>Last landmark visited
    App->>App: Stop GPS Tracking<br/>clearWatch watchId
    App->>User: Journey Complete Screen<br/>Thank you message

---

## 7. Tour Type Filtering - Backend to Frontend Flow

graph TD
    subgraph "User Action"
        A[User Selects Route<br/>Start: King's Cross<br/>End: London Bridge<br/>Mode: Scenic]
    end

    subgraph "Frontend Request"
        A --> B[Read localStorage Data<br/>Keys: alfie_start, alfie_destination<br/>Parse JSON coordinates]
        B --> C[API POST Request<br/>Endpoint: /api/check-tour-availability<br/>Body: start, end, mode]
    end

    subgraph "Backend Processing Loop"
        C --> D[For Each of 9 Tour Types<br/>Architecture, Historical, Royal<br/>Museums, Parks, Religious<br/>Modern, Victorian, All]

        D --> E1[Test: Architecture Tour<br/>Filter by keywords<br/>bridge, tower, palace, cathedral]
        D --> E2[Test: Historical Tour<br/>Filter by keywords<br/>museum, memorial, monument, war]
        D --> E3[Test: Royal Tour<br/>Filter by keywords<br/>palace, royal, king, queen]
        D --> E4[Test: 6 Other Tour Types<br/>Similar keyword filtering<br/>for each theme]

        E1 --> F1[Call plan_route Function<br/>Mode: scenic, Type: architecture<br/>Calculate route with landmarks]
        E2 --> F2[Call plan_route Function<br/>Mode: scenic, Type: historical<br/>Calculate route with landmarks]
        E3 --> F3[Call plan_route Function<br/>Mode: scenic, Type: royal<br/>Calculate route with landmarks]
        E4 --> F4[Call plan_route for Others<br/>Test all remaining types]

        F1 --> G1{Count Landmarks<br/>on Architecture Route}
        F2 --> G2{Count Landmarks<br/>on Historical Route}
        F3 --> G3{Count Landmarks<br/>on Royal Route}
        F4 --> G4{Count for Other Routes}

        G1 -->|Found 5 landmarks| H1[Result: architecture = TRUE<br/>Sufficient POIs available]
        G1 -->|Found 0-1 landmarks| I1[Result: architecture = FALSE<br/>Insufficient for tour]

        G2 -->|Found 4 landmarks| H2[Result: historical = TRUE<br/>Sufficient POIs available]
        G2 -->|Found 1 landmark| I2[Result: historical = FALSE<br/>Insufficient for tour]

        G3 -->|Found 0 landmarks| I3[Result: royal = FALSE<br/>No POIs on this route]

        G4 --> H4[Results for Remaining Types<br/>TRUE or FALSE per type]
    end

    subgraph "API Response"
        H1 --> J[Build Availability Object<br/>architecture: true<br/>historical: true<br/>royal: false<br/>etc.]
        I1 --> J
        H2 --> J
        I2 --> J
        I3 --> J
        H4 --> J

        J --> K[Return JSON Response<br/>status: success<br/>availability: object]
    end

    subgraph "Frontend UI Update"
        K --> L[Receive Availability Data<br/>Parse JSON response]
        L --> M[Loop Through Tour Cards<br/>For each DOM element: .tour-card]

        M --> N{Check Availability<br/>for This Tour Type}

        N -->|availability = FALSE<br/>Insufficient landmarks| O[Apply Disabled Styles<br/>opacity: 0.4<br/>pointerEvents: none<br/>filter: grayscale 0.8]
        N -->|availability = TRUE<br/>Landmarks found| P[Keep Card Enabled<br/>Full opacity<br/>Clickable interaction<br/>Normal styling]

        O --> Q[Add Unavailable Message<br/>Replace tour-meta text<br/>Show: No landmarks on this route]
        P --> R[Keep Original Description<br/>Show normal tour description]

        Q --> S[Final UI State<br/>User sees available tours<br/>Grayed out unavailable ones]
        R --> S
    end

    style C fill:#FFF,stroke:#000,stroke-width:3px
    style G1 fill:#FFF,stroke:#000,stroke-width:3px
    style N fill:#FFF,stroke:#000,stroke-width:3px
    style P fill:#000,stroke:#000,stroke-width:2px,color:#FFF
    style O fill:#FFF,stroke:#000,stroke-width:2px

---

## 8. Performance Optimization - Problem to Solution

graph TB
    subgraph "Initial Problem"
        A[Slow Route Planning<br/>Load Time: 10-15 seconds<br/>User Experience: Poor<br/>Users abandon before loading]
    end

    subgraph "Optimization 1: Lazy Loading"
        B1[Problem: Loading 1.8MB JSON<br/>on every server start<br/>500ms overhead per request]
        B1 --> B2[Solution: Lazy Load Pattern<br/>Load landmarks only when first needed<br/>Cache in memory after first access]
        B2 --> B3[Result: Save 500ms<br/>per subsequent request<br/>First request slower, rest fast]
    end

    subgraph "Optimization 2: Bounding Box Pre-Filter"
        C1[Problem: Distance Calculation<br/>for all 1,327 landmarks<br/>CPU-intensive haversine formula]
        C1 --> C2[Solution: Geographic Bounding Box<br/>Get route min/max lat/lon<br/>Filter landmarks outside box first]
        C2 --> C3[Result: Eliminate 90%<br/>Only calculate ~130 landmarks<br/>10x faster processing]
    end

    subgraph "Optimization 3: Polyline Compression"
        D1[Problem: Large Route Data<br/>Raw coordinates: ~100KB JSON<br/>Slow transfer over network]
        D1 --> D2[Solution: Google Polyline Encoding<br/>Compress lat/lon array<br/>Lossy algorithm reduces size]
        D2 --> D3[Result: 50x Compression<br/>Route data: 100KB → 2KB<br/>Faster API responses]
    end

    subgraph "Optimization 4: Precomputed Categories"
        E1[Problem: Runtime Categorization<br/>Match 1,327 landmarks to tour types<br/>Keyword matching for each request]
        E1 --> E2[Solution: Cached Mapping File<br/>tour_categories.json 155KB<br/>Pre-categorized all landmarks]
        E2 --> E3[Result: Instant Filtering<br/>No runtime computation<br/>Just lookup in cache]
    end

    subgraph "Optimization 5: Custom Haversine"
        F1[Problem: Slow Distance Library<br/>geopy library has overhead<br/>Function call latency]
        F1 --> F2[Solution: Custom Implementation<br/>Direct haversine formula<br/>Optimized for our use case]
        F2 --> F3[Result: 10x Faster<br/>Distance calculations<br/>Removed library dependency]
    end

    subgraph "Final Result"
        G[Improved Performance<br/>Load Time: 3-5 seconds<br/>70% Faster Response<br/>Better User Experience]
    end

    A --> B1
    A --> C1
    A --> D1
    A --> E1
    A --> F1

    B3 --> G
    C3 --> G
    D3 --> G
    E3 --> G
    F3 --> G

    style A fill:#000,stroke:#000,stroke-width:3px,color:#FFF
    style B2 fill:#FFF,stroke:#000,stroke-width:2px
    style C2 fill:#FFF,stroke:#000,stroke-width:2px
    style D2 fill:#FFF,stroke:#000,stroke-width:2px
    style E2 fill:#FFF,stroke:#000,stroke-width:2px
    style F2 fill:#FFF,stroke:#000,stroke-width:2px
    style G fill:#000,stroke:#000,stroke-width:3px,color:#FFF

---

## Mermaid Configuration for IBM Plex Mono + Screen Layout

**IMPORTANT**: Add this configuration at the VERY TOP of the diagram code when pasting into Mermaid Live Editor.

**Configuration Block** (copy this first, then paste diagram code after it):

```
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#FFFFFF',
    'primaryTextColor': '#000000',
    'primaryBorderColor': '#000000',
    'lineColor': '#000000',
    'secondaryColor': '#FFFFFF',
    'tertiaryColor': '#FFFFFF',
    'background': '#FFFFFF',
    'mainBkg': '#FFFFFF',
    'secondBkg': '#FFFFFF',
    'border1': '#000000',
    'border2': '#000000',
    'fontSize': '16px',
    'fontFamily': 'IBM Plex Mono, Courier New, monospace'
  },
  'flowchart': {
    'nodeSpacing': 80,
    'rankSpacing': 100,
    'curve': 'basis',
    'padding': 20,
    'useMaxWidth': true,
    'htmlLabels': true
  }
}}%%
```

**How to Use**:

1. **Copy the config block above** (including %% markers)
2. **Open Mermaid Live Editor**: https://mermaid.live/
3. **Paste config at line 1** of the editor
4. **Paste diagram code right after** (starting from line 2)
5. **Export**: PNG at 1920x1080 (16:9 ratio) or SVG

**Example - Full Diagram with Config**:

```
%%{init: {'theme': 'base', 'themeVariables': {'fontFamily': 'IBM Plex Mono, monospace', 'fontSize': '16px'}}}%%
graph TB
    A[Mobile Web App] --> B[GPS Tracking]
    B --> C[Map Display]

    style A fill:#FFF,stroke:#000,stroke-width:2px
```

**Screen Ratio Optimization**:
- **nodeSpacing: 80** - Horizontal space between nodes (wider for 16:9)
- **rankSpacing: 100** - Vertical space between levels (taller boxes)
- **fontSize: 16px** - Larger font for readability on screens
- **useMaxWidth: true** - Auto-scales to container width

**For PowerPoint/Keynote**:
- Export as PNG at **1920x1080** (standard HD)
- Or export as SVG for infinite scaling

---

## Usage Notes

1. **Copy Correctly**: Select ONLY the diagram code (graph TB to last style line)
2. **Paste into Mermaid Live**: https://mermaid.live/
3. **Add Font Config**: Paste the IBM Plex Mono config at the very top
4. **Export**: PNG at 2-3x resolution for presentations
5. **Customize**: Add colors by changing fill values in style lines

**All labels now explain**:
- What the component does
- What data it contains
- What APIs it calls
- What the output/result is

Someone reviewing your portfolio with no prior knowledge can now understand the entire system flow!
