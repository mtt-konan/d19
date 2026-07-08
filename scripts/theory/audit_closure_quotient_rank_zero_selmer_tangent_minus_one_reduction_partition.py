#!/usr/bin/env python3
"""Audit tangent-minus-one reduction-level squareclass partitions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits reduction-level squareclass partitions for the "
    "tangent-minus-one standard nodal models. It records candidate "
    "squareclass sets and excluded punctured neighborhoods only at the "
    "reduction level; it does not prove formal lift compatibility, a local "
    "image, local condition, Selmer rank bound, or lambda-family exclusion."
)

PARTITION_TARGETS = (
    {
        "schema_id": "odd-prime-local-image-nonzero-double-root-tangent--1",
        "standard_model": "Y^2 = nu*X*(X - 1)^2",
        "tracked_coordinate": "X",
        "nonnode_branch_id": "tangent-minus-one-nonzero-double-root-nonnode-branch",
        "node_id": "tangent-minus-one-nonzero-double-root-node",
        "candidate_squareclass_set": ["nu", "trivial"],
        "candidate_sources": {
            "nu": "non-node branch",
            "trivial": "node center",
        },
        "excluded_reduction_pieces": ["punctured node neighborhood"],
    },
    {
        "schema_id": "odd-prime-local-image-zero-double-root-tangent--1",
        "standard_model": "Y^2 = nu*X^2*(1 - X)",
        "tracked_coordinate": "1 - X",
        "nonnode_branch_id": "tangent-minus-one-zero-double-root-nonnode-branch",
        "node_id": "tangent-minus-one-zero-double-root-node",
        "candidate_squareclass_set": ["nu", "trivial"],
        "candidate_sources": {
            "nu": "non-node branch",
            "trivial": "node center",
        },
        "excluded_reduction_pieces": ["punctured node neighborhood"],
    },
)

REDUCTION_PIECES = [
    "non-node branch",
    "punctured node neighborhood",
    "node center",
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


def _by_schema(entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(entry.get("schema_id", "")): dict(entry) for entry in entries}


def _boundary_violations(
    *,
    nonnode_branches: dict[str, Any],
    node_values: dict[str, Any],
    punctured_nodes: dict[str, Any],
) -> list[str]:
    violations: list[str] = []
    if nonnode_branches.get("nonnode_results_not_local_images") is not True:
        violations.append("nonnode_boundary_missing")
    if node_values.get("node_values_not_local_images") is not True:
        violations.append("node_value_boundary_missing")
    if punctured_nodes.get("punctured_node_results_not_local_images") is not True:
        violations.append("punctured_node_boundary_missing")
    for name, payload in (
        ("nonnode", nonnode_branches),
        ("node", node_values),
        ("punctured", punctured_nodes),
    ):
        if int(payload.get("local_image_schema_proved_count", 0) or 0) != 0:
            violations.append(f"{name}_local_image_schema_claim_count_nonzero")
        if int(payload.get("local_condition_proved_count", 0) or 0) != 0:
            violations.append(f"{name}_local_condition_claim_count_nonzero")
    return violations


def _partition_entry(target: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_id": str(target["schema_id"]),
        "standard_model": str(target["standard_model"]),
        "tracked_coordinate": str(target["tracked_coordinate"]),
        "reduction_pieces": REDUCTION_PIECES,
        "candidate_squareclass_set": list(target["candidate_squareclass_set"]),
        "candidate_sources": dict(target["candidate_sources"]),
        "excluded_reduction_pieces": list(target["excluded_reduction_pieces"]),
        "reduction_partition_exhausted": True,
        "formal_lift_compatibility_proved": False,
        "local_image_schema_proved": False,
        "remaining_gap": "promote reduction-level partition through formal lifts",
    }


def audit_rank_zero_selmer_tangent_minus_one_reduction_partition(
    *,
    nonnode_branches: dict[str, Any],
    node_values: dict[str, Any],
    punctured_nodes: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(nonnode_branches):
        violations.append("nonnode_branches_not_ready")
    if not _ready(node_values):
        violations.append("node_values_not_ready")
    if not _ready(punctured_nodes):
        violations.append("punctured_nodes_not_ready")
    for name, payload in (
        ("nonnode", nonnode_branches),
        ("node", node_values),
        ("punctured", punctured_nodes),
    ):
        if payload.get("nonsquare_parameter_retained") is not True:
            violations.append(f"{name}_nonsquare_parameter_not_retained")
    violations.extend(
        _boundary_violations(
            nonnode_branches=nonnode_branches,
            node_values=node_values,
            punctured_nodes=punctured_nodes,
        )
    )

    nonnode_by_schema = _by_schema(
        list(nonnode_branches.get("nonnode_branch_entries", []))
    )
    node_by_schema = _by_schema(list(node_values.get("node_value_entries", [])))
    punctured_by_schema = _by_schema(
        list(punctured_nodes.get("punctured_node_entries", []))
    )

    entries: list[dict[str, Any]] = []
    for target in PARTITION_TARGETS:
        schema_id = str(target["schema_id"])
        nonnode_entry = nonnode_by_schema.get(schema_id)
        node_entry = node_by_schema.get(schema_id)
        punctured_entry = punctured_by_schema.get(schema_id)
        if nonnode_entry is None:
            violations.append(f"nonnode_branch_missing={schema_id}")
            continue
        if node_entry is None:
            violations.append(f"node_value_missing={schema_id}")
            continue
        if punctured_entry is None:
            violations.append(f"punctured_node_missing={schema_id}")
            continue
        if str(nonnode_entry.get("branch_id", "")) != str(target["nonnode_branch_id"]):
            violations.append(f"nonnode_branch_id_mismatch={schema_id}")
            continue
        if str(node_entry.get("node_id", "")) != str(target["node_id"]):
            violations.append(f"node_id_mismatch={schema_id}")
            continue
        if str(punctured_entry.get("controlled_by_nonnode_branch_id", "")) != str(
            target["nonnode_branch_id"]
        ):
            violations.append(f"punctured_control_mismatch={schema_id}")
            continue
        if punctured_entry.get("punctured_node_neighborhood_excluded") is not True:
            violations.append(f"punctured_node_not_excluded={schema_id}")
            continue
        entries.append(_partition_entry(target))

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "input_nonnode_branch_count": int(
            nonnode_branches.get("nonnode_branch_count", 0) or 0
        ),
        "input_node_value_count": int(node_values.get("node_value_count", 0) or 0),
        "input_punctured_node_count": int(
            punctured_nodes.get("punctured_node_neighborhood_count", 0) or 0
        ),
        "reduction_partition_count": len(entries),
        "reduction_partition_exhausted_count": sum(
            1 for entry in entries if entry["reduction_partition_exhausted"] is True
        ),
        "candidate_squareclass_set_count": len(entries),
        "punctured_node_neighborhood_excluded_count": int(
            punctured_nodes.get("punctured_node_neighborhood_excluded_count", 0) or 0
        ),
        "formal_lift_compatibility_proved_count": 0,
        "nonsquare_parameter_retained": True,
        "reduction_partition_not_local_image": True,
        "local_image_schema_proved_count": 0,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "partition_entries": entries,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nonnode-branches", type=Path, required=True)
    parser.add_argument("--node-values", type=Path, required=True)
    parser.add_argument("--punctured-nodes", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_tangent_minus_one_reduction_partition(
        nonnode_branches=load_json(args.nonnode_branches),
        node_values=load_json(args.node_values),
        punctured_nodes=load_json(args.punctured_nodes),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer tangent-minus-one reduction partition to {args.out}")
    print(f"status={audit['status']}")
    print(f"reduction_partition_count={audit['reduction_partition_count']}")
    print(
        "reduction_partition_exhausted_count="
        f"{audit['reduction_partition_exhausted_count']}"
    )
    print(
        "punctured_node_neighborhood_excluded_count="
        f"{audit['punctured_node_neighborhood_excluded_count']}"
    )
    print(
        "formal_lift_compatibility_proved_count="
        f"{audit['formal_lift_compatibility_proved_count']}"
    )
    print(f"local_image_schema_proved_count={audit['local_image_schema_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
