"""
Scrape Wikipedia images for all landmarks in the database.

Creates a separate landmark_images.json file mapping landmark names to image URLs.
This avoids rebuilding the entire landmark database.

Usage:
    python3 App/scrape_landmark_images.py

Optional arguments:
    --limit N     Only process first N landmarks (for testing)
    --start N     Start from landmark index N (for resuming)
"""

import json
import time
import os
import argparse
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')

# Configuration
LANDMARK_FILE = "Data/final_landmarks_v6.2_Big.json"
OUTPUT_FILE = "Data/landmark_images.json"
METADATA_FILE = "Data/landmark_image_metadata.json"
DELAY_SECONDS = 0.5  # Be nice to APIs

# Wikipedia API endpoint
WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
HEADERS = {'User-Agent': 'AlfieTourGuide/1.0 (image_scraper; educational)'}


def get_wikipedia_image(landmark_name, wiki_url=None):
    """
    Fetch the main image URL from a Wikipedia page using MediaWiki API.

    Args:
        landmark_name: Name of the landmark
        wiki_url: Full Wikipedia URL (optional, not used currently)

    Returns:
        Image URL string or None if no suitable image found
    """
    try:
        # Step 1: Get the page image (main thumbnail) using pageimages API
        params = {
            'action': 'query',
            'format': 'json',
            'titles': landmark_name,
            'prop': 'pageimages',
            'pithumbsize': 500,  # Get high-res thumbnail
        }

        response = requests.get(WIKIPEDIA_API, params=params, headers=HEADERS, timeout=10)
        data = response.json()

        # Extract pages data
        pages = data.get('query', {}).get('pages', {})

        if not pages:
            return None

        # Get first (and should be only) page
        page_data = next(iter(pages.values()))

        # Check if we got a thumbnail
        if 'thumbnail' in page_data:
            return page_data['thumbnail']['source']

        # Fallback: try original image
        if 'original' in page_data:
            return page_data['original']['source']

        return None

    except Exception as e:
        print(f"\n   ⚠️  Error fetching image for '{landmark_name}': {e}")
        return None


def search_wikimedia_commons(landmark_name):
    """Search Wikimedia Commons for landmark images"""
    try:
        params = {
            'action': 'query',
            'format': 'json',
            'generator': 'search',
            'gsrsearch': f"{landmark_name} London",
            'gsrnamespace': 6,  # File namespace
            'gsrlimit': 3,
            'prop': 'imageinfo',
            'iiprop': 'url',
            'iiurlwidth': 500
        }
        response = requests.get(
            "https://commons.wikimedia.org/w/api.php",
            params=params,
            headers=HEADERS,
            timeout=10
        )
        data = response.json()

        if 'query' in data and 'pages' in data['query']:
            for page in data['query']['pages'].values():
                if 'imageinfo' in page:
                    return page['imageinfo'][0].get('thumburl')
        return None
    except Exception as e:
        return None


def search_wikimedia_by_coords(lat, lon, radius=500):
    """Search Wikimedia Commons using coordinates"""
    try:
        params = {
            'action': 'query',
            'format': 'json',
            'generator': 'geosearch',
            'ggsprimary': 'all',
            'ggsnamespace': 6,
            'ggsradius': radius,
            'ggscoord': f"{lat}|{lon}",
            'prop': 'imageinfo',
            'iiprop': 'url',
            'iiurlwidth': 500,
            'ggslimit': 3
        }
        response = requests.get(
            "https://commons.wikimedia.org/w/api.php",
            params=params,
            headers=HEADERS,
            timeout=10
        )
        data = response.json()

        if 'query' in data and 'pages' in data['query']:
            for page in data['query']['pages'].values():
                if 'imageinfo' in page:
                    return page['imageinfo'][0].get('thumburl')
        return None
    except Exception as e:
        return None


def search_pexels(landmark_name):
    """Search Pexels for landmark images"""
    if not PEXELS_API_KEY:
        return None

    try:
        headers = {"Authorization": PEXELS_API_KEY}
        params = {
            'query': f"{landmark_name} London",
            'per_page': 5,
            'orientation': 'landscape'
        }
        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers=headers,
            params=params,
            timeout=10
        )
        data = response.json()

        if data.get('photos'):
            return data['photos'][0]['src']['large']
        return None
    except Exception as e:
        return None


def search_unsplash(landmark_name):
    """Search Unsplash for landmark images"""
    if not UNSPLASH_ACCESS_KEY:
        return None

    try:
        headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
        params = {
            'query': f"{landmark_name} London",
            'per_page': 5,
            'orientation': 'landscape'
        }
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            headers=headers,
            params=params,
            timeout=10
        )
        data = response.json()

        if data.get('results'):
            return data['results'][0]['urls']['regular']
        return None
    except Exception as e:
        return None


