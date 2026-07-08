from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory import (
    audit_closure_quotient_rank_zero_selmer_tangent_minus_one_nonnode_branches as nonnode,
)

audit_rank_zero_selmer_tangent_minus_one_nonnode_branches = (
    nonnode.audit_rank_zero_selmer_tangent_minus_one_nonnode_branches
)
write_json = nonnode.write_json


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


def test_tangent_minus_one_nonnode_branches_record_nonsquare_consequences() -> None:
    audit = audit_rank_zero_selmer_tangent_minus_one_nonnode_branches(
        tangent_minus_one_normal_forms=_minus_one_normal_forms(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["input_normal_form_count"] == 2
    assert audit["nonnode_branch_count"] == 2
    assert audit["nonnode_squareclass_consequence_proved_count"] == 2
    assert audit["nonsquare_parameter_retained"] is True
    assert audit["local_image_schema_proved_count"] == 0
    assert audit["local_condition_proved_count"] == 0
    assert audit["nonnode_branch_entries"] == [
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
            "remaining_gap": "node center and formal lift compatibility",
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
            "remaining_gap": "node center and formal lift compatibility",
        },
    ]
    assert audit["nonnode_results_not_local_images"] is True
    assert audit["search_count_used_as_progress"] is False


def test_tangent_minus_one_nonnode_branches_reject_unready_inputs() -> None:
    normal_forms = _minus_one_normal_forms()
    normal_forms["ready"] = False
    normal_forms["status"] = "issues"

    audit = audit_rank_zero_selmer_tangent_minus_one_nonnode_branches(
        tangent_minus_one_normal_forms=normal_forms,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["tangent_minus_one_normal_forms_not_ready"]


def test_tangent_minus_one_nonnode_branches_cli_writes_audit(tmp_path: Path) -> None:
    normal_forms = tmp_path / "minus_one_normal_forms.json"
    out = tmp_path / "minus_one_nonnode.json"
    normal_forms.write_text(json.dumps(_minus_one_normal_forms()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_minus_one_nonnode_branches.py",
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

    assert "nonnode_squareclass_consequence_proved_count=2" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["nonnode_results_not_local_images"] is True


def test_write_json_writes_sorted_tangent_minus_one_nonnode(tmp_path: Path) -> None:
    out = tmp_path / "minus_one_nonnode.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
