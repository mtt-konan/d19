"""Tests for the D-scaling K_n fast generator (wl085, OPEN_DIRECTIONS A.7).

These tests exercise the algebra-only helpers (no PARI). The PARI-dependent
``enumerate_rational_n`` is exercised via a smoke test that takes ~1s and
verifies the wl063 K_10 hub (554400, 926640) is reproduced from primitive
(70, 117) at d=7920.
"""

from __future__ import annotations

import os
import sys
from fractions import Fraction
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.concordant.dscale_kn import (  # noqa: E402
    KnCandidate,
    RationalNPool,
    is_rational_square,
    k_for_d,
    scan_d_for_target_k,
)


def test_is_rational_square_true_cases() -> None:
    ok, sn, sd = is_rational_square(9, 16)
    assert ok and sn == 3 and sd == 4

    ok, sn, sd = is_rational_square(1, 1)
    assert ok and sn == 1 and sd == 1


def test_is_rational_square_false_cases() -> None:
    ok, _, _ = is_rational_square(8, 16)  # 8 not a square
    assert not ok

    ok, _, _ = is_rational_square(9, 12)  # 12 not a square
    assert not ok

    ok, _, _ = is_rational_square(0, 1)  # zero not allowed
    assert not ok

    ok, _, _ = is_rational_square(-9, 16)  # negative not allowed
    assert not ok


def test_k_for_d_basic() -> None:
    # n's: 1/2, 3/4, 5/6
    ns = [Fraction(1, 2), Fraction(3, 4), Fraction(5, 6)]
    # d=12: all denoms divide 12 → all three become integers
    Ns = k_for_d(ns, 12)
    # 1/2·12=6, 3/4·12=9, 5/6·12=10
    assert Ns == [6, 9, 10]

    # d=4: only 1/2 and 3/4 work (6 doesn't divide 4)
    Ns = k_for_d(ns, 4)
    # 1/2·4=2, 3/4·4=3
    assert Ns == [2, 3]


def test_k_for_d_dedup() -> None:
    # Duplicate Ns get deduplicated (different fractions can give same N at d)
    ns = [Fraction(1, 2), Fraction(3, 6)]  # 3/6 reduces to 1/2 normally but
    # k_for_d takes raw input; both give 6 at d=12 -> one
    Ns = k_for_d(ns, 12)
    assert Ns == [6]


def test_scan_d_target_k_smoke() -> None:
    """Synthetic pool: pick rational_ns with known denom structure, check
    that scan_d_for_target_k finds the predicted minimal d."""
    # primitive (a₀, b₀) = (1, 1) (synthetic, for testing logic)
    pool = RationalNPool(
        a0=1,
        b0=1,
        rank_lower=1,
        rank_upper=1,
        n_generators=1,
        rational_ns=[
            Fraction(1, 1),  # always integer
            Fraction(1, 2),  # needs 2 | d
            Fraction(1, 3),  # needs 3 | d
            Fraction(1, 6),  # needs 6 | d
        ],
    )
    # k≥2: d=2 gives {1, 1/2} → 2 integers (1, 1)... wait, 1/2 * 2 = 1, 1*2=2.
    # Actually with d=2: 1*2=2, 1/2*2=1, 1/3 not (3∤2), 1/6 not.
    # So Ns = [1, 2], k=2.
    cands = scan_d_for_target_k(pool, target_k=2, d_max=10)
    assert cands  # must find at least one
    assert cands[0].d == 2  # smallest d
    assert cands[0].k == 2
    assert cands[0].a == 2 and cands[0].b == 2

    # k≥3: needs three n's' denoms to divide d. Only d=6 covers {1,2,3,6}.
    cands = scan_d_for_target_k(pool, target_k=4, d_max=20)
    assert cands[0].d == 6
    assert cands[0].k == 4
    assert cands[0].concordant_N == [1, 2, 3, 6]


def test_kn_candidate_to_dict() -> None:
    c = KnCandidate(
        a=70, b=117, d=1, primitive_a=70, primitive_b=117,
        k=2, concordant_N=[100, 200], rank_lower=3, rank_upper=3,
    )
    d = c.to_dict()
    assert d["a"] == 70 and d["b"] == 117 and d["k"] == 2
    assert d["concordant_N"] == [100, 200]


# PARI-dependent integration test (slow ~1-3s)
@pytest.mark.skipif(
    os.environ.get("SKIP_PARI_TESTS") == "1",
    reason="PARI tests disabled (SKIP_PARI_TESTS=1)",
)
def test_reproduce_wl063_k10_hub() -> None:
    """End-to-end: from primitive (70, 117) at d=7920 we must recover the
    wl063 K_10 hub (554400, 926640) with all 10 N values."""
    from rational_distance.concordant.dscale_kn import enumerate_rational_n

    pool = enumerate_rational_n(
        70, 117, max_depth=50, ratpoints_bound=300_000, rank_combo_bound=6
    )
    assert pool.rank_lower >= 1
    assert pool.n_count >= 100  # we expect ~240 rational n with these params

    Ns = k_for_d(pool.rational_ns, 7920)
    expected = [
        74250, 270270, 330372, 596700, 694980, 739200,
        1426425, 1688148, 1900800, 6918912,
    ]
    assert Ns == expected, f"Got {Ns}, expected {expected}"
