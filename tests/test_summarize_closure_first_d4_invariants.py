from __future__ import annotations

import json
import subprocess
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
            "A": 7,
            "B": 45,
            "N1": 24,
            "N2": 28,
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
    assert summary["ab_sum"] == 52
    assert summary["ab_diff"] == 38
    assert summary["n_sum"] == 52
    assert summary["n_diff"] == 4
    assert summary["shared_variable_roles"] == {
        "B": ["odd_leg", "odd_leg"],
        "N1": ["even_leg", "even_leg"],
    }
    assert summary["shared_role_pattern"] == "B:odd_leg+odd_leg|N1:even_leg+even_leg"


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
                "A": 7,
                "B": 45,
                "N1": 24,
                "N2": 28,
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
    assert summary["shared_role_pattern_counts"] == {
        "B:odd_leg+odd_leg|N1:even_leg+even_leg": 1,
        "none": 1,
    }
    assert summary["shared_role_pattern_groups_top"] == [
        {
            "shared_role_pattern": "none",
            "d4_points": 1,
            "raw_count": 3,
            "relation_counts": {"sum=A+B": 1},
            "missing_edge_counts": {"B-N1": 1},
            "best_failed_nearest_delta": 11,
            "example": {
                "x": "2/5",
                "y": "1/3",
                "side_n": 30,
                "best_sample": {
                    "A": 12,
                    "B": 18,
                    "N1": 10,
                    "N2": 20,
                    "relation": "sum=A+B",
                    "missing_edges": ["B-N1"],
                    "failed_nearest_delta": 11,
                    "side_n": 30,
                },
            },
        },
        {
            "shared_role_pattern": "B:odd_leg+odd_leg|N1:even_leg+even_leg",
            "d4_points": 1,
            "raw_count": 2,
            "relation_counts": {"sum=A+B": 1},
            "missing_edge_counts": {"A-N2": 1},
            "best_failed_nearest_delta": 7,
            "example": {
                "x": "1/3",
                "y": "2/5",
                "side_n": 30,
                "best_sample": {
                    "A": 7,
                    "B": 45,
                    "N1": 24,
                    "N2": 28,
                    "relation": "sum=A+B",
                    "missing_edges": ["A-N2"],
                    "failed_nearest_delta": 7,
                    "side_n": 30,
                },
            },
        },
    ]


def test_summarize_records_can_focus_pattern_and_relation() -> None:
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
                "A": 7,
                "B": 45,
                "N1": 24,
                "N2": 28,
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

    summary = d4_inv.summarize_records(
        records,
        focus_pattern="B:odd_leg+odd_leg|N1:even_leg+even_leg",
        focus_relation="sum=A+B",
    )

    assert summary["focus"] == {
        "pattern": "B:odd_leg+odd_leg|N1:even_leg+even_leg",
        "relation": "sum=A+B",
        "record_count": 1,
        "raw_count": 2,
    }
    assert len(summary["focus_records"]) == 1
    focus = summary["focus_records"][0]
    assert focus["shared_role_pattern"] == "B:odd_leg+odd_leg|N1:even_leg+even_leg"
    assert focus["best_relation"] == "sum=A+B"
    assert focus["best_sample"] == {
        "A": 7,
        "B": 45,
        "N1": 24,
        "N2": 28,
        "relation": "sum=A+B",
        "missing_edges": ["A-N2"],
        "failed_nearest_delta": 7,
        "side_n": 30,
    }


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


def test_script_path_cli_can_run_from_repo_root(tmp_path) -> None:
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
                    "A": 7,
                    "B": 45,
                    "N1": 24,
                    "N2": 28,
                    "relation": "sum=A+B",
                    "failed_nearest_delta": 7,
                    "missing_edges": ["A-N2"],
                    "square_coordinate": {"x": "1/3", "y": "2/5", "side_n": 30},
                },
            }
        ],
    }
    input_path.write_text(json.dumps(payload), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/summarize_closure_first_d4_invariants.py",
            str(input_path),
            "--out",
            str(output_path),
            "--focus-pattern",
            "B:odd_leg+odd_leg|N1:even_leg+even_leg",
            "--focus-relation",
            "sum=A+B",
        ],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    written = json.loads(output_path.read_text(encoding="utf-8"))
    assert written["shared_role_pattern_counts"] == {
        "B:odd_leg+odd_leg|N1:even_leg+even_leg": 1
    }
    assert written["focus"] == {
        "pattern": "B:odd_leg+odd_leg|N1:even_leg+even_leg",
        "relation": "sum=A+B",
        "record_count": 1,
        "raw_count": 2,
    }
