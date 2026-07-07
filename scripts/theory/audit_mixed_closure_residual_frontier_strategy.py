#!/usr/bin/env python3
"""Audit proof-work routing after mixed-closure residual frontier retries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audit summarizes proof-work routing after Sage retries. "
    "Timeouts are not proofs and do not certify that any residual cover has no rational point."
)

NEXT_ACTIONS = [
    (
        "Stop treating short Sage rechecks as a remaining queue; every recorded "
        "frontier target has timed out."
    ),
    (
        "For rank-zero targets, use an external rank proof or a cover-level "
        "descent/Sha[2] obstruction before promoting any residual cover."
    ),
    (
        "For non-rank-zero targets, separate the visible rank contribution or "
        "produce a deeper independent 2-cover obstruction."
    ),
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _int_value(payload: dict[str, Any], key: str) -> int:
    return int(payload.get(key, 0))


def _status_count(payload: dict[str, Any], status: str) -> int:
    return int(payload.get("target_status_counts", {}).get(status, 0))


def _rank_target_status(target: dict[str, Any]) -> str:
    return str(target.get("rank_proof_queue_status", "missing"))


def _non_rank_target_status(target: dict[str, Any]) -> str:
    return str(target.get("proof_queue_status", "missing"))


def _all_targets_have_status(
    targets: list[dict[str, Any]],
    *,
    status: str,
    status_key: str,
) -> bool:
    if not targets:
        return False
    return all(str(target.get(status_key)) == status for target in targets)


def _short_sage_retry_status(
    *,
    rank_zero_queue: dict[str, Any],
    non_rankzero_queue: dict[str, Any],
) -> str:
    if _status_count(rank_zero_queue, "not-retried"):
        return "still-has-untried-targets"
    if _status_count(non_rankzero_queue, "not-retried"):
        return "still-has-untried-targets"
    rank_zero_target_count = _int_value(
        rank_zero_queue, "rank_zero_frontier_target_count"
    )
    non_rankzero_target_count = _int_value(
        non_rankzero_queue, "non_rankzero_frontier_target_count"
    )
    timeout_count = _status_count(rank_zero_queue, "sage-timeout") + _status_count(
        non_rankzero_queue, "sage-timeout"
    )
    if rank_zero_target_count + non_rankzero_target_count == timeout_count:
        return "exhausted-without-proof"
    return "partially-open"


def _first_external_rank_target(
    targets: list[dict[str, Any]],
) -> dict[str, Any] | None:
    if not targets:
        return None
    first = targets[0]
    timeout_seconds = int(first.get("sage_recheck_timeout_seconds") or 0)
    return {
        "A": int(first["A"]),
        "B": int(first["B"]),
        "curve": str(first["curve"]),
        "priorities": [int(value) for value in first.get("priorities", [])],
        "cover_indices": [int(value) for value in first.get("cover_indices", [])],
        "has_long_sage_timeout": timeout_seconds >= 600,
        "max_timeout_seconds": timeout_seconds,
    }


def audit_frontier_strategy(
    *,
    rank_zero_queue: dict[str, Any],
    non_rankzero_queue: dict[str, Any],
) -> dict[str, Any]:
    rank_targets = list(rank_zero_queue.get("targets", []))
    non_rank_targets = list(non_rankzero_queue.get("targets", []))
    rank_zero_target_count = _int_value(
        rank_zero_queue, "rank_zero_frontier_target_count"
    )
    non_rankzero_target_count = _int_value(
        non_rankzero_queue, "non_rankzero_frontier_target_count"
    )
    short_sage_timeout_count = _status_count(
        rank_zero_queue, "sage-timeout"
    ) + _status_count(non_rankzero_queue, "sage-timeout")
    status = _short_sage_retry_status(
        rank_zero_queue=rank_zero_queue,
        non_rankzero_queue=non_rankzero_queue,
    )
    target_type_counts = dict(
        sorted(non_rankzero_queue.get("target_type_counts", {}).items())
    )
    closed_rank_zero_targets = _int_value(
        rank_zero_queue, "closed_rank_zero_target_count"
    )
    return {
        "status": "ok"
        if rank_zero_queue.get("status") == "ok"
        and non_rankzero_queue.get("status") == "ok"
        else "input-error",
        "short_sage_retry_status": status,
        "short_sage_retry_target_count": rank_zero_target_count
        + non_rankzero_target_count,
        "short_sage_retry_timeout_target_count": short_sage_timeout_count,
        "strict_promotion_count": closed_rank_zero_targets,
        "candidate_not_proof": True,
        "rank_zero_strategy_status": {
            "cover_count": _int_value(
                rank_zero_queue, "rank_zero_frontier_cover_count"
            ),
            "target_count": rank_zero_target_count,
            "closed_target_count": closed_rank_zero_targets,
            "untried_target_count": _status_count(rank_zero_queue, "not-retried"),
            "all_targets_timed_out": _all_targets_have_status(
                rank_targets,
                status="sage-timeout",
                status_key="rank_proof_queue_status",
            ),
            "target_status_counts": dict(
                sorted(rank_zero_queue.get("target_status_counts", {}).items())
            ),
            "proof_status": "rank-proof-frontier-not-proof",
        },
        "non_rankzero_strategy_status": {
            "cover_count": _int_value(
                non_rankzero_queue, "non_rankzero_frontier_cover_count"
            ),
            "target_count": non_rankzero_target_count,
            "all_targets_timed_out": _all_targets_have_status(
                non_rank_targets,
                status="sage-timeout",
                status_key="proof_queue_status",
            ),
            "target_status_counts": dict(
                sorted(non_rankzero_queue.get("target_status_counts", {}).items())
            ),
            "target_type_counts": target_type_counts,
            "proof_status": "non-rankzero-frontier-not-proof",
        },
        "next_strategy_counts": {
            "even_gap4_deeper_descent_or_sha2_obstruction": int(
                target_type_counts.get("even-rank-gap4-needs-deeper-descent", 0)
            ),
            "external_rank_proof_or_cover_level_descent": rank_zero_target_count,
            "rank1_generator_or_sha2_separation": int(
                target_type_counts.get("rank1-needs-visible-generator-or-descent", 0)
            ),
        },
        "first_external_rank_target": _first_external_rank_target(rank_targets),
        "next_actions": NEXT_ACTIONS,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rank-zero-queue", type=Path, required=True)
    parser.add_argument("--non-rankzero-queue", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_frontier_strategy(
        rank_zero_queue=load_json(args.rank_zero_queue),
        non_rankzero_queue=load_json(args.non_rankzero_queue),
    )
    write_json(args.out, audit)
    print(f"wrote residual frontier strategy audit to {args.out}")
    print(f"short_sage_retry_status={audit['short_sage_retry_status']}")
    print(f"strict_promotion_count={audit['strict_promotion_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
