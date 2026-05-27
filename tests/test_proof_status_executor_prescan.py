from __future__ import annotations

import sys
from collections.abc import Callable, Iterable
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def test_process_pairs_parallel_materializes_prescan_before_executor(
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
            item_list = list(items)
            observed["items_is_list"] = isinstance(items, list)
            observed["pairs"] = item_list
            for item in item_list:
                result = fn(item)
                if on_result is not None:
                    on_result(result)
            return []

    db = tmp_path / "parallel-prescan.sqlite3"
    conn = schema.connect_db(db)
    schema.init_schema(conn)
    workflow.process_pair(conn, 1, 5)

    counts = workflow.process_pairs_parallel(
        conn,
        [(1, 5), (1, 3)],
        workers=2,
        commit_every=1,
        executor=FakeExecutor(),
    )

    assert observed["items_is_list"] is True
    assert observed["pairs"] == [(1, 3)]
    assert counts["no_solution"] == 1
