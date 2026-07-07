from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.export_external_cover_descent_packages import (
    BOUNDARY,
    REQUIRED_STRICT_EVIDENCE,
    export_packages,
    write_json,
)


def _frontier_handoff_audit() -> dict[str, object]:
    return {
        "status": "ok",
        "groups": [
            {
                "name": "priority_005_1625_5643_AA_covers_4_3",
                "target": {"A": 1625, "B": 5643, "curve": "AA"},
                "cover_indices": [4, 3],
            }
        ],
    }


def _handoff() -> dict[str, object]:
    return {
        "A": 1625,
        "B": 5643,
        "curve": "AA",
        "target_covers": [
            {
                "index": 4,
                "quartic": "2510769*x^4 - 4527908*x^3 + 3498741",
                "covering_map_to_elliptic": "[x/y^2, x^2/y^3]",
            },
            {
                "index": 3,
                "quartic": "444809*x^4 + 3153444*x^3 + 11120225",
                "covering_map_to_elliptic": "[x/y^2, x^2/y^3]",
            },
        ],
    }


def _write_handoff(handoff_dir: Path) -> None:
    handoff_dir.mkdir()
    (handoff_dir / "priority_005_1625_5643_AA_covers_4_3.json").write_text(
        json.dumps(_handoff()),
        encoding="utf-8",
    )


def test_export_packages_writes_external_task_files(tmp_path: Path) -> None:
    handoff_dir = tmp_path / "handoffs"
    out_dir = tmp_path / "packages"
    _write_handoff(handoff_dir)

    audit = export_packages(
        frontier_handoff_audit=_frontier_handoff_audit(),
        handoff_dir=handoff_dir,
        out_dir=out_dir,
    )

    package = audit["packages"][0]
    magma_path = Path(package["magma_task_path"])
    sage_path = Path(package["sage_task_path"])
    input_path = Path(package["input_path"])

    assert audit["status"] == "ok"
    assert audit["target_count"] == 1
    assert audit["cover_count"] == 2
    assert audit["strict_certificate_ready_count"] == 0
    assert audit["candidate_not_proof"] is True
    assert audit["boundary"] == BOUNDARY
    assert "HyperellipticCurve(f4)" in magma_path.read_text(encoding="utf-8")
    assert "2510769*x^4" in magma_path.read_text(encoding="utf-8")
    assert "HyperellipticCurve(f4)" in sage_path.read_text(encoding="utf-8")
    assert json.loads(input_path.read_text(encoding="utf-8")) == {
        "name": "priority_005_1625_5643_AA_covers_4_3",
        "target": {"A": 1625, "B": 5643, "curve": "AA"},
        "cover_indices": [4, 3],
        "target_covers": [
            {
                "index": 4,
                "quartic": "2510769*x^4 - 4527908*x^3 + 3498741",
                "covering_map_to_elliptic": "[x/y^2, x^2/y^3]",
            },
            {
                "index": 3,
                "quartic": "444809*x^4 + 3153444*x^3 + 11120225",
                "covering_map_to_elliptic": "[x/y^2, x^2/y^3]",
            },
        ],
        "required_strict_evidence": list(REQUIRED_STRICT_EVIDENCE),
        "candidate_not_proof": True,
        "boundary": BOUNDARY,
    }


def test_export_packages_reports_missing_handoff(tmp_path: Path) -> None:
    audit = export_packages(
        frontier_handoff_audit=_frontier_handoff_audit(),
        handoff_dir=tmp_path / "missing",
        out_dir=tmp_path / "packages",
    )

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert audit["target_count"] == 0
    assert audit["missing_handoff_files"] == [
        {
            "name": "priority_005_1625_5643_AA_covers_4_3",
            "path": str(
                tmp_path
                / "missing"
                / "priority_005_1625_5643_AA_covers_4_3.json"
            ),
        }
    ]


def test_export_packages_cli_writes_index(tmp_path: Path) -> None:
    frontier = tmp_path / "frontier.json"
    handoff_dir = tmp_path / "handoffs"
    out_dir = tmp_path / "packages"
    out = tmp_path / "index.json"
    _write_handoff(handoff_dir)
    frontier.write_text(json.dumps(_frontier_handoff_audit()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/export_external_cover_descent_packages.py",
            "--frontier-handoff-audit",
            str(frontier),
            "--handoff-dir",
            str(handoff_dir),
            "--out-dir",
            str(out_dir),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "target_count=1" in result.stdout
    index = json.loads(out.read_text(encoding="utf-8"))
    assert index["package_status"] == "external-task-inputs-ready-not-proof"


def test_write_json_writes_sorted_package_index(tmp_path: Path) -> None:
    out = tmp_path / "index.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
