from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_seed_identities import (
    BOUNDARY,
    audit_rank_zero_seed_identities,
    write_json,
)


def _primitive_models() -> dict[str, object]:
    return {
        "primitive_model_rows": [
            {
                "class": "3:5",
                "unordered_primitive_ray": [3, 5],
                "certifying_curve_patterns": ["AA", "BB"],
                "models": [
                    {
                        "curve": "AA",
                        "primitive_A": 3,
                        "primitive_B": 5,
                        "leg": 3,
                        "total": 8,
                        "p": -56,
                        "q": 10000,
                        "sqrt_q": 100,
                        "weierstrass_model": [0, -56, 0, -40000, 2240000],
                    },
                    {
                        "curve": "BB",
                        "primitive_A": 3,
                        "primitive_B": 5,
                        "leg": 5,
                        "total": 8,
                        "p": 72,
                        "q": 26896,
                        "sqrt_q": 164,
                        "weierstrass_model": [0, 72, 0, -107584, -7746048],
                    },
                ],
            }
        ]
    }


def test_rank_zero_seed_identities_verify_coefficients_and_forced_signs() -> None:
    audit = audit_rank_zero_seed_identities(_primitive_models())

    assert audit == {
        "status": "ok",
        "ready": True,
        "row_count": 1,
        "model_count": 2,
        "coefficient_identity_verified_count": 2,
        "coefficient_identity_violation_count": 0,
        "forced_p_sign_counts_by_curve": {
            "AA": {"negative": 1},
            "BB": {"positive": 1},
        },
        "p_sign_novel_signal_count": 0,
        "violations": [],
        "boundary": BOUNDARY,
    }


def test_rank_zero_seed_identities_report_violations() -> None:
    payload = _primitive_models()
    row = payload["primitive_model_rows"][0]  # type: ignore[index]
    row["models"][0]["p"] = -55  # type: ignore[index]

    audit = audit_rank_zero_seed_identities(payload)

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert audit["coefficient_identity_violation_count"] == 1
    assert audit["violations"] == [
        {
            "class": "3:5",
            "curve": "AA",
            "expected": {
                "leg": 3,
                "p": -56,
                "q": 10000,
                "sqrt_q": 100,
                "total": 8,
                "weierstrass_model": [0, -56, 0, -40000, 2240000],
            },
            "observed": {
                "leg": 3,
                "p": -55,
                "q": 10000,
                "sqrt_q": 100,
                "total": 8,
                "weierstrass_model": [0, -56, 0, -40000, 2240000],
            },
        }
    ]


def test_rank_zero_seed_identities_cli_writes_audit(tmp_path: Path) -> None:
    primitive_models = tmp_path / "primitive_models.json"
    out = tmp_path / "identities.json"
    primitive_models.write_text(json.dumps(_primitive_models()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_seed_identities.py",
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

    assert "coefficient_identity_verified_count=2" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "p_sign_novel_signal_count"
    ] == 0


def test_write_json_writes_sorted_rank_zero_seed_identity_audit(tmp_path: Path) -> None:
    out = tmp_path / "identities.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
