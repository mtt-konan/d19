"""Tests for chain DB persistence and CLI-backed DB flows."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

class TestChainDB:
    """Tests for the chain_db SQLite persistence layer."""

    def _make_conn(self, tmp_path):
        from rational_distance.chain_db import connect_db, init_schema

        conn = connect_db(tmp_path / "test.db")
        init_schema(conn)
        return conn

    @staticmethod
    def _params(**overrides):
        params = {
            "backend": "python",
            "max_hyp": 500,
            "near_miss": False,
            "near_miss_limit": 100000,
            "profile": False,
            "workers": 1,
        }
        params.update(overrides)
        return params

    def test_init_schema_creates_tables(self, tmp_path):
        """init_schema should create the run/result/cache tables."""
        conn = self._make_conn(tmp_path)
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
        names = {r[0] for r in rows}
        assert "chain_meta" in names
        assert "chain_near_misses" in names
        assert "chain_runs" in names
        assert "chain_run_triples" in names
        assert "chain_solutions" in names
        assert "chain_triples" in names

    def test_start_and_finish_run(self, tmp_path):
        """start_run and finish_run should store profile fields."""
        from rational_distance.chain_db import finish_run, get_run, start_run
        from rational_distance.search_chain_fast import ChainFastProfile

        conn = self._make_conn(tmp_path)
        run_id = start_run(
            conn,
            self._params(backend="numpy", profile=True),
            n_triples=160,
            triples_source="generated",
        )
        assert isinstance(run_id, int)
        profile = ChainFastProfile(
            requested_backend="numpy",
            backend="numpy",
            workers=1,
            profile_enabled=True,
            triples_source="generated",
            n_triples=160,
            n_pairs_total=1000,
            n_pairs_after_basic_filters=200,
            n_c3_pass=50,
            n_c4_pass=10,
            n_solutions_before_dedup=3,
            n_solutions_after_dedup=0,
            near_miss_seen=7,
            near_miss_saved=5,
            near_miss_dropped=2,
            time_generate_triples_s=0.1,
            time_outer_loop_s=0.2,
            time_filter_s=0.03,
            time_c3_s=0.04,
            time_c4_s=0.05,
            time_dedup_s=0.06,
            time_db_write_s=0.07,
            db_bytes_after_run=1234,
        )
        finish_run(conn, run_id, elapsed=1.23, profile=profile)
        run = get_run(conn, run_id)
        assert run["status"] == "done"
        assert run["found_count"] == 0
        assert run["near_miss_count"] == 0
        assert abs(run["elapsed_s"] - 1.23) < 0.01
        assert run["n_pairs_total"] == 1000
        assert run["triples_source"] == "generated"

    def test_record_solution_dedup(self, tmp_path):
        """record_solution should dedup within one run and count only real inserts."""
        from rational_distance.chain_db import get_run, record_solution, start_run
        from rational_distance.search_chain import ChainResult

        conn = self._make_conn(tmp_path)
        run_id = start_run(conn, self._params(), n_triples=160)
        r = ChainResult(a=3, b=4, c=5, d=4, x1=5, x2=5, x3=5, x4=5, square_ok=True)
        assert record_solution(conn, run_id, r) is True
        assert record_solution(conn, run_id, r) is False
        count = conn.execute("SELECT COUNT(*) FROM chain_solutions").fetchone()[0]
        run = get_run(conn, run_id)
        assert count == 1
        assert run["found_count"] == 1

    def test_record_solution_isolated_per_run(self, tmp_path):
        """The same solution should be storable in two different runs."""
        from rational_distance.chain_db import get_run, record_solution, start_run
        from rational_distance.search_chain import ChainResult

        conn = self._make_conn(tmp_path)
        run_a = start_run(conn, self._params(max_hyp=500), n_triples=160)
        run_b = start_run(conn, self._params(max_hyp=600), n_triples=200)
        result = ChainResult(a=3, b=4, c=5, d=4, x1=5, x2=5, x3=5, x4=5, square_ok=True)
        assert record_solution(conn, run_a, result) is True
        assert record_solution(conn, run_b, result) is True
        rows = conn.execute(
            "SELECT run_id, COUNT(*) AS n FROM chain_solutions GROUP BY run_id"
        ).fetchall()
        assert {(row["run_id"], row["n"]) for row in rows} == {(run_a, 1), (run_b, 1)}
        assert get_run(conn, run_a)["found_count"] == 1
        assert get_run(conn, run_b)["found_count"] == 1

    def test_checkpoint_and_resume(self, tmp_path):
        """resume_run should only match runs with identical params."""
        from rational_distance.chain_db import checkpoint_t1, resume_run, start_run

        conn = self._make_conn(tmp_path)
        params = self._params(backend="numpy")
        run_id = start_run(conn, params, n_triples=160)
        checkpoint_t1(conn, run_id, t1_index=42)
        result = resume_run(conn, params)
        assert result is not None
        rid, last = result
        assert rid == run_id
        assert last == 42
        assert resume_run(conn, self._params(backend="python")) is None
        assert resume_run(conn, self._params(backend="numpy", near_miss=True)) is None

    def test_record_near_miss(self, tmp_path):
        """record_near_miss should dedup within one run and count only real inserts."""
        from rational_distance.chain_db import get_near_misses, get_run, record_near_miss, start_run

        conn = self._make_conn(tmp_path)
        run_id = start_run(conn, self._params(near_miss=True), n_triples=160)
        # sq4 = 25, h4 = 4 → sq4_deficit = 25 - 16 = 9
        assert record_near_miss(
            conn,
            run_id,
            a=3,
            b_val=4,
            c=5,
            d=6,
            c3_ok=True,
            c4_ok=False,
            sq3=61,
            sq4=25,
            h3=7,
            h4=4,
        ) is True
        assert record_near_miss(
            conn,
            run_id,
            a=3,
            b_val=4,
            c=5,
            d=6,
            c3_ok=True,
            c4_ok=False,
            sq3=61,
            sq4=25,
            h3=7,
            h4=4,
        ) is False
        rows = get_near_misses(conn, run_id)
        assert len(rows) == 1
        assert rows[0]["sq4_deficit"] == 9
        assert get_run(conn, run_id)["near_miss_count"] == 1

    def test_record_near_miss_isolated_per_run(self, tmp_path):
        """The same near-miss should be storable in two different runs."""
        from rational_distance.chain_db import get_run, record_near_miss, start_run

        conn = self._make_conn(tmp_path)
        run_a = start_run(conn, self._params(max_hyp=500, near_miss=True), n_triples=160)
        run_b = start_run(conn, self._params(max_hyp=700, near_miss=True), n_triples=220)
        kwargs = {
            "a": 3,
            "b_val": 4,
            "c": 5,
            "d": 6,
            "c3_ok": True,
            "c4_ok": False,
            "sq3": 61,
            "sq4": 25,
            "h3": 7,
            "h4": 4,
        }
        assert record_near_miss(conn, run_a, **kwargs) is True
        assert record_near_miss(conn, run_b, **kwargs) is True
        rows = conn.execute(
            "SELECT run_id, COUNT(*) AS n FROM chain_near_misses GROUP BY run_id"
        ).fetchall()
        assert {(row["run_id"], row["n"]) for row in rows} == {(run_a, 1), (run_b, 1)}
        assert get_run(conn, run_a)["near_miss_count"] == 1
        assert get_run(conn, run_b)["near_miss_count"] == 1

    def test_finish_run_recomputes_counts(self, tmp_path):
        """finish_run should recompute both counts from the per-run tables."""
        from rational_distance.chain_db import (
            finish_run,
            get_run,
            record_near_miss,
            record_solution,
            start_run,
        )
        from rational_distance.search_chain import ChainResult

        conn = self._make_conn(tmp_path)
        run_id = start_run(conn, self._params(near_miss=True), n_triples=160)
        result = ChainResult(a=3, b=4, c=5, d=4, x1=5, x2=5, x3=5, x4=5, square_ok=True)
        record_solution(conn, run_id, result)
        record_near_miss(
            conn,
            run_id,
            a=3,
            b_val=4,
            c=5,
            d=6,
            c3_ok=True,
            c4_ok=False,
            sq3=61,
            sq4=25,
            h3=7,
            h4=4,
        )
        conn.execute(
            "UPDATE chain_runs SET found_count = 99, near_miss_count = 88 WHERE id = ?",
            (run_id,),
        )
        conn.commit()
        finish_run(conn, run_id, elapsed=1.5)
        run = get_run(conn, run_id)
        assert run["status"] == "done"
        assert run["found_count"] == 1
        assert run["near_miss_count"] == 1

    def test_init_schema_rejects_legacy_chain_db(self, tmp_path):
        """Old chain DBs without a schema marker should be rejected."""
        import sqlite3

        from rational_distance.chain_db import connect_db, init_schema

        db_path = tmp_path / "legacy.db"
        legacy = sqlite3.connect(db_path)
        legacy.execute(
            """
            CREATE TABLE chain_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                max_hyp INTEGER NOT NULL,
                backend TEXT NOT NULL
            )
            """
        )
        legacy.commit()
        legacy.close()

        conn = connect_db(db_path)
        with pytest.raises(ValueError, match="rebuild the chain DB"):
            init_schema(conn)

    def test_cache_and_record_run_triples(self, tmp_path):
        """Triple cache and per-run triple recording should persist ordered triples."""
        from rational_distance.chain_db import (
            cache_triples,
            load_cached_triples,
            record_run_triples,
            start_run,
        )

        conn = self._make_conn(tmp_path)
        triples = [(3, 4, 5), (5, 12, 13)]
        cache_triples(conn, 13, triples)
        assert load_cached_triples(conn, 13) == triples

        run_id = start_run(
            conn,
            self._params(max_hyp=13),
            n_triples=len(triples),
            triples_source="db-cache",
        )
        record_run_triples(conn, run_id, triples)
        count = conn.execute(
            "SELECT COUNT(*) FROM chain_run_triples WHERE run_id = ?",
            (run_id,),
        ).fetchone()[0]
        assert count == len(triples)

    def test_chain_fast_cli_profile_and_cache(self, tmp_path):
        """CLI run should persist profile fields and reuse cached triples on the second run."""
        db_path = tmp_path / "chain.db"
        cmd = [
            sys.executable,
            str(ROOT / "scripts" / "search.py"),
            "chain-fast",
            "--max-hyp",
            "120",
            "--backend",
            "python",
            "--db",
            str(db_path),
            "--profile",
            "--no-progress",
        ]
        first = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=True)
        assert "Profile:" in first.stdout

        from rational_distance.chain_db import connect_db as chain_connect_db
        from rational_distance.chain_db import get_run
        from rational_distance.chain_db import init_schema as chain_init_schema

        conn = chain_connect_db(db_path)
        chain_init_schema(conn)
        run_id = conn.execute("SELECT MAX(id) FROM chain_runs").fetchone()[0]
        run = get_run(conn, run_id)
        assert run is not None
        assert run["n_triples"] > 0
        assert run["db_bytes_after_run"] > 0
        assert run["triples_source"] == "generated"
        triple_count = conn.execute("SELECT COUNT(*) FROM chain_triples").fetchone()[0]
        assert triple_count == run["n_triples"]
        run_triple_count = conn.execute(
            "SELECT COUNT(*) FROM chain_run_triples WHERE run_id = ?",
            (run_id,),
        ).fetchone()[0]
        assert run_triple_count == run["n_triples"]
        conn.close()

        subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=True)
        conn = chain_connect_db(db_path)
        chain_init_schema(conn)
        second_run_id = conn.execute("SELECT MAX(id) FROM chain_runs").fetchone()[0]
        second_run = get_run(conn, second_run_id)
        assert second_run is not None
        assert second_run["triples_source"] == "db-cache"
        conn.close()

    def test_chain_fast_cli_near_miss_limit(self, tmp_path):
        """CLI near-miss logging should respect the configured top-K limit."""
        db_path = tmp_path / "near_miss.db"
        cmd = [
            sys.executable,
            str(ROOT / "scripts" / "search.py"),
            "chain-fast",
            "--max-hyp",
            "500",
            "--backend",
            "python",
            "--db",
            str(db_path),
            "--near-miss",
            "--near-miss-limit",
            "3",
            "--no-progress",
        ]
        subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=True)

        from rational_distance.chain_db import connect_db as chain_connect_db
        from rational_distance.chain_db import get_near_misses as chain_get_near_misses
        from rational_distance.chain_db import get_run
        from rational_distance.chain_db import init_schema as chain_init_schema

        conn = chain_connect_db(db_path)
        chain_init_schema(conn)
        run_id = conn.execute("SELECT MAX(id) FROM chain_runs").fetchone()[0]
        run = get_run(conn, run_id)
        assert run is not None
        assert run["near_miss_seen"] >= run["near_miss_saved"]
        assert run["near_miss_saved"] <= 3
        assert run["near_miss_dropped"] == run["near_miss_seen"] - run["near_miss_saved"]
        rows = chain_get_near_misses(conn, run_id, limit=10)
        assert len(rows) == run["near_miss_saved"]
        if len(rows) > 1:
            ordered = sorted(
                rows,
                key=lambda row: (row["sq4_deficit"], row["sq3_deficit"], row["id"]),
            )
            assert rows == ordered
        conn.close()

    def test_cli_fails_on_legacy_chain_db(self, tmp_path):
        """The chain-fast CLI should fail clearly on an old schema DB."""
        import sqlite3

        db_path = tmp_path / "legacy_cli.db"
        legacy = sqlite3.connect(db_path)
        legacy.execute(
            """
            CREATE TABLE chain_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                max_hyp INTEGER NOT NULL,
                backend TEXT NOT NULL
            )
            """
        )
        legacy.commit()
        legacy.close()

        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "search.py"),
                "chain-fast",
                "--max-hyp",
                "60",
                "--db",
                str(db_path),
                "--no-progress",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert proc.returncode != 0
        combined = f"{proc.stdout}\n{proc.stderr}"
        assert "rebuild the chain DB" in combined
