#!/usr/bin/env python3
"""Audit tangent-minus-one normal forms for odd-prime local-image schemas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits normal-form reductions for tangent-squareclass-minus-one "
    "odd-prime local-image schemas. It absorbs only the square-unit part and "
    "retains a nonsquare unit parameter nu; it does not prove local images, "
    "local conditions, Selmer rank bounds, or lambda-family exclusions."
)

NEXT_GAP = (
    "compute the 2-isogeny local squareclass image with nonsquare unit "
    "parameter nu"
)

NORMAL_FORMS = {
    "odd-prime-local-image-nonzero-double-root-tangent--1": {
        "nonsquare_unit_parameter": "nu",
        "unit_square_root_required": "choose u with u^2 = r/nu",
        "coordinate_change": "x = nu*u^2*X, y = nu*u^3*Y",
        "standard_model": "Y^2 = nu*X*(X - 1)^2",
    },
    "odd-prime-local-image-zero-double-root-tangent--1": {
        "nonsquare_unit_parameter": "nu",
        "unit_square_root_required": "choose u with u^2 = (-s)/nu",
        "coordinate_change": "x = -nu*u^2*X, y = nu*u^3*Y",
        "standard_model": "Y^2 = nu*X^2*(1 - X)",
    },
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _ready(schemas: dict[str, Any]) -> bool:
    return schemas.get("status") == "ok" and schemas.get("ready") is True


def _entry(schema: dict[str, Any]) -> dict[str, Any]:
    schema_id = str(schema.get("schema_id", ""))
    normal_form = NORMAL_FORMS[schema_id]
    return {
        "schema_id": schema_id,
        "nodal_reduction_shape": str(schema.get("nodal_reduction_shape", "")),
        "tangent_squareclass": str(schema.get("tangent_squareclass", "")),
        "source_model_shape": str(schema.get("model_shape", "")),
        **normal_form,
        "normal_form_proved": True,
        "local_image_schema_proved": False,
        "next_gap": NEXT_GAP,
    }


def audit_rank_zero_selmer_tangent_minus_one_normal_forms(
    *,
    odd_prime_local_image_schemas: dict[str, Any],
) -> dict[str, Any]:
    schemas = list(odd_prime_local_image_schemas.get("schemas", []))
    violations: list[str] = []
    if not _ready(odd_prime_local_image_schemas):
        violations.append("odd_prime_local_image_schemas_not_ready")
    if odd_prime_local_image_schemas.get("local_image_schemas_not_conditions") is not True:
        violations.append("local_image_schema_boundary_missing")
    if int(odd_prime_local_image_schemas.get("local_condition_proved_count", 0) or 0) != 0:
        violations.append("local_condition_claim_count_nonzero")
    if int(
        odd_prime_local_image_schemas.get("local_image_schema_proved_count", 0) or 0
    ) != 0:
        violations.append("local_image_schema_claim_count_nonzero")

    tangent_minus_one_schemas = [
        schema
        for schema in schemas
        if str(schema.get("tangent_squareclass", "")) == "-1"
    ]
    unsupported = sorted(
        {
            str(schema.get("schema_id", ""))
            for schema in tangent_minus_one_schemas
            if str(schema.get("schema_id", "")) not in NORMAL_FORMS
        }
    )
    if unsupported:
        violations.append(f"unsupported_tangent_minus_one_schemas={unsupported}")

    entries = [
        _entry(schema)
        for schema in tangent_minus_one_schemas
        if str(schema.get("schema_id", "")) in NORMAL_FORMS
    ]
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "input_schema_count": int(
            odd_prime_local_image_schemas.get("local_image_schema_count", 0) or 0
        ),
        "tangent_minus_one_schema_count": len(tangent_minus_one_schemas),
        "normal_form_count": len(entries),
        "normal_form_proved_count": len(entries),
        "nonsquare_parameter_retained": True,
        "normal_forms_not_local_images": True,
        "local_image_schema_proved_count": 0,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "normal_form_entries": entries,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--odd-prime-local-image-schemas", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_tangent_minus_one_normal_forms(
        odd_prime_local_image_schemas=load_json(args.odd_prime_local_image_schemas),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer tangent-minus-one normal forms to {args.out}")
    print(f"status={audit['status']}")
    print(f"input_schema_count={audit['input_schema_count']}")
    print(f"tangent_minus_one_schema_count={audit['tangent_minus_one_schema_count']}")
    print(f"normal_form_proved_count={audit['normal_form_proved_count']}")
    print(f"local_image_schema_proved_count={audit['local_image_schema_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
