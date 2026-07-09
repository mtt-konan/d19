from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_family_transcript_coverage import (
    BOUNDARY,
    audit_rank_zero_family_transcript_coverage,
    write_json,
)


def _family_obligations() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "rank_zero_family_obligation_count": 3,
        "groups": [
            {
                "pattern": "AA",
                "priority": 1,
                "candidate_class_count": 82,
                "model_count": 82,
            },
            {
                "pattern": "AA+BB",
                "priority": 2,
                "candidate_class_count": 43,
                "model_count": 86,
            },
            {
                "pattern": "BB",
                "priority": 3,
                "candidate_class_count": 75,
                "model_count": 75,
            },
        ],
    }


def _transcript_intake() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "package_count": 9,
        "transcript_package_ready_count": 0,
        "packages_with_reviewable_segment_count": 1,
        "packages": [
            {
                "package_id": "rank-zero-selmer-AA-kernel-minus-p",
                "transcript_package_ready": False,
                "reviewable_segment_count": 0,
            },
            {
                "package_id": "rank-zero-selmer-AA-kernel-neg-2sqrt-q",
                "transcript_package_ready": False,
                "reviewable_segment_count": 1,
            },
            {
                "package_id": "rank-zero-selmer-AA-kernel-pos-2sqrt_q",
                "transcript_package_ready": False,
                "reviewable_segment_count": 0,
            },
            {
                "package_id": "rank-zero-selmer-AA-BB-kernel-minus-p",
                "transcript_package_ready": False,
                "reviewable_segment_count": 0,
            },
            {
                "package_id": "rank-zero-selmer-AA-BB-kernel-neg-2sqrt-q",
                "transcript_package_ready": False,
                "reviewable_segment_count": 0,
            },
            {
                "package_id": "rank-zero-selmer-AA-BB-kernel-pos-2sqrt-q",
                "transcript_package_ready": False,
                "reviewable_segment_count": 0,
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-minus-p",
                "transcript_package_ready": False,
                "reviewable_segment_count": 0,
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-neg-2sqrt-q",
                "transcript_package_ready": False,
                "reviewable_segment_count": 0,
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
                "transcript_package_ready": False,
                "reviewable_segment_count": 0,
            },
        ],
    }


def test_rank_zero_family_transcript_coverage_reports_partial_progress_by_family() -> None:
    audit = audit_rank_zero_family_transcript_coverage(
        family_obligations=_family_obligations(),
        transcript_intake=_transcript_intake(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["family_count"] == 3
    assert audit["package_count"] == 9
    assert audit["packages_with_reviewable_segment_count"] == 1
    assert audit["transcript_package_ready_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["rank_zero_family_proof_complete"] is False
    assert audit["next_main_action"] == (
        "Expand family-proof progress by turning package-level reviewable segments "
        "into full rank-zero Selmer transcripts, without treating partial segments "
        "or sample growth as theorem completion."
    )
    assert audit["families"] == [
        {
            "pattern": "AA",
            "priority": 1,
            "candidate_class_count": 82,
            "model_count": 82,
            "package_count": 3,
            "transcript_package_ready_count": 0,
            "reviewable_segment_package_count": 1,
            "reviewable_segment_total": 1,
            "family_progress_status": "partial-reviewable-segment-present",
        },
        {
            "pattern": "AA+BB",
            "priority": 2,
            "candidate_class_count": 43,
            "model_count": 86,
            "package_count": 3,
            "transcript_package_ready_count": 0,
            "reviewable_segment_package_count": 0,
            "reviewable_segment_total": 0,
            "family_progress_status": "no-reviewable-segment-yet",
        },
        {
            "pattern": "BB",
            "priority": 3,
            "candidate_class_count": 75,
            "model_count": 75,
            "package_count": 3,
            "transcript_package_ready_count": 0,
            "reviewable_segment_package_count": 0,
            "reviewable_segment_total": 0,
            "family_progress_status": "no-reviewable-segment-yet",
        },
    ]
    assert audit["boundary"] == BOUNDARY


def test_rank_zero_family_transcript_coverage_requires_ready_inputs() -> None:
    obligations = _family_obligations()
    obligations["ready"] = False

    audit = audit_rank_zero_family_transcript_coverage(
        family_obligations=obligations,
        transcript_intake=_transcript_intake(),
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["family_obligations_not_ready"]


def test_rank_zero_family_transcript_coverage_cli_writes_audit(
    tmp_path: Path,
) -> None:
    obligations = tmp_path / "obligations.json"
    intake = tmp_path / "intake.json"
    out = tmp_path / "coverage.json"
    obligations.write_text(json.dumps(_family_obligations()), encoding="utf-8")
    intake.write_text(json.dumps(_transcript_intake()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_family_transcript_coverage.py",
            "--family-obligations",
            str(obligations),
            "--transcript-intake",
            str(intake),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "packages_with_reviewable_segment_count=1" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["families"][0]["family_progress_status"] == (
        "partial-reviewable-segment-present"
    )


def test_write_json_writes_sorted_rank_zero_family_transcript_coverage(
    tmp_path: Path,
) -> None:
    out = tmp_path / "coverage.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
