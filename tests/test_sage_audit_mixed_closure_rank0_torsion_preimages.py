from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.sage_audit_mixed_closure_rank0_torsion_preimages import (
    MARKER,
    audit_rank0_torsion_preimages,
    build_rank0_torsion_targets,
    write_json,
)


def test_build_rank0_torsion_targets_selects_gap_type_covers() -> None:
    cover_rows = [
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "model": [0, 196194, 0, -699602500, -137257812885000],
            "covers": [
                {"index": 3, "quartic": "x^4+3", "covering_map_to_elliptic": "[x,y]"},
                {"index": 4, "quartic": "x^4+4", "covering_map_to_elliptic": "[x,y]"},
            ],
        }
    ]
    ledger = {
        "rows": [
            {
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 3,
                "gap_type": "rank0-sha2-gap2",
            },
            {
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 4,
                "gap_type": "rank1-sha2-gap2-open",
            },
        ]
    }

    targets = build_rank0_torsion_targets(
        cover_rows=cover_rows,
        selmer_gap_ledger=ledger,
        gap_type="rank0-sha2-gap2",
    )

    assert targets == [
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "weierstrass_model": [0, 196194, 0, -699602500, -137257812885000],
            "cover_index": 3,
            "quartic": "x^4+3",
            "covering_map_to_elliptic": "[x,y]",
            "gap_type": "rank0-sha2-gap2",
        }
    ]


def test_audit_rank0_torsion_preimages_parses_sage_marker(tmp_path: Path) -> None:
    cover_rows = [
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "model": [0, 196194, 0, -699602500, -137257812885000],
            "covers": [
                {"index": 3, "quartic": "x^4+3", "covering_map_to_elliptic": "[x,y]"},
            ],
        }
    ]
    ledger = {
        "rows": [
            {
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 3,
                "gap_type": "rank0-sha2-gap2",
            }
        ]
    }
    marker_payload = {
        "all_no_torsion_preimages": True,
        "target_cover_count": 1,
        "no_torsion_preimage_count": 1,
        "failed_cover_count": 0,
        "covers": [
            {
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 3,
                "status": "ok",
                "has_rational_infinity": False,
                "rational_branch_point_count": 0,
                "torsion_preimage_count": 0,
            }
        ],
    }

    def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=args,
            returncode=0,
            stdout="noise\n" + MARKER + json.dumps(marker_payload) + "\n",
            stderr="",
        )

    result = audit_rank0_torsion_preimages(
        cover_rows=cover_rows,
        selmer_gap_ledger=ledger,
        gap_type="rank0-sha2-gap2",
        sage_executable="sage",
        timeout_seconds=30,
        dot_sage=tmp_path / "dot_sage",
        run=fake_run,
    )

    assert result == {
        "status": "ok",
        "gap_type": "rank0-sha2-gap2",
        "target_cover_count": 1,
        "all_no_torsion_preimages": True,
        "no_torsion_preimage_count": 1,
        "failed_cover_count": 0,
        "sage": marker_payload,
        "stdout_tail": ["noise", MARKER + json.dumps(marker_payload)],
        "stderr_tail": [],
        "boundary": (
            "This checks torsion preimages on residual covers conditional on "
            "the associated elliptic curve having rank zero. It is not an "
            "unconditional no-point proof."
        ),
    }


def test_rank0_torsion_preimage_cli_writes_failure_audit(tmp_path: Path) -> None:
    covers = tmp_path / "covers.jsonl"
    ledger = tmp_path / "ledger.json"
    out = tmp_path / "out.json"
    covers.write_text(
        json.dumps(
            {
                "A": 115,
                "B": 297,
                "curve": "AA",
                "model": [0, 196194, 0, -699602500, -137257812885000],
                "covers": [
                    {
                        "index": 3,
                        "quartic": "x^4+3",
                        "covering_map_to_elliptic": "[x,y]",
                    }
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    ledger.write_text(
        json.dumps(
            {
                "rows": [
                    {
                        "A": 115,
                        "B": 297,
                        "curve": "AA",
                        "cover_index": 3,
                        "gap_type": "rank0-sha2-gap2",
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
            "scripts/theory/sage_audit_mixed_closure_rank0_torsion_preimages.py",
            "--covers",
            str(covers),
            "--selmer-gap-ledger",
            str(ledger),
            "--out",
            str(out),
            "--sage",
            sys.executable,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "target_cover_count=1" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["status"] == "sage-error"


def test_write_json_writes_sorted_rank0_torsion_preimage_audit(tmp_path: Path) -> None:
    out = tmp_path / "audit.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
