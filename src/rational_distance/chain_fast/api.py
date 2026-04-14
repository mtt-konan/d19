"""Public chain-fast API and stable return types."""

from __future__ import annotations

import time
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from math import ceil, sqrt
from typing import TYPE_CHECKING

from tqdm import tqdm

from rational_distance.math_utils import primitive_pythagorean_triples
from rational_distance.search_chain import ChainResult

from .workflow import (
    _iter_t1_chunks,
    _merge_chunk,
    _resolve_worker_count,
    _scan_t1_range,
    map_chunks_in_parallel,
)

if TYPE_CHECKING:
    from .kernel import ScanProfile

try:
    import numpy as np

    _HAS_NUMPY = True
except ImportError:  # pragma: no cover - exercised only when numpy is missing
    np = None  # type: ignore[assignment]
    _HAS_NUMPY = False

# sq3/sq4 <= 5*H^4 must fit in int64 (< 2^63-1 ~ 9.22e18).
# 5*H^4 < 9.22e18  =>  H < ((9.22e18)/5)^0.25 ~ 36853.
_NUMPY_MAX_HYP = 36000  # conservative safe threshold


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
    """Run chain-fast and return both results and execution profile."""
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
            s_arr = None
            t_arr = None
            if backend_label == "numpy" and np is not None:
                s_arr = np.array([triple[0] for triple in triples], dtype=np.int64)
                t_arr = np.array([triple[1] for triple in triples], dtype=np.int64)

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
            chunk_iter: Iterator = map_chunks_in_parallel(
                chunks,
                triples,
                backend_label,
                profile,
                resolved_workers,
            )
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
    sorted_results = sorted(results, key=lambda result: (result.a, result.b, result.c, result.d))
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