def get_landmark_image_multi_source(landmark):
    """
    Try multiple image sources in priority order.
    Returns (image_url, source, attribution) tuple.
    """
    name = landmark['name']
    wiki_url = landmark.get('wiki_url')
    lat = landmark.get('lat')
    lon = landmark.get('lng')

    # 1. Try Wikipedia PageImages (current method - fastest)
    image_url = get_wikipedia_image(name, wiki_url)
    if image_url:
        return (image_url, "wikipedia", None)

    # 2. Try Wikimedia Commons search
    image_url = search_wikimedia_commons(name)
    if image_url:
        return (image_url, "wikimedia_commons", None)

    # 3. If coordinates available, try geographic search on Commons
    if lat and lon:
        image_url = search_wikimedia_by_coords(lat, lon)
        if image_url:
            return (image_url, "wikimedia_commons_geo", None)

    # 4. Try Pexels for high-quality stock photos
    image_url = search_pexels(name)
    if image_url:
        return (image_url, "pexels", "Photo from Pexels")

    # 5. Try Unsplash for artistic photos (rate limited to 50/hour)
    image_url = search_unsplash(name)
    if image_url:
        return (image_url, "unsplash", "Photo from Unsplash")

    return (None, None, None)


def main():
    parser = argparse.ArgumentParser(description='Scrape Wikipedia images for landmarks')
    parser.add_argument('--limit', type=int, help='Only process first N landmarks')
    parser.add_argument('--start', type=int, default=0, help='Start from landmark index N')
    args = parser.parse_args()

    print("🖼️  Landmark Image Scraper")
    print("=" * 60)

    # Load existing landmarks
    if not os.path.exists(LANDMARK_FILE):
        print(f"❌ Landmark file not found: {LANDMARK_FILE}")
        return

    with open(LANDMARK_FILE, 'r', encoding='utf-8') as f:
        landmarks = json.load(f)

    total = len(landmarks)
    print(f"📊 Found {total} landmarks in database")

    # Load existing image data if resuming
    image_data = {}
    metadata = {}
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            image_data = json.load(f)
        print(f"📂 Loaded {len(image_data)} existing images")

    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

    # Determine range to process
    start_idx = args.start
    end_idx = min(args.limit, total) if args.limit else total

    print(f"🔍 Processing landmarks {start_idx} to {end_idx}")
    print("=" * 60)

    # Process each landmark
    success_count = 0
    skip_count = 0
    fail_count = 0
    source_stats = {}

    for i in range(start_idx, end_idx):
        landmark = landmarks[i]
        name = landmark['name']

        # Skip if already have image
        if name in image_data and image_data[name]:
            print(f"[{i+1}/{total}] {name} - ⏭️  Already have image")
            skip_count += 1
            continue

        print(f"[{i+1}/{total}] {name}...", end=' ', flush=True)

        # Try to get image from multiple sources
        image_url, source, attribution = get_landmark_image_multi_source(landmark)

        if image_url:
            image_data[name] = image_url
            metadata[name] = {
                "source": source,
                "attribution": attribution
            }
            source_stats[source] = source_stats.get(source, 0) + 1
            print(f"✅ Found ({source})")
            success_count += 1
        else:
            image_data[name] = None
            metadata[name] = {
                "source": None,
                "attribution": None
            }
            print(f"❌ No image")
            fail_count += 1

        # Save progress every 10 landmarks
        if (i + 1) % 10 == 0:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(image_data, f, indent=2, ensure_ascii=False)
            with open(METADATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

        # Be nice to APIs
        time.sleep(DELAY_SECONDS)

    # Final save
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(image_data, f, indent=2, ensure_ascii=False)
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("🎉 Complete!")
    print(f"✅ Found images: {success_count}")
    print(f"⏭️  Skipped (already had): {skip_count}")
    print(f"❌ No images: {fail_count}")

    # Show breakdown by source
    if source_stats:
        print("\n📊 Images by source:")
        for source, count in sorted(source_stats.items(), key=lambda x: x[1], reverse=True):
            print(f"   {source}: {count}")

    total_with_images = sum(1 for url in image_data.values() if url is not None)
    print(f"\n📈 Total coverage: {total_with_images}/{len(image_data)} ({total_with_images/len(image_data)*100:.1f}%)")
    print(f"📁 Saved to: {OUTPUT_FILE}")
    print(f"📁 Metadata: {METADATA_FILE}")


if __name__ == "__main__":
    main()
