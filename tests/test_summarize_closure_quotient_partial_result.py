from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.summarize_closure_quotient_partial_result import (
    summarize_partial_result,
    write_json,
)


def test_summarize_partial_result_marks_ready_when_gates_are_clean() -> None:
    claim_audit = {
        "mismatches": [],
        "claim_values": {
            "rank0_torsion_certificates": 275,
            "strict_excluded_pair_count": 220,
            "residual_evidence_candidate_cover_total": 27,
            "priority_top_a": 115,
            "priority_top_b": 297,
            "priority_top_cover_index": 3,
            "language_audit_violations": 0,
            "bsd_analytic_rank0_rows": 2,
        },
    }
    language_audit = {"violations": [], "files": 7}
    priority_summary = {
        "candidate_cover_total": 27,
        "top_targets": [{"A": 115, "B": 297, "curve": "AA", "cover_index": 3}],
    }
    artifact_audit = {"ready": True, "required_file_count": 65, "missing_files": []}

    summary = summarize_partial_result(
        claim_audit=claim_audit,
        language_audit=language_audit,
        priority_summary=priority_summary,
        artifact_audit=artifact_audit,
    )

    assert summary == {
        "ready_for_partial_result": True,
        "blocking_issues": [],
        "strict_certificate": {
            "rank0_torsion_certificates": 275,
            "strict_excluded_pair_count": 220,
        },
        "residual_status": {
            "candidate_cover_total": 27,
            "top_target": {"A": 115, "B": 297, "curve": "AA", "cover_index": 3},
            "bsd_analytic_rank0_rows": 2,
            "proof_status": "candidate-not-proof",
        },
        "language_status": {
            "files": 7,
            "violations": 0,
        },
        "artifact_status": {
            "ready": True,
            "required_file_count": 65,
            "missing_file_count": 0,
        },
        "boundary": (
            "Ready here means the stored partial-result evidence is internally "
            "consistent and wording boundaries are clean. It does not mean the "
            "residual 2-covers have been strictly proven pointless."
        ),
    }


def test_summarize_partial_result_reports_blocking_issues() -> None:
    summary = summarize_partial_result(
        claim_audit={"mismatches": [{"field": "x"}], "claim_values": {}},
        language_audit={"violations": [{"kind": "overclaim"}]},
        priority_summary={"top_targets": []},
        artifact_audit={
            "ready": False,
            "missing_files": [{"path": "results/missing.json"}],
        },
    )

    assert summary["ready_for_partial_result"] is False
    assert summary["blocking_issues"] == [
        "claim-audit-mismatches",
        "language-audit-violations",
        "missing-priority-top-target",
        "artifact-audit-missing-files",
    ]


def test_summary_cli_strict_exits_nonzero_when_not_ready(tmp_path: Path) -> None:
    claim = tmp_path / "claim.json"
    language = tmp_path / "language.json"
    priority = tmp_path / "priority.json"
    artifacts = tmp_path / "artifacts.json"
    out = tmp_path / "summary.json"
    claim.write_text('{"mismatches":[{"field":"x"}],"claim_values":{}}\n', encoding="utf-8")
    language.write_text('{"violations":[],"files":1}\n', encoding="utf-8")
    priority.write_text('{"top_targets":[]}\n', encoding="utf-8")
    artifacts.write_text('{"ready":true,"missing_files":[]}\n', encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/summarize_closure_quotient_partial_result.py",
            "--claim-audit",
            str(claim),
            "--language-audit",
            str(language),
            "--priority-summary",
            str(priority),
            "--artifact-audit",
            str(artifacts),
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
    assert "ready_for_partial_result=False" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["blocking_issues"] == [
        "claim-audit-mismatches",
        "missing-priority-top-target",
    ]


def test_write_json_writes_sorted_partial_summary(tmp_path: Path) -> None:
    out = tmp_path / "summary.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
