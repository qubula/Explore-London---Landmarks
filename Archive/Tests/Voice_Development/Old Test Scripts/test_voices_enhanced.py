"""
Enhanced OpenAI TTS voice testing with prompt engineering.

Uses text preprocessing and strategic formatting to coax more character
and accent from OpenAI's TTS voices without needing external services.
"""

import os
from pathlib import Path
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Sample script from Tower Bridge
BASE_SCRIPT = """The Tower Bridge is that famous drawbridge you'll spot just by the Tower of London on the Thames's east side. It's not just any old bridge—it's got these massive bascules that lift up to let ships through, and it was originally powered by steam and hydraulics before going electric in the '70s. Funny thing is, plenty of people mix it up with London Bridge just down the river, but Tower Bridge's proper fancy look really sets it apart."""


def add_character_hints(script: str, character: str = "london_cabbie") -> str:
    """
    Add subtle character hints to the script using punctuation,
    emphasis markers, and British spelling to influence TTS delivery.

    Args:
        script: Original script text
        character: Character type (london_cabbie, storyteller, etc.)

    Returns:
        Modified script with character hints
    """
    if character == "london_cabbie":
        # Add conversational markers and British colloquialisms
        # Use strategic pauses (commas, dashes) for natural cabbie speech
        modified = script.replace(
            "you'll spot",
            "you'll spot, right"
        ).replace(
            "It's not just any old bridge",
            "Now, it's not just any old bridge, mate"
        ).replace(
            "originally powered",
            "originally powered, see"
        ).replace(
            "Funny thing is",
            "Funny thing is, innit"
        ).replace(
            "proper fancy",
            "proper fancy, like"
        )

        # Add emphasis with CAPS for key words (sparingly)
        modified = modified.replace("massive bascules", "MASSIVE bascules")

        return modified

    return script


def add_phonetic_hints(script: str) -> str:
    """
    Use phonetic respelling for British pronunciation.

    Examples:
    - "Thames" → "Tems" (British pronunciation)
    - "schedule" → "shed-yule" (British vs American "sked-yule")
    """
    hints = {
        "Thames": "Tems",  # British pronunciation
        # Add more as needed
    }

    modified = script
    for word, phonetic in hints.items():
        modified = modified.replace(word, phonetic)

    return modified


def add_prosody_markers(script: str) -> str:
    """
    Add strategic punctuation to control pacing and emphasis.

    - Extra commas = natural pauses (cabbie thinking)
    - Em dashes = conversational asides
    - Ellipses = dramatic pauses
    """
    # Split into sentences
    sentences = script.split('. ')

    modified_sentences = []
    for sentence in sentences:
        # Add natural pauses with commas
        if len(sentence) > 60:  # Long sentences need breathing room
            # Add comma after transition words
            sentence = sentence.replace(" and ", ", and ")
            sentence = sentence.replace(" but ", ", but ")
            sentence = sentence.replace(" so ", ", so ")

        modified_sentences.append(sentence)

    return '. '.join(modified_sentences)


# Voice-specific character strategies
VOICE_STRATEGIES = {
    "onyx": {
        "name": "Onyx (Deep, Authoritative)",
        "description": "Best for masculine cabbie - add directness",
        "modifications": [
            "Add 'mate', 'right', 'see' for working-class authenticity",
            "Use shorter sentences for confident delivery",
            "Add emphasis on key landmarks"
        ]
    },
    "fable": {
        "name": "Fable (British-leaning)",
        "description": "Natural British accent - add colloquialisms",
        "modifications": [
            "Add 'innit', 'proper', 'brilliant' for London flavor",
            "Use 'you'll find' instead of 'you will find'",
            "British spellings (colour, favourite)"
        ]
    },
    "echo": {
        "name": "Echo (Warm, Conversational)",
        "description": "Friendly storyteller - add personal touches",
        "modifications": [
            "Add 'you know what', 'I'll tell you'",
            "More conversational asides",
            "Warmer, friendlier tone cues"
        ]
    }
}


