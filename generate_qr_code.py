#!/usr/bin/env python3
"""
QR Code Generator for PassingBy Taxi App
Generates a QR code that passengers can scan in the cab
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# Your app URL - replace with your custom domain when ready
APP_URL = "https://www.passingby.uk/mobile"

def generate_qr_code(url, filename="passingby_qr_code.png", with_logo=False):
    """
    Generate a QR code for the PassingBy app

    Args:
        url: The URL to encode in the QR code
        filename: Output filename for the QR code
        with_logo: Whether to add the PassingBy logo in the center
    """

    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,  # Controls size (1 is smallest, auto-adjusts)
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for logo overlay
        box_size=10,  # Size of each box in pixels
        border=4,  # Border size in boxes
    )

    # Add data
    qr.add_data(url)
    qr.make(fit=True)

    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Convert to RGB for logo overlay
    qr_img = qr_img.convert('RGB')

    # Add logo in center if requested
    if with_logo:
        logo_path = "App/Logo/LogoPassingBy.png"
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)

            # Calculate logo size (about 20% of QR code)
            qr_width, qr_height = qr_img.size
            logo_size = qr_width // 5

            # Resize logo
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

            # Add white background behind logo for better scanning
            logo_bg = Image.new('RGB', (logo_size + 20, logo_size + 20), 'white')
            logo_bg_pos = ((qr_width - logo_size - 20) // 2, (qr_height - logo_size - 20) // 2)
            qr_img.paste(logo_bg, logo_bg_pos)

            # Paste logo
            logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            qr_img.paste(logo, logo_pos)

    # Save
    qr_img.save(filename)
    print(f"✓ QR code saved to: {filename}")
    print(f"  URL: {url}")
    print(f"  Size: {qr_img.size[0]}x{qr_img.size[1]} pixels")

    return filename


def generate_printable_qr(url, filename="passingby_qr_printable.png"):
    """
    Generate a printable QR code with instructions for taxi passengers
    """

    # Generate base QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=15,  # Larger for printing
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # Create larger canvas with text
    canvas_width = 800
    canvas_height = 1000
    canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
    draw = ImageDraw.Draw(canvas)

    # Center QR code
    qr_width, qr_height = qr_img.size
    qr_x = (canvas_width - qr_width) // 2
    qr_y = 200
    canvas.paste(qr_img, (qr_x, qr_y))

    # Add text (using default font - you can load custom fonts if needed)
    try:
        # Try to use a nice font
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
    except:
        # Fallback to default
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Title
    title = "PassingBy"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((canvas_width - title_width) // 2, 80), title, fill="black", font=title_font)

    # Subtitle
    subtitle = "Your London Tour Guide"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=text_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text(((canvas_width - subtitle_width) // 2, 150), subtitle, fill="gray", font=text_font)

    # Instructions below QR code
    instructions = [
        "1. Scan this QR code",
        "2. Enter your destination",
        "3. Choose your tour theme",
        "4. Enjoy your journey!"
    ]

    instruction_y = qr_y + qr_height + 60
    for instruction in instructions:
        inst_bbox = draw.textbbox((0, 0), instruction, font=text_font)
        inst_width = inst_bbox[2] - inst_bbox[0]
        draw.text(((canvas_width - inst_width) // 2, instruction_y), instruction, fill="black", font=text_font)
        instruction_y += 50

    # Save
    canvas.save(filename)
    print(f"✓ Printable QR code saved to: {filename}")
    print(f"  Ready to print at A4 size")

    return filename


if __name__ == "__main__":
    print("PassingBy QR Code Generator")
    print("=" * 50)

    # Generate simple QR code
    print("\n1. Generating simple QR code...")
    generate_qr_code(APP_URL, "passingby_qr_simple.png", with_logo=False)

    # Generate QR code with logo
    print("\n2. Generating QR code with logo...")
    generate_qr_code(APP_URL, "passingby_qr_logo.png", with_logo=True)

    # Generate printable version
    print("\n3. Generating printable QR code with instructions...")
    generate_printable_qr(APP_URL, "passingby_qr_printable.png")

    print("\n" + "=" * 50)
    print("✓ All QR codes generated successfully!")
    print("\nNext steps:")
    print("1. Get a custom domain (e.g., passingby.app)")
    print("2. Update APP_URL in this script")
    print("3. Regenerate QR codes")
    print("4. Print and laminate for taxi placement")
