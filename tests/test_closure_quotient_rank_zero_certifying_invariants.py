from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.summarize_closure_quotient_rank_zero_certifying_invariants import (
    BOUNDARY,
    summarize_certifying_invariants,
    write_json,
)


def _primitive_models() -> dict[str, object]:
    return {
        "primitive_model_rows": [
            {
                "class": "3:5",
                "unordered_primitive_ray": [3, 5],
                "certifying_curve_patterns": ["AA", "BB"],
                "models": [{"curve": "AA"}, {"curve": "BB"}],
            }
        ]
    }


def _rank_rows() -> list[dict[str, object]]:
    return [
        {
            "A": 3,
            "B": 5,
            "curve": "AA",
            "status": "ok",
            "rank_lower": 0,
            "rank_upper": 0,
            "torsion_order": 4,
            "root_number": 1,
            "sha2_lower": 0,
        },
        {
            "A": 6,
            "B": 10,
            "curve": "AA",
            "status": "ok",
            "rank_lower": 0,
            "rank_upper": 0,
            "torsion_order": 4,
            "root_number": 1,
            "sha2_lower": 2,
        },
        {
            "A": 3,
            "B": 5,
            "curve": "BB",
            "status": "ok",
            "rank_lower": 0,
            "rank_upper": 0,
            "torsion_order": 4,
            "root_number": 1,
            "sha2_lower": 0,
        },
        {
            "A": 7,
            "B": 11,
            "curve": "AA",
            "status": "ok",
            "rank_lower": 1,
            "rank_upper": 1,
            "torsion_order": 4,
            "root_number": -1,
            "sha2_lower": 0,
        },
    ]


def test_certifying_invariants_collapse_scaled_rows_to_primitive_models() -> None:
    summary = summarize_certifying_invariants(
        primitive_models=_primitive_models(),
        rank_rows=_rank_rows(),
    )

    assert summary == {
        "status": "ok",
        "ready": True,
        "primitive_model_count": 2,
        "matched_primitive_model_count": 2,
        "missing_primitive_model_count": 0,
        "matched_rank_row_count": 3,
        "family_exclusion_proved_count": 0,
        "rank_key_counts": {"0/0": 2},
        "torsion_order_counts": {"4": 2},
        "root_number_counts": {"1": 2},
        "sha2_lower_value_counts": {"0": 2, "2": 1},
        "all_matched_models_rank_zero": True,
        "all_matched_models_torsion_order_four": True,
        "all_matched_models_root_number_one": True,
        "models": [
            {
                "class": "3:5",
                "curve": "AA",
                "unordered_primitive_ray": [3, 5],
                "observed_pairs": [[3, 5], [6, 10]],
                "rank_keys": ["0/0"],
                "torsion_orders": [4],
                "root_numbers": [1],
                "sha2_lower_values": [0, 2],
                "certifying_invariant_status": "observed-rank-zero-torsion4-root1",
                "family_exclusion_proved": False,
            },
            {
                "class": "3:5",
                "curve": "BB",
                "unordered_primitive_ray": [3, 5],
                "observed_pairs": [[3, 5]],
                "rank_keys": ["0/0"],
                "torsion_orders": [4],
                "root_numbers": [1],
                "sha2_lower_values": [0],
                "certifying_invariant_status": "observed-rank-zero-torsion4-root1",
                "family_exclusion_proved": False,
            },
        ],
        "missing_primitive_models": [],
        "boundary": BOUNDARY,
    }


def test_certifying_invariants_cli_writes_summary(tmp_path: Path) -> None:
    primitive_models = tmp_path / "primitive_models.json"
    rank_jsonl = tmp_path / "rank.jsonl"
    out = tmp_path / "invariants.json"
    primitive_models.write_text(json.dumps(_primitive_models()), encoding="utf-8")
    rank_jsonl.write_text(
        "\n".join(json.dumps(row) for row in _rank_rows()) + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/summarize_closure_quotient_rank_zero_certifying_invariants.py",
            "--primitive-models",
            str(primitive_models),
            "--rank-jsonl",
            str(rank_jsonl),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "primitive_model_count=2" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "all_matched_models_root_number_one"
    ] is True


def test_write_json_writes_sorted_certifying_invariants(tmp_path: Path) -> None:
    out = tmp_path / "invariants.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
