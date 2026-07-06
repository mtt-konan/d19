from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.summarize_mixed_closure_residual_selmer_gaps import (
    build_selmer_gap_ledger,
    write_json,
)


def test_build_selmer_gap_ledger_joins_priorities_to_sage_diagnostics() -> None:
    priorities = {
        "candidate_cover_total": 2,
        "rows": [
            {
                "priority": 1,
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 3,
                "selmer_gap": 2,
                "has_bsd_conditional_rank0": True,
                "proof_status": "candidate-not-proof",
            },
            {
                "priority": 2,
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "cover_index": 5,
                "selmer_gap": 2,
                "has_bsd_conditional_rank0": False,
                "proof_status": "candidate-not-proof",
            },
        ],
    }
    diagnostics = [
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "status": "ok",
            "rank_bounds": [0, 2],
            "selmer_rank_mwrank": 4,
            "torsion_two_dimension": 2,
            "root_number": 1,
            "conductor": 10548872720,
            "rank_plus_sha2_dimension": 2,
        },
        {
            "A": 209,
            "B": 5355,
            "curve": "BB",
            "status": "timeout",
        },
    ]

    ledger = build_selmer_gap_ledger(
        priorities=priorities,
        diagnostics=diagnostics,
    )

    assert ledger == {
        "candidate_cover_total": 2,
        "diagnostic_status_counts": {"ok": 1, "timeout": 1},
        "rows_with_ok_diagnostics": 1,
        "missing_diagnostic_rows": 0,
        "rank0_sha2_gap2_cover_total": 1,
        "gap_type_counts": {
            "diagnostic-open": 1,
            "rank0-sha2-gap2": 1,
        },
        "all_rows_candidate_not_proof": True,
        "rows": [
            {
                "priority": 1,
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 3,
                "priority_selmer_gap": 2,
                "diagnostic_status": "ok",
                "rank_bounds": [0, 2],
                "selmer_rank": 4,
                "torsion_two_dimension": 2,
                "rank_plus_sha2_dimension": 2,
                "root_number": 1,
                "conductor": 10548872720,
                "has_bsd_conditional_rank0": True,
                "proof_status": "candidate-not-proof",
                "gap_type": "rank0-sha2-gap2",
            },
            {
                "priority": 2,
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "cover_index": 5,
                "priority_selmer_gap": 2,
                "diagnostic_status": "timeout",
                "rank_bounds": [],
                "selmer_rank": 0,
                "torsion_two_dimension": 0,
                "rank_plus_sha2_dimension": 0,
                "root_number": 0,
                "conductor": 0,
                "has_bsd_conditional_rank0": False,
                "proof_status": "candidate-not-proof",
                "gap_type": "diagnostic-open",
            },
        ],
        "boundary": (
            "This ledger organizes residual Selmer/Sha[2] gaps. It does not "
            "prove that any residual cover has no rational point."
        ),
    }


def test_selmer_gap_ledger_cli_writes_json(tmp_path: Path) -> None:
    priorities = tmp_path / "priorities.json"
    diagnostics = tmp_path / "diagnostics.jsonl"
    out = tmp_path / "ledger.json"
    priorities.write_text(
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
                        "selmer_gap": 2,
                        "proof_status": "candidate-not-proof",
                    }
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    diagnostics.write_text(
        json.dumps(
            {
                "A": 115,
                "B": 297,
                "curve": "AA",
                "status": "ok",
                "rank_bounds": [0, 2],
                "selmer_rank_mwrank": 4,
                "torsion_two_dimension": 2,
                "rank_plus_sha2_dimension": 2,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/summarize_mixed_closure_residual_selmer_gaps.py",
            "--priorities",
            str(priorities),
            "--diagnostics",
            str(diagnostics),
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
    assert json.loads(out.read_text(encoding="utf-8"))["rank0_sha2_gap2_cover_total"] == 1


def test_write_json_writes_sorted_selmer_gap_ledger(tmp_path: Path) -> None:
    out = tmp_path / "ledger.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
