"""Analysis helpers for persisted EC search runs."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from statistics import median

from rational_distance._legacy.ec_db import connect_db, resolve_run_row


def parse_triple_arg(text: str) -> tuple[int, int, int]:
    parts = [part.strip() for part in text.split(",")]
    if len(parts) != 3:
        raise ValueError("--triple must look like p,q,r")
    return tuple(int(part) for part in parts)  # type: ignore[return-value]


def _number_stats(values: list[int]) -> dict:
    if not values:
        return {"count": 0, "min": None, "median": None, "max": None}
    return {
        "count": len(values),
        "min": min(values),
        "median": int(median(values)),
        "max": max(values),
    }


def _resolve_descendant_node_ids(conn, seed_id: int) -> set[int]:
    rows = conn.execute(
        """
        WITH RECURSIVE descendants(node_id) AS (
            SELECT id FROM ec_curve_nodes WHERE seed_id = ?
            UNION
            SELECT e.child_node_id
            FROM ec_curve_edges e
            JOIN descendants d ON e.parent_node_id = d.node_id
        )
        SELECT node_id FROM descendants
        """,
        (seed_id,),
    ).fetchall()
    return {int(row["node_id"]) for row in rows}


def _node_source_classes(conn, triple_ids: list[int]) -> dict[int, str]:
    if not triple_ids:
        return {}
    placeholders = ",".join("?" for _ in triple_ids)
    rows = conn.execute(
        f"""
        SELECT child_node_id, relation
        FROM ec_curve_edges
        WHERE triple_id IN ({placeholders})
        """,
        tuple(triple_ids),
    ).fetchall()
    relations_by_node: dict[int, set[str]] = defaultdict(set)
    for row in rows:
        relations_by_node[int(row["child_node_id"])].add(row["relation"])

    classes: dict[int, str] = {}
    for node_id, relations in relations_by_node.items():
        if relations == {"tangent"}:
            classes[node_id] = "tangent"
        elif relations == {"secant"}:
            classes[node_id] = "secant"
        elif relations == {"secant_neg_branch"}:
            classes[node_id] = "secant_neg_branch"
        else:
            classes[node_id] = "mixed"
    return classes


def _point_payload(row) -> dict:
    def _float_or_none(value: str | None) -> float | None:
        return float(Fraction(value)) if value is not None else None

    return {
        "x": float(Fraction(row["x"])),
        "y": float(Fraction(row["y"])),
        "x_str": row["x"],
        "y_str": row["y"],
        "dA": _float_or_none(row["dA"]),
        "dB": _float_or_none(row["dB"]),
        "dC": _float_or_none(row["dC"]),
        "dD": _float_or_none(row["dD"]),
        "dA_str": row["dA"] or "?",
        "dB_str": row["dB"] or "?",
        "dC_str": row["dC"] or "?",
        "dD_str": row["dD"] or "?",
        "missing": row["missing_vertex"],
        "rational_count": int(row["rational_count"]),
        "denominator": int(row["denominator"]),
        "inside": row["region"] == "inside",
    }


def build_analysis_report(
    db_path: str | Path,
    run_selector: str | int = "latest",
    triple: tuple[int, int, int] | None = None,
    seed_id: int | None = None,
    region: str = "all",
) -> dict:
    conn = connect_db(db_path)
    try:
        run = resolve_run_row(conn, run_selector, method="ec")
        params = json.loads(run["params_json"])

        triple_ids: list[int]
        triple_filter = ""
        triple_args: tuple = ()
        if triple is not None:
            triple_row = conn.execute(
                """
                SELECT id, p, q, r
                FROM ec_triples
                WHERE run_id = ? AND p = ? AND q = ? AND r = ?
                """,
                (run["id"], *triple),
            ).fetchone()
            triple_ids = [] if triple_row is None else [int(triple_row["id"])]
            triple_filter = " AND p.id = ?"
            triple_args = (triple_ids[0],) if triple_ids else ()
        elif seed_id is not None:
            seed_row = conn.execute(
                """
                SELECT s.id, s.triple_id
                FROM ec_seeds s
                JOIN ec_triples t ON t.id = s.triple_id
                WHERE s.id = ? AND t.run_id = ?
                """,
                (seed_id, run["id"]),
            ).fetchone()
            triple_ids = [] if seed_row is None else [int(seed_row["triple_id"])]
            triple_filter = " AND p.id = ?"
            triple_args = (triple_ids[0],) if triple_ids else ()
        else:
            triple_rows = conn.execute(
                "SELECT id FROM ec_triples WHERE run_id = ? ORDER BY triple_index",
                (run["id"],),
            ).fetchall()
            triple_ids = [int(row["id"]) for row in triple_rows]

        descendant_nodes = (
            _resolve_descendant_node_ids(conn, seed_id) if seed_id is not None else set()
        )
        point_query = [
            """
            SELECT
                p.*,
                t.p AS triple_p,
                t.q AS triple_q,
                t.r AS triple_r
            FROM ec_points p
            JOIN ec_triples t ON t.id = p.triple_id
            WHERE p.run_id = ?
            """
        ]
        point_args: list = [run["id"]]
        if triple_filter:
            point_query.append(triple_filter)
            point_args.extend(triple_args)
        if seed_id is not None:
            point_query.append(
                " AND (p.source_seed_id = ? OR p.source_node_id IN ({nodes}))".format(
                    nodes=",".join("?" for _ in descendant_nodes) or "NULL"
                )
            )
            point_args.append(seed_id)
            point_args.extend(sorted(descendant_nodes))
        if region in {"inside", "outside"}:
            point_query.append(" AND p.region = ?")
            point_args.append(region)
        point_query.append(" ORDER BY p.id")
        point_rows = conn.execute("".join(point_query), tuple(point_args)).fetchall()

        triple_rows = conn.execute(
            """
            SELECT
                t.id,
                t.p,
                t.q,
                t.r,
                t.seed_count,
                t.point_count,
                SUM(CASE WHEN p.region = 'inside' THEN 1 ELSE 0 END) AS inside_points,
                SUM(CASE WHEN p.region = 'outside' THEN 1 ELSE 0 END) AS outside_points
            FROM ec_triples t
            LEFT JOIN ec_points p ON p.triple_id = t.id
            WHERE t.run_id = ?
            GROUP BY t.id
            ORDER BY t.point_count DESC, t.seed_count DESC, t.r ASC
            """,
            (run["id"],),
        ).fetchall()

        triple_id_set = set(triple_ids)
        relevant_triples = [
            row for row in triple_rows if not triple_id_set or int(row["id"]) in triple_id_set
        ]
        node_classes = _node_source_classes(conn, [int(row["id"]) for row in relevant_triples])

        missing_counts = Counter(str(row["missing_vertex"]) for row in point_rows)
        source_counts = Counter()
        for row in point_rows:
            if row["source_kind"] == "seed":
                source_counts["seed"] += 1
            else:
                source_counts[node_classes.get(int(row["source_node_id"]), "orbit")] += 1

        slope_summary = []
        for row in relevant_triples:
            slope_summary.append(
                {
                    "triple": [int(row["p"]), int(row["q"]), int(row["r"])],
                    "slope": f"{row['q']}/{row['p']}",
                    "seed_count": int(row["seed_count"]),
                    "point_count": int(row["point_count"]),
                    "inside_points": int(row["inside_points"] or 0),
                    "outside_points": int(row["outside_points"] or 0),
                }
            )

        seed_rows = conn.execute(
            """
            SELECT k
            FROM ec_seeds
            WHERE triple_id IN ({placeholders})
            ORDER BY id
            """.format(placeholders=",".join("?" for _ in relevant_triples) or "NULL"),
            tuple(int(row["id"]) for row in relevant_triples),
        ).fetchall()
        seed_k_dens = [Fraction(row["k"]).denominator for row in seed_rows]
        point_dens = [int(row["denominator"]) for row in point_rows]

        payload = {
            "params": {
                **params,
                "analysis_run": int(run["id"]),
                "region": region,
                "seed_id": seed_id,
                "triple": list(triple) if triple is not None else None,
            },
            "elapsed": float(run["elapsed_seconds"]),
            "points": [_point_payload(row) for row in point_rows],
        }

        outside_only = [
            {
                "triple": [int(row["p"]), int(row["q"]), int(row["r"])],
                "seed_count": int(row["seed_count"]),
                "point_count": int(row["point_count"]),
            }
            for row in relevant_triples
            if int(row["outside_points"] or 0) > 0 and int(row["inside_points"] or 0) == 0
        ]

        return {
            "run": {
                "id": int(run["id"]),
                "status": run["status"],
                "backend": run["backend"],
                "started_at": run["started_at"],
                "completed_at": run["completed_at"],
                "elapsed_seconds": float(run["elapsed_seconds"]),
                "params": params,
            },
            "filters": {
                "triple": list(triple) if triple is not None else None,
                "seed_id": seed_id,
                "region": region,
            },
            "summary": {
                "point_count": len(point_rows),
                "triple_count": len(relevant_triples),
                "seed_count": len(seed_rows),
                "missing_vertex_counts": dict(missing_counts),
                "source_counts": dict(source_counts),
                "seed_k_denominators": _number_stats(seed_k_dens),
                "point_denominators": _number_stats(point_dens),
            },
            "top_triples_by_seeds": sorted(
                slope_summary,
                key=lambda item: (-item["seed_count"], -item["point_count"], item["triple"][2]),
            )[:10],
            "top_triples_by_points": sorted(
                slope_summary,
                key=lambda item: (-item["point_count"], -item["seed_count"], item["triple"][2]),
            )[:10],
            "outside_only_triples": outside_only[:10],
            "slope_summary": slope_summary[:10],
            "visualize_payload": payload,
        }
    finally:
        conn.close()
