"""
Test custom Alfie voice with different settings.

This tests your custom-created Alfie voice to ensure it works
and sounds good with the ultra-natural settings.
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# Custom Alfie voice ID
ALFIE_ID = "LPRLepQnqpzvBlsHyfyS"

# Test script with natural pauses and subtle vocal sounds
TEST_SCRIPT = """Alright, mate!

Let me tell you about Tower Bridge, yeah?

It's that famous drawbridge you'll spot... just by the Tower of London... on the Thames's east side.

Now, see... it's not just any old bridge. It's got these massive bascules that lift up to let ships through.

And it was originally powered by steam and hydraulics... before going electric in the seventies, right?"""


def test_alfie_voice(
    stability: float,
    similarity: float,
    style: float,
    name: str,
    description: str,
    output_dir: str = "alfie_custom_test"
):
    """Test custom Alfie voice with specific settings."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    url = f"{ELEVENLABS_API_URL}/{ALFIE_ID}"

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
    """Test custom Alfie voice."""

    print("=" * 70)
    print("TESTING CUSTOM ALFIE VOICE")
    print("Your custom-created voice from ElevenLabs")
    print("=" * 70)
    print()

    if not ELEVENLABS_API_KEY:
        print("❌ ERROR: ELEVENLABS_API_KEY not set")
        return

    # Test your custom Alfie voice with the ultra-natural settings
    test_configs = [
        # (stability, similarity, style, name, description)

        # Your chosen ultra-natural settings from George tests
        (
            0.24, 0.79, 0.76,
            "alfie_ultra_natural",
            "✨ Alfie with ultra-natural settings (from George tests)"
        ),

        # Alternative variations to see how YOUR voice responds
        (
            0.30, 0.80, 0.70,
            "alfie_balanced",
            "Alfie - Slightly more stable, balanced"
        ),

        (
            0.20, 0.75, 0.80,
            "alfie_very_expressive",
            "Alfie - Maximum variation + expression"
        ),

        # Test with default/neutral settings
        (
            0.50, 0.75, 0.50,
            "alfie_neutral",
            "Alfie - Neutral baseline settings"
        ),
    ]

    print("Testing your custom Alfie voice with different settings:")
    print()

    successful = 0
    for stability, similarity, style, name, desc in test_configs:
        result = test_alfie_voice(
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
    print("Location: alfie_custom_test/")
    print()
    print("LISTEN TO YOUR CUSTOM ALFIE VOICE:")
    print()
    print("  • alfie_ultra_natural.mp3    - ✨ With settings from George tests")
    print("  • alfie_balanced.mp3         - Slightly more stable")
    print("  • alfie_very_expressive.mp3  - Maximum variation")
    print("  • alfie_neutral.mp3          - Baseline comparison")
    print()
    print("Since this is YOUR custom voice, it may respond differently")
    print("to settings than the pre-made George voice. Listen and pick")
    print("your favorite settings for the exhibition audio!")
    print()


if __name__ == "__main__":
    main()
