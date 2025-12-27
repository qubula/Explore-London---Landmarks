"""
Ultra-natural storytelling with maximum variation in timing, tone, and speed.

Combines low stability (natural variation) with high style (expressiveness)
and enhanced pauses for truly conversational cabbie storytelling.
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

GEORGE_ID = "JBFqnCBsd6RMkjVDRZzb"

# Enhanced script with strategic pauses for maximum naturality
ULTRA_NATURAL_SCRIPT = """Alright, mate!

Let me tell you about Tower Bridge.

It's that famous drawbridge you'll spot... just by the Tower of London, on the Thames's east side.

Now... it's not just any old bridge—it's got these massive bascules... that lift up to let ships through.

And it was originally powered by steam and hydraulics... before going electric in the seventies.

Funny thing is... plenty of people mix it up with London Bridge... just down the river.

But Tower Bridge's proper fancy look?

Really sets it apart."""


def test_ultra_natural(
    script: str,
    stability: float,
    similarity: float,
    style: float,
    name: str,
    description: str,
    output_dir: str = "ultra_natural"
):
    """Test ultra-natural storytelling voice."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    url = f"{ELEVENLABS_API_URL}/{GEORGE_ID}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    data = {
        "text": script,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity,
            "style": style,
            "use_speaker_boost": True
        }
    }

    print(f"🎙️  {name}")
    print(f"   {description}")
    print(f"   stability={stability}, similarity={similarity}, style={style}")

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
    """Generate ultra-natural variations."""

    print("=" * 70)
    print("ULTRA-NATURAL STORYTELLING")
    print("Maximum variation in timing, tone, and speed")
    print("=" * 70)
    print()

    if not ELEVENLABS_API_KEY:
        print("❌ ERROR: ELEVENLABS_API_KEY not set")
        return

    # Test variations that mix expressiveness with natural variation
    test_configs = [
        # (stability, similarity, style, name, description)

        # Reference points
        (
            0.25, 0.80, 0.65,
            "reference_low_stability",
            "Reference - more_natural_low_stability from before"
        ),
        (
            0.30, 0.80, 0.75,
            "reference_expressive",
            "Reference - expressive_storyteller from before"
        ),

        # NEW MIXES - combining best of both worlds
        (
            0.25, 0.80, 0.75,
            "ultra_natural_v1",
            "Ultra Natural v1 - Low stability + High expressiveness"
        ),
        (
            0.22, 0.80, 0.72,
            "ultra_natural_v2",
            "Ultra Natural v2 - Very low stability + High expression"
        ),
        (
            0.27, 0.78, 0.78,
            "ultra_natural_v3",
            "Ultra Natural v3 - Balanced low + Very expressive"
        ),

        # EXTREME VARIATIONS (for comparison)
        (
            0.20, 0.80, 0.75,
            "maximum_variation",
            "Maximum Variation - Extremely low stability"
        ),
        (
            0.25, 0.80, 0.82,
            "maximum_expression",
            "Maximum Expression - Very theatrical"
        ),

        # RECOMMENDED SWEET SPOT
        (
            0.24, 0.79, 0.76,
            "recommended_ultra_natural",
            "✨ RECOMMENDED - Perfect mix of variation + expression"
        ),
    ]

    print("Testing ultra-natural mixes with enhanced pauses:")
    print()

    successful = 0
    for stability, similarity, style, name, desc in test_configs:
        result = test_ultra_natural(
            ULTRA_NATURAL_SCRIPT,
            stability,
            similarity,
            style,
            name,
            desc
        )
        if result:
            successful += 1
        print()

    print("=" * 70)
    print(f"RESULTS: {successful}/{len(test_configs)} successful")
    print("=" * 70)
    print()
    print("Location: ultra_natural/")
    print()
    print("WHAT EACH PARAMETER DOES:")
    print()
    print("Stability (0.20-0.30):")
    print("  • LOWER = More variation in pace, tone, timing")
    print("  • Natural pauses and hesitations")
    print("  • Sounds spontaneous, not scripted")
    print()
    print("Style (0.70-0.82):")
    print("  • HIGHER = More emotional expression")
    print("  • Dramatic emphasis on key words")
    print("  • Conversational storytelling cadence")
    print()
    print("Similarity (0.78-0.80):")
    print("  • Keeps authentic British accent")
    print("  • Maintains George's character")
    print()
    print("LISTEN FOR:")
    print("  • Varied pacing (not constant speed)")
    print("  • Natural pauses (thinking, breathing)")
    print("  • Tonal variation (emphasis, excitement)")
    print("  • Conversational feel (not reading)")
    print()
    print("COMPARE:")
    print("  • reference_low_stability.mp3      - Your previous choice")
    print("  • reference_expressive.mp3         - More expressive version")
    print("  • recommended_ultra_natural.mp3    - ✨ BEST MIX")
    print("  • maximum_variation.mp3            - Too wild?")
    print()
    print("Pick your favorite for exhibition audio!")
    print()


if __name__ == "__main__":
    main()
