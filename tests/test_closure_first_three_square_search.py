from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory import closure_first_three_square_search as closure_first


def _slim_records(rows: list[dict]) -> list[dict]:
    return [
        {
            "A": row["A"],
            "B": row["B"],
            "N1": row["N1"],
            "N2": row["N2"],
            "relation": row["relation"],
            "missing_edges": row["missing_edges"],
            "failed_nearest_delta": row["failed_nearest_delta"],
            "gcd_AB": row["gcd_AB"],
            "gcd_N1N2": row["gcd_N1N2"],
        }
        for row in rows
    ]


def test_scan_fast_matches_legacy_near_miss_results() -> None:
    legacy = closure_first.scan_legacy(max_leg=100, diff_tail=300, top_k=30)
    fast = closure_first.scan_fast(max_leg=100, diff_tail=300, top_k=30)

    keys = [
        "exact_hits_by_relation",
        "exact_hits_sample",
        "near_miss_3of4_by_relation",
        "near_miss_3of4_total",
        "missing_edge_counts",
        "gcd_AB_counts_top",
        "gcd_N1N2_counts_top",
    ]
    for key in keys:
        assert fast[key] == legacy[key]

    assert _slim_records(fast["top_near_misses"]) == _slim_records(legacy["top_near_misses"])


def test_scan_uses_fast_strategy_by_default() -> None:
    result = closure_first.scan(max_leg=100, diff_tail=300, top_k=30)

    assert result["candidate_strategy"] == "three_edge_common_n"
    assert result["near_miss_3of4_total"] == 16
    assert sum(result["exact_hits_by_relation"].values()) == 0


def test_scan_reports_full_delta_1_to_10_distribution_not_top_k_only() -> None:
    result = closure_first.scan_fast(max_leg=100, diff_tail=300, top_k=3)

    assert len(result["top_near_misses"]) == 3
    assert result["near_miss_3of4_total"] == 16
    assert result["failed_delta_counts_1_to_10"] == {"6": 1, "8": 3, "10": 2}
    assert result["failed_signed_delta_counts_1_to_10"] == {"-8": 3, "-6": 1, "10": 2}
    assert result["failed_delta_1_to_10_by_relation"] == {
        "diff=A+B": {"6": 1, "8": 1, "10": 1},
        "sum=A+B": {"8": 2},
        "sum=|A-B|": {"10": 1},
    }
    assert result["failed_delta_1_to_10_by_missing_edge"] == {
        "A-N1": {"6": 1, "8": 1},
        "A-N2": {"8": 1},
        "B-N1": {"8": 1},
        "B-N2": {"10": 2},
    }


def test_d4_point_key_merges_axis_swap_and_scaling() -> None:
    assert closure_first.square_coordinate_for(7, 45, 24, 28, "sum=A+B") == (
        Fraction(7, 52),
        Fraction(6, 13),
        52,
    )

    point_key = closure_first.square_point_key_for(7, 45, 24, 28, "sum=A+B")
    key = closure_first.d4_point_key_for(7, 45, 24, 28, "sum=A+B")

    assert point_key != closure_first.square_point_key_for(24, 28, 7, 45, "sum=A+B")
    assert point_key == closure_first.square_point_key_for(14, 90, 48, 56, "sum=A+B")
    assert key == closure_first.d4_point_key_for(24, 28, 7, 45, "sum=A+B")
    assert key == closure_first.d4_point_key_for(14, 90, 48, 56, "sum=A+B")


def test_scan_reports_d4_distinct_near_miss_points() -> None:
    result = closure_first.scan(max_leg=100, diff_tail=300, top_k=30)

    assert result["near_miss_3of4_total"] == 16
    assert (
        result["near_miss_3of4_d4_point_total"]
        <= result["near_miss_3of4_coordinate_point_total"]
        <= result["near_miss_3of4_total"]
    )
    assert result["near_miss_3of4_d4_point_total"] < result["near_miss_3of4_total"]
    assert result["near_miss_3of4_coordinate_point_minus_d4_point_total"] == (
        result["near_miss_3of4_coordinate_point_total"] - result["near_miss_3of4_d4_point_total"]
    )
    assert result["near_miss_3of4_raw_minus_d4_point_total"] == (
        result["near_miss_3of4_total"] - result["near_miss_3of4_d4_point_total"]
    )


def test_scan_can_include_d4_point_records() -> None:
    result = closure_first.scan(max_leg=100, diff_tail=300, top_k=30, include_d4_points=True)

    records = result["d4_point_records"]

    assert len(records) == result["near_miss_3of4_d4_point_total"]
    assert sum(record["raw_count"] for record in records) == result["near_miss_3of4_total"]
    assert records == sorted(records, key=lambda r: (r["x_float"], r["y_float"]))
    assert {
        "x",
        "y",
        "x_float",
        "y_float",
        "raw_count",
        "best_failed_nearest_delta",
        "best_sample",
    } <= records[0].keys()
