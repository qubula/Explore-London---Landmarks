# Working Mermaid Diagrams - SVG Export Ready

**IMPORTANT**: Each diagram includes `%%init%%` config at the top for IBM Plex Mono font and proper SVG export.

**How to Use**:
1. Copy entire diagram (including `%%init%%` line)
2. Paste into Mermaid Live Editor: https://mermaid.live/
3. Export as SVG or PNG - text will be visible!

---

## 1. System Architecture Overview

%%{init: {'theme':'base','themeVariables':{'fontFamily':'IBM Plex Mono, monospace','fontSize':'16px','primaryTextColor':'#000000'}}}%%
graph TB
    A[Mobile Web App] --> B[GPS Tracking]
    A --> C[Google Maps Display]
    A --> D[API: plan-route]

    D --> E[Route Optimization]
    E --> F[Google Directions API]
    E --> G[Landmark Database]

    G --> H[1,327 London POIs]
    G --> I[Tour Categories]
    G --> J[AI Scripts]

    F --> K[Route Polyline]
    K --> C
    B --> L[Landmark Detection]
    L --> M[Card Display]

    style A fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style B fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style C fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style D fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style E fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style F fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style G fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style H fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style I fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style J fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style K fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style L fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style M fill:#FFF,stroke:#000,stroke-width:2px,color:#000

---

## 2. User Journey Flow (Simplified)

%%{init: {'theme':'base','themeVariables':{'fontFamily':'IBM Plex Mono, monospace','fontSize':'16px','primaryTextColor':'#000000'}}}%%
flowchart TD
    A([Start: Open App]) --> B[Enter Start & Destination]
    B --> C[Select Route Mode]
    C --> D{Scenic Mode?}
    D -->|Yes| E[Choose Tour Type]
    D -->|No| F[Start Fastest Route]
    E --> G[API: Check Availability]
    G --> H[Gray Out Unavailable]
    H --> I[Confirm Selection]
    I --> J[API: Plan Route]
    F --> J
    J --> K[Display Map & Route]
    K --> L[Start GPS Tracking]
    L --> M{Near Landmark?}
    M -->|Yes| N[Show Card]
    M -->|No| L
    N --> O{More Landmarks?}
    O -->|Yes| L
    O -->|No| P([End: Complete])

    style A fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style B fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style C fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style D fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style E fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style F fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style G fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style H fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style I fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style J fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style K fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style L fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style M fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style N fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style O fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style P fill:#FFF,stroke:#000,stroke-width:2px,color:#000

---

## 3. Route Optimization - 3 Modes

%%{init: {'theme':'base','themeVariables':{'fontFamily':'IBM Plex Mono, monospace','fontSize':'16px','primaryTextColor':'#000000'}}}%%
graph LR
    subgraph Mode1[Mode 1: Fastest]
        A1[Start → End] --> B1[Direct Route]
        B1 --> C1[Extract Landmarks]
    end

    subgraph Mode2[Mode 2: Scenic Auto]
        A2[Start → End + Type] --> B2[Find Grand Landmarks]
        B2 --> C2[Rank & Select Top N]
        C2 --> D2[Re-route via Waypoints]
    end

    subgraph Mode3[Mode 3: User Select]
        A3[Show 8 Landmarks] --> B3[User Picks 3]
        B3 --> C3[Custom Route]
    end

    style A1 fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style B1 fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style C1 fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style A2 fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style B2 fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style C2 fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style D2 fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style A3 fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style B3 fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style C3 fill:#FFF,stroke:#000,stroke-width:2px,color:#000

---

## 4. Landmark Scoring

%%{init: {'theme':'base','themeVariables':{'fontFamily':'IBM Plex Mono, monospace','fontSize':'16px','primaryTextColor':'#000000'}}}%%
graph TD
    A[Landmark Input] --> B[Check Category]
    B --> C{Type?}
    C -->|Palace| D[+60 points]
    C -->|Cathedral| E[+55 points]
    C -->|Museum| F[+50 points]
    C -->|Bridge| G[+30 points]
    D --> H[Add Popularity Boost]
    E --> H
    F --> H
    G --> H
    H --> I[Total Score]
    I --> J{Score ≥ 30?}
    J -->|Yes| K[Include]
    J -->|No| L[Exclude]

    style A fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style B fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style C fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style D fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style E fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style F fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style G fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style H fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style I fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style J fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style K fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style L fill:#FFF,stroke:#000,stroke-width:2px,color:#000

---

## 5. Data Pipeline (5 Stages)

%%{init: {'theme':'base','themeVariables':{'fontFamily':'IBM Plex Mono, monospace','fontSize':'16px','primaryTextColor':'#000000'}}}%%
graph LR
    A[OpenStreetMap] --> D[Merge Data]
    B[Wikipedia] --> D
    C[Google Places] --> D
    D --> E[Filter 1,327 POIs]
    E --> F[OpenAI GPT-4]
    F --> G[Generate Scripts]
    G --> H[JSON Database]
    H --> I[GitHub Push]
    I --> J[Railway Deploy]
    J --> K[Live App]

    style A fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style B fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style C fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style D fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style E fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style F fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style G fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style H fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style I fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style J fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style K fill:#FFF,stroke:#000,stroke-width:2px,color:#000

