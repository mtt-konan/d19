from __future__ import annotations

import sys
from collections.abc import Callable, Iterable
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def test_evaluate_core_chunk_returns_only_survivors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from rational_distance.proof_status import fast_core
    from rational_distance.proof_status import methods as proof_methods
    from rational_distance.proof_status.types import MethodResult

    def fake_safe(A: int, _B: int) -> MethodResult:
        if A == 1:
            return MethodResult("safe_sieve", "no_solution")
        return MethodResult("safe_sieve", "pass")

    def fake_chain(A: int, _B: int) -> MethodResult:
        if A == 2:
            return MethodResult("chain_closure_mod_sieve", "no_solution")
        return MethodResult("chain_closure_mod_sieve", "pass")

    def fake_factor(A: int, _B: int) -> MethodResult:
        if A == 3:
            return MethodResult("factor_concordant", "no_solution")
        return MethodResult(
            "factor_concordant",
            "inconclusive",
            details={"concordant_n_count": 1, "chain_compatible_count": 0},
        )

    monkeypatch.setattr(proof_methods, "run_safe_sieve", fake_safe)
    monkeypatch.setattr(proof_methods, "run_chain_closure_mod_sieve", fake_chain)
    monkeypatch.setattr(proof_methods, "run_factor_concordant", fake_factor)

    result = fast_core.evaluate_core_chunk(((1, 5), (2, 7), (3, 11), (4, 13)))

    assert result.checked == 4
    assert result.no_solution == 3
    assert result.survivors == ((4, 13),)


def test_merge_core_results_combines_counts_and_survivors() -> None:
    from rational_distance.proof_status.fast_core import CoreChunkResult, merge_core_results

    merged = merge_core_results(
        [
            CoreChunkResult(checked=2, no_solution=1, survivors=((1, 5),)),
            CoreChunkResult(checked=3, no_solution=2, survivors=((7, 45),)),
        ]
    )

    assert merged.checked == 5
    assert merged.no_solution == 3
    assert merged.survivors == ((1, 5), (7, 45))


def test_iter_chunks_splits_pairs() -> None:
    from rational_distance.proof_status.fast_core import iter_chunks

    assert list(iter_chunks([(1, 2), (3, 4), (5, 6)], 2)) == [
        ((1, 2), (3, 4)),
        ((5, 6),),
    ]


def test_run_fast_core_uses_parallel_map(monkeypatch: pytest.MonkeyPatch) -> None:
    from rational_distance.proof_status import fast_core
    from rational_distance.proof_status.fast_core import CoreChunkResult

    calls = []

    def fake_parallel_map(
        fn: Callable[[tuple[tuple[int, int], ...]], CoreChunkResult],
        items: Iterable[tuple[tuple[int, int], ...]],
        *,
        workers: int,
        chunksize: int,
        on_result: Callable[[CoreChunkResult], None] | None,
        ordered: bool,
        collect_results: bool,
    ) -> list[CoreChunkResult]:
        calls.append(
            {
                "workers": workers,
                "chunksize": chunksize,
                "ordered": ordered,
                "collect_results": collect_results,
            }
        )
        results = []
        for item in items:
            result = fn(item)
            results.append(result)
            if on_result is not None:
                on_result(result)
        return results

    monkeypatch.setattr(fast_core, "parallel_map", fake_parallel_map)
    def fake_evaluate_core_chunk(
        chunk: tuple[tuple[int, int], ...],
    ) -> CoreChunkResult:
        return CoreChunkResult(len(chunk), len(chunk), ())

    monkeypatch.setattr(fast_core, "evaluate_core_chunk", fake_evaluate_core_chunk)

    result = fast_core.run_fast_core(
        [(1, 5), (2, 7), (3, 11)],
        workers=2,
        pair_chunk_size=2,
        pool_chunksize=1,
    )

    assert result.checked == 3
    assert result.no_solution == 3
    assert result.survivors == ()
    assert calls == [
        {"workers": 2, "chunksize": 1, "ordered": False, "collect_results": True}
    ]
