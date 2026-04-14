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

import time
from collections.abc import Callable, Iterator
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from math import ceil, gcd, isqrt, sqrt
from multiprocessing import cpu_count

from tqdm import tqdm

from .math_utils import primitive_pythagorean_triples
from .search_chain import ChainResult, _symmetry_group

try:
    import numpy as np

    _HAS_NUMPY = True
except ImportError:
    _HAS_NUMPY = False

# sq3/sq4 <= 5*H^4 must fit in int64 (< 2^63-1 ~ 9.22e18).
# 5*H^4 < 9.22e18  =>  H < ((9.22e18)/5)^0.25 ~ 36853.
_NUMPY_MAX_HYP = 36000  # conservative safe threshold
_PARALLEL_T1_CHUNK_SIZE = 16

NearMissRecord = tuple[int, int, int, int, bool, bool, int, int, int, int]

_WORKER_TRIPLES: list[tuple[int, int, int]] = []
_WORKER_BACKEND: str = "python"
_WORKER_S_ARR: np.ndarray | None = None
_WORKER_T_ARR: np.ndarray | None = None
_WORKER_COLLECT_PROFILE = False


@dataclass
class ScanProfile:
    n_pairs_total: int = 0
    n_pairs_after_basic_filters: int = 0
    n_c3_pass: int = 0
    n_c4_pass: int = 0
    n_solutions_before_dedup: int = 0
    n_near_miss: int = 0
    time_filter_s: float = 0.0
    time_c3_s: float = 0.0
    time_c4_s: float = 0.0

    def merge(self, other: ScanProfile) -> None:
        self.n_pairs_total += other.n_pairs_total
        self.n_pairs_after_basic_filters += other.n_pairs_after_basic_filters
        self.n_c3_pass += other.n_c3_pass
        self.n_c4_pass += other.n_c4_pass
        self.n_solutions_before_dedup += other.n_solutions_before_dedup
        self.n_near_miss += other.n_near_miss
        self.time_filter_s += other.time_filter_s
        self.time_c3_s += other.time_c3_s
        self.time_c4_s += other.time_c4_s


@dataclass
class ChainFastProfile:
    requested_backend: str
    backend: str
    workers: int
    profile_enabled: bool
    triples_source: str = "generated"
    n_triples: int = 0
    n_pairs_total: int = 0
    n_pairs_after_basic_filters: int = 0
    n_c3_pass: int = 0
    n_c4_pass: int = 0
    n_solutions_before_dedup: int = 0
    n_solutions_after_dedup: int = 0
    n_near_miss: int = 0
    near_miss_seen: int = 0
    near_miss_saved: int = 0
    near_miss_dropped: int = 0
    time_generate_triples_s: float = 0.0
    time_outer_loop_s: float = 0.0
    time_filter_s: float = 0.0
    time_c3_s: float = 0.0
    time_c4_s: float = 0.0
    time_dedup_s: float = 0.0
    time_db_write_s: float = 0.0
    db_bytes_after_run: int = 0

    def absorb_scan(self, scan: ScanProfile) -> None:
        self.n_pairs_total += scan.n_pairs_total
        self.n_pairs_after_basic_filters += scan.n_pairs_after_basic_filters
        self.n_c3_pass += scan.n_c3_pass
        self.n_c4_pass += scan.n_c4_pass
        self.n_solutions_before_dedup += scan.n_solutions_before_dedup
        self.n_near_miss += scan.n_near_miss
        self.time_filter_s += scan.time_filter_s
        self.time_c3_s += scan.time_c3_s
        self.time_c4_s += scan.time_c4_s

    def as_dict(self) -> dict:
        return {
            "requested_backend": self.requested_backend,
            "backend": self.backend,
            "workers": self.workers,
            "profile_enabled": self.profile_enabled,
            "triples_source": self.triples_source,
            "n_triples": self.n_triples,
            "n_pairs_total": self.n_pairs_total,
            "n_pairs_after_basic_filters": self.n_pairs_after_basic_filters,
            "n_c3_pass": self.n_c3_pass,
            "n_c4_pass": self.n_c4_pass,
            "n_solutions_before_dedup": self.n_solutions_before_dedup,
            "n_solutions_after_dedup": self.n_solutions_after_dedup,
            "n_near_miss": self.n_near_miss,
            "near_miss_seen": self.near_miss_seen,
            "near_miss_saved": self.near_miss_saved,
            "near_miss_dropped": self.near_miss_dropped,
            "time_generate_triples_s": round(self.time_generate_triples_s, 6),
            "time_outer_loop_s": round(self.time_outer_loop_s, 6),
            "time_filter_s": round(self.time_filter_s, 6),
            "time_c3_s": round(self.time_c3_s, 6),
            "time_c4_s": round(self.time_c4_s, 6),
            "time_dedup_s": round(self.time_dedup_s, 6),
            "time_db_write_s": round(self.time_db_write_s, 6),
            "db_bytes_after_run": self.db_bytes_after_run,
        }


