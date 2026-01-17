"""
receipt_generator.py

Generates highly visual, aesthetically curated thermal printer receipts for PassingBy tours.
Creates a beautiful graphical receipt with embedded map, typography, and design elements.

Thermal printer specifications:
- Width: 58mm (384 pixels at 203 DPI)
- Outputs monochrome 1-bit dithered PNG images
- Optimized for ESC/POS thermal printers

INTEGRATION EXAMPLE:
-------------------
from App.planner import plan_route
from App.receipt_generator import generate_visual_receipt

# Plan the route
result = plan_route(
    start="King's Cross Station, London",
    end="Waterloo Station, London",
    mode="2",  # Scenic Auto
    tour_type="historical"
)

# Generate visual receipt
receipt_path = generate_visual_receipt(
    landmarks=result["landmarks"],
    tour_type=result["tour_type"],
    route_mode=result["mode"],
    start_location="King's Cross Station",
    end_location="Waterloo Station",
    journey_time=f"{int(result['chosen_eta'])} min",
    route_points=result["route_points"]
)

# Send receipt_path to thermal printer
"""

from datetime import datetime
from typing import List, Dict, Tuple
import os
import requests
import polyline
from PIL import Image, ImageDraw, ImageFont


# Configuration
PRINTER_WIDTH_PX = 384  # Standard width for 58mm thermal printers (203 DPI)
PADDING = 20
FONT_SIZE_TITLE = 38
FONT_SIZE_HEADER = 24
FONT_SIZE_BODY = 18
FONT_SIZE_SMALL = 14
FONT_SIZE_TINY = 12


def get_font(size: int, bold: bool = False):
    """
    Load system fonts with fallback to PIL default.
    Tries to use Helvetica/Arial for clean, modern aesthetics.
    """
    font_names = []

    if bold:
        font_names = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/SFNSDisplay.ttf",
            "Arial Bold",
            "Helvetica Bold"
        ]
    else:
        font_names = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/SFNSDisplay.ttf",
            "Arial",
            "Helvetica"
        ]

    for font_name in font_names:
        try:
            return ImageFont.truetype(font_name, size)
        except:
            continue

    # Ultimate fallback
    return ImageFont.load_default()


def draw_separator(draw, y, width, thickness=2, style="solid"):
    """
    Draw stylistic horizontal lines.

    Args:
        style: "solid", "double", or "dashed"
    """
    if style == "solid":
        draw.line([(0, y), (width, y)], fill="black", width=thickness)
        return y + thickness + 10
    elif style == "double":
        draw.line([(0, y), (width, y)], fill="black", width=1)
        draw.line([(0, y + 3), (width, y + 3)], fill="black", width=1)
        return y + 13
    elif style == "dashed":
        dash_length = 10
        gap_length = 5
        x = 0
        while x < width:
            draw.line([(x, y), (min(x + dash_length, width), y)], fill="black", width=thickness)
            x += dash_length + gap_length
        return y + thickness + 10


def wrap_text_pixels(text: str, font, max_width: int, draw_obj) -> List[str]:
    """
    Intelligently wrap text to fit pixel width using specific font metrics.
    """
    lines = []
    words = text.split()
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw_obj.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]

        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    return lines if lines else [text]


