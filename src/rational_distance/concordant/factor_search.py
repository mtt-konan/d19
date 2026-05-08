"""PARI-free concordant N search via factor decomposition.

Given integers A < B, find all positive integers N satisfying:
    N² + A² = h3²   (C3)
    N² + B² = h4²   (C4)

Key identity: subtracting C3 from C4 gives
    h4² - h3² = B² - A²
    (h4 - h3)(h4 + h3) = diff,  where diff = B² - A²

For every divisor pair (d1, d2) with d1 * d2 == diff and d1 ≤ d2:
    h3 = (d2 - d1) / 2
    h4 = (d2 + d1) / 2

Both must be positive integers (same-parity requirement), and then:
    N² = h3² - A²

N is a valid concordant integer iff N² ≥ 0 and N² is a perfect square.

Completeness: every integer solution (N, h3, h4) produces exactly one
divisor pair via d1 = h4 - h3, d2 = h4 + h3.  So the enumeration is
provably exhaustive — no upper bound parameter is needed.

Complexity: O(√(B² - A²)) for trial-division factorisation of diff.
For reduced pairs with A, B in the hundreds-to-thousands range this is
typically much faster than the PARI ellratpoints call.
"""

from __future__ import annotations

from math import isqrt


def _divisors_up_to_sqrt(n: int) -> list[int]:
    """Return all divisors d of n with d ≤ sqrt(n), in ascending order."""
    divs: list[int] = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            divs.append(d)
        d += 1
    return divs


def find_concordant_by_factorization(A: int, B: int) -> list[int]:
    """Find all positive integers N with N²+A²=□ and N²+B²=□.

    Uses the factor-decomposition identity h4²-h3² = B²-A² to enumerate
    all solutions directly, without any PARI/EC dependency and without an
    upper-bound parameter.

    Parameters
    ----------
    A, B:
        Positive integers.  A == B is allowed (returns empty list).
        A > B is allowed; the function normalises internally.

    Returns
    -------
    Sorted list of distinct positive integers N satisfying both conditions.
    """
    if A == B:
        return []
    lo, hi = (A, B) if A < B else (B, A)

    a2 = lo * lo
    diff = hi * hi - a2  # > 0 because hi > lo

    results: set[int] = set()
    for d1 in _divisors_up_to_sqrt(diff):
        d2 = diff // d1
        if (d1 + d2) % 2 != 0:
            continue
        h3 = (d2 - d1) // 2
        if h3 < lo:
            continue
        n_sq = h3 * h3 - a2
        if n_sq <= 0:
            continue
        n = isqrt(n_sq)
        if n * n == n_sq:
            results.add(n)

    return sorted(results)


__all__ = ["find_concordant_by_factorization"]
