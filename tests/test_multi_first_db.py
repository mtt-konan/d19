"""Tests for the compact multi-first SQLite persistence layer."""

from __future__ import annotations

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from rational_distance.proof_status import multi_first_db as mfdb


def _write_sample(path: Path) -> int:
    conn = mfdb.connect_db(path)
    try:
        mfdb.init_schema(conn)
        return mfdb.write_run(
            conn,
            max_hyp=2000,
            moduli_name="standard",
            moduli=(9, 25, 49),
            multi_n_pair_count=4,
            safe_sieve_killed=2,
            primary_killed=1,
            dual_killed=0,
            survivor_count=1,
            multi_n_elapsed_s=0.5,
            sieve_elapsed_s=0.1,
            pair_rows=[
                (2, 85, 2, mfdb.VERDICT_SAFE_SIEVE, None),
                (2, 91, 2, mfdb.VERDICT_SAFE_SIEVE, None),
                (25, 91, 2, mfdb.VERDICT_CHAIN_CLOSURE, 9),
                (100, 200, 3, mfdb.VERDICT_SURVIVOR, None),
            ],
            survivor_n_rows=[(100, 200, 7), (100, 200, 11)],
        )
    finally:
        conn.close()


def test_write_run_roundtrip(tmp_path: Path) -> None:
    db = tmp_path / "mf.db"
    run_id = _write_sample(db)
    assert run_id == 1
    # WAL side files should be checkpointed away on clean close.
    assert db.exists()

    conn = mfdb.connect_db(db)
    try:
        version = conn.execute(
            "SELECT value FROM multi_first_meta WHERE key = 'schema_version'"
        ).fetchone()[0]
        assert int(version) == mfdb.MULTI_FIRST_DB_SCHEMA_VERSION

        meta = conn.execute("SELECT * FROM run_meta WHERE id = ?", (run_id,)).fetchone()
        assert meta["max_hyp"] == 2000
        assert meta["moduli"] == "9,25,49"
        assert meta["survivor_count"] == 1

        hist = dict(
            conn.execute("SELECT verdict, count(*) FROM pair_verdict GROUP BY verdict")
        )
        assert hist == {
            mfdb.VERDICT_SAFE_SIEVE: 2,
            mfdb.VERDICT_CHAIN_CLOSURE: 1,
            mfdb.VERDICT_SURVIVOR: 1,
        }

        killer = conn.execute(
            "SELECT killer_modulus FROM pair_verdict WHERE A = 25 AND B = 91"
        ).fetchone()[0]
        assert killer == 9

        survivor_ns = [
            r[0]
            for r in conn.execute(
                "SELECT n FROM survivor_n WHERE A = 100 AND B = 200 ORDER BY n"
            )
        ]
        assert survivor_ns == [7, 11]
    finally:
        conn.close()


def test_pair_verdict_upsert_is_idempotent(tmp_path: Path) -> None:
    db = tmp_path / "mf.db"
    _write_sample(db)
    _write_sample(db)  # second run must not duplicate pair rows (PK on A,B)

    conn = mfdb.connect_db(db)
    try:
        assert conn.execute("SELECT count(*) FROM pair_verdict").fetchone()[0] == 4
        assert conn.execute("SELECT count(*) FROM run_meta").fetchone()[0] == 2
        # survivor_n must not accumulate duplicates across repeated writes.
        assert conn.execute("SELECT count(*) FROM survivor_n").fetchone()[0] == 2
    finally:
        conn.close()


def test_survivor_n_cleared_when_pair_later_killed(tmp_path: Path) -> None:
    db = tmp_path / "mf.db"
    _write_sample(db)  # (100, 200) is a survivor with two concordant N

    # Re-run: the same pair is now killed, so it carries no survivor_n rows.
    conn = mfdb.connect_db(db)
    try:
        mfdb.write_run(
            conn,
            max_hyp=2000,
            moduli_name="standard",
            moduli=(9, 25, 49),
            multi_n_pair_count=1,
            safe_sieve_killed=0,
            primary_killed=0,
            dual_killed=1,
            survivor_count=0,
            multi_n_elapsed_s=0.1,
            sieve_elapsed_s=0.1,
            pair_rows=[(100, 200, 3, mfdb.VERDICT_DUAL, None)],
            survivor_n_rows=[],
        )
        # Stale survivor_n rows for the now-killed pair must be gone.
        assert (
            conn.execute(
                "SELECT count(*) FROM survivor_n WHERE A = 100 AND B = 200"
            ).fetchone()[0]
            == 0
        )
        assert (
            conn.execute(
                "SELECT verdict FROM pair_verdict WHERE A = 100 AND B = 200"
            ).fetchone()[0]
            == mfdb.VERDICT_DUAL
        )
    finally:
        conn.close()
