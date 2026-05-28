"""SQLite persistence for chain-fast search runs.

Schema
------
chain_meta         — schema version marker (old schemas are rejected)
chain_runs         — one row per search run (params, status, progress, profile)
chain_solutions    — discovered solutions, unique within one run
chain_near_misses  — bounded near-miss set, unique within one run
chain_triples      — cached primitive triples for one max_hyp
chain_run_triples  — exact triple list used by one run

Resume support
--------------
Runs are identified by a stable params key instead of only ``max_hyp``.
After each completed chunk, ``last_t1_index`` is updated. On resume, the caller
passes ``start_t1 = last_t1_index + 1`` to ``run_chain_fast``.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from rational_distance._legacy.search_chain import ChainResult
from rational_distance._legacy.search_chain_fast import ChainFastProfile

CHAIN_DB_SCHEMA_VERSION = 4


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def params_key_for_run(params: dict) -> str:
    """Return a stable JSON key for one chain-fast run configuration."""
    normalized = {
        "backend": str(params["backend"]),
        "bucket_stats": bool(params.get("bucket_stats", False)),
        "max_hyp": int(params["max_hyp"]),
        "mod_sieve": bool(params.get("mod_sieve", False)),
        "near_miss": bool(params["near_miss"]),
        "near_miss_limit": int(params.get("near_miss_limit", 100000)),
        "profile": bool(params.get("profile", False)),
        "safe_pair_sieve": bool(params.get("safe_pair_sieve", False)),
        "workers": int(params.get("workers", 1)),
    }
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"))


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
    """Reject older chain DB schemas instead of attempting in-place migration."""
    if _table_exists(conn, "chain_meta"):
        row = conn.execute(
            "SELECT value FROM chain_meta WHERE key = 'schema_version'"
        ).fetchone()
        if row is None:
            raise ValueError(
                "Unsupported chain DB schema: missing schema_version. Please rebuild the chain DB."
            )
        version = int(row["value"])
        if version != CHAIN_DB_SCHEMA_VERSION:
            raise ValueError(
                "Unsupported chain DB schema version "
                f"{version} (expected {CHAIN_DB_SCHEMA_VERSION}). Please rebuild the chain DB."
            )
        return

    legacy_tables = {
        "chain_runs",
        "chain_solutions",
        "chain_near_misses",
        "chain_bucket_stats",
        "chain_triples",
        "chain_run_triples",
    }
    existing = {name for name in legacy_tables if _table_exists(conn, name)}
    if existing:
        raise ValueError(
            "Unsupported legacy chain DB schema detected. Please rebuild the chain DB."
        )


def init_schema(conn: sqlite3.Connection) -> None:
    """Create tables if they do not yet exist, rejecting unsupported old schemas."""
    _require_supported_schema(conn)
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS chain_meta (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS chain_runs (
            id                           INTEGER PRIMARY KEY AUTOINCREMENT,
            params_key                   TEXT    NOT NULL,
            params_json                  TEXT    NOT NULL,
            max_hyp                      INTEGER NOT NULL,
            backend                      TEXT    NOT NULL,
            near_miss                    INTEGER NOT NULL DEFAULT 0,
            near_miss_limit              INTEGER NOT NULL DEFAULT 100000,
            bucket_stats                 INTEGER NOT NULL DEFAULT 0,
            profile                      INTEGER NOT NULL DEFAULT 0,
            triples_source               TEXT    NOT NULL DEFAULT '',
            status                       TEXT    NOT NULL DEFAULT 'running',
            started_at                   TEXT    NOT NULL,
            completed_at                 TEXT,
            elapsed_s                    REAL    NOT NULL DEFAULT 0,
            last_t1_index                INTEGER NOT NULL DEFAULT -1,
            n_triples                    INTEGER NOT NULL DEFAULT 0,
            n_pairs_total                INTEGER NOT NULL DEFAULT 0,
            n_pairs_after_basic_filters  INTEGER NOT NULL DEFAULT 0,
            n_c3_pass                    INTEGER NOT NULL DEFAULT 0,
            n_c4_pass                    INTEGER NOT NULL DEFAULT 0,
            n_solutions_before_dedup     INTEGER NOT NULL DEFAULT 0,
            n_solutions_after_dedup      INTEGER NOT NULL DEFAULT 0,
            found_count                  INTEGER NOT NULL DEFAULT 0,
            near_miss_count              INTEGER NOT NULL DEFAULT 0,
            near_miss_seen               INTEGER NOT NULL DEFAULT 0,
            near_miss_saved              INTEGER NOT NULL DEFAULT 0,
            near_miss_dropped            INTEGER NOT NULL DEFAULT 0,
            time_generate_triples_s      REAL    NOT NULL DEFAULT 0,
            time_outer_loop_s            REAL    NOT NULL DEFAULT 0,
            time_filter_s                REAL    NOT NULL DEFAULT 0,
            time_c3_s                    REAL    NOT NULL DEFAULT 0,
            time_c4_s                    REAL    NOT NULL DEFAULT 0,
            time_dedup_s                 REAL    NOT NULL DEFAULT 0,
            time_db_write_s              REAL    NOT NULL DEFAULT 0,
            db_bytes_after_run           INTEGER NOT NULL DEFAULT 0
        );
        CREATE INDEX IF NOT EXISTS idx_chain_runs_params
            ON chain_runs(params_key, status, id DESC);

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
            UNIQUE(run_id, a, b, c, d)
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
            UNIQUE(run_id, a, b_val, c, d)
        );
        CREATE INDEX IF NOT EXISTS idx_chain_near_misses_deficit
            ON chain_near_misses(run_id, sq4_deficit ASC, sq3_deficit ASC, id ASC);

        CREATE TABLE IF NOT EXISTS chain_triples (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            max_hyp  INTEGER NOT NULL,
            seq      INTEGER NOT NULL,
            s        INTEGER NOT NULL,
            t        INTEGER NOT NULL,
            h        INTEGER NOT NULL,
            UNIQUE(max_hyp, seq),
            UNIQUE(max_hyp, s, t, h)
        );
        CREATE INDEX IF NOT EXISTS idx_chain_triples_lookup
            ON chain_triples(max_hyp, seq);

        CREATE TABLE IF NOT EXISTS chain_run_triples (
            run_id  INTEGER NOT NULL REFERENCES chain_runs(id) ON DELETE CASCADE,
            seq     INTEGER NOT NULL,
            s       INTEGER NOT NULL,
            t       INTEGER NOT NULL,
            h       INTEGER NOT NULL,
            PRIMARY KEY(run_id, seq),
            UNIQUE(run_id, s, t, h)
        );

        CREATE TABLE IF NOT EXISTS chain_bucket_stats (
            run_id               INTEGER NOT NULL REFERENCES chain_runs(id) ON DELETE CASCADE,
            bucket_type          TEXT    NOT NULL,
            bucket_key_json      TEXT    NOT NULL,
            n_total              INTEGER NOT NULL DEFAULT 0,
            n_after_basic        INTEGER NOT NULL DEFAULT 0,
            n_c3_pass            INTEGER NOT NULL DEFAULT 0,
            n_c4_pass            INTEGER NOT NULL DEFAULT 0,
            n_near_miss          INTEGER NOT NULL DEFAULT 0,
            best_sq4_deficit     INTEGER,
            best_sq3_deficit     INTEGER,
            sample_a             INTEGER,
            sample_b             INTEGER,
            sample_c             INTEGER,
            sample_d             INTEGER,
            sample_sq3_deficit   INTEGER,
            sample_sq4_deficit   INTEGER,
            PRIMARY KEY(run_id, bucket_type, bucket_key_json)
        );
        CREATE INDEX IF NOT EXISTS idx_chain_bucket_stats_type
            ON chain_bucket_stats(run_id, bucket_type);
        """
    )
    conn.execute(
        """
        INSERT INTO chain_meta (key, value)
        VALUES ('schema_version', ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """,
        (str(CHAIN_DB_SCHEMA_VERSION),),
    )
    conn.commit()


