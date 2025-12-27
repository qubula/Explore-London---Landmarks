"""
Combine all exhibition audio files into a single MP3 with 8-second breaks.

This creates one continuous audio file that can loop infinitely on any device.
Perfect for ESP32 or simple audio players.

Requirements: pydub (pip install pydub)
Also needs ffmpeg installed: brew install ffmpeg
"""

import os
from pathlib import Path
from pydub import AudioSegment

def create_silence(duration_ms=8000):
    """Create silent audio segment."""
    return AudioSegment.silent(duration=duration_ms)


def combine_audio_files(input_dir="exhibition_audio", output_file="exhibition_loop.mp3"):
    """Combine all audio files with 8-second breaks into one file."""

    input_path = Path(input_dir)

    if not input_path.exists():
        print(f"❌ ERROR: Directory {input_dir} not found")
        return False

    # Get all MP3 files sorted by filename (001_xxx.mp3, 002_xxx.mp3, etc.)
    audio_files = sorted(input_path.glob("*.mp3"))

    if not audio_files:
        print(f"❌ ERROR: No MP3 files found in {input_dir}")
        return False

    print("=" * 70)
    print("COMBINING EXHIBITION AUDIO FILES")
    print(f"Files found: {len(audio_files)}")
    print(f"Break duration: 8 seconds")
    print("=" * 70)
    print()

    # Create the combined audio
    combined = AudioSegment.empty()
    silence = create_silence(8000)  # 8 seconds

    total_duration_ms = 0

    for i, audio_file in enumerate(audio_files, 1):
        print(f"[{i}/{len(audio_files)}] Adding: {audio_file.name}")

        try:
            # Load audio file
            audio = AudioSegment.from_mp3(audio_file)

            # Add to combined audio
            combined += audio
            total_duration_ms += len(audio)

            # Add silence after (except for last file)
            if i < len(audio_files):
                combined += silence
                total_duration_ms += 8000

            # Show progress
            duration_sec = len(audio) / 1000
            print(f"    Duration: {duration_sec:.1f}s")

        except Exception as e:
            print(f"    ❌ Error loading {audio_file.name}: {e}")
            continue

    print()
    print("=" * 70)
    print("EXPORTING COMBINED FILE...")
    print("=" * 70)
    print()

    # Calculate total duration
    total_minutes = total_duration_ms / 1000 / 60

    print(f"📊 Total duration: {total_minutes:.1f} minutes ({total_duration_ms/1000:.0f} seconds)")
    print(f"📁 Output file: {output_file}")
    print()
    print("⏳ Exporting... (this may take a few minutes)")
    print()

    try:
        # Export as MP3
        combined.export(
            output_file,
            format="mp3",
            bitrate="128k",  # Good quality for speech
            parameters=["-ar", "22050"]  # 22.05kHz sample rate (good for speech)
        )

        # Check file size
        file_size_mb = Path(output_file).stat().st_size / (1024 * 1024)

        print("=" * 70)
        print("✅ SUCCESS!")
        print("=" * 70)
        print()
        print(f"Combined audio file created: {output_file}")
        print(f"File size: {file_size_mb:.1f} MB")
        print(f"Duration: {total_minutes:.1f} minutes")
        print(f"Files combined: {len(audio_files)}")
        print()
        print("USAGE:")
        print("  • Copy to ESP32 SD card or flash storage")
        print("  • Play on loop (most audio players have loop/repeat feature)")
        print("  • For exhibition: Set to auto-play on power-up")
        print()
        print("ADVANTAGES:")
        print("  ✅ Simple playback - just loop one file")
        print("  ✅ No complex firmware needed")
        print("  ✅ Works on any audio player")
        print("  ✅ Consistent timing between landmarks")
        print()

        return True

    except Exception as e:
        print(f"❌ ERROR during export: {e}")
        return False


def main():
    """Main function."""

    print()
    print("This will combine all exhibition audio files into one MP3.")
    print()

    # Check if pydub is installed
    try:
        from pydub import AudioSegment
    except ImportError:
        print("❌ ERROR: pydub not installed")
        print()
        print("Install with:")
        print("  pip install pydub")
        print()
        print("Also install ffmpeg:")
        print("  brew install ffmpeg")
        print()
        return

    success = combine_audio_files(
        input_dir="exhibition_audio",
        output_file="exhibition_loop.mp3"
    )

    if not success:
        print("❌ Failed to create combined audio file")


if __name__ == "__main__":
    main()
