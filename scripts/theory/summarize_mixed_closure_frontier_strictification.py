#!/usr/bin/env python3
"""Build the residual frontier strictification queue."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This queue orders residual frontier strictification work. It does not prove "
    "that any residual cover has no rational point."
)

TRACK_REQUIREMENTS = {
    "rank-zero-rank-proof": [
        "strict elliptic rank proof closing rank_bounds to [0,0]",
        "or a cover-level no-rational-point certificate for every listed cover",
    ],
    "rank-one-sha2-separation": [
        "visible rank-one generator plus separation of the residual Sha[2] class",
        "or a cover-level no-rational-point certificate for every listed cover",
    ],
    "even-gap4-deeper-descent": [
        "deeper descent or independent Sha[2] obstruction",
        "or a cover-level no-rational-point certificate for every listed cover",
    ],
}

TRACK_NEXT_ACTIONS = {
    "rank-zero-rank-proof": (
        "Try an external strict rank proof first; if that still leaves "
        "rank_bounds open, switch to cover-level descent/no-point certificates."
    ),
    "rank-one-sha2-separation": (
        "Find a visible generator accounting for the rank-one part, then prove "
        "the remaining 2-cover class is obstructed."
    ),
    "even-gap4-deeper-descent": (
        "Use deeper descent or an independent Sha[2] obstruction before any "
        "residual cover can be promoted."
    ),
}

NONPROOF_EVIDENCE = [
    "sage-timeout",
    "bounded-search-zero-points",
    "rank-bounds-not-closed",
    "local-solubility-witnesses",
    "map-verification",
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


def _int_list(values: Any) -> list[int]:
    return [int(value) for value in values or []]


def _priority(target: dict[str, Any]) -> int:
    priorities = _int_list(target.get("priorities", []))
    return min(priorities) if priorities else 10**9


def _target_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "A": int(row["A"]),
        "B": int(row["B"]),
        "curve": str(row["curve"]),
        "track": str(row["track"]),
        "priorities": _int_list(row.get("priorities", [])),
        "cover_indices": _int_list(row.get("cover_indices", [])),
    }


def _strict_ready(track: str, target: dict[str, Any]) -> bool:
    if track == "rank-zero-rank-proof":
        return _int_list(target.get("rank_bounds", [])) == [0, 0]
    return False


def _rank_zero_row(target: dict[str, Any]) -> dict[str, Any]:
    track = "rank-zero-rank-proof"
    return {
        "A": int(target["A"]),
        "B": int(target["B"]),
        "curve": str(target["curve"]),
        "track": track,
        "frontier_type": "rank-zero-needs-rank-proof",
        "priorities": _int_list(target.get("priorities", [])),
        "cover_indices": _int_list(target.get("cover_indices", [])),
        "cover_count": int(target.get("cover_count", 0)),
        "rank_bounds": _int_list(target.get("rank_bounds", [])),
        "queue_status": str(target.get("rank_proof_queue_status", "")),
        "max_timeout_seconds": int(target.get("sage_recheck_timeout_seconds") or 0),
        "required_strict_evidence": TRACK_REQUIREMENTS[track],
        "nonproof_evidence": NONPROOF_EVIDENCE,
        "next_action": TRACK_NEXT_ACTIONS[track],
        "strict_certificate_ready": _strict_ready(track, target),
        "proof_status": "open-frontier-not-proof",
        "candidate_not_proof": True,
    }


def _non_rankzero_track(frontier_type: str) -> str:
    if frontier_type == "rank1-needs-visible-generator-or-descent":
        return "rank-one-sha2-separation"
    if frontier_type == "even-rank-gap4-needs-deeper-descent":
        return "even-gap4-deeper-descent"
    return "non-rankzero-frontier"


def _non_rankzero_row(target: dict[str, Any]) -> dict[str, Any]:
    frontier_type = str(target.get("frontier_type", ""))
    track = _non_rankzero_track(frontier_type)
    return {
        "A": int(target["A"]),
        "B": int(target["B"]),
        "curve": str(target["curve"]),
        "track": track,
        "frontier_type": frontier_type,
        "priorities": _int_list(target.get("priorities", [])),
        "cover_indices": _int_list(target.get("cover_indices", [])),
        "cover_count": int(target.get("cover_count", 0)),
        "rank_bounds": _int_list(target.get("rank_bounds", [])),
        "queue_status": str(target.get("proof_queue_status", "")),
        "required_strict_evidence": TRACK_REQUIREMENTS.get(track, []),
        "nonproof_evidence": NONPROOF_EVIDENCE,
        "next_action": TRACK_NEXT_ACTIONS.get(track, "produce a strict cover-level proof"),
        "strict_certificate_ready": _strict_ready(track, target),
        "proof_status": "open-frontier-not-proof",
        "candidate_not_proof": True,
    }


def _blocking_issues(
    *,
    rank_zero_queue: dict[str, Any],
    non_rankzero_queue: dict[str, Any],
    frontier_handoff_audit: dict[str, Any],
) -> list[str]:
    issues: list[str] = []
    expected_targets = _int_value(
        rank_zero_queue, "rank_zero_frontier_target_count"
    ) + _int_value(non_rankzero_queue, "non_rankzero_frontier_target_count")
    expected_covers = _int_value(
        rank_zero_queue, "rank_zero_frontier_cover_count"
    ) + _int_value(non_rankzero_queue, "non_rankzero_frontier_cover_count")
    if rank_zero_queue.get("status") != "ok":
        issues.append("rank-zero-frontier-queue-issues")
    if non_rankzero_queue.get("status") != "ok":
        issues.append("non-rankzero-frontier-queue-issues")
    if (
        frontier_handoff_audit.get("status") != "ok"
        or _int_value(frontier_handoff_audit, "handoff_group_count") != expected_targets
        or _int_value(frontier_handoff_audit, "target_cover_count") != expected_covers
        or _int_value(frontier_handoff_audit, "strict_promotion_count") != 0
        or frontier_handoff_audit.get("candidate_not_proof") is not True
        or frontier_handoff_audit.get("missing_files")
        or frontier_handoff_audit.get("violations")
    ):
        issues.append("frontier-handoff-audit-issues")
    return issues


def build_strictification_queue(
    *,
    rank_zero_queue: dict[str, Any],
    non_rankzero_queue: dict[str, Any],
    frontier_handoff_audit: dict[str, Any],
) -> dict[str, Any]:
    targets = [_rank_zero_row(target) for target in rank_zero_queue.get("targets", [])]
    targets.extend(
        _non_rankzero_row(target) for target in non_rankzero_queue.get("targets", [])
    )
    targets = sorted(targets, key=_priority)
    issues = _blocking_issues(
        rank_zero_queue=rank_zero_queue,
        non_rankzero_queue=non_rankzero_queue,
        frontier_handoff_audit=frontier_handoff_audit,
    )
    strict_ready_count = sum(
        1 for target in targets if target.get("strict_certificate_ready") is True
    )
    return {
        "status": "ok" if not issues else "issues",
        "ready": not issues,
        "blocking_issues": issues,
        "target_count": len(targets),
        "cover_count": sum(int(target["cover_count"]) for target in targets),
        "track_counts": dict(
            sorted(Counter(str(target["track"]) for target in targets).items())
        ),
        "strict_certificate_ready_count": strict_ready_count,
        "candidate_not_proof": strict_ready_count == 0,
        "first_target": _target_summary(targets[0]) if targets else None,
        "targets": targets,
        "acceptable_strict_evidence_by_track": TRACK_REQUIREMENTS,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rank-zero-queue", type=Path, required=True)
    parser.add_argument("--non-rankzero-queue", type=Path, required=True)
    parser.add_argument("--frontier-handoff-audit", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    queue = build_strictification_queue(
        rank_zero_queue=load_json(args.rank_zero_queue),
        non_rankzero_queue=load_json(args.non_rankzero_queue),
        frontier_handoff_audit=load_json(args.frontier_handoff_audit),
    )
    write_json(args.out, queue)
    print(f"wrote mixed closure frontier strictification queue to {args.out}")
    print(f"status={queue['status']}")
    print(f"target_count={queue['target_count']}")
    print(f"cover_count={queue['cover_count']}")
    print(f"strict_certificate_ready_count={queue['strict_certificate_ready_count']}")
    if args.strict and queue["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
