from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from urllib.parse import quote_plus

from App.planner import plan_route
from App.landmarks import grand_landmarks_near_route
from App.config import MAX_SCENIC_SELECT_CHOICES, MAX_GRAND_MENU_ITEMS

app = FastAPI()
templates = Jinja2Templates(directory="templates")


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
    # First load: nothing computed yet
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "start": "",
            "end": "",
            "mode": "",
            "fastest": None,
            "scenic_eta": None,
            "scenic_diff": None,
            "grand_list": [],
            "result": None,
            "maps_url": None,
            "max_choices": MAX_SCENIC_SELECT_CHOICES,
        },
    )


@app.post("/", response_class=HTMLResponse)
async def handle_form(
    request: Request,
    start: str = Form(...),
    end: str = Form(...),
    mode: str = Form(""),           # may be blank on first submit
    scenic_choices: str = Form(""), # used only in Scenic Select step 2
):
    error_message = None

    try:
        # 1️⃣ Always compute fastest route (baseline)
        fastest = plan_route(start, end, "1")

        # 2️⃣ Scenic Auto preview (for times)
        scenic_eta = None
        scenic_diff = None
        scenic_preview = None
        try:
            scenic_preview = plan_route(start, end, "2")
            scenic_eta = scenic_preview["chosen_eta"]
            scenic_diff = scenic_preview["difference"]
        except Exception as e:
            print(f"[Warning] Scenic preview failed: {e}")

        # 3️⃣ Grand landmarks (for Scenic Select ONLY, when needed)
        grand_all = grand_landmarks_near_route(fastest["route_points"])
        grand_list = grand_all[:MAX_GRAND_MENU_ITEMS]

        # 4️⃣ Decide what phase we’re in
        result = None
        maps_url = None

        if mode == "1":
            result = fastest

        elif mode == "2":
            result = scenic_preview if scenic_preview is not None else plan_route(
                start, end, "2"
            )

        elif mode == "3":
            # Scenic Select: two-phase, like the terminal.
            if not scenic_choices.strip():
                # Phase 1: user has chosen mode 3, but no landmark numbers yet.
                result = None
            else:
                # Phase 2: user has entered landmark numbers. Now compute Scenic Select.
                indexes = []
                parts = scenic_choices.split(",")
                for p in parts:
                    p = p.strip()
                    if p.isdigit():
                        idx = int(p) - 1
                        if 0 <= idx < len(grand_list):
                            indexes.append(idx)

                indexes = indexes[:MAX_SCENIC_SELECT_CHOICES]
                result = plan_route(start, end, "3", indexes)

        # Build Google Maps URL only when we have a final result
        if result is not None:
            maps_url = build_google_maps_url(start, end, result["landmarks"])
        else:
            maps_url = None

        context = {
            "request": request,
            "start": start,
            "end": end,
            "mode": mode,
            "fastest": fastest,
            "scenic_eta": scenic_eta,
            "scenic_diff": scenic_diff,
            "grand_list": grand_list,
            "result": result,
            "maps_url": maps_url,
            "max_choices": MAX_SCENIC_SELECT_CHOICES,
            "error_message": error_message,
        }

    except RuntimeError as e:
        # Most likely: Google Directions error like NOT_FOUND
        error_message = str(e)
        print(f"[Route error] {error_message}")

        # On error we still want the form & inputs, but no timings/results
        context = {
            "request": request,
            "start": start,
            "end": end,
            "mode": mode,
            "fastest": None,
            "scenic_eta": None,
            "scenic_diff": None,
            "grand_list": [],
            "result": None,
            "maps_url": None,
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
):
    """
    This function runs when the user opens /track in the browser.
    It recomputes the route and sends the landmark list to the browser
    for GPS tracking.
    """

    # Recompute route depending on the mode (same logic as homepage)
    if mode == "1":
        result = plan_route(start, end, "1")
    elif mode == "2":
        result = plan_route(start, end, "2")
    else:
        # For now, scenic select reuses scenic auto path
        result = plan_route(start, end, "2")

    # Landmarks along the route
    landmarks = result["landmarks"]

    # Convert Python list → JSON text for JavaScript
    landmarks_json = json.dumps(landmarks)

    # Render the "track" page
    return templates.TemplateResponse(
        "track.html",
        {
            "request": request,
            "start": start,
            "end": end,
            "mode": mode,
            "landmarks_json": landmarks_json,
        },
    )
