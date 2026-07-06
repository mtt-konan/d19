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
    priority_handoff_audit = {
        "ready": True,
        "groups_checked": 2,
        "target_cover_count": 4,
        "map_verify_status_counts": {"ok": 2},
        "local_witness_status_counts": {"ok": 2},
        "violations": [],
    }
    residual_local_witnesses = {
        "status": "ok",
        "candidate_cover_total": 27,
        "bad_prime_check_total": 251,
        "unresolved_bad_prime_total": 0,
        "sage": {"all_bad_primes_witnessed": True},
    }
    selmer_gap_ledger = {
        "candidate_cover_total": 27,
        "rows_with_ok_diagnostics": 27,
        "missing_diagnostic_rows": 0,
        "rank0_sha2_gap2_cover_total": 20,
        "gap_type_counts": {"rank0-sha2-gap2": 20, "residual-gap-open": 7},
        "all_rows_candidate_not_proof": True,
    }
    residual_cover_map_verify = {
        "all_verified": True,
        "target_cover_count": 27,
        "verified_cover_count": 27,
        "failed_cover_count": 0,
    }
    artifact_audit = {"ready": True, "required_file_count": 98, "missing_files": []}

    summary = summarize_partial_result(
        claim_audit=claim_audit,
        language_audit=language_audit,
        priority_summary=priority_summary,
        priority_handoff_audit=priority_handoff_audit,
        residual_local_witnesses=residual_local_witnesses,
        selmer_gap_ledger=selmer_gap_ledger,
        residual_cover_map_verify=residual_cover_map_verify,
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
        "priority_handoff_status": {
            "ready": True,
            "groups_checked": 2,
            "target_cover_count": 4,
            "map_verified_groups": 2,
            "local_witnessed_groups": 2,
            "violations": 0,
        },
        "residual_local_witness_status": {
            "ready": True,
            "candidate_cover_total": 27,
            "bad_prime_check_total": 251,
            "unresolved_bad_prime_total": 0,
        },
        "residual_selmer_gap_status": {
            "ready": True,
            "candidate_cover_total": 27,
            "rows_with_ok_diagnostics": 27,
            "missing_diagnostic_rows": 0,
            "rank0_sha2_gap2_cover_total": 20,
            "gap_type_counts": {
                "rank0-sha2-gap2": 20,
                "residual-gap-open": 7,
            },
        },
        "residual_cover_map_status": {
            "ready": True,
            "target_cover_count": 27,
            "verified_cover_count": 27,
            "failed_cover_count": 0,
        },
        "artifact_status": {
            "ready": True,
            "required_file_count": 98,
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
        priority_handoff_audit={
            "ready": False,
            "violations": [{"field": "probe.status"}],
        },
        residual_local_witnesses={
            "status": "ok",
            "unresolved_bad_prime_total": 1,
            "sage": {"all_bad_primes_witnessed": False},
        },
        selmer_gap_ledger={
            "candidate_cover_total": 27,
            "missing_diagnostic_rows": 1,
            "all_rows_candidate_not_proof": True,
        },
        residual_cover_map_verify={
            "all_verified": False,
            "target_cover_count": 27,
            "verified_cover_count": 26,
            "failed_cover_count": 1,
        },
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
        "priority-handoff-audit-issues",
        "residual-local-witness-issues",
        "residual-selmer-gap-ledger-issues",
        "residual-cover-map-verify-issues",
        "artifact-audit-missing-files",
    ]


def test_summary_cli_strict_exits_nonzero_when_not_ready(tmp_path: Path) -> None:
    claim = tmp_path / "claim.json"
    language = tmp_path / "language.json"
    priority = tmp_path / "priority.json"
    handoffs = tmp_path / "handoffs.json"
    local_witnesses = tmp_path / "local.json"
    selmer_gaps = tmp_path / "selmer_gaps.json"
    cover_maps = tmp_path / "cover_maps.json"
    artifacts = tmp_path / "artifacts.json"
    out = tmp_path / "summary.json"
    claim.write_text('{"mismatches":[{"field":"x"}],"claim_values":{}}\n', encoding="utf-8")
    language.write_text('{"violations":[],"files":1}\n', encoding="utf-8")
    priority.write_text('{"top_targets":[]}\n', encoding="utf-8")
    handoffs.write_text('{"ready":true,"violations":[]}\n', encoding="utf-8")
    local_witnesses.write_text(
        '{"status":"ok","unresolved_bad_prime_total":0,'
        '"sage":{"all_bad_primes_witnessed":true}}\n',
        encoding="utf-8",
    )
    selmer_gaps.write_text(
        '{"candidate_cover_total":0,"missing_diagnostic_rows":0,'
        '"all_rows_candidate_not_proof":true}\n',
        encoding="utf-8",
    )
    cover_maps.write_text(
        '{"all_verified":true,"target_cover_count":0,'
        '"verified_cover_count":0,"failed_cover_count":0}\n',
        encoding="utf-8",
    )
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
            "--priority-handoff-audit",
            str(handoffs),
            "--residual-local-witnesses",
            str(local_witnesses),
            "--selmer-gap-ledger",
            str(selmer_gaps),
            "--residual-cover-map-verify",
            str(cover_maps),
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
