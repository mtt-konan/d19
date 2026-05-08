"""SQLite cache and run tracking for the default chain search."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from rational_distance.search_chain import ChainResult

CHAIN_CACHE_SCHEMA_VERSION = 2
RESULT_MODE_DEFAULT = "default"
RESULT_MODE_DIAGONAL_SIGN = "diagonal_sign"
RESULT_MODES = (RESULT_MODE_DEFAULT, RESULT_MODE_DIAGONAL_SIGN)


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _require_result_mode(result_mode: str) -> str:
    mode = str(result_mode)
    if mode not in RESULT_MODES:
        raise ValueError(
            f"Unsupported chain result mode {mode!r}. Expected one of {RESULT_MODES}."
        )
    return mode


def connect_db(path: str | Path) -> sqlite3.Connection:
    """Open or create the chain cache database."""
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
    if _table_exists(conn, "chain_cache_meta"):
        row = conn.execute(
            "SELECT value FROM chain_cache_meta WHERE key = 'schema_version'"
        ).fetchone()
        if row is None:
            raise ValueError("Unsupported chain cache schema: missing schema_version.")
        version = int(row["value"])
        if version != CHAIN_CACHE_SCHEMA_VERSION:
            raise ValueError(
                "Unsupported chain cache schema version "
                f"{version} (expected {CHAIN_CACHE_SCHEMA_VERSION}). Rebuild the cache DB."
            )
        return

    legacy_tables = {
        "chain_cache_state",
        "chain_cache_result_state",
        "chain_cache_adjacency",
        "chain_cache_results",
        "chain_cache_runs",
    }
    existing = {name for name in legacy_tables if _table_exists(conn, name)}
    if existing:
        raise ValueError("Unsupported legacy chain cache schema detected. Rebuild the cache DB.")


def init_schema(conn: sqlite3.Connection) -> None:
    """Create cache tables if needed."""
    _require_supported_schema(conn)
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS chain_cache_meta (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS chain_cache_state (
            id                 INTEGER PRIMARY KEY CHECK (id = 1),
            adjacency_max_val  INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS chain_cache_result_state (
            mode                    TEXT PRIMARY KEY,
            results_max_val         INTEGER NOT NULL DEFAULT 0,
            result_count            INTEGER NOT NULL DEFAULT 0,
            square_result_count     INTEGER NOT NULL DEFAULT 0,
            pre_filter_count        INTEGER NOT NULL DEFAULT 0,
            pre_filter_square_count INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS chain_cache_adjacency (
            a  INTEGER NOT NULL,
            b  INTEGER NOT NULL,
            h  INTEGER NOT NULL,
            PRIMARY KEY (a, b)
        );
        CREATE INDEX IF NOT EXISTS idx_chain_cache_adjacency_b
            ON chain_cache_adjacency(b, a);

        CREATE TABLE IF NOT EXISTS chain_cache_results (
            mode       TEXT    NOT NULL,
            a          INTEGER NOT NULL,
            b          INTEGER NOT NULL,
            c          INTEGER NOT NULL,
            d          INTEGER NOT NULL,
            x1         INTEGER NOT NULL,
            x2         INTEGER NOT NULL,
            x3         INTEGER NOT NULL,
            x4         INTEGER NOT NULL,
            square_ok  INTEGER NOT NULL,
            max_side   INTEGER NOT NULL,
            perimeter  INTEGER NOT NULL,
            rect_w     INTEGER NOT NULL,
            rect_h     INTEGER NOT NULL,
            rect_area  INTEGER NOT NULL,
            PRIMARY KEY (mode, a, b, c, d)
        );
        CREATE INDEX IF NOT EXISTS idx_chain_cache_results_mode_max_side
            ON chain_cache_results(
                mode,
                max_side DESC,
                perimeter DESC,
                rect_area DESC,
                a DESC,
                b DESC,
                c DESC,
                d DESC
            );
        CREATE INDEX IF NOT EXISTS idx_chain_cache_results_mode_square
            ON chain_cache_results(mode, square_ok, max_side DESC, a, b, c, d);

        CREATE TABLE IF NOT EXISTS chain_cache_runs (
            id                          INTEGER PRIMARY KEY AUTOINCREMENT,
            requested_max_val           INTEGER NOT NULL,
            result_mode                 TEXT    NOT NULL,
            require_square              INTEGER NOT NULL DEFAULT 0,
            status                      TEXT    NOT NULL DEFAULT 'running',
            started_at                  TEXT    NOT NULL,
            completed_at                TEXT,
            elapsed_s                   REAL    NOT NULL DEFAULT 0,
            starting_adjacency_max_val  INTEGER NOT NULL DEFAULT 0,
            starting_results_max_val    INTEGER NOT NULL DEFAULT 0,
            last_completed_a            INTEGER NOT NULL DEFAULT 0,
            new_adjacency_edges         INTEGER NOT NULL DEFAULT 0,
            new_results                 INTEGER NOT NULL DEFAULT 0,
            pre_filter_count            INTEGER NOT NULL DEFAULT 0,
            pre_filter_square_count     INTEGER NOT NULL DEFAULT 0,
            diagonal_sign_filtered      INTEGER NOT NULL DEFAULT 0,
            build_adjacency_s           REAL    NOT NULL DEFAULT 0,
            load_adjacency_s            REAL    NOT NULL DEFAULT 0,
            search_cycles_s             REAL    NOT NULL DEFAULT 0,
            query_results_s             REAL    NOT NULL DEFAULT 0
        );
        CREATE INDEX IF NOT EXISTS idx_chain_cache_runs_status
            ON chain_cache_runs(status, result_mode, requested_max_val, id DESC);
        """
    )
    conn.execute(
        """
        INSERT INTO chain_cache_meta (key, value)
        VALUES ('schema_version', ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """,
        (str(CHAIN_CACHE_SCHEMA_VERSION),),
    )
    conn.execute(
        """
        INSERT INTO chain_cache_state (id, adjacency_max_val)
        VALUES (1, 0)
        ON CONFLICT(id) DO NOTHING
        """
    )
    for result_mode in RESULT_MODES:
        conn.execute(
            """
            INSERT INTO chain_cache_result_state (
                mode,
                results_max_val,
                result_count,
                square_result_count,
                pre_filter_count,
                pre_filter_square_count
            )
            VALUES (?, 0, 0, 0, 0, 0)
            ON CONFLICT(mode) DO NOTHING
            """,
            (result_mode,),
        )
    conn.commit()


