"""
Test ElevenLabs TTS voices for authentic Alfie character.

ElevenLabs provides much more natural and character-rich voices,
especially for British/London accents.
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ElevenLabs API configuration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# Sample script - ULTRA SHORT (only 10 credits remaining!)
SAMPLE_SCRIPT = """Hello!"""

# Pre-made ElevenLabs voices with British/London character
ELEVENLABS_VOICES = {
    "Adam": {
        "voice_id": "pNInz6obpgDQGcFmaJgB",
        "description": "Deep, middle-aged British male - authoritative narrator",
        "accent": "British",
        "age": "Middle-aged",
        "best_for": "Authoritative London cabbie"
    },
    "Antoni": {
        "voice_id": "ErXwobaYiN019PkySvjV",
        "description": "Well-rounded British male - versatile",
        "accent": "British",
        "age": "Young-middle",
        "best_for": "Friendly cabbie storyteller"
    },
    "Bill": {
        "voice_id": "pqHfZKP75CvOlQylNhV4",
        "description": "Old, gruff male - weathered character",
        "accent": "American (but good for gravelly tone)",
        "age": "Old",
        "best_for": "Veteran cabbie with character"
    },
    "Charlie": {
        "voice_id": "IKne3meq5aSn9XLyUdCD",
        "description": "Casual Australian - can sound British",
        "accent": "Australian/British",
        "age": "Middle-aged",
        "best_for": "Conversational cabbie"
    },
    "George": {
        "voice_id": "JBFqnCBsd6RMkjVDRZzb",
        "description": "Warm British narrator - perfect for stories",
        "accent": "British",
        "age": "Middle-aged",
        "best_for": "Warm London guide"
    },
}


def test_elevenlabs_voice(
    voice_id: str,
    voice_name: str,
    text: str,
    output_path: Path,
    model: str = "eleven_turbo_v2_5",
    stability: float = 0.5,
    similarity_boost: float = 0.75
) -> bool:
    """
    Generate audio using ElevenLabs API.

    Args:
        voice_id: ElevenLabs voice ID
        voice_name: Name for output file
        text: Script text
        output_path: Where to save MP3
        model: Model version (eleven_turbo_v2_5 for free tier, or eleven_multilingual_v2)
        stability: 0-1 (higher = more stable, lower = more variable/emotional)
        similarity_boost: 0-1 (higher = closer to original voice)

    Returns:
        True if successful
    """
    if not ELEVENLABS_API_KEY:
        print("❌ ELEVENLABS_API_KEY not found in environment")
        print("   Set it in .env file: ELEVENLABS_API_KEY=your_key_here")
        return False

    url = f"{ELEVENLABS_API_URL}/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    data = {
        "text": text,
        "model_id": model,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            output_path.write_bytes(response.content)
            size_kb = len(response.content) / 1024
            return True
        else:
            print(f"   ❌ API Error: {response.status_code}")
            print(f"   {response.text}")
            return False

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def generate_elevenlabs_samples(
    output_dir: str = "voice_samples_elevenlabs"
):
    """
    Generate samples for all recommended ElevenLabs voices.
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    print("=" * 70)
    print("GENERATING ELEVENLABS VOICE SAMPLES")
    print("Authentic British/London character voices")
    print("=" * 70)
    print()

    if not ELEVENLABS_API_KEY:
        print("❌ ERROR: ELEVENLABS_API_KEY not set")
        print()
        print("To use ElevenLabs:")
        print("1. Sign up at https://elevenlabs.io")
        print("2. Get your API key from https://elevenlabs.io/app/settings/api-keys")
        print("3. Add to .env file:")
        print("   ELEVENLABS_API_KEY=your_key_here")
        print()
        return

    print(f"Sample script ({len(SAMPLE_SCRIPT.split())} words):")
    print(f'"{SAMPLE_SCRIPT[:100]}..."')
    print()
    print("=" * 70)
    print()

    successful = 0
    failed = 0

    # ONLY TEST ADAM (you have 10 credits left, save them!)
    test_voices = ["Adam"]  # Change to list(ELEVENLABS_VOICES.keys()) to test all

    for voice_name in test_voices:
        if voice_name not in ELEVENLABS_VOICES:
            continue
        voice_info = ELEVENLABS_VOICES[voice_name]
        print(f"🎙️  {voice_name}")
        print(f"   {voice_info['description']}")
        print(f"   Accent: {voice_info['accent']} | Age: {voice_info['age']}")
        print(f"   Best for: {voice_info['best_for']}")

        filename = f"{voice_name.lower()}_elevenlabs.mp3"
        file_path = output_path / filename

        success = test_elevenlabs_voice(
            voice_id=voice_info["voice_id"],
            voice_name=voice_name,
            text=SAMPLE_SCRIPT,
            output_path=file_path
        )

        if success:
            size_kb = file_path.stat().st_size / 1024
            print(f"   ✅ Saved: {filename} ({size_kb:.1f} KB)")
            successful += 1
        else:
            failed += 1

        print()

    print("=" * 70)
    print(f"RESULTS: {successful} successful, {failed} failed")
    print("=" * 70)
    print()

    if successful > 0:
        print(f"Location: {output_path.absolute()}")
        print()
        print("Top recommendations for Alfie:")
        print("  1. Adam  - Best for authoritative middle-aged cabbie")
        print("  2. George - Best for warm, friendly storyteller")
        print("  3. Bill  - Best for gruff, veteran character")
        print()
        print("Listen and choose your favorite!")
        print()
        print("Pricing:")
        print("  • Starter: $5/month (30K characters = ~50-80 scripts)")
        print("  • Creator: $11/month (100K characters = 150+ scripts)")
        print()


