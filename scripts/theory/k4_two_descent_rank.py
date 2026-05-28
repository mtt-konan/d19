#!/usr/bin/env python3
"""F2-rank of half-point 2-descent images for the three k=4 pairs.

For each k=4 pair (A, B):
  1. Find concordant N list.
  2. For each N, take one representative half-point Q_N (positive y).
  3. Compute its 2-descent image (sf(x), sf(x+A^2)) in (Q*/Q*^2)^2.
  4. Stack the 4 images as vectors over F2, indexed by primes appearing.
  5. Print the F2-rank and any non-trivial linear relation.

A relation among the 4 images means the 4 half-points are linearly
dependent in E(Q)/2E(Q), which gives a hard upper bound on what naive
2-descent on these points can prove about rank.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


K4_PAIRS: tuple[tuple[int, int], ...] = (
    (11776, 17199),
    (6669, 26656),
    (7337, 28288),
)


def _factor(n: int) -> dict[int, int]:
    out: dict[int, int] = {}
    if n == 0:
        return out
    sign = -1 if n < 0 else 1
    if sign == -1:
        out[-1] = 1
    n = abs(n)
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def _squarefree_factors(n: int) -> dict[int, int]:
    """Squarefree representation as exponent dict mod 2 (values in {0, 1})."""
    if n == 0:
        return {}
    factors = _factor(n)
    return {p: e % 2 for p, e in factors.items() if e % 2 == 1}


F2Vector = dict[tuple[int, int], int]


def _f2_xor(a: F2Vector, b: F2Vector) -> F2Vector:
    out: F2Vector = dict(a)
    for k, v in b.items():
        out[k] = (out.get(k, 0) + v) % 2
    return {k: v for k, v in out.items() if v == 1}


def _f2_rank(vectors: list[F2Vector]) -> int:
    """Gaussian elimination over F2 on dict-vectors."""
    pivots: dict[tuple[int, int], F2Vector] = {}
    for vec in vectors:
        v: F2Vector = dict(vec)
        while v:
            pivot = max(v.keys())
            if pivot in pivots:
                v = _f2_xor(v, pivots[pivot])
            else:
                pivots[pivot] = v
                break
    return len(pivots)


def _find_relation(
    labels: list[str], vectors: list[F2Vector]
) -> list[list[str]]:
    """Find one non-trivial F2-relation among the vectors, if any."""
    n = len(vectors)
    relations: list[list[str]] = []
    for mask in range(1, 1 << n):
        combined: F2Vector = {}
        for i in range(n):
            if (mask >> i) & 1:
                combined = _f2_xor(combined, vectors[i])
        if not combined:
            chosen = [labels[i] for i in range(n) if (mask >> i) & 1]
            relations.append(chosen)
            return relations
    return relations


def main() -> int:
    from rational_distance.concordant.factor_search import find_concordant_by_factorization
    from rational_distance.concordant.half_points import enumerate_half_points_for_concordant_N

    for a, b in K4_PAIRS:
        ns = sorted(find_concordant_by_factorization(a, b))
        print(f"=== ({a}, {b})  A+B = {a + b} ===")
        print(f"concordant N: {ns}")

        labels: list[str] = []
        first_coords: list[int] = []
        second_coords: list[int] = []
        vectors: list[F2Vector] = []
        for n in ns:
            halves = enumerate_half_points_for_concordant_N(a, b, n)
            positive = [h for h in halves if h.signature[0] > 0]
            if not positive:
                continue
            sig = positive[0].signature
            labels.append(f"N={n}")
            first_coords.append(sig[0])
            second_coords.append(sig[1])
            vec_first = _squarefree_factors(sig[0])
            vec_second = _squarefree_factors(sig[1])
            combined: F2Vector = {}
            for p, e in vec_first.items():
                combined[(p, 0)] = e
            for p, e in vec_second.items():
                combined[(p, 1)] = e
            vectors.append(combined)

        rank = _f2_rank(vectors)
        print("  positive-sig images:")
        for label, c1, c2 in zip(labels, first_coords, second_coords, strict=True):
            print(f"    {label:>10}: ({c1}, {c2})")
        print(f"  F2-rank of 4 images in (Q*/Q*^2)^2: {rank}")
        if rank < len(vectors):
            relation = _find_relation(labels, vectors)
            for rel in relation:
                print(f"  F2-relation: XOR of {rel} == 0")
        else:
            print("  no F2-relation among the 4 images")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
