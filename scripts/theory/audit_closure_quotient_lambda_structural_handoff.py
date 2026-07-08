#!/usr/bin/env python3
"""Audit handoff from c-ratio coverage to lambda structural proof tracks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits that c_+/c_- orientation gaps are handed off to lambda-level "
    "structural routes. It does not prove any lambda-family exclusion, add "
    "no-point certificates, or count search growth as progress."
)

ACCEPTABLE_EVIDENCE_BY_ROUTE = {
    "rank_zero": "family rank-zero proof over oriented lambda classes",
    "root_number": "root-number/parity plus rank or descent theorem",
    "two_cover": (
        "family 2-cover/Selmer obstruction or reviewable no-point certificates"
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


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


def _int(payload: dict[str, Any], key: str) -> int:
    return int(payload.get(key, 0) or 0)


def _family_exclusion_count(*payloads: dict[str, Any]) -> int:
    return sum(_int(payload, "family_exclusion_proved_count") for payload in payloads)


def _route_row(route: dict[str, Any]) -> dict[str, Any]:
    route_name = str(route.get("route", ""))
    return {
        "route": route_name,
        "priority": int(route.get("priority", 0) or 0),
        "class_count": int(route.get("class_count", 0) or 0),
        "structural_goal": str(route.get("missing_theorem", "")),
        "acceptable_evidence": ACCEPTABLE_EVIDENCE_BY_ROUTE.get(
            route_name,
            "reviewable structural proof or no-point certificate",
        ),
        "family_exclusion_proved": bool(route.get("family_exclusion_proved", False)),
    }


def _route_partition_ready(route_partition: dict[str, Any]) -> bool:
    return (
        _ready(route_partition)
        and route_partition.get("missing_classes") == []
        and route_partition.get("overlap_classes") == []
        and route_partition.get("unexpected_classes") == []
    )


def audit_lambda_structural_handoff(
    *,
    c_ratio_coverage: dict[str, Any],
    lambda_frontier: dict[str, Any],
    route_partition: dict[str, Any],
    convergence_priorities: dict[str, Any],
) -> dict[str, Any]:
    orientation_gap_count = _int(c_ratio_coverage, "lambda_orientation_gap_class_count")
    handed_count = _int(route_partition, "covered_class_count")
    unhandled_count = max(orientation_gap_count - handed_count, 0)
    family_exclusion_count = _family_exclusion_count(
        c_ratio_coverage,
        lambda_frontier,
        route_partition,
        convergence_priorities,
    )

    checks = {
        "c_ratio_coverage_ready": (
            _ready(c_ratio_coverage)
            and c_ratio_coverage.get("c_ratio_coverage_not_lambda_family_proof")
            is True
        ),
        "lambda_frontier_ready": (
            _ready(lambda_frontier)
            and lambda_frontier.get("candidate_not_proof") is True
        ),
        "route_partition_ready_for_handoff": _route_partition_ready(route_partition),
        "convergence_priorities_ready": (
            _ready(convergence_priorities)
            and convergence_priorities.get("convergence_complete") is False
            and convergence_priorities.get("search_count_used_as_progress") is False
        ),
        "orientation_gap_classes_handled": unhandled_count == 0,
        "family_exclusion_claim_count_zero": family_exclusion_count == 0,
    }
    violation_names = {
        "c_ratio_coverage_ready": "c_ratio_coverage_not_ready",
        "lambda_frontier_ready": "lambda_frontier_not_ready",
        "route_partition_ready_for_handoff": "route_partition_not_ready_for_handoff",
        "convergence_priorities_ready": "convergence_priorities_not_ready",
        "orientation_gap_classes_handled": "orientation_gap_classes_unhandled",
        "family_exclusion_claim_count_zero": "family_exclusion_claim_count_nonzero",
    }
    violations = [
        violation_names[name] for name, passed in checks.items() if not passed
    ]

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "lambda_structural_handoff_ready": status == "ok",
        "convergence_complete": False,
        "orientation_gap_class_count": orientation_gap_count,
        "handed_to_structural_route_count": handed_count,
        "unhandled_orientation_gap_count": unhandled_count,
        "route_counts": dict(route_partition.get("route_counts", {})),
        "priority_order": list(convergence_priorities.get("priority_order", [])),
        "family_exclusion_proved_count": family_exclusion_count,
        "no_point_certificate_added_count": _int(
            c_ratio_coverage,
            "no_point_certificate_added_count",
        ),
        "search_count_used_as_progress": False,
        "closure_quotient_promoted_to_lambda_proof": False,
        "handoff_rows": [
            _route_row(route)
            for route in convergence_priorities.get("routes", [])
        ],
        "checks": checks,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c-ratio-coverage", type=Path, required=True)
    parser.add_argument("--lambda-frontier", type=Path, required=True)
    parser.add_argument("--route-partition", type=Path, required=True)
    parser.add_argument("--convergence-priorities", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_lambda_structural_handoff(
        c_ratio_coverage=load_json(args.c_ratio_coverage),
        lambda_frontier=load_json(args.lambda_frontier),
        route_partition=load_json(args.route_partition),
        convergence_priorities=load_json(args.convergence_priorities),
    )
    write_json(args.out, audit)
    print(f"wrote closure quotient lambda structural handoff audit to {args.out}")
    print(f"status={audit['status']}")
    print(
        "lambda_structural_handoff_ready="
        f"{audit['lambda_structural_handoff_ready']}"
    )
    print(f"orientation_gap_class_count={audit['orientation_gap_class_count']}")
    print(f"unhandled_orientation_gap_count={audit['unhandled_orientation_gap_count']}")
    print(f"family_exclusion_proved_count={audit['family_exclusion_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