def enhance_script_for_voice(
    script: str,
    voice: str,
    intensity: str = "medium"
) -> str:
    """
    Apply character enhancements based on voice and desired intensity.

    Args:
        script: Original script
        voice: OpenAI voice name
        intensity: low, medium, high (how much character to add)

    Returns:
        Enhanced script
    """
    enhanced = script

    if intensity in ["medium", "high"]:
        enhanced = add_character_hints(enhanced, "london_cabbie")

    if intensity == "high":
        enhanced = add_prosody_markers(enhanced)
        enhanced = add_phonetic_hints(enhanced)

    return enhanced


def generate_enhanced_samples(
    output_dir: str = "voice_samples_enhanced",
    use_hd: bool = True
):
    """
    Generate voice samples with character enhancements.
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    model = "tts-1-hd" if use_hd else "tts-1"

    print("=" * 70)
    print("GENERATING ENHANCED VOICE SAMPLES")
    print(f"Model: {model}")
    print("Strategy: Character-enhanced prompts for London cabbie persona")
    print("=" * 70)
    print()

    # Test best candidates with different enhancement levels
    test_configs = [
        ("onyx", "low", "Baseline - minimal changes"),
        ("onyx", "medium", "Moderate character hints"),
        ("onyx", "high", "Full character enhancement"),
        ("fable", "medium", "British accent + character"),
        ("echo", "medium", "Warm storyteller"),
    ]

    for voice, intensity, description in test_configs:
        print(f"Voice: {voice:8} | Intensity: {intensity:6} | {description}")

        # Enhance the script
        enhanced_script = enhance_script_for_voice(
            BASE_SCRIPT,
            voice,
            intensity
        )

        # Show what was changed (first 100 chars)
        if intensity != "low":
            print(f"  Modified: \"{enhanced_script[:100]}...\"")

        try:
            # Generate audio
            response = client.audio.speech.create(
                model=model,
                voice=voice,
                input=enhanced_script,
                response_format="mp3"
            )

            # Save to file
            filename = f"{voice}_{intensity}_{model.replace('-', '_')}.mp3"
            file_path = output_path / filename

            with open(file_path, 'wb') as f:
                f.write(response.content)

            size_kb = file_path.stat().st_size / 1024
            print(f"  ✓ Saved: {filename} ({size_kb:.1f} KB)")

        except Exception as e:
            print(f"  ✗ Error: {e}")

        print()

    print("=" * 70)
    print("ENHANCED SAMPLES GENERATED")
    print("=" * 70)
    print()
    print(f"Location: {output_path.absolute()}")
    print()
    print("Listen and compare:")
    print("  • onyx_low      - Baseline (no enhancements)")
    print("  • onyx_medium   - Moderate London cabbie character")
    print("  • onyx_high     - Full Alfie persona")
    print("  • fable_medium  - British accent + character")
    print()
    print("Recommendation: Start with onyx_medium or fable_medium")
    print()


def show_enhancement_preview():
    """Show how the script gets enhanced."""
    print("=" * 70)
    print("ENHANCEMENT PREVIEW")
    print("=" * 70)
    print()

    print("ORIGINAL SCRIPT:")
    print(BASE_SCRIPT)
    print()

    print("-" * 70)
    print("MEDIUM ENHANCEMENT (onyx voice):")
    medium = enhance_script_for_voice(BASE_SCRIPT, "onyx", "medium")
    print(medium)
    print()

    print("-" * 70)
    print("HIGH ENHANCEMENT (maximum character):")
    high = enhance_script_for_voice(BASE_SCRIPT, "onyx", "high")
    print(high)
    print()

    print("=" * 70)
    print("Key Changes:")
    print("  • Added conversational markers (mate, right, see, innit)")
    print("  • British colloquialisms (proper, fancy, innit)")
    print("  • Strategic pauses with commas")
    print("  • Phonetic hints (Tems for Thames)")
    print("  • Emphasis on key words")
    print("=" * 70)
    print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate enhanced voice samples with character prompts"
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show enhancement preview without generating audio"
    )
    parser.add_argument(
        "--hd",
        action="store_true",
        default=True,
        help="Use tts-1-hd (default: True)"
    )
    parser.add_argument(
        "--output",
        default="voice_samples_enhanced",
        help="Output directory"
    )

    args = parser.parse_args()

    if args.preview:
        show_enhancement_preview()
    else:
        generate_enhanced_samples(
            output_dir=args.output,
            use_hd=args.hd
        )