def load_cached_triples(conn: sqlite3.Connection, max_hyp: int) -> list[tuple[int, int, int]]:
    """Load cached triples for one ``max_hyp``. Returns [] when cache is empty."""
    rows = conn.execute(
        """
        SELECT s, t, h
        FROM chain_triples
        WHERE max_hyp = ?
        ORDER BY seq ASC
        """,
        (max_hyp,),
    ).fetchall()
    return [(int(row["s"]), int(row["t"]), int(row["h"])) for row in rows]


def cache_triples(
    conn: sqlite3.Connection,
    max_hyp: int,
    triples: list[tuple[int, int, int]],
) -> None:
    """Persist the ordered primitive triple list for one ``max_hyp``."""
    conn.executemany(
        """
        INSERT OR IGNORE INTO chain_triples (max_hyp, seq, s, t, h)
        VALUES (?, ?, ?, ?, ?)
        """,
        [(max_hyp, idx, s, t, h) for idx, (s, t, h) in enumerate(triples)],
    )
    conn.commit()


def record_run_triples(
    conn: sqlite3.Connection,
    run_id: int,
    triples: list[tuple[int, int, int]],
) -> None:
    """Persist the exact ordered triple list used by one run."""
    conn.executemany(
        """
        INSERT OR IGNORE INTO chain_run_triples (run_id, seq, s, t, h)
        VALUES (?, ?, ?, ?, ?)
        """,
        [(run_id, idx, s, t, h) for idx, (s, t, h) in enumerate(triples)],
    )
    conn.commit()


