from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory import (
    audit_closure_quotient_rank_zero_selmer_tangent_one_unit_branch as unit_branch,
)

audit_rank_zero_selmer_tangent_one_unit_branch = (
    unit_branch.audit_rank_zero_selmer_tangent_one_unit_branch
)
write_json = unit_branch.write_json


def _normal_forms() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "input_schema_count": 4,
        "tangent_one_schema_count": 2,
        "normal_form_count": 2,
        "normal_form_proved_count": 2,
        "normal_forms_not_local_images": True,
        "local_image_schema_proved_count": 0,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "normal_form_entries": [
            {
                "schema_id": "odd-prime-local-image-nonzero-double-root-tangent-1",
                "nodal_reduction_shape": "nodal-cubic-with-nonzero-double-root",
                "tangent_squareclass": "1",
                "source_model_shape": (
                    "y^2 = x*(x-r)^2 with r a local unit and tangent squareclass 1"
                ),
                "unit_square_root_required": "choose u with u^2 = r",
                "coordinate_change": "x = u^2*X, y = u^3*Y",
                "standard_model": "Y^2 = X*(X - 1)^2",
                "normal_form_proved": True,
                "local_image_schema_proved": False,
                "next_gap": (
                    "compute the 2-isogeny local squareclass image on the standard "
                    "tangent-one nodal model"
                ),
            },
            {
                "schema_id": "odd-prime-local-image-zero-double-root-tangent-1",
                "nodal_reduction_shape": "nodal-cubic-with-zero-double-root",
                "tangent_squareclass": "1",
                "source_model_shape": (
                    "y^2 = x^2*(x-s) with s a local unit and tangent squareclass 1"
                ),
                "unit_square_root_required": "choose u with u^2 = -s",
                "coordinate_change": "x = -u^2*X, y = u^3*Y",
                "standard_model": "Y^2 = X^2*(X - 1)",
                "normal_form_proved": True,
                "local_image_schema_proved": False,
                "next_gap": (
                    "compute the 2-isogeny local squareclass image on the standard "
                    "tangent-one nodal model"
                ),
            },
        ],
        "violations": [],
    }


def test_tangent_one_unit_branch_records_only_unit_squareclass_consequence() -> None:
    audit = audit_rank_zero_selmer_tangent_one_unit_branch(
        tangent_one_normal_forms=_normal_forms(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["input_normal_form_count"] == 2
    assert audit["unit_branch_count"] == 1
    assert audit["unit_branch_squareclass_consequence_proved_count"] == 1
    assert audit["local_image_schema_proved_count"] == 0
    assert audit["local_condition_proved_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["unit_branch_entries"] == [
        {
            "schema_id": "odd-prime-local-image-nonzero-double-root-tangent-1",
            "standard_model": "Y^2 = X*(X - 1)^2",
            "branch_id": "tangent-one-nonzero-double-root-unit-branch",
            "branch_hypothesis": "X and X - 1 are local units",
            "identity": "X = (Y/(X - 1))^2",
            "squareclass_consequence": "X has trivial local squareclass on this branch",
            "branch_squareclass_consequence_proved": True,
            "local_image_schema_proved": False,
            "uncovered_branches": [
                "X nonunit branch",
                "X - 1 nonunit branch",
                "zero-double-root tangent-one standard model",
                "tangent-squareclass -1 schemas",
            ],
        }
    ]
    assert audit["branch_results_not_local_images"] is True
    assert audit["search_count_used_as_progress"] is False


def test_tangent_one_unit_branch_rejects_unready_normal_forms() -> None:
    normal_forms = _normal_forms()
    normal_forms["ready"] = False
    normal_forms["status"] = "issues"

    audit = audit_rank_zero_selmer_tangent_one_unit_branch(
        tangent_one_normal_forms=normal_forms,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["tangent_one_normal_forms_not_ready"]


def test_tangent_one_unit_branch_cli_writes_audit(tmp_path: Path) -> None:
    normal_forms = tmp_path / "normal_forms.json"
    out = tmp_path / "unit_branch.json"
    normal_forms.write_text(json.dumps(_normal_forms()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_one_unit_branch.py",
            "--tangent-one-normal-forms",
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

    assert "unit_branch_squareclass_consequence_proved_count=1" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["branch_results_not_local_images"] is True


def test_write_json_writes_sorted_tangent_one_unit_branch(tmp_path: Path) -> None:
    out = tmp_path / "unit_branch.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
