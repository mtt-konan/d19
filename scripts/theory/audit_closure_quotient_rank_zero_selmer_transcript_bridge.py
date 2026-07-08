#!/usr/bin/env python3
"""Bridge 9 Selmer transcript tasks onto shared kernel-local schemas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits how rank-zero Selmer transcript tasks reuse shared "
    "kernel-local schemas. It does not compute local Selmer images, prove a "
    "local condition, prove a Selmer rank bound, prove rank zero, or prove any "
    "lambda-family exclusion."
)

SHARED_TRANSCRIPT_FIELDS = ["local_squareclass_conditions"]
PACKAGE_SPECIFIC_TRANSCRIPT_FIELDS = [
    "statement",
    "isogeny_setup",
    "selmer_bound_argument",
    "rank_zero_conclusion",
    "review_notes",
]


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


def _kernel_to_schema(kernel_local_schemas: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("kernel", "")): row
        for row in kernel_local_schemas.get("kernel_schemas", [])
    }


def _intake_by_package(transcript_intake: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("package_id", "")): row
        for row in transcript_intake.get("packages", [])
    }


def _kernel_from_package_id(package_id: str) -> str:
    markers = {
        "-kernel-minus-p": "kernel_minus_p",
        "-kernel-neg-2sqrt-q": "kernel_neg_2sqrt_q",
        "-kernel-pos-2sqrt-q": "kernel_pos_2sqrt_q",
    }
    for marker, kernel in markers.items():
        if marker in package_id:
            return kernel
    return ""


def audit_rank_zero_selmer_transcript_bridge(
    *,
    materialization: dict[str, Any],
    kernel_local_schemas: dict[str, Any],
    transcript_intake: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(materialization):
        violations.append("materialization_not_ready")
    if not _ready(kernel_local_schemas):
        violations.append("kernel_local_schemas_not_ready")
    if not _ready(transcript_intake):
        violations.append("transcript_intake_not_ready")

    schema_by_kernel = _kernel_to_schema(kernel_local_schemas)
    intake_by_package = _intake_by_package(transcript_intake)
    bridge_rows: list[dict[str, Any]] = []

    for package in sorted(
        materialization.get("packages", []),
        key=lambda row: str(row.get("package_id", "")),
    ):
        package_id = str(package.get("package_id", ""))
        kernel = _kernel_from_package_id(package_id)
        schema = schema_by_kernel.get(kernel)
        if schema is None:
            violations.append(f"package_kernel_missing_schema={package_id}")
            continue
        intake_row = intake_by_package.get(package_id, {})
        bridge_rows.append(
            {
                "package_id": package_id,
                "kernel": kernel,
                "kernel_schema_id": str(schema.get("schema_id", "")),
                "shared_transcript_fields": SHARED_TRANSCRIPT_FIELDS,
                "package_specific_transcript_fields": (
                    PACKAGE_SPECIFIC_TRANSCRIPT_FIELDS
                ),
                "transcript_package_ready": bool(
                    intake_row.get("transcript_package_ready", False)
                ),
                "strict_promotion_ready": bool(
                    intake_row.get("strict_promotion_ready", False)
                ),
            }
        )

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "package_count": int(materialization.get("package_count", 0) or 0),
        "kernel_schema_count": int(
            kernel_local_schemas.get("kernel_schema_count", 0) or 0
        ),
        "shared_local_squareclass_template_count": int(
            kernel_local_schemas.get("kernel_schema_count", 0) or 0
        ),
        "package_specific_transcript_count": len(bridge_rows),
        "transcript_package_ready_count": int(
            transcript_intake.get("transcript_package_ready_count", 0) or 0
        ),
        "strict_promotion_ready_count": int(
            transcript_intake.get("strict_promotion_ready_count", 0) or 0
        ),
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "bridge_rows": bridge_rows,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--materialization", type=Path, required=True)
    parser.add_argument("--kernel-local-schemas", type=Path, required=True)
    parser.add_argument("--transcript-intake", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_transcript_bridge(
        materialization=load_json(args.materialization),
        kernel_local_schemas=load_json(args.kernel_local_schemas),
        transcript_intake=load_json(args.transcript_intake),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer transcript bridge audit to {args.out}")
    print(f"status={audit['status']}")
    print(
        "shared_local_squareclass_template_count="
        f"{audit['shared_local_squareclass_template_count']}"
    )
    print(f"package_specific_transcript_count={audit['package_specific_transcript_count']}")
    print(f"transcript_package_ready_count={audit['transcript_package_ready_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
