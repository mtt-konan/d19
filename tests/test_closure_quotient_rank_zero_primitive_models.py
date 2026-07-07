from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.summarize_closure_quotient_rank_zero_primitive_models import (
    BOUNDARY,
    primitive_model_for_candidate,
    summarize_primitive_models,
    write_json,
)


def _candidate_aabb() -> dict[str, object]:
    return {
        "class": "3:5",
        "unordered_primitive_ray": [3, 5],
        "possible_oriented_rays": [[3, 5], [5, 3]],
        "c_ratio": "4",
        "coverage_status": "all-observed-pairs-strict",
        "observed_pair_count": 2,
        "strict_observed_pair_count": 2,
        "certifying_curve_patterns": ["AA", "BB"],
        "family_exclusion_proved": False,
    }


def test_primitive_model_for_candidate_records_aa_bb_models() -> None:
    row = primitive_model_for_candidate(_candidate_aabb())

    assert row == {
        "class": "3:5",
        "unordered_primitive_ray": [3, 5],
        "possible_oriented_rays": [[3, 5], [5, 3]],
        "c_ratio": "4",
        "coverage_status": "all-observed-pairs-strict",
        "certifying_curve_patterns": ["AA", "BB"],
        "family_exclusion_proved": False,
        "models": [
            {
                "curve": "AA",
                "primitive_A": 3,
                "primitive_B": 5,
                "leg": 3,
                "total": 8,
                "p": -56,
                "q": 10000,
                "sqrt_q": 100,
                "weierstrass_model": [0, -56, 0, -40000, 2240000],
            },
            {
                "curve": "BB",
                "primitive_A": 3,
                "primitive_B": 5,
                "leg": 5,
                "total": 8,
                "p": 72,
                "q": 26896,
                "sqrt_q": 164,
                "weierstrass_model": [0, 72, 0, -107584, -7746048],
            },
        ],
    }


def test_summarize_primitive_models_counts_model_patterns() -> None:
    summary = summarize_primitive_models(
        {
            "candidates": [
                _candidate_aabb(),
                {
                    "class": "7:11",
                    "unordered_primitive_ray": [7, 11],
                    "possible_oriented_rays": [[7, 11], [11, 7]],
                    "c_ratio": "9/2",
                    "coverage_status": "all-observed-pairs-strict",
                    "observed_pair_count": 1,
                    "strict_observed_pair_count": 1,
                    "certifying_curve_patterns": ["AA"],
                    "family_exclusion_proved": False,
                },
            ]
        }
    )

    assert summary["status"] == "ok"
    assert summary["candidate_class_count"] == 2
    assert summary["model_count"] == 3
    assert summary["model_counts_by_curve"] == {"AA": 2, "BB": 1}
    assert summary["family_exclusion_proved_count"] == 0
    assert summary["boundary"] == BOUNDARY


def test_rank_zero_primitive_models_cli_writes_summary(tmp_path: Path) -> None:
    candidates = tmp_path / "candidates.json"
    out = tmp_path / "models.json"
    candidates.write_text(
        json.dumps({"candidates": [_candidate_aabb()]}),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/summarize_closure_quotient_rank_zero_primitive_models.py",
            "--candidates",
            str(candidates),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "candidate_class_count=1" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["model_count"] == 2


def test_write_json_writes_sorted_primitive_model_index(tmp_path: Path) -> None:
    out = tmp_path / "models.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
