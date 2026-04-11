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
"""

from __future__ import annotations

import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from fractions import Fraction
from math import gcd, isqrt
from typing import Generator, Iterator, List, Optional

import numpy as np

from rational_distance.math_utils import primitive_pythagorean_triples, rational_sqrt
from rational_distance.square import RationalPoint, make_point


# ── Worker state (set once per process by _init_worker) ──────────────────────

_WORKER_PAIRS: list[tuple[int, int]] = []
_WORKER_A: "np.ndarray | None" = None  # int64 array of a values
_WORKER_B: "np.ndarray | None" = None  # int64 array of b values
_WORKER_SAFE_R_MAX: int = 0            # max r for which int64 arithmetic is overflow-free

# Largest integer X such that X^2 fits in int64 and (X+1)^2 also fits (for the s+1 check).
# Each squared term in tB/tD/tC must stay below INT64_MAX/2 so their sum fits too.
# isqrt(INT64_MAX // 2) = isqrt(4611686018427387903) = 2147483647 = 2^31 - 1.
_INT64_SAFE_HALF: int = (1 << 31) - 1  # 2 147 483 647


def _init_worker(max_k_num: int, max_k_den: int) -> None:
    """Pre-build the coprime (a,b) list and numpy arrays for this worker process."""
    global _WORKER_PAIRS, _WORKER_A, _WORKER_B, _WORKER_SAFE_R_MAX
    pairs = [
        (a, b)
        for b in range(1, max_k_den + 1)
        for a in range(1, max_k_num + 1)
        if gcd(a, b) == 1
    ]
    _WORKER_PAIRS = pairs
    _WORKER_A = np.array([a for a, b in pairs], dtype=np.int64)
    _WORKER_B = np.array([b for a, b in pairs], dtype=np.int64)

    # Determine the largest r for which all int64 squared terms stay safe.
    #
    # The tightest bound comes from tC = (ar − b(p+q))² + (b(p−q))².
    # Worst-case magnitude of (ar − b(p+q)) ≤ (max_a + 2·max_b)·r  (using p+q ≤ 2r).
    # We require each squared term < INT64_MAX/2 so the sum fits in int64.
    # Condition: (max_a + 2·max_b)·r ≤ _INT64_SAFE_HALF  →  r ≤ threshold.
    coeff = max_k_num + 2 * max_k_den
    _WORKER_SAFE_R_MAX = _INT64_SAFE_HALF // coeff if coeff > 0 else 10**18


def _worker(args: tuple) -> list[dict]:
    """Top-level worker function (must be module-level to be picklable).

    Uses the fast numpy int64 path for small r, and falls back to Python's
    arbitrary-precision integers for large r to avoid int64 overflow.
    """
    p, q, r, min_rational = args
    if _WORKER_A is not None and r <= _WORKER_SAFE_R_MAX:
        return _search_triple_numpy(p, q, r, _WORKER_A, _WORKER_B, min_rational)
    return _search_triple_int(p, q, r, _WORKER_PAIRS, min_rational)


# ── Numpy-vectorized search (primary path) ───────────────────────────────────

def _isqrt_vec(t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Vectorized integer square root check.

    Returns (ok, s) where ok[i] is True iff t[i] is a perfect square and
    s[i] = isqrt(t[i]).  Handles float64 rounding by also checking s+1.

    Safe for t values up to ~4×10^18 (int64 range, float64 sqrt precision
    sufficient for sqrt values up to ~10^7; larger values use the +1 fallback).
    """
    s = np.floor(np.sqrt(t.astype(np.float64))).astype(np.int64)
    ok = s * s == t
    # float64 sqrt may round down by 1 for large perfect squares; check s+1
    s1 = s + 1
    fix = ~ok & (s1 * s1 == t)
    ok |= fix
    s[fix] = s1[fix]
    return ok, s


