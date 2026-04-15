"""Elliptic curve analysis for the concordant form problem.

Given integers A, B, the concordant form asks for integer N with:
    N^2 + A^2 = S^2   (perfect square)
    N^2 + B^2 = T^2   (perfect square)

Setting X = N^2, Y = N*S*T gives the Weierstrass model:
    E: Y^2 = X(X + A^2)(X + B^2)
       = X^3 + (A^2 + B^2)X^2 + A^2B^2X

Torsion subgroup is always Z/2Z x Z/4Z, with:
    2-torsion: (0,0), (-A^2,0), (-B^2,0)
    4-torsion: (AB, +/-AB(A+B)), (-AB, +/-AB(A-B))  [when A != B]

Rank > 0 implies concordant N values exist, but this is necessary, not
sufficient, for the chain constraint. Empirically, all (A,B) pairs from the
chain parameterisation have rank >= 1.

IMPORTANT: A rational point (X, Y) on E with X = N^2 (a perfect square)
does NOT guarantee N^2+A^2 and N^2+B^2 are individually squares. The curve
equation only ensures their product X(X+A^2)(X+B^2) is a square.
We must explicitly verify isqrt(N^2+A^2) and isqrt(N^2+B^2) after finding
X = N^2.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from math import gcd, isqrt

from rational_distance.concordant.profile import ConcordantProfile

logger = logging.getLogger(__name__)


@dataclass
class ConcordantResult:
    """Analysis result for a single (A, B) pair."""

    A: int
    B: int
    rank: int
    rank_bounds: tuple[int, int]
    generators: list[tuple[int, int]]
    concordant_n: list[int]
    chain_compatible: list[int]
    ec_bound: int
    raw_square_x: list[int] = field(default_factory=list)

    @property
    def has_concordant(self) -> bool:
        return len(self.concordant_n) > 0

    @property
    def has_chain_solution(self) -> bool:
        return len(self.chain_compatible) > 0

    def summary(self) -> str:
        lines = [
            f"(A={self.A}, B={self.B}): rank={self.rank} "
            f"[{self.rank_bounds[0]},{self.rank_bounds[1]}]",
        ]
        if self.generators:
            lines.append(f"  generators: {self.generators}")
        if self.raw_square_x:
            lines.append(f"  X=N^2 found: N={self.raw_square_x}")
        if self.concordant_n:
            lines.append(f"  concordant N: {self.concordant_n}")
        if self.chain_compatible:
            lines.append(f"  *** CHAIN COMPATIBLE: {self.chain_compatible} ***")
        return "\n".join(lines)


def _is_perfect_square(n: int) -> bool:
    """Check if a non-negative integer is a perfect square."""
    if n < 0:
        return False
    s = isqrt(n)
    return s * s == n


def _ensure_pari():
    """Import and return a PARI instance, allocating memory if needed."""
    try:
        import cypari2
    except ImportError as exc:
        raise ImportError(
            "cypari2 is required for EC analysis. Install with: uv pip install cypari2"
        ) from exc
    pari = cypari2.Pari()
    pari.allocatemem(64 * 1024 * 1024)
    return pari


def compute_rank(
    A: int,
    B: int,
    pari=None,
    *,
    profile: ConcordantProfile | None = None,
) -> tuple[int, tuple[int, int], list]:
    """Compute the rank of E: Y^2 = X(X+A^2)(X+B^2)."""
    started = time.perf_counter() if profile is not None else 0.0
    if pari is None:
        pari = _ensure_pari()

    if A == B:
        result = (-1, (-1, -1), [])
        if profile is not None:
            profile.time_rank_s += time.perf_counter() - started
        return result

    a2, b2 = A * A, B * B
    E = pari(f"ellinit([0, {a2 + b2}, 0, {a2 * b2}, 0])")
    result = pari.ellrank(E)

    lower = int(result[0])
    upper = int(result[1])
    rank = lower

    gens = []
    if len(result) > 3:
        gen_list = result[3]
        for i in range(len(gen_list)):
            pt = gen_list[i]
            gens.append((int(pt[0]), int(pt[1])))

    if profile is not None:
        profile.time_rank_s += time.perf_counter() - started

    return rank, (lower, upper), gens


def find_concordant_integers(
    A: int,
    B: int,
    ec_bound: int = 100000,
    pari=None,
    *,
    profile: ConcordantProfile | None = None,
) -> tuple[list[int], list[int]]:
    """Find concordant integers N using ellratpoints."""
    started = time.perf_counter() if profile is not None else 0.0
    if pari is None:
        pari = _ensure_pari()

    if A == B:
        raw_square_x: list[int] = []
        concordant_n: list[int] = []
        a2 = A * A
        limit = isqrt(ec_bound)
        for N in range(1, limit + 1):
            if _is_perfect_square(N * N + a2):
                raw_square_x.append(N)
                concordant_n.append(N)
        if profile is not None:
            profile.time_find_concordant_s += time.perf_counter() - started
        return raw_square_x, concordant_n

    a2, b2 = A * A, B * B
    E = pari(f"ellinit([0, {a2 + b2}, 0, {a2 * b2}, 0])")

    try:
        points = pari.ellratpoints(E, ec_bound)
    except Exception:
        logger.warning("ellratpoints failed for (A=%d, B=%d, bound=%d)", A, B, ec_bound)
        if profile is not None:
            profile.time_find_concordant_s += time.perf_counter() - started
        return [], []

    raw_square_x: list[int] = []
    concordant_n: list[int] = []

    for i in range(len(points)):
        pt = points[i]
        try:
            x_num = int(pari.numerator(pt[0]))
            x_den = int(pari.denominator(pt[0]))
        except Exception:
            try:
                x_num = int(pt[0])
                x_den = 1
            except (ValueError, TypeError):
                continue

        if x_num <= 0 or x_den <= 0:
            continue

        if not _is_perfect_square(x_num) or not _is_perfect_square(x_den):
            continue

        N_num = isqrt(x_num)
        N_den = isqrt(x_den)
        if N_den != 1 or N_num <= 0:
            continue

        N = N_num
        raw_square_x.append(N)

        if _is_perfect_square(N * N + a2) and _is_perfect_square(N * N + b2):
            concordant_n.append(N)

    raw = sorted(set(raw_square_x))
    concordant = sorted(set(concordant_n))
    if profile is not None:
        profile.time_find_concordant_s += time.perf_counter() - started
    return raw, concordant


def check_chain_compatibility(A: int, B: int, N: int) -> bool:
    """Check if concordant N satisfies the chain constraint."""
    b = A + B - N
    if b <= 0:
        return False

    return _is_perfect_square(B * B + b * b) and _is_perfect_square(b * b + A * A)


def analyze_pair(
    A: int,
    B: int,
    ec_bound: int = 100000,
    pari=None,
    *,
    normalize: bool = False,
    profile: ConcordantProfile | None = None,
) -> ConcordantResult:
    """Full EC analysis of a single (A, B) pair."""
    if pari is None:
        pari = _ensure_pari()

    if normalize:
        g = gcd(A, B)
        A, B = A // g, B // g
    if A > B:
        A, B = B, A

    rank, bounds, gens = compute_rank(A, B, pari, profile=profile)
    raw_square_x, concordant_n = find_concordant_integers(
        A,
        B,
        ec_bound,
        pari,
        profile=profile,
    )
    chain_started = time.perf_counter() if profile is not None else 0.0
    chain_compat = [N for N in concordant_n if check_chain_compatibility(A, B, N)]
    if profile is not None:
        profile.time_chain_compat_s += time.perf_counter() - chain_started
        profile.n_raw_square_x_total += len(raw_square_x)
        profile.n_concordant_n_total += len(concordant_n)

    return ConcordantResult(
        A=A,
        B=B,
        rank=rank,
        rank_bounds=bounds,
        generators=gens,
        concordant_n=concordant_n,
        chain_compatible=chain_compat,
        ec_bound=ec_bound,
        raw_square_x=raw_square_x,
    )


def enumerate_multiples(
    A: int, B: int, max_depth: int = 10, pari=None
) -> list[int]:
    """Search for concordant integers by enumerating multiples of generators."""
    if pari is None:
        pari = _ensure_pari()

    a2, b2 = A * A, B * B
    E = pari(f"ellinit([0, {a2 + b2}, 0, {a2 * b2}, 0])")
    rank_info = pari.ellrank(E)

    gens = []
    if len(rank_info) > 3:
        gen_list = rank_info[3]
        for i in range(len(gen_list)):
            gens.append(gen_list[i])

    if not gens:
        return []

    concordant: set[int] = set()
    checked_x: set[str] = set()

    def _check_point(P) -> None:
        try:
            if len(P) < 2:
                return
            x_val = P[0]
            x_str = str(x_val)
            if x_str in checked_x:
                return
            checked_x.add(x_str)

            x_num = int(pari.numerator(x_val))
            x_den = int(pari.denominator(x_val))
            if x_num <= 0 or x_den <= 0:
                return
            if not _is_perfect_square(x_num) or not _is_perfect_square(x_den):
                return
            N_num = isqrt(x_num)
            N_den = isqrt(x_den)
            if N_den != 1 or N_num <= 0:
                return
            N = N_num
            if _is_perfect_square(N * N + a2) and _is_perfect_square(N * N + b2):
                concordant.add(N)
        except Exception:
            pass

    points_to_check = []
    for G in gens:
        for n in range(1, max_depth + 1):
            try:
                nP = pari.ellmul(E, G, n)
                points_to_check.append(nP)
            except Exception:
                break

    if len(gens) >= 2:
        for i in range(len(gens)):
            for j in range(i + 1, len(gens)):
                try:
                    S = pari.elladd(E, gens[i], gens[j])
                    points_to_check.append(S)
                    for n in range(2, max_depth + 1):
                        nS = pari.ellmul(E, S, n)
                        points_to_check.append(nS)
                except Exception:
                    break

    for point in points_to_check:
        _check_point(point)

    return sorted(concordant)
