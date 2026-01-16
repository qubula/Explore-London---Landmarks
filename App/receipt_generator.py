"""
receipt_generator.py

Generates thermal printer receipts for PassingBy tours.
Creates a formatted text receipt with all landmarks visited during the tour,
plus a static map image showing the route.

Thermal printer specifications:
- Width: 80mm (302 dots) or 58mm (203 dots)
- Character width: 32-48 characters per line
- Supports text alignment and basic formatting
- Can print images (384x384px recommended for map snapshots)

INTEGRATION EXAMPLE:
-------------------
from App.planner import plan_route
from App.receipt_generator import generate_tour_receipt, generate_route_map

# Plan the route
result = plan_route(
    start="King's Cross Station, London",
    end="Waterloo Station, London",
    mode="2",  # Scenic Auto
    tour_type="historical"
)

# Generate text receipt
receipt_text = generate_tour_receipt(
    landmarks=result["landmarks"],
    tour_type=result["tour_type"],
    route_mode=result["mode"],
    start_location="King's Cross Station",
    end_location="Waterloo Station",
    journey_time=f"{int(result['chosen_eta'])} min"
)

# Generate map image
map_path = generate_route_map(
    route_points=result["route_points"],
    start_coords=result["route_points"][0],  # First point
    end_coords=result["route_points"][-1]    # Last point
)

# Print both to thermal printer
# (printer-specific code here)
"""

from datetime import datetime
from typing import List, Dict, Tuple
import os
import requests
import polyline


def format_receipt_line(text: str, width: int = 32, align: str = 'left') -> str:
    """
    Format a line of text for thermal printer.

    Args:
        text: Text to format
        width: Character width (default 32 for 58mm paper)
        align: Alignment ('left', 'center', 'right')

    Returns:
        Formatted line with proper padding
    """
    if len(text) > width:
        text = text[:width-3] + '...'

    if align == 'center':
        return text.center(width)
    elif align == 'right':
        return text.rjust(width)
    else:
        return text.ljust(width)


def generate_tour_receipt(
    landmarks: List[Dict],
    tour_type: str = "all",
    route_mode: str = "Fastest",
    start_location: str = "",
    end_location: str = "",
    journey_time: str = ""
) -> str:
    """
    Generate a thermal printer receipt for a completed tour.

    Args:
        landmarks: List of landmark dicts with 'name' and location info
        tour_type: Type of tour (e.g., "architecture", "historical", "all")
        route_mode: Route mode used (e.g., "Fastest", "Scenic Auto")
        start_location: Starting address
        end_location: Ending address
        journey_time: Total journey time

    Returns:
        Formatted receipt string ready for thermal printer
    """
    WIDTH = 32  # Characters per line for 58mm paper
    receipt = []

    # Header
    receipt.append("=" * WIDTH)
    receipt.append(format_receipt_line("PASSINGBY", WIDTH, 'center'))
    receipt.append(format_receipt_line("London Tour Guide", WIDTH, 'center'))
    receipt.append("=" * WIDTH)
    receipt.append("")

    # Tour date and time
    now = datetime.now()
    date_str = now.strftime("%d %B %Y")
    time_str = now.strftime("%H:%M")
    receipt.append(format_receipt_line(f"Date: {date_str}", WIDTH))
    receipt.append(format_receipt_line(f"Time: {time_str}", WIDTH))
    receipt.append("")

    # Tour details
    receipt.append(format_receipt_line("TOUR DETAILS", WIDTH, 'center'))
    receipt.append("-" * WIDTH)

    # Format tour type name
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

    receipt.append(format_receipt_line(f"Theme: {tour_display}", WIDTH))
    receipt.append(format_receipt_line(f"Route: {route_mode}", WIDTH))

    if journey_time:
        receipt.append(format_receipt_line(f"Duration: {journey_time}", WIDTH))

    receipt.append("")

    # Route summary (if available)
    if start_location or end_location:
        receipt.append(format_receipt_line("ROUTE", WIDTH, 'center'))
        receipt.append("-" * WIDTH)

        if start_location:
            # Wrap long addresses
            start_parts = wrap_text(f"From: {start_location}", WIDTH - 6)
            receipt.append(format_receipt_line(start_parts[0], WIDTH))
            for part in start_parts[1:]:
                receipt.append(format_receipt_line(f"      {part}", WIDTH))

        if end_location:
            end_parts = wrap_text(f"To: {end_location}", WIDTH - 4)
            receipt.append(format_receipt_line(end_parts[0], WIDTH))
            for part in end_parts[1:]:
                receipt.append(format_receipt_line(f"    {part}", WIDTH))

        receipt.append("")

    # Landmarks section
    receipt.append(format_receipt_line("LANDMARKS VISITED", WIDTH, 'center'))
    receipt.append("=" * WIDTH)
    receipt.append("")

    if landmarks:
        for i, landmark in enumerate(landmarks, 1):
            name = landmark.get('name', 'Unknown')

            # Landmark number and name
            receipt.append(format_receipt_line(f"{i}. {name}", WIDTH))

            # Location/postcode (if available in landmark data)
            location = landmark.get('location', '')
            postcode = landmark.get('postcode', '')

            if postcode:
                receipt.append(format_receipt_line(f"   {postcode}", WIDTH))
            elif location:
                receipt.append(format_receipt_line(f"   {location}", WIDTH))

            # Add small gap between landmarks
            if i < len(landmarks):
                receipt.append("")

        receipt.append("")
        receipt.append("-" * WIDTH)
        receipt.append(format_receipt_line(f"Total: {len(landmarks)} landmarks", WIDTH, 'center'))
    else:
        receipt.append(format_receipt_line("No landmarks on route", WIDTH, 'center'))

    receipt.append("")

    # Footer
    receipt.append("=" * WIDTH)
    receipt.append(format_receipt_line("Thank you for using", WIDTH, 'center'))
    receipt.append(format_receipt_line("PASSINGBY", WIDTH, 'center'))
    receipt.append("")
    receipt.append(format_receipt_line("www.passingby.uk", WIDTH, 'center'))
    receipt.append("=" * WIDTH)

    # Add extra lines for paper tear-off
    receipt.append("")
    receipt.append("")
    receipt.append("")

    return "\n".join(receipt)


