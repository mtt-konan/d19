"""CLI and script integration tests for chain-fast."""

from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


class TestChainFastCLI:
    """Tests for chain-fast CLI flows backed by the chain DB."""

    def test_chain_fast_cli_help_hides_experimental_flags(self):
        """Help output should hide experimental sieve flags but keep bucket stats visible."""
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "search.py"),
                "chain-fast",
                "--help",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        assert "--bucket-stats" in proc.stdout
        assert "--mod-sieve" not in proc.stdout
        assert "--safe-pair-sieve" not in proc.stdout

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

        from rational_distance._legacy.chain_db import connect_db as chain_connect_db
        from rational_distance._legacy.chain_db import get_run
        from rational_distance._legacy.chain_db import init_schema as chain_init_schema

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

        from rational_distance._legacy.chain_db import connect_db as chain_connect_db
        from rational_distance._legacy.chain_db import get_near_misses as chain_get_near_misses
        from rational_distance._legacy.chain_db import get_run
        from rational_distance._legacy.chain_db import init_schema as chain_init_schema

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

    def test_chain_fast_cli_bucket_stats_and_analysis(self, tmp_path):
        """CLI bucket stats should persist and the analysis script should read them."""
        db_path = tmp_path / "bucket_stats.db"
        out_json = tmp_path / "analysis.json"
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
            "--bucket-stats",
            "--near-miss",
            "--no-progress",
        ]
        subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=True)

        from rational_distance._legacy.chain_db import connect_db as chain_connect_db
        from rational_distance._legacy.chain_db import get_bucket_stats as chain_get_bucket_stats
        from rational_distance._legacy.chain_db import get_run
        from rational_distance._legacy.chain_db import init_schema as chain_init_schema

        conn = chain_connect_db(db_path)
        chain_init_schema(conn)
        run_id = conn.execute("SELECT MAX(id) FROM chain_runs").fetchone()[0]
        run = get_run(conn, run_id)
        assert run is not None
        assert run["bucket_stats"] == 1
        bucket_rows = chain_get_bucket_stats(conn, run_id)
        assert bucket_rows
        conn.close()

        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "archive" / "analyze_chain_db.py"),
                "--db",
                str(db_path),
                "--run",
                "latest",
                "--bucket-type",
                "g_bucket",
                "--top",
                "3",
                "--min-after-basic",
                "1",
                "--out-json",
                str(out_json),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        assert "Chain database analysis" in proc.stdout
        assert out_json.exists()
        payload = json.loads(out_json.read_text(encoding="utf-8"))
        assert payload["run"]["id"] == run_id
        assert "g_bucket" in payload["rankings"]

    def test_chain_fast_cli_bucket_stats_requires_db(self, tmp_path):
        """bucket stats should fail fast when no DB path is provided."""
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "search.py"),
                "chain-fast",
                "--max-hyp",
                "60",
                "--bucket-stats",
                "--no-progress",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert proc.returncode != 0
        combined = f"{proc.stdout}\n{proc.stderr}"
        assert "--bucket-stats requires --db" in combined

    def test_chain_fast_cli_safe_pair_sieve_python(self):
        """The experimental safe pair sieve should run on the python backend."""
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "search.py"),
                "chain-fast",
                "--max-hyp",
                "120",
                "--backend",
                "python",
                "--profile",
                "--safe-pair-sieve",
                "--no-progress",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        assert "safe_pair_sieve=True" in proc.stdout
        assert "after_safe_pair=" in proc.stdout

    def test_chain_fast_cli_mod_sieve_hidden_but_works(self):
        """The hidden mod sieve flag should still parse and execute."""
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "search.py"),
                "chain-fast",
                "--max-hyp",
                "120",
                "--backend",
                "python",
                "--profile",
                "--mod-sieve",
                "--no-progress",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        assert "mod_sieve=True" in proc.stdout
        assert "after_c3_mod=" in proc.stdout

    def test_chain_fast_cli_safe_pair_sieve_requires_python_backend(self):
        """CLI should fail clearly when safe-pair-sieve would hit numpy."""
        from rational_distance._legacy.search_chain_fast import _HAS_NUMPY

        for backend in ("numpy", "auto"):
            if backend == "auto" and not _HAS_NUMPY:
                continue
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "search.py"),
                    "chain-fast",
                    "--max-hyp",
                    "120",
                    "--backend",
                    backend,
                    "--safe-pair-sieve",
                    "--no-progress",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            assert proc.returncode != 0
            combined = f"{proc.stdout}\n{proc.stderr}"
            assert "--safe-pair-sieve currently supports only backend=python" in combined

    def test_cli_fails_on_legacy_chain_db(self, tmp_path):
        """The chain-fast CLI should fail clearly on an old schema DB."""
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
