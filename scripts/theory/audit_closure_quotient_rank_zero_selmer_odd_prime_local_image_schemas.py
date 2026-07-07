#!/usr/bin/env python3
"""Audit local-image theorem schemas for odd-prime rank-zero Selmer lemmas."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This groups proved odd-prime reduced cubic shapes into local-image theorem "
    "schemas. It does not prove the local-image theorem, compute local Selmer "
    "images, prove local conditions, prove a Selmer rank bound, or prove any "
    "lambda-family exclusion."
)

SCHEMAS = {
    "split-nodal-cubic-with-nonzero-double-root": {
        "schema_id": "odd-prime-local-image-nonzero-double-root",
        "model_shape": "y^2 = x*(x-r)^2 with r a local unit",
        "unit_hypothesis": "r is nonzero modulo ell",
        "required_theorem": (
            "compute the 2-isogeny local squareclass image for the split nodal "
            "unit-double-root model"
        ),
    },
    "split-nodal-cubic-with-zero-double-root": {
        "schema_id": "odd-prime-local-image-zero-double-root",
        "model_shape": "y^2 = x^2*(x-s) with s a local unit",
        "unit_hypothesis": "s is nonzero modulo ell",
        "required_theorem": (
            "compute the 2-isogeny local squareclass image for the split nodal "
            "zero-double-root model"
        ),
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


def _ready(reduction_shapes: dict[str, Any]) -> bool:
    return (
        reduction_shapes.get("status") == "ok"
        and reduction_shapes.get("ready") is True
    )


def _schema_entry(shape: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    template = SCHEMAS[shape]
    return {
        "schema_id": template["schema_id"],
        "nodal_reduction_shape": shape,
        "model_shape": template["model_shape"],
        "unit_hypothesis": template["unit_hypothesis"],
        "covered_reduction_shape_count": len(rows),
        "covered_lemma_ids": sorted(str(row.get("lemma_id", "")) for row in rows),
        "required_theorem": template["required_theorem"],
        "proof_status": "open",
        "local_image_schema_proved": False,
        "local_condition_proved": False,
    }


def audit_rank_zero_selmer_odd_prime_local_image_schemas(
    *,
    odd_prime_reduction_shapes: dict[str, Any],
) -> dict[str, Any]:
    reduction_entries = list(odd_prime_reduction_shapes.get("reduction_entries", []))
    violations: list[str] = []
    if not _ready(odd_prime_reduction_shapes):
        violations.append("odd_prime_reduction_shapes_not_ready")
    if odd_prime_reduction_shapes.get("reduction_shapes_not_local_conditions") is not True:
        violations.append("reduction_shape_boundary_missing")
    if int(odd_prime_reduction_shapes.get("local_condition_proved_count", 0) or 0) != 0:
        violations.append("local_condition_claim_count_nonzero")

    unknown_shapes = sorted(
        {
            str(row.get("nodal_reduction_shape", ""))
            for row in reduction_entries
            if str(row.get("nodal_reduction_shape", "")) not in SCHEMAS
        }
    )
    if unknown_shapes:
        violations.append(f"unknown_nodal_reduction_shapes={unknown_shapes}")

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in reduction_entries:
        shape = str(row.get("nodal_reduction_shape", ""))
        if shape in SCHEMAS:
            grouped[shape].append(row)

    schemas = [
        _schema_entry(shape, grouped[shape])
        for shape in [
            "split-nodal-cubic-with-nonzero-double-root",
            "split-nodal-cubic-with-zero-double-root",
        ]
        if shape in grouped
    ]
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "input_reduction_shape_count": len(reduction_entries),
        "local_image_schema_count": len(schemas),
        "local_image_schema_proved_count": 0,
        "local_image_schemas_not_conditions": True,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "schemas": schemas,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--odd-prime-reduction-shapes", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_odd_prime_local_image_schemas(
        odd_prime_reduction_shapes=load_json(args.odd_prime_reduction_shapes),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer odd-prime local-image schemas to {args.out}")
    print(f"status={audit['status']}")
    print(f"input_reduction_shape_count={audit['input_reduction_shape_count']}")
    print(f"local_image_schema_count={audit['local_image_schema_count']}")
    print(
        "local_image_schema_proved_count="
        f"{audit['local_image_schema_proved_count']}"
    )
    print(f"local_condition_proved_count={audit['local_condition_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