def wrap_text(text: str, max_width: int) -> List[str]:
    """
    Wrap text to fit within max_width, breaking at word boundaries.

    Args:
        text: Text to wrap
        max_width: Maximum characters per line

    Returns:
        List of wrapped lines
    """
    if len(text) <= max_width:
        return [text]

    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        word_length = len(word)
        # +1 for space
        if current_length + word_length + len(current_line) <= max_width:
            current_line.append(word)
            current_length += word_length
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = word_length

    if current_line:
        lines.append(' '.join(current_line))

    return lines


def generate_route_map(
    route_points: List[Tuple[float, float]],
    start_coords: Tuple[float, float] = None,
    end_coords: Tuple[float, float] = None,
    output_path: str = None,
    width: int = 384,
    height: int = 384
) -> str:
    """
    Generate a static map image with the route line using Google Static Maps API.

    NOTE: Requires Google Static Maps API to be enabled in Google Cloud Console.
    Uses the GOOGLE_DIRECTIONS_KEY environment variable for authentication.

    Args:
        route_points: List of (lat, lng) tuples defining the route polyline
        start_coords: Optional (lat, lng) tuple for start marker
        end_coords: Optional (lat, lng) tuple for end marker
        output_path: Path to save the image (auto-generated if not provided)
        width: Map width in pixels (default 384 for thermal printers)
        height: Map height in pixels (default 384)

    Returns:
        Path to saved map image file

    Raises:
        ValueError: If GOOGLE_DIRECTIONS_KEY environment variable is not set
        RuntimeError: If Google Static Maps API request fails
    """
    api_key = os.getenv("GOOGLE_DIRECTIONS_KEY")
    if not api_key:
        raise ValueError("GOOGLE_DIRECTIONS_KEY environment variable not set")

    # Encode route points as polyline for Google Static Maps
    encoded_polyline = polyline.encode(route_points)

    # Build Static Maps API URL
    base_url = "https://maps.googleapis.com/maps/api/staticmap"

    params = {
        "size": f"{width}x{height}",
        "key": api_key,
        "format": "png",
        "maptype": "roadmap",
    }

    # Add route polyline
    params["path"] = f"enc:{encoded_polyline}|color:0xFAF8F3|weight:3"

    # Add start marker (white rounded rectangle - approximated with white marker)
    if start_coords:
        params["markers"] = f"color:white|label:S|{start_coords[0]},{start_coords[1]}"

    # Add end marker (gray circle - approximated with gray marker)
    if end_coords:
        if "markers" in params:
            params["markers"] += f"&markers=color:gray|label:E|{end_coords[0]},{end_coords[1]}"
        else:
            params["markers"] = f"color:gray|label:E|{end_coords[0]},{end_coords[1]}"

    # Make request to Google Static Maps API
    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        raise RuntimeError(f"Google Static Maps API error: {response.status_code}")

    # Save image
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"route_map_{timestamp}.png"

    with open(output_path, 'wb') as f:
        f.write(response.content)

    return output_path


def save_receipt_to_file(receipt_text: str, filename: str = None) -> str:
    """
    Save receipt to a text file.

    Args:
        receipt_text: Formatted receipt string
        filename: Optional filename (auto-generated if not provided)

    Returns:
        Path to saved file
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"receipt_{timestamp}.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(receipt_text)

    return filename


# Example usage
if __name__ == "__main__":
    # Load environment variables for testing
    from dotenv import load_dotenv
    load_dotenv()

    # Sample landmark data
    sample_landmarks = [
        {
            "name": "Big Ben",
            "postcode": "SW1A 0AA",
            "location": "Westminster"
        },
        {
            "name": "Tower Bridge",
            "postcode": "SE1 2UP",
            "location": "Tower Hamlets"
        },
        {
            "name": "St Paul's Cathedral",
            "postcode": "EC4M 8AD",
            "location": "City of London"
        },
        {
            "name": "British Museum",
            "postcode": "WC1B 3DG",
            "location": "Bloomsbury"
        }
    ]

    # Generate receipt
    receipt = generate_tour_receipt(
        landmarks=sample_landmarks,
        tour_type="historical",
        route_mode="Scenic Auto",
        start_location="King's Cross Station",
        end_location="Waterloo Station",
        journey_time="25 min"
    )

    # Print to console
    print(receipt)

    # Save to file
    filename = save_receipt_to_file(receipt)
    print(f"\nReceipt saved to: {filename}")

    # Generate route map (example route points)
    # In real usage, these would come from the planner.py route_points
    sample_route = [
        (51.5309, -0.1233),  # King's Cross
        (51.5074, -0.1278),  # British Museum area
        (51.5138, -0.0984),  # St Paul's
        (51.5007, -0.1246),  # Westminster
        (51.5055, -0.0754),  # Tower Bridge
        (51.5033, -0.1195),  # Waterloo
    ]

    try:
        map_path = generate_route_map(
            route_points=sample_route,
            start_coords=(51.5309, -0.1233),  # King's Cross
            end_coords=(51.5033, -0.1195),    # Waterloo
        )
        print(f"Route map saved to: {map_path}")
    except Exception as e:
        print(f"Could not generate map: {e}")
