from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_selmer_obligations import (
    BOUNDARY,
    audit_rank_zero_selmer_obligations,
    write_json,
)


def _family_obligations() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "rank_zero_family_obligation_count": 2,
        "open_obligation_count": 2,
        "family_exclusion_proved_count": 0,
        "groups": [
            {
                "pattern": "AA",
                "candidate_class_count": 2,
                "model_count": 2,
                "family_exclusion_proved": False,
            },
            {
                "pattern": "BB",
                "candidate_class_count": 1,
                "model_count": 1,
                "family_exclusion_proved": False,
            },
        ],
    }


def _isogeny_templates() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "primitive_model_count": 3,
        "kernel_count": 3,
        "isogeny_template_verified_count": 9,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "verified_by_kernel": {
            "kernel_minus_p": 3,
            "kernel_neg_2sqrt_q": 3,
            "kernel_pos_2sqrt_q": 3,
        },
    }


def test_rank_zero_selmer_obligations_keep_selmer_bound_open() -> None:
    audit = audit_rank_zero_selmer_obligations(
        family_obligations=_family_obligations(),
        isogeny_templates=_isogeny_templates(),
    )

    assert audit["status"] == "ok"
    assert audit["rank_zero_selmer_obligations_complete"] is False
    assert audit["family_obligation_count"] == 2
    assert audit["kernel_count"] == 3
    assert audit["selmer_obligation_count"] == 6
    assert audit["open_selmer_obligation_count"] == 6
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["families"][0] == {
        "pattern": "AA",
        "candidate_class_count": 2,
        "model_count": 2,
        "required_kernel_obligations": [
            "kernel_minus_p",
            "kernel_neg_2sqrt_q",
            "kernel_pos_2sqrt_q",
        ],
        "missing_theorem": (
            "uniform isogeny-Selmer rank upper bound for every listed kernel"
        ),
        "selmer_rank_upper_bound_proved": False,
        "family_exclusion_proved": False,
    }
    assert audit["boundary"] == BOUNDARY


def test_rank_zero_selmer_obligations_report_unready_isogeny_templates() -> None:
    isogeny_templates = _isogeny_templates()
    isogeny_templates["ready"] = False
    isogeny_templates["status"] = "issues"

    audit = audit_rank_zero_selmer_obligations(
        family_obligations=_family_obligations(),
        isogeny_templates=isogeny_templates,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["isogeny_templates_ready"]


def test_rank_zero_selmer_obligations_cli_writes_audit(tmp_path: Path) -> None:
    family_obligations = tmp_path / "family_obligations.json"
    isogeny_templates = tmp_path / "isogeny_templates.json"
    out = tmp_path / "selmer_obligations.json"
    family_obligations.write_text(json.dumps(_family_obligations()), encoding="utf-8")
    isogeny_templates.write_text(json.dumps(_isogeny_templates()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_obligations.py",
            "--family-obligations",
            str(family_obligations),
            "--isogeny-templates",
            str(isogeny_templates),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "selmer_obligation_count=6" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "rank_zero_selmer_obligations_complete"
    ] is False


def test_write_json_writes_sorted_rank_zero_selmer_obligations(tmp_path: Path) -> None:
    out = tmp_path / "selmer_obligations.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
