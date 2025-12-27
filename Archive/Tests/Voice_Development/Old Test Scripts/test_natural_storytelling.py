"""
Test natural storytelling with pauses, emphasis, and varied pacing.

Uses strategic pauses and emphasis to make George sound like he's telling
a story naturally, not reading from a script.
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

GEORGE_ID = "JBFqnCBsd6RMkjVDRZzb"

# Original script (flat, reads like text)
ORIGINAL_SCRIPT = """Alright, mate! Let me tell you about Tower Bridge. It's that famous drawbridge you'll spot just by the Tower of London on the Thames's east side. Now, it's not just any old bridge—it's got these massive bascules that lift up to let ships through, and it was originally powered by steam and hydraulics before going electric in the seventies. Funny thing is, plenty of people mix it up with London Bridge just down the river, but Tower Bridge's proper fancy look really sets it apart."""

# Enhanced with natural pauses and storytelling flow
ENHANCED_SCRIPT = """Alright, mate! Let me tell you about Tower Bridge.

It's that famous drawbridge you'll spot... just by the Tower of London, on the Thames's east side.

Now, it's not just any old bridge—it's got these massive bascules that lift up to let ships through. And it was originally powered by steam and hydraulics... before going electric in the seventies.

Funny thing is... plenty of people mix it up with London Bridge, just down the river. But Tower Bridge's proper fancy look? Really sets it apart."""


def test_storytelling_voice(
    script: str,
    settings: dict,
    name: str,
    description: str,
    output_dir: str = "natural_storytelling"
):
    """Test voice with specific storytelling settings."""
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
            "stability": settings.get("stability", 0.35),
            "similarity_boost": settings.get("similarity_boost", 0.80),
            "style": settings.get("style", 0.60),
            "use_speaker_boost": True
        }
    }

    print(f"🎙️  {name}")
    print(f"   {description}")
    print(f"   Settings: stability={settings['stability']}, style={settings['style']}")

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
    """Generate natural storytelling samples."""

    print("=" * 70)
    print("NATURAL STORYTELLING TEST")
    print("Making George sound like he's telling a story, not reading")
    print("=" * 70)
    print()

    if not ELEVENLABS_API_KEY:
        print("❌ ERROR: ELEVENLABS_API_KEY not set")
        return

    # Test different approaches
    test_configs = [
        # (script, settings, name, description)

        # 1. Baseline (your current settings)
        (
            ORIGINAL_SCRIPT,
            {"stability": 0.35, "similarity_boost": 0.80, "style": 0.60},
            "baseline_original",
            "Baseline - original script, current settings"
        ),

        # 2. Same settings but with natural pauses in script
        (
            ENHANCED_SCRIPT,
            {"stability": 0.35, "similarity_boost": 0.80, "style": 0.60},
            "enhanced_pauses",
            "Enhanced - added pauses for natural storytelling"
        ),

        # 3. Lower stability = more variation (sounds less robotic)
        (
            ENHANCED_SCRIPT,
            {"stability": 0.25, "similarity_boost": 0.80, "style": 0.65},
            "more_natural_low_stability",
            "More natural - lower stability for variation"
        ),

        # 4. Higher style = more expressive/emotional
        (
            ENHANCED_SCRIPT,
            {"stability": 0.30, "similarity_boost": 0.80, "style": 0.75},
            "expressive_storyteller",
            "Expressive - higher style for storytelling emotion"
        ),

        # 5. Balanced naturality
        (
            ENHANCED_SCRIPT,
            {"stability": 0.32, "similarity_boost": 0.78, "style": 0.70},
            "balanced_natural",
            "Balanced - natural pauses + moderate variation"
        ),

        # 6. RECOMMENDED: Natural storytelling settings
        (
            ENHANCED_SCRIPT,
            {"stability": 0.28, "similarity_boost": 0.80, "style": 0.72},
            "recommended_storyteller",
            "RECOMMENDED - Natural cabbie storyteller"
        ),
    ]

    print("Testing different approaches to natural storytelling:")
    print()

    successful = 0
    for script, settings, name, desc in test_configs:
        result = test_storytelling_voice(script, settings, name, desc)
        if result:
            successful += 1
        print()

    print("=" * 70)
    print(f"RESULTS: {successful}/{len(test_configs)} successful")
    print("=" * 70)
    print()
    print("Location: natural_storytelling/")
    print()
    print("KEY IMPROVEMENTS:")
    print()
    print("1. PAUSES IN SCRIPT:")
    print("   • Line breaks = natural pauses")
    print("   • Ellipses (...) = thinking/dramatic pauses")
    print("   • Commas = short breathing pauses")
    print()
    print("2. LOWER STABILITY (0.25-0.32):")
    print("   • More variation in tone and pace")
    print("   • Less robotic, more human-like")
    print("   • Sounds less like reading")
    print()
    print("3. HIGHER STYLE (0.65-0.75):")
    print("   • More emotional expression")
    print("   • Better storytelling cadence")
    print("   • Natural emphasis on key words")
    print()
    print("COMPARE:")
    print("  • baseline_original.mp3    - Your current (sounds read)")
    print("  • enhanced_pauses.mp3      - Same settings + natural pauses")
    print("  • recommended_storyteller.mp3 - BEST: Natural cabbie story")
    print()
    print("Once you pick your favorite, I'll update all scripts with")
    print("natural pauses and use those settings for exhibition audio!")
    print()


if __name__ == "__main__":
    main()
