"""SQLite persistence for EC search runs and provenance graphs."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path

from rational_distance._legacy.search_ec import ECTripleTrace
from rational_distance._legacy.square import RationalPoint


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _fraction_or_none(value: str | None) -> Fraction | None:
    return Fraction(value) if value is not None else None


def _region_for_xy(x: Fraction, y: Fraction) -> str:
    if x in {Fraction(0), Fraction(1)} or y in {Fraction(0), Fraction(1)}:
        return "boundary"
    if Fraction(0) < x < Fraction(1) and Fraction(0) < y < Fraction(1):
        return "inside"
    return "outside"


def _missing_vertex(point: RationalPoint) -> str:
    for name, dist in zip(("A", "B", "C", "D"), point.distances, strict=True):
        if dist is None:
            return name
    return "none"


def _canonical_key(x: Fraction, y: Fraction) -> str:
    return f"{x}|{y}"


def connect_db(path: str | Path) -> sqlite3.Connection:
    db_path = Path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            method TEXT NOT NULL,
            params_key TEXT NOT NULL,
            params_json TEXT NOT NULL,
            backend TEXT NOT NULL,
            status TEXT NOT NULL,
            started_at TEXT NOT NULL,
            completed_at TEXT,
            elapsed_seconds REAL NOT NULL DEFAULT 0
        );
        CREATE INDEX IF NOT EXISTS idx_runs_method_params
            ON runs(method, params_key, id DESC);

        CREATE TABLE IF NOT EXISTS ec_triples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
            triple_index INTEGER NOT NULL,
            p INTEGER NOT NULL,
            q INTEGER NOT NULL,
            r INTEGER NOT NULL,
            status TEXT NOT NULL,
            seed_count INTEGER NOT NULL DEFAULT 0,
            point_count INTEGER NOT NULL DEFAULT 0,
            node_count INTEGER NOT NULL DEFAULT 0,
            processed_at TEXT,
            UNIQUE(run_id, p, q, r)
        );

        CREATE TABLE IF NOT EXISTS ec_seeds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            triple_id INTEGER NOT NULL REFERENCES ec_triples(id) ON DELETE CASCADE,
            seed_index INTEGER NOT NULL,
            a INTEGER NOT NULL,
            b INTEGER NOT NULL,
            k TEXT NOT NULL,
            dB TEXT NOT NULL,
            dD TEXT NOT NULL,
            x TEXT NOT NULL,
            y TEXT NOT NULL,
            region TEXT NOT NULL,
            UNIQUE(triple_id, seed_index)
        );

        CREATE TABLE IF NOT EXISTS ec_curve_nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            triple_id INTEGER NOT NULL REFERENCES ec_triples(id) ON DELETE CASCADE,
            node_index INTEGER NOT NULL,
            t TEXT NOT NULL,
            e TEXT NOT NULL,
            kind TEXT NOT NULL,
            step INTEGER NOT NULL,
            seed_id INTEGER REFERENCES ec_seeds(id) ON DELETE SET NULL,
            is_active INTEGER NOT NULL DEFAULT 0,
            UNIQUE(triple_id, node_index),
            UNIQUE(triple_id, t, e)
        );

        CREATE TABLE IF NOT EXISTS ec_curve_edges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            triple_id INTEGER NOT NULL REFERENCES ec_triples(id) ON DELETE CASCADE,
            child_node_id INTEGER NOT NULL REFERENCES ec_curve_nodes(id) ON DELETE CASCADE,
            parent_node_id INTEGER NOT NULL REFERENCES ec_curve_nodes(id) ON DELETE CASCADE,
            relation TEXT NOT NULL,
            position INTEGER NOT NULL DEFAULT 0,
            UNIQUE(triple_id, child_node_id, parent_node_id, relation, position)
        );

        CREATE TABLE IF NOT EXISTS ec_points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
            triple_id INTEGER NOT NULL REFERENCES ec_triples(id) ON DELETE CASCADE,
            source_kind TEXT NOT NULL,
            source_seed_id INTEGER REFERENCES ec_seeds(id) ON DELETE SET NULL,
            source_node_id INTEGER REFERENCES ec_curve_nodes(id) ON DELETE SET NULL,
            x TEXT NOT NULL,
            y TEXT NOT NULL,
            dA TEXT,
            dB TEXT,
            dC TEXT,
            dD TEXT,
            missing_vertex TEXT NOT NULL,
            rational_count INTEGER NOT NULL,
            denominator INTEGER NOT NULL,
            region TEXT NOT NULL,
            canonical_x TEXT NOT NULL,
            canonical_y TEXT NOT NULL,
            canonical_key TEXT NOT NULL,
            UNIQUE(run_id, canonical_key)
        );
        CREATE INDEX IF NOT EXISTS idx_ec_points_run_triple
            ON ec_points(run_id, triple_id);

        CREATE TABLE IF NOT EXISTS ec_point_candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            triple_id INTEGER NOT NULL REFERENCES ec_triples(id) ON DELETE CASCADE,
            candidate_index INTEGER NOT NULL,
            source_kind TEXT NOT NULL,
            source_seed_id INTEGER REFERENCES ec_seeds(id) ON DELETE SET NULL,
            source_node_id INTEGER REFERENCES ec_curve_nodes(id) ON DELETE SET NULL,
            k TEXT,
            status TEXT NOT NULL,
            x TEXT,
            y TEXT,
            rational_count INTEGER,
            missing_vertex TEXT,
            denominator INTEGER,
            region TEXT,
            canonical_x TEXT,
            canonical_y TEXT,
            point_id INTEGER REFERENCES ec_points(id) ON DELETE SET NULL,
            UNIQUE(triple_id, candidate_index)
        );
        """
    )