def get_adjacency_max_val(conn: sqlite3.Connection) -> int:
    """Return the adjacency cache high-water mark."""
    row = conn.execute(
        """
        SELECT adjacency_max_val
        FROM chain_cache_state
        WHERE id = 1
        """
    ).fetchone()
    if row is None:
        return 0
    return int(row["adjacency_max_val"])


def update_adjacency_max_val(conn: sqlite3.Connection, adjacency_max_val: int) -> None:
    """Persist one new adjacency cache high-water mark."""
    conn.execute(
        """
        UPDATE chain_cache_state
        SET adjacency_max_val = ?
        WHERE id = 1
        """,
        (int(adjacency_max_val),),
    )
    conn.commit()


def get_result_state(
    conn: sqlite3.Connection,
    *,
    result_mode: str = RESULT_MODE_DEFAULT,
) -> sqlite3.Row:
    """Return cached result-state metadata for one mode."""
    mode = _require_result_mode(result_mode)
    row = conn.execute(
        """
        SELECT mode, results_max_val, result_count, square_result_count,
               pre_filter_count, pre_filter_square_count
        FROM chain_cache_result_state
        WHERE mode = ?
        """,
        (mode,),
    ).fetchone()
    if row is None:
        raise ValueError(f"Missing chain_cache_result_state row for mode {mode!r}.")
    return row


