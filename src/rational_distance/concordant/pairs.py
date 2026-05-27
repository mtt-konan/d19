"""Generate deduplicated primitive (A, B) pairs from Pythagorean triple pairs."""

from __future__ import annotations

from collections.abc import Iterator
from math import ceil, gcd, sqrt

from rational_distance.math_utils import primitive_pythagorean_triples


def iter_ab_pairs(max_hyp: int = 500) -> Iterator[tuple[int, int]]:
    max_m = ceil(sqrt(max_hyp)) + 1
    triples = [
        (a, b, c)
        for a, b, c in primitive_pythagorean_triples(max_m)
        if c <= max_hyp
    ]

    seen: set[int] = set()
    shift = max(1, (max_hyp * max_hyp).bit_length())
    for s1, t1, _h1 in triples:
        for s2, t2, _h2 in triples:
            cg = gcd(t1, s2)
            A = (t1 // cg) * t2
            B = s1 * (s2 // cg)

            g = gcd(A, B)
            a, b = A // g, B // g
            if a > b:
                a, b = b, a

            key = (a << shift) | b
            if key in seen:
                continue
            seen.add(key)
            yield (a, b)


def generate_ab_pairs(max_hyp: int = 500) -> list[tuple[int, int]]:
    """Generate all primitive (A, B) pairs from triple-pair parameterisation."""
    return sorted(iter_ab_pairs(max_hyp))
