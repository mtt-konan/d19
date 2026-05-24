"""SQLite persistence for proof_status runs.

Schema
------
proof_meta              — schema version marker (old schemas are rejected)
pair_proof_status       — one row per (A, B); current best-known conclusion
pair_method_attempts    — one row per (pair, method) attempt; full history

Design notes
------------
- The same pair can be tried by multiple methods over many runs. We never
  delete attempts: every attempt is appended to ``pair_method_attempts``.
- ``pair_proof_status`` is a *materialised summary* of the strongest conclusion
  reached so far for the pair. ``no_solution`` and ``solution_found`` are
  terminal; subsequent attempts are still recorded but the summary stays put.
- All "no_solution" conclusions must come from a method that is mathematically
  rigorous (no heuristic shortcuts).
"""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from rational_distance.proof_status.types import MethodResult, PairProofStatus

PROOF_DB_SCHEMA_VERSION = 1


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


def _table_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
        (name,),
    ).fetchone()
    return row is not None


def _require_supported_schema(conn: sqlite3.Connection) -> None:
    """Reject older proof DB schemas instead of attempting in-place migration."""
    if _table_exists(conn, "proof_meta"):
        row = conn.execute("SELECT value FROM proof_meta WHERE key = 'schema_version'").fetchone()
        if row is None:
            raise ValueError(
                "Unsupported proof DB schema: missing schema_version. Please rebuild the proof DB."
            )
        version = int(row["value"])
        if version != PROOF_DB_SCHEMA_VERSION:
            raise ValueError(
                "Unsupported proof DB schema version "
                f"{version} (expected {PROOF_DB_SCHEMA_VERSION}). "
                "Please rebuild the proof DB."
            )
        return

    legacy_tables = {"pair_proof_status", "pair_method_attempts"}
    existing = {name for name in legacy_tables if _table_exists(conn, name)}
    if existing:
        raise ValueError(
            "Unsupported legacy proof DB schema detected. Please rebuild the proof DB."
        )


