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
        "violations": [],
    }
    cover_summary = {
        "rows": 12,
        "covers_without_points_counts": {"2": 10, "3": 1, "4": 1},
        "selmer_gap_alignment_counts": {"match": 12},
        "evidence_level_counts": {"bounded-search-no-point-candidate": 12},
    }
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
        bsd_rows=bsd_rows,
        expected={
            "rank0_torsion_certificates": 275,
            "strict_excluded_pair_count": 220,
            "rank0_aabb_rows": 275,
            "cover_rows": 12,
            "cover_selmer_matches": 12,
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
            "rank0_audit_violations": 0,
            "cover_rows": 12,
            "cover_selmer_matches": 12,
            "cover_bounded_candidates": 12,
            "bsd_ok_rows": 2,
            "bsd_analytic_rank0_rows": 2,
        },
        "expected": {
            "rank0_torsion_certificates": 275,
            "strict_excluded_pair_count": 220,
            "rank0_aabb_rows": 275,
            "cover_rows": 12,
            "cover_selmer_matches": 12,
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
    bsd = tmp_path / "bsd.jsonl"
    out = tmp_path / "audit.json"
    rank_summary.write_text('{"rank0_torsion_certificates": 274}\n', encoding="utf-8")
    rank0_audit.write_text("{}\n", encoding="utf-8")
    cover_summary.write_text("{}\n", encoding="utf-8")
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
