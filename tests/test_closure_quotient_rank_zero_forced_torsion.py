from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_forced_torsion import (
    BOUNDARY,
    audit_forced_torsion,
    write_json,
)


def _primitive_models() -> dict[str, object]:
    return {
        "primitive_model_rows": [
            {
                "class": "3:5",
                "unordered_primitive_ray": [3, 5],
                "models": [
                    {
                        "curve": "AA",
                        "p": -56,
                        "q": 10000,
                        "sqrt_q": 100,
                        "weierstrass_model": [0, -56, 0, -40000, 2240000],
                    }
                ],
            }
        ]
    }


def _invariants() -> dict[str, object]:
    return {
        "models": [
            {
                "class": "3:5",
                "curve": "AA",
                "torsion_orders": [4],
                "family_exclusion_proved": False,
            }
        ]
    }


def test_forced_torsion_audit_splits_formula_torsion_from_observed_exact_order() -> None:
    audit = audit_forced_torsion(
        primitive_models=_primitive_models(),
        certifying_invariants=_invariants(),
    )

    assert audit == {
        "status": "ok",
        "ready": True,
        "primitive_model_count": 1,
        "forced_full_two_torsion_count": 1,
        "forced_two_torsion_violation_count": 0,
        "observed_exact_torsion_order_four_count": 1,
        "observed_extra_torsion_model_count": 0,
        "family_exclusion_proved_count": 0,
        "models": [
            {
                "class": "3:5",
                "curve": "AA",
                "p": -56,
                "sqrt_q": 100,
                "two_torsion_x_roots": [-200, 56, 200],
                "forced_two_torsion_status": "full-rational-2-torsion-forced",
                "observed_torsion_orders": [4],
                "observed_extra_torsion": False,
                "family_exclusion_proved": False,
            }
        ],
        "violations": [],
        "boundary": BOUNDARY,
    }


def test_forced_torsion_audit_reports_bad_model_identity() -> None:
    primitive_models = _primitive_models()
    row = primitive_models["primitive_model_rows"][0]  # type: ignore[index]
    row["models"][0]["weierstrass_model"] = [0, -56, 0, -40000, 1]  # type: ignore[index]

    audit = audit_forced_torsion(
        primitive_models=primitive_models,
        certifying_invariants=_invariants(),
    )

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert audit["forced_two_torsion_violation_count"] == 1
    assert audit["violations"] == [
        {
            "class": "3:5",
            "curve": "AA",
            "expected_model": [0, -56, 0, -40000, 2240000],
            "observed_model": [0, -56, 0, -40000, 1],
        }
    ]


def test_forced_torsion_cli_writes_audit(tmp_path: Path) -> None:
    primitive_models = tmp_path / "primitive_models.json"
    invariants = tmp_path / "invariants.json"
    out = tmp_path / "forced_torsion.json"
    primitive_models.write_text(json.dumps(_primitive_models()), encoding="utf-8")
    invariants.write_text(json.dumps(_invariants()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_forced_torsion.py",
            "--primitive-models",
            str(primitive_models),
            "--certifying-invariants",
            str(invariants),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "forced_full_two_torsion_count=1" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "observed_extra_torsion_model_count"
    ] == 0


def test_write_json_writes_sorted_forced_torsion_audit(tmp_path: Path) -> None:
    out = tmp_path / "forced_torsion.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
