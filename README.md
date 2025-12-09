# Alfie - London Walking Tour Guide

A tour guide app that plans scenic walking routes through London and triggers landmark information based on GPS location.

## Features

- **3 Route Modes:**
  - Fastest: Direct route
  - Scenic Auto: Automatically chooses scenic route
  - Scenic Select: Choose up to 3 landmarks to visit

- **Live GPS Tracking:** Real-time landmark triggers as you walk
- **2,500+ London Landmarks:** Curated from Wikipedia
- **Google Places Integration:** Top 100 landmarks ranked by visitor ratings
- **Smart Triggering:** Dynamic radius based on landmark size (30-120m)

## Deployment

### Railway.app (Recommended)

1. Push to GitHub
2. Connect Railway to your repo
3. Add environment variables:
   - `GOOGLE_DIRECTIONS_KEY`
   - `OPENAI_API_KEY`
4. Deploy!

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python server.py

# Open browser
http://localhost:8000
```

## Tech Stack

- **Backend:** FastAPI, Python 3.9+
- **APIs:** Google Directions, Google Places, OpenAI
- **Frontend:** HTML, JavaScript (vanilla)
- **Data:** GeoJSON, Wikipedia

## Project Structure

```
V4/
├── App/                    # Core application logic
│   ├── config.py          # Configuration constants
│   ├── landmarks.py       # Landmark scoring
│   ├── planner.py         # Route planning
│   └── route_landmark_finder.py
├── Data/                   # Landmark database
├── templates/              # HTML templates
│   ├── index.html         # Route planner
│   └── track.html         # GPS tracking
└── server.py              # FastAPI server
```

## Credits

Built for Unit 9 Personal Project
Generated with Claude Code
