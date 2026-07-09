from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_isogeny_source_shifts import (
    BOUNDARY,
    audit_rank_zero_isogeny_source_shifts,
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


def test_rank_zero_isogeny_source_shifts_verify_shifted_kernel_models() -> None:
    audit = audit_rank_zero_isogeny_source_shifts(_symbolic_inputs())

    assert audit["status"] == "ok"
    assert audit["primitive_model_count"] == 2
    assert audit["kernel_count"] == 3
    assert audit["source_shift_check_count"] == 6
    assert audit["source_shift_verified_count"] == 6
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["symbolic_inputs_ready"] is True
    assert audit["global_relation_search_layer"] == (
        "source differences X-(-p), X-(2*sqrt_q), X-(-2*sqrt_q)"
    )
    assert audit["verified_by_kernel"] == {
        "kernel_minus_p": 2,
        "kernel_neg_2sqrt_q": 2,
        "kernel_pos_2sqrt_q": 2,
    }
    assert audit["templates"]["kernel_minus_p"] == {
        "kernel_root": "-p",
        "shifted_source_model": "y^2 = x*(x - 16*L^2)*(x + 4*T^2)",
        "relative_roots": ["16*L^2", "-4*T^2"],
        "source_a2": "4*T^2 - 16*L^2",
        "source_a4": "-64*L^2*T^2",
        "target_a2_relation": "-2*source_a2",
        "target_a4_relation": (
            "source_a2^2 - 4*source_a4 = 16*(T^2 + 4*L^2)^2"
        ),
    }
    assert audit["templates"]["kernel_pos_2sqrt_q"]["source_a2"] == "4*T^2 + 32*L^2"
    assert audit["boundary"] == BOUNDARY


def test_rank_zero_isogeny_source_shifts_report_unready_symbolic_inputs() -> None:
    symbolic_inputs = _symbolic_inputs()
    symbolic_inputs["status"] = "issues"
    symbolic_inputs["ready"] = False
    symbolic_inputs["symbolic_formula_violation_count"] = 1

    audit = audit_rank_zero_isogeny_source_shifts(symbolic_inputs)

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


def test_rank_zero_isogeny_source_shifts_cli_writes_audit(tmp_path: Path) -> None:
    symbolic_inputs = tmp_path / "symbolic_inputs.json"
    out = tmp_path / "source_shifts.json"
    symbolic_inputs.write_text(json.dumps(_symbolic_inputs()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_isogeny_source_shifts.py",
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

    assert "source_shift_verified_count=6" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "selmer_rank_upper_bound_proved_count"
    ] == 0


def test_write_json_writes_sorted_rank_zero_isogeny_source_shifts(
    tmp_path: Path,
) -> None:
    out = tmp_path / "source_shifts.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
