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

MODULE_NAME = "scripts.theory.audit_closure_quotient_rank_zero_selmer_formal_lift_queue"


def _queue_module() -> ModuleType:
    assert importlib.util.find_spec(MODULE_NAME) is not None
    return importlib.import_module(MODULE_NAME)


def _bound_argument_sections() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "bound_argument_outline_count": 2,
        "open_bound_argument_outline_count": 2,
        "required_section_per_outline_count": 5,
        "required_section_count": 10,
        "shared_odd_prime_local_image_schema_count": 2,
        "reduction_partition_outline_count": 2,
        "formal_lift_compatibility_proved_count": 0,
        "local_image_schema_proved_count": 0,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "required_sections": [
            "shared_isogeny_setup_reference",
            "odd_prime_local_image_theorems",
            "formal_lift_compatibility",
            "dyadic_local_condition",
            "global_selmer_dimension_bound",
        ],
        "argument_outlines": [
            {
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
                "status": "open",
                "proof_status": "sections-open-not-proof",
                "selmer_rank_upper_bound_proved": False,
                "family_exclusion_proved": False,
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
                "family_pattern": "BB",
                "kernel": "kernel_pos_2sqrt_q",
                "required_argument": "selmer_bound_argument",
                "required_sections": [
                    "shared_isogeny_setup_reference",
                    "odd_prime_local_image_theorems",
                    "formal_lift_compatibility",
                    "dyadic_local_condition",
                    "global_selmer_dimension_bound",
                ],
                "status": "open",
                "proof_status": "sections-open-not-proof",
                "selmer_rank_upper_bound_proved": False,
                "family_exclusion_proved": False,
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
                "standard_model": "Y^2 = X*(X - 1)^2",
                "tracked_coordinate": "X",
                "reduction_pieces": [
                    "non-node branch",
                    "punctured node neighborhood",
                    "node center",
                ],
                "candidate_squareclass_set": ["trivial"],
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
                "standard_model": "Y^2 = nu*X^2*(1 - X)",
                "tracked_coordinate": "1 - X",
                "reduction_pieces": [
                    "non-node branch",
                    "punctured node neighborhood",
                    "node center",
                ],
                "candidate_squareclass_set": ["nu", "trivial"],
                "excluded_reduction_pieces": ["punctured node neighborhood"],
                "reduction_partition_exhausted": True,
                "formal_lift_compatibility_proved": False,
                "local_image_schema_proved": False,
                "remaining_gap": "promote reduction-level partition through formal lifts",
            }
        ],
        "violations": [],
    }


def test_formal_lift_queue_lists_reduction_partition_tasks() -> None:
    queue = _queue_module()

    audit = queue.audit_rank_zero_selmer_formal_lift_queue(
        bound_argument_sections=_bound_argument_sections(),
        tangent_one_reduction_partition=_tangent_one_reduction_partition(),
        tangent_minus_one_reduction_partition=_tangent_minus_one_reduction_partition(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["covered_bound_argument_outline_count"] == 2
    assert audit["formal_lift_task_count"] == 2
    assert audit["open_formal_lift_task_count"] == 2
    assert audit["reduction_partition_exhausted_count"] == 2
    assert audit["formal_lift_compatibility_proved_count"] == 0
    assert audit["local_image_schema_proved_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["violations"] == []
    assert audit["formal_lift_tasks"][0] == {
        "task_id": "formal-lift-odd-prime-local-image-nonzero-double-root-tangent-1",
        "schema_id": "odd-prime-local-image-nonzero-double-root-tangent-1",
        "source_partition": "tangent_one_reduction_partition",
        "standard_model": "Y^2 = X*(X - 1)^2",
        "tracked_coordinate": "X",
        "reduction_pieces": [
            "non-node branch",
            "punctured node neighborhood",
            "node center",
        ],
        "candidate_squareclass_set": ["trivial"],
        "excluded_reduction_pieces": [],
        "required_section": "formal_lift_compatibility",
        "acceptable_next_evidence": (
            "reviewable formal-lift compatibility theorem for this local-image schema"
        ),
        "status": "open",
        "formal_lift_compatibility_proved": False,
        "local_image_schema_proved": False,
    }


def test_formal_lift_queue_rejects_promoted_formal_lift_claim() -> None:
    queue = _queue_module()
    tangent_one = _tangent_one_reduction_partition()
    tangent_one["formal_lift_compatibility_proved_count"] = 1

    audit = queue.audit_rank_zero_selmer_formal_lift_queue(
        bound_argument_sections=_bound_argument_sections(),
        tangent_one_reduction_partition=tangent_one,
        tangent_minus_one_reduction_partition=_tangent_minus_one_reduction_partition(),
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "tangent_one_formal_lift_compatibility_claim_count_nonzero"
    ]


def test_formal_lift_queue_cli_writes_audit(tmp_path: Path) -> None:
    paths = {
        "sections": tmp_path / "sections.json",
        "plus": tmp_path / "plus.json",
        "minus": tmp_path / "minus.json",
    }
    paths["sections"].write_text(
        json.dumps(_bound_argument_sections()), encoding="utf-8"
    )
    paths["plus"].write_text(
        json.dumps(_tangent_one_reduction_partition()), encoding="utf-8"
    )
    paths["minus"].write_text(
        json.dumps(_tangent_minus_one_reduction_partition()), encoding="utf-8"
    )
    out = tmp_path / "formal_lift_queue.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_formal_lift_queue.py",
            "--bound-argument-sections",
            str(paths["sections"]),
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

    assert "formal_lift_task_count=2" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["open_formal_lift_task_count"] == 2


def test_write_json_writes_sorted_formal_lift_queue(tmp_path: Path) -> None:
    queue = _queue_module()
    out = tmp_path / "formal_lift_queue.json"

    queue.write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
