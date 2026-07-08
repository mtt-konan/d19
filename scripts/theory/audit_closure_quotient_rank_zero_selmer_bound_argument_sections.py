#!/usr/bin/env python3
"""Audit proof-section outlines for rank-zero Selmer bound arguments."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This decomposes each open rank-zero Selmer bound argument into reviewable "
    "proof sections. It does not prove local-image theorems, formal lift "
    "compatibility, dyadic local conditions, Selmer rank bounds, rank zero, or "
    "any lambda-family exclusion."
)

PRIMARY_REMAINING_PROOF_FIELD = "selmer_bound_argument"
REQUIRED_SECTIONS = [
    "shared_isogeny_setup_reference",
    "odd_prime_local_image_theorems",
    "formal_lift_compatibility",
    "dyadic_local_condition",
    "global_selmer_dimension_bound",
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


def _int(payload: dict[str, Any], key: str) -> int:
    return int(payload.get(key, 0) or 0)


def _proof_count_violations(
    *,
    bound_argument_queue: dict[str, Any],
    odd_prime_local_image_schemas: dict[str, Any],
    tangent_one_reduction_partition: dict[str, Any],
    tangent_minus_one_reduction_partition: dict[str, Any],
) -> list[str]:
    violations: list[str] = []
    if _int(odd_prime_local_image_schemas, "local_image_schema_proved_count") != 0:
        violations.append("local_image_schema_claim_count_nonzero")
    if (
        _int(tangent_one_reduction_partition, "formal_lift_compatibility_proved_count")
        != 0
        or _int(
            tangent_minus_one_reduction_partition,
            "formal_lift_compatibility_proved_count",
        )
        != 0
    ):
        violations.append("formal_lift_compatibility_claim_count_nonzero")

    for name, payload in (
        ("bound_argument_queue", bound_argument_queue),
        ("odd_prime_local_image_schemas", odd_prime_local_image_schemas),
        ("tangent_one_reduction_partition", tangent_one_reduction_partition),
        ("tangent_minus_one_reduction_partition", tangent_minus_one_reduction_partition),
    ):
        if _int(payload, "selmer_rank_upper_bound_proved_count") != 0:
            violations.append(f"{name}_selmer_rank_upper_bound_claim_count_nonzero")
        if _int(payload, "family_exclusion_proved_count") != 0:
            violations.append(f"{name}_family_exclusion_claim_count_nonzero")
        if payload.get("search_count_used_as_progress") is not False:
            violations.append(f"{name}_search_count_used_as_progress")
    return violations


def _reduction_partition_entries(*payloads: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for payload in payloads:
        entries.extend(dict(entry) for entry in payload.get("partition_entries", []))
    return sorted(entries, key=lambda entry: str(entry.get("schema_id", "")))


def _outline(
    *,
    task: dict[str, Any],
    shared_schema_count: int,
    reduction_partition_count: int,
) -> dict[str, Any]:
    return {
        "package_id": str(task.get("package_id", "")),
        "family_pattern": str(task.get("family_pattern", "")),
        "kernel": str(task.get("kernel", "")),
        "required_argument": PRIMARY_REMAINING_PROOF_FIELD,
        "required_sections": REQUIRED_SECTIONS,
        "shared_odd_prime_local_image_schema_count": shared_schema_count,
        "reduction_partition_outline_count": reduction_partition_count,
        "acceptable_next_evidence": str(task.get("acceptable_next_evidence", "")),
        "status": "open",
        "proof_status": "sections-open-not-proof",
        "selmer_rank_upper_bound_proved": False,
        "family_exclusion_proved": False,
    }


def audit_rank_zero_selmer_bound_argument_sections(
    *,
    bound_argument_queue: dict[str, Any],
    odd_prime_local_image_schemas: dict[str, Any],
    tangent_one_reduction_partition: dict[str, Any],
    tangent_minus_one_reduction_partition: dict[str, Any],
) -> dict[str, Any]:
    checks = {
        "bound_argument_queue_ready": _ready(bound_argument_queue),
        "odd_prime_local_image_schemas_ready": _ready(odd_prime_local_image_schemas),
        "tangent_one_reduction_partition_ready": _ready(
            tangent_one_reduction_partition
        ),
        "tangent_minus_one_reduction_partition_ready": _ready(
            tangent_minus_one_reduction_partition
        ),
        "primary_remaining_proof_field_is_selmer_bound_argument": (
            bound_argument_queue.get("primary_remaining_proof_field")
            == PRIMARY_REMAINING_PROOF_FIELD
        ),
        "local_image_schemas_not_conditions": (
            odd_prime_local_image_schemas.get("local_image_schemas_not_conditions")
            is True
        ),
        "tangent_one_reduction_partition_not_local_image": (
            tangent_one_reduction_partition.get("reduction_partition_not_local_image")
            is True
        ),
        "tangent_minus_one_reduction_partition_not_local_image": (
            tangent_minus_one_reduction_partition.get("reduction_partition_not_local_image")
            is True
        ),
    }
    violation_names = {
        "primary_remaining_proof_field_is_selmer_bound_argument": (
            "primary_remaining_proof_field_not_selmer_bound_argument"
        ),
        "local_image_schemas_not_conditions": "local_image_schema_boundary_missing",
        "tangent_one_reduction_partition_not_local_image": (
            "tangent_one_reduction_partition_boundary_missing"
        ),
        "tangent_minus_one_reduction_partition_not_local_image": (
            "tangent_minus_one_reduction_partition_boundary_missing"
        ),
    }
    violations = [
        violation_names.get(name, name)
        for name, passed in checks.items()
        if not passed
    ]
    violations.extend(
        _proof_count_violations(
            bound_argument_queue=bound_argument_queue,
            odd_prime_local_image_schemas=odd_prime_local_image_schemas,
            tangent_one_reduction_partition=tangent_one_reduction_partition,
            tangent_minus_one_reduction_partition=tangent_minus_one_reduction_partition,
        )
    )

    shared_schema_count = len(odd_prime_local_image_schemas.get("schemas", []))
    reduction_entries = _reduction_partition_entries(
        tangent_one_reduction_partition,
        tangent_minus_one_reduction_partition,
    )
    argument_outlines = [
        _outline(
            task=task,
            shared_schema_count=shared_schema_count,
            reduction_partition_count=len(reduction_entries),
        )
        for task in sorted(
            bound_argument_queue.get("tasks", []),
            key=lambda row: str(row.get("package_id", "")),
        )
        if str(task.get("required_argument", "")) == PRIMARY_REMAINING_PROOF_FIELD
    ]

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "bound_argument_outline_count": len(argument_outlines),
        "open_bound_argument_outline_count": sum(
            1 for outline in argument_outlines if outline["status"] == "open"
        ),
        "required_section_per_outline_count": len(REQUIRED_SECTIONS),
        "required_section_count": len(argument_outlines) * len(REQUIRED_SECTIONS),
        "shared_odd_prime_local_image_schema_count": shared_schema_count,
        "reduction_partition_outline_count": len(reduction_entries),
        "formal_lift_compatibility_proved_count": 0,
        "local_image_schema_proved_count": 0,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "required_sections": REQUIRED_SECTIONS,
        "reduction_partition_outlines": reduction_entries,
        "argument_outlines": argument_outlines,
        "checks": checks,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bound-argument-queue", type=Path, required=True)
    parser.add_argument("--odd-prime-local-image-schemas", type=Path, required=True)
    parser.add_argument("--tangent-one-reduction-partition", type=Path, required=True)
    parser.add_argument("--tangent-minus-one-reduction-partition", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_bound_argument_sections(
        bound_argument_queue=load_json(args.bound_argument_queue),
        odd_prime_local_image_schemas=load_json(args.odd_prime_local_image_schemas),
        tangent_one_reduction_partition=load_json(
            args.tangent_one_reduction_partition
        ),
        tangent_minus_one_reduction_partition=load_json(
            args.tangent_minus_one_reduction_partition
        ),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer bound argument sections to {args.out}")
    print(f"status={audit['status']}")
    print(f"bound_argument_outline_count={audit['bound_argument_outline_count']}")
    print(f"required_section_count={audit['required_section_count']}")
    print(
        "local_image_schema_proved_count="
        f"{audit['local_image_schema_proved_count']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
