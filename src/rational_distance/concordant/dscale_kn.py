"""D-scaling K_n fast generator (wl085, OPEN_DIRECTIONS A.7).

Idea
----
Each multi-N pair (A, B) factors as (A, B) = d · (a₀, b₀) where (a₀, b₀)
is the "primitive底型" (gcd-reduced). The two elliptic curves

    E_{a₀, b₀}: y² = x(x + a₀²)(x + b₀²)
    E_{A, B}:   Y² = X(X + A²)(X + B²)

are ℚ-isomorphic via X = d²x, Y = d³y. So **rank(E_{A,B}) = rank(E_{a₀,b₀})**.
But integer concordant N depends on d:

    On primitive: rational n ∈ ℚ where x = n² is a square rational point
    On (A, B):    integer N = d · n  ⟺  n.denominator | d

So given a primitive (a₀, b₀) with rational n pool {n_1, ..., n_M}:

    K(d, primitive) = #{n_i : n_i.denominator | d}

Want K_t hub with t large → find d that's a multiple of many n_i denominators.

This is **much faster than scanning (a, b) ≤ max_hyp** because:
  1. Only need a small set of primitive (a₀, b₀) (few hundred for max_hyp=10000).
  2. For each primitive, PARI ellrank + multiples gives the rational n pool
     in seconds.
  3. Enumerating d is O(d_max).

Verified (wl085): reproduces wl063 K_10 hubs (554400, 926640), (369600, 617760),
(184800, 308880) from primitive (70, 117) at d = 7920 / 5280 / 2640 with all
10 N values matching exactly.

Limitations
-----------
The rational n pool from PARI is **not** complete; it's bounded by the
generator-multiple depth. Increasing max_depth gives more n, but never
enumerates E(ℚ) entirely. So:
  - Sound: every (d·a₀, d·b₀, {N_i}) we output IS a real concordant tuple.
  - Not complete: we may miss K_t hubs with t < pool size if the specific
    n combinations need denominators we haven't sampled.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from fractions import Fraction
from math import gcd, isqrt
from typing import Iterable

from rational_distance.concordant.analysis import _ensure_pari, _is_perfect_square

logger = logging.getLogger(__name__)


__all__ = [
    "RationalNPool",
    "KnCandidate",
    "is_rational_square",
    "enumerate_rational_n",
    "k_for_d",
    "scan_d_for_target_k",
]


def is_rational_square(num: int, den: int) -> tuple[bool, int, int]:
    """Test if num/den (assumed reduced, den > 0) is a perfect rational square.

    Returns (is_square, sqrt_num, sqrt_den). When is_square=True, the rational
    sqrt is sqrt_num / sqrt_den (in lowest terms iff num/den was)."""
    if num <= 0 or den <= 0:
        return False, 0, 0
    if not _is_perfect_square(num) or not _is_perfect_square(den):
        return False, 0, 0
    return True, isqrt(num), isqrt(den)


def _check_x_gives_n(pari, x_val, a2: int, b2: int) -> Fraction | None:
    """Given an EC point's x-coordinate, return the rational n if x = n²
    AND n²+a², n²+b² are both rational squares. Else None."""
    try:
        x_num = int(pari.numerator(x_val))
        x_den = int(pari.denominator(x_val))
    except Exception:
        return None
    is_sq, sn, sd = is_rational_square(x_num, x_den)
    if not is_sq:
        return None
    g = gcd(sn, sd)
    sn, sd = sn // g, sd // g
    n_sq_num, n_sq_den = sn * sn, sd * sd
    for c in (a2, b2):
        sq_ok, _, _ = is_rational_square(n_sq_num + c * n_sq_den, n_sq_den)
        if not sq_ok:
            return None
    return Fraction(sn, sd)


@dataclass
class RationalNPool:
    """The rational n pool for a primitive (a₀, b₀)."""

    a0: int
    b0: int
    rank_lower: int
    rank_upper: int
    n_generators: int
    rational_ns: list[Fraction] = field(default_factory=list)

    @property
    def n_count(self) -> int:
        return len(self.rational_ns)

    @property
    def denominators(self) -> list[int]:
        return sorted({n.denominator for n in self.rational_ns})


@dataclass
class KnCandidate:
    """A K_k candidate (a, b) generated from primitive × d scaling."""

    a: int
    b: int
    d: int
    primitive_a: int
    primitive_b: int
    k: int
    concordant_N: list[int]
    rank_lower: int
    rank_upper: int

    def to_dict(self) -> dict:
        return {
            "a": self.a,
            "b": self.b,
            "d": self.d,
            "primitive_a": self.primitive_a,
            "primitive_b": self.primitive_b,
            "k": self.k,
            "concordant_N": self.concordant_N,
            "rank_lower": self.rank_lower,
            "rank_upper": self.rank_upper,
        }


def enumerate_rational_n(
    a0: int,
    b0: int,
    *,
    max_depth: int = 30,
    ratpoints_bound: int = 100_000,
    rank_combo_bound: int = 5,
    pari=None,
) -> RationalNPool:
    """Enumerate rational n ∈ ℚ such that E_{a₀,b₀}(ℚ) contains a point with
    x = n² (and n²+a₀², n²+b₀² are both rational squares).

    Strategy:
      (a) ellrank gives generators G_1, ..., G_r.  Enumerate ±m·G_i for
          m ∈ [1, max_depth], and for r ≥ 2 also all linear combinations
          ∑ m_i G_i with |m_i| ≤ rank_combo_bound.
      (b) ellratpoints with naive height bound = ratpoints_bound to catch
          any low-height points missed by (a).

    Args:
      max_depth: per-generator multiple depth (positive AND negative).
      ratpoints_bound: ellratpoints naive height bound; 0 disables.
      rank_combo_bound: linear-combination box size for rank ≥ 2.
    """
    if pari is None:
        pari = _ensure_pari()

    a2, b2 = a0 * a0, b0 * b0
    E = pari(f"ellinit([0, {a2 + b2}, 0, {a2 * b2}, 0])")

    rank_info = pari.ellrank(E)
    rank_lower = int(rank_info[0]) if len(rank_info) > 0 else 0
    rank_upper = int(rank_info[1]) if len(rank_info) > 1 else 0
    gens = []
    if len(rank_info) > 3:
        gen_list = rank_info[3]
        for i in range(len(gen_list)):
            gens.append(gen_list[i])

    n_set: set[Fraction] = set()
    if not gens:
        return RationalNPool(a0, b0, rank_lower, rank_upper, 0, [])

    # Get torsion: E_{a,b} always has Z/2 × Z/4 (8 elements)
    # elltors(E) returns [order, [structure], [generators]]
    tors_points: list = []  # list of finite torsion points (not [0])
    try:
        tors_info = pari.elltors(E)
        if len(tors_info) >= 3:
            tors_gens = tors_info[2]
            # build all torsion combinations from the generators
            tors_structure = tors_info[1]
            orders = [int(tors_structure[i]) for i in range(len(tors_structure))]
            if len(tors_gens) == 1:
                T1 = tors_gens[0]
                for k1 in range(orders[0]):
                    if k1 == 0:
                        continue
                    tors_points.append(pari.ellmul(E, T1, k1))
            elif len(tors_gens) == 2:
                T1, T2 = tors_gens[0], tors_gens[1]
                for k1 in range(orders[0]):
                    for k2 in range(orders[1]):
                        if k1 == 0 and k2 == 0:
                            continue
                        P1 = pari.ellmul(E, T1, k1) if k1 > 0 else None
                        P2 = pari.ellmul(E, T2, k2) if k2 > 0 else None
                        if P1 is None:
                            tors_points.append(P2)
                        elif P2 is None:
                            tors_points.append(P1)
                        else:
                            tors_points.append(pari.elladd(E, P1, P2))
    except Exception:
        pass

    points = []

    def _add_with_torsion(P):
        """Append P and P + T for each torsion T."""
        points.append(P)
        for T in tors_points:
            try:
                points.append(pari.elladd(E, P, T))
            except Exception:
                pass

    # Strategy (a): per-generator multiples (positive & negative) + torsion
    for G in gens:
        P = G
        for _ in range(max_depth):
            _add_with_torsion(P)
            try:
                P = pari.elladd(E, P, G)
            except Exception:
                break
        try:
            nG = pari.ellneg(E, G)
            P = nG
            for _ in range(max_depth):
                _add_with_torsion(P)
                try:
                    P = pari.elladd(E, P, nG)
                except Exception:
                    break
        except Exception:
            pass

    # Strategy (a') for rank ≥ 2: all combinations ∑ m_i G_i + torsion
    if len(gens) >= 2:
        from itertools import product

        for ms in product(range(-rank_combo_bound, rank_combo_bound + 1), repeat=len(gens)):
            if all(m == 0 for m in ms):
                continue
            try:
                P = None
                for m, G in zip(ms, gens):
                    if m == 0:
                        continue
                    Q = pari.ellmul(E, G, m)
                    P = Q if P is None else pari.elladd(E, P, Q)
                if P is not None:
                    _add_with_torsion(P)
            except Exception:
                pass

    for P in points:
        try:
            x_val = P[0]
        except Exception:
            continue
        n = _check_x_gives_n(pari, x_val, a2, b2)
        if n is not None:
            n_set.add(n)

    # Strategy (b): ellratpoints fill-in
    if ratpoints_bound > 0:
        try:
            rp = pari.ellratpoints(E, ratpoints_bound)
            for i in range(len(rp)):
                try:
                    P = rp[i]
                    x_val = P[0]
                except Exception:
                    continue
                n = _check_x_gives_n(pari, x_val, a2, b2)
                if n is not None:
                    n_set.add(n)
        except Exception as exc:  # pragma: no cover
            logger.warning("ellratpoints failed for E_{%d,%d}: %s", a0, b0, exc)

    return RationalNPool(
        a0, b0, rank_lower, rank_upper, len(gens), sorted(n_set)
    )


def k_for_d(rational_ns: Iterable[Fraction], d: int) -> list[int]:
    """For scaling d, return all integer N = d · n where n.denominator | d."""
    out: set[int] = set()
    for n in rational_ns:
        if d % n.denominator == 0:
            N = (n.numerator * d) // n.denominator
            if N > 0:
                out.add(N)
    return sorted(out)


def scan_d_for_target_k(
    pool: RationalNPool,
    *,
    target_k: int,
    d_max: int = 100_000,
    d_min: int = 1,
) -> list[KnCandidate]:
    """Scan d ∈ [d_min, d_max] and return all K_k candidates with k ≥ target_k,
    sorted by d ascending (smaller d → smaller (a, b)).

    Each candidate has a = d · a₀, b = d · b₀ and concordant_N = sorted Ns.
    """
    candidates: list[KnCandidate] = []
    for d in range(d_min, d_max + 1):
        Ns = k_for_d(pool.rational_ns, d)
        if len(Ns) >= target_k:
            candidates.append(
                KnCandidate(
                    a=d * pool.a0,
                    b=d * pool.b0,
                    d=d,
                    primitive_a=pool.a0,
                    primitive_b=pool.b0,
                    k=len(Ns),
                    concordant_N=Ns,
                    rank_lower=pool.rank_lower,
                    rank_upper=pool.rank_upper,
                )
            )
    return candidates
