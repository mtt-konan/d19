from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def test_mixed_closure_rank_cli_writes_jsonl_without_pari(tmp_path: Path) -> None:
    out_path = tmp_path / "mixed.jsonl"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/rank_mixed_closure_curves.py",
            "--pair",
            "3,5",
            "--out",
            str(out_path),
            "--no-pari",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    rows = [json.loads(line) for line in out_path.read_text().splitlines()]
    assert len(rows) == 4
    assert {row["curve"] for row in rows} == {"AA", "BB", "AB", "BA"}
    assert all(row["status"] == "pari-unavailable" for row in rows)
    assert "wrote 4 rows" in result.stdout


def test_mixed_closure_rank_cli_can_pull_back_rank_zero_points(tmp_path: Path) -> None:
    out_path = tmp_path / "mixed_pullback.jsonl"

    subprocess.run(
        [
            sys.executable,
            "scripts/theory/rank_mixed_closure_curves.py",
            "--pair",
            "9,35",
            "--out",
            str(out_path),
            "--pullback-height",
            "100",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    rows = [json.loads(line) for line in out_path.read_text().splitlines()]
    aa = next(row for row in rows if row["curve"] == "AA")
    assert aa["rank_lower"] == 0
    assert aa["rank_upper"] == 0
    assert aa["point_count"] == 2
    assert {point["N"] for point in aa["point_classifications"]} == {"22"}
    assert all(point["is_midpoint"] for point in aa["point_classifications"])
    assert not any(point["is_full_closed_square"] for point in aa["point_classifications"])


def test_mixed_closure_rank_cli_can_certify_rank_zero_torsion_pullback(
    tmp_path: Path,
) -> None:
    out_path = tmp_path / "mixed_certified.jsonl"

    subprocess.run(
        [
            sys.executable,
            "scripts/theory/rank_mixed_closure_curves.py",
            "--pair",
            "9,35",
            "--out",
            str(out_path),
            "--certify-rank0-torsion",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    rows = [json.loads(line) for line in out_path.read_text().splitlines()]
    aa = next(row for row in rows if row["curve"] == "AA")
    certificate = aa["rank0_torsion_certificate"]
    assert certificate["status"] == "certified"
    assert certificate["certifies_no_full_closed_square"]
    assert certificate["all_affine_preimages_are_midpoints"]
    assert certificate["affine_preimage_count"] == 2
