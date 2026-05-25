"""Pivot-on-N fast generator for multi-concordant-N pairs.

The slow path (`scripts/multi_concordant_n_scan.py`) iterates over reduced
coprime pairs (A, B) and runs `find_concordant_by_factorization` per pair.
The fast path inverts the loop: for each candidate A, enumerate the divisor
factorizations of A^2 to recover every N with A^2 + N^2 a perfect square,
then group by N. Pairs (A, B) sharing two or more N's are exactly the
multi-concordant pairs.

Correctness rests on the identity::

    A^2 + N^2 = h^2  ⟺  (h - N)(h + N) = A^2

so every concordant (A, N) corresponds to a divisor pair (p, q) of A^2 with
p < q and p ≡ q (mod 2). This enumeration is exhaustive and unique.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator
from math import gcd


def iter_concordant_a_n(max_leg: int) -> Iterator[tuple[int, int]]:
    """Yield every (A, N) with 1 <= A <= max_leg, N >= 1, A^2 + N^2 a square.

    Each (A, N) appears at most once. There is no upper bound on N other
    than the bound implied by the divisor structure of A^2.
    """
    for a in range(1, max_leg + 1):
        a_sq = a * a
        for p in range(1, a):
            if a_sq % p != 0:
                continue
            q = a_sq // p
            if (p + q) % 2 != 0:
                continue
            n = (q - p) // 2
            yield (a, n)


def fast_multi_concordant_pairs(max_hyp: int) -> dict[tuple[int, int], list[int]]:
    """Return all reduced coprime (A, B) with >= 2 concordant N, A < B <= max_hyp.

    For each N, the set of valid A's is collected via `iter_concordant_a_n`.
    Pairs (A, B) drawn from the same A-set share that N as a concordant
    integer. After processing all N's, pairs accumulating two or more N's
    are exactly the multi-concordant pairs.
    """
    a_sets: dict[int, list[int]] = defaultdict(list)
    for a, n in iter_concordant_a_n(max_hyp):
        a_sets[n].append(a)

    pairs_with_n: dict[tuple[int, int], list[int]] = defaultdict(list)
    for n, a_set in a_sets.items():
        sorted_a = sorted(a_set)
        for i, a in enumerate(sorted_a):
            for b in sorted_a[i + 1 :]:
                if gcd(a, b) != 1:
                    continue
                pairs_with_n[(a, b)].append(n)

    return {
        key: sorted(ns) for key, ns in pairs_with_n.items() if len(ns) >= 2
    }


__all__ = ["fast_multi_concordant_pairs", "iter_concordant_a_n"]
