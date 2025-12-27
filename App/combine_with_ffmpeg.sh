#!/bin/bash
# Combine all exhibition audio files with 8-second silence between them
# Uses ffmpeg directly (more reliable than pydub with Python 3.14)

AUDIO_DIR="exhibition_audio"
OUTPUT_FILE="exhibition_loop.mp3"
TEMP_DIR="temp_combine"
SILENCE_FILE="silence_8s.mp3"

echo "======================================================================"
echo "COMBINING EXHIBITION AUDIO FILES"
echo "Using ffmpeg to create single looping file"
echo "======================================================================"
echo ""

# Check if audio directory exists
if [ ! -d "$AUDIO_DIR" ]; then
    echo "❌ ERROR: Directory $AUDIO_DIR not found"
    exit 1
fi

# Count files
FILE_COUNT=$(ls -1 "$AUDIO_DIR"/*.mp3 2>/dev/null | wc -l | tr -d ' ')
if [ "$FILE_COUNT" -eq 0 ]; then
    echo "❌ ERROR: No MP3 files found in $AUDIO_DIR"
    exit 1
fi

echo "Files found: $FILE_COUNT"
echo "Break duration: 8 seconds"
echo ""

# Create temp directory
mkdir -p "$TEMP_DIR"

# Generate 8 seconds of silence
echo "Creating 8-second silence..."
ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 8 -q:a 2 -acodec libmp3lame "$TEMP_DIR/$SILENCE_FILE" -y 2>/dev/null
echo "✅ Silence created"
echo ""

# Create file list for ffmpeg concat
FILELIST="$TEMP_DIR/filelist.txt"
rm -f "$FILELIST"

echo "Building file list..."
COUNT=0
for file in $(ls -1 "$AUDIO_DIR"/*.mp3 | sort); do
    COUNT=$((COUNT + 1))
    echo "[$COUNT/$FILE_COUNT] $(basename "$file")"

    # Add audio file
    echo "file '../$file'" >> "$FILELIST"

    # Add silence after (except for last file)
    if [ $COUNT -lt $FILE_COUNT ]; then
        echo "file '$SILENCE_FILE'" >> "$FILELIST"
    fi
done

echo ""
echo "======================================================================"
echo "COMBINING FILES WITH FFMPEG..."
echo "======================================================================"
echo ""

# Combine all files
ffmpeg -f concat -safe 0 -i "$FILELIST" -c copy "$OUTPUT_FILE" -y

if [ $? -eq 0 ]; then
    FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    DURATION=$(ffmpeg -i "$OUTPUT_FILE" 2>&1 | grep "Duration" | awk '{print $2}' | tr -d ',')

    echo ""
    echo "======================================================================"
    echo "✅ SUCCESS!"
    echo "======================================================================"
    echo ""
    echo "Combined audio file created: $OUTPUT_FILE"
    echo "File size: $FILE_SIZE"
    echo "Duration: $DURATION"
    echo "Files combined: $FILE_COUNT"
    echo ""
    echo "USAGE:"
    echo "  • Copy to ESP32 SD card or flash storage"
    echo "  • Play on loop (most audio players have loop/repeat feature)"
    echo "  • For exhibition: Set to auto-play on power-up"
    echo ""
    echo "ADVANTAGES:"
    echo "  ✅ Simple playback - just loop one file"
    echo "  ✅ No complex firmware needed"
    echo "  ✅ Works on any audio player"
    echo "  ✅ Consistent timing between landmarks"
    echo ""
else
    echo ""
    echo "❌ ERROR: Failed to combine audio files"
    exit 1
fi

# Cleanup
rm -rf "$TEMP_DIR"

echo "🎉 Exhibition audio loop ready!"
