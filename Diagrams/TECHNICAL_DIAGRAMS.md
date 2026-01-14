# Technical Package - Diagrams & Infographics
## PassingBy Tour Guide - Mermaid Visualization Collection

> **How to Use**: Copy any diagram to [Mermaid Live Editor](https://mermaid.live/) to customize colors, fonts, and styling. Export as PNG/SVG for your presentation.

---

## 1. System Architecture - Complete Overview

```mermaid
graph TB
    subgraph "User Interface"
        A[Mobile Web App<br/>HTML5 + JavaScript]
        B[Google Maps Display]
        C[Location Input<br/>Autocomplete]
    end

    subgraph "Frontend Logic"
        D[GPS Tracking<br/>Real-time Position]
        E[Route Visualization<br/>Polyline Rendering]
        F[Landmark Cards<br/>3D Flip Interface]
    end

    subgraph "Backend API - FastAPI"
        G[/api/plan-route<br/>Route Planning]
        H[/api/check-tour-availability<br/>Filtering Logic]
        I[Route Optimization Engine<br/>3 Mode Algorithm]
    end

    subgraph "External APIs"
        J[Google Maps Directions<br/>Route Polylines]
        K[Google Places<br/>Autocomplete + Geocoding]
        L[OpenAI GPT-4<br/>Script Generation]
    end

    subgraph "Data Layer"
        M[(Landmark Database<br/>1,327 London POIs<br/>1.8MB JSON)]
        N[(Tour Categories<br/>Keyword Mapping)]
        O[(Talking Points<br/>Tour-Specific Scripts)]
    end

    C --> K
    A --> D
    A --> G
    G --> I
    I --> J
    I --> M
    I --> N
    H --> M
    M --> O
    J --> E
    E --> B
    D --> F
    G --> A

    style A fill:#FAF8F3,stroke:#1a1a1a,stroke-width:3px
    style G fill:#3b82f6,stroke:#1a1a1a,stroke-width:2px
    style M fill:#fbbf24,stroke:#1a1a1a,stroke-width:2px
    style J fill:#10b981,stroke:#1a1a1a,stroke-width:2px
```

**Customization Notes**:
- Change `fill:#FAF8F3` to any hex color for node backgrounds
- Adjust `stroke-width` for border thickness
- Modify subgraph labels to change section titles

---

## 2. User Journey Flow - Step by Step

```mermaid
flowchart TD
    Start([User Opens App]) --> Landing[Landing Page<br/>PassingBy Branding]
    Landing --> DestInput[Enter Start & Destination<br/>Google Places Autocomplete]
    DestInput --> SaveDest{Save to localStorage}
    SaveDest --> RouteMode[Select Route Mode<br/>Fastest vs Scenic]

    RouteMode --> ModeCheck{Mode = Scenic?}
    ModeCheck -->|Yes| TourType[Select Tour Type<br/>Architecture, Historical, etc.]
    ModeCheck -->|No| DirectTour[Auto: 'All' Tour Type]

    TourType --> API1[API Call:<br/>check-tour-availability]
    API1 --> Filter[Gray Out Unavailable Tours<br/>No landmarks on route]
    Filter --> Confirm[User Confirms Selection]

    Confirm --> API2[API Call:<br/>plan-route]
    DirectTour --> API2

    API2 --> Backend[Backend Processing<br/>Route Optimization]
    Backend --> Response[Return: Route + Landmarks<br/>Polyline + Scripts]
    Response --> Display[Display Active Tour Map]

    Display --> GPS[Start GPS Tracking<br/>watchPosition every 3s]
    GPS --> Proximity{Within Landmark<br/>Trigger Radius?}

    Proximity -->|Yes| ShowCard[Display Landmark Card<br/>Image + Script]
    Proximity -->|No| GPS

    ShowCard --> NextLM{More Landmarks?}
    NextLM -->|Yes| GPS
    NextLM -->|No| End([Journey Complete])

    style Start fill:#10b981,stroke:#1a1a1a,stroke-width:2px,color:#fff
    style API2 fill:#3b82f6,stroke:#1a1a1a,stroke-width:2px,color:#fff
    style Backend fill:#fbbf24,stroke:#1a1a1a,stroke-width:2px
    style End fill:#ef4444,stroke:#1a1a1a,stroke-width:2px,color:#fff
```

**Customization Notes**:
- Decision diamonds (`{}`) auto-style as rhombus
- Change `color:#fff` for text color on filled nodes
- Use `|Label|` on arrows to add transition text

---

## 3. Route Optimization Algorithm - 3 Modes Comparison

```mermaid
graph LR
    subgraph "Mode 1: Fastest Route"
        A1[User Input:<br/>Start → End] --> B1[Google Directions API<br/>Direct Route]
        B1 --> C1[Extract Visible<br/>Landmarks Along Route]
        C1 --> D1[Limit: 0.5 landmarks/min<br/>Dynamic Filtering]
        D1 --> E1[Return Route<br/>+ Landmarks]
    end

    subgraph "Mode 2: Scenic Auto"
        A2[User Input:<br/>Start → End + Tour Type] --> B2[Get Baseline<br/>Fastest Route]
        B2 --> C2[Find Grand Landmarks<br/>Within 1km of Route]
        C2 --> D2[Rank by Score<br/>Filter by Tour Type]
        D2 --> E2[Select Top N<br/>Fit in Time Budget]
        E2 --> F2[Re-route with Waypoints<br/>A→LM1→LM2→B]
        F2 --> G2[Return Optimized Route<br/>+5-10 min added]
    end

    subgraph "Mode 3: Scenic Select"
        A3[User Input:<br/>Start → End] --> B3[Find 8 Grand Landmarks<br/>Near Route]
        B3 --> C3[Display Menu<br/>User Selects up to 3]
        C3 --> D3[Build Custom Route<br/>A→Selected LMs→B]
        D3 --> E3[Return Custom Route<br/>Variable Time Added]
    end

    style B1 fill:#10b981,stroke:#1a1a1a,stroke-width:2px
    style F2 fill:#3b82f6,stroke:#1a1a1a,stroke-width:2px
    style C3 fill:#fbbf24,stroke:#1a1a1a,stroke-width:2px
```

**Customization Notes**:
- Three side-by-side workflows show mode differences
- Color-coded by complexity: Green (simple) → Blue (automated) → Yellow (interactive)

---

## 4. Landmark Scoring System - Calculation Flow

```mermaid
flowchart TD
    Start([Landmark Data Input]) --> Cat[Check Category<br/>palace, cathedral, museum, etc.]

    Cat --> CatScore{Assign Category Score}
    CatScore -->|Palace| S1[+60 points]
    CatScore -->|Cathedral| S2[+55 points]
    CatScore -->|Museum| S3[+50 points]
    CatScore -->|Monument| S4[+40 points]
    CatScore -->|Bridge| S5[+30 points]
    CatScore -->|Park| S6[+25 points]

    S1 & S2 & S3 & S4 & S5 & S6 --> Boost[Check Google Places<br/>Popularity Boost]

    Boost --> BoostCalc{Famous Landmark?}
    BoostCalc -->|Tower Bridge| B1[+56 points]
    BoostCalc -->|British Museum| B2[+54 points]
    BoostCalc -->|Westminster Abbey| B3[+53 points]
    BoostCalc -->|Other| B4[+0-50 points<br/>Variable]

    B1 & B2 & B3 & B4 --> Total[Calculate Total Score<br/>Category + Boost]

    Total --> Example1[Example: Buckingham Palace<br/>60 palace + 50 boost = 110]
    Total --> Example2[Example: Tower Bridge<br/>30 bridge + 56 boost = 86]
    Total --> Example3[Example: Small Church<br/>55 cathedral + 0 boost = 55]

    Example1 & Example2 & Example3 --> Filter{Score ≥ Min Threshold?}

    Filter -->|Yes<br/>Score ≥ 30| Include[Include in Tour]
    Filter -->|No<br/>Score < 30| Exclude[Exclude from Results]

    Include --> End([Final Ranked List<br/>Sorted by Score])

    style CatScore fill:#fbbf24,stroke:#1a1a1a,stroke-width:2px
    style BoostCalc fill:#3b82f6,stroke:#1a1a1a,stroke-width:2px
    style Filter fill:#ef4444,stroke:#1a1a1a,stroke-width:2px,color:#fff
    style End fill:#10b981,stroke:#1a1a1a,stroke-width:2px,color:#fff
```

**Customization Notes**:
- Parallel paths show different scoring tiers
- Examples demonstrate real calculations
- Color transitions: Yellow (category) → Blue (boost) → Red (filter) → Green (output)

---

## 5. Data Pipeline - From Collection to Deployment

```mermaid
graph TB
    subgraph "Stage 1: Data Collection"
        A1[OpenStreetMap API<br/>Overpass Query] --> A2[Extract 2000+<br/>London POIs]
        A3[Wikipedia API<br/>Summary Fetch] --> A4[Get Descriptions<br/>Remove duplicates]
        A5[Google Places API<br/>Popularity Data] --> A6[Boost Scores<br/>0-56 points]
    end

    subgraph "Stage 2: Data Processing"
        B1[Merge Data Sources<br/>Match by name/coords] --> B2[Filter Quality<br/>1,327 landmarks remain]
        B2 --> B3[Calculate Scores<br/>Category + Boost]
        B3 --> B4[Classify Types<br/>Region, Building, Object]
    end

    subgraph "Stage 3: AI Content Generation"
        C1[OpenAI GPT-4 API<br/>Script Generation] --> C2[Generate 60-80 word<br/>Conversational Scripts]
        C2 --> C3[LLM Tagging<br/>Tour-Specific Points]
        C3 --> C4[9 Tour Types<br/>Keyword Matching]
    end

    subgraph "Stage 4: Database Creation"
        D1[Combine All Data] --> D2[(final_landmarks_v6.2_Big.json<br/>1.8 MB)]
        D2 --> D3[(landmark_tags.json<br/>1.2 MB)]
        D2 --> D4[(tour_categories.json<br/>155 KB Cache)]
    end

    subgraph "Stage 5: Production Deployment"
        E1[Git Push to GitHub] --> E2[Railway Auto-Deploy<br/>CI/CD Pipeline]
        E2 --> E3[FastAPI Server<br/>Lazy Load Data]
        E3 --> E4[Live Production App<br/>Cloud Hosted]
    end

    A2 & A4 & A6 --> B1
    B4 --> C1
    C4 --> D1
    D3 & D4 --> E1

    style A2 fill:#10b981,stroke:#1a1a1a,stroke-width:2px
    style C2 fill:#8b5cf6,stroke:#1a1a1a,stroke-width:2px
    style D2 fill:#fbbf24,stroke:#1a1a1a,stroke-width:2px
    style E4 fill:#3b82f6,stroke:#1a1a1a,stroke-width:2px,color:#fff
```

**Customization Notes**:
- 5-stage pipeline shows full data lifecycle
- Database nodes use cylinder shape `[()]`
- Color progression: Green (collection) → Purple (AI) → Yellow (storage) → Blue (deployment)

---

## 6. Real-Time GPS Tracking Logic

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Frontend
    participant Map
    participant Backend

    User->>Browser: Opens Tour Page
    Browser->>Frontend: Load tour_logic.js
    Frontend->>Backend: POST /api/plan-route
    Backend->>Backend: Calculate route + landmarks
    Backend-->>Frontend: Return route_points + landmarks[]

    Frontend->>Map: Render polyline + markers
    Frontend->>Browser: Request geolocation permission
    Browser->>User: "Allow location access?"
    User-->>Browser: Grant permission

    loop Every 3 seconds
        Browser->>Frontend: watchPosition() callback
        Frontend->>Frontend: Calculate distance to landmarks
        Frontend->>Map: Update blue user marker

        alt Within trigger radius (120m)
            Frontend->>Frontend: Mark landmark as visited
            Frontend->>Map: Animate to landmark card
            Frontend->>User: Display card with script
        else Not in range
            Frontend->>User: Show distance: "500m away"
        end
    end

    User->>Frontend: Reaches destination
    Frontend->>Frontend: Stop GPS tracking
    Frontend->>User: Journey complete screen
```

**Customization Notes**:
- Sequence diagram shows time-ordered interactions
- Loop section demonstrates continuous GPS polling
- Alt/else shows conditional logic (proximity detection)

---

## 7. Tour Type Filtering Architecture

```mermaid
graph TD
    subgraph "User Selection Flow"
        A[User Enters Route<br/>Start → End] --> B[Select: Scenic Mode]
        B --> C[Navigate to Tour Type Page]
    end

    subgraph "Frontend Availability Check"
        C --> D[Read localStorage<br/>alfie_start, alfie_destination]
        D --> E[API POST: /api/check-tour-availability<br/>{start, end, mode}]
    end

    subgraph "Backend Processing - For Each Tour Type"
        E --> F1[Architecture Tour]
        E --> F2[Historical Tour]
        E --> F3[Royal Tour]
        E --> F4[... 6 more types]

        F1 --> G1[Filter by keywords<br/>bridge, tower, palace]
        F2 --> G2[Filter by keywords<br/>museum, memorial, monument]
        F3 --> G3[Filter by keywords<br/>palace, royal, king, queen]

        G1 --> H1{Count landmarks<br/>on route}
        G2 --> H2{Count landmarks<br/>on route}
        G3 --> H3{Count landmarks<br/>on route}

        H1 -->|> 1 landmark| I1[architecture: true]
        H1 -->|≤ 1 landmark| I2[architecture: false]
        H2 -->|> 1 landmark| I3[historical: true]
        H2 -->|≤ 1 landmark| I4[historical: false]
        H3 -->|> 1 landmark| I5[royal: true]
        H3 -->|≤ 1 landmark| I6[royal: false]
    end

    subgraph "Frontend UI Update"
        I1 & I2 & I3 & I4 & I5 & I6 --> J[Receive availability object<br/>{arch: true, hist: false, ...}]
        J --> K[For each tour card]
        K --> L{availability = false?}
        L -->|Yes| M[Apply disabled styles<br/>opacity: 0.4, grayscale, no click]
        L -->|No| N[Keep fully enabled<br/>User can select]
        M --> O[Add message:<br/>No landmarks on this route]
    end

    style E fill:#3b82f6,stroke:#1a1a1a,stroke-width:2px,color:#fff
    style L fill:#ef4444,stroke:#1a1a1a,stroke-width:2px,color:#fff
    style N fill:#10b981,stroke:#1a1a1a,stroke-width:2px,color:#fff
```

**Customization Notes**:
- Shows full round-trip: User → Frontend → Backend → UI update
- Parallel processing for multiple tour types
- Color-coded decisions: Blue (API) → Red (filter) → Green (enable)

---

## 8. Performance Optimization Strategy

```mermaid
graph LR
    subgraph "Problem: Slow Route Planning"
        A[Initial Request<br/>10-15 second load time]
    end

    subgraph "Optimization 1: Lazy Loading"
        B1[Load 1.8MB JSON<br/>on first use only] --> B2[Save 500ms<br/>per subsequent request]
    end

    subgraph "Optimization 2: Bounding Box Filter"
        C1[Calculate Route Bounds<br/>min/max lat/lon] --> C2[Pre-filter landmarks<br/>90% eliminated]
        C2 --> C3[Only calc distance<br/>for ~130 landmarks]
    end

    subgraph "Optimization 3: Polyline Encoding"
        D1[Google polyline<br/>compression algorithm] --> D2[Route data:<br/>100KB → 2KB]
    end

    subgraph "Optimization 4: Precomputed Categories"
        E1[Cache tour type mapping<br/>tour_categories.json] --> E2[Instant filtering<br/>no runtime categorization]
    end

    subgraph "Optimization 5: Haversine Distance"
        F1[Custom formula<br/>vs geopy library] --> F2[10x faster<br/>distance calculations]
    end

    subgraph "Result: Improved Performance"
        G[Final Load Time<br/>3-5 seconds ✓]
    end

    A --> B1 & C1 & D1 & E1 & F1
    B2 & C3 & D2 & E2 & F2 --> G

    style A fill:#ef4444,stroke:#1a1a1a,stroke-width:3px,color:#fff
    style G fill:#10b981,stroke:#1a1a1a,stroke-width:3px,color:#fff
    style B2 fill:#fbbf24,stroke:#1a1a1a,stroke-width:2px
    style C3 fill:#fbbf24,stroke:#1a1a1a,stroke-width:2px
    style D2 fill:#fbbf24,stroke:#1a1a1a,stroke-width:2px
    style E2 fill:#fbbf24,stroke:#1a1a1a,stroke-width:2px
    style F2 fill:#fbbf24,stroke:#1a1a1a,stroke-width:2px
```

**Customization Notes**:
- Problem → Solutions → Result structure
- 5 parallel optimizations converge to single outcome
- Color coding: Red (problem) → Yellow (optimizations) → Green (solution)

---

## 9. Design Evolution Timeline

```mermaid
timeline
    title Design System Evolution - Color Palettes & UI Components

    section Early Development
        Golden Peachy Glow : Warm color scheme
                          : Oranges, peaches, yellows
                          : Focus: Brand warmth

    section Mid Development
        Pastel Dreamland : Soft pastel palette
                        : Tour type differentiation
                        : 8 distinct colors per theme
                        : Architecture: #8e9aaf
                        : Historical: #adadc1
                        : Royal: #cbc0d3

    section Final Release
        Minimalist Black & Cream : High contrast
                                 : #1a1a1a (black) + #FAF8F3 (cream)
                                 : Glassmorphism design
                                 : Mobile clarity priority
                                 : Accessibility focused
```

**Customization Notes**:
- Timeline visualization shows chronological progression
- Section breaks group related iterations
- Hex codes show actual color values used

---

## 10. Component Development Iterations

```mermaid
graph LR
    subgraph "Map Markers Evolution"
        M1[Google A/B Labels] -->|Issue: Generic| M2[Emoji Icons ▶ ■]
        M2 -->|Issue: Small, unclear| M3[Custom SVG Pins]
        M3 -->|Refinement| M4[Reduced 50% size<br/>16x28.5px]
    end

    subgraph "Card UI Evolution"
        C1[Standard Cards] -->|Enhancement| C2[3D Flip Animation]
        C2 -->|Issue: Clipping| C3[Fixed container height<br/>45vh]
        C3 -->|Refinement| C4[Border radius iterations<br/>13px → 2px]
    end

    subgraph "Selection Interface"
        S1[Checkboxes] -->|Improvement| S2[Glass Card Buttons]
        S2 -->|Enhancement| S3[Interactive Hover States]
        S3 -->|Accessibility| S4[Touch targets: 44px min]
    end

    subgraph "Modal Patterns"
        P1[Alert Dialogs] -->|Improvement| P2[Bottom Sheets]
        P2 -->|Enhancement| P3[iOS-style Handle]
        P3 -->|Usability| P4[Outside-click to close]
    end

    M4 & C4 & S4 & P4 --> Final[Current Production Design<br/>18+ iterations total]

    style M1 fill:#ef4444,stroke:#1a1a1a,stroke-width:2px
    style C1 fill:#ef4444,stroke:#1a1a1a,stroke-width:2px
    style S1 fill:#ef4444,stroke:#1a1a1a,stroke-width:2px
    style P1 fill:#ef4444,stroke:#1a1a1a,stroke-width:2px
    style Final fill:#10b981,stroke:#1a1a1a,stroke-width:3px,color:#fff
```

**Customization Notes**:
- Shows 4 component types evolving in parallel
- Each path: Initial (red) → Iterations → Final (green)
- Demonstrates iterative design process

---

## 11. Mobile-First Responsive Breakpoints

```mermaid
graph TD
    subgraph "Screen Size Handling"
        A[User Device Detection] --> B{Screen Width?}

        B -->|< 390px| C[Small Mobile<br/>iPhone SE, Mini]
        B -->|390-428px| D[Standard Mobile<br/>iPhone 12-15]
        B -->|428-768px| E[Large Mobile<br/>iPhone Plus, Android]
        B -->|≥ 768px| F[Desktop/Tablet<br/>iPad, Laptop]
    end

    subgraph "Small Mobile Adaptations"
        C --> C1[Reduce font sizes<br/>14px base]
        C1 --> C2[Tighter spacing<br/>12px padding]
        C2 --> C3[Smaller touch targets<br/>40px minimum]
    end

    subgraph "Standard Mobile - Default"
        D --> D1[16px base font<br/>1.6 line-height]
        D1 --> D2[24px spacing<br/>comfortable padding]
        D2 --> D3[44px touch targets<br/>iOS guidelines]
        D3 --> D4[Safe area support<br/>env safe-area-inset-*]
    end

    subgraph "Desktop View"
        F --> F1[Simulated iPhone frame<br/>390x844px mockup]
        F1 --> F2[Centered layout<br/>black bezel styling]
        F2 --> F3[Fixed container<br/>max-width: 428px]
    end

    C3 & D4 & F3 --> G[Responsive Rendering Complete]

    style D fill:#10b981,stroke:#1a1a1a,stroke-width:3px,color:#fff
    style G fill:#3b82f6,stroke:#1a1a1a,stroke-width:2px,color:#fff
```

**Customization Notes**:
- Decision tree based on viewport width
- Default path (D) highlighted in green
- Shows specific pixel values and CSS properties

---

## 12. API Cost & Scalability Analysis

```mermaid
graph TB
    subgraph "API Usage Per User Journey"
        A[Single User Journey] --> B[Google Places Autocomplete<br/>2 calls: start + end]
        B --> C[Google Directions API<br/>1-3 calls depending on mode]
        C --> D[Backend Processing<br/>No external API cost]
    end

    subgraph "Cost Breakdown"
        B --> E[Autocomplete: $0.00283<br/>per session × 2 = $0.00566]
        C --> F[Directions: $0.005<br/>per request × 2 avg = $0.01]
        D --> G[FastAPI Hosting: $0.00167<br/>$5/month ÷ 3000 users]
        E & F & G --> H[Total per journey:<br/>~$0.02]
    end

    subgraph "Scalability Projections"
        H --> I{Monthly Users?}
        I -->|100 users| J1[$2/month<br/>Fits free tier]
        I -->|1,000 users| J2[$20/month<br/>Hobby plan]
        I -->|10,000 users| J3[$200/month<br/>Professional plan]
        I -->|100,000 users| J4[$2,000/month<br/>Enterprise needed]
    end

    subgraph "Optimization Opportunities"
        J4 --> K[Cache common routes<br/>Reduce API calls 40%]
        K --> L[Batch geocoding<br/>Pre-cache popular locations]
        L --> M[CDN for static assets<br/>Reduce server load]
        M --> N[Projected savings:<br/>$800/month at 100k users]
    end

    style H fill:#fbbf24,stroke:#1a1a1a,stroke-width:3px
    style J1 fill:#10b981,stroke:#1a1a1a,stroke-width:2px
    style J2 fill:#10b981,stroke:#1a1a1a,stroke-width:2px
    style J3 fill:#fbbf24,stroke:#1a1a1a,stroke-width:2px
    style J4 fill:#ef4444,stroke:#1a1a1a,stroke-width:2px,color:#fff
    style N fill:#10b981,stroke:#1a1a1a,stroke-width:2px
```

**Customization Notes**:
- Cost breakdown with real pricing
- Scalability tiers color-coded: Green (affordable) → Yellow (moderate) → Red (expensive)
- Shows optimization path for cost reduction

---

## 13. Frontend State Management Flow

```mermaid
stateDiagram-v2
    [*] --> LandingPage
    LandingPage --> DestinationInput: Click "Personalise ride"

    DestinationInput --> RouteMode: Save to localStorage<br/>alfie_start, alfie_destination

    RouteMode --> TourTypeCheck: Save alfie_route_mode

    TourTypeCheck --> TourTypeSelection: mode = "scenic"
    TourTypeCheck --> ActiveTour: mode = "fastest"<br/>Auto-set tour_type = "all"

    TourTypeSelection --> APICheck: Fetch availability
    APICheck --> TourTypeSelection: Gray out unavailable
    TourTypeSelection --> ActiveTour: Save alfie_tour_type

    ActiveTour --> GPSTracking: Initialize map + GPS
    GPSTracking --> LandmarkDetection: watchPosition() loop

    LandmarkDetection --> LandmarkDetection: Distance > 120m<br/>Keep tracking
    LandmarkDetection --> CardDisplay: Distance ≤ 120m<br/>Trigger landmark

    CardDisplay --> LandmarkDetection: More landmarks ahead
    CardDisplay --> [*]: Journey complete

    note right of DestinationInput
        localStorage keys:
        - alfie_start (JSON)
        - alfie_destination (JSON)
    end note

    note right of ActiveTour
        API Response stored:
        - route_points[]
        - landmarks[]
        - fastest_eta
        - chosen_eta
    end note
```

**Customization Notes**:
- State diagram shows page transitions
- Notes explain data storage at each stage
- Loops show continuous GPS tracking logic

---

## Usage Instructions

### How to Edit Diagrams:

1. **Copy diagram code** from this document
2. **Open Mermaid Live Editor**: https://mermaid.live/
3. **Paste code** into left panel
4. **Customize** using the config panel:
   - Change theme: default, forest, dark, neutral
   - Adjust colors in code: `fill:#COLOR`, `stroke:#COLOR`
   - Modify fonts: Add `%%{init: {'theme':'base', 'themeVariables': {'fontSize':'16px'}}}%%` at top
5. **Export** as PNG or SVG for presentations

### Recommended Theme Configuration:

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#FAF8F3',
    'primaryTextColor': '#1a1a1a',
    'primaryBorderColor': '#1a1a1a',
    'lineColor': '#1a1a1a',
    'secondaryColor': '#3b82f6',
    'tertiaryColor': '#fbbf24',
    'fontSize': '14px',
    'fontFamily': 'Satoshi, -apple-system, sans-serif'
  }
}}%%
```

Add this to the top of any diagram to match your app's design system (cream background, black text, glass UI colors).

### Color Palette Reference (From Your App):

- **Cream Background**: `#FAF8F3`
- **Black Text**: `#1a1a1a`
- **Accent Blue**: `#3b82f6`
- **Accent Yellow**: `#fbbf24`
- **Success Green**: `#10b981`
- **Error Red**: `#ef4444`
- **Purple (AI)**: `#8b5cf6`

