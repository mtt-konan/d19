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
    "scripts.theory.audit_closure_quotient_rank_zero_selmer_transcript_bridge"
)


def _bridge_module() -> ModuleType:
    assert importlib.util.find_spec(MODULE_NAME) is not None
    return importlib.import_module(MODULE_NAME)


def _materialization() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "package_count": 6,
        "open_package_count": 6,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "packages": [
            {
                "package_id": "rank-zero-selmer-AA-kernel-minus-p",
                "json_path": "results/packages/rank-zero-selmer-AA-kernel-minus-p.json",
                "markdown_path": "results/packages/rank-zero-selmer-AA-kernel-minus-p.md",
                "status": "open",
                "transcript_status": "missing",
            },
            {
                "package_id": "rank-zero-selmer-AA-kernel-pos-2sqrt-q",
                "json_path": (
                    "results/packages/rank-zero-selmer-AA-kernel-pos-2sqrt-q.json"
                ),
                "markdown_path": (
                    "results/packages/rank-zero-selmer-AA-kernel-pos-2sqrt-q.md"
                ),
                "status": "open",
                "transcript_status": "missing",
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-minus-p",
                "json_path": "results/packages/rank-zero-selmer-BB-kernel-minus-p.json",
                "markdown_path": "results/packages/rank-zero-selmer-BB-kernel-minus-p.md",
                "status": "open",
                "transcript_status": "missing",
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
                "json_path": (
                    "results/packages/rank-zero-selmer-BB-kernel-pos-2sqrt-q.json"
                ),
                "markdown_path": (
                    "results/packages/rank-zero-selmer-BB-kernel-pos-2sqrt-q.md"
                ),
                "status": "open",
                "transcript_status": "missing",
            },
            {
                "package_id": "rank-zero-selmer-AA-BB-kernel-minus-p",
                "json_path": (
                    "results/packages/rank-zero-selmer-AA-BB-kernel-minus-p.json"
                ),
                "markdown_path": (
                    "results/packages/rank-zero-selmer-AA-BB-kernel-minus-p.md"
                ),
                "status": "open",
                "transcript_status": "missing",
            },
            {
                "package_id": "rank-zero-selmer-AA-BB-kernel-pos-2sqrt-q",
                "json_path": (
                    "results/packages/rank-zero-selmer-AA-BB-kernel-pos-2sqrt-q.json"
                ),
                "markdown_path": (
                    "results/packages/rank-zero-selmer-AA-BB-kernel-pos-2sqrt-q.md"
                ),
                "status": "open",
                "transcript_status": "missing",
            },
        ],
    }


def _kernel_local_schemas() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "package_count": 6,
        "support_entry_count": 6,
        "family_pattern_count": 3,
        "kernel_schema_count": 2,
        "shared_kernel_schema_count": 2,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "kernel_schemas": [
            {
                "schema_id": "rank-zero-selmer-local-support-kernel-minus-p",
                "kernel": "kernel_minus_p",
                "family_patterns": ["AA", "AA+BB", "BB"],
                "package_ids": [
                    "rank-zero-selmer-AA-BB-kernel-minus-p",
                    "rank-zero-selmer-AA-kernel-minus-p",
                    "rank-zero-selmer-BB-kernel-minus-p",
                ],
                "package_count": 3,
            },
            {
                "schema_id": "rank-zero-selmer-local-support-kernel-pos-2sqrt-q",
                "kernel": "kernel_pos_2sqrt_q",
                "family_patterns": ["AA", "AA+BB", "BB"],
                "package_ids": [
                    "rank-zero-selmer-AA-BB-kernel-pos-2sqrt-q",
                    "rank-zero-selmer-AA-kernel-pos-2sqrt-q",
                    "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
                ],
                "package_count": 3,
            },
        ],
    }


