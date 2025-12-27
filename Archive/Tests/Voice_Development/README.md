# Voice Development Archive

This folder contains all test files and scripts from the voice development process.

## What's Inside:

### Voice Test Results/
All audio samples generated during voice testing and refinement:
- **voice_samples_custom/** - Initial Adam vs George comparison
- **Voice Tests/** - All George fine-tuning tests
  - george_finetune/ - 9 variations testing stability/similarity/style
  - test_10_landmarks/ - First 10 landmark test with George
  - natural_storytelling/ - Tests to make voice sound less scripted
  - ultra_natural/ - Final ultra-natural mix tests
- **alfie_custom_test/** - Tests with your custom Alfie voice
- **vocal_sounds_test/** - Tests adding vocal fillers (mmm, uh, yeah)
- **final_exhibition_samples_old/** - Old 10-sample test with George

### Old Test Scripts/
Python scripts used for voice testing:
- test_elevenlabs_custom.py - Initial voice comparison
- test_george_finetune.py - Fine-tuning George voice
- test_10_landmarks.py - First 10 landmark generation
- test_natural_storytelling.py - Natural delivery tests
- test_ultra_natural.py - Ultra-natural mix tests
- test_vocal_sounds.py - Vocal filler tests
- test_elevenlabs_voices.py, test_google_tts.py - Early TTS tests
- test_voices.py, test_voices_enhanced.py - Initial voice testing

### Scripts Moved:
- generate_final_samples.py - Generated 10 test samples with Alfie
- test_alfie_custom.py - Tested custom Alfie voice settings
- combine_exhibition_audio.py - Python version of combine script (unused)

## Final Settings Used:

**Voice:** Custom Alfie (LPRLepQnqpzvBlsHyfyS)
**Settings:**
- Stability: 0.24
- Similarity Boost: 0.79
- Style: 0.76

These settings were chosen after extensive testing to achieve:
- Ultra-natural storytelling
- Maximum variation in timing/tone/speed
- Natural pauses and flow
- Conversational London cabbie character

## Final Production Files:

The final exhibition files are in the parent App/ directory:
- **exhibition_audio/** - 99 individual landmark audio files
- **exhibition_loop.mp3** - Combined 48-minute loop
- **exhibition_loop_compatible.mp3** - Re-encoded for compatibility
- **generate_all_exhibition_audio.py** - Production generation script
- **combine_with_ffmpeg.sh** - Combines files with 8-second breaks