def params_key_for_ec(params: dict) -> str:
    normalized = {
        "inside": bool(params["inside"]),
        "max_k_den": int(params["max_k_den"]),
        "max_k_num": int(params["max_k_num"]),
        "max_m": int(params["max_m"]),
        "max_steps": int(params["max_steps"]),
        "min_rational": int(params["min_rational"]),
    }
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"))


def resolve_run_row(
    conn: sqlite3.Connection,
    selector: str | int,
    method: str = "ec",
) -> sqlite3.Row:
    if selector == "latest":
        row = conn.execute(
            "SELECT * FROM runs WHERE method = ? ORDER BY id DESC LIMIT 1",
            (method,),
        ).fetchone()
    else:
        row = conn.execute(
            "SELECT * FROM runs WHERE id = ? AND method = ?",
            (int(selector), method),
        ).fetchone()
    if row is None:
        raise ValueError(f"No {method} run found for selector {selector!r}")
    return row


@dataclass
class ECSearchStore:
    """Persist EC search results into SQLite and support resume."""

    path: Path
    params: dict
    backend: str
    resume: bool = False

    def __post_init__(self) -> None:
        self.path = Path(self.path)
        self.conn = connect_db(self.path)
        init_schema(self.conn)
        self.params_key = params_key_for_ec(self.params)
        self.run_id = self._resolve_run()
        self._canonical_to_point_id: dict[str, int] = {}
        self._existing_points = self._load_existing_points()
        self.processed_triples = self._load_processed_triples()

    def _resolve_run(self) -> int:
        if self.resume:
            row = self.conn.execute(
                "SELECT id FROM runs WHERE method = ? AND params_key = ? ORDER BY id DESC LIMIT 1",
                ("ec", self.params_key),
            ).fetchone()
            if row is not None:
                self.conn.execute(
                    "UPDATE runs SET backend = ?, status = ? WHERE id = ?",
                    (self.backend, "running", row["id"]),
                )
                self.conn.commit()
                return int(row["id"])

        cur = self.conn.execute(
            """
            INSERT INTO runs (method, params_key, params_json, backend, status, started_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "ec",
                self.params_key,
                json.dumps(self.params, sort_keys=True),
                self.backend,
                "running",
                _utc_now(),
            ),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def _load_existing_points(self) -> list[RationalPoint]:
        rows = self.conn.execute(
            """
            SELECT id, x, y, dA, dB, dC, dD, canonical_key
            FROM ec_points
            WHERE run_id = ?
            ORDER BY id
            """,
            (self.run_id,),
        ).fetchall()
        points: list[RationalPoint] = []
        for row in rows:
            self._canonical_to_point_id[row["canonical_key"]] = int(row["id"])
            points.append(
                RationalPoint(
                    x=Fraction(row["x"]),
                    y=Fraction(row["y"]),
                    distances=tuple(_fraction_or_none(row[f"d{name}"]) for name in "ABCD"),
                )
            )
        return points

    def _load_processed_triples(self) -> set[tuple[int, int, int]]:
        rows = self.conn.execute(
            "SELECT p, q, r FROM ec_triples WHERE run_id = ? AND status = ?",
            (self.run_id, "completed"),
        ).fetchall()
        return {(int(row["p"]), int(row["q"]), int(row["r"])) for row in rows}

    def existing_points(self) -> list[RationalPoint]:
        return list(self._existing_points)

    def record_triple(self, triple_index: int, trace: ECTripleTrace) -> None:
        accepted_points = trace.accepted_points()
        with self.conn:
            cur = self.conn.execute(
                """
                INSERT INTO ec_triples (
                    run_id, triple_index, p, q, r, status, seed_count,
                    point_count, node_count, processed_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.run_id,
                    triple_index,
                    trace.p,
                    trace.q,
                    trace.r,
                    "completed",
                    len(trace.seeds),
                    len(accepted_points),
                    len(trace.nodes),
                    _utc_now(),
                ),
            )
            triple_id = int(cur.lastrowid)

            seed_ids: dict[int, int] = {}
            for seed in trace.seeds:
                x = seed.k * Fraction(trace.p, trace.r)
                y = seed.k * Fraction(trace.q, trace.r)
                cur = self.conn.execute(
                    """
                    INSERT INTO ec_seeds (triple_id, seed_index, a, b, k, dB, dD, x, y, region)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        triple_id,
                        seed.seed_index,
                        seed.a,
                        seed.b,
                        str(seed.k),
                        str(seed.dB),
                        str(seed.dD),
                        str(x),
                        str(y),
                        _region_for_xy(x, y),
                    ),
                )
                seed_ids[seed.seed_index] = int(cur.lastrowid)

            node_ids: dict[int, int] = {}
            for node in trace.nodes:
                cur = self.conn.execute(
                    """
                    INSERT INTO ec_curve_nodes (
                        triple_id, node_index, t, e, kind, step, seed_id, is_active
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        triple_id,
                        node.node_index,
                        str(node.t),
                        str(node.E),
                        node.kind,
                        node.step,
                        seed_ids.get(node.seed_index),
                        1 if node.active else 0,
                    ),
                )
                node_ids[node.node_index] = int(cur.lastrowid)

            for edge in trace.edges:
                self.conn.execute(
                    """
                    INSERT INTO ec_curve_edges (
                        triple_id, child_node_id, parent_node_id, relation, position
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        triple_id,
                        node_ids[edge.child_index],
                        node_ids[edge.parent_index],
                        edge.relation,
                        edge.position,
                    ),
                )

            for candidate in trace.candidates:
                point_id = None
                if candidate.canonical_xy is not None:
                    canonical_key = _canonical_key(*candidate.canonical_xy)
                    point_id = self._canonical_to_point_id.get(canonical_key)
                else:
                    canonical_key = None

                if (
                    candidate.status == "accepted"
                    and candidate.point is not None
                    and canonical_key is not None
                ):
                    point = candidate.point
                    point_cur = self.conn.execute(
                        """
                        INSERT INTO ec_points (
                            run_id, triple_id, source_kind, source_seed_id, source_node_id,
                            x, y, dA, dB, dC, dD, missing_vertex, rational_count, denominator,
                            region, canonical_x, canonical_y, canonical_key
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            self.run_id,
                            triple_id,
                            candidate.source_kind,
                            seed_ids.get(candidate.source_seed_index),
                            node_ids.get(candidate.source_node_index),
                            str(point.x),
                            str(point.y),
                            str(point.distances[0]) if point.distances[0] is not None else None,
                            str(point.distances[1]) if point.distances[1] is not None else None,
                            str(point.distances[2]) if point.distances[2] is not None else None,
                            str(point.distances[3]) if point.distances[3] is not None else None,
                            _missing_vertex(point),
                            point.rational_count,
                            point.denominator,
                            _region_for_xy(point.x, point.y),
                            str(candidate.canonical_xy[0]),
                            str(candidate.canonical_xy[1]),
                            canonical_key,
                        ),
                    )
                    point_id = int(point_cur.lastrowid)
                    self._canonical_to_point_id[canonical_key] = point_id

                point = candidate.point
                self.conn.execute(
                    """
                    INSERT INTO ec_point_candidates (
                        triple_id, candidate_index, source_kind, source_seed_id, source_node_id,
                        k, status, x, y, rational_count, missing_vertex, denominator, region,
                        canonical_x, canonical_y, point_id
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        triple_id,
                        candidate.candidate_index,
                        candidate.source_kind,
                        seed_ids.get(candidate.source_seed_index),
                        node_ids.get(candidate.source_node_index),
                        str(candidate.k) if candidate.k is not None else None,
                        candidate.status,
                        str(candidate.x) if candidate.x is not None else None,
                        str(candidate.y) if candidate.y is not None else None,
                        point.rational_count if point is not None else None,
                        _missing_vertex(point) if point is not None else None,
                        point.denominator if point is not None else None,
                        _region_for_xy(candidate.x, candidate.y)
                        if candidate.x is not None and candidate.y is not None
                        else None,
                        (
                            str(candidate.canonical_xy[0])
                            if candidate.canonical_xy is not None
                            else None
                        ),
                        (
                            str(candidate.canonical_xy[1])
                            if candidate.canonical_xy is not None
                            else None
                        ),
                        point_id,
                    ),
                )

        self.processed_triples.add((trace.p, trace.q, trace.r))
        self._existing_points.extend(accepted_points)

    def finish(self, elapsed_seconds: float) -> None:
        with self.conn:
            self.conn.execute(
                """
                UPDATE runs
                SET backend = ?, status = ?, completed_at = ?,
                    elapsed_seconds = elapsed_seconds + ?
                WHERE id = ?
                """,
                (self.backend, "completed", _utc_now(), elapsed_seconds, self.run_id),
            )

    def close(self) -> None:
        self.conn.close()
