from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.summarize_closure_quotient_ray_ledger import (
    BOUNDARY,
    LAMBDA_MAINLINE,
    summarize_ray_ledger,
    write_json,
)


def _rank_row(A: int, B: int, curve: str, lower: int, upper: int) -> dict[str, object]:
    return {
        "A": A,
        "B": B,
        "curve": curve,
        "status": "ok",
        "rank_lower": lower,
        "rank_upper": upper,
    }


def _rank_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for curve in ["AA", "BB", "AB", "BA"]:
        rows.append(_rank_row(6, 10, curve, 0, 0))
        rows.append(_rank_row(9, 15, curve, 0, 0))
        rows.append(_rank_row(10, 6, curve, 0, 2))
        rows.append(_rank_row(5, 5, curve, 1, 1))
    return rows


def test_ray_ledger_groups_pairs_by_primitive_ray_and_c_ratio_class() -> None:
    ledger = summarize_ray_ledger(
        rank_rows=_rank_rows(),
        rank_summary={
            "strict_excluded_pairs": [
                {"A": 6, "B": 10, "certifying_curves": ["AA"]},
                {"A": 9, "B": 15, "certifying_curves": ["BB"]},
            ]
        },
        residual_cover_summary={
            "no_point_cover_rows": [
                {
                    "A": 10,
                    "B": 6,
                    "curve": "AA",
                    "evidence_level": "bounded-search-no-point-candidate",
                    "no_point_cover_indices": [3, 4],
                    "selmer_gap": 2,
                }
            ]
        },
    )

    assert ledger["status"] == "ok"
    assert ledger["pair_count"] == 4
    assert ledger["rank_row_count"] == 16
    assert ledger["primitive_ray_count"] == 3
    assert ledger["c_ratio_class_count"] == 2
    assert ledger["strict_pair_count"] == 2
    assert ledger["strict_ray_count"] == 1
    assert ledger["strict_c_ratio_class_count"] == 1
    assert ledger["residual_candidate_pair_count"] == 1
    assert ledger["c_minus_zero_pair_count"] == 1
    assert ledger["lambda_mainline"] == LAMBDA_MAINLINE
    assert ledger["boundary"] == BOUNDARY

    ray_3_5 = next(
        row
        for row in ledger["ray_rows"]
        if row["primitive_A"] == 3 and row["primitive_B"] == 5
    )
    assert ray_3_5["c_plus_unit"] == 8
    assert ray_3_5["c_minus_unit"] == 2
    assert ray_3_5["c_ratio"] == "4"
    assert ray_3_5["scale_count"] == 2
    assert ray_3_5["coverage_status"] == "all-observed-pairs-strict"

    class_3_5 = next(
        row for row in ledger["c_ratio_class_rows"] if row["class"] == "3:5"
    )
    assert class_3_5["possible_oriented_rays"] == [[3, 5], [5, 3]]
    assert class_3_5["observed_oriented_rays"] == [[3, 5], [5, 3]]
    assert class_3_5["orientation_lost_by_c_ratio"] is True
    assert class_3_5["coverage_status"] == "some-observed-pairs-strict"


def test_ray_ledger_cli_writes_summary(tmp_path: Path) -> None:
    rank_jsonl = tmp_path / "rank.jsonl"
    rank_summary = tmp_path / "rank_summary.json"
    residual = tmp_path / "residual.json"
    out = tmp_path / "ray_ledger.json"
    rank_jsonl.write_text(
        "\n".join(json.dumps(row) for row in _rank_rows()) + "\n",
        encoding="utf-8",
    )
    rank_summary.write_text(
        json.dumps(
            {
                "strict_excluded_pairs": [
                    {"A": 6, "B": 10, "certifying_curves": ["AA"]}
                ]
            }
        ),
        encoding="utf-8",
    )
    residual.write_text(json.dumps({"no_point_cover_rows": []}), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/summarize_closure_quotient_ray_ledger.py",
            "--rank-jsonl",
            str(rank_jsonl),
            "--rank-summary",
            str(rank_summary),
            "--residual-cover-summary",
            str(residual),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "primitive_ray_count=3" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["c_ratio_class_count"] == 2


def test_write_json_writes_sorted_ray_ledger(tmp_path: Path) -> None:
    out = tmp_path / "ledger.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
