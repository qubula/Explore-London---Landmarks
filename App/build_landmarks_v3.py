import os

from dotenv import load_dotenv
load_dotenv()

import json
import time
import re

import wikipediaapi
from openai import OpenAI

# --------------- CONFIGURATION ---------------

# List of GeoJSON files exported from Overpass Turbo
# Put your file(s) in this folder and list them here.
# For example, if you exported "Data_V2.geojson", change to ["Data_V2.geojson"].
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # App folder
V4_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))  # V4 folder
DATA_DIR = os.path.join(V4_DIR, "Data")

INPUT_FILES = [
    os.path.join(DATA_DIR, "Data_Unfiltered.geojson"),
]

# Output: enriched landmarks with cabbie scripts
OUTPUT_FILE = "final_landmarks_v6.3_Big.json"

# Max number of landmarks to process (None = all).
# While testing, keep this small (e.g. 50). Later, set to None.
MAX_ITEMS = None # set to None to process everything

# Debug logging toggle
DEBUG = True

# OpenAI client – reads your API key from environment variable OPENAI_API_KEY
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# --- Check which model OpenAI is actually using ---
def report_model_version():
    try:
        test = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5
        )
        actual = getattr(test, "model", "unknown")
        print(f"Using OpenAI model: {actual}")
    except Exception as e:
        print(f"⚠️ Could not verify model version: {e}")

# Run the model check
report_model_version()


# --------------- WIKIPEDIA SETUP ---------------

wiki = wikipediaapi.Wikipedia(
    user_agent='AlfieCabbieBot/6.0 (example@example.com)',
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI
)

# --------------- HELPER FUNCTIONS ---------------

def simple_cabbie_fallback(landmark_name, wiki_summary):
    """
    If OpenAI fails, generate a simple spoken line so we always have something.
    """
    first_sentence = wiki_summary.split(". ")[0][:200].strip()
    return (
        f"On your left you’ve got {landmark_name}. "
        f"Locals like to say this about it: {first_sentence}."
    )


def trim_to_max_sentences_and_words(text, max_sentences=4, max_words=80):
    """
    Enforce both:
    - maximum number of sentences
    - maximum number of words
    while trying to keep only complete sentences.
    """
    text = text.strip()
    if not text:
        return text

    # Split on likely sentence boundaries
    sentences = re.split(r'(?<=[\.\?\!])\s+', text)
    kept = []
    word_count = 0

    for s in sentences:
        s = s.strip()
        if not s:
            continue
        words = s.split()
        if not words:
            continue

        # Check sentence and word limits
        if len(kept) >= max_sentences:
            break
        if word_count + len(words) > max_words:
            break

        kept.append(" ".join(words))
        word_count += len(words)

    if kept:
        return " ".join(kept)

    # Fallback: if everything fails, just hard-trim the first max_words words
    words = text.split()
    trimmed = " ".join(words[:max_words])
    return trimmed.rstrip(",.;:") + "..."


def tidy_style(text: str) -> str:
    """
    Light clean-up to avoid repetition and heavy slang.
    - Strip repetitive intros like "Right, " or "Alright, ".
    - Soften very strong slang a bit.
    """
    for prefix in ["Right, ", "Alright, "]:
        if text.startswith(prefix):
            text = text[len(prefix):].lstrip()
            break

    # soften very strong slang if it ever appears
    text = text.replace("innit?", "isn’t it?")
    return text


def is_interesting(props):
    """
    Decide if an OSM feature is 'Alfie-worthy' based on its tags.
    We keep obvious landmarks and filter out random shops, banks, etc.
    """

    tourism = props.get("tourism")
    historic = props.get("historic")
    amenity = props.get("amenity")
    building = props.get("building")
    leisure = props.get("leisure")
    place = props.get("place")
    shop = props.get("shop")
    landuse = props.get("landuse")
    memorial = props.get("memorial")
    artwork_type = props.get("artwork_type")

    # --- POSITIVE SIGNALS: we LIKE these ---

    # Tourism-related things
    if tourism in ["attraction", "museum", "gallery", "viewpoint", "theme_park", "zoo", "artwork"]:
        return True

    # Historic things (monuments, memorials, historic buildings, etc.)
    if historic in ["memorial", "monument", "castle", "ruins", "battlefield",
                    "heritage", "archaeological_site", "building", "yes"]:
        return True

    # Explicit memorial / artwork tags (often statues, plaques)
    if memorial or artwork_type:
        return True

    # Cultural venues
    if amenity in ["theatre", "arts_centre", "cinema", "library", "place_of_worship", "townhall"]:
        return True

    # Iconic building types
    if building in ["castle", "cathedral", "church", "chapel", "basilica", "townhall", "museum", "public"]:
        return True

    # Parks and gardens
    if leisure in ["park", "garden", "common"]:
        return True

    # Cemeteries can have big stories
    if landuse == "cemetery":
        return True

    # Named “places” – squares, neighbourhoods etc.
    if place in ["square", "neighbourhood", "suburb", "quarter", "town", "village"]:
        return True

    # --- NEGATIVE SIGNALS: we DON'T want these ---

    # Typical boring amenities
    if amenity in ["bank", "atm", "toilets", "fuel", "parking", "bicycle_parking"]:
        return False

    # Most shops are not landmarks (keep a few big ones)
    if shop and shop not in ["department_store", "mall", "supermarket", "books", "music", "seafood"]:
        return False

    # Default: not interesting enough
    return False


