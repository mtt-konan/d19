from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_isogeny_product_relation import (
    BOUNDARY,
    audit_rank_zero_isogeny_product_relation,
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


def _source_shifts() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "source_shift_violation_count": 0,
    }


def test_rank_zero_isogeny_product_relation_records_common_source_square() -> None:
    audit = audit_rank_zero_isogeny_product_relation(
        symbolic_inputs=_symbolic_inputs(),
        source_shifts=_source_shifts(),
    )

    assert audit["status"] == "ok"
    assert audit["primitive_model_count"] == 2
    assert audit["kernel_count"] == 3
    assert audit["product_relation_verified_count"] == 2
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["common_source_relation"] == (
        "x_minus_p * x_pos_2sqrt_q * x_neg_2sqrt_q = "
        "(X-(-p))*(X-(2*sqrt_q))*(X-(-2*sqrt_q)) = Y^2"
    )
    assert audit["product_exponents_total"] == {"-p": 1, "2*sqrt_q": 1, "-2*sqrt_q": 1}
    assert audit["target_coordinate_formulas"]["kernel_neg_2sqrt_q"] == {
        "denominator": "X-(-2*sqrt_q)",
        "numerator": ["X-(-p)", "X-(2*sqrt_q)"],
        "target_x_formula": "((X-(-p))*(X-(2*sqrt_q)))/(X-(-2*sqrt_q))",
        "exponents": {"-p": 1, "2*sqrt_q": 1, "-2*sqrt_q": -1},
    }
    assert audit["boundary"] == BOUNDARY


def test_rank_zero_isogeny_product_relation_requires_ready_inputs() -> None:
    symbolic_inputs = _symbolic_inputs()
    symbolic_inputs["status"] = "issues"
    source_shifts = _source_shifts()
    source_shifts["ready"] = False

    audit = audit_rank_zero_isogeny_product_relation(
        symbolic_inputs=symbolic_inputs,
        source_shifts=source_shifts,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "symbolic_inputs_not_ready",
        "source_shifts_not_ready",
    ]


def test_rank_zero_isogeny_product_relation_cli_writes_audit(tmp_path: Path) -> None:
    symbolic_inputs = tmp_path / "symbolic_inputs.json"
    source_shifts = tmp_path / "source_shifts.json"
    out = tmp_path / "product_relation.json"
    symbolic_inputs.write_text(json.dumps(_symbolic_inputs()), encoding="utf-8")
    source_shifts.write_text(json.dumps(_source_shifts()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_isogeny_product_relation.py",
            "--symbolic-inputs",
            str(symbolic_inputs),
            "--source-shifts",
            str(source_shifts),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "product_relation_verified_count=2" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "family_exclusion_proved_count"
    ] == 0


def test_write_json_writes_sorted_rank_zero_isogeny_product_relation(
    tmp_path: Path,
) -> None:
    out = tmp_path / "product_relation.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
