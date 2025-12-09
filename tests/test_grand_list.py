import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "App"))

from landmarks import list_grand_landmarks


def test_grand_landmark_list_not_empty():
    grand = list_grand_landmarks()
    assert len(grand) > 5


def test_grand_landmarks_include_big_icons():
    grand = list_grand_landmarks()
    names = [lm["name"].lower() for lm in grand[:20]]

    # Should definitely contain some of the big names near the top
    assert any("palace" in n for n in names) or any("abbey" in n for n in names)
