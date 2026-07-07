from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_selmer_transcript_intake import (
    BOUNDARY,
    REQUIRED_TRANSCRIPT_TYPE,
    audit_rank_zero_selmer_transcript_intake,
    template_index,
    write_json,
)


def _materialization() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "package_count": 2,
        "open_package_count": 2,
        "materialized_json_count": 2,
        "materialized_markdown_count": 2,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "packages_dir": "packages",
        "packages": [
            {
                "package_id": "rank-zero-selmer-AA-kernel-minus-p",
                "json_path": "packages/rank-zero-selmer-AA-kernel-minus-p.json",
                "markdown_path": "packages/rank-zero-selmer-AA-kernel-minus-p.md",
                "status": "open",
                "transcript_status": "missing",
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
                "json_path": "packages/rank-zero-selmer-BB-kernel-pos-2sqrt-q.json",
                "markdown_path": "packages/rank-zero-selmer-BB-kernel-pos-2sqrt-q.md",
                "status": "open",
                "transcript_status": "missing",
            },
        ],
    }


def _write_packages(root: Path) -> None:
    packages_dir = root / "packages"
    packages_dir.mkdir()
    for package in _materialization()["packages"]:
        payload = {
            "package_id": package["package_id"],
            "status": "open",
            "transcript_status": "missing",
            "required_transcript_fields": [
                "statement",
                "isogeny_setup",
                "local_squareclass_conditions",
                "selmer_bound_argument",
                "rank_zero_conclusion",
                "review_notes",
            ],
            "selmer_rank_upper_bound_proved": False,
            "family_exclusion_proved": False,
        }
        (root / package["json_path"]).write_text(
            json.dumps(payload), encoding="utf-8"
        )


def _transcript_index(transcript_path: Path) -> dict[str, object]:
    return {
        "packages": [
            {
                "package_id": "rank-zero-selmer-AA-kernel-minus-p",
                "transcript_path": str(transcript_path),
                "transcript_type": REQUIRED_TRANSCRIPT_TYPE,
                "result": "uniform-isogeny-selmer-rank-bound",
                "field_status": {
                    "statement": "present",
                    "isogeny_setup": "present",
                    "local_squareclass_conditions": "present",
                    "selmer_bound_argument": "present",
                    "rank_zero_conclusion": "present",
                    "review_notes": "present",
                },
            }
        ]
    }


def test_transcript_intake_without_index_keeps_all_packages_open(tmp_path: Path) -> None:
    _write_packages(tmp_path)

    audit = audit_rank_zero_selmer_transcript_intake(
        materialization=_materialization(),
        transcript_index=None,
        root=tmp_path,
    )

    assert audit == {
        "status": "ok",
        "ready": True,
        "package_count": 2,
        "open_package_count": 2,
        "transcript_package_ready_count": 0,
        "missing_transcript_package_count": 2,
        "strict_promotion_ready_count": 0,
        "strict_promotion_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "candidate_not_proof": True,
        "proof_status": "rank-zero-selmer-transcripts-missing-not-proof",
        "packages": [
            {
                "package_id": "rank-zero-selmer-AA-kernel-minus-p",
                "transcript_package_ready": False,
                "strict_promotion_ready": False,
                "proof_status": "no-transcript-package-not-proof",
                "missing_fields": [
                    "statement",
                    "isogeny_setup",
                    "local_squareclass_conditions",
                    "selmer_bound_argument",
                    "rank_zero_conclusion",
                    "review_notes",
                ],
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
                "transcript_package_ready": False,
                "strict_promotion_ready": False,
                "proof_status": "no-transcript-package-not-proof",
                "missing_fields": [
                    "statement",
                    "isogeny_setup",
                    "local_squareclass_conditions",
                    "selmer_bound_argument",
                    "rank_zero_conclusion",
                    "review_notes",
                ],
            },
        ],
        "unexpected_transcript_package_ids": [],
        "violations": [],
        "boundary": BOUNDARY,
    }


