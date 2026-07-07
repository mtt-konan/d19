from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_external_cover_certificate_intake import (
    BOUNDARY,
    REQUIRED_CERTIFICATE_TYPE,
    audit_certificate_intake,
    write_json,
)


def _handoff() -> dict[str, object]:
    return {
        "A": 1625,
        "B": 5643,
        "curve": "AA",
        "target_covers": [
            {"index": 4, "quartic": "2510769*x^4 + 3498741"},
            {"index": 3, "quartic": "444809*x^4 + 11120225"},
        ],
    }


def _certificate(transcript: str) -> dict[str, object]:
    return {
        "target": {"A": 1625, "B": 5643, "curve": "AA"},
        "source_tool": "magma",
        "transcript_path": transcript,
        "cover_certificates": [
            {
                "index": 4,
                "certificate_type": REQUIRED_CERTIFICATE_TYPE,
                "result": "no-rational-points",
                "command_label": "cover-4-descent",
            },
            {
                "index": 3,
                "certificate_type": REQUIRED_CERTIFICATE_TYPE,
                "result": "no-rational-points",
                "command_label": "cover-3-descent",
            },
        ],
    }


def test_certificate_intake_without_certificate_stays_open() -> None:
    audit = audit_certificate_intake(
        handoff=_handoff(),
        certificate=None,
        root=ROOT,
    )

    assert audit == {
        "status": "ok",
        "ready": True,
        "target": {"A": 1625, "B": 5643, "curve": "AA"},
        "cover_count": 2,
        "required_cover_indices": [4, 3],
        "certified_cover_indices": [],
        "missing_cover_indices": [4, 3],
        "unexpected_cover_indices": [],
        "certificate_package_ready": False,
        "strict_promotion_ready": False,
        "strict_promotion_count": 0,
        "candidate_not_proof": True,
        "proof_status": "no-external-certificate-package-not-proof",
        "violations": [],
        "boundary": BOUNDARY,
    }


def test_certificate_intake_accepts_complete_package_but_not_as_math_proof(
    tmp_path: Path,
) -> None:
    transcript = tmp_path / "magma-transcript.txt"
    transcript.write_text("external no-point transcript\n", encoding="utf-8")

    audit = audit_certificate_intake(
        handoff=_handoff(),
        certificate=_certificate(str(transcript)),
        root=ROOT,
    )

    assert audit["status"] == "ok"
    assert audit["certificate_package_ready"] is True
    assert audit["strict_promotion_ready"] is False
    assert audit["strict_promotion_count"] == 0
    assert audit["candidate_not_proof"] is True
    assert audit["proof_status"] == "certificate-package-ready-needs-math-review"
    assert audit["certified_cover_indices"] == [4, 3]
    assert audit["missing_cover_indices"] == []
    assert audit["violations"] == []


def test_certificate_intake_rejects_missing_cover_and_transcript() -> None:
    certificate = _certificate("missing-transcript.txt")
    certificate["cover_certificates"] = [
        {
            "index": 4,
            "certificate_type": REQUIRED_CERTIFICATE_TYPE,
            "result": "no-rational-points",
            "command_label": "cover-4-descent",
        }
    ]

    audit = audit_certificate_intake(
        handoff=_handoff(),
        certificate=certificate,
        root=ROOT,
    )

    assert audit["status"] == "issues"
    assert audit["certificate_package_ready"] is False
    assert audit["missing_cover_indices"] == [3]
    assert audit["strict_promotion_ready"] is False
    assert {
        "field": "transcript_path",
        "expected": "existing transcript file",
        "actual": "missing-transcript.txt",
    } in audit["violations"]


def test_certificate_intake_cli_writes_template_when_certificate_is_absent(
    tmp_path: Path,
) -> None:
    handoff = tmp_path / "handoff.json"
    out = tmp_path / "intake.json"
    template = tmp_path / "template.json"
    handoff.write_text(json.dumps(_handoff()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_external_cover_certificate_intake.py",
            "--handoff",
            str(handoff),
            "--out",
            str(out),
            "--template-out",
            str(template),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "certificate_package_ready=False" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["proof_status"] == (
        "no-external-certificate-package-not-proof"
    )
    template_payload = json.loads(template.read_text(encoding="utf-8"))
    assert template_payload["cover_certificates"][0]["index"] == 4
    assert template_payload["cover_certificates"][1]["index"] == 3


def test_write_json_writes_sorted_certificate_intake(tmp_path: Path) -> None:
    out = tmp_path / "intake.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
