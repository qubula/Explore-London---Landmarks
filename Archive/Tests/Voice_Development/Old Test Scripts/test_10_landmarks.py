"""
Generate 10 landmark audio files with the chosen George voice settings.

This tests the final voice with a variety of different landmarks to ensure
it sounds good across different script styles and content.
"""

import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# George voice ID with your chosen settings
GEORGE_ID = "JBFqnCBsd6RMkjVDRZzb"
CHOSEN_SETTINGS = {
    "stability": 0.35,
    "similarity_boost": 0.80,
    "style": 0.60
}


def load_top_landmarks(limit=10):
    """Load top landmarks by score from the database."""
    landmarks_file = Path("Data/final_landmarks_v6.2_Big.json")

    with open(landmarks_file, 'r', encoding='utf-8') as f:
        all_landmarks = json.load(f)

    # Filter landmarks with scripts
    with_scripts = [lm for lm in all_landmarks if lm.get("script")]

    # Score landmarks (simplified version)
    def score_landmark(lm):
        name = lm.get("name", "").lower()
        score = 0

        # Boost major landmarks
        boost_keywords = {
            "palace": 60, "museum": 50, "cathedral": 55, "abbey": 55,
            "tower": 40, "bridge": 35, "gallery": 50,
            "buckingham": 100, "big ben": 100, "tower of london": 90,
            "st paul": 80, "westminster": 75, "trafalgar": 70,
            "london eye": 65, "british museum": 90
        }

        for keyword, points in boost_keywords.items():
            if keyword in name:
                score += points

        return score

    # Sort by score and take top N
    with_scripts.sort(key=score_landmark, reverse=True)
    return with_scripts[:limit]


def generate_audio(landmark, output_dir="test_10_landmarks"):
    """Generate audio for a single landmark."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    script = landmark.get("script", "")
    name = landmark.get("name", "Unknown")

    if not script:
        return False, "No script"

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
            "stability": CHOSEN_SETTINGS["stability"],
            "similarity_boost": CHOSEN_SETTINGS["similarity_boost"],
            "style": CHOSEN_SETTINGS["style"],
            "use_speaker_boost": True
        }
    }

    print(f"🎙️  {name}")
    print(f"   Script length: {len(script)} chars, {len(script.split())} words")

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
    """Generate 10 test landmark audio files."""

    print("=" * 70)
    print("GENERATING 10 LANDMARK TEST SAMPLES")
    print(f"Voice: George (stability={CHOSEN_SETTINGS['stability']}, "
          f"similarity={CHOSEN_SETTINGS['similarity_boost']}, "
          f"style={CHOSEN_SETTINGS['style']})")
    print("=" * 70)
    print()

    if not ELEVENLABS_API_KEY:
        print("❌ ERROR: ELEVENLABS_API_KEY not set")
        return

    # Load top 10 landmarks
    print("Loading top 10 landmarks...")
    landmarks = load_top_landmarks(10)
    print(f"Found {len(landmarks)} landmarks with scripts")
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
    print("Location: test_10_landmarks/")
    print()
    print("Listen to all 10 samples to verify:")
    print("  • Voice quality is consistent")
    print("  • Character feels right across different landmarks")
    print("  • Accent and tone are authentic")
    print()
    print("If satisfied, we'll proceed to generate all 50-100 exhibition files!")
    print()


if __name__ == "__main__":
    main()
