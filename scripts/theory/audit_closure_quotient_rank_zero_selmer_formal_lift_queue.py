#!/usr/bin/env python3
"""Audit formal-lift theorem tasks for rank-zero Selmer local-image schemas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This turns reduction-level squareclass partitions into formal-lift "
    "compatibility theorem tasks. It does not prove formal lift compatibility, "
    "prove local-image schemas, prove local conditions, prove a Selmer rank "
    "bound, or prove any lambda-family exclusion."
)

REQUIRED_SECTION = "formal_lift_compatibility"
ACCEPTABLE_NEXT_EVIDENCE = (
    "reviewable formal-lift compatibility theorem for this local-image schema"
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


def _int(payload: dict[str, Any], key: str) -> int:
    return int(payload.get(key, 0) or 0)


def _task_id(schema_id: str) -> str:
    return f"formal-lift-{schema_id}"


def _entry_task(entry: dict[str, Any], source_partition: str) -> dict[str, Any]:
    excluded = list(entry.get("excluded_reduction_pieces", []))
    return {
        "task_id": _task_id(str(entry.get("schema_id", ""))),
        "schema_id": str(entry.get("schema_id", "")),
        "source_partition": source_partition,
        "standard_model": str(entry.get("standard_model", "")),
        "tracked_coordinate": str(entry.get("tracked_coordinate", "")),
        "reduction_pieces": list(entry.get("reduction_pieces", [])),
        "candidate_squareclass_set": list(entry.get("candidate_squareclass_set", [])),
        "excluded_reduction_pieces": excluded,
        "required_section": REQUIRED_SECTION,
        "acceptable_next_evidence": ACCEPTABLE_NEXT_EVIDENCE,
        "status": "open",
        "formal_lift_compatibility_proved": False,
        "local_image_schema_proved": False,
    }


def _partition_tasks(
    *,
    tangent_one_reduction_partition: dict[str, Any],
    tangent_minus_one_reduction_partition: dict[str, Any],
) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for entry in tangent_one_reduction_partition.get("partition_entries", []):
        tasks.append(_entry_task(dict(entry), "tangent_one_reduction_partition"))
    for entry in tangent_minus_one_reduction_partition.get("partition_entries", []):
        tasks.append(_entry_task(dict(entry), "tangent_minus_one_reduction_partition"))
    return sorted(tasks, key=lambda task: str(task["task_id"]))


def _proof_count_violations(
    *,
    bound_argument_sections: dict[str, Any],
    tangent_one_reduction_partition: dict[str, Any],
    tangent_minus_one_reduction_partition: dict[str, Any],
) -> list[str]:
    violations: list[str] = []
    if _int(bound_argument_sections, "formal_lift_compatibility_proved_count") != 0:
        violations.append(
            "bound_argument_sections_formal_lift_compatibility_claim_count_nonzero"
        )
    if _int(tangent_one_reduction_partition, "formal_lift_compatibility_proved_count"):
        violations.append("tangent_one_formal_lift_compatibility_claim_count_nonzero")
    if _int(
        tangent_minus_one_reduction_partition,
        "formal_lift_compatibility_proved_count",
    ):
        violations.append(
            "tangent_minus_one_formal_lift_compatibility_claim_count_nonzero"
        )
    for name, payload in (
        ("bound_argument_sections", bound_argument_sections),
        ("tangent_one", tangent_one_reduction_partition),
        ("tangent_minus_one", tangent_minus_one_reduction_partition),
    ):
        if _int(payload, "local_image_schema_proved_count") != 0:
            violations.append(f"{name}_local_image_schema_claim_count_nonzero")
        if _int(payload, "local_condition_proved_count") != 0:
            violations.append(f"{name}_local_condition_claim_count_nonzero")
        if _int(payload, "selmer_rank_upper_bound_proved_count") != 0:
            violations.append(f"{name}_selmer_rank_upper_bound_claim_count_nonzero")
        if _int(payload, "family_exclusion_proved_count") != 0:
            violations.append(f"{name}_family_exclusion_claim_count_nonzero")
        if payload.get("search_count_used_as_progress") is not False:
            violations.append(f"{name}_search_count_used_as_progress")
    return violations


def audit_rank_zero_selmer_formal_lift_queue(
    *,
    bound_argument_sections: dict[str, Any],
    tangent_one_reduction_partition: dict[str, Any],
    tangent_minus_one_reduction_partition: dict[str, Any],
) -> dict[str, Any]:
    checks = {
        "bound_argument_sections_ready": _ready(bound_argument_sections),
        "tangent_one_reduction_partition_ready": _ready(
            tangent_one_reduction_partition
        ),
        "tangent_minus_one_reduction_partition_ready": _ready(
            tangent_minus_one_reduction_partition
        ),
        "formal_lift_section_present": REQUIRED_SECTION
        in bound_argument_sections.get("required_sections", []),
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
        "formal_lift_section_present": "formal_lift_section_missing",
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
            bound_argument_sections=bound_argument_sections,
            tangent_one_reduction_partition=tangent_one_reduction_partition,
            tangent_minus_one_reduction_partition=tangent_minus_one_reduction_partition,
        )
    )

    tasks = _partition_tasks(
        tangent_one_reduction_partition=tangent_one_reduction_partition,
        tangent_minus_one_reduction_partition=tangent_minus_one_reduction_partition,
    )
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "covered_bound_argument_outline_count": _int(
            bound_argument_sections,
            "bound_argument_outline_count",
        ),
        "formal_lift_task_count": len(tasks),
        "open_formal_lift_task_count": sum(
            1 for task in tasks if task["status"] == "open"
        ),
        "reduction_partition_exhausted_count": sum(
            1
            for task in tasks
            if str(task["schema_id"])
            and task["required_section"] == REQUIRED_SECTION
        ),
        "formal_lift_compatibility_proved_count": 0,
        "local_image_schema_proved_count": 0,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "required_section": REQUIRED_SECTION,
        "formal_lift_tasks": tasks,
        "checks": checks,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bound-argument-sections", type=Path, required=True)
    parser.add_argument("--tangent-one-reduction-partition", type=Path, required=True)
    parser.add_argument("--tangent-minus-one-reduction-partition", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_formal_lift_queue(
        bound_argument_sections=load_json(args.bound_argument_sections),
        tangent_one_reduction_partition=load_json(
            args.tangent_one_reduction_partition
        ),
        tangent_minus_one_reduction_partition=load_json(
            args.tangent_minus_one_reduction_partition
        ),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer formal-lift queue to {args.out}")
    print(f"status={audit['status']}")
    print(f"covered_bound_argument_outline_count={audit['covered_bound_argument_outline_count']}")
    print(f"formal_lift_task_count={audit['formal_lift_task_count']}")
    print(f"open_formal_lift_task_count={audit['open_formal_lift_task_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