def get_cache_state(
    conn: sqlite3.Connection,
    *,
    result_mode: str = RESULT_MODE_DEFAULT,
) -> tuple[int, int]:
    """Return `(adjacency_max_val, results_max_val)` for one result mode."""
    result_state = get_result_state(conn, result_mode=result_mode)
    return get_adjacency_max_val(conn), int(result_state["results_max_val"])


def update_cache_state(
    conn: sqlite3.Connection,
    *,
    adjacency_max_val: int | None = None,
    results_max_val: int | None = None,
    result_mode: str = RESULT_MODE_DEFAULT,
) -> None:
    """Backward-compatible helper that updates one or both cache high-water marks."""
    if adjacency_max_val is not None:
        update_adjacency_max_val(conn, adjacency_max_val)
    if results_max_val is not None:
        update_result_state(
            conn,
            result_mode=result_mode,
            results_max_val=results_max_val,
        )


def update_result_state(
    conn: sqlite3.Connection,
    *,
    result_mode: str = RESULT_MODE_DEFAULT,
    results_max_val: int | None = None,
    result_count: int | None = None,
    square_result_count: int | None = None,
    pre_filter_count: int | None = None,
    pre_filter_square_count: int | None = None,
) -> None:
    """Update cached result-state metadata for one mode."""
    row = get_result_state(conn, result_mode=result_mode)
    conn.execute(
        """
        UPDATE chain_cache_result_state
        SET results_max_val = ?,
            result_count = ?,
            square_result_count = ?,
            pre_filter_count = ?,
            pre_filter_square_count = ?
        WHERE mode = ?
        """,
        (
            int(row["results_max_val"]) if results_max_val is None else int(results_max_val),
            int(row["result_count"]) if result_count is None else int(result_count),
            int(row["square_result_count"])
            if square_result_count is None
            else int(square_result_count),
            int(row["pre_filter_count"]) if pre_filter_count is None else int(pre_filter_count),
            int(row["pre_filter_square_count"])
            if pre_filter_square_count is None
            else int(pre_filter_square_count),
            _require_result_mode(result_mode),
        ),
    )
    conn.commit()


def insert_adjacency_rows(
    conn: sqlite3.Connection,
    rows: list[tuple[int, int, int]],
) -> int:
    """Insert one batch of adjacency rows and return the number of new rows."""
    if not rows:
        return 0
    before = conn.total_changes
    conn.executemany(
        """
        INSERT OR IGNORE INTO chain_cache_adjacency (a, b, h)
        VALUES (?, ?, ?)
        """,
        rows,
    )
    conn.commit()
    return conn.total_changes - before


def load_cached_adjacency_rows(
    conn: sqlite3.Connection,
    max_val: int,
) -> list[tuple[int, int, int]]:
    """Load cached `(a, b, h)` rows up to one max value."""
    rows = conn.execute(
        """
        SELECT a, b, h
        FROM chain_cache_adjacency
        WHERE a <= ? AND b <= ?
        ORDER BY a ASC, b ASC
        """,
        (max_val, max_val),
    ).fetchall()
    return [(int(row["a"]), int(row["b"]), int(row["h"])) for row in rows]


def _result_payload(result_mode: str, result: ChainResult) -> tuple[int, ... | str]:
    rect_w, rect_h = result.rectangle
    return (
        _require_result_mode(result_mode),
        result.a,
        result.b,
        result.c,
        result.d,
        result.x1,
        result.x2,
        result.x3,
        result.x4,
        int(result.square_ok),
        max(result.a, result.b, result.c, result.d),
        result.a + result.b + result.c + result.d,
        rect_w,
        rect_h,
        rect_w * rect_h,
    )


