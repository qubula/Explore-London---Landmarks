"""
Generate 10 landmark audio files with FINAL ultra-natural settings.

Voice: George
Settings: stability=0.24, similarity=0.79, style=0.76
Scripts: Enhanced with natural pauses for storytelling
"""

import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# Custom Alfie voice with FINAL ultra-natural settings
ALFIE_ID = "LPRLepQnqpzvBlsHyfyS"
FINAL_SETTINGS = {
    "stability": 0.24,
    "similarity_boost": 0.79,
    "style": 0.76
}


def add_natural_pauses(script: str) -> str:
    """
    Add natural pauses and flow to script for storytelling.

    Techniques:
    - Line breaks after key phrases
    - Ellipses for thinking pauses
    - Strategic paragraph breaks
    """
    # Split into sentences
    sentences = script.split('. ')

    enhanced = []
    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if not sentence:
            continue

        # Add period back if not last sentence
        if i < len(sentences) - 1 and not sentence.endswith('.'):
            sentence += '.'

        # Add natural pauses with ellipses at transition words
        sentence = sentence.replace(', and ', '... and ')
        sentence = sentence.replace(', but ', '... but ')
        sentence = sentence.replace(' though ', '... though ')

        # Line break after sentence
        enhanced.append(sentence)

        # Paragraph break every 2-3 sentences for breathing room
        if (i + 1) % 2 == 0:
            enhanced.append("")  # Empty line = pause

    return '\n\n'.join(enhanced)


def load_top_landmarks(limit=10):
    """Load top landmarks by score."""
    landmarks_file = Path("../Data/final_landmarks_v6.2_Big.json")

    with open(landmarks_file, 'r', encoding='utf-8') as f:
        all_landmarks = json.load(f)

    # Filter landmarks with scripts
    with_scripts = [lm for lm in all_landmarks if lm.get("script")]

    # Score landmarks
    def score_landmark(lm):
        name = lm.get("name", "").lower()
        score = 0

        boost_keywords = {
            "palace": 60, "museum": 50, "cathedral": 55, "abbey": 55,
            "tower": 40, "bridge": 35, "gallery": 50,
            "buckingham": 100, "big ben": 100, "tower of london": 90,
            "st paul": 80, "westminster": 75, "trafalgar": 70,
            "london eye": 65, "british museum": 90, "hyde park": 50
        }

        for keyword, points in boost_keywords.items():
            if keyword in name:
                score += points

        return score

    with_scripts.sort(key=score_landmark, reverse=True)
    return with_scripts[:limit]


def generate_audio(landmark, output_dir="final_exhibition_samples"):
    """Generate audio with final ultra-natural settings."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    script = landmark.get("script", "")
    name = landmark.get("name", "Unknown")

    if not script:
        return False, "No script"

    # Add natural pauses to script
    enhanced_script = add_natural_pauses(script)

    url = f"{ELEVENLABS_API_URL}/{ALFIE_ID}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    data = {
        "text": enhanced_script,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {
            "stability": FINAL_SETTINGS["stability"],
            "similarity_boost": FINAL_SETTINGS["similarity_boost"],
            "style": FINAL_SETTINGS["style"],
            "use_speaker_boost": True
        }
    }

    print(f"🎙️  {name}")
    print(f"   Original: {len(script)} chars, Enhanced: {len(enhanced_script)} chars")

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            # Create safe filename
            safe_name = "".join(c if c.isalnum() or c in (' ', '_') else '_' for c in name)
            safe_name = safe_name.replace(' ', '_').lower()[:50]

            filename = f"{safe_name}.mp3"
            file_path = output_path / filename

            with open(file_path, 'wb') as f:
                f.write(response.content)

            size_kb = file_path.stat().st_size / 1024
            print(f"   ✅ Saved: {filename} ({size_kb:.1f} KB)")
            return True, filename
        else:
            error_data = response.json()
            print(f"   ❌ API Error: {response.status_code}")
            print(f"   {error_data}")
            return False, f"Error {response.status_code}"

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, str(e)

    print()


def main():
    """Generate 10 final exhibition samples."""

    print("=" * 70)
    print("GENERATING FINAL EXHIBITION SAMPLES")
    print(f"Voice: Alfie (Custom Voice - Ultra-Natural Storyteller)")
    print(f"Settings: stability={FINAL_SETTINGS['stability']}, "
          f"similarity={FINAL_SETTINGS['similarity_boost']}, "
          f"style={FINAL_SETTINGS['style']}")
    print("Scripts: Enhanced with natural pauses")
    print("=" * 70)
    print()

    if not ELEVENLABS_API_KEY:
        print("❌ ERROR: ELEVENLABS_API_KEY not set")
        return

    # Load top 10 landmarks
    print("Loading top 10 landmarks...")
    landmarks = load_top_landmarks(10)
    print(f"Found {len(landmarks)} landmarks")
    print()
    print("=" * 70)
    print()

    successful = 0
    failed = 0

    for i, landmark in enumerate(landmarks, 1):
        print(f"[{i}/10]")
        success, result = generate_audio(landmark)
        if success:
            successful += 1
        else:
            failed += 1
        print()

    print("=" * 70)
    print(f"RESULTS: {successful} successful, {failed} failed")
    print("=" * 70)
    print()
    print("Location: final_exhibition_samples/")
    print()
    print("These samples use your FINAL settings:")
    print("  ✨ Ultra-natural storytelling")
    print("  ✨ Maximum variation in timing/tone/speed")
    print("  ✨ Natural pauses and flow")
    print("  ✨ Conversational cabbie character")
    print()
    print("If satisfied with quality and character,")
    print("we'll proceed to generate ALL exhibition audio!")
    print()


if __name__ == "__main__":
    main()
