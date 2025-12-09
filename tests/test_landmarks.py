import sys
from pathlib import Path

# Ensure the App/ folder is on sys.path so we can import its modules
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "App"))

from landmarks import score_grand_landmark, list_grand_landmarks


def test_palace_scores_higher_than_square():
    palace = {"name": "Buckingham Palace"}
    square = {"name": "Random Residential Square"}

    assert score_grand_landmark(palace) > score_grand_landmark(square)


def test_cathedral_scores_higher_than_garden():
    cat = {"name": "Westminster Cathedral"}
    garden = {"name": "Small Garden"}

    assert score_grand_landmark(cat) > score_grand_landmark(garden)
