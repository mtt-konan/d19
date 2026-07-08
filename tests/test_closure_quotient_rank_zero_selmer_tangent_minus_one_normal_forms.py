from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory import (
    audit_closure_quotient_rank_zero_selmer_tangent_minus_one_normal_forms as minus_one,
)

audit_rank_zero_selmer_tangent_minus_one_normal_forms = (
    minus_one.audit_rank_zero_selmer_tangent_minus_one_normal_forms
)
write_json = minus_one.write_json


def _local_image_schemas() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "local_image_schema_count": 4,
        "local_image_schema_proved_count": 0,
        "local_image_schemas_not_conditions": True,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "schemas": [
            {
                "schema_id": "odd-prime-local-image-nonzero-double-root-tangent-1",
                "tangent_squareclass": "1",
                "model_shape": (
                    "y^2 = x*(x-r)^2 with r a local unit and tangent squareclass 1"
                ),
                "local_image_schema_proved": False,
                "local_condition_proved": False,
            },
            {
                "schema_id": "odd-prime-local-image-nonzero-double-root-tangent--1",
                "nodal_reduction_shape": "nodal-cubic-with-nonzero-double-root",
                "tangent_squareclass": "-1",
                "model_shape": (
                    "y^2 = x*(x-r)^2 with r a local unit and tangent squareclass -1"
                ),
                "local_image_schema_proved": False,
                "local_condition_proved": False,
            },
            {
                "schema_id": "odd-prime-local-image-zero-double-root-tangent--1",
                "nodal_reduction_shape": "nodal-cubic-with-zero-double-root",
                "tangent_squareclass": "-1",
                "model_shape": (
                    "y^2 = x^2*(x-s) with s a local unit and tangent squareclass -1"
                ),
                "local_image_schema_proved": False,
                "local_condition_proved": False,
            },
        ],
    }


def test_tangent_minus_one_normal_forms_keep_nonsquare_parameter() -> None:
    audit = audit_rank_zero_selmer_tangent_minus_one_normal_forms(
        odd_prime_local_image_schemas=_local_image_schemas(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["input_schema_count"] == 4
    assert audit["tangent_minus_one_schema_count"] == 2
    assert audit["normal_form_count"] == 2
    assert audit["normal_form_proved_count"] == 2
    assert audit["nonsquare_parameter_retained"] is True
    assert audit["local_image_schema_proved_count"] == 0
    assert audit["local_condition_proved_count"] == 0
    assert audit["normal_form_entries"] == [
        {
            "schema_id": "odd-prime-local-image-nonzero-double-root-tangent--1",
            "nodal_reduction_shape": "nodal-cubic-with-nonzero-double-root",
            "tangent_squareclass": "-1",
            "source_model_shape": (
                "y^2 = x*(x-r)^2 with r a local unit and tangent squareclass -1"
            ),
            "nonsquare_unit_parameter": "nu",
            "unit_square_root_required": "choose u with u^2 = r/nu",
            "coordinate_change": "x = nu*u^2*X, y = nu*u^3*Y",
            "standard_model": "Y^2 = nu*X*(X - 1)^2",
            "normal_form_proved": True,
            "local_image_schema_proved": False,
            "next_gap": (
                "compute the 2-isogeny local squareclass image with nonsquare "
                "unit parameter nu"
            ),
        },
        {
            "schema_id": "odd-prime-local-image-zero-double-root-tangent--1",
            "nodal_reduction_shape": "nodal-cubic-with-zero-double-root",
            "tangent_squareclass": "-1",
            "source_model_shape": (
                "y^2 = x^2*(x-s) with s a local unit and tangent squareclass -1"
            ),
            "nonsquare_unit_parameter": "nu",
            "unit_square_root_required": "choose u with u^2 = (-s)/nu",
            "coordinate_change": "x = -nu*u^2*X, y = nu*u^3*Y",
            "standard_model": "Y^2 = nu*X^2*(1 - X)",
            "normal_form_proved": True,
            "local_image_schema_proved": False,
            "next_gap": (
                "compute the 2-isogeny local squareclass image with nonsquare "
                "unit parameter nu"
            ),
        },
    ]
    assert audit["search_count_used_as_progress"] is False


def test_tangent_minus_one_normal_forms_reject_unready_inputs() -> None:
    schemas = _local_image_schemas()
    schemas["ready"] = False
    schemas["status"] = "issues"

    audit = audit_rank_zero_selmer_tangent_minus_one_normal_forms(
        odd_prime_local_image_schemas=schemas,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["odd_prime_local_image_schemas_not_ready"]


def test_tangent_minus_one_normal_forms_cli_writes_audit(tmp_path: Path) -> None:
    schemas = tmp_path / "local_image_schemas.json"
    out = tmp_path / "minus_one_normal_forms.json"
    schemas.write_text(json.dumps(_local_image_schemas()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_minus_one_normal_forms.py",
            "--odd-prime-local-image-schemas",
            str(schemas),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "tangent_minus_one_schema_count=2" in result.stdout
    assert "normal_form_proved_count=2" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["nonsquare_parameter_retained"] is True


def test_write_json_writes_sorted_tangent_minus_one_normal_forms(tmp_path: Path) -> None:
    out = tmp_path / "minus_one_normal_forms.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
