from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.summarize_closure_quotient_rank_zero_proof_seeds import (
    BOUNDARY,
    summarize_rank_zero_proof_seeds,
    write_json,
)


def _primitive_models() -> dict[str, object]:
    return {
        "primitive_model_rows": [
            {
                "class": "3:5",
                "certifying_curve_patterns": ["AA"],
                "models": [{"curve": "AA", "p": -56}],
                "family_exclusion_proved": False,
            },
            {
                "class": "7:11",
                "certifying_curve_patterns": ["AA", "BB"],
                "models": [{"curve": "AA", "p": -120}, {"curve": "BB", "p": 88}],
                "family_exclusion_proved": False,
            },
        ]
    }


def test_rank_zero_proof_seeds_group_candidates_by_certifying_pattern() -> None:
    audit = summarize_rank_zero_proof_seeds(_primitive_models())

    assert audit == {
        "status": "ok",
        "ready": True,
        "seed_group_count": 2,
        "candidate_class_count": 2,
        "model_count": 3,
        "family_exclusion_proved_count": 0,
        "groups": [
            {
                "pattern": "AA",
                "candidate_class_count": 1,
                "model_count": 1,
                "model_counts_by_curve": {"AA": 1},
                "p_sign_counts": {"negative": 1},
                "classes": ["3:5"],
                "family_exclusion_proved": False,
                "next_action": (
                    "Try to prove this rank-zero pattern as a primitive lambda "
                    "family; this seed group is not itself a theorem."
                ),
            },
            {
                "pattern": "AA+BB",
                "candidate_class_count": 1,
                "model_count": 2,
                "model_counts_by_curve": {"AA": 1, "BB": 1},
                "p_sign_counts": {"negative": 1, "positive": 1},
                "classes": ["7:11"],
                "family_exclusion_proved": False,
                "next_action": (
                    "Try to prove this rank-zero pattern as a primitive lambda "
                    "family; this seed group is not itself a theorem."
                ),
            },
        ],
        "boundary": BOUNDARY,
    }


def test_rank_zero_proof_seeds_cli_writes_audit(tmp_path: Path) -> None:
    models = tmp_path / "models.json"
    out = tmp_path / "seeds.json"
    models.write_text(json.dumps(_primitive_models()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/summarize_closure_quotient_rank_zero_proof_seeds.py",
            "--primitive-models",
            str(models),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "seed_group_count=2" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "family_exclusion_proved_count"
    ] == 0


def test_write_json_writes_sorted_rank_zero_proof_seeds(tmp_path: Path) -> None:
    out = tmp_path / "seeds.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
