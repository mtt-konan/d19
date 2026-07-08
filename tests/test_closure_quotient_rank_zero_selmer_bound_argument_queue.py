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

MODULE_NAME = "scripts.theory.audit_closure_quotient_rank_zero_selmer_bound_argument_queue"


def _queue_module() -> ModuleType:
    assert importlib.util.find_spec(MODULE_NAME) is not None
    return importlib.import_module(MODULE_NAME)


def _field_decomposition() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "required_transcript_field_count": 6,
        "kernel_shared_field_count": 2,
        "kernel_shared_template_count": 2,
        "family_aggregated_field_count": 1,
        "family_conclusion_template_count": 2,
        "package_specific_field_count": 3,
        "package_specific_open_field_obligation_count": 12,
        "primary_remaining_proof_field": "selmer_bound_argument",
        "transcript_package_ready_count": 0,
        "strict_promotion_ready_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "field_decomposition": {
            "kernel_shared_fields": [
                "local_squareclass_conditions",
                "isogeny_setup",
            ],
            "family_aggregated_fields": ["rank_zero_conclusion"],
            "package_specific_fields": [
                "statement",
                "selmer_bound_argument",
                "review_notes",
            ],
        },
    }


def _transcript_bridge() -> dict[str, object]:
    rows = []
    for package_id, kernel in [
        ("rank-zero-selmer-AA-kernel-minus-p", "kernel_minus_p"),
        ("rank-zero-selmer-AA-kernel-pos-2sqrt-q", "kernel_pos_2sqrt_q"),
        ("rank-zero-selmer-BB-kernel-minus-p", "kernel_minus_p"),
        ("rank-zero-selmer-BB-kernel-pos-2sqrt-q", "kernel_pos_2sqrt_q"),
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


def _isogeny_setup_templates() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "package_count": 4,
        "kernel_schema_count": 2,
        "setup_template_count": 2,
        "shared_isogeny_setup_template_count": 2,
        "setup_templates": [
            {
                "kernel": "kernel_minus_p",
                "kernel_schema_id": "schema-kernel_minus_p",
                "package_count": 2,
                "package_ids": [
                    "rank-zero-selmer-AA-kernel-minus-p",
                    "rank-zero-selmer-BB-kernel-minus-p",
                ],
            },
            {
                "kernel": "kernel_pos_2sqrt_q",
                "kernel_schema_id": "schema-kernel_pos_2sqrt_q",
                "package_count": 2,
                "package_ids": [
                    "rank-zero-selmer-AA-kernel-pos-2sqrt-q",
                    "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
                ],
            },
        ],
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
    }


def _family_conclusion_templates() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "family_conclusion_template_count": 2,
        "kernel_bound_package_count": 4,
        "open_family_conclusion_count": 2,
        "rank_zero_conclusion_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "family_conclusion_templates": [
            {
                "family_pattern": "AA",
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
            },
            {
                "family_pattern": "BB",
                "required_kernel_bound_packages": [
                    {
                        "kernel": "kernel_minus_p",
                        "package_id": "rank-zero-selmer-BB-kernel-minus-p",
                        "transcript_package_ready": False,
                    },
                    {
                        "kernel": "kernel_pos_2sqrt_q",
                        "package_id": "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
                        "transcript_package_ready": False,
                    },
                ],
            },
        ],
    }


def test_bound_argument_queue_lists_primary_argument_tasks() -> None:
    queue = _queue_module()

    audit = queue.audit_rank_zero_selmer_bound_argument_queue(
        field_decomposition=_field_decomposition(),
        transcript_bridge=_transcript_bridge(),
        isogeny_setup_templates=_isogeny_setup_templates(),
        family_conclusion_templates=_family_conclusion_templates(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["primary_remaining_proof_field"] == "selmer_bound_argument"
    assert audit["bound_argument_task_count"] == 4
    assert audit["open_bound_argument_task_count"] == 4
    assert audit["kernel_template_reuse_count"] == 2
    assert audit["family_conclusion_target_count"] == 2
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["violations"] == []
    assert audit["tasks"][0] == {
        "package_id": "rank-zero-selmer-AA-kernel-minus-p",
        "family_pattern": "AA",
        "kernel": "kernel_minus_p",
        "kernel_schema_id": "schema-kernel_minus_p",
        "shared_setup_fields": [
            "local_squareclass_conditions",
            "isogeny_setup",
        ],
        "target_family_conclusion": "AA",
        "required_argument": "selmer_bound_argument",
        "acceptable_next_evidence": (
            "reviewable package-level Selmer bound argument transcript"
        ),
        "status": "open",
        "selmer_rank_upper_bound_proved": False,
        "family_exclusion_proved": False,
    }


def test_bound_argument_queue_rejects_wrong_primary_field() -> None:
    queue = _queue_module()
    field_decomposition = _field_decomposition()
    field_decomposition["primary_remaining_proof_field"] = "statement"

    audit = queue.audit_rank_zero_selmer_bound_argument_queue(
        field_decomposition=field_decomposition,
        transcript_bridge=_transcript_bridge(),
        isogeny_setup_templates=_isogeny_setup_templates(),
        family_conclusion_templates=_family_conclusion_templates(),
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["primary_remaining_proof_field_not_selmer_bound_argument"]


def test_bound_argument_queue_cli_writes_audit(tmp_path: Path) -> None:
    paths = {
        "field": tmp_path / "field.json",
        "bridge": tmp_path / "bridge.json",
        "isogeny": tmp_path / "isogeny.json",
        "family": tmp_path / "family.json",
    }
    paths["field"].write_text(json.dumps(_field_decomposition()), encoding="utf-8")
    paths["bridge"].write_text(json.dumps(_transcript_bridge()), encoding="utf-8")
    paths["isogeny"].write_text(
        json.dumps(_isogeny_setup_templates()), encoding="utf-8"
    )
    paths["family"].write_text(
        json.dumps(_family_conclusion_templates()), encoding="utf-8"
    )
    out = tmp_path / "queue.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_bound_argument_queue.py",
            "--field-decomposition",
            str(paths["field"]),
            "--transcript-bridge",
            str(paths["bridge"]),
            "--isogeny-setup-templates",
            str(paths["isogeny"]),
            "--family-conclusion-templates",
            str(paths["family"]),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "bound_argument_task_count=4" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["open_bound_argument_task_count"] == 4


def test_write_json_writes_sorted_bound_argument_queue(tmp_path: Path) -> None:
    queue = _queue_module()
    out = tmp_path / "queue.json"

    queue.write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
