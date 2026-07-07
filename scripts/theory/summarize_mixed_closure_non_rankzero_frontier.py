#!/usr/bin/env python3
"""Summarize non-rank-zero proof targets in the mixed-closure residual frontier."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This queue groups the non-rank-zero residual frontier by elliptic "
    "target. It is a proof-work queue, not a no-point certificate."
)

NEXT_STEPS = {
    "rank1-needs-visible-generator-or-descent": (
        "find a visible rank-one generator and isolate the residual Sha[2] class"
    ),
    "even-rank-gap4-needs-deeper-descent": (
        "run deeper descent or produce an independent Sha[2] obstruction"
    ),
}

QUEUE_STATUSES = {
    "rank1-needs-visible-generator-or-descent": "rank1-open",
    "even-rank-gap4-needs-deeper-descent": "even-gap4-open",
}


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


def build_non_rankzero_frontier_queue(
    *,
    open_frontier_audit: dict[str, Any],
    diagnostics: list[dict[str, Any]],
) -> dict[str, Any]:
    diagnostics_by_key = _diagnostic_index(diagnostics)
    grouped: dict[tuple[int, int, str], list[dict[str, Any]]] = {}

    for row in open_frontier_audit.get("rows", []):
        if row.get("frontier_type") not in NEXT_STEPS:
            continue
        grouped.setdefault(_target_key(row), []).append(row)

    targets: list[dict[str, Any]] = []
    for key, rows in sorted(
        grouped.items(), key=lambda item: min(int(row["priority"]) for row in item[1])
    ):
        first_row = min(rows, key=lambda row: int(row["priority"]))
        frontier_type = str(first_row["frontier_type"])
        diagnostic = diagnostics_by_key.get(key, {})
        targets.append(
            {
                "A": key[0],
                "B": key[1],
                "curve": key[2],
                "frontier_type": frontier_type,
                "gap_type": str(first_row["gap_type"]),
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
                "proof_queue_status": QUEUE_STATUSES[frontier_type],
                "next_step": NEXT_STEPS[frontier_type],
                "candidate_not_proof": True,
            }
        )

    return {
        "status": "ok",
        "non_rankzero_frontier_cover_count": sum(
            int(target["cover_count"]) for target in targets
        ),
        "non_rankzero_frontier_target_count": len(targets),
        "target_type_counts": dict(
            sorted(Counter(str(target["frontier_type"]) for target in targets).items())
        ),
        "targets": targets,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--open-frontier-audit", type=Path, required=True)
    parser.add_argument("--diagnostics", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    queue = build_non_rankzero_frontier_queue(
        open_frontier_audit=load_json(args.open_frontier_audit),
        diagnostics=load_jsonl(args.diagnostics),
    )
    write_json(args.out, queue)
    print(f"wrote non-rankzero frontier queue to {args.out}")
    print(
        "non_rankzero_frontier_cover_count="
        f"{queue['non_rankzero_frontier_cover_count']}"
    )
    print(
        "non_rankzero_frontier_target_count="
        f"{queue['non_rankzero_frontier_target_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
