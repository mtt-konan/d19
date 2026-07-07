#!/usr/bin/env python3
"""Summarize rank-zero proof targets in the mixed-closure residual frontier."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This queue groups rank-zero residual covers by elliptic rank target. "
    "It records proof attempts, but does not prove rank zero."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _target_key(row: dict[str, Any]) -> tuple[int, int, str]:
    return int(row["A"]), int(row["B"]), str(row["curve"])


def _diagnostic_index(
    diagnostics: list[dict[str, Any]],
) -> dict[tuple[int, int, str], dict[str, Any]]:
    return {_target_key(row): row for row in diagnostics}


def _recheck_index(
    sage_rechecks: list[dict[str, Any]],
) -> dict[tuple[int, int, str], dict[str, Any]]:
    return {_target_key(row): row for row in sage_rechecks}


def _second_limits(recheck: dict[str, Any] | None) -> list[int]:
    limits = []
    for row in (recheck or {}).get("limits", []):
        if "second_limit" in row:
            limits.append(int(row["second_limit"]))
    return limits


def _optional_int(recheck: dict[str, Any] | None, key: str) -> int | None:
    if recheck is None or recheck.get(key) is None:
        return None
    return int(recheck[key])


def _optional_float(recheck: dict[str, Any] | None, key: str) -> float | None:
    if recheck is None or recheck.get(key) is None:
        return None
    return float(recheck[key])


def _queue_status(recheck: dict[str, Any] | None) -> str:
    if recheck is None:
        return "not-retried"
    if recheck.get("status") == "ok" and recheck.get("final_rank_bounds") == [0, 0]:
        return "rank-zero-proved"
    if recheck.get("status") == "timeout":
        return "sage-timeout"
    if recheck.get("status") == "ok":
        return "sage-open"
    return "sage-error"


def _next_step(status: str) -> str:
    if status == "rank-zero-proved":
        return "rerun torsion-preimage audit under the new strict rank-zero proof"
    if status == "not-retried":
        return "run Sage rank recheck with higher descent limits"
    return "retry rank proof with stronger descent tooling or external CAS"


def build_rank_zero_frontier_queue(
    *,
    open_frontier_audit: dict[str, Any],
    diagnostics: list[dict[str, Any]],
    sage_rechecks: list[dict[str, Any]],
) -> dict[str, Any]:
    diagnostics_by_key = _diagnostic_index(diagnostics)
    rechecks_by_key = _recheck_index(sage_rechecks)
    grouped: dict[tuple[int, int, str], list[dict[str, Any]]] = {}

    for row in open_frontier_audit.get("rows", []):
        if row.get("frontier_type") != "rank-zero-needs-rank-proof":
            continue
        grouped.setdefault(_target_key(row), []).append(row)

    targets: list[dict[str, Any]] = []
    for key, rows in sorted(
        grouped.items(), key=lambda item: min(int(row["priority"]) for row in item[1])
    ):
        diagnostic = diagnostics_by_key.get(key, {})
        recheck = rechecks_by_key.get(key)
        status = _queue_status(recheck)
        targets.append(
            {
                "A": key[0],
                "B": key[1],
                "curve": key[2],
                "priorities": sorted(int(row["priority"]) for row in rows),
                "cover_indices": sorted(int(row["cover_index"]) for row in rows),
                "cover_count": len(rows),
                "diagnostic_status": str(diagnostic.get("status", "missing")),
                "model": [int(value) for value in diagnostic.get("model", [])],
                "rank_bounds": [
                    int(value) for value in diagnostic.get("rank_bounds", [])
                ],
                "rank_plus_sha2_dimension": int(
                    diagnostic.get("rank_plus_sha2_dimension", 0)
                ),
                "root_number": int(diagnostic.get("root_number", 0)),
                "conductor": int(diagnostic.get("conductor", 0)),
                "torsion_two_dimension": int(
                    diagnostic.get("torsion_two_dimension", 0)
                ),
                "sage_recheck_status": None if recheck is None else recheck.get("status"),
                "sage_recheck_final_rank_bounds": None
                if recheck is None
                else recheck.get("final_rank_bounds"),
                "sage_recheck_second_limits": _second_limits(recheck),
                "sage_recheck_timeout_seconds": _optional_int(
                    recheck, "timeout_seconds"
                ),
                "sage_recheck_elapsed_seconds": _optional_float(
                    recheck, "elapsed_seconds"
                ),
                "rank_proof_queue_status": status,
                "next_step": _next_step(status),
                "candidate_not_proof": True,
            }
        )

    status_counts = dict(
        sorted(Counter(str(target["rank_proof_queue_status"]) for target in targets).items())
    )
    return {
        "status": "ok",
        "rank_zero_frontier_cover_count": sum(
            int(target["cover_count"]) for target in targets
        ),
        "rank_zero_frontier_target_count": len(targets),
        "closed_rank_zero_target_count": status_counts.get("rank-zero-proved", 0),
        "target_status_counts": status_counts,
        "targets": targets,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--open-frontier-audit", type=Path, required=True)
    parser.add_argument("--diagnostics", type=Path, required=True)
    parser.add_argument("--sage-recheck", type=Path, action="append", default=[])
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sage_rechecks: list[dict[str, Any]] = []
    for path in args.sage_recheck:
        sage_rechecks.extend(load_jsonl(path))
    queue = build_rank_zero_frontier_queue(
        open_frontier_audit=load_json(args.open_frontier_audit),
        diagnostics=load_jsonl(args.diagnostics),
        sage_rechecks=sage_rechecks,
    )
    write_json(args.out, queue)
    print(f"wrote rank-zero frontier queue to {args.out}")
    print(
        "rank_zero_frontier_cover_count="
        f"{queue['rank_zero_frontier_cover_count']}"
    )
    print(
        "rank_zero_frontier_target_count="
        f"{queue['rank_zero_frontier_target_count']}"
    )
    print(f"closed_rank_zero_target_count={queue['closed_rank_zero_target_count']}")
    if args.strict and queue["closed_rank_zero_target_count"] != 0:
        print("strict rank-zero targets were found; rerun downstream strict audits")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
