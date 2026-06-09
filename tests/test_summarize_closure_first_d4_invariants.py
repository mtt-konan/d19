from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory import summarize_closure_first_d4_invariants as d4_inv


def test_invariant_record_uses_d4_symmetric_coordinate_products() -> None:
    record = {
        "x": "1/3",
        "y": "2/5",
        "x_float": 1 / 3,
        "y_float": 2 / 5,
        "raw_count": 4,
        "best_failed_nearest_delta": 7,
        "best_relation": "sum=A+B",
        "best_missing_edges": ["A-N2"],
        "best_sample": {
            "A": 10,
            "B": 20,
            "N1": 12,
            "N2": 18,
            "relation": "sum=A+B",
            "failed_nearest_delta": 7,
            "missing_edges": ["A-N2"],
            "square_coordinate": {"x": "1/3", "y": "2/5", "side_n": 30},
        },
    }

    summary = d4_inv.invariant_record(record)

    assert summary["x1mx"] == "2/9"
    assert summary["y1my"] == "6/25"
    assert summary["uv_pair"] == ["2/9", "6/25"]
    assert summary["uv_sum"] == "104/225"
    assert summary["uv_product"] == "4/75"
    assert summary["side_n"] == 30
    assert summary["ab_sum"] == 30
    assert summary["ab_diff"] == 10
    assert summary["n_sum"] == 30
    assert summary["n_diff"] == 6


def test_summarize_records_groups_by_invariant_pair_and_tracks_low_delta() -> None:
    records = [
        {
            "x": "1/3",
            "y": "2/5",
            "x_float": 1 / 3,
            "y_float": 2 / 5,
            "raw_count": 2,
            "best_failed_nearest_delta": 7,
            "best_relation": "sum=A+B",
            "best_missing_edges": ["A-N2"],
            "best_sample": {
                "A": 10,
                "B": 20,
                "N1": 12,
                "N2": 18,
                "relation": "sum=A+B",
                "failed_nearest_delta": 7,
                "missing_edges": ["A-N2"],
                "square_coordinate": {"x": "1/3", "y": "2/5", "side_n": 30},
            },
        },
        {
            "x": "2/5",
            "y": "1/3",
            "x_float": 2 / 5,
            "y_float": 1 / 3,
            "raw_count": 3,
            "best_failed_nearest_delta": 11,
            "best_relation": "sum=A+B",
            "best_missing_edges": ["B-N1"],
            "best_sample": {
                "A": 12,
                "B": 18,
                "N1": 10,
                "N2": 20,
                "relation": "sum=A+B",
                "failed_nearest_delta": 11,
                "missing_edges": ["B-N1"],
                "square_coordinate": {"x": "2/5", "y": "1/3", "side_n": 30},
            },
        },
    ]

    summary = d4_inv.summarize_records(records, low_delta=10)

    assert summary["record_count"] == 2
    assert summary["raw_count_total"] == 5
    assert summary["uv_pair_group_count"] == 1
    assert summary["uv_pair_groups_top"][0]["uv_pair"] == ["2/9", "6/25"]
    assert summary["uv_pair_groups_top"][0]["d4_points"] == 2
    assert summary["uv_pair_groups_top"][0]["raw_count"] == 5
    assert summary["low_delta_records"][0]["best_failed_nearest_delta"] == 7


def test_cli_writes_summary_json(tmp_path) -> None:
    input_path = tmp_path / "points.json"
    output_path = tmp_path / "summary.json"
    payload = {
        "max_leg": 100,
        "diff_tail": 300,
        "d4_point_records": [
            {
                "x": "1/3",
                "y": "2/5",
                "x_float": 1 / 3,
                "y_float": 2 / 5,
                "raw_count": 2,
                "best_failed_nearest_delta": 7,
                "best_relation": "sum=A+B",
                "best_missing_edges": ["A-N2"],
                "best_sample": {
                    "A": 10,
                    "B": 20,
                    "N1": 12,
                    "N2": 18,
                    "relation": "sum=A+B",
                    "failed_nearest_delta": 7,
                    "missing_edges": ["A-N2"],
                    "square_coordinate": {"x": "1/3", "y": "2/5", "side_n": 30},
                },
            }
        ],
    }
    input_path.write_text(json.dumps(payload), encoding="utf-8")

    assert d4_inv.main([str(input_path), "--out", str(output_path)]) == 0

    written = json.loads(output_path.read_text(encoding="utf-8"))
    assert written["source"]["max_leg"] == 100
    assert written["source"]["diff_tail"] == 300
    assert written["record_count"] == 1
