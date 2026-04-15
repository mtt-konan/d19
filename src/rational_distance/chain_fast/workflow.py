"""Chain-fast orchestration helpers."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from multiprocessing import cpu_count

from rational_distance.search_chain import ChainResult, _symmetry_group

from .bucket_stats import BucketStatsCollector
from .kernel import NearMissRecord, ScanProfile, _numpy_scan_t1, _python_scan_t1

try:
    import numpy as np
except ImportError:  # pragma: no cover - exercised only when numpy is missing
    np = None  # type: ignore[assignment]

_PARALLEL_T1_CHUNK_SIZE = 16

_WORKER_TRIPLES: list[tuple[int, int, int]] = []
_WORKER_BACKEND: str = "python"
_WORKER_S_ARR = None
_WORKER_T_ARR = None
_WORKER_COLLECT_PROFILE = False
_WORKER_SAFE_PAIR_SIEVE_ENABLED = False
_WORKER_MOD_SIEVE_ENABLED = False
_WORKER_BUCKET_STATS_ENABLED = False


@dataclass(frozen=True)
class ChunkScanResult:
    start_t1: int
    end_t1: int
    solutions: list[ChainResult]
    near_misses: list[NearMissRecord]
    scan_profile: ScanProfile
    bucket_stats: BucketStatsCollector | None = None

    @property
    def last_t1_index(self) -> int:
        return self.end_t1 - 1


def _iter_t1_chunks(start_t1: int, stop_t1: int) -> list[tuple[int, int]]:
    return [
        (chunk_start, min(stop_t1, chunk_start + _PARALLEL_T1_CHUNK_SIZE))
        for chunk_start in range(start_t1, stop_t1, _PARALLEL_T1_CHUNK_SIZE)
    ]


def _solution_key(result: ChainResult) -> tuple[int, int, int, int]:
    return min(_symmetry_group(result.a, result.b, result.c, result.d))


def _scan_t1_range(
    start_t1: int,
    end_t1: int,
    triples: list[tuple[int, int, int]],
    backend_label: str,
    s_arr=None,
    t_arr=None,
    collect_profile: bool = False,
    safe_pair_sieve_enabled: bool = False,
    mod_sieve_enabled: bool = False,
    collect_bucket_stats: bool = False,
) -> ChunkScanResult:
    solutions: list[ChainResult] = []
    near_misses: list[NearMissRecord] = []
    scan_profile = ScanProfile()
    bucket_stats = BucketStatsCollector() if collect_bucket_stats else None

    if backend_label == "numpy" and s_arr is None and np is not None:
        s_arr = np.array([triple[0] for triple in triples], dtype=np.int64)
        t_arr = np.array([triple[1] for triple in triples], dtype=np.int64)

    for i in range(start_t1, end_t1):
        if backend_label == "numpy":
            chunk_solutions, chunk_near_misses, t1_profile, t1_bucket_stats = _numpy_scan_t1(
                i,
                triples,
                s_arr,
                t_arr,
                collect_profile=collect_profile,
                safe_pair_sieve_enabled=safe_pair_sieve_enabled,
                mod_sieve_enabled=mod_sieve_enabled,
                collect_bucket_stats=collect_bucket_stats,
            )
        else:
            chunk_solutions, chunk_near_misses, t1_profile, t1_bucket_stats = _python_scan_t1(
                i,
                triples,
                collect_profile=collect_profile,
                safe_pair_sieve_enabled=safe_pair_sieve_enabled,
                mod_sieve_enabled=mod_sieve_enabled,
                collect_bucket_stats=collect_bucket_stats,
            )
        solutions.extend(chunk_solutions)
        near_misses.extend(chunk_near_misses)
        if collect_profile:
            scan_profile.merge(t1_profile)
        if bucket_stats is not None:
            bucket_stats.merge(t1_bucket_stats)

    return ChunkScanResult(
        start_t1=start_t1,
        end_t1=end_t1,
        solutions=solutions,
        near_misses=near_misses,
        scan_profile=scan_profile,
        bucket_stats=bucket_stats,
    )


def _init_parallel_worker(
    triples: list[tuple[int, int, int]],
    backend_label: str,
    collect_profile: bool,
    safe_pair_sieve_enabled: bool,
    mod_sieve_enabled: bool,
    collect_bucket_stats: bool,
) -> None:
    global _WORKER_BACKEND, _WORKER_BUCKET_STATS_ENABLED, _WORKER_COLLECT_PROFILE
    global _WORKER_MOD_SIEVE_ENABLED, _WORKER_S_ARR, _WORKER_SAFE_PAIR_SIEVE_ENABLED
    global _WORKER_T_ARR, _WORKER_TRIPLES

    _WORKER_TRIPLES = triples
    _WORKER_BACKEND = backend_label
    _WORKER_COLLECT_PROFILE = collect_profile
    _WORKER_SAFE_PAIR_SIEVE_ENABLED = safe_pair_sieve_enabled
    _WORKER_MOD_SIEVE_ENABLED = mod_sieve_enabled
    _WORKER_BUCKET_STATS_ENABLED = collect_bucket_stats
    if backend_label == "numpy" and np is not None:
        _WORKER_S_ARR = np.array([triple[0] for triple in triples], dtype=np.int64)
        _WORKER_T_ARR = np.array([triple[1] for triple in triples], dtype=np.int64)
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
        _WORKER_SAFE_PAIR_SIEVE_ENABLED,
        _WORKER_MOD_SIEVE_ENABLED,
        _WORKER_BUCKET_STATS_ENABLED,
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


def map_chunks_in_parallel(
    chunks: list[tuple[int, int]],
    triples: list[tuple[int, int, int]],
    backend_label: str,
    collect_profile: bool,
    workers: int,
    safe_pair_sieve_enabled: bool,
    mod_sieve_enabled: bool,
    collect_bucket_stats: bool,
) -> Iterator[ChunkScanResult]:
    with ProcessPoolExecutor(
        max_workers=workers,
        initializer=_init_parallel_worker,
        initargs=(
            triples,
            backend_label,
            collect_profile,
            safe_pair_sieve_enabled,
            mod_sieve_enabled,
            collect_bucket_stats,
        ),
    ) as executor:
        yield from executor.map(_worker_process_chunk, chunks)
