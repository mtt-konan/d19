#!/usr/bin/env python3
"""Audit package-level rank-zero Selmer bound argument tasks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This turns the remaining rank-zero Selmer transcript blocker into an "
    "explicit package-level selmer_bound_argument queue. It does not prove a "
    "Selmer rank bound, prove rank zero, or prove any lambda-family exclusion."
)

PRIMARY_REMAINING_PROOF_FIELD = "selmer_bound_argument"
SHARED_SETUP_FIELDS = ["local_squareclass_conditions", "isogeny_setup"]
ACCEPTABLE_NEXT_EVIDENCE = "reviewable package-level Selmer bound argument transcript"


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


def _family_targets(
    family_conclusion_templates: dict[str, Any],
) -> dict[str, str]:
    targets: dict[str, str] = {}
    for template in family_conclusion_templates.get("family_conclusion_templates", []):
        family_pattern = str(template.get("family_pattern", ""))
        for package in template.get("required_kernel_bound_packages", []):
            package_id = str(package.get("package_id", ""))
            if package_id:
                targets[package_id] = family_pattern
    return targets


def _setup_templates_by_kernel(
    isogeny_setup_templates: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    return {
        str(template.get("kernel", "")): template
        for template in isogeny_setup_templates.get("setup_templates", [])
    }


def _task(
    *,
    row: dict[str, Any],
    setup_template: dict[str, Any] | None,
    target_family_conclusion: str,
) -> dict[str, Any]:
    kernel = str(row.get("kernel", ""))
    kernel_schema_id = str(row.get("kernel_schema_id", ""))
    if setup_template is not None:
        kernel_schema_id = str(setup_template.get("kernel_schema_id", kernel_schema_id))

    return {
        "package_id": str(row.get("package_id", "")),
        "family_pattern": target_family_conclusion,
        "kernel": kernel,
        "kernel_schema_id": kernel_schema_id,
        "shared_setup_fields": SHARED_SETUP_FIELDS,
        "target_family_conclusion": target_family_conclusion,
        "required_argument": PRIMARY_REMAINING_PROOF_FIELD,
        "acceptable_next_evidence": ACCEPTABLE_NEXT_EVIDENCE,
        "status": "open",
        "selmer_rank_upper_bound_proved": False,
        "family_exclusion_proved": False,
    }


def audit_rank_zero_selmer_bound_argument_queue(
    *,
    field_decomposition: dict[str, Any],
    transcript_bridge: dict[str, Any],
    isogeny_setup_templates: dict[str, Any],
    family_conclusion_templates: dict[str, Any],
) -> dict[str, Any]:
    checks = {
        "field_decomposition_ready": _ready(field_decomposition),
        "transcript_bridge_ready": _ready(transcript_bridge),
        "isogeny_setup_templates_ready": _ready(isogeny_setup_templates),
        "family_conclusion_templates_ready": _ready(family_conclusion_templates),
        "primary_remaining_proof_field_is_selmer_bound_argument": (
            field_decomposition.get("primary_remaining_proof_field")
            == PRIMARY_REMAINING_PROOF_FIELD
        ),
        "selmer_rank_upper_bound_claim_count_zero": all(
            _int(payload, "selmer_rank_upper_bound_proved_count") == 0
            for payload in (
                field_decomposition,
                transcript_bridge,
                isogeny_setup_templates,
                family_conclusion_templates,
            )
        ),
        "family_exclusion_claim_count_zero": all(
            _int(payload, "family_exclusion_proved_count") == 0
            for payload in (
                field_decomposition,
                transcript_bridge,
                isogeny_setup_templates,
                family_conclusion_templates,
            )
        ),
        "search_count_not_used_as_progress": all(
            payload.get("search_count_used_as_progress") is False
            for payload in (
                field_decomposition,
                transcript_bridge,
                isogeny_setup_templates,
                family_conclusion_templates,
            )
        ),
    }
    violation_names = {
        "primary_remaining_proof_field_is_selmer_bound_argument": (
            "primary_remaining_proof_field_not_selmer_bound_argument"
        ),
        "selmer_rank_upper_bound_claim_count_zero": (
            "selmer_rank_upper_bound_claim_count_nonzero"
        ),
        "family_exclusion_claim_count_zero": "family_exclusion_claim_count_nonzero",
        "search_count_not_used_as_progress": "search_count_used_as_progress",
    }
    violations = [
        violation_names.get(name, name)
        for name, passed in checks.items()
        if not passed
    ]

    family_targets = _family_targets(family_conclusion_templates)
    setup_by_kernel = _setup_templates_by_kernel(isogeny_setup_templates)
    tasks: list[dict[str, Any]] = []

    for row in sorted(
        transcript_bridge.get("bridge_rows", []),
        key=lambda item: str(item.get("package_id", "")),
    ):
        package_id = str(row.get("package_id", ""))
        kernel = str(row.get("kernel", ""))
        target_family = family_targets.get(package_id)
        if target_family is None:
            violations.append(f"missing_family_conclusion_target={package_id}")
            continue
        if kernel not in setup_by_kernel:
            violations.append(f"missing_isogeny_setup_template={kernel}")
        tasks.append(
            _task(
                row=row,
                setup_template=setup_by_kernel.get(kernel),
                target_family_conclusion=target_family,
            )
        )

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "primary_remaining_proof_field": field_decomposition.get(
            "primary_remaining_proof_field"
        ),
        "bound_argument_task_count": len(tasks),
        "open_bound_argument_task_count": sum(
            1 for task in tasks if task["status"] == "open"
        ),
        "kernel_template_reuse_count": len({task["kernel"] for task in tasks}),
        "family_conclusion_target_count": len(
            {task["target_family_conclusion"] for task in tasks}
        ),
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "tasks": tasks,
        "checks": checks,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-decomposition", type=Path, required=True)
    parser.add_argument("--transcript-bridge", type=Path, required=True)
    parser.add_argument("--isogeny-setup-templates", type=Path, required=True)
    parser.add_argument("--family-conclusion-templates", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_bound_argument_queue(
        field_decomposition=load_json(args.field_decomposition),
        transcript_bridge=load_json(args.transcript_bridge),
        isogeny_setup_templates=load_json(args.isogeny_setup_templates),
        family_conclusion_templates=load_json(args.family_conclusion_templates),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer bound argument queue audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"primary_remaining_proof_field={audit['primary_remaining_proof_field']}")
    print(f"bound_argument_task_count={audit['bound_argument_task_count']}")
    print(f"open_bound_argument_task_count={audit['open_bound_argument_task_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
