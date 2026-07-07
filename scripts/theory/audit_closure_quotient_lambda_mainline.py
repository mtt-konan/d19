#!/usr/bin/env python3
"""Audit the closure quotient lambda-mainline objective gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits that the closure quotient work is organized as a lambda-level "
    "structural proof mainline. It does not prove any lambda-family exclusion."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _ray_ledger_has_c_minus(ray_ledger: dict[str, Any]) -> bool:
    rows = list(ray_ledger.get("pair_rows", []))
    return bool(rows) and all(
        "c_minus" in row and "c_plus" in row and "c_ratio" in row for row in rows
    )


def _route_partition_complete(route_partition: dict[str, Any]) -> bool:
    return (
        route_partition.get("status") == "ok"
        and not route_partition.get("missing_classes")
        and not route_partition.get("overlap_classes")
        and not route_partition.get("unexpected_classes")
        and route_partition.get("lambda_class_count")
        == route_partition.get("covered_class_count")
    )


def _search_count_rejected(lambda_frontier: dict[str, Any]) -> bool:
    rejected = {
        str(metric) for metric in lambda_frontier.get("rejected_progress_metrics", [])
    }
    return "more individual (A,B) search hits" in rejected


def _two_cover_requires_strict_evidence(two_cover_frontier: dict[str, Any]) -> bool:
    required_phrases = {
        "family 2-cover or Selmer obstruction",
        "or reviewable cover-level no-point certificates for every listed cover",
    }
    targets = list(two_cover_frontier.get("targets", []))
    return bool(targets) and all(
        required_phrases.issubset(
            {str(item) for item in target.get("required_strict_evidence", [])}
        )
        and target.get("candidate_not_proof") is True
        for target in targets
    )


def _family_exclusion_count_zero(*payloads: dict[str, Any]) -> bool:
    return all(int(payload.get("family_exclusion_proved_count", 0)) == 0 for payload in payloads)


def audit_lambda_mainline(
    *,
    ray_ledger: dict[str, Any],
    lambda_frontier: dict[str, Any],
    route_partition: dict[str, Any],
    two_cover_frontier: dict[str, Any],
) -> dict[str, Any]:
    checks = {
        "ray_ledger_has_c_minus": _ray_ledger_has_c_minus(ray_ledger),
        "route_partition_complete": _route_partition_complete(route_partition),
        "search_count_rejected_as_progress": _search_count_rejected(lambda_frontier),
        "two_cover_requires_strict_evidence": _two_cover_requires_strict_evidence(
            two_cover_frontier
        ),
        "family_exclusion_claim_count_zero": _family_exclusion_count_zero(
            lambda_frontier,
            route_partition,
            two_cover_frontier,
        ),
    }
    violations = []
    if not checks["ray_ledger_has_c_minus"]:
        violations.append("ray-ledger-missing-c-minus-or-c-ratio")
    if not checks["route_partition_complete"]:
        violations.append("lambda-route-partition-incomplete")
    if not checks["search_count_rejected_as_progress"]:
        violations.append("search-count-not-rejected-as-progress")
    if not checks["two_cover_requires_strict_evidence"]:
        violations.append("two-cover-frontier-missing-strict-evidence-boundary")
    if not checks["family_exclusion_claim_count_zero"]:
        violations.append("family-exclusion-count-nonzero-without-theorem")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "lambda_class_count": int(route_partition.get("lambda_class_count", 0)),
        "covered_class_count": int(route_partition.get("covered_class_count", 0)),
        "route_counts": route_partition.get("route_counts", {}),
        "checks": checks,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ray-ledger", type=Path, required=True)
    parser.add_argument("--lambda-frontier", type=Path, required=True)
    parser.add_argument("--route-partition", type=Path, required=True)
    parser.add_argument("--two-cover-frontier", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_lambda_mainline(
        ray_ledger=load_json(args.ray_ledger),
        lambda_frontier=load_json(args.lambda_frontier),
        route_partition=load_json(args.route_partition),
        two_cover_frontier=load_json(args.two_cover_frontier),
    )
    write_json(args.out, audit)
    print(f"wrote closure quotient lambda mainline audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"lambda_class_count={audit['lambda_class_count']}")
    print(f"covered_class_count={audit['covered_class_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