def insert_results(
    conn: sqlite3.Connection,
    *,
    result_mode: str = RESULT_MODE_DEFAULT,
    results: list[ChainResult],
) -> int:
    """Insert one batch of cached results and return the new-row count."""
    if not results:
        return 0
    before = conn.total_changes
    conn.executemany(
        """
        INSERT OR IGNORE INTO chain_cache_results (
            mode, a, b, c, d, x1, x2, x3, x4, square_ok,
            max_side, perimeter, rect_w, rect_h, rect_area
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [_result_payload(result_mode, result) for result in results],
    )
    conn.commit()
    return conn.total_changes - before


def count_cached_results(
    conn: sqlite3.Connection,
    max_val: int,
    *,
    result_mode: str = RESULT_MODE_DEFAULT,
    require_square: bool = False,
) -> int:
    """Count cached results up to one max value."""
    mode = _require_result_mode(result_mode)
    if require_square:
        row = conn.execute(
            """
            SELECT COUNT(*) AS n
            FROM chain_cache_results
            WHERE mode = ? AND max_side <= ? AND square_ok = 1
            """,
            (mode, max_val),
        ).fetchone()
    else:
        row = conn.execute(
            """
            SELECT COUNT(*) AS n
            FROM chain_cache_results
            WHERE mode = ? AND max_side <= ?
            """,
            (mode, max_val),
        ).fetchone()
    return 0 if row is None else int(row["n"])


def load_cached_results(
    conn: sqlite3.Connection,
    max_val: int,
    *,
    result_mode: str = RESULT_MODE_DEFAULT,
    require_square: bool = False,
) -> list[ChainResult]:
    """Load cached results up to one max value."""
    mode = _require_result_mode(result_mode)
    if require_square:
        rows = conn.execute(
            """
            SELECT a, b, c, d, x1, x2, x3, x4, square_ok
            FROM chain_cache_results
            WHERE mode = ? AND max_side <= ? AND square_ok = 1
            ORDER BY a ASC, b ASC, c ASC, d ASC
            """,
            (mode, max_val),
        ).fetchall()
    else:
        rows = conn.execute(
            """
            SELECT a, b, c, d, x1, x2, x3, x4, square_ok
            FROM chain_cache_results
            WHERE mode = ? AND max_side <= ?
            ORDER BY a ASC, b ASC, c ASC, d ASC
            """,
            (mode, max_val),
        ).fetchall()
    return [
        ChainResult(
            a=int(row["a"]),
            b=int(row["b"]),
            c=int(row["c"]),
            d=int(row["d"]),
            x1=int(row["x1"]),
            x2=int(row["x2"]),
            x3=int(row["x3"]),
            x4=int(row["x4"]),
            square_ok=bool(row["square_ok"]),
        )
        for row in rows
    ]


def get_largest_cached_result(
    conn: sqlite3.Connection,
    max_val: int,
    *,
    result_mode: str = RESULT_MODE_DEFAULT,
) -> ChainResult | None:
    """Return the cached result with the largest side up to one max value."""
    row = conn.execute(
        """
        SELECT a, b, c, d, x1, x2, x3, x4, square_ok
        FROM chain_cache_results
        WHERE mode = ? AND max_side <= ?
        ORDER BY max_side DESC, perimeter DESC, rect_area DESC, a DESC, b DESC, c DESC, d DESC
        LIMIT 1
        """,
        (_require_result_mode(result_mode), max_val),
    ).fetchone()
    if row is None:
        return None
    return ChainResult(
        a=int(row["a"]),
        b=int(row["b"]),
        c=int(row["c"]),
        d=int(row["d"]),
        x1=int(row["x1"]),
        x2=int(row["x2"]),
        x3=int(row["x3"]),
        x4=int(row["x4"]),
        square_ok=bool(row["square_ok"]),
    )


def start_run(
    conn: sqlite3.Connection,
    *,
    requested_max_val: int,
    result_mode: str = RESULT_MODE_DEFAULT,
    require_square: bool,
    starting_adjacency_max_val: int,
    starting_results_max_val: int,
) -> int:
    """Insert a new cache run and return its id."""
    cur = conn.execute(
        """
        INSERT INTO chain_cache_runs (
            requested_max_val,
            result_mode,
            require_square,
            status,
            started_at,
            starting_adjacency_max_val,
            starting_results_max_val
        )
        VALUES (?, ?, ?, 'running', ?, ?, ?)
        """,
        (
            int(requested_max_val),
            _require_result_mode(result_mode),
            int(bool(require_square)),
            _utc_now(),
            int(starting_adjacency_max_val),
            int(starting_results_max_val),
        ),
    )
    conn.commit()
    return int(cur.lastrowid)


def get_resumable_run(
    conn: sqlite3.Connection,
    *,
    requested_max_val: int,
    result_mode: str = RESULT_MODE_DEFAULT,
) -> sqlite3.Row | None:
    """Return the latest incomplete run for one max value and result mode."""
    return conn.execute(
        """
        SELECT *
        FROM chain_cache_runs
        WHERE requested_max_val = ? AND result_mode = ? AND status = 'running'
        ORDER BY id DESC
        LIMIT 1
        """,
        (requested_max_val, _require_result_mode(result_mode)),
    ).fetchone()


def checkpoint_run(
    conn: sqlite3.Connection,
    run_id: int,
    last_completed_a: int,
    *,
    new_results: int | None = None,
    pre_filter_count: int | None = None,
    pre_filter_square_count: int | None = None,
    diagonal_sign_filtered: int | None = None,
) -> None:
    """Persist progress for one cache run."""
    row = get_run(conn, run_id)
    if row is None:
        raise ValueError(f"Unknown chain cache run id {run_id}.")
    conn.execute(
        """
        UPDATE chain_cache_runs
        SET last_completed_a = ?,
            new_results = ?,
            pre_filter_count = ?,
            pre_filter_square_count = ?,
            diagonal_sign_filtered = ?
        WHERE id = ?
        """,
        (
            int(last_completed_a),
            int(row["new_results"]) if new_results is None else int(new_results),
            int(row["pre_filter_count"]) if pre_filter_count is None else int(pre_filter_count),
            int(row["pre_filter_square_count"])
            if pre_filter_square_count is None
            else int(pre_filter_square_count),
            int(row["diagonal_sign_filtered"])
            if diagonal_sign_filtered is None
            else int(diagonal_sign_filtered),
            int(run_id),
        ),
    )
    conn.commit()


def finish_run(
    conn: sqlite3.Connection,
    run_id: int,
    *,
    elapsed_s: float,
    new_adjacency_edges: int,
    new_results: int,
    pre_filter_count: int,
    pre_filter_square_count: int,
    diagonal_sign_filtered: int,
    build_adjacency_s: float,
    load_adjacency_s: float,
    search_cycles_s: float,
    query_results_s: float,
) -> None:
    """Mark one cache run as completed and persist its metrics."""
    conn.execute(
        """
        UPDATE chain_cache_runs
        SET status = 'completed',
            completed_at = ?,
            elapsed_s = ?,
            new_adjacency_edges = ?,
            new_results = ?,
            pre_filter_count = ?,
            pre_filter_square_count = ?,
            diagonal_sign_filtered = ?,
            build_adjacency_s = ?,
            load_adjacency_s = ?,
            search_cycles_s = ?,
            query_results_s = ?
        WHERE id = ?
        """,
        (
            _utc_now(),
            float(elapsed_s),
            int(new_adjacency_edges),
            int(new_results),
            int(pre_filter_count),
            int(pre_filter_square_count),
            int(diagonal_sign_filtered),
            float(build_adjacency_s),
            float(load_adjacency_s),
            float(search_cycles_s),
            float(query_results_s),
            int(run_id),
        ),
    )
    conn.commit()


def get_run(conn: sqlite3.Connection, run_id: int) -> sqlite3.Row | None:
    """Return one cache run row by id."""
    return conn.execute(
        """
        SELECT *
        FROM chain_cache_runs
        WHERE id = ?
        """,
        (run_id,),
    ).fetchone()
