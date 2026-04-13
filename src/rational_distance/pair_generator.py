"""Generate deduplicated primitive (A, B) pairs from Pythagorean triple pairs.

Extracts the chain-fast pair-generation logic into a reusable generator.
Each yielded pair (A, B) with A ≤ B is the gcd-reduced pair from the
primitive triple-pair parameterisation, suitable for EC analysis.
"""

from __future__ import annotations

from math import ceil, gcd, sqrt

from .math_utils import primitive_pythagorean_triples


def generate_ab_pairs(
    max_hyp: int = 500,
) -> list[tuple[int, int]]:
    """Generate all primitive (A, B) pairs from triple-pair parameterisation.

    For each ordered pair (T1, T2) of primitive triples with hypotenuse ≤ max_hyp,
    computes A = t1·t2/g, B = s1·s2/g where g = gcd(t1, s2), then reduces by
    gcd(A, B) and normalises so A ≤ B.

    Returns:
        Sorted list of unique (A, B) tuples with A ≤ B, gcd(A, B) = 1.
    """
    max_m = ceil(sqrt(max_hyp)) + 1
    triples = [
        (a, b, c)
        for a, b, c in primitive_pythagorean_triples(max_m)
        if c <= max_hyp
    ]

    seen: set[tuple[int, int]] = set()
    for s1, t1, _h1 in triples:
        for s2, t2, _h2 in triples:
            cg = gcd(t1, s2)
            A = (t1 // cg) * t2
            B = s1 * (s2 // cg)

            g = gcd(A, B)
            a, b = A // g, B // g
            if a > b:
                a, b = b, a

            if (a, b) not in seen:
                seen.add((a, b))

    return sorted(seen)
