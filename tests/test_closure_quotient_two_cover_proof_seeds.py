from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.summarize_closure_quotient_two_cover_proof_seeds import (
    BOUNDARY,
    summarize_two_cover_proof_seeds,
    write_json,
)


def _frontier() -> dict[str, object]:
    return {
        "targets": [
            {
                "class": "115:297",
                "observed_pair": [115, 297],
                "candidate_cover_count": 2,
                "rank_counts_by_curve": {
                    "AA": {"0/2": 1},
                    "AB": {"1/1": 1},
                    "BA": {"1/1": 1},
                    "BB": {"1/1": 1},
                },
                "residual_cover_rows": [
                    {
                        "curve": "AA",
                        "selmer_gap": 2,
                        "no_point_cover_indices": [3, 4],
                        "evidence_level": "bounded-search-no-point-candidate",
                    }
                ],
                "family_exclusion_proved": False,
                "candidate_not_proof": True,
            },
            {
                "class": "575:4641",
                "observed_pair": [575, 4641],
                "candidate_cover_count": 2,
                "rank_counts_by_curve": {
                    "AA": {"0/2": 1},
                    "AB": {"1/1": 1},
                    "BA": {"1/1": 1},
                    "BB": {"2/2": 1},
                },
                "residual_cover_rows": [
                    {
                        "curve": "AA",
                        "selmer_gap": 2,
                        "no_point_cover_indices": [3, 4],
                        "evidence_level": "bounded-search-no-point-candidate",
                    }
                ],
                "family_exclusion_proved": False,
                "candidate_not_proof": True,
            },
            {
                "class": "1449:12155",
                "observed_pair": [1449, 12155],
                "candidate_cover_count": 4,
                "rank_counts_by_curve": {
                    "AA": {"2/2": 1},
                    "AB": {"1/1": 1},
                    "BA": {"1/1": 1},
                    "BB": {"0/2": 1},
                },
                "residual_cover_rows": [
                    {
                        "curve": "BB",
                        "selmer_gap": 4,
                        "no_point_cover_indices": [3, 4, 5, 6],
                        "evidence_level": "bounded-search-no-point-candidate",
                    }
                ],
                "family_exclusion_proved": False,
                "candidate_not_proof": True,
            },
        ]
    }


def test_two_cover_proof_seeds_group_by_cover_certificate_need() -> None:
    summary = summarize_two_cover_proof_seeds(_frontier())

    assert summary == {
        "status": "ok",
        "ready": True,
        "seed_group_count": 3,
        "target_class_count": 3,
        "target_pair_count": 3,
        "candidate_cover_total": 8,
        "family_exclusion_proved_count": 0,
        "groups": [
            {
                "seed_pattern": (
                    "curve=AA selmer_gap=2 cover_count=2 "
                    "rank[AA:0/2|AB:1/1|BA:1/1|BB:1/1]"
                ),
                "curve": "AA",
                "selmer_gap": 2,
                "cover_count": 2,
                "rank_pattern": "AA:0/2|AB:1/1|BA:1/1|BB:1/1",
                "target_class_count": 1,
                "target_pair_count": 1,
                "candidate_cover_total": 2,
                "classes": ["115:297"],
                "candidate_not_proof": True,
                "family_exclusion_proved": False,
                "required_strict_evidence": [
                    "family 2-cover or Selmer obstruction",
                    "or reviewable cover-level no-point certificates for every listed cover",
                ],
            },
            {
                "seed_pattern": (
                    "curve=AA selmer_gap=2 cover_count=2 "
                    "rank[AA:0/2|AB:1/1|BA:1/1|BB:2/2]"
                ),
                "curve": "AA",
                "selmer_gap": 2,
                "cover_count": 2,
                "rank_pattern": "AA:0/2|AB:1/1|BA:1/1|BB:2/2",
                "target_class_count": 1,
                "target_pair_count": 1,
                "candidate_cover_total": 2,
                "classes": ["575:4641"],
                "candidate_not_proof": True,
                "family_exclusion_proved": False,
                "required_strict_evidence": [
                    "family 2-cover or Selmer obstruction",
                    "or reviewable cover-level no-point certificates for every listed cover",
                ],
            },
            {
                "seed_pattern": (
                    "curve=BB selmer_gap=4 cover_count=4 "
                    "rank[AA:2/2|AB:1/1|BA:1/1|BB:0/2]"
                ),
                "curve": "BB",
                "selmer_gap": 4,
                "cover_count": 4,
                "rank_pattern": "AA:2/2|AB:1/1|BA:1/1|BB:0/2",
                "target_class_count": 1,
                "target_pair_count": 1,
                "candidate_cover_total": 4,
                "classes": ["1449:12155"],
                "candidate_not_proof": True,
                "family_exclusion_proved": False,
                "required_strict_evidence": [
                    "family 2-cover or Selmer obstruction",
                    "or reviewable cover-level no-point certificates for every listed cover",
                ],
            },
        ],
        "boundary": BOUNDARY,
    }


def test_two_cover_proof_seeds_cli_writes_summary(tmp_path: Path) -> None:
    frontier = tmp_path / "frontier.json"
    out = tmp_path / "seeds.json"
    frontier.write_text(json.dumps(_frontier()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/summarize_closure_quotient_two_cover_proof_seeds.py",
            "--frontier",
            str(frontier),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "candidate_cover_total=8" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "family_exclusion_proved_count"
    ] == 0


def test_write_json_writes_sorted_two_cover_proof_seeds(tmp_path: Path) -> None:
    out = tmp_path / "seeds.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