def fetch_route_map(
    route_points: List[Tuple[float, float]],
    start_coords: Tuple[float, float] = None,
    end_coords: Tuple[float, float] = None,
    width: int = 384,
    height: int = 250
) -> Image.Image:
    """
    Fetch map from Google Static Maps API and return as PIL Image.
    Converts to grayscale and applies high contrast for thermal printing.
    """
    api_key = os.getenv("GOOGLE_DIRECTIONS_KEY")
    if not api_key:
        print("Warning: GOOGLE_DIRECTIONS_KEY not set, skipping map")
        return None

    encoded_polyline = polyline.encode(route_points)
    base_url = "https://maps.googleapis.com/maps/api/staticmap"

    # Build markers list properly
    markers_list = []
    if start_coords:
        markers_list.append(f"color:0x000000|label:S|{start_coords[0]},{start_coords[1]}")
    if end_coords:
        markers_list.append(f"color:0x000000|label:E|{end_coords[0]},{end_coords[1]}")

    params = {
        "size": f"{width}x{height}",
        "key": api_key,
        "format": "png",
        "maptype": "roadmap",
        "style": [
            "feature:all|element:all|saturation:-100",  # Black and white
            "feature:all|element:geometry|lightness:20",  # Lighter background
            "feature:road|element:geometry|lightness:40",  # Even lighter roads
        ],
        "path": f"enc:{encoded_polyline}|color:0x000000ff|weight:4"  # Black route line
    }

    # Add markers as list
    if markers_list:
        params["markers"] = markers_list

    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            from io import BytesIO
            map_img = Image.open(BytesIO(response.content))
            # Convert to grayscale and increase contrast
            map_img = map_img.convert('L')
            return map_img
    except Exception as e:
        print(f"Error fetching map: {e}")

    return None


