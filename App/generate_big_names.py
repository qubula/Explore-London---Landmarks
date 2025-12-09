"""
Generate BIG_NAME_BOOST dictionary using Google Places API ratings.

This script:
1. Gets all "grand" landmarks from the existing database
2. Queries Google Places API for ratings and review counts
3. Ranks landmarks by popularity (rating × log(reviews))
4. Selects top 100 and calculates boost scores
5. Outputs a Python dictionary to copy into landmarks.py

Usage:
    python -m App.generate_big_names

Requirements:
    - GOOGLE_DIRECTIONS_KEY in .env file
    - pip install requests python-dotenv
"""

import os
import json
import time
import math
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Import our existing landmark functions
from App.landmarks import list_grand_landmarks

# Google Places API configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_DIRECTIONS_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_DIRECTIONS_KEY not found in .env file")

PLACES_TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
PLACES_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"


def search_place(landmark_name):
    """
    Search for a place using Google Places Text Search API.
    Returns the Place ID if found, None otherwise.
    """
    params = {
        "query": f"{landmark_name}, London, UK",
        "key": GOOGLE_API_KEY,
    }

    try:
        response = requests.get(PLACES_TEXT_SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "OK" and len(data["results"]) > 0:
            # Return the first result's place_id
            return data["results"][0]["place_id"]
        else:
            print(f"  ⚠️  No results for: {landmark_name}")
            return None

    except Exception as e:
        print(f"  ❌ Error searching for {landmark_name}: {e}")
        return None


def get_place_details(place_id):
    """
    Get place details including rating and user_ratings_total.
    Returns dict with rating and reviews, or None if failed.
    """
    params = {
        "place_id": place_id,
        "fields": "name,rating,user_ratings_total",
        "key": GOOGLE_API_KEY,
    }

    try:
        response = requests.get(PLACES_DETAILS_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "OK":
            result = data["result"]
            return {
                "name": result.get("name"),
                "rating": result.get("rating"),
                "reviews": result.get("user_ratings_total", 0)
            }
        else:
            print(f"  ⚠️  Failed to get details for place_id: {place_id}")
            return None

    except Exception as e:
        print(f"  ❌ Error fetching details for {place_id}: {e}")
        return None


def calculate_popularity_score(rating, reviews):
    """
    Calculate popularity score: rating × log(reviews + 1)
    This prioritizes landmarks with both high ratings AND many reviews.
    """
    if rating is None or reviews is None:
        return 0
    return rating * math.log(reviews + 1)


def calculate_boost_score(rating, reviews):
    """
    Calculate the boost score to add to BIG_NAME_BOOST.
    Formula: (rating - 4.0) × 20 + min(reviews / 100, 40)

    Examples:
    - 4.5★ with 1,000 reviews → 10 + 10 = 20 points
    - 4.7★ with 5,000 reviews → 14 + 40 = 54 points
    - 4.9★ with 10,000 reviews → 18 + 40 = 58 points
    """
    if rating is None or reviews is None or rating < 4.0:
        return 0

    rating_component = (rating - 4.0) * 20
    review_component = min(reviews / 100, 40)

    return int(rating_component + review_component)


def main():
    print("=" * 70)
    print("GENERATING BIG_NAME_BOOST DICTIONARY FROM GOOGLE PLACES API")
    print("=" * 70)
    print()

    # Get all grand landmarks from our database
    print("📍 Loading grand landmarks from database...")
    grand_landmarks = list_grand_landmarks()
    print(f"   Found {len(grand_landmarks)} grand landmarks")
    print()

    # Fetch ratings for each landmark
    print("🔍 Querying Google Places API for ratings...")
    print("   (This will take a few minutes and cost ~$10 in API credits)")
    print()

    enriched_landmarks = []
    api_calls = 0

    for i, landmark in enumerate(grand_landmarks, 1):
        name = landmark["name"]
        print(f"[{i}/{len(grand_landmarks)}] {name}")

        # Search for place
        place_id = search_place(name)
        api_calls += 1

        if place_id:
            # Get details
            time.sleep(0.1)  # Rate limiting: 10 requests/second
            details = get_place_details(place_id)
            api_calls += 1

            if details and details["rating"]:
                popularity = calculate_popularity_score(details["rating"], details["reviews"])
                enriched_landmarks.append({
                    "name": name,
                    "rating": details["rating"],
                    "reviews": details["reviews"],
                    "popularity_score": popularity
                })
                print(f"   ✅ {details['rating']}★ ({details['reviews']:,} reviews)")
            else:
                print(f"   ⚠️  No rating data available")

        time.sleep(0.05)  # Additional rate limiting

    print()
    print(f"✅ API queries complete! Total API calls: {api_calls}")
    print(f"   Estimated cost: ${api_calls * 0.032:.2f}")
    print()

    # Sort by popularity and take top 100
    enriched_landmarks.sort(key=lambda x: x["popularity_score"], reverse=True)
    top_100 = enriched_landmarks[:100]

    print(f"🏆 Top 100 most popular landmarks:")
    print()

    # Generate BIG_NAME_BOOST dictionary
    big_name_boost = {}

    for i, lm in enumerate(top_100, 1):
        boost_score = calculate_boost_score(lm["rating"], lm["reviews"])
        big_name_boost[lm["name"].lower()] = boost_score

        if i <= 20:  # Print top 20 for preview
            print(f"{i:2}. {lm['name'][:40]:40} "
                  f"{lm['rating']}★ ({lm['reviews']:6,} reviews) → +{boost_score:2} pts")

    if len(top_100) > 20:
        print(f"    ... and {len(top_100) - 20} more")

    print()
    print("=" * 70)
    print("GENERATED BIG_NAME_BOOST DICTIONARY")
    print("=" * 70)
    print()
    print("Copy the following dictionary into App/landmarks.py (lines 8-25):")
    print()
    print("BIG_NAME_BOOST = {")

    for name, score in sorted(big_name_boost.items(), key=lambda x: -x[1]):
        print(f'    "{name}": {score},')

    print("}")
    print()

    # Save to Data folder for organization
    output_file = "Data/generated_big_name_boost.txt"
    with open(output_file, "w") as f:
        f.write("# Generated BIG_NAME_BOOST dictionary\n")
        f.write(f"# Generated from Google Places API on {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total landmarks: {len(big_name_boost)}\n")
        f.write(f"# API calls made: {api_calls}\n")
        f.write(f"# Estimated cost: ${api_calls * 0.032:.2f}\n")
        f.write("\n")
        f.write("BIG_NAME_BOOST = {\n")
        for name, score in sorted(big_name_boost.items(), key=lambda x: -x[1]):
            f.write(f'    "{name}": {score},\n')
        f.write("}\n")

    print(f"💾 Dictionary also saved to: {output_file}")
    print()
    print("✅ Done! Update App/landmarks.py with the generated dictionary.")


if __name__ == "__main__":
    main()
