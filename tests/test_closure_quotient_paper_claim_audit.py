from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_paper_claims import (
    audit_claims,
    write_json,
)


def test_audit_claims_collects_paper_level_numbers() -> None:
    rank_summary = {
        "rows": 1536,
        "rank0_torsion_certificates": 275,
        "certified_no_full_closed_square": 275,
        "certified_all_midpoint": 275,
        "strict_excluded_pair_count": 220,
        "uncertain_rank_rows": [{"curve": "AA"}, {"curve": "BB"}],
    }
    rank0_audit = {
        "rank0_aabb_rows": 275,
        "certified_rows": 275,
        "strict_no_full_closed_rows": 275,
        "only_midpoint_rows": 275,
        "classification_detail_rows": 275,
        "classification_detail_point_count": 550,
        "violations": [],
    }
    cover_summary = {
        "rows": 12,
        "covers_without_points_counts": {"2": 10, "3": 1, "4": 1},
        "selmer_gap_alignment_counts": {"match": 12},
        "evidence_level_counts": {"bounded-search-no-point-candidate": 12},
    }
    residual_evidence_audit = {
        "target_rows": 12,
        "candidate_cover_total": 27,
        "candidate_rows": 12,
        "bsd_conditional_rank0_rows": 2,
        "violations": [],
    }
    residual_local_witnesses = {
        "candidate_cover_total": 27,
        "bad_prime_check_total": 251,
        "unresolved_bad_prime_total": 0,
        "sage": {"all_bad_primes_witnessed": True},
    }
    priority_summary = {
        "candidate_cover_total": 27,
        "rows": [
            {
                "priority": 1,
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 3,
                "has_bsd_conditional_rank0": True,
            },
            {
                "priority": 2,
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 4,
                "has_bsd_conditional_rank0": True,
            },
            {
                "priority": 3,
                "A": 575,
                "B": 4641,
                "curve": "AA",
                "cover_index": 4,
                "has_bsd_conditional_rank0": True,
            },
            {
                "priority": 4,
                "A": 575,
                "B": 4641,
                "curve": "AA",
                "cover_index": 3,
                "has_bsd_conditional_rank0": True,
            },
        ],
    }
    language_audit = {
        "files": 7,
        "violations": [],
        "required_boundary_hits": {
            "candidate_not_proof": 2,
            "sha2_candidate": 5,
            "bounded_search_not_proof": 1,
            "bsd_not_strict_certificate": 1,
        },
    }
    identity_audit = {"all_verified": True}
    bsd_rows = [
        {"status": "ok", "analytic_rank": 0},
        {"status": "ok", "analytic_rank": 0},
        {"status": "timeout"},
        {"status": "pari-error"},
    ]

    audit = audit_claims(
        rank_summary=rank_summary,
        rank0_audit=rank0_audit,
        cover_summary=cover_summary,
        residual_evidence_audit=residual_evidence_audit,
        residual_local_witnesses=residual_local_witnesses,
        priority_summary=priority_summary,
        language_audit=language_audit,
        identity_audit=identity_audit,
        bsd_rows=bsd_rows,
        expected={
            "rank0_torsion_certificates": 275,
            "strict_excluded_pair_count": 220,
            "rank0_aabb_rows": 275,
            "classification_detail_rows": 275,
            "classification_detail_point_count": 550,
            "cover_rows": 12,
            "cover_selmer_matches": 12,
            "residual_evidence_target_rows": 12,
            "residual_evidence_candidate_cover_total": 27,
            "residual_evidence_violations": 0,
            "residual_local_witness_candidate_cover_total": 27,
            "residual_local_witness_bad_prime_check_total": 251,
            "residual_local_witness_unresolved_bad_prime_total": 0,
            "residual_local_witness_all_bad_primes_witnessed": 1,
            "priority_candidate_cover_total": 27,
            "priority_top_a": 115,
            "priority_top_b": 297,
            "priority_top_cover_index": 3,
            "priority_top4_bsd_rank0_rows": 4,
            "language_audit_violations": 0,
            "language_audit_files": 7,
            "language_candidate_not_proof_hits": 2,
            "language_sha2_candidate_hits": 5,
            "language_bounded_search_not_proof_hits": 1,
            "language_bsd_not_strict_certificate_hits": 1,
            "even_model_identities_verified": 1,
            "bsd_ok_rows": 2,
            "bsd_analytic_rank0_rows": 2,
        },
    )

    assert audit == {
        "claim_values": {
            "rank_summary_rows": 1536,
            "rank0_torsion_certificates": 275,
            "certified_no_full_closed_square": 275,
            "certified_all_midpoint": 275,
            "strict_excluded_pair_count": 220,
            "uncertain_rank_rows": 2,
            "rank0_aabb_rows": 275,
            "rank0_certified_rows": 275,
            "rank0_strict_no_full_closed_rows": 275,
            "rank0_only_midpoint_rows": 275,
            "classification_detail_rows": 275,
            "classification_detail_point_count": 550,
            "rank0_audit_violations": 0,
            "cover_rows": 12,
            "cover_selmer_matches": 12,
            "cover_bounded_candidates": 12,
            "residual_evidence_target_rows": 12,
            "residual_evidence_candidate_cover_total": 27,
            "residual_evidence_candidate_rows": 12,
            "residual_evidence_bsd_conditional_rank0_rows": 2,
            "residual_evidence_violations": 0,
            "residual_local_witness_candidate_cover_total": 27,
            "residual_local_witness_bad_prime_check_total": 251,
            "residual_local_witness_unresolved_bad_prime_total": 0,
            "residual_local_witness_all_bad_primes_witnessed": 1,
            "priority_candidate_cover_total": 27,
            "priority_top_a": 115,
            "priority_top_b": 297,
            "priority_top_cover_index": 3,
            "priority_top_curve_is_aa": 1,
            "priority_top4_bsd_rank0_rows": 4,
            "language_audit_violations": 0,
            "language_audit_files": 7,
            "language_candidate_not_proof_hits": 2,
            "language_sha2_candidate_hits": 5,
            "language_bounded_search_not_proof_hits": 1,
            "language_bsd_not_strict_certificate_hits": 1,
            "even_model_identities_verified": 1,
            "bsd_ok_rows": 2,
            "bsd_analytic_rank0_rows": 2,
        },
        "expected": {
            "rank0_torsion_certificates": 275,
            "strict_excluded_pair_count": 220,
            "rank0_aabb_rows": 275,
            "classification_detail_rows": 275,
            "classification_detail_point_count": 550,
            "cover_rows": 12,
            "cover_selmer_matches": 12,
            "residual_evidence_target_rows": 12,
            "residual_evidence_candidate_cover_total": 27,
            "residual_evidence_violations": 0,
            "residual_local_witness_candidate_cover_total": 27,
            "residual_local_witness_bad_prime_check_total": 251,
            "residual_local_witness_unresolved_bad_prime_total": 0,
            "residual_local_witness_all_bad_primes_witnessed": 1,
            "priority_candidate_cover_total": 27,
            "priority_top_a": 115,
            "priority_top_b": 297,
            "priority_top_cover_index": 3,
            "priority_top4_bsd_rank0_rows": 4,
            "language_audit_violations": 0,
            "language_audit_files": 7,
            "language_candidate_not_proof_hits": 2,
            "language_sha2_candidate_hits": 5,
            "language_bounded_search_not_proof_hits": 1,
            "language_bsd_not_strict_certificate_hits": 1,
            "even_model_identities_verified": 1,
            "bsd_ok_rows": 2,
            "bsd_analytic_rank0_rows": 2,
        },
        "mismatches": [],
        "boundary": (
            "This checks consistency of stored result files and paper-level "
            "claims. It does not create new mathematical certificates."
        ),
    }


