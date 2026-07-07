from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.summarize_closure_quotient_rank_zero_family_candidates import (
    BOUNDARY,
    summarize_rank_zero_family_candidates,
    write_json,
)


def _ray_ledger() -> dict[str, object]:
    return {
        "c_ratio_class_rows": [
            {
                "class": "3:5",
                "unordered_primitive_ray": [3, 5],
                "possible_oriented_rays": [[3, 5], [5, 3]],
                "c_ratio": "4",
                "coverage_status": "all-observed-pairs-strict",
            },
            {
                "class": "7:11",
                "unordered_primitive_ray": [7, 11],
                "possible_oriented_rays": [[7, 11], [11, 7]],
                "c_ratio": "9/2",
                "coverage_status": "residual-candidate-open",
            },
        ],
        "pair_rows": [
            {
                "A": 6,
                "B": 10,
                "primitive_A": 3,
                "primitive_B": 5,
                "c_ratio_class": "3:5",
                "status": "strict-local-tool-excludes-observed-pair",
                "certifying_curves": ["AA"],
            },
            {
                "A": 9,
                "B": 15,
                "primitive_A": 3,
                "primitive_B": 5,
                "c_ratio_class": "3:5",
                "status": "strict-local-tool-excludes-observed-pair",
                "certifying_curves": ["BB"],
            },
            {
                "A": 7,
                "B": 11,
                "primitive_A": 7,
                "primitive_B": 11,
                "c_ratio_class": "7:11",
                "status": "residual-candidate-not-proof",
                "certifying_curves": [],
            },
        ],
    }


def test_rank_zero_family_candidates_summarize_certifying_curve_patterns() -> None:
    audit = summarize_rank_zero_family_candidates(_ray_ledger())

    assert audit == {
        "status": "ok",
        "ready": True,
        "candidate_class_count": 1,
        "strict_observed_pair_count": 2,
        "family_exclusion_proved_count": 0,
        "certifying_curve_pattern_counts": {"AA": 1, "BB": 1},
        "candidates": [
            {
                "class": "3:5",
                "unordered_primitive_ray": [3, 5],
                "possible_oriented_rays": [[3, 5], [5, 3]],
                "c_ratio": "4",
                "coverage_status": "all-observed-pairs-strict",
                "observed_pair_count": 2,
                "strict_observed_pair_count": 2,
                "certifying_curve_patterns": ["AA", "BB"],
                "family_exclusion_proved": False,
                "next_action": (
                    "Try to prove the listed AA/BB rank-zero mechanism over the "
                    "primitive lambda class; do not add more scaled pair samples "
                    "as the main progress metric."
                ),
            }
        ],
        "boundary": BOUNDARY,
    }


def test_rank_zero_family_candidates_cli_writes_audit(tmp_path: Path) -> None:
    ledger = tmp_path / "ray.json"
    out = tmp_path / "candidates.json"
    ledger.write_text(json.dumps(_ray_ledger()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/summarize_closure_quotient_rank_zero_family_candidates.py",
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

    assert "candidate_class_count=1" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "family_exclusion_proved_count"
    ] == 0


def test_write_json_writes_sorted_rank_zero_candidate_audit(tmp_path: Path) -> None:
    out = tmp_path / "candidates.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