def init_schema(conn: sqlite3.Connection) -> None:
    """Create tables if they do not yet exist, rejecting unsupported old schemas."""
    _require_supported_schema(conn)
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS proof_meta (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS pair_proof_status (
            id                       INTEGER PRIMARY KEY AUTOINCREMENT,
            A                        INTEGER NOT NULL,
            B                        INTEGER NOT NULL,
            status                   TEXT    NOT NULL DEFAULT 'unknown',
            method                   TEXT,
            rank_lower               INTEGER,
            rank_upper               INTEGER,
            concordant_n_count       INTEGER,
            chain_compatible_count   INTEGER,
            notes                    TEXT    NOT NULL DEFAULT '',
            updated_at               TEXT    NOT NULL,
            UNIQUE(A, B)
        );
        CREATE INDEX IF NOT EXISTS idx_pair_proof_status_status
            ON pair_proof_status(status);

        CREATE TABLE IF NOT EXISTS pair_method_attempts (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            A               INTEGER NOT NULL,
            B               INTEGER NOT NULL,
            method          TEXT    NOT NULL,
            outcome         TEXT    NOT NULL,
            details_json    TEXT    NOT NULL DEFAULT '{}',
            elapsed_s       REAL    NOT NULL DEFAULT 0,
            notes           TEXT    NOT NULL DEFAULT '',
            attempted_at    TEXT    NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_pair_method_attempts_pair
            ON pair_method_attempts(A, B);
        CREATE INDEX IF NOT EXISTS idx_pair_method_attempts_method
            ON pair_method_attempts(method, outcome);
        """
    )
    conn.execute(
        """
        INSERT INTO proof_meta (key, value)
        VALUES ('schema_version', ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """,
        (str(PROOF_DB_SCHEMA_VERSION),),
    )
    conn.commit()


def get_pair_status(conn: sqlite3.Connection, A: int, B: int) -> PairProofStatus | None:
    """Return the current materialised status for one pair, or None if absent."""
    row = conn.execute(
        "SELECT * FROM pair_proof_status WHERE A = ? AND B = ?",
        (A, B),
    ).fetchone()
    if row is None:
        return None
    return PairProofStatus(
        A=int(row["A"]),
        B=int(row["B"]),
        status=row["status"],
        method=row["method"],
        rank_lower=row["rank_lower"],
        rank_upper=row["rank_upper"],
        concordant_n_count=row["concordant_n_count"],
        chain_compatible_count=row["chain_compatible_count"],
        notes=row["notes"] or "",
        updated_at=row["updated_at"],
    )


def upsert_pair_status(
    conn: sqlite3.Connection,
    *,
    A: int,
    B: int,
    status: str,
    method: str | None = None,
    rank_lower: int | None = None,
    rank_upper: int | None = None,
    concordant_n_count: int | None = None,
    chain_compatible_count: int | None = None,
    notes: str = "",
    commit: bool = True,
) -> None:
    """Insert or update the materialised proof status for one pair.

    Set ``commit=False`` to defer the commit (useful for batched/parallel
    writes where the caller drives commits at a coarser granularity).
    """
    conn.execute(
        """
        INSERT INTO pair_proof_status (
            A, B, status, method,
            rank_lower, rank_upper,
            concordant_n_count, chain_compatible_count,
            notes, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(A, B) DO UPDATE SET
            status                 = excluded.status,
            method                 = excluded.method,
            rank_lower             = COALESCE(excluded.rank_lower, pair_proof_status.rank_lower),
            rank_upper             = COALESCE(excluded.rank_upper, pair_proof_status.rank_upper),
            concordant_n_count     = COALESCE(
                excluded.concordant_n_count, pair_proof_status.concordant_n_count
            ),
            chain_compatible_count = COALESCE(
                excluded.chain_compatible_count, pair_proof_status.chain_compatible_count
            ),
            notes                  = excluded.notes,
            updated_at             = excluded.updated_at
        """,
        (
            A,
            B,
            status,
            method,
            rank_lower,
            rank_upper,
            concordant_n_count,
            chain_compatible_count,
            notes,
            _utc_now(),
        ),
    )
    if commit:
        conn.commit()


def record_method_attempt(
    conn: sqlite3.Connection,
    *,
    A: int,
    B: int,
    result: MethodResult,
    commit: bool = True,
) -> None:
    """Append one method attempt for this pair to the audit log.

    Set ``commit=False`` to defer the commit (useful for batched/parallel
    writes where the caller drives commits at a coarser granularity).
    """
    conn.execute(
        """
        INSERT INTO pair_method_attempts
        (A, B, method, outcome, details_json, elapsed_s, notes, attempted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            A,
            B,
            result.method,
            result.outcome,
            json.dumps(result.details, sort_keys=True, separators=(",", ":")),
            float(result.elapsed_s),
            result.notes,
            _utc_now(),
        ),
    )
    if commit:
        conn.commit()


def status_counts(conn: sqlite3.Connection) -> dict[str, int]:
    """Return a count breakdown across status values."""
    rows = conn.execute(
        "SELECT status, COUNT(*) AS n FROM pair_proof_status GROUP BY status"
    ).fetchall()
    return {row["status"]: int(row["n"]) for row in rows}


def method_outcome_counts(conn: sqlite3.Connection) -> dict[tuple[str, str], int]:
    """Return a count breakdown by (method, outcome) across all attempts."""
    rows = conn.execute(
        """
        SELECT method, outcome, COUNT(*) AS n
        FROM pair_method_attempts
        GROUP BY method, outcome
        ORDER BY method ASC, outcome ASC
        """
    ).fetchall()
    return {(row["method"], row["outcome"]): int(row["n"]) for row in rows}


def iter_hard_cases(conn: sqlite3.Connection, limit: int | None = None):
    """Yield pairs currently classified as hard_case for downstream analysis."""
    query = (
        "SELECT A, B, rank_lower, rank_upper, notes, updated_at "
        "FROM pair_proof_status WHERE status = 'hard_case' "
        "ORDER BY A ASC, B ASC"
    )
    if limit is not None:
        query += f" LIMIT {int(limit)}"
    yield from (dict(row) for row in conn.execute(query).fetchall())


__all__ = [
    "PROOF_DB_SCHEMA_VERSION",
    "connect_db",
    "get_pair_status",
    "init_schema",
    "iter_hard_cases",
    "method_outcome_counts",
    "record_method_attempt",
    "status_counts",
    "upsert_pair_status",
]
