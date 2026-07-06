from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.prioritize_mixed_closure_residual_covers import (
    prioritize_residual_covers,
    quartic_complexity,
    write_json,
)


def test_quartic_complexity_extracts_degree_terms_and_height() -> None:
    assert quartic_complexity("41*x^4 + 10812*x^3 - 54060*x + 1025") == {
        "degree": 4,
        "term_count": 4,
        "coefficient_height": 54060,
    }


def test_prioritize_residual_covers_prefers_bsd_rank0_then_smaller_height() -> None:
    cover_summary = {
        "no_point_cover_rows": [
            {
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "selmer_gap": 3,
                "no_point_covers": [
                    {"index": 3, "quartic": "1000*x^4 + 7"},
                    {"index": 4, "quartic": "9*x^4 + 8*x + 1"},
                ],
            },
            {
                "A": 115,
                "B": 297,
                "curve": "AA",
                "selmer_gap": 2,
                "no_point_covers": [
                    {"index": 3, "quartic": "41*x^4 + 10812*x^3 - 54060*x + 1025"},
                    {"index": 4, "quartic": "-19*x^4 + 1848*x^3 - 6281875"},
                ],
            },
        ]
    }
    evidence_audit = {
        "residual_rows": [
            {
                "A": 115,
                "B": 297,
                "curve": "AA",
                "bsd_status": "ok",
                "bsd_analytic_rank": 0,
                "proof_status": "candidate-not-proof",
            },
            {
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "bsd_status": "timeout",
                "bsd_analytic_rank": None,
                "proof_status": "candidate-not-proof",
            },
        ]
    }

    result = prioritize_residual_covers(
        cover_summary=cover_summary,
        evidence_audit=evidence_audit,
    )

    assert result == {
        "candidate_cover_total": 4,
        "rows": [
            {
                "priority": 1,
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 3,
                "quartic": "41*x^4 + 10812*x^3 - 54060*x + 1025",
                "degree": 4,
                "term_count": 4,
                "coefficient_height": 54060,
                "selmer_gap": 2,
                "bsd_status": "ok",
                "bsd_analytic_rank": 0,
                "has_bsd_conditional_rank0": True,
                "proof_status": "candidate-not-proof",
            },
            {
                "priority": 2,
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 4,
                "quartic": "-19*x^4 + 1848*x^3 - 6281875",
                "degree": 4,
                "term_count": 3,
                "coefficient_height": 6281875,
                "selmer_gap": 2,
                "bsd_status": "ok",
                "bsd_analytic_rank": 0,
                "has_bsd_conditional_rank0": True,
                "proof_status": "candidate-not-proof",
            },
            {
                "priority": 3,
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "cover_index": 4,
                "quartic": "9*x^4 + 8*x + 1",
                "degree": 4,
                "term_count": 3,
                "coefficient_height": 9,
                "selmer_gap": 3,
                "bsd_status": "timeout",
                "bsd_analytic_rank": None,
                "has_bsd_conditional_rank0": False,
                "proof_status": "candidate-not-proof",
            },
            {
                "priority": 4,
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "cover_index": 3,
                "quartic": "1000*x^4 + 7",
                "degree": 4,
                "term_count": 2,
                "coefficient_height": 1000,
                "selmer_gap": 3,
                "bsd_status": "timeout",
                "bsd_analytic_rank": None,
                "has_bsd_conditional_rank0": False,
                "proof_status": "candidate-not-proof",
            },
        ],
        "top_targets": [
            {"A": 115, "B": 297, "curve": "AA", "cover_index": 3},
            {"A": 115, "B": 297, "curve": "AA", "cover_index": 4},
            {"A": 209, "B": 5355, "curve": "BB", "cover_index": 4},
            {"A": 209, "B": 5355, "curve": "BB", "cover_index": 3},
        ],
        "boundary": (
            "This is a prioritization table for explicit Sha[2] candidates. "
            "It ranks follow-up targets; it does not prove that any cover has "
            "no rational point."
        ),
    }


def test_prioritize_cli_writes_sorted_json(tmp_path: Path) -> None:
    cover_summary = tmp_path / "cover_summary.json"
    evidence = tmp_path / "evidence.json"
    out = tmp_path / "priorities.json"
    cover_summary.write_text(
        json.dumps(
            {
                "no_point_cover_rows": [
                    {
                        "A": 1,
                        "B": 2,
                        "curve": "AA",
                        "selmer_gap": 1,
                        "no_point_covers": [{"index": 3, "quartic": "5*x^4 + 1"}],
                    }
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )
    evidence.write_text(
        json.dumps(
            {
                "residual_rows": [
                    {
                        "A": 1,
                        "B": 2,
                        "curve": "AA",
                        "bsd_status": "ok",
                        "bsd_analytic_rank": 0,
                        "proof_status": "candidate-not-proof",
                    }
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/prioritize_mixed_closure_residual_covers.py",
            "--cover-summary",
            str(cover_summary),
            "--evidence-audit",
            str(evidence),
            "--out",
            str(out),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "candidate_cover_total=1" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["rows"][0]["priority"] == 1


def test_write_json_writes_sorted_priorities(tmp_path: Path) -> None:
    out = tmp_path / "priorities.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
