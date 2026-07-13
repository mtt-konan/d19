#!/usr/bin/env python3
"""Audit transcript progress across the three rank-zero lambda families."""

from __future__ import annotations

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

import argparse
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits transcript progress across the three rank-zero primitive "
    "lambda families. It does not prove a Selmer bound, rank zero, or any "
    "lambda-family exclusion."
)

NEXT_MAIN_ACTION = (
    "Expand family-proof progress by turning package-level reviewable segments "
    "into full rank-zero Selmer transcripts, without treating partial segments "
    "or sample growth as theorem completion."
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


def _progress_status(*, ready_count: int, reviewable_count: int) -> str:
    if ready_count > 0:
        return "transcript-package-ready-present"
    if reviewable_count > 0:
        return "partial-reviewable-segment-present"
    return "no-reviewable-segment-yet"


def audit_rank_zero_family_transcript_coverage(
    *,
    family_obligations: dict[str, Any],
    transcript_intake: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(family_obligations):
        violations.append("family_obligations_not_ready")
    if not _ready(transcript_intake):
        violations.append("transcript_intake_not_ready")

    packages_by_pattern: dict[str, list[dict[str, Any]]] = {"AA": [], "AA+BB": [], "BB": []}
    for package in transcript_intake.get("packages", []):
        pattern = _pattern_from_package_id(str(package.get("package_id", "")))
        if not pattern:
            violations.append(
                f"unexpected_package_pattern={package.get('package_id', '')}"
            )
            continue
        packages_by_pattern.setdefault(pattern, []).append(dict(package))

    families: list[dict[str, Any]] = []
    for group in family_obligations.get("groups", []):
        pattern = str(group.get("pattern", ""))
        packages = packages_by_pattern.get(pattern, [])
        ready_count = sum(
            1 for package in packages if bool(package.get("transcript_package_ready", False))
        )
        reviewable_packages = [
            package
            for package in packages
            if int(package.get("reviewable_segment_count", 0) or 0) > 0
        ]
        reviewable_package_count = len(reviewable_packages)
        reviewable_segment_total = sum(
            int(package.get("reviewable_segment_count", 0) or 0)
            for package in packages
        )
        families.append(
            {
                "pattern": pattern,
                "priority": int(group.get("priority", 0) or 0),
                "candidate_class_count": int(group.get("candidate_class_count", 0) or 0),
                "model_count": int(group.get("model_count", 0) or 0),
                "package_count": len(packages),
                "transcript_package_ready_count": ready_count,
                "reviewable_segment_package_count": reviewable_package_count,
                "reviewable_segment_total": reviewable_segment_total,
                "family_progress_status": _progress_status(
                    ready_count=ready_count,
                    reviewable_count=reviewable_package_count,
                ),
            }
        )

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "family_count": len(families),
        "package_count": int(transcript_intake.get("package_count", 0) or 0),
        "transcript_package_ready_count": int(
            transcript_intake.get("transcript_package_ready_count", 0) or 0
        ),
        "packages_with_reviewable_segment_count": int(
            transcript_intake.get("packages_with_reviewable_segment_count", 0) or 0
        ),
        "family_exclusion_proved_count": 0,
        "rank_zero_family_proof_complete": False,
        "next_main_action": NEXT_MAIN_ACTION,
        "families": families,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family-obligations", type=Path, required=True)
    parser.add_argument("--transcript-intake", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_family_transcript_coverage(
        family_obligations=load_json(args.family_obligations),
        transcript_intake=load_json(args.transcript_intake),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero family transcript coverage to {args.out}")
    print(f"status={audit['status']}")
    print(f"family_count={audit['family_count']}")
    print(
        "packages_with_reviewable_segment_count="
        f"{audit['packages_with_reviewable_segment_count']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