---

## 6. GPS Tracking Flow (Improved - Flowchart Style)

%%{init: {'theme':'base','themeVariables':{'fontFamily':'IBM Plex Mono, monospace','fontSize':'16px','primaryTextColor':'#000000'}}}%%
flowchart TD
    A([User Opens Tour Page]) --> B[App Initializes Map<br/>Load route & landmarks]
    B --> C[Request GPS Permission]
    C --> D{User Grants<br/>Permission?}
    D -->|No| E[Show Error Message<br/>Cannot track location]
    D -->|Yes| F[Start Tracking Loop<br/>watchPosition active]

    F --> G[Get Current Position<br/>Latitude & Longitude]
    G --> H[Update Blue Marker<br/>Show user on map]
    H --> I[Calculate Distance to<br/>All Unvisited Landmarks]

    I --> J{Distance to<br/>Nearest Landmark?}

    J -->|≤ 120m<br/>Within Range| K[Trigger Landmark<br/>Mark as visited]
    J -->|> 120m<br/>Still Far| L[Update Distance Text<br/>Show: 500m away]

    K --> M[Animate to Card<br/>Swipe to landmark]
    M --> N[Display Card Content<br/>Image, name, script]

    N --> O[Wait 3 Seconds<br/>GPS update interval]
    L --> O

    O --> P{More Unvisited<br/>Landmarks?}
    P -->|Yes| G
    P -->|No| Q([Journey Complete<br/>End tracking])

    style A fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style B fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style C fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style D fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style E fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style F fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style G fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style H fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style I fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style J fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style K fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style L fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style M fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style N fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style O fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style P fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style Q fill:#FFF,stroke:#000,stroke-width:2px,color:#000

---

## 6B. GPS Tracking - Alternative State-Based View

%%{init: {'theme':'base','themeVariables':{'fontFamily':'IBM Plex Mono, monospace','fontSize':'16px','primaryTextColor':'#000000'}}}%%
stateDiagram-v2
    [*] --> Initializing: User Opens Tour
    Initializing --> PermissionRequest: Request GPS Access
    PermissionRequest --> Denied: User Denies
    PermissionRequest --> Tracking: User Allows

    Denied --> [*]: Show Error

    state Tracking {
        [*] --> GettingPosition
        GettingPosition --> CalculatingDistance: Position Received
        CalculatingDistance --> FarAway: Distance > 120m
        CalculatingDistance --> NearLandmark: Distance ≤ 120m

        FarAway --> WaitingUpdate: Show Distance
        NearLandmark --> ShowingCard: Trigger Card
        ShowingCard --> WaitingUpdate: Card Displayed

        WaitingUpdate --> GettingPosition: After 3 seconds
    }

    Tracking --> Complete: No More Landmarks
    Complete --> [*]

---

## 7. Performance Optimization

%%{init: {'theme':'base','themeVariables':{'fontFamily':'IBM Plex Mono, monospace','fontSize':'16px','primaryTextColor':'#000000'}}}%%
graph TB
    A[Problem: 10-15s Load] --> B[Optimization 1]
    A --> C[Optimization 2]
    A --> D[Optimization 3]
    A --> E[Optimization 4]

    B[Lazy Loading] --> F[Result]
    C[Bounding Box Filter] --> F
    D[Polyline Encoding] --> F
    E[Precomputed Cache] --> F

    F[Solution: 3-5s Load]

    style A fill:#FFF,stroke:#000,stroke-width:2px
    style B fill:#FFF,stroke:#000,stroke-width:2px
    style C fill:#FFF,stroke:#000,stroke-width:2px
    style D fill:#FFF,stroke:#000,stroke-width:2px
    style E fill:#FFF,stroke:#000,stroke-width:2px
    style F fill:#FFF,stroke:#000,stroke-width:2px

---

## Solution 2: Recommendation for Isometric Style

Since you want **isometric/3D diagrams like Frame 8.svg**, Mermaid won't achieve that look. Here are better tools:

### Recommended Tools:
1. **Figma** (what you're already using) - Continue creating diagrams there
2. **Excalidraw** - https://excalidraw.com/ - Hand-drawn style, simple isometric
3. **Draw.io** - https://app.diagrams.net/ - Has isometric shape libraries
4. **PowerPoint/Keynote** - Use 3D shapes with shadows/gradients

### Quick Guide for Isometric Diagrams in Figma:

1. **Create isometric grid**: 30° angle lines
2. **Use skewed rectangles**: Transform → Skew by 30°
3. **Layer with shadows**: Drop shadows at 30° angles
4. **Color palette**: Use your app colors (#FAF8F3, #1a1a1a, #3b82f6)
5. **Add depth**: Darker shades for sides, lighter for tops

Would you like me to:
- **A)** Create simplified text-based diagrams (ASCII art style) that you can easily recreate in Figma?
- **B)** Provide detailed descriptions of each diagram so you can design them in Figma?
- **C)** Create a template structure document showing what content each diagram should contain?