def generate_visual_receipt(
    landmarks: List[Dict],
    tour_type: str = "all",
    route_mode: str = "Fastest",
    start_location: str = "",
    end_location: str = "",
    journey_time: str = "",
    route_points: List[Tuple[float, float]] = None
) -> str:
    """
    Generate a highly visual, aesthetically curated receipt image for thermal printing.

    Args:
        landmarks: List of landmark dicts with 'name' and location info
        tour_type: Type of tour (e.g., "architecture", "historical", "all")
        route_mode: Route mode used (e.g., "Fastest", "Scenic Auto")
        start_location: Starting address
        end_location: Ending address
        journey_time: Total journey time (e.g., "25 min")
        route_points: List of (lat, lng) tuples for the route (optional, for map)

    Returns:
        Path to saved receipt PNG file
    """

    # Setup canvas (start tall, crop to content later)
    MAX_HEIGHT = 4000
    content_width = PRINTER_WIDTH_PX - (PADDING * 2)

    img = Image.new('RGB', (PRINTER_WIDTH_PX, MAX_HEIGHT), 'white')
    draw = ImageDraw.Draw(img)

    # Define fonts
    font_title = get_font(FONT_SIZE_TITLE, bold=True)
    font_header = get_font(FONT_SIZE_HEADER, bold=True)
    font_body = get_font(FONT_SIZE_BODY, bold=False)
    font_small = get_font(FONT_SIZE_SMALL, bold=False)
    font_tiny = get_font(FONT_SIZE_TINY, bold=False)

    cursor_y = PADDING

    # ==================== HEADER ====================
    # Large centered title
    title_text = "PASSINGBY"
    bbox = draw.textbbox((0, 0), title_text, font=font_title)
    title_w = bbox[2] - bbox[0]
    draw.text(((PRINTER_WIDTH_PX - title_w) / 2, cursor_y), title_text, font=font_title, fill="black")
    cursor_y += 48

    # Subtitle
    subtitle = "London Tour Guide"
    bbox = draw.textbbox((0, 0), subtitle, font=font_small)
    sub_w = bbox[2] - bbox[0]
    draw.text(((PRINTER_WIDTH_PX - sub_w) / 2, cursor_y), subtitle, font=font_small, fill="black")
    cursor_y += 28

    # Heavy separator
    cursor_y = draw_separator(draw, cursor_y, PRINTER_WIDTH_PX, thickness=3, style="solid")

    # ==================== MAP SECTION ====================
    if route_points:
        start_coords = route_points[0] if route_points else None
        end_coords = route_points[-1] if route_points else None
        map_img = fetch_route_map(route_points, start_coords, end_coords)

        if map_img:
            # Resize to full width maintaining aspect ratio
            aspect = map_img.height / map_img.width
            new_height = int(PRINTER_WIDTH_PX * aspect)
            map_img = map_img.resize((PRINTER_WIDTH_PX, new_height), Image.Resampling.LANCZOS)
            img.paste(map_img, (0, cursor_y))
            cursor_y += new_height + 20

    # ==================== METADATA GRID ====================
    now = datetime.now()
    date_str = now.strftime("%d.%m.%y")
    time_str = now.strftime("%H:%M")

    # Left: Date/Time
    draw.text((PADDING, cursor_y), f"DATE", font=font_tiny, fill="black")
    draw.text((PADDING, cursor_y + 16), date_str, font=font_body, fill="black")

    draw.text((PADDING, cursor_y + 40), f"TIME", font=font_tiny, fill="black")
    draw.text((PADDING, cursor_y + 56), time_str, font=font_body, fill="black")

    # Right: Duration (large, right-aligned)
    if journey_time:
        bbox = draw.textbbox((0, 0), journey_time, font=font_header)
        dur_w = bbox[2] - bbox[0]
        draw.text((PRINTER_WIDTH_PX - PADDING - dur_w, cursor_y), journey_time, font=font_header, fill="black")

        lbl_text = "DURATION"
        bbox = draw.textbbox((0, 0), lbl_text, font=font_tiny)
        lbl_w = bbox[2] - bbox[0]
        draw.text((PRINTER_WIDTH_PX - PADDING - lbl_w, cursor_y + 28), lbl_text, font=font_tiny, fill="black")

    cursor_y += 90
    cursor_y = draw_separator(draw, cursor_y, PRINTER_WIDTH_PX, thickness=1, style="solid")

    # ==================== ROUTE DETAILS ====================
    cursor_y += 5

    # Tour type mapping
    tour_name_map = {
        "architecture": "Architecture",
        "historical": "History",
        "royal": "Royal",
        "modern": "Modern",
        "museums_galleries": "Museums & Galleries",
        "parks_gardens": "Parks & Gardens",
        "religious": "Religious",
        "victorian": "Victorian",
        "all": "Surprise Me"
    }
    tour_display = tour_name_map.get(tour_type, tour_type.title())

    # Mode and Theme
    draw.text((PADDING, cursor_y), f"MODE", font=font_tiny, fill="black")
    draw.text((PADDING, cursor_y + 16), route_mode.upper(), font=font_body, fill="black")
    cursor_y += 40

    draw.text((PADDING, cursor_y), f"THEME", font=font_tiny, fill="black")
    draw.text((PADDING, cursor_y + 16), tour_display.upper(), font=font_body, fill="black")
    cursor_y += 45

    # From / To
    if start_location:
        draw.text((PADDING, cursor_y), "FROM", font=font_tiny, fill="black")
        cursor_y += 16
        wrapped_start = wrap_text_pixels(start_location, font_small, content_width, draw)
        for line in wrapped_start:
            draw.text((PADDING, cursor_y), line, font=font_small, fill="black")
            cursor_y += 18
        cursor_y += 10

    if end_location:
        draw.text((PADDING, cursor_y), "TO", font=font_tiny, fill="black")
        cursor_y += 16
        wrapped_end = wrap_text_pixels(end_location, font_small, content_width, draw)
        for line in wrapped_end:
            draw.text((PADDING, cursor_y), line, font=font_small, fill="black")
            cursor_y += 18

    cursor_y += 25
    cursor_y = draw_separator(draw, cursor_y, PRINTER_WIDTH_PX, thickness=3, style="solid")

    # ==================== LANDMARKS LIST ====================
    # Centered header
    header = "LANDMARKS VISITED"
    bbox = draw.textbbox((0, 0), header, font=font_header)
    h_w = bbox[2] - bbox[0]
    draw.text(((PRINTER_WIDTH_PX - h_w) / 2, cursor_y + 15), header, font=font_header, fill="black")
    cursor_y += 55

    if landmarks:
        for i, lm in enumerate(landmarks, 1):
            name = lm.get('name', 'Unknown')
            loc = lm.get('location', '')

            # Number circle (left)
            num_str = f"{i:02d}"
            draw.text((PADDING, cursor_y), num_str, font=font_body, fill="black")

            # Name (indented, bold)
            name_lines = wrap_text_pixels(name, font_body, content_width - 45, draw)
            for line in name_lines:
                draw.text((PADDING + 40, cursor_y), line, font=font_body, fill="black")
                cursor_y += 22

            # Location (small, uppercase)
            if loc:
                draw.text((PADDING + 40, cursor_y), loc.upper(), font=font_tiny, fill="black")
                cursor_y += 18

            cursor_y += 18  # Gap between items
    else:
        no_text = "No landmarks recorded"
        bbox = draw.textbbox((0, 0), no_text, font=font_small)
        w = bbox[2] - bbox[0]
        draw.text(((PRINTER_WIDTH_PX - w) / 2, cursor_y), no_text, font=font_small, fill="black")
        cursor_y += 35

    cursor_y += 15
    cursor_y = draw_separator(draw, cursor_y, PRINTER_WIDTH_PX, thickness=1, style="dashed")

    # ==================== FOOTER ====================
    cursor_y += 20

    # Total count badge
    if landmarks:
        total_text = f"{len(landmarks)} LANDMARKS"
        bbox = draw.textbbox((0, 0), total_text, font=font_small)
        t_w = bbox[2] - bbox[0]
        # Draw rounded rectangle background (simulate with rectangle)
        padding = 8
        draw.rectangle(
            [(PRINTER_WIDTH_PX - t_w) / 2 - padding, cursor_y - 4,
             (PRINTER_WIDTH_PX + t_w) / 2 + padding, cursor_y + 18],
            outline="black", width=2
        )
        draw.text(((PRINTER_WIDTH_PX - t_w) / 2, cursor_y), total_text, font=font_small, fill="black")
        cursor_y += 35

    # Website
    footer_text = "www.passingby.uk"
    bbox = draw.textbbox((0, 0), footer_text, font=font_body)
    f_w = bbox[2] - bbox[0]
    draw.text(((PRINTER_WIDTH_PX - f_w) / 2, cursor_y), footer_text, font=font_body, fill="black")
    cursor_y += 40

    # ==================== FINALIZE IMAGE ====================
    # Crop to actual content + padding for tear-off
    final_height = cursor_y + 80
    final_img = img.crop((0, 0, PRINTER_WIDTH_PX, final_height))

    # Convert to 1-bit monochrome with Floyd-Steinberg dithering
    # This is CRITICAL for thermal printers to achieve proper contrast
    final_img = final_img.convert('1')

    # Save with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"receipt_visual_{timestamp}.png"
    final_img.save(filename, dpi=(203, 203))  # Specify DPI for thermal printer

    return filename


