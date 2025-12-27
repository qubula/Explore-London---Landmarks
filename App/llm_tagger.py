"""
LLM-Based Landmark Tagging Engine

This module uses GPT-4o to categorize landmarks into tour types based on
contextual understanding of Wikipedia summaries.

Usage:
    python3 App/llm_tagger.py --test  # Test on 30 landmarks
    python3 App/llm_tagger.py         # Process all 1,327 landmarks
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Tour type definitions for the prompt
TOUR_CATEGORIES = """
1. **architecture** - Buildings, bridges, architectural marvels (Tower Bridge, St Paul's Cathedral)
2. **historical** - Museums, monuments, historical sites (British Museum, Churchill War Rooms)
3. **royal** - Palaces, royal parks, ceremonial sites (Buckingham Palace, Kensington Palace)
4. **museums_galleries** - Art galleries, museums, cultural institutions (Tate Modern, National Gallery)
5. **parks_gardens** - Green spaces, parks, botanical gardens (Hyde Park, Kew Gardens)
6. **religious** - Cathedrals, churches, abbeys, religious sites (Westminster Abbey, temples)
7. **modern** - Contemporary architecture, 21st century landmarks 2000+ (The Shard, London Eye)
8. **victorian** - 19th century landmarks 1837-1901 (Tower Bridge, Victorian railway stations)
"""

# Theme test samples (10 landmarks per theme for comprehensive validation)
THEME_SAMPLES = {
    "architecture": [
        "Tower Bridge", "The Shard", "St Paul's Cathedral", "Lloyd's building",
        "Battersea Power Station", "Westminster Bridge", "Royal Albert Hall",
        "BT Tower", "Leadenhall Building", "Somerset House"
    ],
    "historical": [
        "British Museum", "Churchill War Rooms", "Tower of London",
        "Imperial War Museum", "Monument to the Great Fire", "Old Royal Naval College",
        "HMS Belfast", "Cabinet War Rooms", "Banqueting House", "London Wall"
    ],
    "royal": [
        "Buckingham Palace", "Kensington Palace", "St James's Palace",
        "The Royal Mews", "Clarence House", "Queen Victoria Memorial",
        "Royal Hospital Chelsea", "Hampton Court Palace", "Kew Palace", "Windsor Castle"
    ],
    "museums_galleries": [
        "Tate Modern", "National Gallery", "Victoria and Albert Museum",
        "Natural History Museum", "Science Museum", "Dulwich Picture Gallery",
        "Saatchi Gallery", "Courtauld Gallery", "Wallace Collection", "Serpentine Galleries"
    ],
    "parks_gardens": [
        "Hyde Park", "Regent's Park", "Kew Gardens", "Richmond Park",
        "St James's Park", "Green Park", "Hampstead Heath", "Russell Square",
        "Victoria Park", "Battersea Park"
    ],
    "religious": [
        "Westminster Abbey", "Southwark Cathedral", "St Paul's Cathedral",
        "Temple Church", "Westminster Cathedral", "Brompton Oratory",
        "Central Mosque", "Bevis Marks Synagogue", "St Clement Danes",
        "St Martin-in-the-Fields"
    ],
    "modern": [
        "The Shard", "London Eye", "Millennium Bridge", "Tate Modern",
        "City Hall", "ArcelorMittal Orbit", "Sky Garden", "The Gherkin",
        "Canary Wharf", "Olympic Park"
    ],
    "victorian": [
        "Tower Bridge", "Albert Memorial", "Royal Albert Hall",
        "Natural History Museum", "St Pancras Station", "Victoria and Albert Museum",
        "Battersea Power Station", "Victoria Park", "Waterloo Station", "Clapham Common"
    ]
}

TAGGING_PROMPT_TEMPLATE = """You are an expert London tour guide categorizing landmarks for themed tours.

Given a landmark's name and Wikipedia summary, assign it to relevant tour categories with confidence scores (0.0-1.0).

## Available Tour Categories:

{categories}

## Instructions:

1. Assign 1-3 relevant categories (can be multiple if landmark fits multiple themes)
2. Provide confidence score (0.0-1.0) for each assigned category:
   - 0.9-1.0: Extremely confident (iconic example of the category)
   - 0.7-0.9: Very confident (strong match)
   - 0.5-0.7: Confident (clear match)
   - 0.3-0.5: Somewhat confident (moderate match)
   - 0.0-0.3: Low confidence (weak match, but still relevant)
3. Identify the PRIMARY category (most prominent feature)
4. Brief reasoning (1-2 sentences explaining the categorization)
5. **IMPORTANT**: For EACH assigned category, provide a 1-2 sentence talking point that explains WHY it fits that theme. These will be used in tour guide scripts.

## Landmark:

**Name**: {name}

**Summary**: {summary}

## Response Format (JSON only, no markdown):

{{
    "tags": {{
        "architecture": 0.85,
        "historical": 0.60
    }},
    "primary_tag": "architecture",
    "reasoning": "Primarily an architectural landmark due to iconic design, with historical significance from construction era.",
    "talking_points": {{
        "architecture": "This Gothic Revival masterpiece showcases Victorian engineering at its finest, with its distinctive twin towers and suspended walkways.",
        "historical": "Built in 1894, it witnessed the transformation of London's docklands and served as a vital crossing point during both World Wars."
    }}
}}
"""


def tag_landmark_with_llm(
    name: str,
    summary: str,
    model: str = "gpt-4o",
    max_retries: int = 3
) -> Optional[Dict]:
    """
    Tag a single landmark using LLM.

    Args:
        name: Landmark name
        summary: Wikipedia summary
        model: OpenAI model to use
        max_retries: Number of retry attempts on failure

    Returns:
        Dict with tags, primary_tag, and reasoning, or None on failure
    """
    prompt = TAGGING_PROMPT_TEMPLATE.format(
        categories=TOUR_CATEGORIES,
        name=name,
        summary=summary[:2000]  # Limit summary length to control costs
    )

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a London tour guide expert. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent categorization
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)

            # Validate result structure
            if "tags" not in result or "primary_tag" not in result or "talking_points" not in result:
                print(f"  ⚠️  Invalid response structure for {name}, retrying...")
                continue

            return result

        except json.JSONDecodeError as e:
            print(f"  ⚠️  JSON decode error for {name}: {e}, retrying...")
            time.sleep(1)
            continue

        except Exception as e:
            print(f"  ⚠️  Error tagging {name} (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
            continue

    print(f"  ❌ Failed to tag {name} after {max_retries} attempts")
    return None


def tag_landmarks_batch(
    landmarks: List[Dict],
    model: str = "gpt-4o",
    start_index: int = 0
) -> Dict[str, Dict]:
    """
    Tag a batch of landmarks with progress tracking.

    Args:
        landmarks: List of landmark dicts with 'name' and 'summary'
        model: OpenAI model to use
        start_index: Index to start from (for resume capability)

    Returns:
        Dict mapping landmark name to tagging results
    """
    results = {}
    total = len(landmarks)

    print(f"\n{'='*70}")
    print(f"TAGGING {total} LANDMARKS WITH {model.upper()}")
    print(f"{'='*70}\n")

    start_time = time.time()

    for i, landmark in enumerate(landmarks[start_index:], start=start_index):
        name = landmark.get("name", "Unknown")
        summary = landmark.get("summary", "")

        # Progress indicator
        progress = f"[{i+1:4d}/{total:4d}]"
        print(f"{progress} Processing: {name[:50]:<50}", end="", flush=True)

        # Tag landmark
        result = tag_landmark_with_llm(name, summary, model=model)

        if result:
            results[name] = result
            tags_str = ", ".join(f"{k}:{v:.2f}" for k, v in result.get("tags", {}).items())
            print(f" ✅ {tags_str}")
        else:
            print(f" ❌ Failed")

        # Rate limiting (OpenAI allows ~500 RPM for GPT-4)
        time.sleep(0.15)  # ~400 requests per minute

    elapsed = time.time() - start_time
    print(f"\n{'='*70}")
    print(f"COMPLETED IN {elapsed:.1f}s ({elapsed/total:.2f}s per landmark)")
    print(f"{'='*70}\n")

    return results


def save_results(
    results: Dict[str, Dict],
    output_file: str,
    model: str,
    landmarks: List[Dict]
):
    """
    Save tagging results to JSON file with metadata.

    Args:
        results: Tagging results dict
        output_file: Output file path
        model: Model used
        landmarks: Original landmarks list
    """
    # Calculate statistics
    total_landmarks = len(landmarks)
    tagged_landmarks = len(results)
    multi_tagged = sum(1 for r in results.values() if len(r.get("tags", {})) > 1)
    avg_tags = sum(len(r.get("tags", {})) for r in results.values()) / max(tagged_landmarks, 1)

    output_data = {
        "metadata": {
            "total_landmarks": total_landmarks,
            "tagged_landmarks": tagged_landmarks,
            "model_used": model,
            "generated_at": datetime.now().isoformat(),
            "average_tags_per_landmark": round(avg_tags, 2),
            "multi_tagged_landmarks": multi_tagged,
            "multi_tag_percentage": round(multi_tagged / max(tagged_landmarks, 1) * 100, 1)
        },
        "tags": results
    }

    # Ensure directory exists
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"💾 Results saved to: {output_file}")
    print(f"\n📊 STATISTICS:")
    print(f"   Tagged: {tagged_landmarks}/{total_landmarks} landmarks")
    print(f"   Multi-tagged: {multi_tagged} ({multi_tagged/max(tagged_landmarks,1)*100:.1f}%)")
    print(f"   Avg tags per landmark: {avg_tags:.2f}")


def main():
    """Main entry point for LLM tagging."""
    import argparse

    parser = argparse.ArgumentParser(description='Tag landmarks using LLM')
    parser.add_argument('--test', action='store_true', help='Run test on 30 landmarks only')
    parser.add_argument('--test-small', action='store_true', help='Run quick test on 20 landmarks')
    parser.add_argument('--test-themes', action='store_true', help='Run theme test on 80 landmarks (10 per theme)')
    parser.add_argument('--model', default='gpt-4o', help='OpenAI model to use')
    parser.add_argument('--output', default='Data/landmark_tags.json', help='Output file')
    parser.add_argument('--start', type=int, default=0, help='Start index (for resume)')
    args = parser.parse_args()

    # Load landmarks
    landmarks_file = 'Data/final_landmarks_v6.2_Big.json'
    print(f"📂 Loading landmarks from: {landmarks_file}")

    with open(landmarks_file, 'r', encoding='utf-8') as f:
        all_landmarks = json.load(f)

    print(f"✅ Loaded {len(all_landmarks)} landmarks")

    # Select subset for testing if requested
    if args.test:
        # Select diverse 30-landmark sample
        # Mix of: architecture, historical, parks, multi-category, edge cases, religious
        test_indices = [
            0, 1, 2, 3, 4,      # First 5 (likely major landmarks)
            10, 20, 30, 40, 50,  # Spread across dataset
            100, 200, 300, 400, 500,  # More spread
            600, 700, 800, 900, 1000,  # Even more spread
            50, 150, 250, 350, 450,  # Fill to 30
            550, 650, 750, 850, 950
        ]
        landmarks = [all_landmarks[i] for i in test_indices if i < len(all_landmarks)]
        landmarks = landmarks[:30]  # Ensure exactly 30
        args.output = 'Data/landmark_tags_test.json'
        print(f"🧪 TEST MODE: Processing {len(landmarks)} landmarks")
    elif args.test_small:
        # Quick 20-landmark test - diverse sample
        test_indices = [
            0, 1, 2, 3, 4,      # First 5 (major landmarks)
            10, 25, 50, 75, 100,  # Spread across dataset
            150, 200, 300, 400, 500,  # More coverage
            650, 800, 950, 1100, 1250   # Wide spread
        ]
        landmarks = [all_landmarks[i] for i in test_indices if i < len(all_landmarks)]
        landmarks = landmarks[:20]  # Ensure exactly 20
        args.output = 'Tests/Data/landmark_tags_small_test.json'
        print(f"⚡ QUICK TEST MODE: Processing {len(landmarks)} landmarks")
    elif args.test_themes:
        # Select 80 landmarks (10 per theme) for comprehensive theme validation
        # Create name lookup for fast searching
        landmark_lookup = {lm["name"]: lm for lm in all_landmarks}

        # Collect landmarks from theme samples
        theme_landmarks = []
        found_count = 0
        missing_landmarks = []

        for theme, sample_names in THEME_SAMPLES.items():
            for name in sample_names:
                if name in landmark_lookup:
                    theme_landmarks.append(landmark_lookup[name])
                    found_count += 1
                else:
                    missing_landmarks.append(f"{theme}: {name}")

        # Remove duplicates (some landmarks appear in multiple themes)
        seen_names = set()
        unique_landmarks = []
        for lm in theme_landmarks:
            if lm["name"] not in seen_names:
                unique_landmarks.append(lm)
                seen_names.add(lm["name"])

        landmarks = unique_landmarks
        args.output = 'Tests/Data/landmark_tags_themes_test.json'

        print(f"🎨 THEME TEST MODE: Processing {len(landmarks)} landmarks")
        print(f"   Found: {found_count} landmark references")
        print(f"   Unique: {len(landmarks)} unique landmarks")

        if missing_landmarks:
            print(f"   ⚠️  Missing {len(missing_landmarks)} landmarks from database:")
            for missing in missing_landmarks[:5]:  # Show first 5
                print(f"      - {missing}")
            if len(missing_landmarks) > 5:
                print(f"      ... and {len(missing_landmarks) - 5} more")
    else:
        landmarks = all_landmarks
        print(f"🚀 FULL MODE: Processing {len(landmarks)} landmarks")

    # Tag landmarks
    results = tag_landmarks_batch(
        landmarks,
        model=args.model,
        start_index=args.start
    )

    # Save results
    save_results(results, args.output, args.model, landmarks)

    print(f"\n✅ TAGGING COMPLETE!")


if __name__ == "__main__":
    main()
