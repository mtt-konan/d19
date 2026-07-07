from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_mixed_closure_residual_open_frontier import (
    audit_residual_open_frontier,
    write_json,
)


def test_audit_residual_open_frontier_splits_conditional_and_open_covers() -> None:
    selmer_gap_ledger = {
        "candidate_cover_total": 4,
        "rows": [
            {
                "priority": 1,
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 3,
                "gap_type": "rank0-sha2-gap2",
            },
            {
                "priority": 2,
                "A": 1625,
                "B": 5643,
                "curve": "AA",
                "cover_index": 4,
                "gap_type": "rank0-sha2-gap2",
            },
            {
                "priority": 3,
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "cover_index": 5,
                "gap_type": "rank1-sha2-gap2-open",
            },
            {
                "priority": 4,
                "A": 1449,
                "B": 12155,
                "curve": "BB",
                "cover_index": 6,
                "gap_type": "even-rank-sha2-gap4-open",
            },
        ],
    }
    bsd_conditional_no_point_audit = {
        "rows": [
            {
                "priority": 1,
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 3,
                "conditional_no_point_status": "bsd-conditional-no-point",
            },
            {
                "priority": 2,
                "A": 1625,
                "B": 5643,
                "curve": "AA",
                "cover_index": 4,
                "conditional_no_point_status": "rank-zero-open",
            },
        ]
    }

    audit = audit_residual_open_frontier(
        selmer_gap_ledger=selmer_gap_ledger,
        bsd_conditional_no_point_audit=bsd_conditional_no_point_audit,
    )

    assert audit == {
        "status": "ok",
        "candidate_cover_total": 4,
        "conditional_no_point_cover_count": 1,
        "strict_no_point_cover_count": 0,
        "open_frontier_cover_count": 3,
        "frontier_type_counts": {
            "bsd-conditional-no-point": 1,
            "even-rank-gap4-needs-deeper-descent": 1,
            "rank-zero-needs-rank-proof": 1,
            "rank1-needs-visible-generator-or-descent": 1,
        },
        "open_frontier_type_counts": {
            "even-rank-gap4-needs-deeper-descent": 1,
            "rank-zero-needs-rank-proof": 1,
            "rank1-needs-visible-generator-or-descent": 1,
        },
        "rows": [
            {
                "priority": 1,
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 3,
                "gap_type": "rank0-sha2-gap2",
                "frontier_type": "bsd-conditional-no-point",
                "next_step": "conditional evidence only; do not count as strict proof",
                "candidate_not_proof": True,
            },
            {
                "priority": 2,
                "A": 1625,
                "B": 5643,
                "curve": "AA",
                "cover_index": 4,
                "gap_type": "rank0-sha2-gap2",
                "frontier_type": "rank-zero-needs-rank-proof",
                "next_step": "prove rank zero; torsion-preimage audit can then rule out points",
                "candidate_not_proof": True,
            },
            {
                "priority": 3,
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "cover_index": 5,
                "gap_type": "rank1-sha2-gap2-open",
                "frontier_type": "rank1-needs-visible-generator-or-descent",
                "next_step": "separate the rank-one part from the residual Sha[2] class",
                "candidate_not_proof": True,
            },
            {
                "priority": 4,
                "A": 1449,
                "B": 12155,
                "curve": "BB",
                "cover_index": 6,
                "gap_type": "even-rank-sha2-gap4-open",
                "frontier_type": "even-rank-gap4-needs-deeper-descent",
                "next_step": "run a deeper descent or independent Sha[2] obstruction",
                "candidate_not_proof": True,
            },
        ],
        "boundary": (
            "This is an open-frontier ledger. It sorts remaining residual covers "
            "by the next missing proof ingredient; it does not prove no-pointness."
        ),
    }


def test_residual_open_frontier_cli_writes_audit(tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.json"
    bsd = tmp_path / "bsd.json"
    out = tmp_path / "frontier.json"
    ledger.write_text(
        json.dumps(
            {
                "candidate_cover_total": 1,
                "rows": [
                    {
                        "priority": 1,
                        "A": 115,
                        "B": 297,
                        "curve": "AA",
                        "cover_index": 3,
                        "gap_type": "rank0-sha2-gap2",
                    }
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    bsd.write_text(
        json.dumps(
            {
                "rows": [
                    {
                        "A": 115,
                        "B": 297,
                        "curve": "AA",
                        "cover_index": 3,
                        "conditional_no_point_status": "bsd-conditional-no-point",
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
            "scripts/theory/audit_mixed_closure_residual_open_frontier.py",
            "--selmer-gap-ledger",
            str(ledger),
            "--bsd-conditional-no-point-audit",
            str(bsd),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "open_frontier_cover_count=0" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["candidate_cover_total"] == 1


def test_write_json_writes_sorted_residual_open_frontier_audit(tmp_path: Path) -> None:
    out = tmp_path / "frontier.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