def _search_triple_numpy(
    p: int,
    q: int,
    r: int,
    a_arr: np.ndarray,
    b_arr: np.ndarray,
    min_rational: int,
) -> list[dict]:
    """Numpy-vectorized search for one Pythagorean triple.

    Computes all (a,b) combinations simultaneously using array operations,
    then extracts hits with a Python loop (hits are rare, so this is fast).

    Points on extended sides (x=1 or y=1) are always excluded by theorem
    (proven via elliptic curves; x=0 and y=0 are impossible here).
    """
    # Theorem: no rational-distance solution to any vertex lies on x=0,1 or y=0,1.
    # x=a*p/(b*r), so x=1 iff a*p==b*r; y=1 iff a*q==b*r.
    # (x=0 and y=0 are impossible since all parameters are positive.)
    off_side = ~((a_arr * p == b_arr * r) | (a_arr * q == b_arr * r))
    if not off_side.all():
        a_arr = a_arr[off_side]
        b_arr = b_arr[off_side]
    if len(a_arr) == 0:
        return []

    ar = a_arr * r
    bp = b_arr * p
    bq = b_arr * q
    br = b_arr * r

    okB, sB = _isqrt_vec((ar - bp) ** 2 + bq ** 2)
    okD, sD = _isqrt_vec((ar - bq) ** 2 + bp ** 2)
    okC, sC = _isqrt_vec((ar - b_arr * (p + q)) ** 2 + (b_arr * (p - q)) ** 2)

    rational_count = 1 + okB + okD + okC  # bool arrays treated as 0/1
    mask = rational_count >= min_rational

    if not mask.any():
        return []

    results: list[dict] = []
    seen: set[tuple[int, int, int, int]] = set()

    for i in mask.nonzero()[0]:
        a_i, b_i, br_i = int(a_arr[i]), int(b_arr[i]), int(br[i])

        xn, xd = a_i * p, br_i
        g = gcd(xn, xd); xn //= g; xd //= g
        yn, yd = a_i * q, br_i
        g = gcd(yn, yd); yn //= g; yd //= g
        key = (xn, xd, yn, yd)
        if key in seen:
            continue
        seen.add(key)

        results.append({
            "x":  (a_i * p, br_i),
            "y":  (a_i * q, br_i),
            "dA": (a_i, b_i),
            "dB": (int(sB[i]), br_i) if okB[i] else None,
            "dC": (int(sC[i]), br_i) if okC[i] else None,
            "dD": (int(sD[i]), br_i) if okD[i] else None,
        })

    return results


# ── Core integer-arithmetic search (fallback) ────────────────────────────────

def _search_triple_int(
    p: int,
    q: int,
    r: int,
    pairs: list[tuple[int, int]],
    min_rational: int,
) -> list[dict]:
    """Search one Pythagorean triple (p,q,r) using only integer arithmetic.

    Returns a list of raw dicts with integer numerator/denominator pairs.
    Fraction conversion is deferred to the caller so the hot loop stays fast.
    """
    results: list[dict] = []
    seen: set[tuple[int, int, int, int]] = set()

    for a, b in pairs:
        # Theorem: no rational-distance solution lies on extended sides (x=1 or y=1)
        if a * p == b * r or a * q == b * r:
            continue
        ar = a * r
        bp = b * p
        bq = b * q
        br = b * r

        # ── d(B) ─────────────────────────────────────────────────────────
        uB = ar - bp
        tB = uB * uB + bq * bq
        sB = isqrt(tB)
        okB = sB * sB == tB

        # ── d(D) ─────────────────────────────────────────────────────────
        uD = ar - bq
        tD = uD * uD + bp * bp
        sD = isqrt(tD)
        okD = sD * sD == tD

        # ── d(C) ─────────────────────────────────────────────────────────
        uC = ar - b * (p + q)
        vC = b * (p - q)          # sign irrelevant (squared)
        tC = uC * uC + vC * vC
        sC = isqrt(tC)
        okC = sC * sC == tC

        if 1 + okB + okD + okC < min_rational:
            continue

        # Deduplicate by reduced (x, y) key
        xn, xd = a * p, br
        g = gcd(xn, xd); xn //= g; xd //= g
        yn, yd = a * q, br
        g = gcd(yn, yd); yn //= g; yd //= g
        key = (xn, xd, yn, yd)
        if key in seen:
            continue
        seen.add(key)

        results.append({
            "x":  (a * p, br),
            "y":  (a * q, br),
            "dA": (a, b),
            "dB": (sB, br) if okB else None,
            "dC": (sC, br) if okC else None,
            "dD": (sD, br) if okD else None,
        })

    return results


