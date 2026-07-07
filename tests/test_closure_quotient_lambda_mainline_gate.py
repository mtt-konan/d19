from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_lambda_mainline import (
    BOUNDARY,
    audit_lambda_mainline,
    write_json,
)


def _ray_ledger() -> dict[str, object]:
    return {
        "pair_rows": [
            {
                "A": 3,
                "B": 5,
                "c_minus": 2,
                "c_plus": 8,
                "c_ratio": "4",
                "c_ratio_class": "3:5",
            }
        ],
        "c_ratio_class_count": 3,
        "c_ratio_class_rows": [
            {"class": "3:5"},
            {"class": "7:11"},
            {"class": "13:17"},
        ],
    }


def _lambda_frontier() -> dict[str, object]:
    return {
        "lambda_class_count": 3,
        "family_exclusion_proved_count": 0,
        "rejected_progress_metrics": [
            "more individual (A,B) search hits",
            "bounded point search with zero points",
        ],
    }


def _partition() -> dict[str, object]:
    return {
        "status": "ok",
        "lambda_class_count": 3,
        "covered_class_count": 3,
        "missing_classes": [],
        "overlap_classes": [],
        "unexpected_classes": [],
        "route_counts": {
            "rank-zero-family-generalization": 1,
            "root-number-rank-structure-triage": 1,
            "two-cover-or-reviewable-no-point-certificate": 1,
        },
        "family_exclusion_proved_count": 0,
    }


def _two_cover() -> dict[str, object]:
    return {
        "target_class_count": 1,
        "candidate_cover_total": 2,
        "family_exclusion_proved_count": 0,
        "targets": [
            {
                "required_strict_evidence": [
                    "family 2-cover or Selmer obstruction",
                    "or reviewable cover-level no-point certificates for every listed cover",
                ],
                "candidate_not_proof": True,
            }
        ],
    }


def test_lambda_mainline_gate_accepts_current_objective_shape() -> None:
    audit = audit_lambda_mainline(
        ray_ledger=_ray_ledger(),
        lambda_frontier=_lambda_frontier(),
        route_partition=_partition(),
        two_cover_frontier=_two_cover(),
    )

    assert audit == {
        "status": "ok",
        "ready": True,
        "lambda_class_count": 3,
        "covered_class_count": 3,
        "route_counts": {
            "rank-zero-family-generalization": 1,
            "root-number-rank-structure-triage": 1,
            "two-cover-or-reviewable-no-point-certificate": 1,
        },
        "checks": {
            "ray_ledger_has_c_minus": True,
            "route_partition_complete": True,
            "search_count_rejected_as_progress": True,
            "two_cover_requires_strict_evidence": True,
            "family_exclusion_claim_count_zero": True,
        },
        "violations": [],
        "boundary": BOUNDARY,
    }


def test_lambda_mainline_gate_reports_objective_violations() -> None:
    ray_ledger = _ray_ledger()
    ray_ledger["pair_rows"] = [{"A": 3, "B": 5, "c_plus": 8}]
    lambda_frontier = _lambda_frontier()
    lambda_frontier["family_exclusion_proved_count"] = 1
    partition = _partition()
    partition["missing_classes"] = ["13:17"]
    two_cover = _two_cover()
    two_cover["targets"] = [{"candidate_not_proof": False}]

    audit = audit_lambda_mainline(
        ray_ledger=ray_ledger,
        lambda_frontier=lambda_frontier,
        route_partition=partition,
        two_cover_frontier=two_cover,
    )

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert audit["violations"] == [
        "ray-ledger-missing-c-minus-or-c-ratio",
        "lambda-route-partition-incomplete",
        "two-cover-frontier-missing-strict-evidence-boundary",
        "family-exclusion-count-nonzero-without-theorem",
    ]


def test_lambda_mainline_gate_cli_writes_audit(tmp_path: Path) -> None:
    ray = tmp_path / "ray.json"
    frontier = tmp_path / "frontier.json"
    partition = tmp_path / "partition.json"
    two_cover = tmp_path / "two_cover.json"
    out = tmp_path / "gate.json"
    ray.write_text(json.dumps(_ray_ledger()), encoding="utf-8")
    frontier.write_text(json.dumps(_lambda_frontier()), encoding="utf-8")
    partition.write_text(json.dumps(_partition()), encoding="utf-8")
    two_cover.write_text(json.dumps(_two_cover()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_lambda_mainline.py",
            "--ray-ledger",
            str(ray),
            "--lambda-frontier",
            str(frontier),
            "--route-partition",
            str(partition),
            "--two-cover-frontier",
            str(two_cover),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "status=ok" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["ready"] is True


def test_write_json_writes_sorted_lambda_mainline_gate(tmp_path: Path) -> None:
    out = tmp_path / "gate.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
