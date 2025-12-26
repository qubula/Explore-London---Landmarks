from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from urllib.parse import quote_plus
import os

from App.planner import plan_route
from App.landmarks import grand_landmarks_near_route
from App.config import MAX_SCENIC_SELECT_CHOICES, MAX_GRAND_MENU_ITEMS

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mount static files for mobile web app
app.mount("/static", StaticFiles(directory="App/Web_App/static"), name="static")

# Add mobile templates directory
mobile_templates = Jinja2Templates(directory="App/Web_App/templates")


def build_google_maps_url(start: str, end: str, landmarks, travelmode: str = "walking") -> str:
    """
    Build a Google Maps directions URL with optional waypoints from landmark names.
    """
    origin = quote_plus(start)
    dest = quote_plus(end)

    if landmarks:
        names = [lm["name"] + ", London" for lm in landmarks[:5]]
        waypoints = "|".join(quote_plus(n) for n in names)
        waypoints_part = f"&waypoints={waypoints}"
    else:
        waypoints_part = ""

    return (
        f"https://www.google.com/maps/dir/?api=1"
        f"&origin={origin}"
        f"&destination={dest}"
        f"&travelmode={travelmode}"
        f"{waypoints_part}"
    )


@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    # Initial page load
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "start": "",
            "end": "",
            "mode": "1",
            "tour_type": "all",
            "grand_list": [],
            "result": None,
            "maps_url": None,
            "max_choices": MAX_SCENIC_SELECT_CHOICES,
            "error_message": None,
        },
    )


@app.post("/", response_class=HTMLResponse)
async def handle_form(
    request: Request,
    start: str = Form(...),
    end: str = Form(...),
    mode: str = Form("1"),
    tour_type: str = Form("all"),
    scenic_choices: str = Form(""),
):
    error_message = None
    grand_list = []
    result = None
    maps_url = None

    try:
        # Mode 3 (Scenic Select) requires grand landmarks list
        if mode == "3":
            # Always compute fastest route to get grand landmarks
            fastest = plan_route(start, end, "1", tour_type=tour_type)
            grand_all = grand_landmarks_near_route(
                fastest["route_points"],
                tour_type=tour_type
            )
            grand_list = grand_all[:MAX_GRAND_MENU_ITEMS]

            # If user selected landmarks, compute route
            if scenic_choices.strip():
                indexes = []
                for num in scenic_choices.split(","):
                    num = num.strip()
                    if num.isdigit():
                        idx = int(num) - 1  # Convert to 0-indexed
                        if 0 <= idx < len(grand_list):
                            indexes.append(idx)

                indexes = indexes[:MAX_SCENIC_SELECT_CHOICES]
                result = plan_route(start, end, "3", indexes, tour_type=tour_type)
            # else: show landmark selection (no result yet)

        # Mode 1 (Fastest) or Mode 2 (Scenic Auto)
        else:
            result = plan_route(start, end, mode, tour_type=tour_type)

        # Build Google Maps URL if we have a result
        if result:
            maps_url = build_google_maps_url(start, end, result["landmarks"])

    except RuntimeError as e:
        error_message = str(e)
        print(f"[Route error] {error_message}")

    context = {
        "request": request,
        "start": start,
        "end": end,
        "mode": mode,
        "tour_type": tour_type,
        "grand_list": grand_list,
        "result": result,
        "maps_url": maps_url,
        "max_choices": MAX_SCENIC_SELECT_CHOICES,
        "error_message": error_message,
    }

    return templates.TemplateResponse("index.html", context)


from fastapi import Query
import json

@app.get("/track", response_class=HTMLResponse)
async def track_page(
    request: Request,
    start: str = Query(...),
    end: str = Query(...),
    mode: str = Query("1"),
    tour_type: str = Query("all"),
):
    """
    GPS tracking page for live audio tour.
    """
    # Recompute route with tour type
    if mode == "1":
        result = plan_route(start, end, "1", tour_type=tour_type)
    elif mode == "2":
        result = plan_route(start, end, "2", tour_type=tour_type)
    else:
        # Scenic select defaults to scenic auto for tracking
        result = plan_route(start, end, "2", tour_type=tour_type)

    landmarks = result["landmarks"]
    landmarks_json = json.dumps(landmarks)

    return templates.TemplateResponse(
        "track.html",
        {
            "request": request,
            "start": start,
            "end": end,
            "mode": mode,
            "tour_type": tour_type,
            "landmarks_json": landmarks_json,
        },
    )


# ==================== MOBILE WEB APP ROUTES ====================

@app.get("/mobile", response_class=HTMLResponse)
async def mobile_home(request: Request):
    """Mobile app landing page"""
    google_maps_key = os.getenv("GOOGLE_DIRECTIONS_KEY", "")
    return mobile_templates.TemplateResponse(
        "mobile/index.html",
        {"request": request, "google_maps_key": google_maps_key}
    )


@app.get("/mobile/destination", response_class=HTMLResponse)
async def mobile_destination(request: Request):
    """Mobile destination selection page"""
    google_maps_key = os.getenv("GOOGLE_DIRECTIONS_KEY", "")
    return mobile_templates.TemplateResponse(
        "mobile/destination.html",
        {"request": request, "google_maps_key": google_maps_key}
    )


@app.get("/mobile/route-mode", response_class=HTMLResponse)
async def mobile_route_mode(request: Request):
    """Mobile route mode selection page"""
    return mobile_templates.TemplateResponse(
        "mobile/route_mode.html",
        {"request": request}
    )


@app.get("/mobile/tour-type", response_class=HTMLResponse)
async def mobile_tour_type(request: Request):
    """Mobile tour type selection page"""
    return mobile_templates.TemplateResponse(
        "mobile/tour_type.html",
        {"request": request}
    )


@app.get("/mobile/tour", response_class=HTMLResponse)
async def mobile_tour(request: Request):
    """Mobile active tour page"""
    google_maps_key = os.getenv("GOOGLE_DIRECTIONS_KEY", "")
    return mobile_templates.TemplateResponse(
        "mobile/tour.html",
        {"request": request, "google_maps_key": google_maps_key}
    )


@app.post("/api/check-tour-availability")
async def api_check_tour_availability(request: Request):
    """Check which tour types have landmarks for the given route"""
    try:
        data = await request.json()
        start = data.get("start")
        end = data.get("end")
        mode = data.get("mode", "1")

        if not start or not end:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Start and end locations are required"}
            )

        # Define all tour types to check
        tour_types = [
            'architecture', 'historical', 'royal', 'modern',
            'museums_galleries', 'parks_gardens', 'religious', 'victorian', 'all'
        ]

        # Check each tour type for landmarks
        availability = {}
        for tour_type in tour_types:
            result = plan_route(start, end, mode, tour_type=tour_type)
            # Check if there are any landmarks in the result
            landmark_count = len(result.get('landmarks', []))
            availability[tour_type] = landmark_count > 0

        return JSONResponse(content={"status": "success", "availability": availability})

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )


@app.post("/api/plan-route")
async def api_plan_route(request: Request):
    """API endpoint for mobile app route planning"""
    try:
        data = await request.json()
        start = data.get("start")
        end = data.get("end")
        mode = data.get("mode", "1")
        tour_type = data.get("tour_type", "all")

        if not start or not end:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Start and end locations are required"}
            )

        # Plan the route
        result = plan_route(start, end, mode, tour_type=tour_type)

        return JSONResponse(content={"status": "success", "result": result})

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )
