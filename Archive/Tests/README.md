# Test Files Archive

This directory contains archived test files and test data from the development of the London Tour Guide application.

## Directory Structure

```
Archive/Tests/
├── LLM_Tagging_Tests/          # LLM-based landmark categorization tests
│   ├── Data/                   # Test data files
│   │   ├── landmark_tags_test.json              # 30-landmark initial test
│   │   ├── landmark_tags_small_test.json        # 20-landmark quick test
│   │   ├── landmark_tags_themes_test.json       # 43-landmark theme test
│   │   ├── test_results_2025-12-13_15-58-57.json # Theme validation results
│   │   └── test_results_2025-12-13_15-59-03.json # Theme validation results
│   └── test_theme_talking_points.py # Theme validation test script
│
├── Legacy_Tests/               # Earlier system tests
│   ├── test_grand_list.py      # Grand landmark list tests
│   ├── test_landmarks.py       # Landmark scoring tests
│   ├── test_planner.py         # Route planning tests
│   └── test_tour_types.py      # Tour type categorization tests
│
└── Voice_Development/          # Audio/TTS testing and development
    ├── Old Test Scripts/       # Voice testing scripts
    │   ├── test_10_landmarks.py
    │   ├── test_alfie_custom.py
    │   ├── test_elevenlabs_custom.py
    │   ├── test_elevenlabs_voices.py
    │   ├── test_george_finetune.py
    │   ├── test_google_tts.py
    │   ├── test_natural_storytelling.py
    │   ├── test_ultra_natural.py
    │   ├── test_vocal_sounds.py
    │   ├── test_voices.py
    │   └── test_voices_enhanced.py
    ├── Voice Test Results/     # Audio test output files
    ├── combine_exhibition_audio.py
    ├── generate_final_samples.py
    └── README.md
```

## LLM Tagging Tests

These tests were used during the development of the dynamic tour-specific script system (Option 2).

### Test Data Files

1. **landmark_tags_test.json** (30 landmarks)
   - Initial test run with diverse sample
   - Date: 2025-12-12
   - Cost: ~$0.07

2. **landmark_tags_small_test.json** (20 landmarks)
   - Quick validation test
   - Date: 2025-12-13
   - Cost: ~$0.05
   - Results: 95% multi-tagged, 2.7 avg tags per landmark

3. **landmark_tags_themes_test.json** (43 landmarks)
   - Comprehensive theme validation (10 landmarks per theme × 8 themes)
   - Date: 2025-12-13
   - Cost: ~$0.10
   - Purpose: Validate talking points for all 8 tour types

4. **test_results_*.json**
   - Theme validation test results
   - Coverage statistics per tour type
   - Quality metrics (word count, relevance)

### Test Scripts

- **test_theme_talking_points.py**: Validates talking points for each theme across sample landmarks

## Legacy Tests

These tests were used during earlier development phases before the LLM-based system.

- **test_grand_list.py**: Tested grand landmark scoring system
- **test_landmarks.py**: Tested landmark data loading and scoring
- **test_planner.py**: Tested route planning algorithms
- **test_tour_types.py**: Tested keyword-based tour type categorization

## Voice Development Tests

Audio generation and text-to-speech testing from December 2024.

### Test Scripts
- **test_elevenlabs_voices.py**: Tested various ElevenLabs voice models
- **test_google_tts.py**: Tested Google Cloud TTS
- **test_alfie_custom.py**: Custom voice testing for "Alfie" persona
- **test_george_finetune.py**: Fine-tuned voice testing for "George"
- **test_natural_storytelling.py**: Natural speech pattern tests
- **test_ultra_natural.py**: Ultra-realistic voice tests
- **test_vocal_sounds.py**: Vocal characteristics and sound quality tests
- **test_voices.py** & **test_voices_enhanced.py**: General voice comparison tests
- **test_10_landmarks.py**: Audio generation for 10 sample landmarks

### Utility Scripts
- **combine_exhibition_audio.py**: Audio file concatenation for exhibitions
- **generate_final_samples.py**: Final audio sample generation

### Test Results
Audio samples and test outputs stored in `Voice Test Results/` directory

## Key Insights from Tests

### Repetition Analysis (from small test)
- 80% of landmarks have name repetition at start of both talking point and generic script
- Only 10% have high word overlap (>6 words) in actual content
- 90% have low overlap - acceptable quality
- 100% have good talking point length (15-60 words)

### Theme Coverage (from themes test)
- Architecture: High coverage with iconic landmarks
- Historical: Excellent coverage with diverse sites
- Royal: Strong coverage with palaces and ceremonial sites
- Museums/Galleries: Complete coverage with major institutions
- Parks/Gardens: Excellent coverage from garden squares to major parks
- Religious: Good coverage with diverse religious sites
- Modern: Strong coverage with 21st century landmarks
- Victorian: Excellent coverage with 19th century sites

### Multi-tagging Success
- 95% of landmarks received multiple tags (2-3 tags per landmark)
- Average 2.7 tags per landmark
- Demonstrates successful contextual understanding by GPT-4o

## Production System

The full production system uses:
- **Data/landmark_tags.json**: 1,327 landmarks with talking points (~$3.90 to generate)
- **App/talking_points.py**: Dynamic script selection module
- **App/llm_tagger.py**: LLM tagging engine

All test files in this archive were used to validate the system before the full batch run.

## Archive Date

Files archived: 2025-12-13

## Notes

These files are kept for reference and documentation purposes. They show the iterative testing process used to develop and validate the LLM-based dynamic script system.