def start_run(
    conn: sqlite3.Connection,
    params: dict,
    n_triples: int,
    triples_source: str = "",
) -> int:
    """Insert a new run row and return its id."""
    params_key = params_key_for_run(params)
    params_json = json.dumps(params, sort_keys=True, separators=(",", ":"))
    cur = conn.execute(
        """
        INSERT INTO chain_runs (
            params_key,
            params_json,
            max_hyp,
            backend,
            near_miss,
            near_miss_limit,
            bucket_stats,
            profile,
            triples_source,
            status,
            started_at,
            n_triples
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'running', ?, ?)
        """,
        (
            params_key,
            params_json,
            int(params["max_hyp"]),
            str(params["backend"]),
            int(bool(params["near_miss"])),
            int(params.get("near_miss_limit", 100000)),
            int(bool(params.get("bucket_stats", False))),
            int(bool(params.get("profile", False))),
            triples_source,
            _utc_now(),
            n_triples,
        ),
    )
    conn.commit()
    return int(cur.lastrowid)


def resume_run(conn: sqlite3.Connection, params: dict) -> tuple[int, int] | None:
    """Find the latest interrupted run for the exact chain-fast params."""
    params_key = params_key_for_run(params)
    row = conn.execute(
        """
        SELECT id, last_t1_index
        FROM chain_runs
        WHERE params_key = ? AND status = 'running'
        ORDER BY id DESC
        LIMIT 1
        """,
        (params_key,),
    ).fetchone()
    if row is None:
        return None
    return int(row["id"]), int(row["last_t1_index"])


def checkpoint_t1(conn: sqlite3.Connection, run_id: int, t1_index: int) -> None:
    """Persist the latest fully completed outer-loop index."""
    conn.execute(
        "UPDATE chain_runs SET last_t1_index = ? WHERE id = ?",
        (t1_index, run_id),
    )
    conn.commit()


def record_solution(conn: sqlite3.Connection, run_id: int, result: ChainResult) -> bool:
    """Insert a solution and increment the run count only if it is new."""
    cur = conn.execute(
        """
        INSERT OR IGNORE INTO chain_solutions
        (run_id, a, b, c, d, x1, x2, x3, x4)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_id,
            result.a,
            result.b,
            result.c,
            result.d,
            result.x1,
            result.x2,
            result.x3,
            result.x4,
        ),
    )
    inserted = cur.rowcount == 1
    if inserted:
        conn.execute(
            "UPDATE chain_runs SET found_count = found_count + 1 WHERE id = ?",
            (run_id,),
        )
    conn.commit()
    return inserted


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
) -> bool:
    """Insert one near-miss row and increment the run count only if it is new."""
    sq3_deficit = sq3 - h3 * h3
    sq4_deficit = sq4 - h4 * h4
    cur = conn.execute(
        """
        INSERT OR IGNORE INTO chain_near_misses
        (run_id, a, b_val, c, d, c3_ok, c4_ok, sq3, sq4, h3, h4, sq3_deficit, sq4_deficit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_id,
            a,
            b_val,
            c,
            d,
            int(c3_ok),
            int(c4_ok),
            sq3,
            sq4,
            h3,
            h4,
            sq3_deficit,
            sq4_deficit,
        ),
    )
    inserted = cur.rowcount == 1
    if inserted:
        conn.execute(
            "UPDATE chain_runs SET near_miss_count = near_miss_count + 1 WHERE id = ?",
            (run_id,),
        )
    conn.commit()
    return inserted


