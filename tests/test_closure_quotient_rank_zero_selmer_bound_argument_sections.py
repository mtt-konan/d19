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

MODULE_NAME = "scripts.theory.audit_closure_quotient_rank_zero_selmer_bound_argument_sections"


def _sections_module() -> ModuleType:
    assert importlib.util.find_spec(MODULE_NAME) is not None
    return importlib.import_module(MODULE_NAME)


def _bound_argument_queue() -> dict[str, object]:
    tasks = []
    for package_id, family, kernel in [
        ("rank-zero-selmer-AA-kernel-minus-p", "AA", "kernel_minus_p"),
        ("rank-zero-selmer-BB-kernel-pos-2sqrt-q", "BB", "kernel_pos_2sqrt_q"),
    ]:
        tasks.append(
            {
                "package_id": package_id,
                "family_pattern": family,
                "kernel": kernel,
                "kernel_schema_id": f"schema-{kernel}",
                "shared_setup_fields": [
                    "local_squareclass_conditions",
                    "isogeny_setup",
                ],
                "target_family_conclusion": family,
                "required_argument": "selmer_bound_argument",
                "acceptable_next_evidence": (
                    "reviewable package-level Selmer bound argument transcript"
                ),
                "status": "open",
                "selmer_rank_upper_bound_proved": False,
                "family_exclusion_proved": False,
            }
        )
    return {
        "status": "ok",
        "ready": True,
        "primary_remaining_proof_field": "selmer_bound_argument",
        "bound_argument_task_count": 2,
        "open_bound_argument_task_count": 2,
        "kernel_template_reuse_count": 2,
        "family_conclusion_target_count": 2,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "tasks": tasks,
        "violations": [],
    }


def _odd_prime_local_image_schemas() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "input_reduction_shape_count": 2,
        "local_image_schema_count": 2,
        "local_image_schema_proved_count": 0,
        "local_image_schemas_not_conditions": True,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "schemas": [
            {
                "schema_id": "odd-prime-local-image-nonzero-double-root-tangent-1",
                "covered_lemma_ids": ["lemma-a"],
                "proof_status": "open",
                "local_image_schema_proved": False,
                "local_condition_proved": False,
            },
            {
                "schema_id": "odd-prime-local-image-zero-double-root-tangent--1",
                "covered_lemma_ids": ["lemma-b"],
                "proof_status": "open",
                "local_image_schema_proved": False,
                "local_condition_proved": False,
            },
        ],
        "violations": [],
    }


def _tangent_one_reduction_partition() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "reduction_partition_count": 1,
        "reduction_partition_exhausted_count": 1,
        "formal_lift_compatibility_proved_count": 0,
        "reduction_partition_not_local_image": True,
        "local_image_schema_proved_count": 0,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "partition_entries": [
            {
                "schema_id": "odd-prime-local-image-nonzero-double-root-tangent-1",
                "reduction_partition_exhausted": True,
                "formal_lift_compatibility_proved": False,
                "local_image_schema_proved": False,
                "remaining_gap": "promote reduction-level partition through formal lifts",
            }
        ],
        "violations": [],
    }


def _tangent_minus_one_reduction_partition() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "reduction_partition_count": 1,
        "reduction_partition_exhausted_count": 1,
        "formal_lift_compatibility_proved_count": 0,
        "reduction_partition_not_local_image": True,
        "local_image_schema_proved_count": 0,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "partition_entries": [
            {
                "schema_id": "odd-prime-local-image-zero-double-root-tangent--1",
                "reduction_partition_exhausted": True,
                "formal_lift_compatibility_proved": False,
                "local_image_schema_proved": False,
                "remaining_gap": "promote reduction-level partition through formal lifts",
            }
        ],
        "violations": [],
    }


def test_bound_argument_sections_decompose_open_package_tasks() -> None:
    sections = _sections_module()

    audit = sections.audit_rank_zero_selmer_bound_argument_sections(
        bound_argument_queue=_bound_argument_queue(),
        odd_prime_local_image_schemas=_odd_prime_local_image_schemas(),
        tangent_one_reduction_partition=_tangent_one_reduction_partition(),
        tangent_minus_one_reduction_partition=_tangent_minus_one_reduction_partition(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["bound_argument_outline_count"] == 2
    assert audit["open_bound_argument_outline_count"] == 2
    assert audit["required_section_per_outline_count"] == 5
    assert audit["required_section_count"] == 10
    assert audit["shared_odd_prime_local_image_schema_count"] == 2
    assert audit["reduction_partition_outline_count"] == 2
    assert audit["formal_lift_compatibility_proved_count"] == 0
    assert audit["local_image_schema_proved_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["violations"] == []
    assert audit["argument_outlines"][0] == {
        "package_id": "rank-zero-selmer-AA-kernel-minus-p",
        "family_pattern": "AA",
        "kernel": "kernel_minus_p",
        "required_argument": "selmer_bound_argument",
        "required_sections": [
            "shared_isogeny_setup_reference",
            "odd_prime_local_image_theorems",
            "formal_lift_compatibility",
            "dyadic_local_condition",
            "global_selmer_dimension_bound",
        ],
        "shared_odd_prime_local_image_schema_count": 2,
        "reduction_partition_outline_count": 2,
        "acceptable_next_evidence": (
            "reviewable package-level Selmer bound argument transcript"
        ),
        "status": "open",
        "proof_status": "sections-open-not-proof",
        "selmer_rank_upper_bound_proved": False,
        "family_exclusion_proved": False,
    }


def test_bound_argument_sections_reject_local_image_claims() -> None:
    sections = _sections_module()
    local_images = _odd_prime_local_image_schemas()
    local_images["local_image_schema_proved_count"] = 1

    audit = sections.audit_rank_zero_selmer_bound_argument_sections(
        bound_argument_queue=_bound_argument_queue(),
        odd_prime_local_image_schemas=local_images,
        tangent_one_reduction_partition=_tangent_one_reduction_partition(),
        tangent_minus_one_reduction_partition=_tangent_minus_one_reduction_partition(),
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["local_image_schema_claim_count_nonzero"]


def test_bound_argument_sections_cli_writes_audit(tmp_path: Path) -> None:
    paths = {
        "queue": tmp_path / "queue.json",
        "local": tmp_path / "local.json",
        "plus": tmp_path / "plus.json",
        "minus": tmp_path / "minus.json",
    }
    paths["queue"].write_text(json.dumps(_bound_argument_queue()), encoding="utf-8")
    paths["local"].write_text(
        json.dumps(_odd_prime_local_image_schemas()), encoding="utf-8"
    )
    paths["plus"].write_text(
        json.dumps(_tangent_one_reduction_partition()), encoding="utf-8"
    )
    paths["minus"].write_text(
        json.dumps(_tangent_minus_one_reduction_partition()), encoding="utf-8"
    )
    out = tmp_path / "sections.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_bound_argument_sections.py",
            "--bound-argument-queue",
            str(paths["queue"]),
            "--odd-prime-local-image-schemas",
            str(paths["local"]),
            "--tangent-one-reduction-partition",
            str(paths["plus"]),
            "--tangent-minus-one-reduction-partition",
            str(paths["minus"]),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "bound_argument_outline_count=2" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["required_section_count"] == 10


def test_write_json_writes_sorted_bound_argument_sections(tmp_path: Path) -> None:
    sections = _sections_module()
    out = tmp_path / "sections.json"

    sections.write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
