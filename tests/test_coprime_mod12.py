"""Regression test for the coprime-leg mod-12 theorem (MATH §8.5.1 / wl097).

Theorem: if gcd(A,B)=1 and N is concordant for (A,B) (N^2+A^2 and N^2+B^2 both
perfect squares), then 12 | N. Coprimality is necessary; we also assert the two
documented boundary counterexamples where it fails.
"""

from __future__ import annotations

import sys
from itertools import combinations
from math import gcd, isqrt
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.concordant.fast_multi_n import exact_concordant_pair


def _is_square(n: int) -> bool:
    r = isqrt(n)
    return r * r == n


def test_coprime_legs_force_concordant_N_divisible_by_12() -> None:
    """Exhaustive small-range check: gcd(A,B)=1 => every concordant N ≡ 0 (mod 12)."""
    checked = 0
    for a in range(1, 220):
        for b in range(a + 1, 220):
            if gcd(a, b) != 1:
                continue
            ns = exact_concordant_pair(a, b)
            for n in ns:
                # sanity: each returned N really is concordant
                assert _is_square(n * n + a * a)
                assert _is_square(n * n + b * b)
                assert n % 12 == 0, f"coprime ({a},{b}) has concordant N={n} not divisible by 12"
                checked += 1
    assert checked > 0


def test_no_coprime_concordant_N_pair_for_coprime_leg() -> None:
    """Corollary: coprime (A,B) never has a coprime concordant N-pair (12 | gcd)."""
    for a in range(1, 220):
        for b in range(a + 1, 220):
            if gcd(a, b) != 1:
                continue
            ns = exact_concordant_pair(a, b)
            for ni, nj in combinations(ns, 2):
                assert gcd(ni, nj) % 12 == 0


def test_gcd_aware_mod12_law() -> None:
    """gcd-aware mod-12 theorem (MATH §8.5.2 / wl098): for g = gcd(A,B),
    3 | N whenever 3 ∤ g, and 4 | N whenever 4 ∤ g. Exhaustive small range,
    including (and especially) non-coprime pairs.
    """
    checked = 0
    for a in range(2, 240):
        for b in range(a + 1, 240):
            g = gcd(a, b)
            for n in exact_concordant_pair(a, b):
                if g % 3 != 0:
                    assert n % 3 == 0, f"({a},{b}) g={g}: 3∤g but 3∤N={n}"
                if g % 4 != 0:
                    assert n % 4 == 0, f"({a},{b}) g={g}: 4∤g but 4∤N={n}"
                checked += 1
    assert checked > 0


def test_gcd_aware_recovers_coprime_special_case() -> None:
    """g=1 special case must reproduce 12 | N (consistency with §8.5.1)."""
    for a in range(2, 200):
        for b in range(a + 1, 200):
            if gcd(a, b) != 1:
                continue
            for n in exact_concordant_pair(a, b):
                assert n % 12 == 0


def test_boundary_noncoprime_counterexamples() -> None:
    """Coprimality is necessary: documented failures of each proof step."""
    # (6,15): gcd=3, both multiples of 3 -> step (a) fails, N=8 with 3 ∤ 8
    ns = exact_concordant_pair(6, 15)
    assert 8 in ns and 8 % 12 != 0
    assert _is_square(8 * 8 + 6 * 6) and _is_square(8 * 8 + 15 * 15)
    # (8,20): gcd=4, both even -> step (b) fails, N=15 odd
    ns = exact_concordant_pair(8, 20)
    assert 15 in ns and 15 % 4 != 0
    assert _is_square(15 * 15 + 8 * 8) and _is_square(15 * 15 + 20 * 20)