# Example usage
if __name__ == "__main__":
    # Load environment variables for testing
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        pass

    # Sample landmark data
    sample_landmarks = [
        {
            "name": "Big Ben",
            "location": "Westminster"
        },
        {
            "name": "Tower Bridge",
            "location": "Tower Hamlets"
        },
        {
            "name": "St Paul's Cathedral",
            "location": "City of London"
        },
        {
            "name": "British Museum",
            "location": "Bloomsbury"
        }
    ]

    # Sample route points
    sample_route = [
        (51.5309, -0.1233),  # King's Cross
        (51.5074, -0.1278),  # British Museum area
        (51.5138, -0.0984),  # St Paul's
        (51.5007, -0.1246),  # Westminster
        (51.5055, -0.0754),  # Tower Bridge
        (51.5033, -0.1195),  # Waterloo
    ]

    # Generate visual receipt
    print("Generating visual receipt...")
    output_file = generate_visual_receipt(
        landmarks=sample_landmarks,
        tour_type="historical",
        route_mode="Scenic Auto",
        start_location="King's Cross Station, London",
        end_location="Waterloo Station, London",
        journey_time="25 min",
        route_points=sample_route
    )

    print(f"✓ Receipt saved to: {output_file}")
    print("  Ready for thermal printer")
    print("  384px wide, 1-bit monochrome, 203 DPI")
