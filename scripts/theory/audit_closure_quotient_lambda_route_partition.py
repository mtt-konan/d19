#!/usr/bin/env python3
"""Audit that lambda classes are partitioned into structural proof routes."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits route coverage for lambda classes. It verifies partitioning "
    "of existing ledgers, not any family exclusion theorem."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _classes(rows: list[dict[str, Any]]) -> set[str]:
    return {str(row.get("class", "")) for row in rows}


def audit_lambda_route_partition(
    *,
    ray_ledger: dict[str, Any],
    rank_zero_candidates: dict[str, Any],
    root_number_triage: dict[str, Any],
    two_cover_frontier: dict[str, Any],
) -> dict[str, Any]:
    all_classes = _classes(list(ray_ledger.get("c_ratio_class_rows", [])))
    route_sets = {
        "rank-zero-family-generalization": _classes(
            list(rank_zero_candidates.get("candidates", []))
        ),
        "root-number-rank-structure-triage": _classes(
            list(root_number_triage.get("targets", []))
        ),
        "two-cover-or-reviewable-no-point-certificate": _classes(
            list(two_cover_frontier.get("targets", []))
        ),
    }
    memberships: Counter[str] = Counter()
    for route_classes in route_sets.values():
        memberships.update(route_classes)
    covered_classes = set(memberships)
    missing_classes = sorted(all_classes - covered_classes)
    overlap_classes = sorted(
        class_name for class_name, count in memberships.items() if count > 1
    )
    unexpected_classes = sorted(covered_classes - all_classes)
    status = (
        "ok"
        if not missing_classes and not overlap_classes and not unexpected_classes
        else "issues"
    )
    return {
        "status": status,
        "ready": status == "ok",
        "lambda_class_count": len(all_classes),
        "rank_zero_class_count": len(route_sets["rank-zero-family-generalization"]),
        "root_number_class_count": len(route_sets["root-number-rank-structure-triage"]),
        "two_cover_class_count": len(
            route_sets["two-cover-or-reviewable-no-point-certificate"]
        ),
        "covered_class_count": len(covered_classes & all_classes),
        "missing_classes": missing_classes,
        "overlap_classes": overlap_classes,
        "unexpected_classes": unexpected_classes,
        "route_counts": {
            route: len(classes) for route, classes in route_sets.items()
        },
        "family_exclusion_proved_count": 0,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ray-ledger", type=Path, required=True)
    parser.add_argument("--rank-zero-candidates", type=Path, required=True)
    parser.add_argument("--root-number-triage", type=Path, required=True)
    parser.add_argument("--two-cover-frontier", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_lambda_route_partition(
        ray_ledger=load_json(args.ray_ledger),
        rank_zero_candidates=load_json(args.rank_zero_candidates),
        root_number_triage=load_json(args.root_number_triage),
        two_cover_frontier=load_json(args.two_cover_frontier),
    )
    write_json(args.out, audit)
    print(f"wrote closure quotient lambda route partition audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"lambda_class_count={audit['lambda_class_count']}")
    print(f"covered_class_count={audit['covered_class_count']}")
    print(f"family_exclusion_proved_count={audit['family_exclusion_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
