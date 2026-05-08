"""Tests for the default chain SQLite cache."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def _cache_adjacency_to(conn, old_max: int, new_max: int) -> int:
    from rational_distance.chain_cache_db import insert_adjacency_rows
    from rational_distance.search_chain import _iter_pythagorean_pairs

    inserted = 0
    if new_max <= old_max:
        return inserted

    if old_max == 0:
        ranges = [(1, new_max, 1, new_max)]
    else:
        ranges = [
            (1, old_max, old_max + 1, new_max),
            (old_max + 1, new_max, 1, new_max),
        ]

    for start_a, stop_a, b_start, b_stop in ranges:
        rows = list(
            _iter_pythagorean_pairs(
                start_a,
                stop_a,
                b_start,
                b_stop,
                progress=False,
            )
        )
        inserted += insert_adjacency_rows(conn, rows)
    return inserted


class TestChainCacheDb:
    def test_adjacency_round_trip_incremental(self, tmp_path):
        from rational_distance.chain_cache_db import (
            connect_db,
            get_cache_state,
            init_schema,
            load_cached_adjacency_rows,
            update_cache_state,
        )
        from rational_distance.search_chain import _build_adjacency, build_adjacency_from_rows

        db_path = tmp_path / "chain-cache.db"
        conn = connect_db(db_path)
        init_schema(conn)

        _cache_adjacency_to(conn, 0, 40)
        update_cache_state(conn, adjacency_max_val=40)
        _cache_adjacency_to(conn, 40, 60)
        update_cache_state(conn, adjacency_max_val=60)

        assert get_cache_state(conn) == (60, 0)

        rows = load_cached_adjacency_rows(conn, 60)
        cached_adj, cached_hyp = build_adjacency_from_rows(60, iter(rows))
        fresh_adj, fresh_hyp = _build_adjacency(60, progress=False)

        assert cached_adj == fresh_adj
        assert cached_hyp == fresh_hyp
        conn.close()

    def test_cached_results_match_fresh_search_and_filters(self, tmp_path):
        from rational_distance.chain_cache_db import (
            RESULT_MODE_DEFAULT,
            RESULT_MODE_DIAGONAL_SIGN,
            connect_db,
            get_largest_cached_result,
            init_schema,
            insert_results,
            load_cached_adjacency_rows,
            load_cached_results,
            update_adjacency_max_val,
            update_result_state,
        )
        from rational_distance.search_chain import (
            build_adjacency_from_rows,
            find_chains,
            iter_chain_results,
        )

        db_path = tmp_path / "chain-results.db"
        conn = connect_db(db_path)
        init_schema(conn)

        _cache_adjacency_to(conn, 0, 400)
        update_adjacency_max_val(conn, 400)

        rows = load_cached_adjacency_rows(conn, 400)
        adj, hyp = build_adjacency_from_rows(400, iter(rows))

        default_results = iter_chain_results(
            adj,
            hyp,
            max_val=400,
            require_square=False,
            canonical=True,
            progress=False,
        )
        diagonal_results = iter_chain_results(
            adj,
            hyp,
            max_val=400,
            require_square=False,
            diagonal_sign_sieve=True,
            canonical=True,
            progress=False,
        )

        insert_results(conn, result_mode=RESULT_MODE_DEFAULT, results=default_results)
        insert_results(conn, result_mode=RESULT_MODE_DIAGONAL_SIGN, results=diagonal_results)

        default_square_count = sum(1 for result in default_results if result.square_ok)
        diagonal_square_count = sum(1 for result in diagonal_results if result.square_ok)

        update_result_state(
            conn,
            result_mode=RESULT_MODE_DEFAULT,
            results_max_val=400,
            result_count=len(default_results),
            square_result_count=default_square_count,
            pre_filter_count=len(default_results),
            pre_filter_square_count=default_square_count,
        )
        update_result_state(
            conn,
            result_mode=RESULT_MODE_DIAGONAL_SIGN,
            results_max_val=400,
            result_count=len(diagonal_results),
            square_result_count=diagonal_square_count,
            pre_filter_count=len(default_results),
            pre_filter_square_count=default_square_count,
        )

        fresh_default = find_chains(max_val=400, progress=False)
        cached_default = load_cached_results(conn, 400, result_mode=RESULT_MODE_DEFAULT)
        assert [(r.a, r.b, r.c, r.d) for r in cached_default] == [
            (r.a, r.b, r.c, r.d) for r in fresh_default
        ]

        fresh_diagonal = find_chains(max_val=400, diagonal_sign_sieve=True, progress=False)
        cached_diagonal = load_cached_results(conn, 400, result_mode=RESULT_MODE_DIAGONAL_SIGN)
        assert [(r.a, r.b, r.c, r.d) for r in cached_diagonal] == [
            (r.a, r.b, r.c, r.d) for r in fresh_diagonal
        ]

        fresh_diagonal_sq = find_chains(
            max_val=400,
            require_square=True,
            diagonal_sign_sieve=True,
            progress=False,
        )
        cached_diagonal_sq = load_cached_results(
            conn,
            400,
            result_mode=RESULT_MODE_DIAGONAL_SIGN,
            require_square=True,
        )
        assert [(r.a, r.b, r.c, r.d) for r in cached_diagonal_sq] == [
            (r.a, r.b, r.c, r.d) for r in fresh_diagonal_sq
        ]

        largest = get_largest_cached_result(conn, 400, result_mode=RESULT_MODE_DIAGONAL_SIGN)
        expected = max(
            fresh_diagonal,
            key=lambda result: (
                max(result.a, result.b, result.c, result.d),
                result.a + result.b + result.c + result.d,
                (result.a + result.c) * (result.b + result.d),
                result.a,
                result.b,
                result.c,
                result.d,
            ),
        )
        assert largest is not None
        assert (largest.a, largest.b, largest.c, largest.d) == (
            expected.a,
            expected.b,
            expected.c,
            expected.d,
        )
        conn.close()

    def test_run_resume_bookkeeping_isolated_by_result_mode(self, tmp_path):
        from rational_distance.chain_cache_db import (
            RESULT_MODE_DEFAULT,
            RESULT_MODE_DIAGONAL_SIGN,
            checkpoint_run,
            connect_db,
            finish_run,
            get_resumable_run,
            get_run,
            init_schema,
            start_run,
        )

        db_path = tmp_path / "chain-runs.db"
        conn = connect_db(db_path)
        init_schema(conn)

        default_run = start_run(
            conn,
            requested_max_val=80,
            result_mode=RESULT_MODE_DEFAULT,
            require_square=False,
            starting_adjacency_max_val=40,
            starting_results_max_val=40,
        )
        diagonal_run = start_run(
            conn,
            requested_max_val=80,
            result_mode=RESULT_MODE_DIAGONAL_SIGN,
            require_square=False,
            starting_adjacency_max_val=40,
            starting_results_max_val=40,
        )

        checkpoint_run(conn, default_run, 63, new_results=7, pre_filter_count=11)
        checkpoint_run(conn, diagonal_run, 58, new_results=3, pre_filter_count=9)

        default_row = get_resumable_run(
            conn,
            requested_max_val=80,
            result_mode=RESULT_MODE_DEFAULT,
        )
        diagonal_row = get_resumable_run(
            conn,
            requested_max_val=80,
            result_mode=RESULT_MODE_DIAGONAL_SIGN,
        )

        assert default_row is not None
        assert diagonal_row is not None
        assert int(default_row["id"]) == default_run
        assert int(diagonal_row["id"]) == diagonal_run
        assert int(default_row["last_completed_a"]) == 63
        assert int(diagonal_row["last_completed_a"]) == 58

        finish_run(
            conn,
            default_run,
            elapsed_s=1.23,
            new_adjacency_edges=10,
            new_results=7,
            pre_filter_count=11,
            pre_filter_square_count=0,
            diagonal_sign_filtered=4,
            build_adjacency_s=0.5,
            load_adjacency_s=0.1,
            search_cycles_s=0.6,
            query_results_s=0.03,
        )
        finished = get_run(conn, default_run)
        assert finished is not None
        assert finished["status"] == "completed"
        assert (
            get_resumable_run(
                conn,
                requested_max_val=80,
                result_mode=RESULT_MODE_DEFAULT,
            )
            is None
        )
        assert (
            get_resumable_run(
                conn,
                requested_max_val=80,
                result_mode=RESULT_MODE_DIAGONAL_SIGN,
            )
            is not None
        )
        conn.close()

    def test_schema_v1_db_is_rejected(self, tmp_path):
        from rational_distance.chain_cache_db import connect_db, init_schema

        db_path = tmp_path / "legacy-v1.sqlite3"
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE chain_cache_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
        conn.execute(
            "INSERT INTO chain_cache_meta (key, value) VALUES ('schema_version', '1')"
        )
        conn.commit()
        conn.close()

        conn = connect_db(db_path)
        try:
            try:
                init_schema(conn)
            except ValueError as exc:
                assert "expected 2" in str(exc)
            else:
                raise AssertionError("init_schema unexpectedly accepted schema v1")
        finally:
            conn.close()
