from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_family_formal_lift_coverage import (
    BOUNDARY,
    audit_rank_zero_family_formal_lift_coverage,
    write_json,
)


def _family_obligations() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "groups": [
            {"pattern": "AA", "priority": 1, "candidate_class_count": 82, "model_count": 82},
            {"pattern": "AA+BB", "priority": 2, "candidate_class_count": 43, "model_count": 86},
            {"pattern": "BB", "priority": 3, "candidate_class_count": 75, "model_count": 75},
        ],
    }


def _package_segments() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "segments": [
            {
                "package_id": "rank-zero-selmer-AA-kernel-minus-p",
                "required_field": "selmer_bound_argument",
                "proof_section": "formal_lift_compatibility",
                "segment_status": "reviewable-proof",
            },
            {
                "package_id": "rank-zero-selmer-AA-kernel-neg-2sqrt-q",
                "required_field": "selmer_bound_argument",
                "proof_section": "formal_lift_compatibility",
                "segment_status": "reviewable-proof",
            },
            {
                "package_id": "rank-zero-selmer-AA-kernel-pos-2sqrt-q",
                "required_field": "selmer_bound_argument",
                "proof_section": "formal_lift_compatibility",
                "segment_status": "reviewable-proof",
            },
        ],
    }


def _package_segments_with_partial_bb() -> dict[str, object]:
    payload = _package_segments()
    payload["segments"] = list(payload["segments"]) + [
        {
            "package_id": "rank-zero-selmer-BB-kernel-neg-2sqrt-q",
            "required_field": "selmer_bound_argument",
            "proof_section": "formal_lift_compatibility",
            "segment_status": "reviewable-proof",
        }
    ]
    return payload


def _package_segments_all_families_complete() -> dict[str, object]:
    payload = _package_segments()
    payload["segments"] = list(payload["segments"]) + [
        {
            "package_id": "rank-zero-selmer-AA-BB-kernel-minus-p",
            "required_field": "selmer_bound_argument",
            "proof_section": "formal_lift_compatibility",
            "segment_status": "reviewable-proof",
        },
        {
            "package_id": "rank-zero-selmer-AA-BB-kernel-neg-2sqrt-q",
            "required_field": "selmer_bound_argument",
            "proof_section": "formal_lift_compatibility",
            "segment_status": "reviewable-proof",
        },
        {
            "package_id": "rank-zero-selmer-AA-BB-kernel-pos-2sqrt-q",
            "required_field": "selmer_bound_argument",
            "proof_section": "formal_lift_compatibility",
            "segment_status": "reviewable-proof",
        },
        {
            "package_id": "rank-zero-selmer-BB-kernel-minus-p",
            "required_field": "selmer_bound_argument",
            "proof_section": "formal_lift_compatibility",
            "segment_status": "reviewable-proof",
        },
        {
            "package_id": "rank-zero-selmer-BB-kernel-neg-2sqrt-q",
            "required_field": "selmer_bound_argument",
            "proof_section": "formal_lift_compatibility",
            "segment_status": "reviewable-proof",
        },
        {
            "package_id": "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
            "required_field": "selmer_bound_argument",
            "proof_section": "formal_lift_compatibility",
            "segment_status": "reviewable-proof",
        },
    ]
    return payload