def _transcript_intake() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "package_count": 6,
        "open_package_count": 6,
        "transcript_package_ready_count": 0,
        "missing_transcript_package_count": 6,
        "strict_promotion_ready_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "candidate_not_proof": True,
        "proof_status": "rank-zero-selmer-transcripts-missing-not-proof",
        "packages": [
            {
                "package_id": "rank-zero-selmer-AA-kernel-minus-p",
                "missing_fields": [
                    "statement",
                    "isogeny_setup",
                    "local_squareclass_conditions",
                    "selmer_bound_argument",
                    "rank_zero_conclusion",
                    "review_notes",
                ],
                "transcript_package_ready": False,
                "strict_promotion_ready": False,
            },
            {
                "package_id": "rank-zero-selmer-AA-kernel-pos-2sqrt-q",
                "missing_fields": [
                    "statement",
                    "isogeny_setup",
                    "local_squareclass_conditions",
                    "selmer_bound_argument",
                    "rank_zero_conclusion",
                    "review_notes",
                ],
                "transcript_package_ready": False,
                "strict_promotion_ready": False,
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-minus-p",
                "missing_fields": [
                    "statement",
                    "isogeny_setup",
                    "local_squareclass_conditions",
                    "selmer_bound_argument",
                    "rank_zero_conclusion",
                    "review_notes",
                ],
                "transcript_package_ready": False,
                "strict_promotion_ready": False,
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
                "missing_fields": [
                    "statement",
                    "isogeny_setup",
                    "local_squareclass_conditions",
                    "selmer_bound_argument",
                    "rank_zero_conclusion",
                    "review_notes",
                ],
                "transcript_package_ready": False,
                "strict_promotion_ready": False,
            },
            {
                "package_id": "rank-zero-selmer-AA-BB-kernel-minus-p",
                "missing_fields": [
                    "statement",
                    "isogeny_setup",
                    "local_squareclass_conditions",
                    "selmer_bound_argument",
                    "rank_zero_conclusion",
                    "review_notes",
                ],
                "transcript_package_ready": False,
                "strict_promotion_ready": False,
            },
            {
                "package_id": "rank-zero-selmer-AA-BB-kernel-pos-2sqrt-q",
                "missing_fields": [
                    "statement",
                    "isogeny_setup",
                    "local_squareclass_conditions",
                    "selmer_bound_argument",
                    "rank_zero_conclusion",
                    "review_notes",
                ],
                "transcript_package_ready": False,
                "strict_promotion_ready": False,
            },
        ],
    }


def test_transcript_bridge_reuses_kernel_local_templates() -> None:
    bridge = _bridge_module()

    audit = bridge.audit_rank_zero_selmer_transcript_bridge(
        materialization=_materialization(),
        kernel_local_schemas=_kernel_local_schemas(),
        transcript_intake=_transcript_intake(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["package_count"] == 6
    assert audit["kernel_schema_count"] == 2
    assert audit["shared_local_squareclass_template_count"] == 2
    assert audit["package_specific_transcript_count"] == 6
    assert audit["transcript_package_ready_count"] == 0
    assert audit["strict_promotion_ready_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["violations"] == []
    assert audit["bridge_rows"][0] == {
        "package_id": "rank-zero-selmer-AA-BB-kernel-minus-p",
        "kernel": "kernel_minus_p",
        "kernel_schema_id": "rank-zero-selmer-local-support-kernel-minus-p",
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


def test_transcript_bridge_reports_package_without_kernel_schema() -> None:
    bridge = _bridge_module()
    schemas = _kernel_local_schemas()
    schemas["kernel_schemas"] = schemas["kernel_schemas"][:1]
    schemas["kernel_schema_count"] = 1
    schemas["shared_kernel_schema_count"] = 1

    audit = bridge.audit_rank_zero_selmer_transcript_bridge(
        materialization=_materialization(),
        kernel_local_schemas=schemas,
        transcript_intake=_transcript_intake(),
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "package_kernel_missing_schema=rank-zero-selmer-AA-BB-kernel-pos-2sqrt-q",
        "package_kernel_missing_schema=rank-zero-selmer-AA-kernel-pos-2sqrt-q",
        "package_kernel_missing_schema=rank-zero-selmer-BB-kernel-pos-2sqrt-q",
    ]


def test_transcript_bridge_cli_writes_audit(tmp_path: Path) -> None:
    paths = {
        "materialization": tmp_path / "materialization.json",
        "schemas": tmp_path / "schemas.json",
        "intake": tmp_path / "intake.json",
    }
    paths["materialization"].write_text(
        json.dumps(_materialization()), encoding="utf-8"
    )
    paths["schemas"].write_text(json.dumps(_kernel_local_schemas()), encoding="utf-8")
    paths["intake"].write_text(json.dumps(_transcript_intake()), encoding="utf-8")
    out = tmp_path / "bridge.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_transcript_bridge.py",
            "--materialization",
            str(paths["materialization"]),
            "--kernel-local-schemas",
            str(paths["schemas"]),
            "--transcript-intake",
            str(paths["intake"]),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "shared_local_squareclass_template_count=2" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["package_specific_transcript_count"] == 6


def test_write_json_writes_sorted_transcript_bridge(tmp_path: Path) -> None:
    bridge = _bridge_module()
    out = tmp_path / "bridge.json"

    bridge.write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
