"""Compact SQLite persistence for the multi-N-first dual-closure prover.

This is a deliberately small schema, designed after profiling the legacy
``proof_status`` DB (a 10k-range snapshot weighed ~970 MB). The bloat there came
from storing, for every one of millions of pairs, a full audit row with a
free-text ``notes`` sentence, a small ``details_json`` blob, an ISO-8601 text
timestamp and a per-row float timing — almost all of which is either constant or
derivable from the verdict.

Design goals here:

- One ``run_meta`` row per run holds the run-level aggregates and the single
  timestamp (no per-row timestamps).
- ``pair_verdict`` stores one tiny row per evaluated ``(A, B)`` pair: the verdict
  is an INTEGER enum (not a repeated text string), and no notes / JSON are kept.
- ``survivor_n`` only stores the concordant-N list for the (rare) survivors, so
  the killed mass never carries a variable-length payload.

At ``max_hyp=1_000_000`` this produces a few-MB DB instead of ~1 GB.
"""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path

MULTI_FIRST_DB_SCHEMA_VERSION = 1

# Verdict enum codes stored in ``pair_verdict.verdict``.
VERDICT_SAFE_SIEVE = 0  # killed by 2-adic safe_sieve (mixed parity / mod 4)
VERDICT_CHAIN_CLOSURE = 1  # killed by chain_closure_mod_sieve on (A, B)
VERDICT_DUAL = 2  # killed by dual chain_closure on every (N_i, N_j)
VERDICT_SURVIVOR = 3  # survived every sieve

VERDICT_NAMES: dict[int, str] = {
    VERDICT_SAFE_SIEVE: "safe_sieve",
    VERDICT_CHAIN_CLOSURE: "chain_closure",
    VERDICT_DUAL: "dual_closure",
    VERDICT_SURVIVOR: "survivor",
}


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def connect_db(path: str | Path) -> sqlite3.Connection:
    """Open (or create) the compact multi-first DB at *path*."""
    db_path = Path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    """Create the compact tables if absent."""
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS multi_first_meta (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS run_meta (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            max_hyp             INTEGER NOT NULL,
            moduli_name         TEXT    NOT NULL,
            moduli              TEXT    NOT NULL,
            multi_n_pair_count  INTEGER NOT NULL,
            safe_sieve_killed   INTEGER NOT NULL,
            primary_killed      INTEGER NOT NULL,
            dual_killed         INTEGER NOT NULL,
            survivor_count      INTEGER NOT NULL,
            multi_n_elapsed_s   REAL    NOT NULL,
            sieve_elapsed_s     REAL    NOT NULL,
            created_at          TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS pair_verdict (
            A              INTEGER NOT NULL,
            B              INTEGER NOT NULL,
            k              INTEGER NOT NULL,
            verdict        INTEGER NOT NULL,
            killer_modulus INTEGER,
            PRIMARY KEY (A, B)
        ) WITHOUT ROWID;

        CREATE TABLE IF NOT EXISTS survivor_n (
            A INTEGER NOT NULL,
            B INTEGER NOT NULL,
            n INTEGER NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_survivor_n_pair ON survivor_n(A, B);
        """
    )
    conn.execute(
        """
        INSERT INTO multi_first_meta (key, value)
        VALUES ('schema_version', ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """,
        (str(MULTI_FIRST_DB_SCHEMA_VERSION),),
    )
    conn.commit()


def write_run(
    conn: sqlite3.Connection,
    *,
    max_hyp: int,
    moduli_name: str,
    moduli: tuple[int, ...],
    multi_n_pair_count: int,
    safe_sieve_killed: int,
    primary_killed: int,
    dual_killed: int,
    survivor_count: int,
    multi_n_elapsed_s: float,
    sieve_elapsed_s: float,
    pair_rows: list[tuple[int, int, int, int, int | None]],
    survivor_n_rows: list[tuple[int, int, int]],
) -> int:
    """Persist one run plus its per-pair verdicts. Returns the run_meta id.

    ``pair_rows`` items are ``(A, B, k, verdict, killer_modulus)``;
    ``survivor_n_rows`` items are ``(A, B, n)``.
    """
    cur = conn.execute(
        """
        INSERT INTO run_meta (
            max_hyp, moduli_name, moduli, multi_n_pair_count, safe_sieve_killed,
            primary_killed, dual_killed, survivor_count, multi_n_elapsed_s,
            sieve_elapsed_s, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            max_hyp,
            moduli_name,
            ",".join(str(m) for m in moduli),
            multi_n_pair_count,
            safe_sieve_killed,
            primary_killed,
            dual_killed,
            survivor_count,
            multi_n_elapsed_s,
            sieve_elapsed_s,
            _utc_now(),
        ),
    )
    run_id = int(cur.lastrowid or 0)
    conn.executemany(
        """
        INSERT INTO pair_verdict (A, B, k, verdict, killer_modulus)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(A, B) DO UPDATE SET
            k = excluded.k,
            verdict = excluded.verdict,
            killer_modulus = excluded.killer_modulus
        """,
        pair_rows,
    )
    if survivor_n_rows:
        conn.executemany(
            "INSERT INTO survivor_n (A, B, n) VALUES (?, ?, ?)",
            survivor_n_rows,
        )
    conn.commit()
    return run_id


__all__ = [
    "MULTI_FIRST_DB_SCHEMA_VERSION",
    "VERDICT_CHAIN_CLOSURE",
    "VERDICT_DUAL",
    "VERDICT_NAMES",
    "VERDICT_SAFE_SIEVE",
    "VERDICT_SURVIVOR",
    "connect_db",
    "init_schema",
    "write_run",
]