def test_rank_zero_family_formal_lift_coverage_marks_aa_complete_at_odd_primes() -> None:
    audit = audit_rank_zero_family_formal_lift_coverage(
        family_obligations=_family_obligations(),
        package_segments=_package_segments(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["family_count"] == 3
    assert audit["reviewable_formal_lift_package_count"] == 3
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["families"] == [
        {
            "pattern": "AA",
            "priority": 1,
            "candidate_class_count": 82,
            "model_count": 82,
            "package_count": 3,
            "reviewable_formal_lift_package_count": 3,
            "odd_prime_formal_lift_complete": True,
            "family_progress_status": "odd-prime-formal-lift-complete-not-proof",
        },
        {
            "pattern": "AA+BB",
            "priority": 2,
            "candidate_class_count": 43,
            "model_count": 86,
            "package_count": 3,
            "reviewable_formal_lift_package_count": 0,
            "odd_prime_formal_lift_complete": False,
            "family_progress_status": "no-reviewable-formal-lift-segment-yet",
        },
        {
            "pattern": "BB",
            "priority": 3,
            "candidate_class_count": 75,
            "model_count": 75,
            "package_count": 3,
            "reviewable_formal_lift_package_count": 0,
            "odd_prime_formal_lift_complete": False,
            "family_progress_status": "no-reviewable-formal-lift-segment-yet",
        },
    ]
    assert audit["next_main_action"] == (
        "For AA, move from odd-prime formal-lift completion to the dyadic local "
        "condition, global Selmer dimension bound, and rank-zero conclusion; for "
        "AA+BB and BB, continue obtaining reviewable formal-lift segments until "
        "each family closes all three packages."
    )
    assert audit["boundary"] == BOUNDARY


def test_rank_zero_family_formal_lift_coverage_marks_partial_bb_progress() -> None:
    audit = audit_rank_zero_family_formal_lift_coverage(
        family_obligations=_family_obligations(),
        package_segments=_package_segments_with_partial_bb(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["reviewable_formal_lift_package_count"] == 4
    assert audit["families"] == [
        {
            "pattern": "AA",
            "priority": 1,
            "candidate_class_count": 82,
            "model_count": 82,
            "package_count": 3,
            "reviewable_formal_lift_package_count": 3,
            "odd_prime_formal_lift_complete": True,
            "family_progress_status": "odd-prime-formal-lift-complete-not-proof",
        },
        {
            "pattern": "AA+BB",
            "priority": 2,
            "candidate_class_count": 43,
            "model_count": 86,
            "package_count": 3,
            "reviewable_formal_lift_package_count": 0,
            "odd_prime_formal_lift_complete": False,
            "family_progress_status": "no-reviewable-formal-lift-segment-yet",
        },
        {
            "pattern": "BB",
            "priority": 3,
            "candidate_class_count": 75,
            "model_count": 75,
            "package_count": 3,
            "reviewable_formal_lift_package_count": 1,
            "odd_prime_formal_lift_complete": False,
            "family_progress_status": "partial-reviewable-formal-lift-segment-present",
        },
    ]


def test_rank_zero_family_formal_lift_coverage_moves_on_when_all_families_complete() -> None:
    audit = audit_rank_zero_family_formal_lift_coverage(
        family_obligations=_family_obligations(),
        package_segments=_package_segments_all_families_complete(),
    )

    assert audit["status"] == "ok"
    assert audit["reviewable_formal_lift_package_count"] == 9
    assert all(family["odd_prime_formal_lift_complete"] for family in audit["families"])
    assert audit["next_main_action"] == (
        "Odd-prime formal-lift coverage is complete for AA, AA+BB, and BB; "
        "move to the dyadic local conditions, global Selmer dimension bounds, "
        "and rank-zero conclusions without treating partial transcripts as "
        "family-level theorems."
    )


def test_rank_zero_family_formal_lift_coverage_requires_ready_inputs() -> None:
    obligations = _family_obligations()
    obligations["ready"] = False

    audit = audit_rank_zero_family_formal_lift_coverage(
        family_obligations=obligations,
        package_segments=_package_segments(),
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["family_obligations_not_ready"]


def test_rank_zero_family_formal_lift_coverage_cli_writes_audit(
    tmp_path: Path,
) -> None:
    obligations = tmp_path / "obligations.json"
    segments = tmp_path / "segments.json"
    out = tmp_path / "coverage.json"
    obligations.write_text(json.dumps(_family_obligations()), encoding="utf-8")
    segments.write_text(json.dumps(_package_segments()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_family_formal_lift_coverage.py",
            "--family-obligations",
            str(obligations),
            "--package-segments",
            str(segments),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "reviewable_formal_lift_package_count=3" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["families"][0]["family_progress_status"] == (
        "odd-prime-formal-lift-complete-not-proof"
    )


def test_write_json_writes_sorted_rank_zero_family_formal_lift_coverage(
    tmp_path: Path,
) -> None:
    out = tmp_path / "coverage.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
