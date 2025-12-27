"""
Test ElevenLabs with custom voice settings to dial in Alfie's character.

Experiment with stability and similarity_boost to get the perfect
"intense middle-aged London cabbie" character.
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# Test script with character (shorter to save credits)
TEST_SCRIPT = """Alright, mate! Let me tell you about Tower Bridge. It's that famous drawbridge you'll spot just by the Tower of London on the Thames. Now, it's not just any old bridge - it's got these massive bascules that lift up to let ships through, see."""


def test_voice_with_settings(
    voice_id: str,
    voice_name: str,
    stability: float,
    similarity_boost: float,
    description: str,
    output_dir: str = "voice_samples_custom"
):
    """
    Test a voice with specific settings.

    Args:
        voice_id: ElevenLabs voice ID
        voice_name: Name for display and filename
        stability: 0-1 (lower = more expressive/variable)
        similarity_boost: 0-1 (higher = stays closer to voice)
        description: What these settings should achieve
        output_dir: Where to save samples
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    url = f"{ELEVENLABS_API_URL}/{voice_id}"

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
            "style": 0.5,  # Medium style
            "use_speaker_boost": True
        }
    }

    print(f"🎙️  {voice_name}")
    print(f"   Settings: stability={stability}, similarity={similarity_boost}")
    print(f"   Goal: {description}")

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            filename = f"{voice_name.lower().replace(' ', '_')}.mp3"
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
    """Generate samples with different character settings."""

    print("=" * 70)
    print("ELEVENLABS CUSTOM VOICE SETTINGS TEST")
    print("Dialing in the perfect Alfie character")
    print("=" * 70)
    print()

    if not ELEVENLABS_API_KEY:
        print("❌ ERROR: ELEVENLABS_API_KEY not set in .env")
        return

    print(f"Test script ({len(TEST_SCRIPT.split())} words):")
    print(f'"{TEST_SCRIPT[:80]}..."')
    print()
    print("=" * 70)
    print()

    # Voice IDs
    adam_id = "pNInz6obpgDQGcFmaJgB"
    george_id = "JBFqnCBsd6RMkjVDRZzb"

    # Test different voices and character settings
    test_configs = [
        # (voice_id, stability, similarity_boost, name, description)
        (adam_id, 0.4, 0.80, "adam_intense", "Adam - Intense cabbie character"),
        (adam_id, 0.3, 0.75, "adam_expressive", "Adam - More expressive/emotional"),
        (george_id, 0.4, 0.80, "george_intense", "George - Warm cabbie storyteller"),
        (george_id, 0.5, 0.75, "george_balanced", "George - Balanced, natural"),
        (george_id, 0.3, 0.85, "george_character", "George - Strong character"),
    ]

    print("Testing Adam and George voices with character settings:")
    print("(Each test uses ~160 characters = ~160 credits)")
    print()

    successful = 0
    for voice_id, stability, similarity, name, desc in test_configs:
        result = test_voice_with_settings(
            voice_id,
            name,
            stability,
            similarity,
            desc
        )
        if result:
            successful += 1
        print()

    print("=" * 70)
    print(f"RESULTS: {successful}/{len(test_configs)} successful")
    print("=" * 70)
    print()
    print("Location: voice_samples_custom/")
    print()
    print("Listen to each sample and compare:")
    print()
    print("Adam (Deep, authoritative):")
    print("  • adam_intense      - Intense cabbie character")
    print("  • adam_expressive   - More emotional delivery")
    print()
    print("George (Warm, storyteller):")
    print("  • george_intense    - Warm cabbie storyteller")
    print("  • george_balanced   - Balanced, natural")
    print("  • george_character  - Strong character")
    print()
    print("Once you find your favorite, we'll use those settings")
    print("for all 50-100 exhibition audio files!")
    print()


if __name__ == "__main__":
    main()
