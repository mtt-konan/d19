"""CLI integration tests for the default chain cache."""

from __future__ import annotations

import subprocess
import sys
from contextlib import suppress
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


class _StopScan(Exception):
    pass


class TestChainCliCache:
    def test_chain_cli_help_shows_cache_flags(self):
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "search.py"),
                "chain",
                "--help",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        assert "--db" in proc.stdout
        assert "--resume" in proc.stdout
        assert "--diagonal-sign-sieve" in proc.stdout

    def test_chain_cli_diagonal_sign_sieve_reports_filtered_count(self):
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "search.py"),
                "chain",
                "--max-val",
                "500",
                "--diagonal-sign-sieve",
                "--no-progress",
                "--top",
                "0",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        assert "result_mode=diagonal_sign" in proc.stdout
        assert "Found 2 canonical 4-cycles" in proc.stdout
        assert "experimental diagonal_sign_sieve: kept 2/10, filtered 8" in proc.stdout

    def test_chain_cli_cache_reuse_by_result_mode(self, tmp_path):
        from rational_distance._legacy.chain_cache_db import (
            RESULT_MODE_DEFAULT,
            RESULT_MODE_DIAGONAL_SIGN,
            connect_db,
            get_cache_state,
            init_schema,
        )

        db_path = tmp_path / "chain-cache.sqlite3"
        default_cmd = [
            sys.executable,
            str(ROOT / "scripts" / "search.py"),
            "chain",
            "--max-val",
            "400",
            "--db",
            str(db_path),
            "--no-progress",
            "--top",
            "0",
        ]
        diagonal_cmd = [*default_cmd, "--diagonal-sign-sieve"]

        first = subprocess.run(default_cmd, cwd=ROOT, capture_output=True, text=True, check=True)
        assert (
            "cache high-water: result_mode=default  adjacency_max_val=400  results_max_val=400"
            in first.stdout
        )

        second = subprocess.run(
            diagonal_cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        assert (
            "cache high-water: result_mode=diagonal_sign  adjacency_max_val=400  "
            "results_max_val=400" in second.stdout
        )

        conn = connect_db(db_path)
        init_schema(conn)
        assert get_cache_state(conn, result_mode=RESULT_MODE_DEFAULT) == (400, 400)
        assert get_cache_state(conn, result_mode=RESULT_MODE_DIAGONAL_SIGN) == (400, 400)
        default_count = conn.execute(
            "SELECT COUNT(*) FROM chain_cache_results WHERE mode = ?",
            (RESULT_MODE_DEFAULT,),
        ).fetchone()[0]
        diagonal_count = conn.execute(
            "SELECT COUNT(*) FROM chain_cache_results WHERE mode = ?",
            (RESULT_MODE_DIAGONAL_SIGN,),
        ).fetchone()[0]
        assert default_count > 0
        assert diagonal_count > 0
        assert diagonal_count < default_count
        conn.close()

        third = subprocess.run(default_cmd, cwd=ROOT, capture_output=True, text=True, check=True)
        assert (
            "cache high-water: result_mode=default  adjacency_max_val=400  results_max_val=400"
            in third.stdout
        )

    def test_chain_cli_resume_completes_partial_run(self, tmp_path):
        from rational_distance._legacy.chain_cache_db import (
            RESULT_MODE_DEFAULT,
            checkpoint_run,
            connect_db,
            get_cache_state,
            get_run,
            init_schema,
            insert_results,
            load_cached_adjacency_rows,
            start_run,
            update_adjacency_max_val,
        )
        from rational_distance._legacy.search_chain import (
            _iter_pythagorean_pairs,
            build_adjacency_from_rows,
            find_chains,
            iter_chain_results,
        )

        db_path = tmp_path / "chain-resume.sqlite3"
        conn = connect_db(db_path)
        init_schema(conn)

        rows = list(_iter_pythagorean_pairs(1, 80, 1, 80, progress=False))
        conn.executemany(
            "INSERT OR IGNORE INTO chain_cache_adjacency (a, b, h) VALUES (?, ?, ?)",
            rows,
        )
        conn.commit()
        update_adjacency_max_val(conn, 80)

        run_id = start_run(
            conn,
            requested_max_val=80,
            result_mode=RESULT_MODE_DEFAULT,
            require_square=False,
            starting_adjacency_max_val=80,
            starting_results_max_val=0,
        )
        cached_rows = load_cached_adjacency_rows(conn, 80)
        adj, hyp = build_adjacency_from_rows(80, iter(cached_rows))
        partial_results = []

        def _on_result(result) -> None:
            partial_results.append(result)

        def _on_outer_complete(a: int) -> None:
            if a == 40:
                raise _StopScan

        with suppress(_StopScan):
            iter_chain_results(
                adj,
                hyp,
                max_val=80,
                require_square=False,
                canonical=True,
                progress=False,
                start_a=1,
                result_callback=_on_result,
                outer_complete_callback=_on_outer_complete,
            )

        insert_results(conn, result_mode=RESULT_MODE_DEFAULT, results=partial_results)
        checkpoint_run(
            conn,
            run_id,
            40,
            new_results=len(partial_results),
            pre_filter_count=len(partial_results),
        )
        conn.close()

        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "search.py"),
                "chain",
                "--max-val",
                "80",
                "--db",
                str(db_path),
                "--resume",
                "--no-progress",
                "--top",
                "0",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        assert f"Resuming chain cache run {run_id} from a=41 (mode=default)" in proc.stdout

        conn = connect_db(db_path)
        init_schema(conn)
        assert get_cache_state(conn, result_mode=RESULT_MODE_DEFAULT) == (80, 80)
        run = get_run(conn, run_id)
        assert run is not None
        assert run["status"] == "completed"

        cached = conn.execute(
            """
            SELECT a, b, c, d
            FROM chain_cache_results
            WHERE mode = ? AND max_side <= 80
            ORDER BY a, b, c, d
            """,
            (RESULT_MODE_DEFAULT,),
        ).fetchall()
        fresh = find_chains(max_val=80, progress=False)
        assert [(int(row["a"]), int(row["b"]), int(row["c"]), int(row["d"])) for row in cached] == [
            (result.a, result.b, result.c, result.d) for result in fresh
        ]
        conn.close()
