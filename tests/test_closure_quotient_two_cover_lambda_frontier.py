from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.summarize_closure_quotient_two_cover_lambda_frontier import (
    BOUNDARY,
    summarize_two_cover_frontier,
    write_json,
)


def _ray_ledger() -> dict[str, object]:
    return {
        "pair_rows": [
            {
                "A": 115,
                "B": 297,
                "primitive_A": 115,
                "primitive_B": 297,
                "lambda": "115/297",
                "c_ratio": "206/91",
                "c_ratio_class": "115:297",
                "status": "residual-candidate-not-proof",
                "rank_counts_by_curve": {
                    "AA": {"0/2": 1},
                    "BB": {"1/1": 1},
                },
                "residual_cover_rows": [
                    {
                        "curve": "AA",
                        "evidence_level": "bounded-search-no-point-candidate",
                        "no_point_cover_indices": [3, 4],
                        "selmer_gap": 2,
                    }
                ],
            },
            {
                "A": 3,
                "B": 5,
                "primitive_A": 3,
                "primitive_B": 5,
                "lambda": "3/5",
                "c_ratio": "4",
                "c_ratio_class": "3:5",
                "status": "strict-local-tool-excludes-observed-pair",
                "rank_counts_by_curve": {"AA": {"0/0": 1}},
                "residual_cover_rows": [],
            },
        ]
    }


def test_two_cover_frontier_keeps_only_residual_lambda_classes() -> None:
    audit = summarize_two_cover_frontier(_ray_ledger())

    assert audit == {
        "status": "ok",
        "ready": True,
        "target_class_count": 1,
        "target_pair_count": 1,
        "candidate_cover_total": 2,
        "selmer_gap_counts": {"2": 1},
        "evidence_level_counts": {"bounded-search-no-point-candidate": 1},
        "family_exclusion_proved_count": 0,
        "targets": [
            {
                "class": "115:297",
                "primitive_A": 115,
                "primitive_B": 297,
                "lambda": "115/297",
                "c_ratio": "206/91",
                "observed_pair": [115, 297],
                "rank_counts_by_curve": {
                    "AA": {"0/2": 1},
                    "BB": {"1/1": 1},
                },
                "residual_cover_rows": [
                    {
                        "curve": "AA",
                        "evidence_level": "bounded-search-no-point-candidate",
                        "no_point_cover_indices": [3, 4],
                        "selmer_gap": 2,
                    }
                ],
                "candidate_cover_count": 2,
                "required_strict_evidence": [
                    "family 2-cover or Selmer obstruction",
                    "or reviewable cover-level no-point certificates for every listed cover",
                ],
                "family_exclusion_proved": False,
                "candidate_not_proof": True,
            }
        ],
        "boundary": BOUNDARY,
    }


def test_two_cover_frontier_cli_writes_audit(tmp_path: Path) -> None:
    ledger = tmp_path / "ray.json"
    out = tmp_path / "frontier.json"
    ledger.write_text(json.dumps(_ray_ledger()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/summarize_closure_quotient_two_cover_lambda_frontier.py",
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
    assert json.loads(out.read_text(encoding="utf-8"))["candidate_cover_total"] == 2


def test_write_json_writes_sorted_two_cover_frontier(tmp_path: Path) -> None:
    out = tmp_path / "frontier.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
