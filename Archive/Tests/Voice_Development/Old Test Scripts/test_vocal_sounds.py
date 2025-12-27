"""
Test adding vocal sounds and conversational fillers to make speech more natural.

Techniques:
- "Mmm", "Hmm", "Uh" for thinking
- "You know", "I mean", "See" for conversational flow
- "Right?", "Yeah" for engagement
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

GEORGE_ID = "JBFqnCBsd6RMkjVDRZzb"
FINAL_SETTINGS = {
    "stability": 0.24,
    "similarity_boost": 0.79,
    "style": 0.76
}

# Original script
ORIGINAL = """Alright, mate! Let me tell you about Tower Bridge. It's that famous drawbridge you'll spot just by the Tower of London on the Thames's east side. Now, it's not just any old bridge—it's got these massive bascules that lift up to let ships through, and it was originally powered by steam and hydraulics before going electric in the seventies."""

# With vocal sounds and fillers
WITH_VOCAL_SOUNDS = """Alright, mate!

Mmm, let me tell you about Tower Bridge.

It's that famous drawbridge... uh... you'll spot just by the Tower of London, yeah, on the Thames's east side.

Now... hmm... it's not just any old bridge, you know? It's got these massive bascules... that lift up to let ships through.

And, uh, it was originally powered by steam and hydraulics... before going electric in the seventies, right?"""

# Heavy conversational fillers (British cabbie style)
HEAVY_FILLERS = """Alright, mate!

Right, so... let me tell you about Tower Bridge, yeah?

It's that famous drawbridge... you know the one... you'll spot just by the Tower of London, innit... on the Thames's east side.

Now, see... it's not just any old bridge, mate. Nah... it's got these massive bascules, right, that lift up to let ships through.

And, uh... it was originally powered by steam and hydraulics, you see... before going electric in the seventies. Proper interesting, that."""

# Subtle and natural (recommended)
SUBTLE_NATURAL = """Alright, mate!

Let me tell you about Tower Bridge, yeah?

It's that famous drawbridge... you'll spot just by the Tower of London... on the Thames's east side.

Now, see... it's not just any old bridge. It's got these massive bascules that lift up to let ships through.

And it was originally powered by steam and hydraulics... before going electric in the seventies, right?"""


def test_vocal_style(
    script: str,
    name: str,
    description: str,
    output_dir: str = "vocal_sounds_test"
):
    """Test script with vocal sounds."""
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
            "stability": FINAL_SETTINGS["stability"],
            "similarity_boost": FINAL_SETTINGS["similarity_boost"],
            "style": FINAL_SETTINGS["style"],
            "use_speaker_boost": True
        }
    }

    print(f"🎙️  {name}")
    print(f"   {description}")

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
    """Generate samples with different vocal sound levels."""

    print("=" * 70)
    print("VOCAL SOUNDS & CONVERSATIONAL FILLERS TEST")
    print("Adding 'mmm', 'uh', 'yeah', 'you know', etc.")
    print("=" * 70)
    print()

    if not ELEVENLABS_API_KEY:
        print("❌ ERROR: ELEVENLABS_API_KEY not set")
        return

    test_configs = [
        (ORIGINAL, "original_no_sounds", "Baseline - no vocal sounds"),
        (WITH_VOCAL_SOUNDS, "with_vocal_sounds", "With vocal sounds - mmm, uh, hmm"),
        (HEAVY_FILLERS, "heavy_fillers", "Heavy fillers - very conversational"),
        (SUBTLE_NATURAL, "subtle_natural", "✨ Subtle & natural - RECOMMENDED"),
    ]

    print("Testing different levels of vocal sounds:")
    print()

    successful = 0
    for script, name, desc in test_configs:
        result = test_vocal_style(script, name, desc)
        if result:
            successful += 1
        print()

    print("=" * 70)
    print(f"RESULTS: {successful}/{len(test_configs)} successful")
    print("=" * 70)
    print()
    print("Location: vocal_sounds_test/")
    print()
    print("VOCAL SOUNDS TESTED:")
    print()
    print("Thinking sounds:")
    print("  • 'Mmm' - contemplating")
    print("  • 'Hmm' - considering")
    print("  • 'Uh' - pausing to think")
    print()
    print("Conversational fillers:")
    print("  • 'You know' - engaging listener")
    print("  • 'See' - explanatory")
    print("  • 'Right?' - seeking agreement")
    print("  • 'Yeah' - affirming")
    print("  • 'Innit' - British colloquial")
    print()
    print("COMPARE:")
    print("  • original_no_sounds.mp3   - Clean, no fillers")
    print("  • with_vocal_sounds.mp3    - With mmm, uh, hmm")
    print("  • heavy_fillers.mp3        - Very conversational (might be too much)")
    print("  • subtle_natural.mp3       - ✨ Balanced and natural")
    print()
    print("WARNING: Too many vocal sounds can sound forced.")
    print("Recommendation: Use subtly for natural effect.")
    print()


if __name__ == "__main__":
    main()
