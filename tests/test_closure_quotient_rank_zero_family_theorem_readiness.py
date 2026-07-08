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

MODULE_NAME = "scripts.theory.audit_closure_quotient_rank_zero_family_theorem_readiness"


def _readiness_module() -> ModuleType:
    assert importlib.util.find_spec(MODULE_NAME) is not None
    return importlib.import_module(MODULE_NAME)


def _lambda_handoff() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lambda_structural_handoff_ready": True,
        "route_counts": {
            "rank-zero-family-generalization": 3,
            "root-number-rank-structure-triage": 2,
            "two-cover-or-reviewable-no-point-certificate": 1,
        },
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "closure_quotient_promoted_to_lambda_proof": False,
    }


def _family_obligations() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "rank_zero_family_proof_complete": False,
        "candidate_class_count": 3,
        "primitive_model_count": 4,
        "rank_zero_family_obligation_count": 2,
        "open_obligation_count": 2,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
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
                "model_count": 2,
                "family_exclusion_proved": False,
            },
        ],
    }


def _symbolic_inputs() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "primitive_model_count": 4,
        "symbolic_formula_verified_count": 4,
        "symbolic_formula_violation_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
    }


def _isogeny_templates() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "primitive_model_count": 4,
        "kernel_count": 3,
        "isogeny_template_verified_count": 12,
        "isogeny_template_violation_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
    }


def _local_supports() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "package_count": 6,
        "support_entry_count": 6,
        "kernel_count": 3,
        "support_candidates_not_conditions": True,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
    }


def _selmer_obligations() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "rank_zero_selmer_obligations_complete": False,
        "family_obligation_count": 2,
        "kernel_count": 3,
        "selmer_obligation_count": 6,
        "open_selmer_obligation_count": 6,
        "primitive_model_count": 4,
        "isogeny_template_verified_count": 12,
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
                    "kernel_neg_2sqrt_q",
                    "kernel_pos_2sqrt_q",
                ],
                "selmer_rank_upper_bound_proved": False,
                "family_exclusion_proved": False,
            },
            {
                "pattern": "BB",
                "candidate_class_count": 1,
                "model_count": 2,
                "required_kernel_obligations": [
                    "kernel_minus_p",
                    "kernel_neg_2sqrt_q",
                    "kernel_pos_2sqrt_q",
                ],
                "selmer_rank_upper_bound_proved": False,
                "family_exclusion_proved": False,
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
    }


def test_rank_zero_family_theorem_readiness_keeps_transcripts_as_blocker() -> None:
    readiness = _readiness_module()

    audit = readiness.audit_rank_zero_family_theorem_readiness(
        lambda_handoff=_lambda_handoff(),
        family_obligations=_family_obligations(),
        symbolic_inputs=_symbolic_inputs(),
        isogeny_templates=_isogeny_templates(),
        local_supports=_local_supports(),
        selmer_obligations=_selmer_obligations(),
        transcript_intake=_transcript_intake(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["rank_zero_input_chain_ready"] is True
    assert audit["rank_zero_family_theorem_ready"] is False
    assert audit["rank_zero_route_class_count"] == 3
    assert audit["family_obligation_count"] == 2
    assert audit["selmer_obligation_count"] == 6
    assert audit["open_selmer_obligation_count"] == 6
    assert audit["transcript_package_ready_count"] == 0
    assert audit["missing_transcript_package_count"] == 6
    assert audit["strict_promotion_ready_count"] == 0
    assert audit["local_condition_proved_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["next_blocker"] == "rank-zero-selmer-transcripts-missing-not-proof"
    assert audit["readiness_rows"] == [
        {
            "pattern": "AA",
            "candidate_class_count": 2,
            "model_count": 2,
            "required_kernel_obligations": [
                "kernel_minus_p",
                "kernel_neg_2sqrt_q",
                "kernel_pos_2sqrt_q",
            ],
            "acceptable_next_evidence": (
                "uniform isogeny-Selmer rank-bound transcript or external "
                "reviewable rank-zero theorem certificate"
            ),
            "family_exclusion_proved": False,
        },
        {
            "pattern": "BB",
            "candidate_class_count": 1,
            "model_count": 2,
            "required_kernel_obligations": [
                "kernel_minus_p",
                "kernel_neg_2sqrt_q",
                "kernel_pos_2sqrt_q",
            ],
            "acceptable_next_evidence": (
                "uniform isogeny-Selmer rank-bound transcript or external "
                "reviewable rank-zero theorem certificate"
            ),
            "family_exclusion_proved": False,
        },
    ]


def test_rank_zero_family_theorem_readiness_rejects_local_condition_promotion() -> None:
    readiness = _readiness_module()
    local_supports = _local_supports()
    local_supports["local_condition_proved_count"] = 1

    audit = readiness.audit_rank_zero_family_theorem_readiness(
        lambda_handoff=_lambda_handoff(),
        family_obligations=_family_obligations(),
        symbolic_inputs=_symbolic_inputs(),
        isogeny_templates=_isogeny_templates(),
        local_supports=local_supports,
        selmer_obligations=_selmer_obligations(),
        transcript_intake=_transcript_intake(),
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "local_supports_promoted_to_conditions",
    ]


def test_rank_zero_family_theorem_readiness_cli_writes_audit(tmp_path: Path) -> None:
    paths = {
        "lambda": tmp_path / "lambda.json",
        "family": tmp_path / "family.json",
        "symbolic": tmp_path / "symbolic.json",
        "isogeny": tmp_path / "isogeny.json",
        "local": tmp_path / "local.json",
        "selmer": tmp_path / "selmer.json",
        "transcript": tmp_path / "transcript.json",
    }
    paths["lambda"].write_text(json.dumps(_lambda_handoff()), encoding="utf-8")
    paths["family"].write_text(json.dumps(_family_obligations()), encoding="utf-8")
    paths["symbolic"].write_text(json.dumps(_symbolic_inputs()), encoding="utf-8")
    paths["isogeny"].write_text(json.dumps(_isogeny_templates()), encoding="utf-8")
    paths["local"].write_text(json.dumps(_local_supports()), encoding="utf-8")
    paths["selmer"].write_text(json.dumps(_selmer_obligations()), encoding="utf-8")
    paths["transcript"].write_text(json.dumps(_transcript_intake()), encoding="utf-8")
    out = tmp_path / "readiness.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_family_theorem_readiness.py",
            "--lambda-handoff",
            str(paths["lambda"]),
            "--family-obligations",
            str(paths["family"]),
            "--symbolic-inputs",
            str(paths["symbolic"]),
            "--isogeny-templates",
            str(paths["isogeny"]),
            "--local-supports",
            str(paths["local"]),
            "--selmer-obligations",
            str(paths["selmer"]),
            "--transcript-intake",
            str(paths["transcript"]),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "rank_zero_family_theorem_ready=False" in result.stdout
    assert "missing_transcript_package_count=6" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["rank_zero_input_chain_ready"] is True


def test_write_json_writes_sorted_rank_zero_family_theorem_readiness(
    tmp_path: Path,
) -> None:
    readiness = _readiness_module()
    out = tmp_path / "readiness.json"

    readiness.write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
