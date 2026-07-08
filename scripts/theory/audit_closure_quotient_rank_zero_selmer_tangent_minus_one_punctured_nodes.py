#!/usr/bin/env python3
"""Audit tangent-minus-one punctured node-neighborhood obstructions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits squareclass contradictions on punctured neighborhoods of the "
    "tangent-minus-one nodes by comparing the non-node branch identities with "
    "the trivial squareclass of principal units near the node. It does not "
    "prove node-center lift analysis, a local image, local condition, Selmer "
    "rank bound, or lambda-family exclusion."
)

PUNCTURED_NODE_TARGETS = (
    {
        "schema_id": "odd-prime-local-image-nonzero-double-root-tangent--1",
        "standard_model": "Y^2 = nu*X*(X - 1)^2",
        "node_id": "tangent-minus-one-nonzero-double-root-node",
        "punctured_neighborhood_hypothesis": "X - 1 has positive valuation",
        "controlled_by_nonnode_branch_id": (
            "tangent-minus-one-nonzero-double-root-nonnode-branch"
        ),
        "near_node_squareclass": "X has trivial squareclass",
        "nonnode_required_squareclass": "X has squareclass nu",
        "squareclass_contradiction": "trivial != nu",
        "punctured_node_neighborhood_excluded": True,
        "node_center_value": "X = 1",
        "node_center_lift_analysis_proved": False,
        "remaining_gap": "prove formal lift compatibility at the node center",
    },
    {
        "schema_id": "odd-prime-local-image-zero-double-root-tangent--1",
        "standard_model": "Y^2 = nu*X^2*(1 - X)",
        "node_id": "tangent-minus-one-zero-double-root-node",
        "punctured_neighborhood_hypothesis": "X has positive valuation",
        "controlled_by_nonnode_branch_id": (
            "tangent-minus-one-zero-double-root-nonnode-branch"
        ),
        "near_node_squareclass": "1 - X has trivial squareclass",
        "nonnode_required_squareclass": "1 - X has squareclass nu",
        "squareclass_contradiction": "trivial != nu",
        "punctured_node_neighborhood_excluded": True,
        "node_center_value": "1 - X = 1",
        "node_center_lift_analysis_proved": False,
        "remaining_gap": "prove formal lift compatibility at the node center",
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


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


def _by_schema(entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(entry.get("schema_id", "")): dict(entry) for entry in entries}


def _boundary_violations(
    *,
    nonnode_branches: dict[str, Any],
    node_values: dict[str, Any],
) -> list[str]:
    violations: list[str] = []
    if nonnode_branches.get("nonnode_results_not_local_images") is not True:
        violations.append("nonnode_boundary_missing")
    if node_values.get("node_values_not_local_images") is not True:
        violations.append("node_value_boundary_missing")
    for name, payload in (
        ("nonnode", nonnode_branches),
        ("node", node_values),
    ):
        if int(payload.get("local_image_schema_proved_count", 0) or 0) != 0:
            violations.append(f"{name}_local_image_schema_claim_count_nonzero")
        if int(payload.get("local_condition_proved_count", 0) or 0) != 0:
            violations.append(f"{name}_local_condition_claim_count_nonzero")
    return violations


def audit_rank_zero_selmer_tangent_minus_one_punctured_nodes(
    *,
    nonnode_branches: dict[str, Any],
    node_values: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(nonnode_branches):
        violations.append("nonnode_branches_not_ready")
    if not _ready(node_values):
        violations.append("node_values_not_ready")
    if nonnode_branches.get("nonsquare_parameter_retained") is not True:
        violations.append("nonnode_nonsquare_parameter_not_retained")
    if node_values.get("nonsquare_parameter_retained") is not True:
        violations.append("node_nonsquare_parameter_not_retained")
    violations.extend(
        _boundary_violations(
            nonnode_branches=nonnode_branches,
            node_values=node_values,
        )
    )

    nonnode_by_schema = _by_schema(
        list(nonnode_branches.get("nonnode_branch_entries", []))
    )
    node_by_schema = _by_schema(list(node_values.get("node_value_entries", [])))

    entries: list[dict[str, Any]] = []
    for target in PUNCTURED_NODE_TARGETS:
        schema_id = str(target["schema_id"])
        nonnode_entry = nonnode_by_schema.get(schema_id)
        node_entry = node_by_schema.get(schema_id)
        if nonnode_entry is None:
            violations.append(f"nonnode_branch_missing={schema_id}")
            continue
        if node_entry is None:
            violations.append(f"node_value_missing={schema_id}")
            continue
        if str(nonnode_entry.get("branch_id", "")) != str(
            target["controlled_by_nonnode_branch_id"]
        ):
            violations.append(f"nonnode_branch_id_mismatch={schema_id}")
            continue
        if str(node_entry.get("coordinate_value", "")) != str(
            target["node_center_value"]
        ):
            violations.append(f"node_value_mismatch={schema_id}")
            continue
        entries.append(dict(target))

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "input_nonnode_branch_count": int(
            nonnode_branches.get("nonnode_branch_count", 0) or 0
        ),
        "input_node_value_count": int(node_values.get("node_value_count", 0) or 0),
        "punctured_node_neighborhood_count": len(entries),
        "punctured_node_neighborhood_excluded_count": len(entries),
        "squareclass_contradiction_proved_count": len(entries),
        "node_center_lift_analysis_proved_count": 0,
        "nonsquare_parameter_retained": True,
        "punctured_node_results_not_local_images": True,
        "local_image_schema_proved_count": 0,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "punctured_node_entries": entries,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nonnode-branches", type=Path, required=True)
    parser.add_argument("--node-values", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_tangent_minus_one_punctured_nodes(
        nonnode_branches=load_json(args.nonnode_branches),
        node_values=load_json(args.node_values),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer tangent-minus-one punctured node audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"input_nonnode_branch_count={audit['input_nonnode_branch_count']}")
    print(f"input_node_value_count={audit['input_node_value_count']}")
    print(
        "punctured_node_neighborhood_excluded_count="
        f"{audit['punctured_node_neighborhood_excluded_count']}"
    )
    print(
        "node_center_lift_analysis_proved_count="
        f"{audit['node_center_lift_analysis_proved_count']}"
    )
    print(f"local_image_schema_proved_count={audit['local_image_schema_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