---

## Additional Infographic Ideas (Text-Based)

### 14. Technology Stack Breakdown

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                       │
├─────────────────────────────────────────────────────────┤
│ • HTML5 + Vanilla JavaScript (No framework overhead)    │
│ • Google Maps JavaScript SDK v3                         │
│ • Swiper.js 11.0 (Card carousel)                       │
│ • Custom CSS with glassmorphism effects                │
│ • Browser APIs: Geolocation, localStorage              │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                   BACKEND LAYER                         │
├─────────────────────────────────────────────────────────┤
│ • FastAPI 0.104.1 (Async Python web framework)         │
│ • Uvicorn ASGI server                                  │
│ • Python 3.11.x                                        │
│ • Custom route optimization algorithms                 │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                   EXTERNAL APIs                         │
├─────────────────────────────────────────────────────────┤
│ • Google Maps Directions API (Route polylines)         │
│ • Google Places API (Autocomplete + Geocoding)         │
│ • OpenAI GPT-4 API (Script generation - offline)       │
│ • ElevenLabs TTS (Planned - voice narration)           │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    DATA LAYER                           │
├─────────────────────────────────────────────────────────┤
│ • final_landmarks_v6.2_Big.json (1.8 MB - 1,327 POIs) │
│ • landmark_tags.json (1.2 MB - Tour-specific scripts)  │
│ • tour_categories.json (155 KB - Cached mappings)      │
│ • landmark_images.json (250 KB - Image URLs)           │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                 DEPLOYMENT LAYER                        │
├─────────────────────────────────────────────────────────┤
│ • Railway.app (Cloud hosting)                          │
│ • GitHub (Version control + CI/CD trigger)             │
│ • Automatic deployments on git push                    │
│ • Environment variables for API keys                   │
└─────────────────────────────────────────────────────────┘
```

### 15. Performance Metrics Table

| Metric | Before Optimization | After Optimization | Improvement |
|--------|--------------------|--------------------|-------------|
| **Initial Load Time** | 10-15 seconds | 3-5 seconds | **70% faster** |
| **Landmark Database Load** | Every request (500ms) | Lazy load once | **500ms saved** |
| **Distance Calculations** | 1,327 per request | ~130 per request (90% reduction) | **10x faster** |
| **Route Data Size** | 100 KB raw JSON | 2 KB polyline | **50x smaller** |
| **Tour Type Filtering** | Runtime categorization | Precomputed cache | **Instant** |
| **Memory Usage** | 15 MB | 8 MB | **47% reduction** |
| **API Calls per Journey** | 5-7 calls | 2-3 calls | **60% fewer** |

### 16. Feature Comparison Matrix

| Feature | Traditional Tour | Navigation App | PassingBy |
|---------|-----------------|----------------|-----------|
| **Route Planning** | Fixed path | Fastest only | 3 modes: Fast/Scenic/Custom |
| **Landmarks** | Pre-selected by guide | None | AI-curated (1,327 total) |
| **Personalization** | None | Avoid tolls/highways | 9 themed tour types |
| **Narration** | Live guide | Turn-by-turn | AI scripts (planned voice) |
| **Flexibility** | Scheduled times | Anytime | Anytime + adaptive routing |
| **Cost** | £25-50 per person | Free | Free (cloud hosted) |
| **Offline Support** | N/A | Limited | Planned (service worker) |
| **Real-time Adaptation** | No | Traffic only | Landmarks + traffic |

### 17. Git Commit History Highlights

```
Recent Development Timeline (Last 30 Days):

