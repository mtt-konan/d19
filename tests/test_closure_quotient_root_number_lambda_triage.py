from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.summarize_closure_quotient_root_number_lambda_triage import (
    BOUNDARY,
    summarize_root_number_triage,
    write_json,
)


def _rank_row(
    A: int,
    B: int,
    curve: str,
    lower: int,
    upper: int,
    root_number: int,
) -> dict[str, object]:
    return {
        "A": A,
        "B": B,
        "curve": curve,
        "status": "ok",
        "rank_lower": lower,
        "rank_upper": upper,
        "root_number": root_number,
    }


def _ray_ledger() -> dict[str, object]:
    return {
        "c_ratio_class_rows": [
            {
                "class": "3:5",
                "unordered_primitive_ray": [3, 5],
                "c_ratio": "4",
                "coverage_status": "observed-open",
            },
            {
                "class": "7:11",
                "unordered_primitive_ray": [7, 11],
                "c_ratio": "9/2",
                "coverage_status": "all-observed-pairs-strict",
            },
        ]
    }


def test_root_number_triage_keeps_root_number_as_diagnostic_only() -> None:
    rows = [
        _rank_row(3, 5, "AA", 1, 1, -1),
        _rank_row(3, 5, "BB", 0, 2, 1),
        _rank_row(3, 5, "AB", 2, 2, 1),
        _rank_row(3, 5, "BA", 1, 3, -1),
        _rank_row(7, 11, "AA", 0, 0, 1),
    ]

    audit = summarize_root_number_triage(rank_rows=rows, ray_ledger=_ray_ledger())

    assert audit == {
        "status": "ok",
        "ready": True,
        "target_class_count": 1,
        "target_pair_count": 1,
        "family_exclusion_proved_count": 0,
        "root_number_pattern_counts": {"AA:-1|AB:1|BA:-1|BB:1": 1},
        "rank_key_pattern_counts": {"AA:1/1|AB:2/2|BA:1/3|BB:0/2": 1},
        "targets": [
            {
                "class": "3:5",
                "unordered_primitive_ray": [3, 5],
                "c_ratio": "4",
                "coverage_status": "observed-open",
                "observed_pairs": [[3, 5]],
                "root_numbers_by_curve": {
                    "AA": [-1],
                    "AB": [1],
                    "BA": [-1],
                    "BB": [1],
                },
                "rank_keys_by_curve": {
                    "AA": ["1/1"],
                    "AB": ["2/2"],
                    "BA": ["1/3"],
                    "BB": ["0/2"],
                },
                "root_number_pattern": "AA:-1|AB:1|BA:-1|BB:1",
                "rank_key_pattern": "AA:1/1|AB:2/2|BA:1/3|BB:0/2",
                "family_exclusion_proved": False,
                "next_action": (
                    "Use this root-number/rank pattern only to choose a "
                    "family rank or descent problem; root number alone is not "
                    "a no-point proof."
                ),
            }
        ],
        "boundary": BOUNDARY,
    }


def test_root_number_triage_cli_writes_audit(tmp_path: Path) -> None:
    rank_jsonl = tmp_path / "rank.jsonl"
    ledger = tmp_path / "ray.json"
    out = tmp_path / "triage.json"
    rank_jsonl.write_text(
        "\n".join(
            json.dumps(row)
            for row in [
                _rank_row(3, 5, "AA", 1, 1, -1),
                _rank_row(3, 5, "BB", 0, 2, 1),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    ledger.write_text(json.dumps(_ray_ledger()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/summarize_closure_quotient_root_number_lambda_triage.py",
            "--rank-jsonl",
            str(rank_jsonl),
            "--ray-ledger",
            str(ledger),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "target_class_count=1" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "family_exclusion_proved_count"
    ] == 0


def test_write_json_writes_sorted_root_number_triage(tmp_path: Path) -> None:
    out = tmp_path / "triage.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
