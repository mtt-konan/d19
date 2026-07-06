from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_partial_artifacts import (
    DEFAULT_REQUIRED_ARTIFACTS,
    Artifact,
    audit_artifacts,
    parse_required_artifact,
    write_json,
)


def test_audit_artifacts_marks_ready_when_required_files_exist(tmp_path: Path) -> None:
    required = [
        Artifact("script", "scripts/theory/example.py"),
        Artifact("test", "tests/test_example.py"),
        Artifact("result", "results/example.json"),
        Artifact("worklog", "docs/work-logs/999-example.md"),
    ]
    for artifact in required:
        path = tmp_path / artifact.path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("ok\n", encoding="utf-8")

    audit = audit_artifacts(root=tmp_path, required=required)

    assert audit == {
        "ready": True,
        "required_file_count": 4,
        "category_counts": {
            "result": 1,
            "script": 1,
            "test": 1,
            "worklog": 1,
        },
        "missing_files": [],
        "required_files": [
            {"category": "script", "path": "scripts/theory/example.py"},
            {"category": "test", "path": "tests/test_example.py"},
            {"category": "result", "path": "results/example.json"},
            {"category": "worklog", "path": "docs/work-logs/999-example.md"},
        ],
        "boundary": (
            "This checks artifact presence for the closure-quotient partial-result "
            "package. It does not check mathematical truth."
        ),
    }


def test_audit_artifacts_reports_missing_files(tmp_path: Path) -> None:
    required = [
        Artifact("script", "scripts/theory/present.py"),
        Artifact("result", "results/missing.json"),
    ]
    present = tmp_path / "scripts/theory/present.py"
    present.parent.mkdir(parents=True, exist_ok=True)
    present.write_text("ok\n", encoding="utf-8")

    audit = audit_artifacts(root=tmp_path, required=required)

    assert audit["ready"] is False
    assert audit["missing_files"] == [
        {"category": "result", "path": "results/missing.json"}
    ]


def test_default_artifact_manifest_includes_priority_handoff_audit() -> None:
    paths = {artifact.path for artifact in DEFAULT_REQUIRED_ARTIFACTS}

    assert "scripts/theory/audit_mixed_closure_priority_handoffs.py" in paths
    assert "scripts/theory/sage_verify_mixed_closure_handoff_maps.py" in paths
    assert "tests/test_mixed_closure_priority_handoff_audit.py" in paths
    assert "tests/test_sage_verify_mixed_closure_handoff_maps.py" in paths
    assert "docs/work-logs/313-priority-handoff-probe-audit.md" in paths
    assert "docs/work-logs/314-sage-cover-map-identity-verification.md" in paths
    assert "results/mixed_closure_priority_handoff_audit_top4.json" in paths
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_001_115_297_AA_covers_3_4_sage_probe.json"
    ) in paths
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_001_115_297_AA_covers_3_4_map_verify.json"
    ) in paths


def test_parse_required_artifact_requires_category_and_path() -> None:
    assert parse_required_artifact("script:scripts/theory/x.py") == Artifact(
        "script", "scripts/theory/x.py"
    )


def test_artifact_cli_strict_exits_nonzero_when_required_file_is_missing(
    tmp_path: Path,
) -> None:
    out = tmp_path / "audit.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_partial_artifacts.py",
            "--root",
            str(tmp_path),
            "--require",
            "script:scripts/theory/missing.py",
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
    assert "ready=False" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["missing_files"] == [
        {"category": "script", "path": "scripts/theory/missing.py"}
    ]


def test_write_json_writes_sorted_artifact_audit(tmp_path: Path) -> None:
    out = tmp_path / "audit.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