def record_near_misses(conn: sqlite3.Connection, run_id: int, rows: list[dict]) -> int:
    """Bulk insert near-misses. Returns the number of inserted rows."""
    inserted = 0
    for row in rows:
        cur = conn.execute(
            """
            INSERT OR IGNORE INTO chain_near_misses
            (run_id, a, b_val, c, d, c3_ok, c4_ok, sq3, sq4, h3, h4, sq3_deficit, sq4_deficit)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                int(row["a"]),
                int(row["b_val"]),
                int(row["c"]),
                int(row["d"]),
                int(bool(row["c3_ok"])),
                int(bool(row["c4_ok"])),
                int(row["sq3"]),
                int(row["sq4"]),
                int(row["h3"]),
                int(row["h4"]),
                int(row["sq3_deficit"]),
                int(row["sq4_deficit"]),
            ),
        )
        inserted += int(cur.rowcount == 1)
    if inserted:
        conn.execute(
            "UPDATE chain_runs SET near_miss_count = near_miss_count + ? WHERE id = ?",
            (inserted, run_id),
        )
    conn.commit()
    return inserted


def finish_run(
    conn: sqlite3.Connection,
    run_id: int,
    elapsed: float,
    profile: ChainFastProfile | None = None,
) -> None:
    """Mark the run as completed, storing the latest profile snapshot."""
    found_count = conn.execute(
        "SELECT COUNT(*) FROM chain_solutions WHERE run_id = ?",
        (run_id,),
    ).fetchone()[0]
    near_miss_count = conn.execute(
        "SELECT COUNT(*) FROM chain_near_misses WHERE run_id = ?",
        (run_id,),
    ).fetchone()[0]

    values: dict[str, object] = {
        "completed_at": _utc_now(),
        "elapsed_s": elapsed,
        "found_count": int(found_count),
        "near_miss_count": int(near_miss_count),
        "status": "done",
        "n_triples": None,
        "n_pairs_total": None,
        "n_pairs_after_basic_filters": None,
        "n_c3_pass": None,
        "n_c4_pass": None,
        "n_solutions_before_dedup": None,
        "n_solutions_after_dedup": None,
        "near_miss_seen": None,
        "near_miss_saved": None,
        "near_miss_dropped": None,
        "time_generate_triples_s": None,
        "time_outer_loop_s": None,
        "time_filter_s": None,
        "time_c3_s": None,
        "time_c4_s": None,
        "time_dedup_s": None,
        "time_db_write_s": None,
        "db_bytes_after_run": None,
        "triples_source": None,
    }
    if profile is not None:
        values.update(profile.as_dict())
        values["n_solutions_after_dedup"] = int(found_count)
        values["near_miss_saved"] = int(profile.near_miss_saved or near_miss_count)

    conn.execute(
        """
        UPDATE chain_runs
        SET status = :status,
            completed_at = :completed_at,
            elapsed_s = :elapsed_s,
            found_count = :found_count,
            near_miss_count = :near_miss_count,
            n_triples = COALESCE(:n_triples, n_triples),
            n_pairs_total = COALESCE(:n_pairs_total, n_pairs_total),
            n_pairs_after_basic_filters = COALESCE(
                :n_pairs_after_basic_filters,
                n_pairs_after_basic_filters
            ),
            n_c3_pass = COALESCE(:n_c3_pass, n_c3_pass),
            n_c4_pass = COALESCE(:n_c4_pass, n_c4_pass),
            n_solutions_before_dedup = COALESCE(
                :n_solutions_before_dedup,
                n_solutions_before_dedup
            ),
            n_solutions_after_dedup = COALESCE(:n_solutions_after_dedup, n_solutions_after_dedup),
            near_miss_seen = COALESCE(:near_miss_seen, near_miss_seen),
            near_miss_saved = COALESCE(:near_miss_saved, near_miss_saved),
            near_miss_dropped = COALESCE(:near_miss_dropped, near_miss_dropped),
            time_generate_triples_s = COALESCE(:time_generate_triples_s, time_generate_triples_s),
            time_outer_loop_s = COALESCE(:time_outer_loop_s, time_outer_loop_s),
            time_filter_s = COALESCE(:time_filter_s, time_filter_s),
            time_c3_s = COALESCE(:time_c3_s, time_c3_s),
            time_c4_s = COALESCE(:time_c4_s, time_c4_s),
            time_dedup_s = COALESCE(:time_dedup_s, time_dedup_s),
            time_db_write_s = COALESCE(:time_db_write_s, time_db_write_s),
            db_bytes_after_run = COALESCE(:db_bytes_after_run, db_bytes_after_run),
            triples_source = COALESCE(:triples_source, triples_source)
        WHERE id = :run_id
        """,
        {**values, "run_id": run_id},
    )
    conn.commit()


def update_run_db_size(conn: sqlite3.Connection, run_id: int, db_bytes_after_run: int) -> None:
    """Persist the final SQLite file size after a run."""
    conn.execute(
        "UPDATE chain_runs SET db_bytes_after_run = ? WHERE id = ?",
        (db_bytes_after_run, run_id),
    )
    conn.commit()


def record_bucket_stats(conn: sqlite3.Connection, run_id: int, rows: list[dict]) -> int:
    """Bulk insert aggregated bucket-stat rows for one run."""
    if not rows:
        return 0
    conn.executemany(
        """
        INSERT OR REPLACE INTO chain_bucket_stats (
            run_id,
            bucket_type,
            bucket_key_json,
            n_total,
            n_after_basic,
            n_c3_pass,
            n_c4_pass,
            n_near_miss,
            best_sq4_deficit,
            best_sq3_deficit,
            sample_a,
            sample_b,
            sample_c,
            sample_d,
            sample_sq3_deficit,
            sample_sq4_deficit
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                run_id,
                str(row["bucket_type"]),
                str(row["bucket_key_json"]),
                int(row["n_total"]),
                int(row["n_after_basic"]),
                int(row["n_c3_pass"]),
                int(row["n_c4_pass"]),
                int(row["n_near_miss"]),
                row["best_sq4_deficit"],
                row["best_sq3_deficit"],
                row["sample_a"],
                row["sample_b"],
                row["sample_c"],
                row["sample_d"],
                row["sample_sq3_deficit"],
                row["sample_sq4_deficit"],
            )
            for row in rows
        ],
    )
    conn.commit()
    return len(rows)


