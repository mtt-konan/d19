"""Cycle linear-relation tracking on the concordant curve (OPEN_DIRECTIONS A.2).

For a pair ``(A, B)`` with several concordant integers ``N_1, ..., N_k`` (a
``multi-N`` / ``K_n`` vertex in the partner graph), each ``N_i`` gives an
integer point on the concordant curve

    E: Y^2 = X(X + A^2)(X + B^2),   X = N_i^2,  Y = N_i * sqrt(N_i^2+A^2) * sqrt(N_i^2+B^2)

These points are denoted ``Q_{N_i}``.  When the Mordell-Weil rank ``r`` is
smaller than ``k`` (the ``rank deficit`` observed in wl059), the ``Q_{N_i}``
cannot be independent: there exist integer vectors ``lambda`` with

    sum_i lambda_i * Q_{N_i}  =  (a torsion point)   in E(Q).

This module computes, for each ``Q_{N_i}``, its integer coordinates in the
Mordell-Weil lattice (modulo torsion) via the Neron-Tate height pairing, then
extracts a basis of the integer relation lattice and **verifies every relation
exactly** with PARI point arithmetic (no reliance on the floating-point round).

The motivating question (wl058/wl059, OPEN_DIRECTIONS A.2 / E.3): do these
cycle relations follow a universal pattern that could give an algebraic
obstruction to 4-chain closure?  This module produces the data to answer that;
it does not by itself prove anything.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isqrt
from typing import Any

from rational_distance.concordant.analysis import (
    _ensure_pari,
    compute_rank,
    find_concordant_integers,
)


def _is_perfect_square(n: int) -> bool:
    if n < 0:
        return False
    s = isqrt(n)
    return s * s == n


@dataclass(frozen=True)
class CyclePointCoord:
    """Integer Mordell-Weil coordinates of one ``Q_N`` modulo torsion."""

    N: int
    x: int
    y: int
    coords: tuple[int, ...]
    """Integer combination of the free generators: Q_N = sum coords_i * G_i + T."""
    torsion_order: int
    """Order of the residual torsion point T = Q_N - sum coords_i * G_i (1 = identity)."""
    two_divisible: bool
    """True iff Q_N is exactly divisible by 2 in E(Q) (PARI ellisdivisible)."""
    verified: bool
    """True iff Q_N - sum coords_i*G_i was confirmed (exactly) to be torsion."""


@dataclass(frozen=True)
class CycleRelation:
    """One integer relation sum_i coeffs_i * Q_{N_i} = torsion point."""

    coeffs: tuple[int, ...]
    residual_torsion_order: int
    """Order of sum_i coeffs_i*Q_{N_i} in E(Q); 1 means it equals the identity O."""
    verified: bool
    """True iff the relation was confirmed exactly via PARI point arithmetic."""


@dataclass
class CycleRelationResult:
    A: int
    B: int
    concordant_n: list[int]
    rank: int | None
    rank_bounds: tuple[int, int] | None
    generators: list[tuple[int, int]]
    point_coords: list[CyclePointCoord] = field(default_factory=list)
    relations: list[CycleRelation] = field(default_factory=list)
    coord_matrix_rank: int | None = None
    skipped_reason: str | None = None

    @property
    def k(self) -> int:
        return len(self.concordant_n)

    @property
    def k_minus_rank(self) -> int | None:
        if self.rank is None:
            return None
        return self.k - self.rank

    @property
    def relation_count(self) -> int:
        return len(self.relations)

    @property
    def all_verified(self) -> bool:
        return all(p.verified for p in self.point_coords) and all(
            r.verified for r in self.relations
        )

    @property
    def all_two_divisible(self) -> bool:
        """True iff every concordant point lies in 2*E(Q) (descent-trivial)."""
        return len(self.point_coords) > 0 and all(p.two_divisible for p in self.point_coords)

    def summary(self) -> str:
        lines = [
            f"(A={self.A}, B={self.B}): k={self.k} rank={self.rank} "
            f"deficit={self.k_minus_rank} relations={self.relation_count}",
        ]
        if self.skipped_reason:
            lines.append(f"  skipped: {self.skipped_reason}")
            return "\n".join(lines)
        for p in self.point_coords:
            mark = "" if p.verified else " (UNVERIFIED)"
            t = "" if p.torsion_order == 1 else f" + T(ord {p.torsion_order})"
            lines.append(f"  Q_{p.N} = {list(p.coords)}*G{t}{mark}")
        for rel in self.relations:
            terms = " + ".join(
                f"{c}*Q_{N}" for c, N in zip(rel.coeffs, self.concordant_n, strict=True) if c
            )
            order = rel.residual_torsion_order
            tail = "O" if order == 1 else f"T(ord {order})"
            mark = "" if rel.verified else " (UNVERIFIED)"
            lines.append(f"  relation: {terms} = {tail}{mark}")
        return "\n".join(lines)


def concordant_point(A: int, B: int, N: int) -> tuple[int, int]:
    """Return the integer point (X, Y) = (N^2, N*r2*r3) on E for concordant N."""
    a2, b2 = A * A, B * B
    sq_a = N * N + a2
    sq_b = N * N + b2
    if not _is_perfect_square(sq_a) or not _is_perfect_square(sq_b):
        raise ValueError(f"N={N} is not concordant for (A={A}, B={B})")
    return N * N, N * isqrt(sq_a) * isqrt(sq_b)


def _solve_round(height_matrix: list[list[float]], pairings: list[float]) -> list[int] | None:
    """Solve H c = v for c (reals) then round to integers. Tiny dimension only."""
    r = len(pairings)
    if r == 0:
        return []
    # Build augmented system and Gaussian-eliminate (r is at most ~5).
    aug = [[*map(float, row), pairings[i]] for i, row in enumerate(height_matrix)]
    for col in range(r):
        pivot = max(range(col, r), key=lambda i: abs(aug[i][col]))
        if abs(aug[pivot][col]) < 1e-12:
            return None
        aug[col], aug[pivot] = aug[pivot], aug[col]
        piv = aug[col][col]
        for i in range(r):
            if i == col:
                continue
            factor = aug[i][col] / piv
            for j in range(col, r + 1):
                aug[i][j] -= factor * aug[col][j]
    coords = [aug[i][r] / aug[i][i] for i in range(r)]
    return [round(c) for c in coords]


def _torsion_order(pari: Any, E: Any, point: Any) -> int:
    try:
        return int(pari.ellorder(E, point))
    except Exception:
        return 0


def _is_two_divisible(pari: Any, E: Any, point: Any) -> bool:
    """True iff ``point`` is divisible by 2 in E(Q) (PARI ellisdivisible)."""
    try:
        return bool(int(pari.ellisdivisible(E, point, 2)))
    except Exception:
        return False


def _combine_free_part(pari: Any, E: Any, gens: Any, coords: list[int]) -> Any:
    """Compute sum_i coords_i * G_i in E(Q)."""
    acc = pari("[0]")  # point at infinity
    for i, c in enumerate(coords):
        if c == 0:
            continue
        acc = pari.elladd(E, acc, pari.ellmul(E, gens[i], c))
    return acc


def mw_coordinates(
    A: int,
    B: int,
    Ns: list[int],
    *,
    pari: Any = None,
    effort: int = 1,
) -> CycleRelationResult:
    """Express each Q_N as an integer combination of MW generators (mod torsion)."""
    if pari is None:
        pari = _ensure_pari()
    a2, b2 = A * A, B * B
    E = pari(f"ellinit([0, {a2 + b2}, 0, {a2 * b2}, 0])")
    rank, bounds, _sha2, gen_coords = compute_rank(A, B, pari, effort=effort)
    gens = [pari([gx, gy]) for gx, gy in gen_coords]
    r = len(gens)

    result = CycleRelationResult(
        A=A,
        B=B,
        concordant_n=list(Ns),
        rank=rank,
        rank_bounds=bounds,
        generators=gen_coords,
    )

    if r == 0:
        result.skipped_reason = "rank 0 / no generators returned"
        return result

    height_matrix = [
        [float(pari.ellheight(E, gens[i], gens[j])) for j in range(r)] for i in range(r)
    ]

    for N in Ns:
        x, y = concordant_point(A, B, N)
        Q = pari([x, y])
        pairings = [float(pari.ellheight(E, Q, gens[j])) for j in range(r)]
        coords = _solve_round(height_matrix, pairings)
        if coords is None:
            result.point_coords.append(
                CyclePointCoord(
                    N=N,
                    x=x,
                    y=y,
                    coords=(),
                    torsion_order=0,
                    two_divisible=_is_two_divisible(pari, E, Q),
                    verified=False,
                )
            )
            continue
        free = _combine_free_part(pari, E, gens, coords)
        residual = pari.ellsub(E, Q, free)
        order = _torsion_order(pari, E, residual)
        verified = order in (1, 2, 4)
        result.point_coords.append(
            CyclePointCoord(
                N=N,
                x=x,
                y=y,
                coords=tuple(coords),
                torsion_order=order,
                two_divisible=_is_two_divisible(pari, E, Q),
                verified=verified,
            )
        )
    return result


def _integer_left_nullspace(matrix: list[list[int]]) -> list[list[int]]:
    """Return an integer basis of {lambda : lambda^T M = 0} for integer matrix M (k x r)."""
    import sympy

    if not matrix:
        return []
    M = sympy.Matrix(matrix)  # k x r
    basis = M.T.nullspace()  # vectors x in Q^k with M^T x = 0  <=>  x^T M = 0
    out: list[list[int]] = []
    for vec in basis:
        denom = sympy.ilcm(*[term.q for term in vec]) if vec else 1
        ints = [int(term * denom) for term in vec]
        g = 0
        for v in ints:
            g = sympy.igcd(g, v)
        if g > 1:
            ints = [v // g for v in ints]
        # normalize sign: first nonzero entry positive
        for v in ints:
            if v != 0:
                if v < 0:
                    ints = [-v for v in ints]
                break
        out.append(ints)
    return out


def analyze_cycle_relations(
    A: int,
    B: int,
    Ns: list[int] | None = None,
    *,
    pari: Any = None,
    effort: int = 1,
    ec_bound: int = 100000,
) -> CycleRelationResult:
    """Full A.2 analysis: MW coordinates + verified integer relation lattice.

    If ``Ns`` is omitted, the concordant N are found via ``ellratpoints`` up to
    ``ec_bound`` (keep this small to avoid long runs).
    """
    if pari is None:
        pari = _ensure_pari()
    if Ns is None:
        _raw, Ns = find_concordant_integers(A, B, ec_bound, pari)
    Ns = sorted(set(Ns))

    result = mw_coordinates(A, B, Ns, pari=pari, effort=effort)
    if result.skipped_reason is not None:
        return result

    coord_matrix = [list(p.coords) for p in result.point_coords if p.verified and p.coords]
    verified_Ns = [p.N for p in result.point_coords if p.verified and p.coords]
    if not coord_matrix:
        result.coord_matrix_rank = 0
        return result

    import sympy

    result.coord_matrix_rank = sympy.Matrix(coord_matrix).rank()

    # Build relations over the full N list (coeff 0 for unverified/dropped points).
    index_of = {N: i for i, N in enumerate(result.concordant_n)}
    relations = _integer_left_nullspace(coord_matrix)
    a2, b2 = A * A, B * B
    E = pari(f"ellinit([0, {a2 + b2}, 0, {a2 * b2}, 0])")

    for rel in relations:
        full = [0] * len(result.concordant_n)
        for coeff, N in zip(rel, verified_Ns, strict=True):
            full[index_of[N]] = coeff
        # Exact verification: sum coeff_i * Q_{N_i} must be torsion.
        acc = pari("[0]")
        for coeff, N in zip(full, result.concordant_n, strict=True):
            if coeff == 0:
                continue
            x, y = concordant_point(A, B, N)
            acc = pari.elladd(E, acc, pari.ellmul(E, pari([x, y]), coeff))
        order = _torsion_order(pari, E, acc)
        result.relations.append(
            CycleRelation(
                coeffs=tuple(full),
                residual_torsion_order=order,
                verified=order in (1, 2, 4),
            )
        )
    return result