def test_transcript_intake_counts_ready_package_but_never_promotes(
    tmp_path: Path,
) -> None:
    _write_packages(tmp_path)
    transcript = tmp_path / "aa-minus-p-transcript.txt"
    transcript.write_text("reviewable Selmer transcript\n", encoding="utf-8")

    audit = audit_rank_zero_selmer_transcript_intake(
        materialization=_materialization(),
        transcript_index=_transcript_index(transcript),
        root=tmp_path,
    )

    assert audit["status"] == "ok"
    assert audit["transcript_package_ready_count"] == 1
    assert audit["missing_transcript_package_count"] == 1
    assert audit["strict_promotion_ready_count"] == 0
    assert audit["strict_promotion_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["candidate_not_proof"] is True
    assert audit["proof_status"] == "rank-zero-selmer-transcripts-partial-not-proof"
    assert audit["packages"][0]["proof_status"] == (
        "transcript-package-ready-needs-math-review"
    )
    assert audit["packages"][0]["missing_fields"] == []
    assert audit["violations"] == []


def test_transcript_intake_rejects_bad_transcript_package(tmp_path: Path) -> None:
    _write_packages(tmp_path)
    transcript_index = _transcript_index(tmp_path / "missing.txt")
    transcript_index["packages"][0]["field_status"] = {"statement": "present"}
    transcript_index["packages"].append(
        {
            "package_id": "rank-zero-selmer-unexpected",
            "transcript_path": "unexpected.txt",
            "transcript_type": REQUIRED_TRANSCRIPT_TYPE,
            "result": "uniform-isogeny-selmer-rank-bound",
            "field_status": {},
        }
    )

    audit = audit_rank_zero_selmer_transcript_intake(
        materialization=_materialization(),
        transcript_index=transcript_index,
        root=tmp_path,
    )

    assert audit["status"] == "issues"
    assert audit["transcript_package_ready_count"] == 0
    assert audit["unexpected_transcript_package_ids"] == [
        "rank-zero-selmer-unexpected"
    ]
    assert {
        "package_id": "rank-zero-selmer-AA-kernel-minus-p",
        "field": "transcript_path",
        "expected": "existing transcript file",
        "actual": str(tmp_path / "missing.txt"),
    } in audit["violations"]


def test_template_index_lists_expected_transcript_paths() -> None:
    index = template_index(_materialization())

    assert index["package_count"] == 2
    assert index["templates"][0] == {
        "package_id": "rank-zero-selmer-AA-kernel-minus-p",
        "transcript_index_entry": {
            "package_id": "rank-zero-selmer-AA-kernel-minus-p",
            "transcript_path": (
                "docs/external/rank_zero_selmer/"
                "rank-zero-selmer-AA-kernel-minus-p-transcript.txt"
            ),
            "transcript_type": REQUIRED_TRANSCRIPT_TYPE,
            "result": "uniform-isogeny-selmer-rank-bound",
            "field_status": {
                "statement": "missing",
                "isogeny_setup": "missing",
                "local_squareclass_conditions": "missing",
                "selmer_bound_argument": "missing",
                "rank_zero_conclusion": "missing",
                "review_notes": "missing",
            },
        },
    }


def test_transcript_intake_cli_writes_audit_and_template_index(
    tmp_path: Path,
) -> None:
    materialization = tmp_path / "materialization.json"
    out = tmp_path / "audit.json"
    templates = tmp_path / "templates.json"
    _write_packages(tmp_path)
    materialization.write_text(json.dumps(_materialization()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_transcript_intake.py",
            "--materialization",
            str(materialization),
            "--out",
            str(out),
            "--template-index-out",
            str(templates),
            "--root",
            str(tmp_path),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "transcript_package_ready_count=0" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["proof_status"] == (
        "rank-zero-selmer-transcripts-missing-not-proof"
    )
    assert json.loads(templates.read_text(encoding="utf-8"))["package_count"] == 2


def test_write_json_writes_sorted_transcript_intake(tmp_path: Path) -> None:
    out = tmp_path / "intake.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
