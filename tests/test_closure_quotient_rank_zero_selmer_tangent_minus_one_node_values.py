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
    "audit_closure_quotient_rank_zero_selmer_tangent_minus_one_node_values"
)


def _node_values_module() -> ModuleType:
    assert importlib.util.find_spec(MODULE_NAME) is not None
    return importlib.import_module(MODULE_NAME)


def _minus_one_normal_forms() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "input_schema_count": 4,
        "tangent_minus_one_schema_count": 2,
        "normal_form_count": 2,
        "normal_form_proved_count": 2,
        "nonsquare_parameter_retained": True,
        "normal_forms_not_local_images": True,
        "local_image_schema_proved_count": 0,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "normal_form_entries": [
            {
                "schema_id": "odd-prime-local-image-nonzero-double-root-tangent--1",
                "standard_model": "Y^2 = nu*X*(X - 1)^2",
                "nonsquare_unit_parameter": "nu",
                "normal_form_proved": True,
                "local_image_schema_proved": False,
            },
            {
                "schema_id": "odd-prime-local-image-zero-double-root-tangent--1",
                "standard_model": "Y^2 = nu*X^2*(1 - X)",
                "nonsquare_unit_parameter": "nu",
                "normal_form_proved": True,
                "local_image_schema_proved": False,
            },
        ],
        "violations": [],
    }


def test_tangent_minus_one_node_values_record_reduction_values_only() -> None:
    node_values = _node_values_module()

    audit = node_values.audit_rank_zero_selmer_tangent_minus_one_node_values(
        tangent_minus_one_normal_forms=_minus_one_normal_forms(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["input_normal_form_count"] == 2
    assert audit["node_value_count"] == 2
    assert audit["node_reduction_value_proved_count"] == 2
    assert audit["node_local_lift_analysis_proved_count"] == 0
    assert audit["local_image_schema_proved_count"] == 0
    assert audit["local_condition_proved_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["node_value_entries"] == [
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
    ]
    assert audit["node_values_not_local_images"] is True
    assert audit["search_count_used_as_progress"] is False


def test_tangent_minus_one_node_values_reject_unready_normal_forms() -> None:
    node_values = _node_values_module()
    normal_forms = _minus_one_normal_forms()
    normal_forms["ready"] = False
    normal_forms["status"] = "issues"

    audit = node_values.audit_rank_zero_selmer_tangent_minus_one_node_values(
        tangent_minus_one_normal_forms=normal_forms,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["tangent_minus_one_normal_forms_not_ready"]


def test_tangent_minus_one_node_values_cli_writes_audit(tmp_path: Path) -> None:
    normal_forms = tmp_path / "minus_one_normal_forms.json"
    out = tmp_path / "minus_one_node_values.json"
    normal_forms.write_text(json.dumps(_minus_one_normal_forms()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_minus_one_node_values.py",
            "--tangent-minus-one-normal-forms",
            str(normal_forms),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "node_reduction_value_proved_count=2" in result.stdout
    assert "node_local_lift_analysis_proved_count=0" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["node_values_not_local_images"] is True


def test_write_json_writes_sorted_tangent_minus_one_node_values(tmp_path: Path) -> None:
    node_values = _node_values_module()
    out = tmp_path / "minus_one_node_values.json"

    node_values.write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
