#!/usr/bin/env python3
"""Build the post-rank-method escalation queue for residual frontier work."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audit routes residual frontier targets after same-level rank-method "
    "attempts are exhausted. It does not prove that any residual cover has no "
    "rational point."
)

TRACK_ROUTES = {
    "rank-zero-rank-proof": (
        "rank-zero-external-rank-proof-or-cover-descent",
        "external strict rank proof, then cover-level no-point certificates",
    ),
    "rank-one-sha2-separation": (
        "rank-one-generator-sha2-separation-or-cover-descent",
        "visible rank-one generator plus Sha[2] separation, or cover-level "
        "no-point certificates",
    ),
    "even-gap4-deeper-descent": (
        "even-gap4-deeper-descent-or-cover-descent",
        "deeper descent or independent Sha[2] obstruction, or cover-level "
        "no-point certificates",
    ),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _int_value(payload: dict[str, Any], key: str) -> int:
    return int(payload.get(key, 0) or 0)


def _target_entry(
    target: dict[str, Any],
    *,
    rank_method_attempt_status: str,
) -> dict[str, Any]:
    track = str(target.get("track", ""))
    _, route = TRACK_ROUTES.get(track, ("unknown-route", "produce strict evidence"))
    entry = {
        "A": _int_value(target, "A"),
        "B": _int_value(target, "B"),
        "curve": str(target.get("curve", "")),
        "track": track,
        "cover_indices": list(target.get("cover_indices", [])),
        "cover_count": _int_value(target, "cover_count"),
        "priorities": list(target.get("priorities", [])),
        "rank_bounds": list(target.get("rank_bounds", [])),
        "primary_escalation_route": route,
        "required_strict_evidence": list(target.get("required_strict_evidence", [])),
        "nonproof_evidence_not_promotable": list(target.get("nonproof_evidence", [])),
        "strict_certificate_ready": bool(target.get("strict_certificate_ready", False)),
        "candidate_not_proof": True,
    }
    if track == "rank-zero-rank-proof":
        entry["rank_method_attempt_status"] = rank_method_attempt_status
    return entry


def _validate_inputs(
    *,
    strictification_queue: dict[str, Any],
    attempt_audit: dict[str, Any],
    next_action_audit: dict[str, Any],
    rank_zero_target_count: int,
) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    for name, payload in (
        ("strictification_queue", strictification_queue),
        ("attempt_audit", attempt_audit),
        ("next_action_audit", next_action_audit),
    ):
        if payload.get("status") != "ok":
            violations.append(
                {
                    "name": name,
                    "field": "status",
                    "expected": "ok",
                    "actual": payload.get("status"),
                }
            )
    expected_booleans = {
        "rank_zero_rank_method_target_hopping_exhausted": True,
        "cheap_rank_method_target_hopping_exhausted": True,
    }
    for field, expected in expected_booleans.items():
        actual = next_action_audit.get(field)
        if actual is not expected:
            violations.append(
                {
                    "name": "next_action_audit",
                    "field": field,
                    "expected": expected,
                    "actual": actual,
                }
            )
    if _int_value(attempt_audit, "strict_certificate_ready_count") != 0:
        violations.append(
            {
                "name": "attempt_audit",
                "field": "strict_certificate_ready_count",
                "expected": 0,
                "actual": attempt_audit.get("strict_certificate_ready_count"),
            }
        )
    if _int_value(attempt_audit, "target_count_with_attempts") < rank_zero_target_count:
        violations.append(
            {
                "name": "attempt_audit",
                "field": "target_count_with_attempts",
                "expected": rank_zero_target_count,
                "actual": attempt_audit.get("target_count_with_attempts"),
            }
        )
    if _int_value(strictification_queue, "strict_certificate_ready_count") != 0:
        violations.append(
            {
                "name": "strictification_queue",
                "field": "strict_certificate_ready_count",
                "expected": 0,
                "actual": strictification_queue.get("strict_certificate_ready_count"),
            }
        )
    return violations


def audit_escalation_queue(
    *,
    strictification_queue: dict[str, Any],
    attempt_audit: dict[str, Any],
    next_action_audit: dict[str, Any],
) -> dict[str, Any]:
    raw_targets = list(strictification_queue.get("targets", []))
    rank_zero_target_count = sum(
        1 for target in raw_targets if target.get("track") == "rank-zero-rank-proof"
    )
    violations = _validate_inputs(
        strictification_queue=strictification_queue,
        attempt_audit=attempt_audit,
        next_action_audit=next_action_audit,
        rank_zero_target_count=rank_zero_target_count,
    )
    rank_method_attempt_status = (
        "exhausted-without-proof"
        if next_action_audit.get("rank_zero_rank_method_target_hopping_exhausted")
        is True
        else "not-exhausted"
    )
    targets = [
        _target_entry(
            target,
            rank_method_attempt_status=rank_method_attempt_status,
        )
        for target in raw_targets
    ]
    route_counts: Counter[str] = Counter()
    for target in targets:
        route_key, _ = TRACK_ROUTES.get(
            str(target.get("track", "")), ("unknown-route", "")
        )
        route_counts[route_key] += 1
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "target_count": len(targets),
        "cover_count": sum(_int_value(target, "cover_count") for target in targets),
        "rank_zero_target_count": rank_zero_target_count,
        "rank_zero_rank_method_target_hopping_exhausted": next_action_audit.get(
            "rank_zero_rank_method_target_hopping_exhausted"
        )
        is True,
        "strict_certificate_ready_count": 0,
        "route_counts": dict(sorted(route_counts.items())),
        "targets": targets,
        "violations": violations,
        "candidate_not_proof": True,
        "proof_status": "escalation-queue-not-proof",
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strictification-queue", type=Path, required=True)
    parser.add_argument("--attempt-audit", type=Path, required=True)
    parser.add_argument("--next-action-audit", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_escalation_queue(
        strictification_queue=load_json(args.strictification_queue),
        attempt_audit=load_json(args.attempt_audit),
        next_action_audit=load_json(args.next_action_audit),
    )
    write_json(args.out, audit)
    print(f"wrote frontier escalation queue audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"target_count={audit['target_count']}")
    print(f"strict_certificate_ready_count={audit['strict_certificate_ready_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