def test_audit_claims_reports_expected_value_mismatch() -> None:
    audit = audit_claims(
        rank_summary={"rank0_torsion_certificates": 274},
        rank0_audit={},
        cover_summary={},
        residual_evidence_audit=None,
        residual_local_witnesses=None,
        priority_summary=None,
        language_audit=None,
        identity_audit={},
        bsd_rows=[],
        expected={"rank0_torsion_certificates": 275},
    )

    assert audit["mismatches"] == [
        {
            "field": "rank0_torsion_certificates",
            "expected": 275,
            "actual": 274,
        }
    ]


def test_audit_cli_strict_exits_nonzero_on_mismatch(tmp_path: Path) -> None:
    rank_summary = tmp_path / "summary.json"
    rank0_audit = tmp_path / "rank0.json"
    cover_summary = tmp_path / "cover.json"
    residual_local_witnesses = tmp_path / "local_witnesses.json"
    priorities = tmp_path / "priorities.json"
    language = tmp_path / "language.json"
    identity_audit = tmp_path / "identity.json"
    bsd = tmp_path / "bsd.jsonl"
    out = tmp_path / "audit.json"
    rank_summary.write_text('{"rank0_torsion_certificates": 274}\n', encoding="utf-8")
    rank0_audit.write_text("{}\n", encoding="utf-8")
    cover_summary.write_text("{}\n", encoding="utf-8")
    residual_local_witnesses.write_text("{}\n", encoding="utf-8")
    priorities.write_text("{}\n", encoding="utf-8")
    language.write_text("{}\n", encoding="utf-8")
    identity_audit.write_text("{}\n", encoding="utf-8")
    bsd.write_text("", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_paper_claims.py",
            "--rank-summary",
            str(rank_summary),
            "--rank0-audit",
            str(rank0_audit),
            "--cover-summary",
            str(cover_summary),
            "--residual-evidence-audit",
            str(cover_summary),
            "--residual-local-witnesses",
            str(residual_local_witnesses),
            "--priority-summary",
            str(priorities),
            "--language-audit",
            str(language),
            "--identity-audit",
            str(identity_audit),
            "--bsd",
            str(bsd),
            "--out",
            str(out),
            "--expect",
            "rank0_torsion_certificates=275",
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "mismatches=1" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["mismatches"][0]["actual"] == 274


def test_write_json_writes_sorted_claim_audit(tmp_path: Path) -> None:
    out = tmp_path / "claims.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
