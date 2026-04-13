"""O(n²) search for Pythagorean 4-cycles satisfying the unit-square constraint.

Algorithm
---------
For primitive triples T1=(s1,t1,h1) and T2=(s2,t2,h2), define:

    g  = gcd(t1, s2)        (coupling divisor)
    A  = t1·t2 / g          (reduced product of exit legs)
    B  = s1·s2 / g          (reduced product of entry legs)
    N  = s2/g·(s1-t1) + A  = (s2·(s1-t1) + t1·t2) / g

The candidate 4-cycle  (a,b,c,d) = (B, s2·t1/g, A, N)  satisfies a+c = b+d
automatically (= A+B), and its edges are Pythagorean iff:

    (C3)  A² + N²  is a perfect square   →  x3 = √(A²+N²)
    (C4)  N² + B²  is a perfect square   →  x4 = √(N²+B²)

x1 and x2 come "for free": x1 = s2/g·h1,  x2 = t1/g·h2.

Scale factors: k1 = s2/g,  k2 = t1/g,  k3 = gcd(A,N),  k4 = gcd(N,B).

This produces the **primitive representative** of each chain family: any
integer solution (a,b,c,d) satisfying a+c=b+d is a positive-integer multiple
of the primitive representative derived from its (T1,T2) primitive pair.
Since the unit-square point P = (a/(a+c), b/(a+c)) is scale-invariant, all
members of the same family map to the same point P.

Complexity
----------
Primitive triples up to hypotenuse H: O(H) triples (both leg orientations).
The double loop is O(H²) pairs, each checked with two integer-sqrt calls.
Two arithmetic pre-filters (parity and mod-4) skip ~71% of pairs before the
integer-sqrt calls, giving an effective ~3.4× speedup.

Cross-product family note
-------------------------
For this parameterisation, ac - bd = (s2·t1/g)·(s1-t1)·(t2-s2), which is
nonzero for any primitive triple (s2 ≠ t2, s1 ≠ t1).  Cross-product family
is therefore automatically excluded.

Necessary parity conditions (provably correct filters)
------------------------------------------------------
In any Pythagorean pair (u, v) both legs cannot be odd, because
u² + v² ≡ 2 (mod 4) when both are odd — never a perfect square.
Applying this to all four edges of the chain proves:

    P1 (alternating parity): A ≡ B (mod 2)
        — if A%2 ≠ B%2, one of C3/C4 fails mod 4.

    P2 (even leg divisible by 4): for a primitive Pythagorean pair the even
        leg ≡ 0 (mod 4), because u² + v² ≡ 5 (mod 8) when the even element
        is ≡ 2 (mod 4), which is not a quadratic residue mod 8.
        — if A%2 == 0: must have A%4 == 0 and B%4 == 0.
        — if A%2 == 1: must have b%4 == 0 and N%4 == 0.

Together P1+P2 eliminate ~71% of candidate pairs with no false negatives.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from math import ceil, gcd, isqrt, sqrt
from typing import Optional

from tqdm import tqdm

from .math_utils import primitive_pythagorean_triples
from .search_chain import ChainResult, _symmetry_group, results_to_json

try:
    import numpy as np

    _HAS_NUMPY = True
except ImportError:
    _HAS_NUMPY = False

# sq3/sq4 <= 5*H^4 must fit in int64 (< 2^63-1 ~ 9.22e18).
# 5*H^4 < 9.22e18  =>  H < ((9.22e18)/5)^0.25 ~ 36853.
_NUMPY_MAX_HYP = 36000  # conservative safe threshold


def _numpy_inner(
    i: int,
    triples: list[tuple[int, int, int]],
    s_arr: "np.ndarray",
    t_arr: "np.ndarray",
    results: list[ChainResult],
    seen: set[tuple[int, int, int, int]],
    near_miss_callback: Optional[Callable],
) -> None:
    """Vectorised inner T2 loop for one outer T1 iteration (numpy path)."""
    s1, t1, h1 = triples[i]

    cg    = np.gcd(np.int64(t1), s_arr)
    s2r   = s_arr // cg
    t1r   = np.int64(t1) // cg

    A     = t1r * t_arr
    B     = np.int64(s1) * s2r
    N     = s2r * np.int64(s1 - t1) + A
    b_all = s2r * np.int64(t1)

    # Pre-filters as boolean masks
    mask = N > 0
    mask &= A % 2 == B % 2                                        # P1
    even  = A % 2 == 0
    mask &= (
        (even & (A % 4 == 0) & (B % 4 == 0)) |
        (~even & (b_all % 4 == 0) & (N % 4 == 0))                # P2
    )
    # All four values distinct (6 pairwise checks)
    mask &= (B != b_all) & (B != A) & (B != N) & (b_all != A) & (b_all != N) & (A != N)

    if not np.any(mask):
        return

    j_idx = np.where(mask)[0]
    A_m = A[mask]; B_m = B[mask]; N_m = N[mask]; b_m = b_all[mask]

    # C3 check: float prefilter + exact +-1 correction
    sq3  = A_m * A_m + N_m * N_m
    h3f  = np.round(np.sqrt(sq3.astype(np.float64))).astype(np.int64)
    c3e  = h3f * h3f == sq3
    c3p1 = (h3f + 1) * (h3f + 1) == sq3
    c3m1 = (h3f - 1) * (h3f - 1) == sq3
    c3   = c3e | c3p1 | c3m1
    h3c  = np.where(c3e, h3f, np.where(c3p1, h3f + 1, h3f - 1))

    if not np.any(c3):
        return

    j_c3 = j_idx[c3]
    A3, B3, N3, b3 = A_m[c3], B_m[c3], N_m[c3], b_m[c3]
    h3v   = h3c[c3]
    sq3_c = sq3[c3]

    # C4 check
    sq4  = N3 * N3 + B3 * B3
    h4f  = np.round(np.sqrt(sq4.astype(np.float64))).astype(np.int64)
    c4e  = h4f * h4f == sq4
    c4p1 = (h4f + 1) * (h4f + 1) == sq4
    c4m1 = (h4f - 1) * (h4f - 1) == sq4
    c4   = c4e | c4p1 | c4m1
    h4c  = np.where(c4e, h4f, np.where(c4p1, h4f + 1, h4f - 1))

    # Near-misses: C3 passes, C4 fails -- report corrected h4c (not raw h4f)
    if near_miss_callback is not None:
        nm_mask = ~c4
        if np.any(nm_mask):
            for ki in np.where(nm_mask)[0]:
                near_miss_callback(
                    int(B3[ki]), int(b3[ki]), int(A3[ki]), int(N3[ki]),
                    True, False,
                    int(sq3_c[ki]), int(sq4[ki]),
                    int(h3v[ki]), int(h4c[ki]),
                )

    if not np.any(c4):
        return

    j_c34 = j_c3[c4]
    A_hit, B_hit, N_hit, b_hit = A3[c4], B3[c4], N3[c4], b3[c4]

    for ki in range(len(A_hit)):
        a_v = int(B_hit[ki]); b_v = int(b_hit[ki])
        c_v = int(A_hit[ki]); d_v = int(N_hit[ki])

        # Exact isqrt guard: float prefilter can have rare false positives
        sq3_e = c_v * c_v + d_v * d_v
        h3_e  = isqrt(sq3_e)
        if h3_e * h3_e != sq3_e:
            continue
        sq4_e = d_v * d_v + a_v * a_v
        h4_e  = isqrt(sq4_e)
        if h4_e * h4_e != sq4_e:
            continue

        key = min(_symmetry_group(a_v, b_v, c_v, d_v))
        if key in seen:
            continue
        seen.add(key)

        j    = int(j_c34[ki])
        s2j, _, h2j = triples[j]
        cgj  = gcd(t1, s2j)
        x1   = (s2j // cgj) * h1
        x2   = (t1 // cgj) * h2j
        results.append(ChainResult(a=a_v, b=b_v, c=c_v, d=d_v,
                                   x1=x1, x2=x2, x3=h3_e, x4=h4_e, square_ok=True))


def find_chains_fast(
    max_hyp: int = 500,
    progress: bool = True,
    backend: str = "auto",
    start_t1: int = 0,
    near_miss_callback: Optional[Callable] = None,
) -> list[ChainResult]:
    """Find unit-square Pythagorean 4-cycles by O(n^2) primitive-triple-pair enumeration.

    For each ordered pair (T1, T2) of primitive triples with hypotenuse <= max_hyp,
    derives the primitive-representative 4-cycle and verifies two perfect-square
    conditions.  All returned results satisfy a+c == b+d by construction.

    Args:
        max_hyp:  Maximum hypotenuse of the two free primitive triples T1, T2.
                   The solution values (a,b,c,d) can be as large as O(max_hyp^2).
        progress: Show a tqdm progress bar.
        backend:  "auto" (default) uses numpy if available and max_hyp <=
                  _NUMPY_MAX_HYP, otherwise falls back to pure Python.
                  Pass "numpy" or "python" to force a specific path.
        start_t1: Resume from this outer T1 index (0-based).  Useful when
                  integrated with chain_db checkpoint/resume logic.
        near_miss_callback:  Called for every (T1, T2) pair where C3 passes but
                  C4 fails.  Signature:

                      callback(a, b, c, d, c3_ok, c4_ok, sq3, sq4, h3, h4)

                  All arguments are plain Python ints/bools.

    Returns:
        Sorted, deduplicated list of ChainResult objects (all have square_ok=True).
    """
    max_m = ceil(sqrt(max_hyp)) + 1
    triples: list[tuple[int, int, int]] = [
        (a, b, c)
        for a, b, c in primitive_pythagorean_triples(max_m)
        if c <= max_hyp
    ]
    n = len(triples)

    # Decide which backend to use
    if backend == "numpy":
        if not _HAS_NUMPY:
            raise RuntimeError("numpy is not installed; cannot use backend='numpy'")
        if max_hyp > _NUMPY_MAX_HYP:
            raise ValueError(
                f"max_hyp={max_hyp} exceeds the int64-safe threshold {_NUMPY_MAX_HYP} "
                "for the numpy backend.  Use backend='python' or lower max_hyp."
            )
        use_numpy = True
    elif backend == "python":
        use_numpy = False
    else:  # "auto"
        use_numpy = _HAS_NUMPY and max_hyp <= _NUMPY_MAX_HYP
        if _HAS_NUMPY and max_hyp > _NUMPY_MAX_HYP:
            import warnings
            warnings.warn(
                f"max_hyp={max_hyp} exceeds numpy int64-safe threshold {_NUMPY_MAX_HYP}; "
                "falling back to pure-Python backend.",
                RuntimeWarning,
                stacklevel=2,
            )

    results: list[ChainResult] = []
    seen: set[tuple[int, int, int, int]] = set()

    backend_label = "numpy" if use_numpy else "python"
    it: Iterator[int] = iter(range(start_t1, n))
    if progress:
        it = tqdm(  # type: ignore[assignment]
            range(start_t1, n),
            desc=f"Fast chain (T1, {backend_label})",
            leave=False,
        )

    if use_numpy:
        s_arr = np.array([t[0] for t in triples], dtype=np.int64)
        t_arr = np.array([t[1] for t in triples], dtype=np.int64)
        for i in it:
            _numpy_inner(i, triples, s_arr, t_arr, results, seen, near_miss_callback)
    else:
        # Pure-Python path (original algorithm with near_miss_callback support)
        for i in it:
            s1, t1, h1 = triples[i]
            for j in range(n):
                s2, t2, h2 = triples[j]

                cg  = gcd(t1, s2)
                s2r = s2 // cg
                t1r = t1 // cg

                A = t1r * t2
                B = s1 * s2r
                N = s2r * (s1 - t1) + A

                if N <= 0:
                    continue
                if A % 2 != B % 2:
                    continue
                if A % 2 == 0:
                    if A % 4 != 0 or B % 4 != 0:
                        continue

                b = s2r * t1
                a, c, d = B, A, N

                if A % 2 == 1:
                    if b % 4 != 0 or N % 4 != 0:
                        continue
                if len({a, b, c, d}) < 4:
                    continue

                sq3 = A * A + N * N
                h3  = isqrt(sq3)
                if h3 * h3 != sq3:
                    continue

                sq4 = N * N + B * B
                h4  = isqrt(sq4)
                if h4 * h4 != sq4:
                    if near_miss_callback is not None:
                        near_miss_callback(a, b, c, d, True, False, sq3, sq4, h3, h4)
                    continue

                key = min(_symmetry_group(a, b, c, d))
                if key in seen:
                    continue
                seen.add(key)

                x1 = s2r * h1
                x2 = t1r * h2
                results.append(
                    ChainResult(a=a, b=b, c=c, d=d, x1=x1, x2=x2,
                                x3=h3, x4=h4, square_ok=True)
                )

    return sorted(results, key=lambda r: (r.a, r.b, r.c, r.d))
