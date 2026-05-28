"""Analysis helpers for persisted chain-fast runs."""

from __future__ import annotations

import json
from pathlib import Path

from rational_distance._legacy.chain_db import connect_db, get_bucket_stats, init_schema

_BUCKET_TYPES = ("g_bucket", "delta_bucket", "residue_bucket")


def _resolve_run_row(conn, run_selector: str | int):
    if run_selector == "latest":
        row = conn.execute(
            """
            SELECT *
            FROM chain_runs
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()
    else:
        row = conn.execute(
            """
            SELECT *
            FROM chain_runs
            WHERE id = ?
            """,
            (int(run_selector),),
        ).fetchone()
    if row is None:
        raise ValueError("No matching chain-fast run found in the database.")
    return row


def _selected_bucket_types(bucket_type: str) -> list[str]:
    if bucket_type == "all":
        return list(_BUCKET_TYPES)
    if bucket_type not in _BUCKET_TYPES:
        raise ValueError(f"Unsupported bucket type: {bucket_type}")
    return [bucket_type]


def _rate(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return numerator / denominator


def _sample_payload(row: dict) -> dict | None:
    if row["sample_a"] is None:
        return None
    return {
        "a": int(row["sample_a"]),
        "b": int(row["sample_b"]),
        "c": int(row["sample_c"]),
        "d": int(row["sample_d"]),
        "sq3_deficit": int(row["sample_sq3_deficit"]),
        "sq4_deficit": int(row["sample_sq4_deficit"]),
    }


def _ranked_bucket_payload(row: dict) -> dict:
    n_after_basic = int(row["n_after_basic"])
    n_c3_pass = int(row["n_c3_pass"])
    n_near_miss = int(row["n_near_miss"])
    return {
        "bucket_type": str(row["bucket_type"]),
        "bucket_key": json.loads(row["bucket_key_json"]),
        "bucket_key_json": str(row["bucket_key_json"]),
        "n_total": int(row["n_total"]),
        "n_after_basic": n_after_basic,
        "n_c3_pass": n_c3_pass,
        "n_c4_pass": int(row["n_c4_pass"]),
        "n_near_miss": n_near_miss,
        "c3_rate": _rate(n_c3_pass, n_after_basic),
        "near_miss_rate": _rate(n_near_miss, n_after_basic),
        "best_sq4_deficit": row["best_sq4_deficit"],
        "best_sq3_deficit": row["best_sq3_deficit"],
        "best_sample": _sample_payload(row),
    }


def _bucket_type_summary(rows: list[dict]) -> dict:
    return {
        "row_count": len(rows),
        "n_total": sum(int(row["n_total"]) for row in rows),
        "n_after_basic": sum(int(row["n_after_basic"]) for row in rows),
        "n_c3_pass": sum(int(row["n_c3_pass"]) for row in rows),
        "n_c4_pass": sum(int(row["n_c4_pass"]) for row in rows),
        "n_near_miss": sum(int(row["n_near_miss"]) for row in rows),
    }


def build_chain_analysis_report(
    db_path: str | Path,
    run_selector: str | int = "latest",
    bucket_type: str = "all",
    top: int = 20,
    min_after_basic: int = 1000,
) -> dict:
    conn = connect_db(db_path)
    try:
        init_schema(conn)
        run = _resolve_run_row(conn, run_selector)
        params = json.loads(run["params_json"])
        selected_types = _selected_bucket_types(bucket_type)
        rows = get_bucket_stats(conn, int(run["id"]))
        rows_by_type = {
            name: [row for row in rows if row["bucket_type"] == name]
            for name in selected_types
        }

        summaries = {
            name: _bucket_type_summary(type_rows)
            for name, type_rows in rows_by_type.items()
        }
        rankings: dict[str, dict[str, list[dict]]] = {}
        for name, type_rows in rows_by_type.items():
            qualified = [
                row for row in type_rows if int(row["n_after_basic"]) >= int(min_after_basic)
            ]
            top_n = max(0, int(top))
            rankings[name] = {
                "top_c3_rate": [
                    _ranked_bucket_payload(row)
                    for row in sorted(
                        qualified,
                        key=lambda row: (
                            -_rate(int(row["n_c3_pass"]), int(row["n_after_basic"])),
                            -int(row["n_after_basic"]),
                            str(row["bucket_key_json"]),
                        ),
                    )[:top_n]
                ],
                "top_near_miss_rate": [
                    _ranked_bucket_payload(row)
                    for row in sorted(
                        qualified,
                        key=lambda row: (
                            -_rate(int(row["n_near_miss"]), int(row["n_after_basic"])),
                            -int(row["n_after_basic"]),
                            str(row["bucket_key_json"]),
                        ),
                    )[:top_n]
                ],
                "closest_sq4_near_miss": [
                    _ranked_bucket_payload(row)
                    for row in sorted(
                        [
                            row
                            for row in qualified
                            if row["best_sq4_deficit"] is not None and int(row["n_near_miss"]) > 0
                        ],
                        key=lambda row: (
                            int(row["best_sq4_deficit"]),
                            int(row["best_sq3_deficit"]),
                            -int(row["n_after_basic"]),
                            str(row["bucket_key_json"]),
                        ),
                    )[:top_n]
                ],
            }

        return {
            "run": {
                "id": int(run["id"]),
                "status": str(run["status"]),
                "backend": str(run["backend"]),
                "bucket_stats": bool(run["bucket_stats"]),
                "started_at": run["started_at"],
                "completed_at": run["completed_at"],
                "elapsed_s": float(run["elapsed_s"]),
                "params": params,
            },
            "filters": {
                "bucket_type": bucket_type,
                "top": int(top),
                "min_after_basic": int(min_after_basic),
            },
            "summary": {
                "selected_bucket_types": selected_types,
                "bucket_type_summaries": summaries,
            },
            "rankings": rankings,
        }
    finally:
        conn.close()
