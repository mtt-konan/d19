"""SQLite persistence for chain-fast search runs.

Schema
------
chain_runs        — one row per search run (parameters, status, progress counter)
chain_solutions   — discovered solutions (empty until Harborth conjecture is resolved)
chain_near_misses — pairs where C3 passes but C4 fails; used for proximity analysis

Resume support
--------------
After each checkpoint interval, `last_t1_index` is updated.  On resume, the caller
passes `start_t1 = last_t1_index + 1` to `find_chains_fast`.
"""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from math import isqrt
from pathlib import Path

from rational_distance.search_chain import ChainResult


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def connect_db(path: str | Path) -> sqlite3.Connection:
    """Open (or create) a SQLite database at *path* and return the connection."""
    db_path = Path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    """Create tables if they do not yet exist."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS chain_runs (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            max_hyp          INTEGER NOT NULL,
            backend          TEXT    NOT NULL DEFAULT 'python',
            status           TEXT    NOT NULL DEFAULT 'running',
            started_at       TEXT    NOT NULL,
            completed_at     TEXT,
            elapsed_s        REAL    NOT NULL DEFAULT 0,
            last_t1_index    INTEGER NOT NULL DEFAULT -1,
            n_triples        INTEGER NOT NULL DEFAULT 0,
            found_count      INTEGER NOT NULL DEFAULT 0,
            near_miss_count  INTEGER NOT NULL DEFAULT 0
        );
        CREATE INDEX IF NOT EXISTS idx_chain_runs_params
            ON chain_runs(max_hyp, status, id DESC);

        CREATE TABLE IF NOT EXISTS chain_solutions (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id  INTEGER NOT NULL REFERENCES chain_runs(id) ON DELETE CASCADE,
            a       INTEGER NOT NULL,
            b       INTEGER NOT NULL,
            c       INTEGER NOT NULL,
            d       INTEGER NOT NULL,
            x1      INTEGER NOT NULL,
            x2      INTEGER NOT NULL,
            x3      INTEGER NOT NULL,
            x4      INTEGER NOT NULL,
            UNIQUE(a, b, c, d)
        );

        CREATE TABLE IF NOT EXISTS chain_near_misses (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id       INTEGER NOT NULL REFERENCES chain_runs(id) ON DELETE CASCADE,
            a            INTEGER NOT NULL,
            b_val        INTEGER NOT NULL,
            c            INTEGER NOT NULL,
            d            INTEGER NOT NULL,
            c3_ok        INTEGER NOT NULL,
            c4_ok        INTEGER NOT NULL,
            sq3          INTEGER NOT NULL,
            sq4          INTEGER NOT NULL,
            h3           INTEGER NOT NULL,
            h4           INTEGER NOT NULL,
            sq3_deficit  INTEGER NOT NULL,
            sq4_deficit  INTEGER NOT NULL,
            UNIQUE(a, b_val, c, d)
        );
        CREATE INDEX IF NOT EXISTS idx_chain_near_misses_deficit
            ON chain_near_misses(run_id, sq4_deficit ASC);
    """)
    conn.commit()


def start_run(
    conn: sqlite3.Connection,
    max_hyp: int,
    backend: str,
    n_triples: int,
) -> int:
    """Insert a new run row and return its id."""
    cur = conn.execute(
        "INSERT INTO chain_runs (max_hyp, backend, status, started_at, n_triples) "
        "VALUES (?, ?, 'running', ?, ?)",
        (max_hyp, backend, _utc_now(), n_triples),
    )
    conn.commit()
    return int(cur.lastrowid)  # type: ignore[arg-type]


def resume_run(conn: sqlite3.Connection, max_hyp: int) -> tuple[int, int] | None:
    """Find the latest interrupted run with *max_hyp*.

    Returns (run_id, last_t1_index) so the caller can restart from
    start_t1 = last_t1_index + 1.  Returns None if no resumable run exists.
    """
    row = conn.execute(
        "SELECT id, last_t1_index FROM chain_runs "
        "WHERE max_hyp = ? AND status = 'running' "
        "ORDER BY id DESC LIMIT 1",
        (max_hyp,),
    ).fetchone()
    if row is None:
        return None
    return int(row["id"]), int(row["last_t1_index"])


def checkpoint_t1(
    conn: sqlite3.Connection,
    run_id: int,
    t1_index: int,
    near_miss_count: int,
) -> None:
    """Persist the current outer-loop position so the run can be resumed."""
    conn.execute(
        "UPDATE chain_runs "
        "SET last_t1_index = ?, near_miss_count = ? "
        "WHERE id = ?",
        (t1_index, near_miss_count, run_id),
    )
    conn.commit()


def record_solution(conn: sqlite3.Connection, run_id: int, result: ChainResult) -> None:
    """Insert a solution and increment the run's found_count."""
    conn.execute(
        "INSERT OR IGNORE INTO chain_solutions "
        "(run_id, a, b, c, d, x1, x2, x3, x4) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            run_id,
            result.a, result.b, result.c, result.d,
            result.x1, result.x2, result.x3, result.x4,
        ),
    )
    conn.execute(
        "UPDATE chain_runs SET found_count = found_count + 1 WHERE id = ?",
        (run_id,),
    )
    conn.commit()


def record_near_miss(
    conn: sqlite3.Connection,
    run_id: int,
    a: int,
    b_val: int,
    c: int,
    d: int,
    c3_ok: bool,
    c4_ok: bool,
    sq3: int,
    sq4: int,
    h3: int,
    h4: int,
) -> None:
    """Insert a near-miss row (C3 pass / C4 fail or vice versa).

    The deficit columns are computed here from the raw values:
        sq3_deficit = sq3 - h3²   (0 when C3 passes)
        sq4_deficit = sq4 - h4²   (0 when C4 passes)
    """
    sq3_deficit = sq3 - h3 * h3
    sq4_deficit = sq4 - h4 * h4
    conn.execute(
        "INSERT OR IGNORE INTO chain_near_misses "
        "(run_id, a, b_val, c, d, c3_ok, c4_ok, "
        " sq3, sq4, h3, h4, sq3_deficit, sq4_deficit) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            run_id, a, b_val, c, d,
            int(c3_ok), int(c4_ok),
            sq3, sq4, h3, h4,
            sq3_deficit, sq4_deficit,
        ),
    )
    conn.commit()


def finish_run(
    conn: sqlite3.Connection,
    run_id: int,
    found_count: int,
    elapsed: float,
) -> None:
    """Mark the run as completed."""
    conn.execute(
        "UPDATE chain_runs "
        "SET status = 'done', completed_at = ?, elapsed_s = ?, found_count = ? "
        "WHERE id = ?",
        (_utc_now(), elapsed, found_count, run_id),
    )
    conn.commit()


def get_near_misses(
    conn: sqlite3.Connection,
    run_id: int,
    limit: int = 100,
) -> list[dict]:
    """Return near-misses sorted by smallest sq4_deficit (closest to a solution)."""
    rows = conn.execute(
        "SELECT * FROM chain_near_misses WHERE run_id = ? "
        "ORDER BY sq4_deficit ASC LIMIT ?",
        (run_id, limit),
    ).fetchall()
    return [dict(row) for row in rows]


def get_run(conn: sqlite3.Connection, run_id: int) -> dict | None:
    """Fetch a single run row as a dict, or None if not found."""
    row = conn.execute("SELECT * FROM chain_runs WHERE id = ?", (run_id,)).fetchone()
    return dict(row) if row else None
