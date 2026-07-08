#!/usr/bin/env python3
"""Audit the field-level decomposition of rank-zero Selmer transcripts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This decomposes rank-zero Selmer transcript fields into shared kernel "
    "templates, family-level conclusions, and package-specific fields. It does "
    "not prove local conditions, Selmer rank bounds, rank zero, or any "
    "lambda-family exclusion."
)

REQUIRED_TRANSCRIPT_FIELDS = [
    "statement",
    "isogeny_setup",
    "local_squareclass_conditions",
    "selmer_bound_argument",
    "rank_zero_conclusion",
    "review_notes",
]
KERNEL_SHARED_FIELDS = ["local_squareclass_conditions", "isogeny_setup"]
FAMILY_AGGREGATED_FIELDS = ["rank_zero_conclusion"]
PACKAGE_SPECIFIC_FIELDS = ["statement", "selmer_bound_argument", "review_notes"]
PRIMARY_REMAINING_PROOF_FIELD = "selmer_bound_argument"


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


def audit_rank_zero_selmer_transcript_field_decomposition(
    *,
    transcript_intake: dict[str, Any],
    transcript_bridge: dict[str, Any],
    isogeny_setup_templates: dict[str, Any],
    family_conclusion_templates: dict[str, Any],
) -> dict[str, Any]:
    checks = {
        "transcript_intake_ready": _ready(transcript_intake),
        "transcript_bridge_ready": _ready(transcript_bridge),
        "isogeny_setup_templates_ready": _ready(isogeny_setup_templates),
        "family_conclusion_templates_ready": _ready(family_conclusion_templates),
        "transcript_packages_not_ready": (
            _int(transcript_intake, "transcript_package_ready_count") == 0
        ),
        "strict_promotion_ready_count_zero": (
            _int(transcript_intake, "strict_promotion_ready_count") == 0
        ),
        "rank_zero_conclusion_claim_count_zero": (
            _int(family_conclusion_templates, "rank_zero_conclusion_proved_count")
            == 0
        ),
    }
    violations = [name for name, passed in checks.items() if not passed]
    if "rank_zero_conclusion_claim_count_zero" in violations:
        violations = [
            "rank_zero_conclusion_claim_count_nonzero"
            if value == "rank_zero_conclusion_claim_count_zero"
            else value
            for value in violations
        ]

    package_count = _int(transcript_intake, "package_count")
    kernel_shared_template_count = min(
        _int(transcript_bridge, "shared_local_squareclass_template_count"),
        _int(isogeny_setup_templates, "shared_isogeny_setup_template_count"),
    )
    package_specific_open_field_obligation_count = (
        package_count * len(PACKAGE_SPECIFIC_FIELDS)
    )
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "required_transcript_field_count": len(REQUIRED_TRANSCRIPT_FIELDS),
        "kernel_shared_field_count": len(KERNEL_SHARED_FIELDS),
        "kernel_shared_template_count": kernel_shared_template_count,
        "family_aggregated_field_count": len(FAMILY_AGGREGATED_FIELDS),
        "family_conclusion_template_count": _int(
            family_conclusion_templates,
            "family_conclusion_template_count",
        ),
        "package_specific_field_count": len(PACKAGE_SPECIFIC_FIELDS),
        "package_specific_open_field_obligation_count": (
            package_specific_open_field_obligation_count
        ),
        "primary_remaining_proof_field": PRIMARY_REMAINING_PROOF_FIELD,
        "transcript_package_ready_count": _int(
            transcript_intake,
            "transcript_package_ready_count",
        ),
        "strict_promotion_ready_count": _int(
            transcript_intake,
            "strict_promotion_ready_count",
        ),
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "field_decomposition": {
            "kernel_shared_fields": KERNEL_SHARED_FIELDS,
            "family_aggregated_fields": FAMILY_AGGREGATED_FIELDS,
            "package_specific_fields": PACKAGE_SPECIFIC_FIELDS,
        },
        "checks": checks,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transcript-intake", type=Path, required=True)
    parser.add_argument("--transcript-bridge", type=Path, required=True)
    parser.add_argument("--isogeny-setup-templates", type=Path, required=True)
    parser.add_argument("--family-conclusion-templates", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_transcript_field_decomposition(
        transcript_intake=load_json(args.transcript_intake),
        transcript_bridge=load_json(args.transcript_bridge),
        isogeny_setup_templates=load_json(args.isogeny_setup_templates),
        family_conclusion_templates=load_json(args.family_conclusion_templates),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer transcript field decomposition to {args.out}")
    print(f"status={audit['status']}")
    print(f"kernel_shared_field_count={audit['kernel_shared_field_count']}")
    print(f"family_aggregated_field_count={audit['family_aggregated_field_count']}")
    print(f"package_specific_field_count={audit['package_specific_field_count']}")
    print(f"primary_remaining_proof_field={audit['primary_remaining_proof_field']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
