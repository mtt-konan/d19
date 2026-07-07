from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.export_closure_quotient_rank_zero_selmer_package_index import (
    BOUNDARY,
    export_rank_zero_selmer_package_index,
    write_json,
)


def _selmer_obligations() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "family_obligation_count": 2,
        "kernel_count": 3,
        "selmer_obligation_count": 6,
        "open_selmer_obligation_count": 6,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "families": [
            {
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
            },
            {
                "pattern": "BB",
                "candidate_class_count": 1,
                "model_count": 1,
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
            },
        ],
    }


def _isogeny_templates() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "templates": {
            "kernel_minus_p": {
                "kernel_root": "-p",
                "symbolic_a2": "32*L^2 - 8*T^2",
                "symbolic_a4": "16*(T^2 + 4*L^2)^2",
            },
            "kernel_neg_2sqrt_q": {
                "kernel_root": "-2*sqrt_q",
                "symbolic_a2": "16*(T^2 + 2*L^2)",
                "symbolic_a4": "256*L^4",
            },
            "kernel_pos_2sqrt_q": {
                "kernel_root": "2*sqrt_q",
                "symbolic_a2": "-8*(T^2 + 8*L^2)",
                "symbolic_a4": "16*T^4",
            },
        },
    }


def test_rank_zero_selmer_package_index_exports_open_tasks() -> None:
    index = export_rank_zero_selmer_package_index(
        selmer_obligations=_selmer_obligations(),
        isogeny_templates=_isogeny_templates(),
    )

    assert index["status"] == "ok"
    assert index["package_count"] == 6
    assert index["open_package_count"] == 6
    assert index["selmer_rank_upper_bound_proved_count"] == 0
    assert index["family_exclusion_proved_count"] == 0
    assert index["search_count_used_as_progress"] is False
    assert index["packages"][0] == {
        "package_id": "rank-zero-selmer-AA-kernel-minus-p",
        "family_pattern": "AA",
        "kernel": "kernel_minus_p",
        "candidate_class_count": 2,
        "model_count": 2,
        "kernel_root": "-p",
        "target_a2": "32*L^2 - 8*T^2",
        "target_a4": "16*(T^2 + 4*L^2)^2",
        "required_output": (
            "reviewable transcript proving the uniform isogeny-Selmer rank "
            "upper bound for this family/kernel"
        ),
        "status": "open",
        "selmer_rank_upper_bound_proved": False,
        "family_exclusion_proved": False,
    }
    assert index["boundary"] == BOUNDARY


def test_rank_zero_selmer_package_index_reports_unready_inputs() -> None:
    selmer_obligations = _selmer_obligations()
    selmer_obligations["ready"] = False
    selmer_obligations["status"] = "issues"

    index = export_rank_zero_selmer_package_index(
        selmer_obligations=selmer_obligations,
        isogeny_templates=_isogeny_templates(),
    )

    assert index["status"] == "issues"
    assert index["violations"] == ["selmer_obligations_ready"]


def test_rank_zero_selmer_package_index_cli_writes_index(tmp_path: Path) -> None:
    selmer_obligations = tmp_path / "selmer_obligations.json"
    isogeny_templates = tmp_path / "isogeny_templates.json"
    out = tmp_path / "package_index.json"
    selmer_obligations.write_text(json.dumps(_selmer_obligations()), encoding="utf-8")
    isogeny_templates.write_text(json.dumps(_isogeny_templates()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/export_closure_quotient_rank_zero_selmer_package_index.py",
            "--selmer-obligations",
            str(selmer_obligations),
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

    assert "package_count=6" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["open_package_count"] == 6


def test_write_json_writes_sorted_rank_zero_selmer_package_index(tmp_path: Path) -> None:
    out = tmp_path / "package_index.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
