from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_partial_dependencies import (
    BOUNDARY,
    REQUIRED_DEPENDENCIES,
    audit_dependencies,
    write_json,
)


def _summary() -> dict[str, object]:
    return {
        "ready_for_partial_result": True,
        "strict_certificate": {"rank0_torsion_certificates": 275},
        "residual_status": {"candidate_cover_total": 27},
        "residual_open_frontier_status": {"open_frontier_cover_count": 23},
        "frontier_strictification_status": {"target_count": 10},
        "external_certificate_frontier_status": {"target_count": 10},
        "paper_structure_status": {"ready": True},
        "artifact_status": {"ready": True},
    }


def _artifact_audit(tmp_path: Path) -> dict[str, object]:
    required_files = [
        {"category": "result", "path": dependency["path"]}
        for dependency in REQUIRED_DEPENDENCIES
    ]
    for row in required_files:
        path = tmp_path / row["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n", encoding="utf-8")
    return {
        "ready": True,
        "required_files": required_files,
        "missing_files": [],
    }


def test_dependency_audit_accepts_complete_dependency_map(tmp_path: Path) -> None:
    artifact_audit = _artifact_audit(tmp_path)

    audit = audit_dependencies(
        summary=_summary(),
        artifact_audit=artifact_audit,
        root=tmp_path,
    )

    assert audit == {
        "status": "ok",
        "ready": True,
        "dependency_count": len(REQUIRED_DEPENDENCIES),
        "summary_status_count": 7,
        "missing_summary_statuses": [],
        "missing_files": [],
        "not_in_artifact_audit": [],
        "dependencies": REQUIRED_DEPENDENCIES,
        "boundary": BOUNDARY,
    }


def test_dependency_audit_reports_missing_summary_status_and_file(
    tmp_path: Path,
) -> None:
    artifact_audit = _artifact_audit(tmp_path)
    missing_path = tmp_path / REQUIRED_DEPENDENCIES[0]["path"]
    missing_path.unlink()

    audit = audit_dependencies(
        summary={"ready_for_partial_result": True},
        artifact_audit=artifact_audit,
        root=tmp_path,
    )

    assert audit["status"] == "issues"
    assert "strict_certificate" in audit["missing_summary_statuses"]
    assert audit["missing_files"] == [REQUIRED_DEPENDENCIES[0]]


def test_dependency_cli_strict_exits_nonzero_on_missing_dependency(
    tmp_path: Path,
) -> None:
    summary = tmp_path / "summary.json"
    artifacts = tmp_path / "artifacts.json"
    out = tmp_path / "deps.json"
    summary.write_text('{"ready_for_partial_result":true}\n', encoding="utf-8")
    artifacts.write_text(
        json.dumps({"ready": True, "required_files": [], "missing_files": []}) + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_partial_dependencies.py",
            "--summary",
            str(summary),
            "--artifact-audit",
            str(artifacts),
            "--root",
            str(tmp_path),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "status=issues" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["ready"] is False


def test_write_json_writes_sorted_dependency_audit(tmp_path: Path) -> None:
    out = tmp_path / "deps.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
