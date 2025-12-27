import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "App"))

from planner import plan_route


def test_plan_route_fastest_mode_basic():
    result = plan_route("Pimlico Station", "Victoria Station", "1")

    assert "fastest_eta" in result
    assert "chosen_eta" in result
    assert "landmarks" in result
    assert result["mode"] == "Fastest"

    # In fastest mode, chosen == fastest
    assert abs(result["fastest_eta"] - result["chosen_eta"]) < 0.01
