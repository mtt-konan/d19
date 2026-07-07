from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_isogeny_templates import (
    BOUNDARY,
    audit_rank_zero_isogeny_templates,
    write_json,
)


def _symbolic_inputs() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "symbolic_formula_violation_count": 0,
        "models": [
            {"class": "3:5", "curve": "AA", "leg": 3, "total": 8},
            {"class": "7:11", "curve": "BB", "leg": 11, "total": 18},
        ],
    }


def test_rank_zero_isogeny_templates_verify_three_kernel_targets() -> None:
    audit = audit_rank_zero_isogeny_templates(_symbolic_inputs())

    assert audit["status"] == "ok"
    assert audit["primitive_model_count"] == 2
    assert audit["kernel_count"] == 3
    assert audit["isogeny_template_check_count"] == 6
    assert audit["isogeny_template_verified_count"] == 6
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["symbolic_inputs_ready"] is True
    assert audit["verified_by_kernel"] == {
        "kernel_minus_p": 2,
        "kernel_neg_2sqrt_q": 2,
        "kernel_pos_2sqrt_q": 2,
    }
    assert audit["templates"]["kernel_pos_2sqrt_q"] == {
        "kernel_root": "2*sqrt_q",
        "target_model": (
            "y^2 = x^3 + (-2p - 12*sqrt_q)*x^2 + "
            "(p - 2*sqrt_q)^2*x"
        ),
        "symbolic_a2": "-8*(T^2 + 8*L^2)",
        "symbolic_a4": "16*T^4",
        "a4_square": "(4*T^2)^2",
    }
    assert audit["boundary"] == BOUNDARY


def test_rank_zero_isogeny_templates_report_unready_symbolic_inputs() -> None:
    symbolic_inputs = _symbolic_inputs()
    symbolic_inputs["status"] = "issues"
    symbolic_inputs["ready"] = False
    symbolic_inputs["symbolic_formula_violation_count"] = 1

    audit = audit_rank_zero_isogeny_templates(symbolic_inputs)

    assert audit["status"] == "issues"
    assert audit["symbolic_inputs_ready"] is False
    assert audit["violations"] == [
        {
            "field": "symbolic_inputs",
            "status": "issues",
            "ready": False,
            "symbolic_formula_violation_count": 1,
        }
    ]


def test_rank_zero_isogeny_templates_cli_writes_audit(tmp_path: Path) -> None:
    symbolic_inputs = tmp_path / "symbolic_inputs.json"
    out = tmp_path / "isogeny_templates.json"
    symbolic_inputs.write_text(json.dumps(_symbolic_inputs()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_isogeny_templates.py",
            "--symbolic-inputs",
            str(symbolic_inputs),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "isogeny_template_verified_count=6" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "selmer_rank_upper_bound_proved_count"
    ] == 0


def test_write_json_writes_sorted_rank_zero_isogeny_templates(tmp_path: Path) -> None:
    out = tmp_path / "isogeny_templates.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
