from __future__ import annotations

import sys
from collections.abc import Callable, Iterable
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def test_process_pairs_parallel_accepts_streaming_iterable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import rational_distance.parallel as parallel
    from rational_distance.proof_status import schema, workflow

    observed: dict[str, object] = {}

    def fake_parallel_map(
        fn: Callable[[tuple[int, int]], object],
        items: Iterable[tuple[int, int]],
        *,
        workers: int | None = None,
        chunksize: int = 50,
        on_result: Callable[[object], None] | None = None,
        ordered: bool = False,
        collect_results: bool = True,
    ) -> list[object]:
        observed["items_is_list"] = isinstance(items, list)
        for item in items:
            result = fn(item)
            if on_result is not None:
                on_result(result)
        return []

    monkeypatch.setattr(parallel, "parallel_map", fake_parallel_map)

    def pair_stream() -> Iterable[tuple[int, int]]:
        yield (1, 5)
        yield (1, 3)

    db = tmp_path / "parallel-stream.sqlite3"
    conn = schema.connect_db(db)
    schema.init_schema(conn)

    counts = workflow.process_pairs_parallel(
        conn,
        pair_stream(),
        workers=2,
        commit_every=1,
        skip_terminal=False,
    )

    assert observed["items_is_list"] is False
    assert counts["no_solution"] == 2


def test_process_pairs_parallel_skips_prescan_for_empty_db(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import rational_distance.parallel as parallel
    from rational_distance.proof_status import schema, workflow

    def fake_parallel_map(
        fn: Callable[[tuple[int, int]], object],
        items: Iterable[tuple[int, int]],
        *,
        workers: int | None = None,
        chunksize: int = 50,
        on_result: Callable[[object], None] | None = None,
        ordered: bool = False,
        collect_results: bool = True,
    ) -> list[object]:
        for item in items:
            result = fn(item)
            if on_result is not None:
                on_result(result)
        return []

    def fail_get_pair_status(_conn: object, _A: int, _B: int) -> object:
        raise AssertionError("fresh DB should not pre-scan pair statuses")

    monkeypatch.setattr(parallel, "parallel_map", fake_parallel_map)

    db = tmp_path / "parallel-fresh.sqlite3"
    conn = schema.connect_db(db)
    schema.init_schema(conn)
    monkeypatch.setattr(schema, "get_pair_status", fail_get_pair_status)

    counts = workflow.process_pairs_parallel(
        conn,
        [(1, 5), (1, 3)],
        workers=2,
        commit_every=1,
    )

    assert counts["no_solution"] == 2


def test_process_pairs_parallel_can_use_reusable_executor(
    tmp_path: Path,
) -> None:
    from rational_distance.proof_status import schema, workflow

    observed: dict[str, object] = {}

    class FakeExecutor:
        def map(
            self,
            fn: Callable[[tuple[int, int]], object],
            items: Iterable[tuple[int, int]],
            on_result: Callable[[object], None] | None = None,
            *,
            collect_results: bool = True,
        ) -> list[object]:
            observed["used_executor"] = True
            observed["collect_results"] = collect_results
            for item in items:
                result = fn(item)
                if on_result is not None:
                    on_result(result)
            return []

    db = tmp_path / "parallel-executor.sqlite3"
    conn = schema.connect_db(db)
    schema.init_schema(conn)

    counts = workflow.process_pairs_parallel(
        conn,
        [(1, 5), (1, 3)],
        workers=2,
        commit_every=1,
        executor=FakeExecutor(),
    )

    assert observed["used_executor"] is True
    assert observed["collect_results"] is False
    assert counts["no_solution"] == 2