c6f6429 - Bump tour_logic.js version to v=6 for cache refresh
56fae4d - Reduce SVG pin marker size by 50%
2d87ad5 - Bump JS version to force cache refresh
16ac753 - Replace map marker labels with custom SVG pins
115646c - Gray out unavailable tour types instead of hiding
9ccc95d - Add debug logging to tour type filtering
697438b - Fix tour type filtering by correcting localStorage keys
c58d609 - Replace map markers with icons and hide highway shields
c4be56c - Restore card corner radius to 12px to match other elements

Total Commits: 150+
Contributors: 2 (You + Google Antigravity contractor)
Lines of Code:
  - Python: 3,500+ lines
  - JavaScript: 2,800+ lines
  - CSS: 1,268 lines
  - HTML: 850+ lines
```

---

## End of Diagrams Collection

**Total Diagrams Created**: 13 Mermaid diagrams + 4 text-based infographics

**Next Steps**:
1. Copy diagrams to Mermaid Live Editor
2. Customize colors to match your brand (#FAF8F3, #1a1a1a)
3. Export as PNG/SVG (recommended: 1920x1080px for slides)
4. Insert into your presentation software
5. Use text infographics as speaker notes or supplementary slides

**Pro Tip**: For presentations, use **PNG exports at 2x resolution** (3840x2160) then scale down in slides for crisp rendering on projectors.
