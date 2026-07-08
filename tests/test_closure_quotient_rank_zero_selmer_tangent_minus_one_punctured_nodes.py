from __future__ import annotations

import importlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

MODULE_NAME = (
    "scripts.theory."
    "audit_closure_quotient_rank_zero_selmer_tangent_minus_one_punctured_nodes"
)


def _punctured_module() -> ModuleType:
    assert importlib.util.find_spec(MODULE_NAME) is not None
    return importlib.import_module(MODULE_NAME)


def _nonnode_branches() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "input_normal_form_count": 2,
        "nonnode_branch_count": 2,
        "nonnode_squareclass_consequence_proved_count": 2,
        "nonsquare_parameter_retained": True,
        "nonnode_results_not_local_images": True,
        "local_image_schema_proved_count": 0,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "nonnode_branch_entries": [
            {
                "schema_id": "odd-prime-local-image-nonzero-double-root-tangent--1",
                "standard_model": "Y^2 = nu*X*(X - 1)^2",
                "branch_id": "tangent-minus-one-nonzero-double-root-nonnode-branch",
                "branch_hypothesis": "X - 1 is nonzero in the local field",
                "identity": "nu*X = (Y/(X - 1))^2",
                "squareclass_consequence": (
                    "X has nonsquare local squareclass nu on every non-node branch"
                ),
                "branch_squareclass_consequence_proved": True,
                "local_image_schema_proved": False,
            },
            {
                "schema_id": "odd-prime-local-image-zero-double-root-tangent--1",
                "standard_model": "Y^2 = nu*X^2*(1 - X)",
                "branch_id": "tangent-minus-one-zero-double-root-nonnode-branch",
                "branch_hypothesis": "X is nonzero in the local field",
                "identity": "nu*(1 - X) = (Y/X)^2",
                "squareclass_consequence": (
                    "1 - X has nonsquare local squareclass nu on every non-node branch"
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
        "nonsquare_parameter_retained": True,
        "node_values_not_local_images": True,
        "local_image_schema_proved_count": 0,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "node_value_entries": [
            {
                "schema_id": "odd-prime-local-image-nonzero-double-root-tangent--1",
                "standard_model": "Y^2 = nu*X*(X - 1)^2",
                "node_id": "tangent-minus-one-nonzero-double-root-node",
                "node_coordinates": {"X": "1", "Y": "0"},
                "coordinate_value": "X = 1",
                "squareclass_value": "trivial",
                "node_reduction_value_proved": True,
                "local_lift_analysis_proved": False,
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
            },
        ],
        "violations": [],
    }


def test_tangent_minus_one_punctured_nodes_record_squareclass_obstructions() -> None:
    punctured = _punctured_module()

    audit = punctured.audit_rank_zero_selmer_tangent_minus_one_punctured_nodes(
        nonnode_branches=_nonnode_branches(),
        node_values=_node_values(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["punctured_node_neighborhood_count"] == 2
    assert audit["punctured_node_neighborhood_excluded_count"] == 2
    assert audit["squareclass_contradiction_proved_count"] == 2
    assert audit["node_center_lift_analysis_proved_count"] == 0
    assert audit["local_image_schema_proved_count"] == 0
    assert audit["local_condition_proved_count"] == 0
    assert audit["punctured_node_entries"] == [
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
    ]
    assert audit["punctured_node_results_not_local_images"] is True
    assert audit["search_count_used_as_progress"] is False


def test_tangent_minus_one_punctured_nodes_reject_unready_inputs() -> None:
    punctured = _punctured_module()
    node_values = _node_values()
    node_values["ready"] = False
    node_values["status"] = "issues"

    audit = punctured.audit_rank_zero_selmer_tangent_minus_one_punctured_nodes(
        nonnode_branches=_nonnode_branches(),
        node_values=node_values,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["node_values_not_ready"]


def test_tangent_minus_one_punctured_nodes_cli_writes_audit(tmp_path: Path) -> None:
    nonnode = tmp_path / "nonnode.json"
    nodes = tmp_path / "node_values.json"
    out = tmp_path / "punctured_nodes.json"
    nonnode.write_text(json.dumps(_nonnode_branches()), encoding="utf-8")
    nodes.write_text(json.dumps(_node_values()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_minus_one_punctured_nodes.py",
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

    assert "punctured_node_neighborhood_excluded_count=2" in result.stdout
    assert "node_center_lift_analysis_proved_count=0" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["punctured_node_results_not_local_images"] is True


def test_write_json_writes_sorted_tangent_minus_one_punctured_nodes(
    tmp_path: Path,
) -> None:
    punctured = _punctured_module()
    out = tmp_path / "minus_one_punctured_nodes.json"

    punctured.write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
