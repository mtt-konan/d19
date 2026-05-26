"""Tests for G_M closure-delta helpers."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.results.gm_closure_delta import DeltaRow, summarize_pair_deltas


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
