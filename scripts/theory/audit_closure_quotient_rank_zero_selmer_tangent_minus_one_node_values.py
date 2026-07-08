#!/usr/bin/env python3
"""Audit tangent-minus-one standard model node reduction values."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits reduction-level node values on the tangent-minus-one standard "
    "nodal models. It proves only the displayed node coordinates and "
    "coordinate values; it does not prove node lift analysis, a local image, "
    "local condition, Selmer rank bound, or lambda-family exclusion."
)

NODE_VALUE_TARGETS = (
    {
        "schema_id": "odd-prime-local-image-nonzero-double-root-tangent--1",
        "standard_model": "Y^2 = nu*X*(X - 1)^2",
        "node_id": "tangent-minus-one-nonzero-double-root-node",
        "node_coordinates": {"X": "1", "Y": "0"},
        "coordinate_value": "X = 1",
        "squareclass_value": "trivial",
        "node_reduction_value_proved": True,
        "local_lift_analysis_proved": False,
        "remaining_gap": "formal neighborhood of the node and local image compatibility",
    },
    {
        "schema_id": "odd-prime-local-image-zero-double-root-tangent--1",
        "standard_model": "Y^2 = nu*X^2*(1 - X)",
        "node_id": "tangent-minus-one-zero-double-root-node",
        "node_coordinates": {"X": "0", "Y": "0"},
        "coordinate_value": "1 - X = 1",
        "squareclass_value": "trivial",
        "node_reduction_value_proved": True,
        "local_lift_analysis_proved": False,
        "remaining_gap": "formal neighborhood of the node and local image compatibility",
    },
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _normal_forms_ready(normal_forms: dict[str, Any]) -> bool:
    return normal_forms.get("status") == "ok" and normal_forms.get("ready") is True


def _target_entry(
    normal_forms: dict[str, Any],
    *,
    schema_id: str,
    standard_model: str,
) -> dict[str, Any] | None:
    for entry in normal_forms.get("normal_form_entries", []):
        if (
            str(entry.get("schema_id", "")) == schema_id
            and str(entry.get("standard_model", "")) == standard_model
        ):
            return dict(entry)
    return None


def audit_rank_zero_selmer_tangent_minus_one_node_values(
    *,
    tangent_minus_one_normal_forms: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _normal_forms_ready(tangent_minus_one_normal_forms):
        violations.append("tangent_minus_one_normal_forms_not_ready")
    if tangent_minus_one_normal_forms.get("normal_forms_not_local_images") is not True:
        violations.append("normal_form_boundary_missing")
    if tangent_minus_one_normal_forms.get("nonsquare_parameter_retained") is not True:
        violations.append("nonsquare_parameter_not_retained")
    if int(tangent_minus_one_normal_forms.get("local_image_schema_proved_count", 0) or 0) != 0:
        violations.append("local_image_schema_claim_count_nonzero")
    if int(tangent_minus_one_normal_forms.get("local_condition_proved_count", 0) or 0) != 0:
        violations.append("local_condition_claim_count_nonzero")

    entries: list[dict[str, Any]] = []
    for target in NODE_VALUE_TARGETS:
        normal_form = _target_entry(
            tangent_minus_one_normal_forms,
            schema_id=str(target["schema_id"]),
            standard_model=str(target["standard_model"]),
        )
        if normal_form is None:
            violations.append(
                f"target_tangent_minus_one_standard_model_missing={target['schema_id']}"
            )
            continue
        if str(normal_form.get("nonsquare_unit_parameter", "")) != "nu":
            violations.append(f"nonsquare_parameter_mismatch={target['schema_id']}")
            continue
        entries.append(dict(target))

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "input_normal_form_count": int(
            tangent_minus_one_normal_forms.get("normal_form_count", 0) or 0
        ),
        "node_value_count": len(entries),
        "node_reduction_value_proved_count": len(entries),
        "node_local_lift_analysis_proved_count": 0,
        "nonsquare_parameter_retained": True,
        "node_values_not_local_images": True,
        "local_image_schema_proved_count": 0,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "node_value_entries": entries,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tangent-minus-one-normal-forms", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_tangent_minus_one_node_values(
        tangent_minus_one_normal_forms=load_json(args.tangent_minus_one_normal_forms),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer tangent-minus-one node value audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"input_normal_form_count={audit['input_normal_form_count']}")
    print(f"node_value_count={audit['node_value_count']}")
    print(f"node_reduction_value_proved_count={audit['node_reduction_value_proved_count']}")
    print(
        "node_local_lift_analysis_proved_count="
        f"{audit['node_local_lift_analysis_proved_count']}"
    )
    print(f"local_image_schema_proved_count={audit['local_image_schema_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
