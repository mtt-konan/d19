"""Search strategies for rational-distance points on the unit square.

Two complementary search modes
────────────────────────────────────────────────────────────────────────
parametric_search_fast  (recommended)
    Integer-arithmetic + multiprocessing.  Each primitive Pythagorean
    triple (p,q,r) is processed by a worker; no Fraction objects in the
    hot loop.  Speed gains over the naive Fraction approach:

      • Integer isqrt check instead of Fraction.rational_sqrt  → ~20×
      • ProcessPoolExecutor over CPU cores                     → ~N×
      • Pre-built coprime-pair list (no gcd in inner loop)     → ~2×

parametric_search  (fallback, generator)
    Original Fraction-based generator; kept for backward compatibility
    and small interactive searches.

brute_force_search
    Enumerate all rational (x,y) with denominator ≤ max_den.  Useful
    as an exhaustive ground-truth for small ranges.

────────────────────────────────────────────────────────────────────────
Integer distance formula (derivation):
  Point P = (ap/br, aq/br)  for coprime integers a,b and triple (p,q,r).
  d(A) = a/b  (always rational)
  d(B)² = ((ar−bp)² + (bq)²) / (br)²   → rational iff (ar−bp)²+(bq)² is □
  d(D)² = ((ar−bq)² + (bp)²) / (br)²   → rational iff (ar−bq)²+(bp)² is □
  d(C)² = ((ar−b(p+q))²+(b(p−q))²)/(br)² → rational iff numerator is □
  (Proof: expand d(B)²=(k−p/r)²+(kq/r)² with k=a/b, use p²+q²=r².)

Architecture guard:
  Parametric filtering, distance formulas, square checks, and exact fallback
  rules must stay in `parametric_core.py`. This module should only handle CPU
  orchestration and compatibility wrappers.
"""

from __future__ import annotations

import multiprocessing
from collections.abc import Generator, Iterator
from concurrent.futures import ProcessPoolExecutor, as_completed
from fractions import Fraction
from math import gcd

import numpy as np

from rational_distance import parametric_core as core
from rational_distance.math_utils import primitive_pythagorean_triples, rational_sqrt
from rational_distance.square import RationalPoint, make_point

# ── Worker state (set once per process by _init_worker) ──────────────────────

_WORKER_PAIRS: list[tuple[int, int]] = []
_WORKER_A: np.ndarray | None = None  # int64 array of a values
_WORKER_B: np.ndarray | None = None  # int64 array of b values
_WORKER_SAFE_R_MAX: int = 0  # max r for which int64 arithmetic is overflow-free


def _init_worker(max_k_num: int, max_k_den: int) -> None:
    """Pre-build the coprime (a,b) list and numpy arrays for this worker process."""
    global _WORKER_PAIRS, _WORKER_A, _WORKER_B, _WORKER_SAFE_R_MAX
    _WORKER_PAIRS, _WORKER_A, _WORKER_B = core.build_coprime_data(max_k_num, max_k_den)
    _WORKER_SAFE_R_MAX = core.safe_r_max(max_k_num, max_k_den)


def _worker(args: tuple) -> list[dict]:
    """Top-level worker function (must be module-level to be picklable).

    Uses the fast numpy int64 path for small r, and falls back to Python's
    arbitrary-precision integers for large r to avoid int64 overflow.
    """
    p, q, r, min_rational, inside_only = args
    if _WORKER_A is not None and r <= _WORKER_SAFE_R_MAX:
        return core.search_triple_vectorized(
            np, p, q, r, _WORKER_A, _WORKER_B, min_rational, inside_only
        )
    return core.search_triple_exact(p, q, r, _WORKER_PAIRS, min_rational, inside_only)


def _parametric_search_fast_run(
    max_m: int = 80,
    max_k_num: int = 500,
    max_k_den: int = 200,
    min_rational: int = 3,
    workers: int = 0,
    progress: bool = True,
    inside_only: bool = False,
) -> tuple[list[RationalPoint], core.ParametricRunStats]:
    """Run the fast CPU search and return both results and shared stats."""
    try:
        from tqdm import tqdm as _tqdm
    except ImportError:
        _tqdm = None

    n_workers = workers if workers > 0 else multiprocessing.cpu_count()
    triples = primitive_pythagorean_triples(max_m)
    args_list = [(p, q, r, min_rational, inside_only) for p, q, r in triples]
    stats = core.make_run_stats(triples, max_k_num, max_k_den)

    print(
        f"  triples={stats.total_triples}, "
        f"k-pairs per triple={stats.candidate_pairs:,}, workers={n_workers}"
    )
    if stats.exact_fallback_triples:
        pct = 100 * stats.exact_fallback_triples // max(stats.total_triples, 1)
        print(
            f"  Note: {stats.exact_fallback_triples}/{stats.total_triples} triples ({pct}%) "
            f"use the Python-int fallback (r > {stats.safe_r_max:,}) to avoid int64 overflow "
            f"— results are still exact."
        )

    all_raw: list[dict] = []
    if n_workers == 1:
        _init_worker(max_k_num, max_k_den)
        it: Iterator = iter(args_list)
        if progress and _tqdm:
            it = _tqdm(it, total=len(args_list), desc="Searching", unit="triple")
        for arg in it:
            all_raw.extend(_worker(arg))
    else:
        with ProcessPoolExecutor(
            max_workers=n_workers,
            initializer=_init_worker,
            initargs=(max_k_num, max_k_den),
        ) as executor:
            futs = {executor.submit(_worker, a): a for a in args_list}
            completed = as_completed(futs)
            if progress and _tqdm:
                completed = _tqdm(
                    completed,
                    total=len(args_list),
                    desc="Searching",
                    unit="triple",
                )
            for fut in completed:
                all_raw.extend(fut.result())

    return core.best_points_from_raw(all_raw), stats