def test_voice_settings(
    voice_name: str = "Adam",
    output_dir: str = "voice_samples_elevenlabs"
):
    """
    Test different stability/similarity settings for fine-tuning character.
    """
    voice_info = ELEVENLABS_VOICES.get(voice_name)
    if not voice_info:
        print(f"❌ Voice '{voice_name}' not found")
        return

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    print("=" * 70)
    print(f"TESTING VOICE SETTINGS: {voice_name}")
    print("=" * 70)
    print()

    # Test different settings
    settings = [
        (0.3, 0.75, "more_variable"),  # More emotional variation
        (0.5, 0.75, "balanced"),       # Default balanced
        (0.7, 0.75, "more_stable"),    # More consistent delivery
    ]

    for stability, similarity, label in settings:
        print(f"Settings: stability={stability}, similarity={similarity} ({label})")

        filename = f"{voice_name.lower()}_{label}_elevenlabs.mp3"
        file_path = output_path / filename

        success = test_elevenlabs_voice(
            voice_id=voice_info["voice_id"],
            voice_name=f"{voice_name}_{label}",
            text=SAMPLE_SCRIPT,
            output_path=file_path,
            stability=stability,
            similarity_boost=similarity
        )

        if success:
            size_kb = file_path.stat().st_size / 1024
            print(f"  ✅ Saved: {filename} ({size_kb:.1f} KB)")

        print()

    print("=" * 70)
    print("Compare the three versions:")
    print("  • more_variable - More emotional, storytelling feel")
    print("  • balanced      - Good middle ground")
    print("  • more_stable   - Consistent, professional delivery")
    print("=" * 70)
    print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Test ElevenLabs voices for Alfie character"
    )
    parser.add_argument(
        "--test-settings",
        action="store_true",
        help="Test different voice settings for Adam"
    )
    parser.add_argument(
        "--voice",
        default="Adam",
        choices=list(ELEVENLABS_VOICES.keys()),
        help="Voice to test settings for (default: Adam)"
    )
    parser.add_argument(
        "--output",
        default="voice_samples_elevenlabs",
        help="Output directory"
    )

    args = parser.parse_args()

    if args.test_settings:
        test_voice_settings(voice_name=args.voice, output_dir=args.output)
    else:
        generate_elevenlabs_samples(output_dir=args.output)
