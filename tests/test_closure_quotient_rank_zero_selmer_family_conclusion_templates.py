from __future__ import annotations

import importlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

MODULE_NAME = (
    "scripts.theory."
    "audit_closure_quotient_rank_zero_selmer_family_conclusion_templates"
)


def _templates_module() -> ModuleType:
    assert importlib.util.find_spec(MODULE_NAME) is not None
    return importlib.import_module(MODULE_NAME)


def _selmer_obligations() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "family_obligation_count": 2,
        "kernel_count": 2,
        "selmer_obligation_count": 4,
        "open_selmer_obligation_count": 4,
        "rank_zero_selmer_obligations_complete": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "families": [
            {
                "pattern": "AA",
                "candidate_class_count": 2,
                "model_count": 2,
                "required_kernel_obligations": [
                    "kernel_minus_p",
                    "kernel_pos_2sqrt_q",
                ],
                "selmer_rank_upper_bound_proved": False,
                "family_exclusion_proved": False,
            },
            {
                "pattern": "AA+BB",
                "candidate_class_count": 1,
                "model_count": 2,
                "required_kernel_obligations": [
                    "kernel_minus_p",
                    "kernel_pos_2sqrt_q",
                ],
                "selmer_rank_upper_bound_proved": False,
                "family_exclusion_proved": False,
            },
        ],
    }


def _transcript_bridge() -> dict[str, object]:
    rows = []
    for package_id, kernel in [
        ("rank-zero-selmer-AA-kernel-minus-p", "kernel_minus_p"),
        ("rank-zero-selmer-AA-kernel-pos-2sqrt-q", "kernel_pos_2sqrt_q"),
        ("rank-zero-selmer-AA-BB-kernel-minus-p", "kernel_minus_p"),
        ("rank-zero-selmer-AA-BB-kernel-pos-2sqrt-q", "kernel_pos_2sqrt_q"),
    ]:
        rows.append(
            {
                "package_id": package_id,
                "kernel": kernel,
                "kernel_schema_id": f"schema-{kernel}",
                "shared_transcript_fields": ["local_squareclass_conditions"],
                "package_specific_transcript_fields": [
                    "statement",
                    "isogeny_setup",
                    "selmer_bound_argument",
                    "rank_zero_conclusion",
                    "review_notes",
                ],
                "transcript_package_ready": False,
                "strict_promotion_ready": False,
            }
        )
    return {
        "status": "ok",
        "ready": True,
        "package_count": 4,
        "kernel_schema_count": 2,
        "shared_local_squareclass_template_count": 2,
        "package_specific_transcript_count": 4,
        "transcript_package_ready_count": 0,
        "strict_promotion_ready_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "bridge_rows": rows,
    }


def test_family_conclusion_templates_group_kernel_bounds_by_family() -> None:
    templates = _templates_module()

    audit = templates.audit_rank_zero_selmer_family_conclusion_templates(
        selmer_obligations=_selmer_obligations(),
        transcript_bridge=_transcript_bridge(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["family_conclusion_template_count"] == 2
    assert audit["kernel_bound_package_count"] == 4
    assert audit["open_family_conclusion_count"] == 2
    assert audit["rank_zero_conclusion_proved_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["violations"] == []
    assert audit["family_conclusion_templates"][0] == {
        "family_pattern": "AA",
        "candidate_class_count": 2,
        "model_count": 2,
        "required_kernel_count": 2,
        "required_kernel_bound_packages": [
            {
                "kernel": "kernel_minus_p",
                "package_id": "rank-zero-selmer-AA-kernel-minus-p",
                "transcript_package_ready": False,
            },
            {
                "kernel": "kernel_pos_2sqrt_q",
                "package_id": "rank-zero-selmer-AA-kernel-pos-2sqrt-q",
                "transcript_package_ready": False,
            },
        ],
        "rank_zero_conclusion_ready": False,
        "rank_zero_conclusion_proved": False,
        "remaining_transcript_field": "rank_zero_conclusion",
    }


def test_family_conclusion_templates_report_missing_kernel_package() -> None:
    templates = _templates_module()
    bridge = _transcript_bridge()
    bridge["bridge_rows"] = bridge["bridge_rows"][:-1]

    audit = templates.audit_rank_zero_selmer_family_conclusion_templates(
        selmer_obligations=_selmer_obligations(),
        transcript_bridge=bridge,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "missing_family_kernel_package=AA+BB:kernel_pos_2sqrt_q"
    ]


def test_family_conclusion_templates_cli_writes_audit(tmp_path: Path) -> None:
    selmer_obligations = tmp_path / "selmer_obligations.json"
    transcript_bridge = tmp_path / "transcript_bridge.json"
    out = tmp_path / "family_conclusions.json"
    selmer_obligations.write_text(
        json.dumps(_selmer_obligations()), encoding="utf-8"
    )
    transcript_bridge.write_text(json.dumps(_transcript_bridge()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            (
                "scripts/theory/"
                "audit_closure_quotient_rank_zero_selmer_family_conclusion_templates.py"
            ),
            "--selmer-obligations",
            str(selmer_obligations),
            "--transcript-bridge",
            str(transcript_bridge),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "family_conclusion_template_count=2" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["open_family_conclusion_count"] == 2


def test_write_json_writes_sorted_family_conclusion_templates(tmp_path: Path) -> None:
    templates = _templates_module()
    out = tmp_path / "family_conclusions.json"

    templates.write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
