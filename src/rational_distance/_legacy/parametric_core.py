"""Shared helpers for the parametric rational-distance search.

This module is the single source of truth for the parametric search logic.
CPU multiprocessing and GPU/APU acceleration only differ in how candidate
pairs are executed; the filtering, distance formulas, exact verification,
deduplication, and overflow rules all live here.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd, isqrt

import numpy as np

from rational_distance.backend import _xp_cast
from rational_distance._legacy.square import RationalPoint

# Largest integer X such that X^2 and (X+1)^2 both fit in int64 after the
# "sum of two squares" safety margin is applied.
_INT64_SAFE_HALF: int = (1 << 31) - 1


@dataclass(frozen=True)
class ParametricRunStats:
    """Execution statistics shared by CPU and accelerated parametric runs."""

    total_triples: int
    candidate_pairs: int
    safe_r_max: int
    exact_fallback_triples: int = 0

    @property
    def fallback_triggered(self) -> bool:
        return self.exact_fallback_triples > 0


def count_coprime_pairs(max_k_num: int, max_k_den: int) -> int:
    """Count reduced pairs (a, b) with 1<=a<=max_k_num and 1<=b<=max_k_den."""
    return sum(
        1 for b in range(1, max_k_den + 1) for a in range(1, max_k_num + 1) if gcd(a, b) == 1
    )


def build_coprime_data(
    max_k_num: int,
    max_k_den: int,
) -> tuple[list[tuple[int, int]], np.ndarray, np.ndarray]:
    """Build reduced (a, b) pairs along with matching int64 numpy arrays."""
    pairs = [
        (a, b) for b in range(1, max_k_den + 1) for a in range(1, max_k_num + 1) if gcd(a, b) == 1
    ]
    a_arr = np.array([a for a, _ in pairs], dtype=np.int64)
    b_arr = np.array([b for _, b in pairs], dtype=np.int64)
    return pairs, a_arr, b_arr


def safe_r_max(max_k_num: int, max_k_den: int) -> int:
    """Return the largest r that keeps all int64 parametric terms safe."""
    coeff = max_k_num + 2 * max_k_den
    if coeff <= 0:
        return 10**18
    return _INT64_SAFE_HALF // coeff


def make_run_stats(
    triples: list[tuple[int, int, int]],
    max_k_num: int,
    max_k_den: int,
) -> ParametricRunStats:
    """Compute the shared overflow/fallback statistics for one run."""
    safe_limit = safe_r_max(max_k_num, max_k_den)
    fallback_triples = sum(1 for _, _, r in triples if r > safe_limit)
    return ParametricRunStats(
        total_triples=len(triples),
        candidate_pairs=count_coprime_pairs(max_k_num, max_k_den),
        safe_r_max=safe_limit,
        exact_fallback_triples=fallback_triples,
    )


def candidate_mask(a_arr, b_arr, p: int, q: int, r: int, inside_only: bool = False):
    """Return the shared candidate filter mask for array backends."""
    mask = ~((a_arr * p == b_arr * r) | (a_arr * q == b_arr * r))
    if inside_only:
        mask = mask & (a_arr * p < b_arr * r) & (a_arr * q < b_arr * r)
    return mask


def filter_candidate_arrays(a_arr, b_arr, p: int, q: int, r: int, inside_only: bool = False):
    """Filter array-backed candidate pairs using the shared mask."""
    mask = candidate_mask(a_arr, b_arr, p, q, r, inside_only)
    if bool(np.all(mask)) if isinstance(mask, np.ndarray) else False:
        return a_arr, b_arr
    return a_arr[mask], b_arr[mask]


def pair_allowed(a: int, b: int, p: int, q: int, r: int, inside_only: bool = False) -> bool:
    """Return True iff the exact pair passes side and optional inside filters."""
    if a * p == b * r or a * q == b * r:
        return False
    return not (inside_only and (a * p >= b * r or a * q >= b * r))


def compute_terms(a_arr, b_arr, p: int, q: int, r: int):
    """Compute the shared squared-distance numerators for array backends."""
    ar = a_arr * r
    bp = b_arr * p
    bq = b_arr * q
    br = b_arr * r
    tB = (ar - bp) ** 2 + bq**2
    tD = (ar - bq) ** 2 + bp**2
    tC = (ar - b_arr * (p + q)) ** 2 + (b_arr * (p - q)) ** 2
    return br, tB, tC, tD


def approx_square_mask(xp, t):
    """Approximate perfect-square mask with the shared s+1 correction."""
    s = _xp_cast(xp.floor(xp.sqrt(_xp_cast(t, xp.float64))), xp.int64)
    ok = s * s == t
    s1 = s + 1
    fix = ~ok & (s1 * s1 == t)
    if xp.any(fix):
        ok = ok | fix
        s[fix] = s1[fix]
    return ok, s


def reduce_fraction(num: int, den: int) -> tuple[int, int]:
    """Return num/den in lowest terms."""
    g = gcd(num, den)
    return num // g, den // g


def exact_square_root(n: int) -> int | None:
    """Return the exact integer square root when n is a perfect square."""
    root = isqrt(n)
    if root * root == n:
        return root
    return None


def _pair_exact_details(
    a: int,
    b: int,
    p: int,
    q: int,
    r: int,
) -> tuple[int, int, int, int, int | None, int | None, int | None]:
    br = b * r
    tB = (a * r - b * p) ** 2 + (b * q) ** 2
    tD = (a * r - b * q) ** 2 + (b * p) ** 2
    tC = (a * r - b * (p + q)) ** 2 + (b * (p - q)) ** 2
    return (
        *reduce_fraction(a * p, br),
        *reduce_fraction(a * q, br),
        exact_square_root(tB),
        exact_square_root(tC),
        exact_square_root(tD),
    )


def evaluate_pair_exact(
    a: int,
    b: int,
    p: int,
    q: int,
    r: int,
    min_rational: int,
    inside_only: bool = False,
) -> dict | None:
    """Evaluate one candidate pair exactly using Python integers."""
    if not pair_allowed(a, b, p, q, r, inside_only):
        return None

    xn, xd, yn, yd, sB, sC, sD = _pair_exact_details(a, b, p, q, r)
    rational_count = 1 + (sB is not None) + (sC is not None) + (sD is not None)
    if rational_count < min_rational:
        return None

    br = b * r
    return {
        "x": (xn, xd),
        "y": (yn, yd),
        "dA": (a, b),
        "dB": (sB, br) if sB is not None else None,
        "dC": (sC, br) if sC is not None else None,
        "dD": (sD, br) if sD is not None else None,
    }


def _to_cpu(arr, idx):
    sliced = arr[idx]
    if hasattr(sliced, "get"):
        return sliced.get()
    if hasattr(sliced, "cpu"):
        return sliced.cpu().numpy()
    return np.asarray(sliced)


def search_triple_vectorized(
    xp,
    p: int,
    q: int,
    r: int,
    a_arr,
    b_arr,
    min_rational: int,
    inside_only: bool = False,
) -> list[dict]:
    """Shared vectorized search for one triple with exact verification on hits."""
    a, b = filter_candidate_arrays(a_arr, b_arr, p, q, r, inside_only)
    if len(a) == 0:
        return []

    _, tB, tC, tD = compute_terms(a, b, p, q, r)
    okB, _ = approx_square_mask(xp, tB)
    okC, _ = approx_square_mask(xp, tC)
    okD, _ = approx_square_mask(xp, tD)

    rational_count = 1 + _xp_cast(okB, xp.int64) + _xp_cast(okC, xp.int64) + _xp_cast(okD, xp.int64)
    mask = rational_count >= min_rational
    if not xp.any(mask):
        return []

    idx = xp.where(mask)[0]
    a_hit = _to_cpu(a, idx)
    b_hit = _to_cpu(b, idx)

    results: list[dict] = []
    seen: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    for i in range(len(a_hit)):
        raw = evaluate_pair_exact(
            int(a_hit[i]),
            int(b_hit[i]),
            p,
            q,
            r,
            min_rational,
            inside_only,
        )
        if raw is None:
            continue
        key = (raw["x"], raw["y"])
        if key in seen:
            continue
        seen.add(key)
        results.append(raw)
    return results


def search_triple_exact(
    p: int,
    q: int,
    r: int,
    pairs: list[tuple[int, int]],
    min_rational: int,
    inside_only: bool = False,
) -> list[dict]:
    """Exact Python-int fallback for one triple."""
    results: list[dict] = []
    seen: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    for a, b in pairs:
        raw = evaluate_pair_exact(a, b, p, q, r, min_rational, inside_only)
        if raw is None:
            continue
        key = (raw["x"], raw["y"])
        if key in seen:
            continue
        seen.add(key)
        results.append(raw)
    return results


def raw_to_point(raw: dict) -> RationalPoint:
    """Convert one raw hit dict to a `RationalPoint`."""
    return RationalPoint(
        x=Fraction(*raw["x"]),
        y=Fraction(*raw["y"]),
        distances=(
            Fraction(*raw["dA"]),
            Fraction(*raw["dB"]) if raw["dB"] is not None else None,
            Fraction(*raw["dC"]) if raw["dC"] is not None else None,
            Fraction(*raw["dD"]) if raw["dD"] is not None else None,
        ),
    )


def sort_points(points: list[RationalPoint]) -> list[RationalPoint]:
    """Apply the shared stable sort order for parametric results."""
    return sorted(
        points,
        key=lambda pt: (-pt.rational_count, pt.denominator, pt.x, pt.y),
    )


def best_points_from_raw(raw_hits: list[dict]) -> list[RationalPoint]:
    """Deduplicate raw hits globally and return sorted `RationalPoint`s."""
    best: dict[tuple[Fraction, Fraction], RationalPoint] = {}
    for raw in raw_hits:
        pt = raw_to_point(raw)
        key = (pt.x, pt.y)
        if key not in best or pt.rational_count > best[key].rational_count:
            best[key] = pt
    return sort_points(list(best.values()))
