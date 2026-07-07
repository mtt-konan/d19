from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_symbolic_descent_inputs import (
    BOUNDARY,
    audit_rank_zero_symbolic_descent_inputs,
    write_json,
)


def _model(*, primitive_a: int, primitive_b: int, curve: str) -> dict[str, object]:
    total = primitive_a + primitive_b
    leg = primitive_a if curve == "AA" else primitive_b
    sqrt_q = total * total + 4 * leg * leg
    p = 8 * leg * leg - 2 * total * total
    return {
        "curve": curve,
        "primitive_A": primitive_a,
        "primitive_B": primitive_b,
        "leg": leg,
        "total": total,
        "p": p,
        "q": sqrt_q * sqrt_q,
        "sqrt_q": sqrt_q,
        "weierstrass_model": [0, p, 0, -4 * sqrt_q * sqrt_q, -4 * p * sqrt_q * sqrt_q],
    }


def _primitive_models() -> dict[str, object]:
    return {
        "primitive_model_rows": [
            {
                "class": "3:5",
                "unordered_primitive_ray": [3, 5],
                "models": [_model(primitive_a=3, primitive_b=5, curve="AA")],
            },
            {
                "class": "7:11",
                "unordered_primitive_ray": [7, 11],
                "models": [_model(primitive_a=7, primitive_b=11, curve="BB")],
            },
        ]
    }


def test_rank_zero_symbolic_descent_inputs_verify_uniform_root_differences() -> None:
    audit = audit_rank_zero_symbolic_descent_inputs(_primitive_models())

    assert audit["status"] == "ok"
    assert audit["primitive_model_count"] == 2
    assert audit["symbolic_formula_verified_count"] == 2
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["models"][0] == {
        "class": "3:5",
        "curve": "AA",
        "leg": 3,
        "total": 8,
        "root_differences": {
            "minus_p_minus_pos_2sqrt_q": -144,
            "minus_p_minus_neg_2sqrt_q": 256,
            "pos_2sqrt_q_minus_neg_2sqrt_q": 400,
        },
        "squareclass_inputs": {
            "minus_p_minus_pos_2sqrt_q": "-1 times a square",
            "minus_p_minus_neg_2sqrt_q": "square",
            "pos_2sqrt_q_minus_neg_2sqrt_q": "4*(T^2 + 4*L^2)",
        },
        "selmer_rank_upper_bound_proved": False,
        "family_exclusion_proved": False,
    }
    assert audit["boundary"] == BOUNDARY


def test_rank_zero_symbolic_descent_inputs_reports_formula_mismatch() -> None:
    primitive_models = _primitive_models()
    primitive_models["primitive_model_rows"][0]["models"][0]["p"] = 123

    audit = audit_rank_zero_symbolic_descent_inputs(primitive_models)

    assert audit["status"] == "issues"
    assert audit["symbolic_formula_violation_count"] == 1
    assert audit["violations"][0]["class"] == "3:5"


def test_rank_zero_symbolic_descent_inputs_cli_writes_audit(tmp_path: Path) -> None:
    primitive_models = tmp_path / "primitive_models.json"
    out = tmp_path / "symbolic_inputs.json"
    primitive_models.write_text(json.dumps(_primitive_models()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_symbolic_descent_inputs.py",
            "--primitive-models",
            str(primitive_models),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "symbolic_formula_verified_count=2" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "selmer_rank_upper_bound_proved_count"
    ] == 0


def test_write_json_writes_sorted_rank_zero_symbolic_inputs(tmp_path: Path) -> None:
    out = tmp_path / "symbolic_inputs.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
