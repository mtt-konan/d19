"""Tests for the pivot-on-N fast multi-concordant-N generator."""

from __future__ import annotations

import sys
from math import gcd, isqrt
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

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
