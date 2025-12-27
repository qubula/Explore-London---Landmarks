"""
Test OpenAI TTS voices for exhibition audio.

Generates sample audio files using different voice options so you can
choose which voice sounds best for Alfie the cabbie before generating
all 50-100 exhibition audio files.
"""

import os
from pathlib import Path
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Sample script to test (from Tower Bridge - one of the best landmarks)
SAMPLE_SCRIPT = """The Tower Bridge is that famous drawbridge you'll spot just by the Tower of London on the Thames's east side. It's not just any old bridge—it's got these massive bascules that lift up to let ships through, and it was originally powered by steam and hydraulics before going electric in the '70s. Funny thing is, plenty of people mix it up with London Bridge just down the river, but Tower Bridge's proper fancy look really sets it apart."""

# Available voices
VOICES = {
    "alloy": "Neutral, balanced (default)",
    "echo": "Warm, conversational - good for storytelling",
    "fable": "British-leaning accent - matches London theme",
    "onyx": "Deep, authoritative - masculine cabbie voice",
    "nova": "Young, energetic - modern feel",
    "shimmer": "Soft, calm - gentle narrator"
}

# TTS models
MODELS = {
    "tts-1": "Standard quality, faster, cheaper ($15/1M chars)",
    "tts-1-hd": "High definition, better quality ($30/1M chars)"
}


def generate_voice_samples(output_dir: str = "voice_samples", use_hd: bool = False):
    """
    Generate sample audio files for each voice.

    Args:
        output_dir: Directory to save sample files
        use_hd: Use tts-1-hd (better quality) or tts-1 (faster/cheaper)
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    model = "tts-1-hd" if use_hd else "tts-1"

    print("=" * 70)
    print(f"GENERATING VOICE SAMPLES")
    print(f"Model: {model} ({MODELS[model]})")
    print("=" * 70)
    print()
    print(f"Sample script ({len(SAMPLE_SCRIPT.split())} words):")
    print(f'"{SAMPLE_SCRIPT[:100]}..."')
    print()
    print("=" * 70)
    print()

    for voice, description in VOICES.items():
        print(f"Generating: {voice:10} - {description}")

        try:
            # Generate audio
            response = client.audio.speech.create(
                model=model,
                voice=voice,
                input=SAMPLE_SCRIPT,
                response_format="mp3"
            )

            # Save to file
            filename = f"{voice}_{model.replace('-', '_')}.mp3"
            file_path = output_path / filename
            response.stream_to_file(str(file_path))

            # Get file size
            size_kb = file_path.stat().st_size / 1024

            print(f"  ✓ Saved: {filename} ({size_kb:.1f} KB)")

        except Exception as e:
            print(f"  ✗ Error: {e}")

        print()

    print("=" * 70)
    print("SAMPLES GENERATED")
    print("=" * 70)
    print()
    print(f"Location: {output_path.absolute()}")
    print()
    print("Next steps:")
    print("1. Listen to each voice sample")
    print("2. Choose your favorite voice")
    print("3. Run create_exhibition_audio.py with chosen voice")
    print()
    print("Recommendations:")
    print("  • onyx  - Best for masculine, authoritative cabbie")
    print("  • echo  - Best for warm, friendly storytelling")
    print("  • fable - Best for authentic British London tour")
    print()


def compare_models(voice: str = "onyx", output_dir: str = "voice_samples"):
    """
    Compare standard vs HD quality for a specific voice.

    Args:
        voice: Voice to test (default: onyx)
        output_dir: Directory to save comparison files
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    print("=" * 70)
    print(f"COMPARING MODELS FOR VOICE: {voice}")
    print("=" * 70)
    print()

    for model in ["tts-1", "tts-1-hd"]:
        print(f"Generating: {model} ({MODELS[model]})")

        try:
            response = client.audio.speech.create(
                model=model,
                voice=voice,
                input=SAMPLE_SCRIPT,
                response_format="mp3"
            )

            filename = f"{voice}_{model.replace('-', '_')}_comparison.mp3"
            file_path = output_path / filename
            response.stream_to_file(str(file_path))

            size_kb = file_path.stat().st_size / 1024
            print(f"  ✓ Saved: {filename} ({size_kb:.1f} KB)")

        except Exception as e:
            print(f"  ✗ Error: {e}")

        print()

    print("=" * 70)
    print("Listen to both files and decide if HD quality is worth 2x cost")
    print("For 100 scripts: tts-1 = $0.55, tts-1-hd = $1.10")
    print("=" * 70)
    print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate voice samples for exhibition audio testing"
    )
    parser.add_argument(
        "--hd",
        action="store_true",
        help="Use tts-1-hd (better quality, 2x cost)"
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare standard vs HD for onyx voice"
    )
    parser.add_argument(
        "--voice",
        default="onyx",
        choices=list(VOICES.keys()),
        help="Voice to use for model comparison (default: onyx)"
    )
    parser.add_argument(
        "--output",
        default="voice_samples",
        help="Output directory (default: voice_samples)"
    )

    args = parser.parse_args()

    if args.compare:
        compare_models(voice=args.voice, output_dir=args.output)
    else:
        generate_voice_samples(output_dir=args.output, use_hd=args.hd)
