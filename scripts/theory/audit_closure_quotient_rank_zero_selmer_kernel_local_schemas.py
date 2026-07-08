#!/usr/bin/env python3
"""Group rank-zero Selmer local-support candidates into kernel-local schemas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This groups symbolic rank-zero Selmer local-support candidates by kernel "
    "schema. It does not compute local Selmer images, prove a local condition, "
    "prove a Selmer rank bound, prove rank zero, or prove any lambda-family "
    "exclusion."
)

SIGNATURE_KEYS = (
    "target_a2",
    "target_a4",
    "a4_square_root",
    "quadratic_discriminant",
    "quadratic_discriminant_squareclass",
    "candidate_bad_factors",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _ready(local_supports: dict[str, Any]) -> bool:
    return local_supports.get("status") == "ok" and local_supports.get("ready") is True


def _signature(row: dict[str, Any]) -> tuple[Any, ...]:
    return tuple(
        tuple(row.get(key, [])) if key == "candidate_bad_factors" else row.get(key)
        for key in SIGNATURE_KEYS
    )


def _schema_id(kernel: str) -> str:
    return f"rank-zero-selmer-local-support-{kernel.replace('_', '-')}"


def audit_rank_zero_selmer_kernel_local_schemas(
    *,
    local_supports: dict[str, Any],
) -> dict[str, Any]:
    support_entries = list(local_supports.get("support_entries", []))
    violations: list[str] = []
    if not _ready(local_supports):
        violations.append("local_supports_not_ready")
    if local_supports.get("support_candidates_not_conditions") is not True:
        violations.append("support_candidates_promoted_to_conditions")
    if int(local_supports.get("local_condition_proved_count", 0) or 0) != 0:
        violations.append("local_condition_claim_count_nonzero")

    observed_family_patterns = sorted(
        {str(row.get("family_pattern", "")) for row in support_entries}
    )
    groups: dict[str, list[dict[str, Any]]] = {}
    for row in support_entries:
        kernel = str(row.get("kernel", ""))
        groups.setdefault(kernel, []).append(row)

    kernel_schemas: list[dict[str, Any]] = []
    shared_kernel_schema_count = 0
    for kernel in sorted(groups):
        rows = groups[kernel]
        reference = _signature(rows[0])
        if any(_signature(row) != reference for row in rows[1:]):
            violations.append(f"kernel_signature_mismatch={kernel}")
            continue

        family_patterns = sorted({str(row.get("family_pattern", "")) for row in rows})
        if family_patterns == observed_family_patterns:
            shared_kernel_schema_count += 1
        representative = rows[0]
        kernel_schemas.append(
            {
                "schema_id": _schema_id(kernel),
                "kernel": kernel,
                "family_patterns": family_patterns,
                "package_ids": sorted(str(row.get("package_id", "")) for row in rows),
                "package_count": len(rows),
                "target_a2": str(representative.get("target_a2", "")),
                "target_a4": str(representative.get("target_a4", "")),
                "a4_square_root": str(representative.get("a4_square_root", "")),
                "quadratic_discriminant": str(
                    representative.get("quadratic_discriminant", "")
                ),
                "quadratic_discriminant_squareclass": str(
                    representative.get("quadratic_discriminant_squareclass", "")
                ),
                "candidate_bad_factors": list(
                    representative.get("candidate_bad_factors", [])
                ),
                "support_candidates_not_conditions": True,
                "local_condition_proved": False,
                "selmer_rank_upper_bound_proved": False,
                "family_exclusion_proved": False,
            }
        )

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "package_count": int(local_supports.get("package_count", 0) or 0),
        "support_entry_count": int(local_supports.get("support_entry_count", 0) or 0),
        "family_pattern_count": len(observed_family_patterns),
        "kernel_schema_count": len(kernel_schemas),
        "shared_kernel_schema_count": shared_kernel_schema_count,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "kernel_schemas": kernel_schemas,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local-supports", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_kernel_local_schemas(
        local_supports=load_json(args.local_supports),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer kernel-local schema audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"kernel_schema_count={audit['kernel_schema_count']}")
    print(f"shared_kernel_schema_count={audit['shared_kernel_schema_count']}")
    print(f"local_condition_proved_count={audit['local_condition_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
