from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.summarize_closure_quotient_lambda_frontier import (
    ACCEPTED_STRUCTURAL_ROUTES,
    BOUNDARY,
    REJECTED_PROGRESS_METRICS,
    summarize_lambda_frontier,
    write_json,
)


def _ray_ledger() -> dict[str, object]:
    return {
        "c_ratio_class_rows": [
            {
                "class": "3:5",
                "unordered_primitive_ray": [3, 5],
                "possible_oriented_rays": [[3, 5], [5, 3]],
                "observed_oriented_rays": [[3, 5]],
                "c_ratio": "4",
                "coverage_status": "all-observed-pairs-strict",
            },
            {
                "class": "7:11",
                "unordered_primitive_ray": [7, 11],
                "possible_oriented_rays": [[7, 11], [11, 7]],
                "observed_oriented_rays": [[7, 11]],
                "c_ratio": "9/2",
                "coverage_status": "residual-candidate-open",
            },
            {
                "class": "13:17",
                "unordered_primitive_ray": [13, 17],
                "possible_oriented_rays": [[13, 17], [17, 13]],
                "observed_oriented_rays": [[13, 17]],
                "c_ratio": "15/2",
                "coverage_status": "observed-open",
            },
        ]
    }


def test_lambda_frontier_routes_classes_to_structural_tracks() -> None:
    audit = summarize_lambda_frontier(_ray_ledger())

    assert audit == {
        "status": "ok",
        "ready": True,
        "lambda_class_count": 3,
        "track_counts": {
            "rank-zero-family-generalization": 1,
            "root-number-rank-structure-triage": 1,
            "two-cover-or-reviewable-no-point-certificate": 1,
        },
        "coverage_status_counts": {
            "all-observed-pairs-strict": 1,
            "observed-open": 1,
            "residual-candidate-open": 1,
        },
        "family_exclusion_proved_count": 0,
        "candidate_not_proof": True,
        "accepted_structural_routes": list(ACCEPTED_STRUCTURAL_ROUTES),
        "rejected_progress_metrics": list(REJECTED_PROGRESS_METRICS),
        "mainline": (
            "Move from pair-count accumulation to lambda=A/B structural proof "
            "tracks."
        ),
        "routes": [
            {
                "class": "3:5",
                "unordered_primitive_ray": [3, 5],
                "possible_oriented_rays": [[3, 5], [5, 3]],
                "observed_oriented_rays": [[3, 5]],
                "c_ratio": "4",
                "coverage_status": "all-observed-pairs-strict",
                "track": "rank-zero-family-generalization",
                "next_action": (
                    "Try to prove that the observed AA/BB rank-zero "
                    "torsion-pullback mechanism persists on the primitive lambda "
                    "class, instead of adding more scaled (A,B) samples."
                ),
                "family_exclusion_proved": False,
                "candidate_not_proof": True,
            },
            {
                "class": "7:11",
                "unordered_primitive_ray": [7, 11],
                "possible_oriented_rays": [[7, 11], [11, 7]],
                "observed_oriented_rays": [[7, 11]],
                "c_ratio": "9/2",
                "coverage_status": "residual-candidate-open",
                "track": "two-cover-or-reviewable-no-point-certificate",
                "next_action": (
                    "Replace the residual candidate with a family 2-cover "
                    "obstruction or a reviewable cover-level no-point certificate."
                ),
                "family_exclusion_proved": False,
                "candidate_not_proof": True,
            },
            {
                "class": "13:17",
                "unordered_primitive_ray": [13, 17],
                "possible_oriented_rays": [[13, 17], [17, 13]],
                "observed_oriented_rays": [[13, 17]],
                "c_ratio": "15/2",
                "coverage_status": "observed-open",
                "track": "root-number-rank-structure-triage",
                "next_action": (
                    "Use root-number and rank-pattern diagnostics only to choose "
                    "a family rank/descent problem; do not count the diagnostic "
                    "as proof."
                ),
                "family_exclusion_proved": False,
                "candidate_not_proof": True,
            },
        ],
        "boundary": BOUNDARY,
    }


def test_lambda_frontier_cli_writes_audit(tmp_path: Path) -> None:
    ledger = tmp_path / "ray.json"
    out = tmp_path / "lambda.json"
    ledger.write_text(json.dumps(_ray_ledger()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/summarize_closure_quotient_lambda_frontier.py",
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

    assert "lambda_class_count=3" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "family_exclusion_proved_count"
    ] == 0


def test_write_json_writes_sorted_lambda_frontier(tmp_path: Path) -> None:
    out = tmp_path / "lambda.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
