from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Sequence
from dataclasses import dataclass
from itertools import islice

from rational_distance.parallel import parallel_map
from rational_distance.proof_status import methods as proof_methods

Pair = tuple[int, int]


@dataclass(frozen=True)
class CoreChunkResult:
    checked: int
    no_solution: int
    survivors: tuple[Pair, ...]


def evaluate_core_pair(A: int, B: int) -> bool:
    safe = proof_methods.run_safe_sieve(A, B)
    if safe.outcome == "no_solution":
        return False

    chain = proof_methods.run_chain_closure_mod_sieve(A, B)
    if chain.outcome == "no_solution":
        return False

    factor = proof_methods.run_factor_concordant(A, B)
    if factor.outcome == "no_solution":
        return False

    return True


def evaluate_core_chunk(pairs: Sequence[Pair]) -> CoreChunkResult:
    survivors: list[Pair] = []
    no_solution = 0
    for A, B in pairs:
        if evaluate_core_pair(A, B):
            survivors.append((A, B))
        else:
            no_solution += 1
    return CoreChunkResult(
        checked=len(pairs),
        no_solution=no_solution,
        survivors=tuple(survivors),
    )


def merge_core_results(results: Iterable[CoreChunkResult]) -> CoreChunkResult:
    checked = 0
    no_solution = 0
    survivors: list[Pair] = []
    for result in results:
        checked += result.checked
        no_solution += result.no_solution
        survivors.extend(result.survivors)
    return CoreChunkResult(
        checked=checked,
        no_solution=no_solution,
        survivors=tuple(survivors),
    )


def iter_chunks(pairs: Iterable[Pair], chunk_size: int) -> Iterator[tuple[Pair, ...]]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    iterator = iter(pairs)
    while True:
        chunk = tuple(islice(iterator, chunk_size))
        if not chunk:
            return
        yield chunk


def run_fast_core(
    pairs: Iterable[Pair],
    *,
    workers: int,
    pair_chunk_size: int = 50_000,
    pool_chunksize: int = 1,
    on_chunk: Callable[[CoreChunkResult], None] | None = None,
) -> CoreChunkResult:
    results = parallel_map(
        evaluate_core_chunk,
        iter_chunks(pairs, pair_chunk_size),
        workers=workers,
        chunksize=pool_chunksize,
        on_result=on_chunk,
        ordered=False,
        collect_results=True,
    )
    return merge_core_results(results)