def _raw_to_point(raw: dict) -> RationalPoint:
    return RationalPoint(
        x=Fraction(*raw["x"]),
        y=Fraction(*raw["y"]),
        distances=(
            Fraction(*raw["dA"]),
            Fraction(*raw["dB"]) if raw["dB"] else None,
            Fraction(*raw["dC"]) if raw["dC"] else None,
            Fraction(*raw["dD"]) if raw["dD"] else None,
        ),
    )


# ── Public fast search ────────────────────────────────────────────────────────

def parametric_search_fast(
    max_m: int = 80,
    max_k_num: int = 500,
    max_k_den: int = 200,
    min_rational: int = 3,
    workers: int = 0,
    progress: bool = True,
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

    Returns a deduplicated list sorted by (-rational_count, x, y).
    """
    try:
        from tqdm import tqdm as _tqdm
    except ImportError:
        _tqdm = None

    n_workers = workers if workers > 0 else multiprocessing.cpu_count()
    triples   = primitive_pythagorean_triples(max_m)
    args_list = [(p, q, r, min_rational) for p, q, r in triples]

    # Report search volume
    n_pairs = sum(
        1 for b in range(1, max_k_den + 1)
        for a in range(1, max_k_num + 1)
        if gcd(a, b) == 1
    )
    print(f"  triples={len(triples)}, k-pairs per triple={n_pairs:,}, workers={n_workers}")

    # Warn if large-r triples will use the slower Python int fallback path.
    safe_r = _INT64_SAFE_HALF // (max_k_num + 2 * max_k_den)
    r_max_possible = max_m * max_m  # rough upper bound for r = m^2 + n^2
    if r_max_possible > safe_r:
        n_slow = sum(1 for _, _, r in triples if r > safe_r)
        pct = 100 * n_slow // max(len(triples), 1)
        print(
            f"  Note: {n_slow}/{len(triples)} triples ({pct}%) use the Python-int fallback "
            f"(r > {safe_r:,}) to avoid int64 overflow — results are still exact."
        )

    all_raw: list[dict] = []

    if n_workers == 1:
        # Single-process: simpler, good for debugging
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

    # Global deduplication across triples
    best: dict[tuple[Fraction, Fraction], RationalPoint] = {}
    for raw in all_raw:
        pt  = _raw_to_point(raw)
        key = (pt.x, pt.y)
        if key not in best or pt.rational_count > best[key].rational_count:
            best[key] = pt

    return sorted(best.values(), key=lambda p: (-p.rational_count, p.denominator, p.x, p.y))


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
        pr  = Fraction(p, r)
        qr  = Fraction(q, r)
        pqr = Fraction(p + q, r)

        for k in _rational_k_values(max_k_num, max_k_den):
            k2  = k * k
            dB  = rational_sqrt(k2 - 2 * k * pr  + 1)
            dD  = rational_sqrt(k2 - 2 * k * qr  + 1)
            dC  = rational_sqrt(k2 - 2 * k * pqr + 2)

            if 1 + (dB is not None) + (dD is not None) + (dC is not None) < min_rational:
                continue

            x, y = k * pr, k * qr
            key  = (x, y)
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
        if prev is None:
            best[key] = pt
        elif pt.rational_count > prev.rational_count:
            best[key] = pt
        elif pt.rational_count == prev.rational_count and pt.denominator < prev.denominator:
            best[key] = pt

    return sorted(best.values(), key=lambda p: (-p.rational_count, p.denominator, p.x, p.y))
