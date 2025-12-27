"""
Fine-tune George voice for perfect Alfie character.

Test George with a wider range of stability and similarity settings
to dial in exactly the character you want.
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# George voice ID
GEORGE_ID = "JBFqnCBsd6RMkjVDRZzb"

# Test script
TEST_SCRIPT = """Alright, mate! Let me tell you about Tower Bridge. It's that famous drawbridge you'll spot just by the Tower of London on the Thames's east side. Now, it's not just any old bridge—it's got these massive bascules that lift up to let ships through, and it was originally powered by steam and hydraulics before going electric in the seventies. Funny thing is, plenty of people mix it up with London Bridge just down the river, but Tower Bridge's proper fancy look really sets it apart."""


def test_george_settings(
    stability: float,
    similarity_boost: float,
    style: float,
    description: str,
    output_dir: str = "george_finetune"
):
    """Test George with specific settings."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    url = f"{ELEVENLABS_API_URL}/{GEORGE_ID}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    data = {
        "text": TEST_SCRIPT,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
            "style": style,
            "use_speaker_boost": True
        }
    }

    name = f"george_s{int(stability*10)}_sim{int(similarity_boost*10)}_st{int(style*10)}"

    print(f"🎙️  {description}")
    print(f"   stability={stability}, similarity={similarity_boost}, style={style}")

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            filename = f"{name}.mp3"
            file_path = output_path / filename

            with open(file_path, 'wb') as f:
                f.write(response.content)

            size_kb = file_path.stat().st_size / 1024
            print(f"   ✅ Saved: {filename} ({size_kb:.1f} KB)")
            return True
        else:
            error_data = response.json()
            print(f"   ❌ API Error: {response.status_code}")
            print(f"   {error_data}")
            return False

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

    print()


def main():
    """Generate George samples with fine-tuned settings."""

    print("=" * 70)
    print("GEORGE VOICE FINE-TUNING")
    print("Finding the perfect Alfie character")
    print("=" * 70)
    print()

    if not ELEVENLABS_API_KEY:
        print("❌ ERROR: ELEVENLABS_API_KEY not set")
        return

    print(f"Test script ({len(TEST_SCRIPT.split())} words):")
    print(f'"{TEST_SCRIPT[:80]}..."')
    print()
    print("=" * 70)
    print()

    # Fine-tuning matrix for George
    # Stability: Lower = more expressive/variable, Higher = more consistent
    # Similarity: Lower = more creative, Higher = stays true to voice
    # Style: Controls expressiveness and emotion

    test_configs = [
        # (stability, similarity, style, description)

        # BASELINE (what you already have)
        (0.5, 0.75, 0.5, "Baseline - balanced"),

        # MORE CHARACTER (lower stability = more variation/expression)
        (0.35, 0.80, 0.6, "More character - expressive with strong British"),
        (0.30, 0.75, 0.7, "Very expressive - dramatic cabbie"),
        (0.25, 0.80, 0.5, "Maximum variation - wild character"),

        # DIFFERENT STYLES (adjusting style parameter)
        (0.40, 0.80, 0.3, "Calm cabbie - less dramatic"),
        (0.40, 0.80, 0.8, "Theatrical cabbie - very expressive"),

        # DIFFERENT SIMILARITY (how much it sounds like George)
        (0.35, 0.70, 0.6, "More creative - less George-like"),
        (0.35, 0.85, 0.6, "Very George - stays true to voice"),

        # RECOMMENDED FOR ALFIE
        (0.38, 0.78, 0.65, "RECOMMENDED: Intense cabbie with character"),
    ]

    print("Testing George with different character intensities:")
    print(f"(Each test uses ~{len(TEST_SCRIPT)} characters)")
    print()

    successful = 0
    for stability, similarity, style, desc in test_configs:
        result = test_george_settings(stability, similarity, style, desc)
        if result:
            successful += 1
        print()

    print("=" * 70)
    print(f"RESULTS: {successful}/{len(test_configs)} successful")
    print("=" * 70)
    print()
    print("Location: george_finetune/")
    print()
    print("PARAMETER GUIDE:")
    print()
    print("Stability (0.0 - 1.0):")
    print("  • Lower (0.2-0.3) = More expressive, variable, emotional")
    print("  • Medium (0.4-0.5) = Balanced character and consistency")
    print("  • Higher (0.6-0.8) = More stable, predictable delivery")
    print()
    print("Similarity Boost (0.0 - 1.0):")
    print("  • Lower (0.6-0.7) = More creative, can deviate from George")
    print("  • Medium (0.75-0.8) = Balanced authenticity")
    print("  • Higher (0.85-0.9) = Very true to George's voice")
    print()
    print("Style (0.0 - 1.0):")
    print("  • Lower (0.3-0.4) = Calmer, less dramatic")
    print("  • Medium (0.5-0.6) = Balanced expressiveness")
    print("  • Higher (0.7-0.8) = More theatrical, expressive")
    print()
    print("Listen to all samples and pick your favorite!")
    print("Then tell me the exact settings to use for exhibition audio.")
    print()


if __name__ == "__main__":
    main()
