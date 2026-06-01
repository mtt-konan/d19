"""Tests for the pivot-on-N fast multi-concordant-N generator."""

from __future__ import annotations

import sys
from math import gcd, isqrt
from pathlib import Path

from pytest import MonkeyPatch

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.concordant import fast_multi_n as fast_multi_module
from rational_distance.concordant.fast_multi_n import iter_concordant_a_n


def _brute_force_a_n_pairs(max_leg: int) -> set[tuple[int, int]]:
    pairs: set[tuple[int, int]] = set()
    for a in range(1, max_leg + 1):
        n_max = (a * a) // 2
        for n in range(1, n_max + 1):
            total = a * a + n * n
            root = isqrt(total)
            if root * root == total:
                pairs.add((a, n))
    return pairs


def test_iter_concordant_a_n_matches_brute_force_for_small_max_leg() -> None:
    max_leg = 20
    generated = list(iter_concordant_a_n(max_leg=max_leg))

    assert len(generated) == len(set(generated)), "must yield each (A,N) only once"

    for a, n in generated:
        assert 1 <= a <= max_leg
        assert n >= 1
        total = a * a + n * n
        root = isqrt(total)
        assert root * root == total, f"({a},{n}) does not satisfy A^2+N^2=square"

    assert set(generated) == _brute_force_a_n_pairs(max_leg)


def test_iter_concordant_a_n_includes_known_concordant_examples() -> None:
    pairs = set(iter_concordant_a_n(max_leg=600))

    # (A=153, N=204) is a known concordant pair (153^2 + 204^2 = 255^2)
    assert (153, 204) in pairs
    # (A=560, N=204) is also concordant (560^2 + 204^2 = 596^2)
    assert (560, 204) in pairs


def test_iter_concordant_a_n_uses_spf_factorization(
    monkeypatch: MonkeyPatch,
) -> None:
    """Ensure ``iter_concordant_a_n`` factors every A via the SPF table
    (not via repeated trial division of A^2)."""
    calls: list[int] = []
    original = fast_multi_module._factor_with_spf

    def tracking_factor_with_spf(value: int, spf: list[int]) -> dict[int, int]:
        calls.append(value)
        return original(value, spf)

    monkeypatch.setattr(
        fast_multi_module,
        "_factor_with_spf",
        tracking_factor_with_spf,
    )

    generated = list(fast_multi_module.iter_concordant_a_n(max_leg=20))

    assert generated
    # A=1 is skipped (1^2 + N^2 = h^2 has no positive N), so calls is [2..20].
    assert calls == list(range(2, 21))


def _slow_multi_concordant(max_hyp: int) -> dict[tuple[int, int], list[int]]:
    from rational_distance.concordant.factor_search import find_concordant_by_factorization

    out: dict[tuple[int, int], list[int]] = {}
    for a in range(1, max_hyp + 1):
        for b in range(a + 1, max_hyp + 1):
            if gcd(a, b) != 1:
                continue
            ns = find_concordant_by_factorization(a, b)
            if len(ns) >= 2:
                out[(a, b)] = sorted(ns)
    return out


def test_fast_multi_concordant_pairs_matches_brute_force_at_small_max_hyp() -> None:
    from rational_distance.concordant.fast_multi_n import fast_multi_concordant_pairs

    max_hyp = 200
    fast = fast_multi_concordant_pairs(max_hyp=max_hyp)
    slow = _slow_multi_concordant(max_hyp=max_hyp)

    assert set(fast.keys()) == set(slow.keys())
    for key, expected_ns in slow.items():
        assert sorted(fast[key]) == expected_ns


def _brute_concordant_n_for_leg(a: int, n_cap: int) -> set[int]:
    out: set[int] = set()
    for n in range(1, n_cap + 1):
        total = a * a + n * n
        root = isqrt(total)
        if root * root == total:
            out.add(n)
    return out


def test_concordant_n_for_leg_matches_brute_force() -> None:
    from rational_distance.concordant.fast_multi_n import concordant_n_for_leg

    for a in range(2, 80):
        # every concordant N is <= (a^2 - 1) / 2, so this cap is exhaustive
        n_cap = (a * a) // 2
        assert concordant_n_for_leg(a) == _brute_concordant_n_for_leg(a, n_cap)


def test_exact_concordant_pair_matches_canonical_factor_search() -> None:
    """``exact_concordant_pair`` (divisor-intersection) must agree with the
    canonical ``find_concordant_by_factorization`` on assorted pairs, including
    a scaled (non-coprime) hub far outside any bounded scan range."""
    from rational_distance.concordant.factor_search import (
        find_concordant_by_factorization,
    )
    from rational_distance.concordant.fast_multi_n import exact_concordant_pair

    pairs = [(27, 160), (25, 91), (153, 560), (264, 420), (300, 1092)]
    for a, b in pairs:
        assert exact_concordant_pair(a, b) == sorted(find_concordant_by_factorization(a, b))

    # K_14 scaled hub (prim (91, 990), d = 28560): 14 concordant N, coords ~1e8.
    a, b = 2598960, 28274400
    got = exact_concordant_pair(a, b)
    assert got == sorted(find_concordant_by_factorization(a, b))
    assert len(got) == 14


def test_exact_concordant_pair_factor_hint_matches_plain() -> None:
    """Supplying precomputed factorizations must not change the result."""
    from rational_distance.concordant.fast_multi_n import (
        _factor,
        exact_concordant_pair,
    )

    a0, b0, d = 91, 990, 5040
    a, b = d * a0, d * b0
    # merge factor hints the way k14_search does
    from collections import Counter

    def merge(*facts):
        c: Counter[int] = Counter()
        for f in facts:
            for p, e in f:
                c[p] += e
        return tuple(sorted(c.items()))

    fa = merge(_factor(d), _factor(a0))
    fb = merge(_factor(d), _factor(b0))
    assert exact_concordant_pair(a, b, fa, fb) == exact_concordant_pair(a, b)
