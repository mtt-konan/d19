"""Tests for partner-edge reciprocal / translation audit."""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from rational_distance.concordant.rational_ratio import reciprocal_ratio
from scripts.partner.partner_edge_reciprocal_audit import (
    audit_partner_edge_row,
    audit_partner_orientation,
    partner_edge_quartets,
    summarize_partner_edge_reciprocal_audit,
)


def test_audit_uses_data_n_j_not_constructed_reciprocal() -> None:
    """The second ratio must come from edge ``N_j/B``, not ``lambda/r_i``."""
    row = {"u": [25, 91], "v": [60, 312]}

    (item,) = audit_partner_edge_row(row)

    lam = Fraction(25, 91)
    assert item.r_i == Fraction(60, 91)
    assert item.r_j == Fraction(312, 91)
    assert item.r_j == Fraction(24, 7)
    assert item.constructed_reciprocal == reciprocal_ratio(lam, item.r_i)
    assert item.constructed_reciprocal == Fraction(5, 12)
    assert item.r_j != item.constructed_reciprocal
    assert item.uses_data_n_j
    assert item.both_members
    assert not item.reciprocal
    assert not item.closing_relations


def test_wrong_reciprocal_construction_would_miss_real_n_j() -> None:
    """Show why constructing ``lambda/r`` is not equivalent to reading ``N_j``."""
    a, b, n_i, n_j = 25, 91, 60, 312
    lam = Fraction(a, b)
    r_i = Fraction(n_i, b)
    r_j = Fraction(n_j, b)
    constructed = reciprocal_ratio(lam, r_i)

    assert constructed != r_j
    assert int(constructed * b) != n_j


def test_partner_edge_quartets_is_canonical_under_swap() -> None:
    u = (25, 91)
    v = (60, 312)
    expected = ((25, 91, 60, 312),)

    assert partner_edge_quartets(u, v) == expected
    assert partner_edge_quartets(v, u) == expected


def test_summarize_counts_closure_buckets() -> None:
    rows = [
        {"u": [25, 91], "v": [60, 312]},
        {"u": [25, 91], "v": [312, 60]},
    ]

    summary = summarize_partner_edge_reciprocal_audit(rows)

    assert summary["edges_scanned"] == 2
    assert summary["orientations_audited"] == 2
    assert summary["both_members"] == 2
    assert summary["closure_any"] == 0
    assert summary["closure_true_nonreciprocal"] == 0


def test_audit_orientation_reports_membership_flags() -> None:
    item = audit_partner_orientation(25, 91, 60, 312)

    assert item.r_i_member
    assert item.r_j_member
    assert item.both_members
    assert item.lambda_ratio == Fraction(25, 91)
