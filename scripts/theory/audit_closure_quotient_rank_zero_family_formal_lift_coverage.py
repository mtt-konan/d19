#!/usr/bin/env python3
"""Audit odd-prime formal-lift transcript coverage across rank-zero families."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits reviewable odd-prime formal-lift coverage across the three "
    "rank-zero primitive lambda families. It does not prove a dyadic local "
    "condition, a Selmer rank bound, rank zero, or any lambda-family exclusion."
)

NEXT_MAIN_ACTION = (
    "For AA, move from odd-prime formal-lift completion to the dyadic local "
    "condition, global Selmer dimension bound, and rank-zero conclusion; for "
    "AA+BB and BB, continue obtaining reviewable formal-lift segments until "
    "each family closes all three packages."
)

ALL_COMPLETE_NEXT_MAIN_ACTION = (
    "Odd-prime formal-lift coverage is complete for AA, AA+BB, and BB; "
    "move to the dyadic local conditions, global Selmer dimension bounds, "
    "and rank-zero conclusions without treating partial transcripts as "
    "family-level theorems."
)


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


def _pattern_from_package_id(package_id: str) -> str:
    if "rank-zero-selmer-AA-BB-" in package_id:
        return "AA+BB"
    if "rank-zero-selmer-AA-" in package_id:
        return "AA"
    if "rank-zero-selmer-BB-" in package_id:
        return "BB"
    return ""


def _reviewable_formal_lift_packages(package_segments: dict[str, Any]) -> set[str]:
    packages: set[str] = set()
    for row in package_segments.get("segments", []):
        if (
            str(row.get("required_field", "")) == "selmer_bound_argument"
            and str(row.get("proof_section", "")) == "formal_lift_compatibility"
            and str(row.get("segment_status", "")) == "reviewable-proof"
        ):
            packages.add(str(row.get("package_id", "")))
    return packages


def _progress_status(*, count: int, package_count: int) -> str:
    if count == package_count:
        return "odd-prime-formal-lift-complete-not-proof"
    if count > 0:
        return "partial-reviewable-formal-lift-segment-present"
    return "no-reviewable-formal-lift-segment-yet"


def audit_rank_zero_family_formal_lift_coverage(
    *,
    family_obligations: dict[str, Any],
    package_segments: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(family_obligations):
        violations.append("family_obligations_not_ready")
    if not _ready(package_segments):
        violations.append("package_segments_not_ready")

    reviewable_packages = _reviewable_formal_lift_packages(package_segments)
    families: list[dict[str, Any]] = []

    for group in family_obligations.get("groups", []):
        pattern = str(group.get("pattern", ""))
        package_count = 3
        count = sum(
            1
            for package_id in reviewable_packages
            if _pattern_from_package_id(package_id) == pattern
        )
        families.append(
            {
                "pattern": pattern,
                "priority": int(group.get("priority", 0) or 0),
                "candidate_class_count": int(group.get("candidate_class_count", 0) or 0),
                "model_count": int(group.get("model_count", 0) or 0),
                "package_count": package_count,
                "reviewable_formal_lift_package_count": count,
                "odd_prime_formal_lift_complete": count == package_count,
                "family_progress_status": _progress_status(
                    count=count,
                    package_count=package_count,
                ),
            }
        )

    status = "ok" if not violations else "issues"
    all_families_complete = all(
        bool(family.get("odd_prime_formal_lift_complete", False))
        for family in families
    )
    return {
        "status": status,
        "ready": status == "ok",
        "family_count": len(families),
        "reviewable_formal_lift_package_count": len(reviewable_packages),
        "family_exclusion_proved_count": 0,
        "families": families,
        "next_main_action": (
            ALL_COMPLETE_NEXT_MAIN_ACTION
            if families and all_families_complete
            else NEXT_MAIN_ACTION
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family-obligations", type=Path, required=True)
    parser.add_argument("--package-segments", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_family_formal_lift_coverage(
        family_obligations=load_json(args.family_obligations),
        package_segments=load_json(args.package_segments),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero family formal-lift coverage to {args.out}")
    print(f"status={audit['status']}")
    print(f"family_count={audit['family_count']}")
    print(
        "reviewable_formal_lift_package_count="
        f"{audit['reviewable_formal_lift_package_count']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
