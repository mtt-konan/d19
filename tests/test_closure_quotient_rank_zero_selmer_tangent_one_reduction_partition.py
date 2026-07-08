from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory import (
    audit_closure_quotient_rank_zero_selmer_tangent_one_reduction_partition as partition,
)

audit_rank_zero_selmer_tangent_one_reduction_partition = (
    partition.audit_rank_zero_selmer_tangent_one_reduction_partition
)
write_json = partition.write_json


def _nonnode_branches() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "nonnode_branch_count": 2,
        "nonnode_squareclass_consequence_proved_count": 2,
        "nonnode_results_not_local_images": True,
        "local_image_schema_proved_count": 0,
        "local_condition_proved_count": 0,
        "nonnode_branch_entries": [
            {
                "schema_id": "odd-prime-local-image-nonzero-double-root-tangent-1",
                "branch_id": "tangent-one-nonzero-double-root-nonnode-branch",
                "squareclass_consequence": (
                    "X has trivial local squareclass on every non-node branch"
                ),
                "local_image_schema_proved": False,
            },
            {
                "schema_id": "odd-prime-local-image-zero-double-root-tangent-1",
                "branch_id": "tangent-one-zero-double-root-nonnode-branch",
                "squareclass_consequence": (
                    "1 - X has trivial local squareclass on every non-node branch"
                ),
                "local_image_schema_proved": False,
            },
        ],
    }


def _node_values() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "node_value_count": 2,
        "node_reduction_value_proved_count": 2,
        "node_local_lift_analysis_proved_count": 0,
        "node_values_not_local_images": True,
        "local_image_schema_proved_count": 0,
        "local_condition_proved_count": 0,
        "node_value_entries": [
            {
                "schema_id": "odd-prime-local-image-nonzero-double-root-tangent-1",
                "node_id": "tangent-one-nonzero-double-root-node",
                "coordinate_value": "X = 1",
                "squareclass_value": "trivial",
                "local_lift_analysis_proved": False,
            },
            {
                "schema_id": "odd-prime-local-image-zero-double-root-tangent-1",
                "node_id": "tangent-one-zero-double-root-node",
                "coordinate_value": "1 - X = 1",
                "squareclass_value": "trivial",
                "local_lift_analysis_proved": False,
            },
        ],
    }


def _punctured_nodes() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "punctured_node_neighborhood_count": 2,
        "punctured_node_neighborhood_control_proved_count": 2,
        "node_center_lift_analysis_proved_count": 0,
        "punctured_node_results_not_local_images": True,
        "local_image_schema_proved_count": 0,
        "local_condition_proved_count": 0,
        "punctured_node_entries": [
            {
                "schema_id": "odd-prime-local-image-nonzero-double-root-tangent-1",
                "node_id": "tangent-one-nonzero-double-root-node",
                "controlled_by_nonnode_branch_id": (
                    "tangent-one-nonzero-double-root-nonnode-branch"
                ),
                "squareclass_consequence": (
                    "X has trivial local squareclass on the punctured node neighborhood"
                ),
                "node_center_lift_analysis_proved": False,
            },
            {
                "schema_id": "odd-prime-local-image-zero-double-root-tangent-1",
                "node_id": "tangent-one-zero-double-root-node",
                "controlled_by_nonnode_branch_id": (
                    "tangent-one-zero-double-root-nonnode-branch"
                ),
                "squareclass_consequence": (
                    "1 - X has trivial local squareclass on the punctured node neighborhood"
                ),
                "node_center_lift_analysis_proved": False,
            },
        ],
    }


def test_tangent_one_reduction_partition_records_candidate_squareclasses() -> None:
    audit = audit_rank_zero_selmer_tangent_one_reduction_partition(
        nonnode_branches=_nonnode_branches(),
        node_values=_node_values(),
        punctured_nodes=_punctured_nodes(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["reduction_partition_count"] == 2
    assert audit["reduction_partition_exhausted_count"] == 2
    assert audit["candidate_squareclass_set_count"] == 2
    assert audit["formal_lift_compatibility_proved_count"] == 0
    assert audit["local_image_schema_proved_count"] == 0
    assert audit["local_condition_proved_count"] == 0
    assert audit["partition_entries"] == [
        {
            "schema_id": "odd-prime-local-image-nonzero-double-root-tangent-1",
            "standard_model": "Y^2 = X*(X - 1)^2",
            "tracked_coordinate": "X",
            "reduction_pieces": [
                "non-node branch",
                "punctured node neighborhood",
                "node center",
            ],
            "candidate_squareclass_set": ["trivial"],
            "reduction_partition_exhausted": True,
            "formal_lift_compatibility_proved": False,
            "local_image_schema_proved": False,
            "remaining_gap": "promote reduction-level partition through formal lifts",
        },
        {
            "schema_id": "odd-prime-local-image-zero-double-root-tangent-1",
            "standard_model": "Y^2 = X^2*(1 - X)",
            "tracked_coordinate": "1 - X",
            "reduction_pieces": [
                "non-node branch",
                "punctured node neighborhood",
                "node center",
            ],
            "candidate_squareclass_set": ["trivial"],
            "reduction_partition_exhausted": True,
            "formal_lift_compatibility_proved": False,
            "local_image_schema_proved": False,
            "remaining_gap": "promote reduction-level partition through formal lifts",
        },
    ]
    assert audit["reduction_partition_not_local_image"] is True
    assert audit["search_count_used_as_progress"] is False


def test_tangent_one_reduction_partition_rejects_unready_inputs() -> None:
    punctured = _punctured_nodes()
    punctured["ready"] = False
    punctured["status"] = "issues"

    audit = audit_rank_zero_selmer_tangent_one_reduction_partition(
        nonnode_branches=_nonnode_branches(),
        node_values=_node_values(),
        punctured_nodes=punctured,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["punctured_nodes_not_ready"]


def test_tangent_one_reduction_partition_cli_writes_audit(tmp_path: Path) -> None:
    nonnode = tmp_path / "nonnode.json"
    nodes = tmp_path / "node_values.json"
    punctured = tmp_path / "punctured_nodes.json"
    out = tmp_path / "reduction_partition.json"
    nonnode.write_text(json.dumps(_nonnode_branches()), encoding="utf-8")
    nodes.write_text(json.dumps(_node_values()), encoding="utf-8")
    punctured.write_text(json.dumps(_punctured_nodes()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_one_reduction_partition.py",
            "--nonnode-branches",
            str(nonnode),
            "--node-values",
            str(nodes),
            "--punctured-nodes",
            str(punctured),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "reduction_partition_exhausted_count=2" in result.stdout
    assert "formal_lift_compatibility_proved_count=0" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["reduction_partition_not_local_image"] is True


def test_write_json_writes_sorted_tangent_one_reduction_partition(tmp_path: Path) -> None:
    out = tmp_path / "reduction_partition.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
