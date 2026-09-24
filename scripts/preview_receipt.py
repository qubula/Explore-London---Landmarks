"""
preview_receipt.py

Generate and preview a visual receipt with realistic thermal printer simulation.
Creates a side-by-side comparison showing the actual receipt and a scaled preview.
"""

from App.receipt_generator import generate_visual_receipt
from PIL import Image, ImageDraw, ImageFont
import os


def create_thermal_preview(receipt_path: str) -> str:
    """
    Create a realistic preview of how the receipt will look when printed.
    Adds paper texture and scaling for better visualization.
    """
    # Load the receipt
    receipt = Image.open(receipt_path)

    # Create a larger canvas to show the receipt at 2x scale for better visibility
    scale = 2
    preview_width = receipt.width * scale
    preview_height = receipt.height * scale

    # Create white background (simulating thermal paper)
    preview = Image.new('RGB', (preview_width + 40, preview_height + 80), '#f5f5f0')

    # Scale up the receipt
    receipt_scaled = receipt.resize((preview_width, preview_height), Image.Resampling.NEAREST)

    # Paste onto background with margins
    preview.paste(receipt_scaled, (20, 40))

    # Add label at top
    draw = ImageDraw.Draw(preview)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except:
        font = ImageFont.load_default()

    label = "THERMAL RECEIPT PREVIEW (2x scale)"
    draw.text((20, 10), label, font=font, fill="black")

    # Add dimensions at bottom
    dims = f"Actual size: {receipt.width}px × {receipt.height}px (58mm × {receipt.height * 0.125:.1f}mm)"
    draw.text((20, preview_height + 50), dims, font=font, fill="gray")

    # Save preview to iterations folder
    preview_filename = os.path.basename(receipt_path).replace('.png', '_preview.png')
    preview_path = os.path.join('Receipt_Iterations', preview_filename)
    preview.save(preview_path)

    return preview_path


if __name__ == "__main__":
    print("=" * 60)
    print("THERMAL RECEIPT PREVIEW GENERATOR")
    print("=" * 60)
    print()

    # Sample data for a realistic tour
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
        },
        {
            "name": "The Shard",
            "location": "Southwark"
        }
    ]

    # Sample route
    sample_route = [
        (51.5309, -0.1233),  # King's Cross
        (51.5074, -0.1278),  # British Museum
        (51.5138, -0.0984),  # St Paul's
        (51.5007, -0.1246),  # Westminster (Big Ben)
        (51.5055, -0.0754),  # Tower Bridge
        (51.5045, -0.0865),  # The Shard
    ]

    # Ensure iterations folder exists
    os.makedirs('Receipt_Iterations', exist_ok=True)

    print("Generating visual receipt...")
    receipt_path = generate_visual_receipt(
        landmarks=sample_landmarks,
        tour_type="historical",
        route_mode="Scenic Auto",
        start_location="King's Cross Station, London",
        end_location="London Bridge Station, London",
        journey_time="38 min",
        route_points=sample_route
    )

    # Move receipt to iterations folder
    receipt_filename = os.path.basename(receipt_path)
    new_receipt_path = os.path.join('Receipt_Iterations', receipt_filename)
    os.rename(receipt_path, new_receipt_path)
    receipt_path = new_receipt_path

    print(f"✓ Receipt generated: {receipt_path}")
    print()

    print("Creating thermal preview (2x scale)...")
    preview_path = create_thermal_preview(receipt_path)
    print(f"✓ Preview created: {preview_path}")
    print()

    # Open preview in default image viewer (not HTML)
    print("Opening preview in default image viewer...")
    os.system(f'open "{preview_path}"')

    print()
    print("=" * 60)
    print("RECEIPT SPECIFICATIONS")
    print("=" * 60)
    print(f"Width: 384 pixels (58mm / 2.25 inches)")
    print(f"Resolution: 203 DPI")
    print(f"Format: 1-bit monochrome (optimized for thermal)")
    print(f"Paper: Standard 58mm thermal printer roll")
    print()
    print("The preview shows the receipt at 2x scale for easier viewing.")
    print("Actual printed size will be narrower (58mm wide).")
    print("=" * 60)
