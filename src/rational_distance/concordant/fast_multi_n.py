"""Pivot-on-N fast generator for multi-concordant-N pairs.

The slow path (`scripts/multi_n/multi_concordant_n_scan.py`) iterates over reduced
coprime pairs (A, B) and runs `find_concordant_by_factorization` per pair.
The fast path inverts the loop: for each candidate A, enumerate the divisor
factorizations of A^2 to recover every N with A^2 + N^2 a perfect square,
then group by N. Pairs (A, B) sharing two or more N's are exactly the
multi-concordant pairs.

Correctness rests on the identity::

    A^2 + N^2 = h^2  ⟺  (h - N)(h + N) = A^2

so every concordant (A, N) corresponds to a divisor pair (p, q) of A^2 with
p < q and p ≡ q (mod 2). This enumeration is exhaustive and unique.

Performance notes
=================

The naive ``_factor(A)`` is O(√A) trial division and dominates the cost at
large ``max_hyp`` (e.g. ~75s of the 75s wall time at max_hyp=1e6).
``iter_concordant_a_n`` therefore precomputes the smallest-prime-factor
(SPF) table over ``[2, max_leg]`` via a linear sieve and reuses it for every
A. This drops the per-A factorization to O(log A) and cuts total wall time
by an order of magnitude on max_hyp ≥ 1e5.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator
from math import gcd, isqrt


def _build_smallest_prime_factor(limit: int) -> list[int]:
    """Linear sieve: ``spf[n]`` = smallest prime factor of n, for n in [2, limit].

    spf[0] = spf[1] = 0 by convention (unused).
    """
    if limit < 2:
        return [0] * (limit + 1)
    spf = [0] * (limit + 1)
    primes: list[int] = []
    for i in range(2, limit + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)
        for p in primes:
            ip = i * p
            if p > spf[i] or ip > limit:
                break
            spf[ip] = p
    return spf


def _factor_with_spf(n: int, spf: list[int]) -> dict[int, int]:
    """Factor ``n`` using the precomputed SPF table; returns ``{prime: exponent}``."""
    out: dict[int, int] = {}
    while n > 1:
        p = spf[n]
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        out[p] = e
    return out


def _factor(n: int) -> tuple[tuple[int, int], ...]:
    """Trial-division factorization. Used as a fallback / for small inputs."""
    factors: list[tuple[int, int]] = []
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            exponent = 0
            while n % divisor == 0:
                n //= divisor
                exponent += 1
            factors.append((divisor, exponent))
        divisor += 1 if divisor == 2 else 2
    if n > 1:
        factors.append((n, 1))
    return tuple(factors)


def _smaller_divisors_from_factors(
    factor_items: tuple[tuple[int, int], ...], root: int
) -> list[int]:
    """Return every divisor of ``root**2`` strictly less than ``root``,
    given the factorization of ``root`` (``root**2`` raises each prime to
    ``2 * exponent``).

    Materialised as a list (no sort) — callers do not depend on order.
    Faster than the iterator form because list comprehension stays in C.
    """
    divisors: list[int] = [1]
    for prime, exponent in factor_items:
        powers = [prime ** k for k in range(2 * exponent + 1)]
        divisors = [d * p for d in divisors for p in powers]
    return [d for d in divisors if d < root]


def iter_square_divisors(square: int) -> Iterator[int]:
    """Yield every divisor of ``square`` strictly less than ``√square``.

    Kept for backward compatibility / public API; uses trial division.
    """
    root = isqrt(square)
    if root * root != square:
        raise ValueError("square must be a perfect square")
    yield from _smaller_divisors_from_factors(_factor(root), root)


def iter_concordant_a_n(max_leg: int) -> Iterator[tuple[int, int]]:
    """Yield every (A, N) with 1 <= A <= max_leg, N >= 1, A^2 + N^2 a square.

    Each (A, N) appears at most once. There is no upper bound on N other
    than the bound implied by the divisor structure of A^2.

    Uses a precomputed smallest-prime-factor table for O(log A) factorization
    per A (linear-sieve build is O(max_leg)).
    """
    if max_leg < 1:
        return
    spf = _build_smallest_prime_factor(max_leg)
    for a in range(1, max_leg + 1):
        if a == 1:
            # 1^2 + N^2 = h^2 ⇒ N=0, no positive N. Skip.
            continue
        factors = _factor_with_spf(a, spf)
        factor_items = tuple(factors.items())
        a_sq = a * a
        for p in _smaller_divisors_from_factors(factor_items, a):
            q = a_sq // p
            if (p + q) & 1:
                continue
            n = (q - p) >> 1
            yield (a, n)


def fast_multi_concordant_pairs(max_hyp: int) -> dict[tuple[int, int], list[int]]:
    """Return all reduced coprime (A, B) with >= 2 concordant N, A < B <= max_hyp.

    For each N, the set of valid A's is collected via `iter_concordant_a_n`.
    Pairs (A, B) drawn from the same A-set share that N as a concordant
    integer. After processing all N's, pairs accumulating two or more N's
    are exactly the multi-concordant pairs.

    Performance: skips (even, even) pair candidates (always gcd ≥ 2 so never
    coprime), and only keeps N-buckets with ≥ 2 entries (single-A buckets
    cannot produce a pair).
    """
    a_sets: dict[int, list[int]] = defaultdict(list)
    for a, n in iter_concordant_a_n(max_hyp):
        a_sets[n].append(a)

    pairs_with_n: dict[tuple[int, int], list[int]] = defaultdict(list)
    for n, a_set in a_sets.items():
        if len(a_set) < 2:
            continue
        # Sort once per bucket, then walk only candidate pairs that are not
        # both even (those are guaranteed non-coprime).
        a_set.sort()
        m = len(a_set)
        for i in range(m):
            ai = a_set[i]
            ai_is_odd = ai & 1
            for j in range(i + 1, m):
                aj = a_set[j]
                # Skip even-even pairs (gcd ≥ 2 always).
                if not ai_is_odd and not (aj & 1):
                    continue
                if gcd(ai, aj) != 1:
                    continue
                pairs_with_n[(ai, aj)].append(n)

    return {key: sorted(ns) for key, ns in pairs_with_n.items() if len(ns) >= 2}


__all__ = ["fast_multi_concordant_pairs", "iter_concordant_a_n", "iter_square_divisors"]
