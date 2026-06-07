"""Tests for G_M closure-delta helpers."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.results.gm_closure_delta import (
    DeltaRow,
    FullPlaneDeltaRow,
    summarize_full_plane_pair_deltas,
    summarize_pair_deltas,
)


def test_summarize_pair_deltas_reports_all_pair_deltas() -> None:
    summary = summarize_pair_deltas(153, 560, [204, 420, 3900])

    assert summary.A == 153
    assert summary.B == 560
    assert summary.target == 713
    assert summary.k == 3
    assert summary.total_pairs == 3
    assert summary.min_abs_delta == 89
    assert summary.closest_rows == [
        DeltaRow(N1=204, N2=420, delta=89),
    ]


def test_summarize_pair_deltas_keeps_all_tied_closest_rows() -> None:
    summary = summarize_pair_deltas(4, 6, [1, 7, 11])

    assert summary.target == 10
    assert summary.total_pairs == 3
    assert summary.min_abs_delta == 2
    assert summary.closest_rows == [
        DeltaRow(N1=1, N2=7, delta=2),
        DeltaRow(N1=1, N2=11, delta=-2),
    ]


def test_summarize_pair_deltas_returns_empty_for_single_n() -> None:
    summary = summarize_pair_deltas(70, 117, [9360])

    assert summary.target == 187
    assert summary.k == 1
    assert summary.total_pairs == 0
    assert summary.min_abs_delta is None
    assert summary.closest_rows == []


def test_summarize_full_plane_pair_deltas_finds_difference_near_miss() -> None:
    summary = summarize_full_plane_pair_deltas(
        15960,
        61776,
        [4950, 10368, 20007, 49280, 95095],
    )

    assert summary.A == 15960
    assert summary.B == 61776
    assert summary.k == 5
    assert summary.total_relation_rows == 50
    assert summary.min_abs_delta == 1
    assert summary.closest_rows == [
        FullPlaneDeltaRow(
            N1=49280,
            N2=95095,
            relation="diff=|A-B|",
            lhs=45815,
            rhs=45816,
            signed_delta=1,
        ),
    ]
    assert summary.closure_hits == []
    assert summary.min_abs_delta_by_relation == {
        "diff=A+B": 2648,
        "diff=|A-B|": 1,
        "sum=A+B": 8449,
        "sum=|A-B|": 5802,
    }


def test_summarize_full_plane_pair_deltas_allows_equal_n_for_sum_only() -> None:
    summary = summarize_full_plane_pair_deltas(153, 560, [204, 420, 3900])

    assert summary.min_abs_delta == 1
    assert summary.closest_rows == [
        FullPlaneDeltaRow(
            N1=204,
            N2=204,
            relation="sum=|A-B|",
            lhs=408,
            rhs=407,
            signed_delta=-1,
        )
    ]


def test_summarize_full_plane_pair_deltas_reports_exact_closure_hits() -> None:
    summary = summarize_full_plane_pair_deltas(4, 6, [2, 4, 8])

    assert summary.min_abs_delta == 0
    assert (
        FullPlaneDeltaRow(
            N1=2,
            N2=8,
            relation="sum=A+B",
            lhs=10,
            rhs=10,
            signed_delta=0,
        )
        in summary.closure_hits
    )