@dataclass
class ChainFastExecution:
    results: list[ChainResult]
    profile: ChainFastProfile
    triples: list[tuple[int, int, int]]


@dataclass(frozen=True)
class ChunkScanResult:
    start_t1: int
    end_t1: int
    solutions: list[ChainResult]
    near_misses: list[NearMissRecord]
    scan_profile: ScanProfile

    @property
    def last_t1_index(self) -> int:
        return self.end_t1 - 1


def build_chain_fast_triples(max_hyp: int) -> list[tuple[int, int, int]]:
    max_m = ceil(sqrt(max_hyp)) + 1
    return [(a, b, c) for a, b, c in primitive_pythagorean_triples(max_m) if c <= max_hyp]


def resolve_backend_choice(max_hyp: int, backend: str) -> str:
    """Resolve the effective backend for one run."""
    if backend == "numpy":
        if not _HAS_NUMPY:
            raise RuntimeError("numpy is not installed; cannot use backend='numpy'")
        if max_hyp > _NUMPY_MAX_HYP:
            raise ValueError(
                f"max_hyp={max_hyp} exceeds the int64-safe threshold {_NUMPY_MAX_HYP} "
                "for the numpy backend.  Use backend='python' or lower max_hyp."
            )
        return "numpy"
    if backend == "python":
        return "python"
    if _HAS_NUMPY and max_hyp <= _NUMPY_MAX_HYP:
        return "numpy"
    if _HAS_NUMPY and max_hyp > _NUMPY_MAX_HYP:
        import warnings

        warnings.warn(
            f"max_hyp={max_hyp} exceeds numpy int64-safe threshold {_NUMPY_MAX_HYP}; "
            "falling back to pure-Python backend.",
            RuntimeWarning,
            stacklevel=2,
        )
    return "python"


def _iter_t1_chunks(start_t1: int, stop_t1: int) -> list[tuple[int, int]]:
    return [
        (chunk_start, min(stop_t1, chunk_start + _PARALLEL_T1_CHUNK_SIZE))
        for chunk_start in range(start_t1, stop_t1, _PARALLEL_T1_CHUNK_SIZE)
    ]


def _solution_key(result: ChainResult) -> tuple[int, int, int, int]:
    return min(_symmetry_group(result.a, result.b, result.c, result.d))


def _append_solution_if_valid(
    solutions: list[ChainResult],
    a: int,
    b: int,
    c: int,
    d: int,
    x1: int,
    x2: int,
    x3: int,
    x4: int,
) -> None:
    solutions.append(
        ChainResult(a=a, b=b, c=c, d=d, x1=x1, x2=x2, x3=x3, x4=x4, square_ok=True)
    )