# --------------- MAIN AI FUNCTION (OpenAI) ---------------

def rewrite_with_alfie(landmark_name, wiki_text):
    """
    Turn Wikipedia text into a short spoken story in Alfie's voice.
    - 3–4 sentences, about 60–80 words.
    - First sentence: what the place is and roughly where it is in London.
    - Then: ONE surprising or less obvious detail (odd history, big change, scandal, legend, etc.).
    - Tone: warm London cabbie, friendly and a bit cheeky, but clear for non-native speakers.
    """

    if not client.api_key:
        if DEBUG:
            print("   ⚠️ No OPENAI_API_KEY set. Skipping AI and using fallback.")
        return None

    prompt = f"""
You are Alfie, a friendly London black cab driver.

Speak as if you’re chatting to a passenger in the cab. They may not know London well.

For the landmark below, say:

- 3–4 sentences of natural spoken English (around 60–80 words).
- First sentence: clearly say what the place is and roughly where it is in London.
- - Whenever natural, start the sentence with "'The' + (landmark name)" instead of filler words like “Right,” or “Alright,”.
- Then give ONE surprising or less obvious detail that even many Londoners might not know.
  This could be a strange origin, a big change over time, a scandal, a legend, or an odd fact.
- Keep the tone warm, confident and a bit cheeky, but easy to understand for non-native speakers.
- A little British flavour is fine (“posh”, “bit of a glow-up”), but avoid heavy slang.
- Do not use stock phrases like “cheeky twist”, “funny thing is”, or “not bad, eh?”.
- End on a complete, satisfying thought, like something you’d say just as the cab drives past.

Landmark name: "{landmark_name}"

Source information:
\"\"\"{wiki_text[:2000]}\"\"\"

Now give ONE short spoken paragraph in Alfie’s voice (no bullet points, no headings).
"""

    # ---- First attempt ----
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=220,
            temperature=0.85,
        )
        text = response.choices[0].message.content.strip()
    except Exception as e:
        if DEBUG:
            print(f"   ❌ OpenAI error on first attempt: {e}")
        return None

    # ---- If it ends mid-sentence, ask for one finishing sentence ----
    if not text.endswith((".", "!", "?")):
        if DEBUG:
            print("   🔄 Text ended mid-sentence. Retrying to finish...")

        retry_prompt = f"""
The previous answer ended too early.

Please add ONE more sentence that finishes it naturally and makes it feel complete.

Here is the unfinished text:
\"\"\"{text}\"\"\"

Add just one more sentence in Alfie’s voice. Do NOT restart from the beginning.
"""

        try:
            retry_response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": retry_prompt}],
                max_tokens=60,
                temperature=0.7,
            )
            extra = retry_response.choices[0].message.content.strip()
            text = (text + " " + extra).strip()
        except Exception as e:
            if DEBUG:
                print(f"   ⚠️ Retry failed: {e}")

    # ---- Trim to 4 sentences / 80 words ----
    text = trim_to_max_sentences_and_words(text, max_sentences=4, max_words=80)

    # ---- If it’s very short, ask once to enrich it a bit ----
    word_count = len(text.split())
    if word_count < 45:
        if DEBUG:
            print(f"   🔄 Script too short ({word_count} words). Asking Alfie to enrich it slightly...")

        enrich_prompt = f"""
This spoken description is good but too short:

\"\"\"{text}\"\"\"

Please rewrite it in Alfie’s voice, keeping the same main idea but adding ONE more vivid, surprising detail.
Stay under 80 words in total, and keep it to 3–4 short sentences.
Use clear English that non-native speakers can follow.
"""

        try:
            enrich_response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": enrich_prompt}],
                max_tokens=160,
                temperature=0.8,
            )
            enriched = enrich_response.choices[0].message.content.strip()
            enriched = trim_to_max_sentences_and_words(enriched, max_sentences=4, max_words=80)
            text = enriched
        except Exception as e:
            if DEBUG:
                print(f"   ⚠️ Enrich attempt failed: {e}")

    return text

# --------------- MAIN PIPELINE: BUILD DATABASE ---------------

def build_database():
    print("🚕 Starting Alfie V6 landmark builder...")

    raw_items = []

    # 1. Load raw GeoJSON map data from all input files
    print("📂 Loading map data from GeoJSON files...")

    for path in INPUT_FILES:
        if not os.path.exists(path):
            print(f"   ⚠️ Warning: {path} not found, skipping.")
            continue

        print(f"   📂 Reading {path}...")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            features = data.get("features", [])

            file_total = len(features)
            file_named_interesting = 0
            file_used = 0
