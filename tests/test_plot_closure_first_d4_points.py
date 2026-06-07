from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory import plot_closure_first_d4_points as plot_d4


def test_load_d4_point_records_requires_serialized_records(tmp_path) -> None:
    path = tmp_path / "points.json"
    path.write_text(json.dumps({"d4_point_records": []}), encoding="utf-8")

    try:
        plot_d4.load_d4_point_records(path)
    except ValueError as exc:
        assert "d4_point_records" in str(exc)
    else:
        raise AssertionError("expected missing d4_point_records to fail")


def test_load_d4_point_records_returns_records(tmp_path) -> None:
    path = tmp_path / "points.json"
    row = {
        "x": "1/3",
        "y": "1/4",
        "x_float": 1 / 3,
        "y_float": 1 / 4,
        "raw_count": 7,
        "best_failed_nearest_delta": 1,
    }
    path.write_text(json.dumps({"d4_point_records": [row]}), encoding="utf-8")

    assert plot_d4.load_d4_point_records(path) == [row]
