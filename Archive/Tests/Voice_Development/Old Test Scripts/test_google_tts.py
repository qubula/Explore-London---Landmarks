"""
Test Google Cloud Text-to-Speech with British voices for Alfie.

Google Cloud TTS doesn't support character prompts, but it has excellent
authentic British accents. We'll test multiple British male voices with
settings optimized for a cabbie character.
"""

import os
import requests
import base64
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GOOGLE_TTS_API_KEY = os.getenv("GOOGLE_TTS_API_KEY")
GOOGLE_TTS_API_URL = "https://texttospeech.googleapis.com/v1/text:synthesize"

# Test script with Tower Bridge
TEST_SCRIPT = """Alright, mate! Let me tell you about Tower Bridge. It's that famous drawbridge you'll spot just by the Tower of London on the Thames's east side. Now, it's not just any old bridge—it's got these massive bascules that lift up to let ships through, and it was originally powered by steam and hydraulics before going electric in the seventies. Funny thing is, plenty of people mix it up with London Bridge just down the river, but Tower Bridge's proper fancy look really sets it apart."""

# British voices to test
BRITISH_VOICES = {
    "en-GB-Neural2-B": {
        "description": "British male, deep voice - BEST for authoritative cabbie",
        "type": "Neural2",
        "gender": "MALE"
    },
    "en-GB-Neural2-D": {
        "description": "British male, conversational - Good for friendly cabbie",
        "type": "Neural2",
        "gender": "MALE"
    },
    "en-GB-Wavenet-B": {
        "description": "British male, premium quality - Natural storyteller",
        "type": "WaveNet",
        "gender": "MALE"
    },
    "en-GB-Wavenet-D": {
        "description": "British male, mature voice - Experienced guide",
        "type": "WaveNet",
        "gender": "MALE"
    },
}


def test_google_voice(
    voice_name: str,
    voice_info: dict,
    text: str,
    speaking_rate: float = 0.9,
    pitch: float = -3.0,
    output_dir: str = "voice_samples_google"
):
    """
    Test a Google Cloud TTS voice.

    Args:
        voice_name: Voice identifier (e.g., "en-GB-Neural2-B")
        voice_info: Voice metadata
        text: Script to speak
        speaking_rate: 0.25-4.0 (1.0=normal, <1.0=slower for clarity)
        pitch: -20 to +20 (lower = deeper, more mature)
        output_dir: Where to save samples
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    if not GOOGLE_TTS_API_KEY:
        print("❌ ERROR: GOOGLE_TTS_API_KEY not set in .env")
        return False

    print(f"🎙️  {voice_name}")
    print(f"   {voice_info['description']}")
    print(f"   Settings: speaking_rate={speaking_rate}, pitch={pitch}")

    # Build request
    request_data = {
        "input": {"text": text},
        "voice": {
            "languageCode": "en-GB",
            "name": voice_name,
            "ssmlGender": voice_info["gender"]
        },
        "audioConfig": {
            "audioEncoding": "MP3",
            "speakingRate": speaking_rate,
            "pitch": pitch,
            "volumeGainDb": 0.0,
            "sampleRateHertz": 24000
        }
    }

    try:
        response = requests.post(
            f"{GOOGLE_TTS_API_URL}?key={GOOGLE_TTS_API_KEY}",
            json=request_data
        )

        if response.status_code == 200:
            result = response.json()
            audio_content = base64.b64decode(result["audioContent"])

            filename = f"{voice_name.lower().replace('-', '_')}.mp3"
            file_path = output_path / filename

            with open(file_path, 'wb') as f:
                f.write(audio_content)

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
    """Generate samples with different British voices."""

    print("=" * 70)
    print("GOOGLE CLOUD TTS - BRITISH VOICES TEST")
    print("Strong British accent, slower speaking rate")
    print("=" * 70)
    print()

    if not GOOGLE_TTS_API_KEY:
        print("❌ ERROR: GOOGLE_TTS_API_KEY not set")
        print()
        print("Setup instructions:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Enable Text-to-Speech API")
        print("3. Create API key at https://console.cloud.google.com/apis/credentials")
        print("4. Add to .env: GOOGLE_TTS_API_KEY=your_key_here")
        print()
        print("Note: New accounts get $300 free credit!")
        return

    print(f"Test script ({len(TEST_SCRIPT.split())} words):")
    print(f'"{TEST_SCRIPT[:80]}..."')
    print()
    print("=" * 70)
    print()

    # Voice settings optimized for cabbie character:
    # - speaking_rate=0.9 (slightly slower for clarity, not too fast)
    # - pitch=-3.0 (deeper voice for middle-aged male)

    successful = 0
    for voice_name, voice_info in BRITISH_VOICES.items():
        result = test_google_voice(
            voice_name,
            voice_info,
            TEST_SCRIPT,
            speaking_rate=0.9,  # Slightly slower, clear delivery
            pitch=-3.0           # Deeper, mature male voice
        )
        if result:
            successful += 1
        print()

    print("=" * 70)
    print(f"RESULTS: {successful}/{len(BRITISH_VOICES)} successful")
    print("=" * 70)
    print()
    print("Location: voice_samples_google/")
    print()
    print("Listen to each voice:")
    print("  • en_gb_neural2_b  - Deep, authoritative (RECOMMENDED)")
    print("  • en_gb_neural2_d  - Conversational, friendly")
    print("  • en_gb_wavenet_b  - Premium quality, natural")
    print("  • en_gb_wavenet_d  - Mature, experienced")
    print()
    print("Settings used:")
    print("  • Speaking rate: 0.9 (10% slower than normal)")
    print("  • Pitch: -3.0 (deeper, middle-aged male)")
    print("  • Accent: British English (en-GB)")
    print()
    print("If you want even slower, edit speaking_rate to 0.85 or 0.8")
    print("If you want deeper voice, edit pitch to -4.0 or -5.0")
    print()


if __name__ == "__main__":
    main()
