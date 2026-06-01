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
from rational_distance.concordant.safe_pair_sieve import (
    gcd_aware_kills,
    guaranteed_divisor,
)


def _v(n: int, p: int) -> int:
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


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


def test_guaranteed_divisor_soundness() -> None:
    """D_g = guaranteed_divisor(A,B) must divide EVERY concordant N (MATH §8.5.2,
    wl099), including the 2-adic refinement v2(g)=1 => 8|N. Exhaustive small range.
    """
    checked = 0
    for a in range(2, 240):
        for b in range(a + 1, 240):
            d = guaranteed_divisor(a, b)
            for n in exact_concordant_pair(a, b):
                assert n % d == 0, f"({a},{b}) D_g={d} but N={n} not divisible"
                checked += 1
    assert checked > 0


def test_guaranteed_divisor_values() -> None:
    """D_g formula: P2(v2(g)) * P3(v3(g)); coprime -> 12, g=2 -> 24."""
    assert guaranteed_divisor(3, 4) == 12   # g=1
    assert guaranteed_divisor(7, 17) == 12  # g=1, both odd
    assert guaranteed_divisor(6, 8) == 24   # g=2: v2=1 -> 8, v3=0 -> 3
    assert guaranteed_divisor(6, 15) == 4   # g=3: v2=0 -> 4, v3=1 -> 1
    assert guaranteed_divisor(8, 20) == 3   # g=4: v2=2 -> 1, v3=0 -> 3
    assert guaranteed_divisor(12, 24) == 1  # g=12: v2>=2, v3>=1


def test_v2g_eq1_forces_8_divides_N() -> None:
    """Refinement: v2(gcd(A,B))=1 => 8 | N for every concordant N."""
    seen = 0
    for a in range(2, 300):
        for b in range(a + 1, 300):
            if _v(gcd(a, b), 2) != 1:
                continue
            for n in exact_concordant_pair(a, b):
                assert n % 8 == 0, f"v2(g)=1 ({a},{b}) has N={n} not divisible by 8"
                seen += 1
    assert seen > 0


def test_gcd_aware_kills_is_sound() -> None:
    """If gcd_aware_kills(A,B) is True, the pair must have NO closure: assert
    its complete concordant set has no N_i±N_j hitting {A+B,|A-B|}."""
    for a in range(2, 200):
        for b in range(a + 1, 200):
            if not gcd_aware_kills(a, b):
                continue
            S = exact_concordant_pair(a, b)
            targets = {a + b, abs(a - b)}
            for i in range(len(S)):
                for j in range(i + 1, len(S)):
                    assert (S[i] + S[j]) not in targets
                    assert abs(S[i] - S[j]) not in targets


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
