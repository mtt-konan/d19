"""Pythagorean 4-cycle search (independent module).

Finds integer 4-tuples (a, b, c, d) with 1 ≤ each ≤ max_val satisfying:

  a² + b² = x₁²   (Pythagorean condition on pair (a,b))
  b² + c² = x₂²   (Pythagorean condition on pair (b,c))
  c² + d² = x₃²   (Pythagorean condition on pair (c,d))
  d² + a² = x₄²   (Pythagorean condition on pair (d,a))

Optionally also filters for the unit-square constraint:

  a + c == b + d   (5th constraint)

If the 5th constraint is satisfied, let k = a+c = b+d; then the point
(a/k, b/k) lies in [0,1]² and has rational distances to all four corners
A(0,0), B(1,0), C(1,1), D(0,1) of the unit square:

  dist(P, A) = x₁/k,  dist(P, B) = x₂/k,
  dist(P, C) = x₃/k,  dist(P, D) = x₄/k

This module is intentionally independent of the parametric / EC search
infrastructure so its logic can be audited and extended without risk of
cross-contamination.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from math import gcd, isqrt
from typing import Iterator

import numpy as np
from tqdm import tqdm


# ── Data class ────────────────────────────────────────────────────────────────


@dataclass
class ChainResult:
    """One solution to the Pythagorean 4-cycle system."""

    a: int
    b: int
    c: int
    d: int
    x1: int  # isqrt(a²+b²)
    x2: int  # isqrt(b²+c²)
    x3: int  # isqrt(c²+d²)
    x4: int  # isqrt(d²+a²)
    square_ok: bool  # a+c == b+d

    # Unit-square point (populated when square_ok is True)
    k: int = field(default=0)            # a+c = b+d
    px_num: int = field(default=0)       # reduced numerator of a/k
    px_den: int = field(default=0)       # reduced denominator of a/k
    py_num: int = field(default=0)       # reduced numerator of b/k
    py_den: int = field(default=0)       # reduced denominator of b/k

    def __post_init__(self) -> None:
        if self.square_ok:
            k = self.a + self.c
            self.k = k
            g1 = gcd(self.a, k)
            g2 = gcd(self.b, k)
            self.px_num, self.px_den = self.a // g1, k // g1
            self.py_num, self.py_den = self.b // g2, k // g2

    @property
    def rectangle(self) -> tuple[int, int]:
        """Width and height of the bounding rectangle (a+c) × (b+d)."""
        return (self.a + self.c, self.b + self.d)

    def __str__(self) -> str:
        sq = "✓" if self.square_ok else "✗"
        w, h = self.rectangle
        s = (
            f"({self.a},{self.b},{self.c},{self.d})  "
            f"hyp=({self.x1},{self.x2},{self.x3},{self.x4})  "
            f"rect={w}×{h}  sq={sq}"
        )
        if self.square_ok:
            s += f"  point=({self.px_num}/{self.px_den}, {self.py_num}/{self.py_den})"
        return s


# ── Core helpers ──────────────────────────────────────────────────────────────


def _build_adjacency(
    max_val: int,
    progress: bool = True,
) -> tuple[dict[int, list[int]], dict[int, dict[int, int]]]:
    """Build Pythagorean adjacency structures using numpy.

    Returns:
        adj:  adj[a]    = sorted list of b ∈ [1, max_val] with a²+b² a perfect square
        hyp:  hyp[a][b] = isqrt(a²+b²)  for every such pair
    """
    vals = np.arange(1, max_val + 1, dtype=np.int64)
    adj: dict[int, list[int]] = {}
    hyp: dict[int, dict[int, int]] = {}

    it = range(1, max_val + 1)
    if progress:
        it = tqdm(it, desc="Building Pythagorean pairs", leave=False)

    for a in it:
        sq_a = np.int64(a) ** 2
        sums = sq_a + vals ** 2
        roots = np.floor(np.sqrt(sums.astype(np.float64))).astype(np.int64)
        # Correct float-sqrt rounding errors (±1)
        over = (roots + 1) ** 2 == sums
        roots[over] += 1
        hits = roots ** 2 == sums

        b_arr = vals[hits]
        r_arr = roots[hits]
        adj[a] = b_arr.tolist()
        hyp[a] = {int(b): int(r) for b, r in zip(b_arr, r_arr)}

    return adj, hyp


def _symmetry_group(a: int, b: int, c: int, d: int) -> list[tuple[int, int, int, int]]:
    """Return all 8 dihedral images of a 4-cycle (4 rotations × 2 reflections)."""
    return [
        (a, b, c, d), (b, c, d, a), (c, d, a, b), (d, a, b, c),  # rotations
        (a, d, c, b), (d, c, b, a), (c, b, a, d), (b, a, d, c),  # reflections
    ]


# ── Public API ────────────────────────────────────────────────────────────────


def find_chains(
    max_val: int = 500,
    require_square: bool = False,
    canonical: bool = True,
    progress: bool = True,
) -> list[ChainResult]:
    """Find all Pythagorean 4-cycles (a, b, c, d) with values in [1, max_val].

    Args:
        max_val:        Upper bound for all four integers.
        require_square: If True, only return solutions with a+c == b+d.
        canonical:      If True, deduplicate under cyclic rotation and reflection
                        (8-element dihedral group); keeps the lexicographically
                        smallest representative.
        progress:       Show tqdm progress bars.

    Returns:
        Sorted list of ChainResult objects.
    """
    adj, hyp = _build_adjacency(max_val, progress=progress)
    adj_sets = {a: set(bs) for a, bs in adj.items()}

    results: list[ChainResult] = []
    seen: set[tuple[int, int, int, int]] = set()

    it: Iterator[int] = iter(range(1, max_val + 1))
    if progress:
        it = tqdm(range(1, max_val + 1), desc="Searching 4-cycles", leave=False)  # type: ignore[assignment]

    for a in it:
        for b in adj[a]:
            for c in adj.get(b, []):
                # d must close the cycle: d in adj[c] (c²+d² sq.) ∩ adj[a] (d²+a² sq.)
                d_set = adj_sets.get(c, set()) & adj_sets.get(a, set())
                for d in sorted(d_set):
                    square_ok = (a + c == b + d)
                    if require_square and not square_ok:
                        continue

                    if canonical:
                        key = min(_symmetry_group(a, b, c, d))
                        if key in seen:
                            continue
                        seen.add(key)

                    results.append(
                        ChainResult(
                            a=a, b=b, c=c, d=d,
                            x1=hyp[a][b],
                            x2=hyp[b][c],
                            x3=hyp[c][d],
                            x4=hyp[d][a],
                            square_ok=square_ok,
                        )
                    )

    return results


def results_to_json(
    results: list[ChainResult],
    max_val: int,
    require_square: bool,
    elapsed: float,
) -> dict:
    """Serialise results to a JSON-compatible dict."""
    return {
        "params": {
            "max_val": max_val,
            "require_square": require_square,
        },
        "elapsed_s": round(elapsed, 3),
        "count": len(results),
        "count_square": sum(1 for r in results if r.square_ok),
        "results": [asdict(r) for r in results],
    }