def get_near_misses(
    conn: sqlite3.Connection,
    run_id: int,
    limit: int = 100,
) -> list[dict]:
    """Return near-misses sorted by smallest deficits within one run."""
    rows = conn.execute(
        """
        SELECT *
        FROM chain_near_misses
        WHERE run_id = ?
        ORDER BY sq4_deficit ASC, sq3_deficit ASC, id ASC
        LIMIT ?
        """,
        (run_id, limit),
    ).fetchall()
    return [dict(row) for row in rows]


def get_run(conn: sqlite3.Connection, run_id: int) -> dict | None:
    """Fetch a single run row as a dict, or None if not found."""
    row = conn.execute("SELECT * FROM chain_runs WHERE id = ?", (run_id,)).fetchone()
    return dict(row) if row else None


def get_bucket_stats(
    conn: sqlite3.Connection,
    run_id: int,
    bucket_type: str | None = None,
) -> list[dict]:
    """Fetch persisted bucket stats for one run."""
    if bucket_type is None:
        rows = conn.execute(
            """
            SELECT *
            FROM chain_bucket_stats
            WHERE run_id = ?
            ORDER BY bucket_type ASC, bucket_key_json ASC
            """,
            (run_id,),
        ).fetchall()
    else:
        rows = conn.execute(
            """
            SELECT *
            FROM chain_bucket_stats
            WHERE run_id = ? AND bucket_type = ?
            ORDER BY bucket_key_json ASC
            """,
            (run_id, bucket_type),
        ).fetchall()
    return [dict(row) for row in rows]
