from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


def test_fixed_ratio_concordant_n_uses_exact_factor_search() -> None:
    from rational_distance.concordant.fixed_ratio_exact import fixed_ratio_concordant_n

    assert fixed_ratio_concordant_n(k=7, b=5) == [12]
    assert fixed_ratio_concordant_n(k=7, b=12) == [35]


def test_collect_fixed_ratio_ratios_deduplicates_scaled_b_values() -> None:
    from rational_distance.concordant.fixed_ratio_exact import collect_fixed_ratio_ratios

    summary = collect_fixed_ratio_ratios(k=7, max_b=30)

    assert summary.k == 7
    assert summary.max_b == 30
    assert summary.ratios == (Fraction(12, 5), Fraction(35, 12))
    assert summary.ratio_count == 2
    assert summary.b_with_n_count == 8
    assert summary.total_n_count == 8


def test_find_fixed_ratio_ratio_hits_checks_full_plane_relations() -> None:
    from rational_distance.concordant.fixed_ratio_exact import find_fixed_ratio_ratio_hits

    hits = find_fixed_ratio_ratio_hits(k=7, ratios=(Fraction(2), Fraction(6)))

    assert [(hit.r1, hit.r2, hit.relation) for hit in hits] == [
        (Fraction(2), Fraction(6), "sum=A+B")
    ]


def test_collect_fixed_ratio_ratios_reports_no_hit_for_k7_small_exact_data() -> None:
    from rational_distance.concordant.fixed_ratio_exact import collect_fixed_ratio_ratios

    summary = collect_fixed_ratio_ratios(k=7, max_b=30)

    assert summary.noncenter_hits == ()
    assert summary.centerline_hits == ()


def test_centerline_hits_are_reported_separately_from_noncenter_hits() -> None:
    from rational_distance.concordant.fixed_ratio_exact import find_fixed_ratio_ratio_hits

    hits = find_fixed_ratio_ratio_hits(k=7, ratios=(Fraction(4),), include_centerline=True)

    assert [(hit.r1, hit.r2, hit.relation, hit.centerline) for hit in hits] == [
        (Fraction(4), Fraction(4), "sum=A+B", True)
    ]
