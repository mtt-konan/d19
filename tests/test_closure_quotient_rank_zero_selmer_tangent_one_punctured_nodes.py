from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory import (
    audit_closure_quotient_rank_zero_selmer_tangent_one_punctured_nodes as punctured,
)

audit_rank_zero_selmer_tangent_one_punctured_nodes = (
    punctured.audit_rank_zero_selmer_tangent_one_punctured_nodes
)
write_json = punctured.write_json


def _nonnode_branches() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "input_normal_form_count": 2,
        "nonnode_branch_count": 2,
        "nonnode_squareclass_consequence_proved_count": 2,
        "nonnode_results_not_local_images": True,
        "local_image_schema_proved_count": 0,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "nonnode_branch_entries": [
            {
                "schema_id": "odd-prime-local-image-nonzero-double-root-tangent-1",
                "standard_model": "Y^2 = X*(X - 1)^2",
                "branch_id": "tangent-one-nonzero-double-root-nonnode-branch",
                "branch_hypothesis": "X - 1 is nonzero in the local field",
                "identity": "X = (Y/(X - 1))^2",
                "squareclass_consequence": (
                    "X has trivial local squareclass on every non-node branch"
                ),
                "branch_squareclass_consequence_proved": True,
                "local_image_schema_proved": False,
            },
            {
                "schema_id": "odd-prime-local-image-zero-double-root-tangent-1",
                "standard_model": "Y^2 = X^2*(X - 1)",
                "branch_id": "tangent-one-zero-double-root-nonnode-branch",
                "branch_hypothesis": "X is nonzero in the local field",
                "identity": "X - 1 = (Y/X)^2",
                "squareclass_consequence": (
                    "X - 1 has trivial local squareclass on every non-node branch"
                ),
                "branch_squareclass_consequence_proved": True,
                "local_image_schema_proved": False,
            },
        ],
        "violations": [],
    }


def _node_values() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "input_normal_form_count": 2,
        "node_value_count": 2,
        "node_reduction_value_proved_count": 2,
        "node_local_lift_analysis_proved_count": 0,
        "node_values_not_local_images": True,
        "local_image_schema_proved_count": 0,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "node_value_entries": [
            {
                "schema_id": "odd-prime-local-image-nonzero-double-root-tangent-1",
                "standard_model": "Y^2 = X*(X - 1)^2",
                "node_id": "tangent-one-nonzero-double-root-node",
                "node_coordinates": {"X": "1", "Y": "0"},
                "coordinate_value": "X = 1",
                "squareclass_value": "trivial",
                "node_reduction_value_proved": True,
                "local_lift_analysis_proved": False,
            },
            {
                "schema_id": "odd-prime-local-image-zero-double-root-tangent-1",
                "standard_model": "Y^2 = X^2*(X - 1)",
                "node_id": "tangent-one-zero-double-root-node",
                "node_coordinates": {"X": "0", "Y": "0"},
                "coordinate_value": "X - 1 = -1",
                "squareclass_value": "-1",
                "node_reduction_value_proved": True,
                "local_lift_analysis_proved": False,
            },
        ],
        "violations": [],
    }


def test_tangent_one_punctured_nodes_record_controlled_neighborhoods() -> None:
    audit = audit_rank_zero_selmer_tangent_one_punctured_nodes(
        nonnode_branches=_nonnode_branches(),
        node_values=_node_values(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["punctured_node_neighborhood_count"] == 2
    assert audit["punctured_node_neighborhood_control_proved_count"] == 2
    assert audit["node_center_lift_analysis_proved_count"] == 0
    assert audit["local_image_schema_proved_count"] == 0
    assert audit["local_condition_proved_count"] == 0
    assert audit["punctured_node_entries"] == [
        {
            "schema_id": "odd-prime-local-image-nonzero-double-root-tangent-1",
            "standard_model": "Y^2 = X*(X - 1)^2",
            "node_id": "tangent-one-nonzero-double-root-node",
            "punctured_neighborhood_hypothesis": "X - 1 is nonzero and has positive valuation",
            "controlled_by_nonnode_branch_id": (
                "tangent-one-nonzero-double-root-nonnode-branch"
            ),
            "identity": "X = (Y/(X - 1))^2",
            "squareclass_consequence": (
                "X has trivial local squareclass on the punctured node neighborhood"
            ),
            "node_center_value": "X = 1",
            "punctured_node_neighborhood_control_proved": True,
            "node_center_lift_analysis_proved": False,
            "remaining_gap": "prove formal lift compatibility at the node center",
        },
        {
            "schema_id": "odd-prime-local-image-zero-double-root-tangent-1",
            "standard_model": "Y^2 = X^2*(X - 1)",
            "node_id": "tangent-one-zero-double-root-node",
            "punctured_neighborhood_hypothesis": "X is nonzero and has positive valuation",
            "controlled_by_nonnode_branch_id": (
                "tangent-one-zero-double-root-nonnode-branch"
            ),
            "identity": "X - 1 = (Y/X)^2",
            "squareclass_consequence": (
                "X - 1 has trivial local squareclass on the punctured node neighborhood"
            ),
            "node_center_value": "X - 1 = -1",
            "punctured_node_neighborhood_control_proved": True,
            "node_center_lift_analysis_proved": False,
            "remaining_gap": "prove formal lift compatibility at the node center",
        },
    ]
    assert audit["punctured_node_results_not_local_images"] is True
    assert audit["search_count_used_as_progress"] is False


def test_tangent_one_punctured_nodes_reject_unready_inputs() -> None:
    nonnode = _nonnode_branches()
    nonnode["ready"] = False
    nonnode["status"] = "issues"

    audit = audit_rank_zero_selmer_tangent_one_punctured_nodes(
        nonnode_branches=nonnode,
        node_values=_node_values(),
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["nonnode_branches_not_ready"]


def test_tangent_one_punctured_nodes_cli_writes_audit(tmp_path: Path) -> None:
    nonnode = tmp_path / "nonnode.json"
    nodes = tmp_path / "node_values.json"
    out = tmp_path / "punctured_nodes.json"
    nonnode.write_text(json.dumps(_nonnode_branches()), encoding="utf-8")
    nodes.write_text(json.dumps(_node_values()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_one_punctured_nodes.py",
            "--nonnode-branches",
            str(nonnode),
            "--node-values",
            str(nodes),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "punctured_node_neighborhood_control_proved_count=2" in result.stdout
    assert "node_center_lift_analysis_proved_count=0" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["punctured_node_results_not_local_images"] is True


def test_write_json_writes_sorted_tangent_one_punctured_nodes(tmp_path: Path) -> None:
    out = tmp_path / "punctured_nodes.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
