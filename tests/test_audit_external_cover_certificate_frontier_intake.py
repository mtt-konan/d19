from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_external_cover_certificate_frontier_intake import (
    BOUNDARY,
    audit_frontier_certificate_intake,
    template_index,
    write_json,
)


def _frontier_handoff_audit() -> dict[str, object]:
    return {
        "status": "ok",
        "groups": [
            {
                "name": "priority_005_1625_5643_AA_covers_4_3",
                "target": {"A": 1625, "B": 5643, "curve": "AA"},
                "cover_indices": [3, 4],
            },
            {
                "name": "priority_008_209_5355_BB_covers_5_4_3",
                "target": {"A": 209, "B": 5355, "curve": "BB"},
                "cover_indices": [3, 4, 5],
            },
        ],
    }


def _handoff(target: dict[str, object], cover_indices: list[int]) -> dict[str, object]:
    return {
        "A": target["A"],
        "B": target["B"],
        "curve": target["curve"],
        "target_covers": [
            {"index": index, "quartic": f"{index}*x^4 + 1"}
            for index in cover_indices
        ],
    }


def _write_handoffs(handoff_dir: Path) -> None:
    handoff_dir.mkdir(parents=True)
    for group in _frontier_handoff_audit()["groups"]:
        (handoff_dir / f"{group['name']}.json").write_text(
            json.dumps(_handoff(group["target"], group["cover_indices"])),
            encoding="utf-8",
        )


def test_frontier_certificate_intake_marks_all_groups_open_without_certificates(
    tmp_path: Path,
) -> None:
    handoff_dir = tmp_path / "handoffs"
    certificate_dir = tmp_path / "certificates"
    _write_handoffs(handoff_dir)

    audit = audit_frontier_certificate_intake(
        frontier_handoff_audit=_frontier_handoff_audit(),
        handoff_dir=handoff_dir,
        certificate_dir=certificate_dir,
        root=tmp_path,
    )

    assert audit == {
        "status": "ok",
        "ready": True,
        "target_count": 2,
        "cover_count": 5,
        "certificate_package_ready_count": 0,
        "missing_certificate_package_count": 2,
        "strict_promotion_ready_count": 0,
        "strict_promotion_count": 0,
        "candidate_not_proof": True,
        "missing_handoff_files": [],
        "violations": [],
        "proof_status": "frontier-external-certificates-missing-not-proof",
        "groups": [
            {
                "name": "priority_005_1625_5643_AA_covers_4_3",
                "target": {"A": 1625, "B": 5643, "curve": "AA"},
                "cover_count": 2,
                "certificate_package_ready": False,
                "strict_promotion_ready": False,
                "proof_status": "no-external-certificate-package-not-proof",
            },
            {
                "name": "priority_008_209_5355_BB_covers_5_4_3",
                "target": {"A": 209, "B": 5355, "curve": "BB"},
                "cover_count": 3,
                "certificate_package_ready": False,
                "strict_promotion_ready": False,
                "proof_status": "no-external-certificate-package-not-proof",
            },
        ],
        "boundary": BOUNDARY,
    }


def test_frontier_certificate_intake_counts_ready_package_but_no_promotion(
    tmp_path: Path,
) -> None:
    handoff_dir = tmp_path / "handoffs"
    certificate_dir = tmp_path / "certificates"
    transcript = tmp_path / "transcript.txt"
    _write_handoffs(handoff_dir)
    certificate_dir.mkdir()
    transcript.write_text("external certificate transcript\n", encoding="utf-8")
    (certificate_dir / "priority_005_1625_5643_AA_covers_4_3_certificate.json").write_text(
        json.dumps(
            {
                "target": {"A": 1625, "B": 5643, "curve": "AA"},
                "source_tool": "magma",
                "transcript_path": str(transcript),
                "cover_certificates": [
                    {
                        "index": 4,
                        "certificate_type": "cover-no-rational-point-certificate",
                        "result": "no-rational-points",
                        "command_label": "cover-4",
                    },
                    {
                        "index": 3,
                        "certificate_type": "cover-no-rational-point-certificate",
                        "result": "no-rational-points",
                        "command_label": "cover-3",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    audit = audit_frontier_certificate_intake(
        frontier_handoff_audit=_frontier_handoff_audit(),
        handoff_dir=handoff_dir,
        certificate_dir=certificate_dir,
        root=tmp_path,
    )

    assert audit["status"] == "ok"
    assert audit["certificate_package_ready_count"] == 1
    assert audit["missing_certificate_package_count"] == 1
    assert audit["strict_promotion_ready_count"] == 0
    assert audit["strict_promotion_count"] == 0
    assert audit["candidate_not_proof"] is True
    assert audit["proof_status"] == "frontier-external-certificates-partial-not-proof"


def test_template_index_lists_certificate_paths() -> None:
    index = template_index(_frontier_handoff_audit())

    assert index["target_count"] == 2
    assert index["cover_count"] == 5
    assert index["templates"][0] == {
        "name": "priority_005_1625_5643_AA_covers_4_3",
        "certificate_path": (
            "external_certificates/"
            "priority_005_1625_5643_AA_covers_4_3_certificate.json"
        ),
        "cover_indices": [3, 4],
    }


def test_frontier_certificate_intake_cli_writes_template_index(
    tmp_path: Path,
) -> None:
    handoff_dir = tmp_path / "handoffs"
    frontier = tmp_path / "frontier.json"
    out = tmp_path / "audit.json"
    templates = tmp_path / "templates.json"
    _write_handoffs(handoff_dir)
    frontier.write_text(json.dumps(_frontier_handoff_audit()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_external_cover_certificate_frontier_intake.py",
            "--frontier-handoff-audit",
            str(frontier),
            "--handoff-dir",
            str(handoff_dir),
            "--certificate-dir",
            str(tmp_path / "certificates"),
            "--out",
            str(out),
            "--template-index-out",
            str(templates),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "target_count=2" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["cover_count"] == 5
    assert json.loads(templates.read_text(encoding="utf-8"))["target_count"] == 2


def test_write_json_writes_sorted_frontier_intake(tmp_path: Path) -> None:
    out = tmp_path / "frontier.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
