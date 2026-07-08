#!/usr/bin/env python3
"""Audit shared isogeny-setup templates for rank-zero Selmer transcript tasks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This groups transcript isogeny-setup inputs by kernel template. It does "
    "not prove a local condition, prove a Selmer rank bound, prove rank zero, "
    "or prove any lambda-family exclusion."
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


def _package_payload(package: dict[str, Any]) -> dict[str, Any]:
    inline = package.get("package_payload")
    if isinstance(inline, dict):
        return inline
    return load_json(Path(str(package.get("json_path", ""))))


def _kernel_schema_map(kernel_local_schemas: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("kernel", "")): row
        for row in kernel_local_schemas.get("kernel_schemas", [])
    }


def audit_rank_zero_selmer_isogeny_setup_templates(
    *,
    materialization: dict[str, Any],
    kernel_local_schemas: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(materialization):
        violations.append("materialization_not_ready")
    if not _ready(kernel_local_schemas):
        violations.append("kernel_local_schemas_not_ready")

    schema_map = _kernel_schema_map(kernel_local_schemas)
    packages = sorted(
        materialization.get("packages", []),
        key=lambda row: str(row.get("package_id", "")),
    )
    grouped: dict[str, list[dict[str, Any]]] = {}
    for package in packages:
        payload = _package_payload(package)
        kernel = str(payload.get("kernel", ""))
        grouped.setdefault(kernel, []).append(payload)

    setup_templates: list[dict[str, Any]] = []
    for kernel in sorted(grouped):
        rows = grouped[kernel]
        schema = schema_map.get(kernel)
        if schema is None:
            violations.append(f"kernel_missing_schema={kernel}")
            continue
        reference_model = rows[0].get("symbolic_model", {})
        if any(row.get("symbolic_model", {}) != reference_model for row in rows[1:]):
            violations.append(f"kernel_symbolic_model_mismatch={kernel}")
            continue
        setup_templates.append(
            {
                "kernel": kernel,
                "kernel_schema_id": str(schema.get("schema_id", "")),
                "package_count": len(rows),
                "package_ids": sorted(str(row.get("package_id", "")) for row in rows),
                "symbolic_model": reference_model,
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
        "setup_template_count": len(setup_templates),
        "shared_isogeny_setup_template_count": len(setup_templates),
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "setup_templates": setup_templates,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--materialization", type=Path, required=True)
    parser.add_argument("--kernel-local-schemas", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_isogeny_setup_templates(
        materialization=load_json(args.materialization),
        kernel_local_schemas=load_json(args.kernel_local_schemas),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer isogeny-setup template audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"setup_template_count={audit['setup_template_count']}")
    print(
        "shared_isogeny_setup_template_count="
        f"{audit['shared_isogeny_setup_template_count']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