import json
import requests
import math
import os
import wikipediaapi
import time

# Wikipedia API Setup
wiki_wiki = wikipediaapi.Wikipedia(
    user_agent='PassingBy_App/1.0 (kuba@example.com)',
    language='en'
)

IMAGE_CACHE_FILE = "landmark_images_cache.json"

# Define the Overpass API endpoint
OVERPASS_URL = "http://overpass-api.de/api/interpreter"

# Define the query to fetch landmarks in London
OVERPASS_QUERY = """
[out:json];
(
  node["tourism"="attraction"](51.28,-0.51,51.69,0.33);
  node["historic"="monument"](51.28,-0.51,51.69,0.33);
  node["historic"="memorial"](51.28,-0.51,51.69,0.33);
  node["amenity"="place_of_worship"](51.28,-0.51,51.69,0.33);
  way["tourism"="attraction"](51.28,-0.51,51.69,0.33);
  way["historic"="monument"](51.28,-0.51,51.69,0.33);
  way["historic"="memorial"](51.28,-0.51,51.69,0.33);
);
out center;
"""

def load_image_cache():
    if os.path.exists(IMAGE_CACHE_FILE):
        with open(IMAGE_CACHE_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_image_cache(cache):
    with open(IMAGE_CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)

image_cache = load_image_cache()

def fetch_image_url(name):
    """Fetch image URL from Wikipedia with caching"""
    if name in image_cache:
        return image_cache[name]
    
    print(f"Fetching image for: {name}...")
    url = None
    try:
        # Try direct name
        page = wiki_wiki.page(name)
        if not page.exists():
            # Try appending London
            page = wiki_wiki.page(f"{name}, London")
        
        if page.exists():
            # Get main image using MediaWiki API for PageImages
            response = requests.get(
                "https://en.wikipedia.org/w/api.php",
                params={
                    "action": "query",
                    "format": "json",
                    "titles": page.title,
                    "prop": "pageimages",
                    "pithumbsize": 600
                },
                timeout=5
            ).json()
            
            pages = response.get("query", {}).get("pages", {})
            for _, pdata in pages.items():
                if "thumbnail" in pdata:
                    url = pdata["thumbnail"]["source"]
                    break
        else:
            print(f"  Page not found for {name}")

    except Exception as e:
        print(f"  Error fetching {name}: {e}")
    
    image_cache[name] = url
    return url

def main():
    print("Fetching data from Overpass API...")
    try:
        response = requests.get(OVERPASS_URL, params={'data': OVERPASS_QUERY})
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    print(f"📊 Found {total} raw map features across all files after interest + geometry filters.")
    print("🕵️ Filtering and enriching with Wikipedia + Alfie V6...")

    final_db = []
    seen_names = set()

    # 2. Process each candidate
    for i, item in enumerate(raw_items):
        # Optional limit for testing
        if MAX_ITEMS is not None and len(final_db) >= MAX_ITEMS:
            print(f"\n⏹ Reached MAX_ITEMS={MAX_ITEMS}, stopping early.")
            break

        name = item["name"]
        tag = item["wiki_tag"]

        # Avoid duplicate names
        if name in seen_names:
            continue

        print(f"[{i}/{total}] Processing {name}...", end="", flush=True)

        # Resolve Wikipedia page
        page = None
        try:
            if tag and isinstance(tag, str) and tag.startswith("en:"):
                page_title = tag.replace("en:", "", 1)
                page = wiki.page(page_title)
            else:
                # Fallback: try using the name directly
                page = wiki.page(name)

            if not page or not page.exists():
                print(" ❌ Wikipedia page not found.")
                continue

            summary = page.summary.strip()
            full_text = page.text.strip()

            # Basic summary quality filter
            if "may refer to:" in summary.lower() or len(summary) < 120:
                print(" ⚪ Too generic/short, skipping.")
                continue

            wiki_source = (summary + "\n\n" + full_text) if full_text else summary

            # Use OpenAI to get Alfie's spoken line
            script = rewrite_with_alfie(name, wiki_source)

            if not script:
                script = simple_cabbie_fallback(name, summary)
                print(" ⚠️ AI failed, used simple fallback.")
            else:
                print(" ✅ Alfie line added.")

            out_item = {
                "name": name,
                "lat": item["lat"],
                "lng": item["lng"],
                "wiki_tag": tag,
                "wiki_url": page.fullurl,
                "summary": summary,
                "script": script
            }

            final_db.append(out_item)
            seen_names.add(name)

        except Exception as e:
            print(f" ❌ Error: {e}")

        # Periodically save progress
        if len(final_db) > 0 and len(final_db) % 10 == 0:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(final_db, f, indent=2, ensure_ascii=False)

        # Be nice to Wikipedia and OpenAI
        time.sleep(1.5)

    # Final save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_db, f, indent=2, ensure_ascii=False)

    print(f"\n🎉 DONE! Saved {len(final_db)} landmarks with stories to {OUTPUT_FILE}")


# --------------- SCRIPT ENTRY POINT ---------------

if __name__ == "__main__":
    build_database()