def _numpy_scan_t1(
    i: int,
    triples: list[tuple[int, int, int]],
    s_arr: np.ndarray,
    t_arr: np.ndarray,
) -> tuple[list[ChainResult], list[NearMissRecord], ScanProfile]:
    """Vectorised inner T2 loop for one outer T1 iteration (numpy path)."""
    s1, t1, h1 = triples[i]
    solutions: list[ChainResult] = []
    near_misses: list[NearMissRecord] = []
    scan_profile = ScanProfile(n_pairs_total=len(triples))

    filter_started = time.perf_counter() if _WORKER_COLLECT_PROFILE else 0.0
    cg = np.gcd(np.int64(t1), s_arr)
    s2r = s_arr // cg
    t1r = np.int64(t1) // cg

    A = t1r * t_arr
    B = np.int64(s1) * s2r
    N = s2r * np.int64(s1 - t1) + A
    b_all = s2r * np.int64(t1)

    mask = N > 0
    mask &= A % 2 == B % 2  # P1
    even = A % 2 == 0
    mask &= ((even & (A % 4 == 0) & (B % 4 == 0)) | (~even & (b_all % 4 == 0) & (N % 4 == 0)))
    mask &= (b_all != B) & (B != A) & (B != N) & (b_all != A) & (b_all != N) & (A != N)
    scan_profile.n_pairs_after_basic_filters = int(np.count_nonzero(mask))
    if _WORKER_COLLECT_PROFILE:
        scan_profile.time_filter_s = time.perf_counter() - filter_started

    if not np.any(mask):
        return solutions, near_misses, scan_profile

    j_idx = np.where(mask)[0]
    A_m = A[mask]
    B_m = B[mask]
    N_m = N[mask]
    b_m = b_all[mask]

    c3_started = time.perf_counter() if _WORKER_COLLECT_PROFILE else 0.0
    sq3 = A_m * A_m + N_m * N_m
    h3f = np.round(np.sqrt(sq3.astype(np.float64))).astype(np.int64)
    c3e = h3f * h3f == sq3
    c3p1 = (h3f + 1) * (h3f + 1) == sq3
    c3m1 = (h3f - 1) * (h3f - 1) == sq3
    c3 = c3e | c3p1 | c3m1
    h3c = np.where(c3e, h3f, np.where(c3p1, h3f + 1, h3f - 1))
    scan_profile.n_c3_pass = int(np.count_nonzero(c3))
    if _WORKER_COLLECT_PROFILE:
        scan_profile.time_c3_s = time.perf_counter() - c3_started

    if not np.any(c3):
        return solutions, near_misses, scan_profile

    j_c3 = j_idx[c3]
    A3 = A_m[c3]
    B3 = B_m[c3]
    N3 = N_m[c3]
    b3 = b_m[c3]
    h3v = h3c[c3]
    sq3_c = sq3[c3]

    c4_started = time.perf_counter() if _WORKER_COLLECT_PROFILE else 0.0
    sq4 = N3 * N3 + B3 * B3
    h4f = np.round(np.sqrt(sq4.astype(np.float64))).astype(np.int64)
    c4e = h4f * h4f == sq4
    c4p1 = (h4f + 1) * (h4f + 1) == sq4
    c4m1 = (h4f - 1) * (h4f - 1) == sq4
    c4 = c4e | c4p1 | c4m1
    h4c = np.where(c4e, h4f, np.where(c4p1, h4f + 1, h4f - 1))
    scan_profile.n_c4_pass = int(np.count_nonzero(c4))

    nm_mask = ~c4
    if np.any(nm_mask):
        for ki in np.where(nm_mask)[0]:
            near_misses.append(
                (
                    int(B3[ki]),
                    int(b3[ki]),
                    int(A3[ki]),
                    int(N3[ki]),
                    True,
                    False,
                    int(sq3_c[ki]),
                    int(sq4[ki]),
                    int(h3v[ki]),
                    int(h4c[ki]),
                )
            )
    scan_profile.n_near_miss = len(near_misses)
    if _WORKER_COLLECT_PROFILE:
        scan_profile.time_c4_s = time.perf_counter() - c4_started

    if not np.any(c4):
        return solutions, near_misses, scan_profile

    j_c34 = j_c3[c4]
    A_hit = A3[c4]
    B_hit = B3[c4]
    N_hit = N3[c4]
    b_hit = b3[c4]

    for ki in range(len(A_hit)):
        a_v = int(B_hit[ki])
        b_v = int(b_hit[ki])
        c_v = int(A_hit[ki])
        d_v = int(N_hit[ki])

        sq3_e = c_v * c_v + d_v * d_v
        h3_e = isqrt(sq3_e)
        if h3_e * h3_e != sq3_e:
            continue
        sq4_e = d_v * d_v + a_v * a_v
        h4_e = isqrt(sq4_e)
        if h4_e * h4_e != sq4_e:
            continue

        j = int(j_c34[ki])
        s2j, _, h2j = triples[j]
        cgj = gcd(t1, s2j)
        x1 = (s2j // cgj) * h1
        x2 = (t1 // cgj) * h2j
        _append_solution_if_valid(solutions, a_v, b_v, c_v, d_v, x1, x2, h3_e, h4_e)

    scan_profile.n_solutions_before_dedup = len(solutions)
    return solutions, near_misses, scan_profile


def _python_scan_t1(
    i: int,
    triples: list[tuple[int, int, int]],
) -> tuple[list[ChainResult], list[NearMissRecord], ScanProfile]:
    solutions: list[ChainResult] = []
    near_misses: list[NearMissRecord] = []
    scan_profile = ScanProfile(n_pairs_total=len(triples))
    s1, t1, h1 = triples[i]
    n = len(triples)

    for j in range(n):
        s2, t2, h2 = triples[j]

        filter_started = time.perf_counter() if _WORKER_COLLECT_PROFILE else 0.0
        cg = gcd(t1, s2)
        s2r = s2 // cg
        t1r = t1 // cg

        A = t1r * t2
        B = s1 * s2r
        N = s2r * (s1 - t1) + A

        if N <= 0:
            if _WORKER_COLLECT_PROFILE:
                scan_profile.time_filter_s += time.perf_counter() - filter_started
            continue
        if A % 2 != B % 2:
            if _WORKER_COLLECT_PROFILE:
                scan_profile.time_filter_s += time.perf_counter() - filter_started
            continue
        if A % 2 == 0 and (A % 4 != 0 or B % 4 != 0):
            if _WORKER_COLLECT_PROFILE:
                scan_profile.time_filter_s += time.perf_counter() - filter_started
            continue

        b = s2r * t1
        a, c, d = B, A, N

        if A % 2 == 1 and (b % 4 != 0 or N % 4 != 0):
            if _WORKER_COLLECT_PROFILE:
                scan_profile.time_filter_s += time.perf_counter() - filter_started
            continue
        if len({a, b, c, d}) < 4:
            if _WORKER_COLLECT_PROFILE:
                scan_profile.time_filter_s += time.perf_counter() - filter_started
            continue
        scan_profile.n_pairs_after_basic_filters += 1
        if _WORKER_COLLECT_PROFILE:
            scan_profile.time_filter_s += time.perf_counter() - filter_started

        c3_started = time.perf_counter() if _WORKER_COLLECT_PROFILE else 0.0
        sq3 = A * A + N * N
        h3 = isqrt(sq3)
        if _WORKER_COLLECT_PROFILE:
            scan_profile.time_c3_s += time.perf_counter() - c3_started
        if h3 * h3 != sq3:
            continue
        scan_profile.n_c3_pass += 1

        c4_started = time.perf_counter() if _WORKER_COLLECT_PROFILE else 0.0
        sq4 = N * N + B * B
        h4 = isqrt(sq4)
        if _WORKER_COLLECT_PROFILE:
            scan_profile.time_c4_s += time.perf_counter() - c4_started
        if h4 * h4 != sq4:
            near_misses.append((a, b, c, d, True, False, sq3, sq4, h3, h4))
            continue
        scan_profile.n_c4_pass += 1

        x1 = s2r * h1
        x2 = t1r * h2
        _append_solution_if_valid(solutions, a, b, c, d, x1, x2, h3, h4)

    scan_profile.n_solutions_before_dedup = len(solutions)
    scan_profile.n_near_miss = len(near_misses)
    return solutions, near_misses, scan_profile


def _scan_t1_range(
    start_t1: int,
    end_t1: int,
    triples: list[tuple[int, int, int]],
    backend_label: str,
    s_arr: np.ndarray | None = None,
    t_arr: np.ndarray | None = None,
    collect_profile: bool = False,
) -> ChunkScanResult:
    solutions: list[ChainResult] = []
    near_misses: list[NearMissRecord] = []
    scan_profile = ScanProfile()

    for i in range(start_t1, end_t1):
        if backend_label == "numpy":
            chunk_solutions, chunk_near_misses, t1_profile = _numpy_scan_t1(
                i,
                triples,
                s_arr,
                t_arr,
            )  # type: ignore[arg-type]
        else:
            chunk_solutions, chunk_near_misses, t1_profile = _python_scan_t1(i, triples)
        solutions.extend(chunk_solutions)
        near_misses.extend(chunk_near_misses)
        if collect_profile:
            scan_profile.merge(t1_profile)

    return ChunkScanResult(
        start_t1=start_t1,
        end_t1=end_t1,
        solutions=solutions,
        near_misses=near_misses,
        scan_profile=scan_profile,
    )


def _init_parallel_worker(
    triples: list[tuple[int, int, int]],
    backend_label: str,
    collect_profile: bool,
) -> None:
    global _WORKER_BACKEND, _WORKER_COLLECT_PROFILE, _WORKER_S_ARR, _WORKER_T_ARR, _WORKER_TRIPLES

    _WORKER_TRIPLES = triples
    _WORKER_BACKEND = backend_label
    _WORKER_COLLECT_PROFILE = collect_profile
    if backend_label == "numpy":
        _WORKER_S_ARR = np.array([t[0] for t in triples], dtype=np.int64)
        _WORKER_T_ARR = np.array([t[1] for t in triples], dtype=np.int64)
    else:
        _WORKER_S_ARR = None
        _WORKER_T_ARR = None


def _worker_process_chunk(bounds: tuple[int, int]) -> ChunkScanResult:
    start_t1, end_t1 = bounds
    return _scan_t1_range(
        start_t1,
        end_t1,
        _WORKER_TRIPLES,
        _WORKER_BACKEND,
        _WORKER_S_ARR,
        _WORKER_T_ARR,
        _WORKER_COLLECT_PROFILE,
    )


def _merge_chunk(
    chunk: ChunkScanResult,
    results: list[ChainResult],
    seen: set[tuple[int, int, int, int]],
    near_miss_callback: Callable | None,
) -> None:
    if near_miss_callback is not None:
        for near_miss in chunk.near_misses:
            near_miss_callback(*near_miss)

    for result in chunk.solutions:
        key = _solution_key(result)
        if key in seen:
            continue
        seen.add(key)
        results.append(result)


def _resolve_worker_count(workers: int, remaining_t1: int) -> int:
    if remaining_t1 <= 0:
        return 1
    if workers <= 0:
        workers = cpu_count() or 1
    return max(1, min(workers, remaining_t1))


def run_chain_fast(
    max_hyp: int = 500,
    progress: bool = True,
    backend: str = "auto",
    workers: int = 1,
    start_t1: int = 0,
    near_miss_callback: Callable | None = None,
    chunk_complete_callback: Callable[[int], None] | None = None,
    triples: list[tuple[int, int, int]] | None = None,
    profile: bool = False,
    triples_source: str = "generated",
) -> ChainFastExecution:
    """Run chain-fast and return both results and execution profile.

    The returned profile always includes basic run metadata. Detailed per-stage
    timings and counts are only populated when ``profile=True``.
    """
    profile_data = ChainFastProfile(
        requested_backend=backend,
        backend=resolve_backend_choice(max_hyp, backend),
        workers=workers,
        profile_enabled=profile,
        triples_source=triples_source,
    )

    if triples is None:
        build_started = time.perf_counter()
        triples = build_chain_fast_triples(max_hyp)
        profile_data.time_generate_triples_s = time.perf_counter() - build_started
        profile_data.triples_source = "generated"

    n = len(triples)
    profile_data.n_triples = n
    if not profile:
        profile_data.n_pairs_total = max(0, n - max(start_t1, 0)) * n
    backend_label = profile_data.backend

    if start_t1 < 0:
        raise ValueError("start_t1 must be >= 0")
    if start_t1 >= n:
        profile_data.n_solutions_after_dedup = 0
        return ChainFastExecution(results=[], profile=profile_data, triples=triples)

    chunks = _iter_t1_chunks(start_t1, n)
    results: list[ChainResult] = []
    seen: set[tuple[int, int, int, int]] = set()
    resolved_workers = _resolve_worker_count(workers, n - start_t1)
    profile_data.workers = resolved_workers

    progress_bar = None
    if progress:
        progress_bar = tqdm(
            total=n - start_t1,
            desc=f"Fast chain (T1, {backend_label})",
            leave=False,
        )

    loop_started = time.perf_counter()
    try:
        if resolved_workers == 1:
            global _WORKER_COLLECT_PROFILE
            _WORKER_COLLECT_PROFILE = profile
            s_arr = None
            t_arr = None
            if backend_label == "numpy":
                s_arr = np.array([t[0] for t in triples], dtype=np.int64)
                t_arr = np.array([t[1] for t in triples], dtype=np.int64)

            for start_idx, end_idx in chunks:
                chunk = _scan_t1_range(
                    start_idx,
                    end_idx,
                    triples,
                    backend_label,
                    s_arr,
                    t_arr,
                    profile,
                )
                if profile:
                    profile_data.absorb_scan(chunk.scan_profile)
                dedup_started = time.perf_counter() if profile else 0.0
                _merge_chunk(chunk, results, seen, near_miss_callback)
                if profile:
                    profile_data.time_dedup_s += time.perf_counter() - dedup_started
                if chunk_complete_callback is not None:
                    chunk_complete_callback(chunk.last_t1_index)
                if progress_bar is not None:
                    progress_bar.update(end_idx - start_idx)
        else:
            with ProcessPoolExecutor(
                max_workers=resolved_workers,
                initializer=_init_parallel_worker,
                initargs=(triples, backend_label, profile),
            ) as executor:
                chunk_iter: Iterator[ChunkScanResult] = executor.map(_worker_process_chunk, chunks)
                for (start_idx, end_idx), chunk in zip(chunks, chunk_iter, strict=True):
                    if profile:
                        profile_data.absorb_scan(chunk.scan_profile)
                    dedup_started = time.perf_counter() if profile else 0.0
                    _merge_chunk(chunk, results, seen, near_miss_callback)
                    if profile:
                        profile_data.time_dedup_s += time.perf_counter() - dedup_started
                    if chunk_complete_callback is not None:
                        chunk_complete_callback(chunk.last_t1_index)
                    if progress_bar is not None:
                        progress_bar.update(end_idx - start_idx)
    finally:
        if progress_bar is not None:
            progress_bar.close()

    profile_data.time_outer_loop_s = time.perf_counter() - loop_started
    sorted_results = sorted(results, key=lambda r: (r.a, r.b, r.c, r.d))
    profile_data.n_solutions_after_dedup = len(sorted_results)
    profile_data.near_miss_seen = profile_data.n_near_miss
    return ChainFastExecution(results=sorted_results, profile=profile_data, triples=triples)


def find_chains_fast(
    max_hyp: int = 500,
    progress: bool = True,
    backend: str = "auto",
    workers: int = 1,
    start_t1: int = 0,
    near_miss_callback: Callable | None = None,
    chunk_complete_callback: Callable[[int], None] | None = None,
) -> list[ChainResult]:
    """Compatibility wrapper returning only the deduplicated result list."""
    return run_chain_fast(
        max_hyp=max_hyp,
        progress=progress,
        backend=backend,
        workers=workers,
        start_t1=start_t1,
        near_miss_callback=near_miss_callback,
        chunk_complete_callback=chunk_complete_callback,
    ).results
