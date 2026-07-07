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
        "gap_type_counts": {
            "even-rank-sha2-gap4-open": 4,
            "rank0-sha2-gap2": 20,
            "rank1-sha2-gap2-open": 3,
        },
        "all_rows_candidate_not_proof": True,
    }
    residual_cover_map_verify = {
        "all_verified": True,
        "target_cover_count": 27,
        "verified_cover_count": 27,
        "failed_cover_count": 0,
    }
    rank0_torsion_preimage_audit = {
        "status": "ok",
        "gap_type": "rank0-sha2-gap2",
        "target_cover_count": 20,
        "all_no_torsion_preimages": True,
        "no_torsion_preimage_count": 20,
        "failed_cover_count": 0,
    }
    bsd_conditional_no_point_audit = {
        "status": "ok",
        "bsd_conditional_no_point_cover_count": 4,
        "rank0_sha2_gap2_cover_count": 20,
        "strict_no_point_cover_count": 0,
        "candidate_not_proof": True,
    }
    residual_open_frontier_audit = {
        "status": "ok",
        "candidate_cover_total": 27,
        "conditional_no_point_cover_count": 4,
        "strict_no_point_cover_count": 0,
        "open_frontier_cover_count": 23,
        "open_frontier_type_counts": {
            "even-rank-gap4-needs-deeper-descent": 4,
            "rank-zero-needs-rank-proof": 16,
            "rank1-needs-visible-generator-or-descent": 3,
        },
    }
    rank_zero_frontier_queue = {
        "status": "ok",
        "rank_zero_frontier_cover_count": 16,
        "rank_zero_frontier_target_count": 8,
        "closed_rank_zero_target_count": 0,
        "target_status_counts": {"not-retried": 7, "sage-timeout": 1},
    }
    non_rankzero_frontier_queue = {
        "status": "ok",
        "non_rankzero_frontier_cover_count": 7,
        "non_rankzero_frontier_target_count": 2,
        "target_type_counts": {
            "even-rank-gap4-needs-deeper-descent": 1,
            "rank1-needs-visible-generator-or-descent": 1,
        },
        "target_status_counts": {"even-gap4-open": 1, "sage-timeout": 1},
    }
    artifact_audit = {"ready": True, "required_file_count": 122, "missing_files": []}

    summary = summarize_partial_result(
        claim_audit=claim_audit,
        language_audit=language_audit,
        priority_summary=priority_summary,
        priority_handoff_audit=priority_handoff_audit,
        residual_local_witnesses=residual_local_witnesses,
        selmer_gap_ledger=selmer_gap_ledger,
        residual_cover_map_verify=residual_cover_map_verify,
        rank0_torsion_preimage_audit=rank0_torsion_preimage_audit,
        bsd_conditional_no_point_audit=bsd_conditional_no_point_audit,
        residual_open_frontier_audit=residual_open_frontier_audit,
        rank_zero_frontier_queue=rank_zero_frontier_queue,
        non_rankzero_frontier_queue=non_rankzero_frontier_queue,
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
                "even-rank-sha2-gap4-open": 4,
                "rank0-sha2-gap2": 20,
                "rank1-sha2-gap2-open": 3,
            },
        },
        "residual_cover_map_status": {
            "ready": True,
            "target_cover_count": 27,
            "verified_cover_count": 27,
            "failed_cover_count": 0,
        },
        "rank0_torsion_preimage_status": {
            "ready": True,
            "target_cover_count": 20,
            "no_torsion_preimage_count": 20,
            "failed_cover_count": 0,
            "conditional_on_rank_zero": True,
        },
        "bsd_conditional_no_point_status": {
            "ready": True,
            "bsd_conditional_no_point_cover_count": 4,
            "rank0_sha2_gap2_cover_count": 20,
            "strict_no_point_cover_count": 0,
            "candidate_not_proof": True,
            "proof_status": "conditional-not-proof",
        },
        "residual_open_frontier_status": {
            "ready": True,
            "candidate_cover_total": 27,
            "conditional_no_point_cover_count": 4,
            "strict_no_point_cover_count": 0,
            "open_frontier_cover_count": 23,
            "open_frontier_type_counts": {
                "even-rank-gap4-needs-deeper-descent": 4,
                "rank-zero-needs-rank-proof": 16,
                "rank1-needs-visible-generator-or-descent": 3,
            },
            "proof_status": "open-frontier-not-proof",
        },
        "rank_zero_frontier_status": {
            "ready": True,
            "rank_zero_frontier_cover_count": 16,
            "rank_zero_frontier_target_count": 8,
            "closed_rank_zero_target_count": 0,
            "target_status_counts": {"not-retried": 7, "sage-timeout": 1},
            "proof_status": "rank-proof-frontier-not-proof",
        },
        "non_rankzero_frontier_status": {
            "ready": True,
            "non_rankzero_frontier_cover_count": 7,
            "non_rankzero_frontier_target_count": 2,
            "target_type_counts": {
                "even-rank-gap4-needs-deeper-descent": 1,
                "rank1-needs-visible-generator-or-descent": 1,
            },
            "target_status_counts": {"even-gap4-open": 1, "sage-timeout": 1},
            "proof_status": "non-rankzero-frontier-not-proof",
        },
        "artifact_status": {
            "ready": True,
            "required_file_count": 122,
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
        rank0_torsion_preimage_audit={
            "status": "sage-error",
            "target_cover_count": 20,
            "all_no_torsion_preimages": False,
            "failed_cover_count": 1,
        },
        bsd_conditional_no_point_audit={
            "status": "error",
            "rank0_sha2_gap2_cover_count": 19,
            "strict_no_point_cover_count": 1,
            "candidate_not_proof": False,
        },
        residual_open_frontier_audit={
            "status": "error",
            "candidate_cover_total": 26,
            "conditional_no_point_cover_count": 4,
            "strict_no_point_cover_count": 1,
        },
        rank_zero_frontier_queue={
            "status": "error",
            "rank_zero_frontier_cover_count": 15,
            "closed_rank_zero_target_count": 1,
        },
        non_rankzero_frontier_queue={
            "status": "error",
            "non_rankzero_frontier_cover_count": 6,
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
        "rank0-torsion-preimage-audit-issues",
        "bsd-conditional-no-point-audit-issues",
        "residual-open-frontier-audit-issues",
        "rank-zero-frontier-queue-issues",
        "non-rankzero-frontier-queue-issues",
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
    torsion_preimages = tmp_path / "torsion_preimages.json"
    bsd_no_points = tmp_path / "bsd_no_points.json"
    open_frontier = tmp_path / "open_frontier.json"
    rank_zero_frontier = tmp_path / "rank_zero_frontier.json"
    non_rankzero_frontier = tmp_path / "non_rankzero_frontier.json"
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
    torsion_preimages.write_text(
        '{"status":"ok","target_cover_count":0,'
        '"all_no_torsion_preimages":true,"failed_cover_count":0}\n',
        encoding="utf-8",
    )
    bsd_no_points.write_text(
        '{"status":"ok","rank0_sha2_gap2_cover_count":0,'
        '"strict_no_point_cover_count":0,"candidate_not_proof":true}\n',
        encoding="utf-8",
    )
    open_frontier.write_text(
        '{"status":"ok","candidate_cover_total":0,'
        '"conditional_no_point_cover_count":0,'
        '"strict_no_point_cover_count":0}\n',
        encoding="utf-8",
    )
    rank_zero_frontier.write_text(
        '{"status":"ok","rank_zero_frontier_cover_count":0,'
        '"closed_rank_zero_target_count":0}\n',
        encoding="utf-8",
    )
    non_rankzero_frontier.write_text(
        '{"status":"ok","non_rankzero_frontier_cover_count":0}\n',
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
            "--rank0-torsion-preimage-audit",
            str(torsion_preimages),
            "--bsd-conditional-no-point-audit",
            str(bsd_no_points),
            "--residual-open-frontier-audit",
            str(open_frontier),
            "--rank-zero-frontier-queue",
            str(rank_zero_frontier),
            "--non-rankzero-frontier-queue",
            str(non_rankzero_frontier),
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
