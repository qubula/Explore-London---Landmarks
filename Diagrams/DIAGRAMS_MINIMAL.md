# Minimalist Technical Diagrams - Black, White & Red

**Color Scheme**: Black (#000000), White (#FFFFFF), Red (#FF0000) accent

**How to Use**:
1. Copy diagram code (WITHOUT the ```mermaid wrapper)
2. Paste into [Mermaid Live Editor](https://mermaid.live/)
3. Export as PNG/SVG

---

## 1. System Architecture Overview

graph TB
    A[Mobile Web App] --> B[GPS Tracking]
    A --> C[Google Maps]
    A --> D[API Endpoint]

    D --> E[Route Engine]
    E --> F[Google Directions]
    E --> G[Landmark DB]

    G --> H[1,327 POIs]
    G --> I[Categories]
    G --> J[AI Scripts]

    F --> K[Polyline]
    K --> C
    B --> L[Detection]
    L --> M[Card UI]

    style A fill:#000,stroke:#FF0000,stroke-width:3px,color:#FFF
    style D fill:#FF0000,stroke:#000,stroke-width:2px,color:#FFF
    style G fill:#FFF,stroke:#000,stroke-width:2px,color:#000
    style M fill:#FF0000,stroke:#000,stroke-width:2px,color:#FFF

---

## 2. User Journey Flow

flowchart TD
    Start([Open App]) --> A[Enter Locations]
    A --> B[Select Mode]
    B --> C{Scenic?}
    C -->|Yes| D[Choose Tour Type]
    C -->|No| E[Start Journey]
    D --> F[Check Available]
    F --> G[Confirm]
    G --> H[Plan Route]
    E --> H
    H --> I[Show Map]
    I --> J[GPS Loop]
    J --> K{Near POI?}
    K -->|Yes| L[Show Card]
    K -->|No| J
    L --> M{More?}
    M -->|Yes| J
    M -->|No| End([Complete])

    style Start fill:#000,stroke:#000,stroke-width:2px,color:#FFF
    style C fill:#FF0000,stroke:#000,stroke-width:2px,color:#FFF
    style H fill:#FF0000,stroke:#000,stroke-width:2px,color:#FFF
    style End fill:#000,stroke:#000,stroke-width:2px,color:#FFF

---

## 3. Route Optimization - 3 Modes

graph LR
    subgraph M1[" MODE 1: FASTEST "]
        A1[A → B] --> B1[Direct]
        B1 --> C1[Done]
    end

    subgraph M2[" MODE 2: SCENIC AUTO "]
        A2[A → B] --> B2[Find POIs]
        B2 --> C2[Rank]
        C2 --> D2[Re-route]
    end

    subgraph M3[" MODE 3: USER SELECT "]
        A3[Show 8] --> B3[Pick 3]
        B3 --> C3[Custom]
    end

    style M1 fill:#FFF,stroke:#000,stroke-width:2px
    style M2 fill:#FFF,stroke:#FF0000,stroke-width:3px
    style M3 fill:#FFF,stroke:#000,stroke-width:2px
    style D2 fill:#FF0000,stroke:#000,color:#FFF

---

## 4. Landmark Scoring System

graph TD
    A[Input: POI] --> B{Category}
    B -->|Palace| C[+60]
    B -->|Cathedral| D[+55]
    B -->|Museum| E[+50]
    B -->|Bridge| F[+30]

    C --> G[Boost]
    D --> G
    E --> G
    F --> G

    G --> H[Total Score]
    H --> I{≥ 30?}
    I -->|Yes| J[Include]
    I -->|No| K[Exclude]

    style A fill:#000,stroke:#000,color:#FFF
    style B fill:#FF0000,stroke:#000,stroke-width:2px,color:#FFF
    style I fill:#FF0000,stroke:#000,stroke-width:2px,color:#FFF
    style J fill:#000,stroke:#000,color:#FFF
    style K fill:#FFF,stroke:#000,stroke-width:2px,color:#000

---

## 5. Data Pipeline (5 Stages)

graph LR
    A[OSM API] --> D[Merge]
    B[Wikipedia] --> D
    C[Google] --> D

    D --> E[Filter]
    E --> F[GPT-4]
    F --> G[JSON DB]
    G --> H[GitHub]
    H --> I[Deploy]
    I --> J[Live]

    style A fill:#FFF,stroke:#000,stroke-width:2px
    style B fill:#FFF,stroke:#000,stroke-width:2px
    style C fill:#FFF,stroke:#000,stroke-width:2px
    style F fill:#FF0000,stroke:#000,color:#FFF
    style G fill:#000,stroke:#000,color:#FFF
    style J fill:#FF0000,stroke:#000,stroke-width:3px,color:#FFF

---

## 6. GPS Tracking Sequence

sequenceDiagram
    participant U as User
    participant A as App
    participant G as GPS
    participant M as Map

    U->>A: Open Tour
    A->>G: Request
    G-->>U: Allow?
    U-->>G: ✓

    loop Every 3s
        G->>A: Position
        A->>A: Calculate
        alt Within 120m
            A->>M: Show Card
        else Far
            A->>M: Distance
        end
    end

---

## 7. Tour Type Filtering

graph TD
    A[User Route] --> B[API Call]
    B --> C[For Each Type]

    C --> D1[Architecture]
    C --> D2[Historical]
    C --> D3[Royal]
    C --> D4[8 more...]

    D1 --> E1{Count POIs}
    D2 --> E2{Count POIs}
    D3 --> E3{Count POIs}

    E1 -->|> 1| F1[Enable]
    E1 -->|≤ 1| G1[Disable]
    E2 -->|> 1| F2[Enable]
    E2 -->|≤ 1| G2[Disable]
    E3 -->|> 1| F3[Enable]
    E3 -->|≤ 1| G3[Disable]

    F1 --> H[UI Update]
    G1 --> H
    F2 --> H
    G2 --> H
    F3 --> H
    G3 --> H

    H --> I[Gray Out Disabled]

    style B fill:#FF0000,stroke:#000,color:#FFF
    style F1 fill:#000,stroke:#000,color:#FFF
    style F2 fill:#000,stroke:#000,color:#FFF
    style F3 fill:#000,stroke:#000,color:#FFF
    style G1 fill:#FFF,stroke:#000,stroke-width:2px
    style G2 fill:#FFF,stroke:#000,stroke-width:2px
    style G3 fill:#FFF,stroke:#000,stroke-width:2px
    style I fill:#FF0000,stroke:#000,color:#FFF

---

## 8. Performance Optimization

graph TB
    A[Problem<br/>10-15s Load] --> B[Lazy Load]
    A --> C[Bounding Box]
    A --> D[Polyline Compress]
    A --> E[Cache]
    A --> F[Haversine]

    B --> G[Solution<br/>3-5s Load]
    C --> G
    D --> G
    E --> G
    F --> G

    style A fill:#FF0000,stroke:#000,stroke-width:3px,color:#FFF
    style B fill:#FFF,stroke:#000,stroke-width:2px
    style C fill:#FFF,stroke:#000,stroke-width:2px
    style D fill:#FFF,stroke:#000,stroke-width:2px
    style E fill:#FFF,stroke:#000,stroke-width:2px
    style F fill:#FFF,stroke:#000,stroke-width:2px
    style G fill:#000,stroke:#000,stroke-width:3px,color:#FFF

---

## 9. Design Evolution Timeline

graph LR
    A[Early: Golden<br/>Peachy Glow] --> B[Mid: Pastel<br/>Dreamland]
    B --> C[Final: Black<br/>& Cream]

    A --> A1[Warm colors]
    B --> B1[8 pastels]
    C --> C1[High contrast]

    style A fill:#FFF,stroke:#000,stroke-width:2px
    style B fill:#FFF,stroke:#000,stroke-width:2px
    style C fill:#FF0000,stroke:#000,stroke-width:3px,color:#FFF
    style C1 fill:#000,stroke:#000,color:#FFF

---

## 10. Component Evolution

graph LR
    M1[Map: A/B] --> M2[Emoji Icons]
    M2 --> M3[SVG Pins]
    M3 --> M4[Reduced 50%]

    C1[Cards] --> C2[3D Flip]
    C2 --> C3[Fixed Height]
    C3 --> C4[Final Radius]

    M4 --> Final[Production]
    C4 --> Final

    style M1 fill:#FFF,stroke:#000,stroke-width:1px
    style M2 fill:#FFF,stroke:#000,stroke-width:1px
    style M3 fill:#FFF,stroke:#000,stroke-width:2px
    style M4 fill:#FF0000,stroke:#000,color:#FFF
    style C1 fill:#FFF,stroke:#000,stroke-width:1px
    style C2 fill:#FFF,stroke:#000,stroke-width:1px
    style C3 fill:#FFF,stroke:#000,stroke-width:2px
    style C4 fill:#FF0000,stroke:#000,color:#FFF
    style Final fill:#000,stroke:#000,stroke-width:3px,color:#FFF

---

## 11. Responsive Breakpoints

graph TD
    A[Device Width] --> B{Size?}

    B -->|< 390px| C[Small Mobile]
    B -->|390-428px| D[Standard Mobile]
    B -->|≥ 768px| E[Desktop]

    C --> C1[14px font]
    C --> C2[12px padding]

    D --> D1[16px font]
    D --> D2[24px padding]
    D --> D3[44px targets]

    E --> E1[iPhone Frame]
    E --> E2[Centered]

    C2 --> F[Render]
    D3 --> F
    E2 --> F

    style B fill:#FF0000,stroke:#000,stroke-width:2px,color:#FFF
    style D fill:#000,stroke:#000,stroke-width:2px,color:#FFF
    style F fill:#000,stroke:#000,stroke-width:2px,color:#FFF

---

## 12. API Cost Breakdown

graph TB
    A[Per Journey] --> B[Autocomplete<br/>$0.006]
    A --> C[Directions<br/>$0.010]
    A --> D[Hosting<br/>$0.002]

    B --> E[Total: $0.02]
    C --> E
    D --> E

    E --> F{Users?}
    F -->|100| G1[$2/mo]
    F -->|1,000| G2[$20/mo]
    F -->|10,000| G3[$200/mo]
    F -->|100,000| G4[$2,000/mo]

    G4 --> H[Optimize]
    H --> I[Save 40%]

    style A fill:#000,stroke:#000,color:#FFF
    style E fill:#FF0000,stroke:#000,stroke-width:2px,color:#FFF
    style G1 fill:#000,stroke:#000,color:#FFF
    style G2 fill:#000,stroke:#000,color:#FFF
    style G3 fill:#FFF,stroke:#000,stroke-width:2px
    style G4 fill:#FF0000,stroke:#000,color:#FFF
    style I fill:#000,stroke:#000,color:#FFF

---

## 13. State Management Flow

stateDiagram-v2
    [*] --> Landing
    Landing --> Destination
    Destination --> RouteMode
    RouteMode --> TourType: scenic
    RouteMode --> ActiveTour: fastest
    TourType --> APICheck
    APICheck --> TourType
    TourType --> ActiveTour
    ActiveTour --> GPS
    GPS --> Detection
    Detection --> Detection: tracking
    Detection --> Card: triggered
    Card --> Detection: continue
    Card --> [*]: complete

---

## Color Customization Template

Add this at the top of any diagram to ensure consistent styling:

%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#FFFFFF',
    'primaryTextColor': '#000000',
    'primaryBorderColor': '#000000',
    'lineColor': '#000000',
    'secondaryColor': '#FF0000',
    'tertiaryColor': '#FFFFFF',
    'background': '#FFFFFF',
    'mainBkg': '#FFFFFF',
    'secondBkg': '#FF0000',
    'lineColor': '#000000',
    'border1': '#000000',
    'border2': '#FF0000',
    'fontSize': '14px',
    'fontFamily': 'Arial, sans-serif'
  }
}}%%

---

## Export Settings for Mermaid Live

**Recommended Export Settings**:
- Format: **PNG** (for presentations) or **SVG** (for editing)
- Resolution: **2x** or **3x** (for crisp display)
- Width: **1920px** (standard slide width)
- Background: **Transparent** or **White**

**How to Apply Red Accent Consistently**:
- Use `fill:#FF0000` for important/active nodes
- Use `fill:#000` for start/end points
- Use `fill:#FFF,stroke:#000` for standard nodes
- Use `stroke:#FF0000,stroke-width:3px` for emphasis

---

## Usage Tips

1. **Copy Code**: Select from first line (e.g., `graph TB`) to last style line
2. **Don't Include**: The ```mermaid wrapper or this text
3. **Paste**: Directly into Mermaid Live Editor
4. **Customize**: Adjust node labels, add/remove connections
5. **Export**: Use PNG at 2x resolution for presentations

All diagrams use:
- **Black** (#000000) for text, borders, emphasis
- **White** (#FFFFFF) for backgrounds, neutral elements
- **Red** (#FF0000) for key actions, decisions, highlights
