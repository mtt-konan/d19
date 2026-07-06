from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_mixed_closure_residual_evidence import (
    audit_residual_evidence,
    write_json,
)


def test_audit_residual_evidence_aligns_all_residual_sources() -> None:
    rank_summary = {
        "uncertain_rank_rows": [
            {
                "A": 115,
                "B": 297,
                "curve": "AA",
                "rank": "0/2",
                "model": [0, 196194, 0, -699602500, -137257812885000],
            },
            {
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "rank": "1/3",
                "model": [0, 88310146, 0, -3289257639202500, -290474822349588098565000],
            },
            {
                "A": 3,
                "B": 5,
                "curve": "AB",
                "rank": "1/3",
                "model": [0, 1, 0, -1, 0],
            },
        ]
    }
    diagnostic_rows = [
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "status": "ok",
            "selmer_rank_pari": 4,
            "selmer_rank_mwrank": 4,
            "torsion_two_dimension": 2,
            "rank_plus_sha2_dimension": 2,
        },
        {
            "A": 209,
            "B": 5355,
            "curve": "BB",
            "status": "ok",
            "selmer_rank_pari": 5,
            "selmer_rank_mwrank": 5,
            "torsion_two_dimension": 2,
            "rank_plus_sha2_dimension": 3,
        },
    ]
    cover_rows = [
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "status": "ok",
            "cover_count": 4,
            "covers_without_points": 2,
            "covers": [
                {"index": 1, "point_count": 6},
                {"index": 2, "point_count": 2},
                {"index": 3, "point_count": 0},
                {"index": 4, "point_count": 0},
            ],
        },
        {
            "A": 209,
            "B": 5355,
            "curve": "BB",
            "status": "ok",
            "cover_count": 5,
            "covers_without_points": 3,
            "covers": [
                {"index": 1, "point_count": 8},
                {"index": 2, "point_count": 2},
                {"index": 3, "point_count": 0},
                {"index": 4, "point_count": 0},
                {"index": 5, "point_count": 0},
            ],
        },
    ]
    bsd_rows = [
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "status": "ok",
            "analytic_rank": 0,
            "evidence_level": "bsd-conditional-diagnostic",
        },
        {
            "A": 209,
            "B": 5355,
            "curve": "BB",
            "status": "timeout",
            "evidence_level": "no-bsd-diagnostic",
        },
    ]

    audit = audit_residual_evidence(
        rank_summary=rank_summary,
        diagnostic_rows=diagnostic_rows,
        cover_rows=cover_rows,
        bsd_rows=bsd_rows,
        curves={"AA", "BB"},
    )

    assert audit == {
        "target_curves": ["AA", "BB"],
        "target_rows": 2,
        "diagnostic_rows": 2,
        "cover_rows": 2,
        "bsd_rows": 2,
        "diagnostic_status_counts": {"ok": 2},
        "cover_status_counts": {"ok": 2},
        "bsd_status_counts": {"ok": 1, "timeout": 1},
        "selmer_backend_alignment_counts": {"match": 2},
        "rank_plus_sha2_alignment_counts": {"match": 2},
        "cover_count_selmer_alignment_counts": {"match": 2},
        "no_point_selmer_gap_alignment_counts": {"match": 2},
        "candidate_cover_total": 5,
        "candidate_rows": 2,
        "bsd_conditional_rank0_rows": 1,
        "violations": [],
        "residual_rows": [
            {
                "A": 115,
                "B": 297,
                "curve": "AA",
                "input_rank": "0/2",
                "selmer_rank_pari": 4,
                "selmer_rank_mwrank": 4,
                "torsion_two_dimension": 2,
                "selmer_gap": 2,
                "cover_count": 4,
                "covers_without_points": 2,
                "no_point_cover_indices": [3, 4],
                "bsd_status": "ok",
                "bsd_analytic_rank": 0,
                "evidence_level": "explicit-sha2-candidate",
                "proof_status": "candidate-not-proof",
            },
            {
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "input_rank": "1/3",
                "selmer_rank_pari": 5,
                "selmer_rank_mwrank": 5,
                "torsion_two_dimension": 2,
                "selmer_gap": 3,
                "cover_count": 5,
                "covers_without_points": 3,
                "no_point_cover_indices": [3, 4, 5],
                "bsd_status": "timeout",
                "bsd_analytic_rank": None,
                "evidence_level": "explicit-sha2-candidate",
                "proof_status": "candidate-not-proof",
            },
        ],
        "boundary": (
            "This audit aligns stored residual evidence across rank summary, Sage "
            "Selmer diagnostics, PARI ell2cover probes, and BSD diagnostics. "
            "Every no-point cover remains a bounded-search Sha[2] candidate, not "
            "a proof that the cover has no rational point."
        ),
    }


def test_audit_residual_evidence_reports_alignment_violations() -> None:
    audit = audit_residual_evidence(
        rank_summary={
            "uncertain_rank_rows": [
                {"A": 115, "B": 297, "curve": "AA", "rank": "0/2", "model": []}
            ]
        },
        diagnostic_rows=[
            {
                "A": 115,
                "B": 297,
                "curve": "AA",
                "status": "ok",
                "selmer_rank_pari": 4,
                "selmer_rank_mwrank": 3,
                "torsion_two_dimension": 2,
                "rank_plus_sha2_dimension": 7,
            }
        ],
        cover_rows=[
            {
                "A": 115,
                "B": 297,
                "curve": "AA",
                "status": "ok",
                "cover_count": 4,
                "covers_without_points": 1,
                "covers": [{"index": 1, "point_count": 0}],
            }
        ],
        bsd_rows=[],
        curves={"AA", "BB"},
    )

    assert audit["violations"] == [
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "kind": "missing-bsd-row",
        },
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "kind": "selmer-backend-mismatch",
            "selmer_rank_pari": 4,
            "selmer_rank_mwrank": 3,
        },
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "kind": "rank-plus-sha2-mismatch",
            "expected": 2,
            "actual": 7,
        },
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "kind": "no-point-selmer-gap-mismatch",
            "expected": 2,
            "actual": 1,
        },
    ]


def test_audit_residual_evidence_cli_strict_exits_nonzero_on_violation(
    tmp_path: Path,
) -> None:
    rank_summary = tmp_path / "rank_summary.json"
    diagnostics = tmp_path / "diagnostics.jsonl"
    covers = tmp_path / "covers.jsonl"
    bsd = tmp_path / "bsd.jsonl"
    out = tmp_path / "audit.json"
    rank_summary.write_text(
        json.dumps(
            {
                "uncertain_rank_rows": [
                    {"A": 115, "B": 297, "curve": "AA", "rank": "0/2", "model": []}
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )
    diagnostics.write_text("", encoding="utf-8")
    covers.write_text("", encoding="utf-8")
    bsd.write_text("", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_mixed_closure_residual_evidence.py",
            "--rank-summary",
            str(rank_summary),
            "--diagnostics",
            str(diagnostics),
            "--covers",
            str(covers),
            "--bsd",
            str(bsd),
            "--out",
            str(out),
            "--curve",
            "AA",
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "violations=3" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["violations"][0]["kind"] == (
        "missing-diagnostic-row"
    )


def test_write_json_writes_sorted_residual_audit(tmp_path: Path) -> None:
    out = tmp_path / "audit.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
