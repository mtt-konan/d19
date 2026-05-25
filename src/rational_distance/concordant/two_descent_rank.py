"""F₂-rank of half-point 2-descent images for a concordant pair.

For a reduced coprime pair `(A, B)` with concordant integers ``ns``, take one
positive-signature half-point per N, compute its `(sf(x), sf(x + A²))` image
in `(Q*/Q*²)²`, and run F₂-Gaussian elimination over the resulting set of
vectors.

The F₂-rank obtained is a fast, PARI-free proxy for the Mordell-Weil rank
of E_{A,B}: see `docs/work-logs/048-fast-pivot-on-n-scanner.md` §Phase 2.

In particular,

```text
F₂-rank == k     =>  candidate "true" rank-k half-point span (rank ≥ F₂-rank − 2)
F₂-rank <  k     =>  the extra concordant Ns come from 2-torsion folding
```

PARI ellrank confirms the predictions on the three k=4 pairs at
`max_hyp=50000`.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from rational_distance.concordant.half_points import (
    enumerate_half_points_for_concordant_N,
    squarefree_part,
)

F2Vector = dict[tuple[int, int], int]


@dataclass(frozen=True)
class F2RankResult:
    """Outcome of F₂-rank classification on a concordant pair."""

    A: int
    B: int
    ns: tuple[int, ...]
    images: tuple[tuple[int, int], ...]
    """Positive-signature image `(sf(x), sf(x + A²))` for each N in ``ns``."""

    f2_rank: int
    """F₂-rank of the image vectors in `(Q*/Q*²)²`."""

    minimal_relation: tuple[int, ...] | None
    """Smallest subset of ``ns`` whose F₂ images XOR to zero, or ``None``."""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _factor_squarefree_to_f2(value: int, slot: int) -> F2Vector:
    """Encode the squarefree part of ``value`` as F₂ coordinates.

    Each prime divisor (and the sign for negative values) becomes a single
    coordinate ``(prime_or_-1, slot)`` with value 1.
    """
    if value == 0:
        return {}
    out: F2Vector = {}
    sign = -1 if value < 0 else 1
    if sign < 0:
        out[(-1, slot)] = 1
    n = abs(value)
    p = 2
    while p * p <= n:
        exp = 0
        while n % p == 0:
            n //= p
            exp += 1
        if exp % 2 == 1:
            out[(p, slot)] = 1
        p += 1 if p == 2 else 2
    if n > 1:
        out[(n, slot)] = 1
    return out


def _f2_xor(a: F2Vector, b: F2Vector) -> F2Vector:
    out: F2Vector = dict(a)
    for k, v in b.items():
        out[k] = (out.get(k, 0) + v) % 2
    return {k: v for k, v in out.items() if v == 1}


def _f2_rank(vectors: Sequence[F2Vector]) -> int:
    """Gaussian elimination over F₂ on dict-vectors."""
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


def _find_minimal_relation(
    labels: Sequence[int], vectors: Sequence[F2Vector]
) -> tuple[int, ...] | None:
    """Return the smallest non-empty subset of ``labels`` whose vectors XOR to 0.

    Search order: by subset size ascending; within a size, by lexicographic
    order of the included indices. Returns ``None`` if no relation exists.
    """
    n = len(vectors)
    for size in range(1, n + 1):
        for mask in _masks_of_size(n, size):
            combined: F2Vector = {}
            for i in range(n):
                if (mask >> i) & 1:
                    combined = _f2_xor(combined, vectors[i])
            if not combined:
                return tuple(labels[i] for i in range(n) if (mask >> i) & 1)
    return None


def _masks_of_size(n: int, size: int) -> Iterable[int]:
    """Yield all `n`-bit masks with exactly ``size`` bits set, low bits first."""
    if size == 0:
        yield 0
        return
    if size > n:
        return
    indices = list(range(size))
    while True:
        mask = 0
        for idx in indices:
            mask |= 1 << idx
        yield mask
        # advance to next combination
        i = size - 1
        while i >= 0 and indices[i] == n - size + i:
            i -= 1
        if i < 0:
            return
        indices[i] += 1
        for j in range(i + 1, size):
            indices[j] = indices[j - 1] + 1


def _positive_image(A: int, B: int, n: int) -> tuple[int, int]:
    """Return `(sf(x), sf(x + A²))` for one positive-signature half-point."""
    halves = enumerate_half_points_for_concordant_N(A, B, n)
    if not halves:
        raise ValueError(
            f"N={n} is not concordant for (A={A}, B={B}); "
            "no half-point available"
        )
    for h in halves:
        if h.signature[0] > 0 and h.y > 0:
            return (h.signature[0], h.signature[1])
    # fall back to any positive-y half-point (signature[0] could be ±)
    for h in halves:
        if h.y > 0:
            return (h.signature[0], h.signature[1])
    h = halves[0]
    return (h.signature[0], h.signature[1])


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def f2_rank_of_concordant_pair(
    A: int, B: int, ns: Sequence[int]
) -> F2RankResult:
    """Compute the F₂-rank of half-point images for `(A, B)` and ``ns``.

    Parameters
    ----------
    A, B
        The reduced coprime pair (caller's responsibility).
    ns
        Concordant integers for `(A, B)`. ``N`` must satisfy ``A² + N²`` and
        ``B² + N²`` both squares; otherwise a ``ValueError`` is raised.

    Returns
    -------
    F2RankResult
        Carries the input, the positive-sig images, the F₂-rank, and a
        minimal F₂-relation if one exists.
    """
    ns_tuple = tuple(ns)
    if not ns_tuple:
        return F2RankResult(
            A=A, B=B, ns=(), images=(), f2_rank=0, minimal_relation=None
        )

    images: list[tuple[int, int]] = []
    vectors: list[F2Vector] = []
    for n in ns_tuple:
        c1, c2 = _positive_image(A, B, n)
        images.append((c1, c2))
        v_first = _factor_squarefree_to_f2(squarefree_part(c1), 0)
        v_second = _factor_squarefree_to_f2(squarefree_part(c2), 1)
        vectors.append({**v_first, **v_second})

    rank = _f2_rank(vectors)
    relation = (
        _find_minimal_relation(ns_tuple, vectors) if rank < len(ns_tuple) else None
    )
    return F2RankResult(
        A=A,
        B=B,
        ns=ns_tuple,
        images=tuple(images),
        f2_rank=rank,
        minimal_relation=relation,
    )


__all__ = ["F2RankResult", "f2_rank_of_concordant_pair"]