# ── Public fast search ────────────────────────────────────────────────────────


def parametric_search_fast(
    max_m: int = 80,
    max_k_num: int = 500,
    max_k_den: int = 200,
    min_rational: int = 3,
    workers: int = 0,
    progress: bool = True,
    inside_only: bool = False,
) -> list[RationalPoint]:
    """Fast search using integer arithmetic and multiprocessing.

    Parameters
    ----------
    max_m       : max parameter m for Pythagorean triple generation
    max_k_num   : max numerator of scale factor k = a/b
    max_k_den   : max denominator of scale factor k
    min_rational: minimum rational distances required (3 or 4)
    workers     : number of worker processes; 0 = auto (cpu_count)
    progress    : show tqdm progress bar if available
    inside_only : if True, only return points strictly inside the unit square
                  (0 < x < 1 and 0 < y < 1); this is a strict mathematical
                  constraint (no theorems guarantee all solutions are inside)

    Returns a deduplicated list sorted by (-rational_count, x, y).
    """
    points, _ = _parametric_search_fast_run(
        max_m=max_m,
        max_k_num=max_k_num,
        max_k_den=max_k_den,
        min_rational=min_rational,
        workers=workers,
        progress=progress,
        inside_only=inside_only,
    )
    return points


# ── Original generator (kept for backward compatibility) ─────────────────────


def _rational_k_values(max_num: int, max_den: int) -> Iterator[Fraction]:
    for den in range(1, max_den + 1):
        for num in range(1, max_num + 1):
            if gcd(num, den) == 1:
                yield Fraction(num, den)


def parametric_search(
    max_m: int = 80,
    max_k_num: int = 300,
    max_k_den: int = 150,
    min_rational: int = 3,
) -> Generator[RationalPoint, None, None]:
    """Fraction-based generator search (slower, kept for compatibility)."""
    triples = primitive_pythagorean_triples(max_m)
    seen: set[tuple[Fraction, Fraction]] = set()

    for p, q, r in triples:
        pr = Fraction(p, r)
        qr = Fraction(q, r)
        pqr = Fraction(p + q, r)

        for k in _rational_k_values(max_k_num, max_k_den):
            k2 = k * k
            dB = rational_sqrt(k2 - 2 * k * pr + 1)
            dD = rational_sqrt(k2 - 2 * k * qr + 1)
            dC = rational_sqrt(k2 - 2 * k * pqr + 2)

            if 1 + (dB is not None) + (dD is not None) + (dC is not None) < min_rational:
                continue

            x, y = k * pr, k * qr
            key = (x, y)
            if key in seen:
                continue
            seen.add(key)
            yield RationalPoint(x=x, y=y, distances=(k, dB, dC, dD))


# ── Brute-force exhaustive search ────────────────────────────────────────────


def brute_force_search(
    max_den: int = 30,
    x_range: tuple[int, int] = (-1, 2),
    y_range: tuple[int, int] = (-1, 2),
    min_rational: int = 3,
) -> Generator[RationalPoint, None, None]:
    """Enumerate all reduced (x,y) with denominator ≤ max_den."""
    _SIDES = {Fraction(0), Fraction(1)}
    seen: set[tuple[Fraction, Fraction]] = set()
    for den in range(1, max_den + 1):
        for nx in range(x_range[0] * den, x_range[1] * den + 1):
            if nx != 0 and gcd(abs(nx), den) != 1:
                continue
            x = Fraction(nx, den)
            # Theorem: no rational-distance solution lies on extended sides
            if x in _SIDES:
                continue
            for ny in range(y_range[0] * den, y_range[1] * den + 1):
                if ny != 0 and gcd(abs(ny), den) != 1:
                    continue
                y = Fraction(ny, den)
                if y in _SIDES:
                    continue
                key = (x, y)
                if key in seen:
                    continue
                seen.add(key)
                pt = make_point(x, y)
                if pt.rational_count >= min_rational:
                    yield pt


def merge_results(
    *iterables: Iterator[RationalPoint],
) -> Generator[RationalPoint, None, None]:
    best: dict[tuple[Fraction, Fraction], RationalPoint] = {}
    for it in iterables:
        for pt in it:
            key = (pt.x, pt.y)
            if key not in best or pt.rational_count > best[key].rational_count:
                best[key] = pt
    yield from sorted(best.values(), key=lambda p: (-p.rational_count, p.denominator, p.x, p.y))


# ── Symmetry deduplication ────────────────────────────────────────────────────


def dedup_by_symmetry(points: list[RationalPoint]) -> list[RationalPoint]:
    """Reduce a list of points to one representative per D4 symmetry orbit.

    The unit square's D4 symmetry group has 8 elements (rotations + reflections).
    Symmetric points share the same set of rational distances (just permuted),
    so they are mathematically equivalent solutions.

    For each orbit the representative kept is the one with the most rational
    distances; ties are broken by smallest denominator, then lexicographic (x,y).
    """
    from rational_distance.square import canonical_xy

    best: dict[tuple[Fraction, Fraction], RationalPoint] = {}
    for pt in points:
        key = canonical_xy(pt.x, pt.y)
        prev = best.get(key)
        if (
            prev is None
            or pt.rational_count > prev.rational_count
            or (pt.rational_count == prev.rational_count and pt.denominator < prev.denominator)
        ):
            best[key] = pt

    return sorted(best.values(), key=lambda p: (-p.rational_count, p.denominator, p.x, p.y))
