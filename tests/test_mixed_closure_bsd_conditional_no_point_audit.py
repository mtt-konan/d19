from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_mixed_closure_bsd_conditional_no_points import (
    audit_bsd_conditional_no_points,
    write_json,
)


def test_audit_bsd_conditional_no_points_combines_rank0_and_torsion_preimage() -> None:
    selmer_gap_ledger = {
        "rows": [
            {
                "priority": 1,
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 3,
                "gap_type": "rank0-sha2-gap2",
                "has_bsd_conditional_rank0": True,
            },
            {
                "priority": 2,
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 4,
                "gap_type": "rank0-sha2-gap2",
                "has_bsd_conditional_rank0": False,
            },
            {
                "priority": 3,
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "cover_index": 5,
                "gap_type": "rank1-sha2-gap2-open",
                "has_bsd_conditional_rank0": True,
            },
        ]
    }
    torsion_preimage_audit = {
        "status": "ok",
        "all_no_torsion_preimages": True,
        "sage": {
            "covers": [
                {
                    "A": 115,
                    "B": 297,
                    "curve": "AA",
                    "cover_index": 3,
                    "no_torsion_preimage": True,
                },
                {
                    "A": 115,
                    "B": 297,
                    "curve": "AA",
                    "cover_index": 4,
                    "no_torsion_preimage": True,
                },
            ]
        },
    }

    audit = audit_bsd_conditional_no_points(
        selmer_gap_ledger=selmer_gap_ledger,
        torsion_preimage_audit=torsion_preimage_audit,
    )

    assert audit == {
        "status": "ok",
        "bsd_conditional_no_point_cover_count": 1,
        "rank0_sha2_gap2_cover_count": 2,
        "torsion_preimage_cover_count": 2,
        "strict_no_point_cover_count": 0,
        "candidate_not_proof": True,
        "rows": [
            {
                "priority": 1,
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 3,
                "gap_type": "rank0-sha2-gap2",
                "has_bsd_conditional_rank0": True,
                "no_torsion_preimage": True,
                "conditional_no_point_status": "bsd-conditional-no-point",
            },
            {
                "priority": 2,
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 4,
                "gap_type": "rank0-sha2-gap2",
                "has_bsd_conditional_rank0": False,
                "no_torsion_preimage": True,
                "conditional_no_point_status": "rank-zero-open",
            },
        ],
        "boundary": (
            "This combines BSD-conditional rank-zero diagnostics with a torsion "
            "preimage audit. It is conditional evidence, not a strict no-point proof."
        ),
    }


def test_bsd_conditional_no_point_cli_writes_audit(tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.json"
    torsion = tmp_path / "torsion.json"
    out = tmp_path / "audit.json"
    ledger.write_text(
        json.dumps(
            {
                "rows": [
                    {
                        "priority": 1,
                        "A": 115,
                        "B": 297,
                        "curve": "AA",
                        "cover_index": 3,
                        "gap_type": "rank0-sha2-gap2",
                        "has_bsd_conditional_rank0": True,
                    }
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )
    torsion.write_text(
        json.dumps(
            {
                "sage": {
                    "covers": [
                        {
                            "A": 115,
                            "B": 297,
                            "curve": "AA",
                            "cover_index": 3,
                            "no_torsion_preimage": True,
                        }
                    ]
                }
            }
        )
        + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_mixed_closure_bsd_conditional_no_points.py",
            "--selmer-gap-ledger",
            str(ledger),
            "--rank0-torsion-preimage-audit",
            str(torsion),
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
    assert "bsd_conditional_no_point_cover_count=1" in result.stdout
    assert (
        json.loads(out.read_text(encoding="utf-8"))[
            "bsd_conditional_no_point_cover_count"
        ]
        == 1
    )


def test_write_json_writes_sorted_bsd_conditional_no_point_audit(tmp_path: Path) -> None:
    out = tmp_path / "audit.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
