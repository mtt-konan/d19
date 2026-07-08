from __future__ import annotations

import importlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

MODULE_NAME = "scripts.theory.audit_closure_quotient_lambda_structural_handoff"


def _handoff_module() -> ModuleType:
    assert importlib.util.find_spec(MODULE_NAME) is not None
    return importlib.import_module(MODULE_NAME)


def _c_ratio_coverage() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "defined_c_ratio_class_count": 3,
        "lambda_orientation_gap_class_count": 3,
        "strict_unordered_class_count": 1,
        "residual_unordered_class_count": 1,
        "open_unordered_class_count": 1,
        "lambda_family_exclusion_proved_count": 0,
        "no_point_certificate_added_count": 0,
        "search_count_used_as_progress": False,
        "c_ratio_coverage_not_lambda_family_proof": True,
    }


def _lambda_frontier() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lambda_class_count": 3,
        "track_counts": {
            "rank-zero-family-generalization": 1,
            "root-number-rank-structure-triage": 1,
            "two-cover-or-reviewable-no-point-certificate": 1,
        },
        "family_exclusion_proved_count": 0,
        "candidate_not_proof": True,
    }


def _route_partition() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
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


def _convergence_priorities() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "convergence_complete": False,
        "lambda_class_count": 3,
        "priority_order": ["rank_zero", "root_number", "two_cover"],
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "routes": [
            {
                "route": "rank_zero",
                "priority": 1,
                "class_count": 1,
                "missing_theorem": "rank-zero primitive lambda family theorem",
                "family_exclusion_proved": False,
            },
            {
                "route": "root_number",
                "priority": 2,
                "class_count": 1,
                "missing_theorem": "family rank or descent argument beyond parity data",
                "family_exclusion_proved": False,
            },
            {
                "route": "two_cover",
                "priority": 3,
                "class_count": 1,
                "missing_theorem": (
                    "family 2-cover obstruction or cover-level no-point certificates"
                ),
                "family_exclusion_proved": False,
            },
        ],
    }


def test_lambda_structural_handoff_routes_all_orientation_gaps() -> None:
    handoff = _handoff_module()

    audit = handoff.audit_lambda_structural_handoff(
        c_ratio_coverage=_c_ratio_coverage(),
        lambda_frontier=_lambda_frontier(),
        route_partition=_route_partition(),
        convergence_priorities=_convergence_priorities(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lambda_structural_handoff_ready"] is True
    assert audit["convergence_complete"] is False
    assert audit["orientation_gap_class_count"] == 3
    assert audit["handed_to_structural_route_count"] == 3
    assert audit["unhandled_orientation_gap_count"] == 0
    assert audit["route_counts"] == {
        "rank-zero-family-generalization": 1,
        "root-number-rank-structure-triage": 1,
        "two-cover-or-reviewable-no-point-certificate": 1,
    }
    assert audit["priority_order"] == ["rank_zero", "root_number", "two_cover"]
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["no_point_certificate_added_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["closure_quotient_promoted_to_lambda_proof"] is False
    assert audit["handoff_rows"] == [
        {
            "route": "rank_zero",
            "priority": 1,
            "class_count": 1,
            "structural_goal": "rank-zero primitive lambda family theorem",
            "acceptable_evidence": "family rank-zero proof over oriented lambda classes",
            "family_exclusion_proved": False,
        },
        {
            "route": "root_number",
            "priority": 2,
            "class_count": 1,
            "structural_goal": "family rank or descent argument beyond parity data",
            "acceptable_evidence": "root-number/parity plus rank or descent theorem",
            "family_exclusion_proved": False,
        },
        {
            "route": "two_cover",
            "priority": 3,
            "class_count": 1,
            "structural_goal": (
                "family 2-cover obstruction or cover-level no-point certificates"
            ),
            "acceptable_evidence": (
                "family 2-cover/Selmer obstruction or reviewable no-point certificates"
            ),
            "family_exclusion_proved": False,
        },
    ]


def test_lambda_structural_handoff_reports_unhandled_orientation_gaps() -> None:
    handoff = _handoff_module()
    route_partition = _route_partition()
    route_partition["covered_class_count"] = 2
    route_partition["missing_classes"] = ["13:17"]

    audit = handoff.audit_lambda_structural_handoff(
        c_ratio_coverage=_c_ratio_coverage(),
        lambda_frontier=_lambda_frontier(),
        route_partition=route_partition,
        convergence_priorities=_convergence_priorities(),
    )

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert audit["unhandled_orientation_gap_count"] == 1
    assert audit["violations"] == [
        "route_partition_not_ready_for_handoff",
        "orientation_gap_classes_unhandled",
    ]


def test_lambda_structural_handoff_cli_writes_audit(tmp_path: Path) -> None:
    c_ratio = tmp_path / "c_ratio.json"
    frontier = tmp_path / "frontier.json"
    partition = tmp_path / "partition.json"
    priorities = tmp_path / "priorities.json"
    out = tmp_path / "handoff.json"
    c_ratio.write_text(json.dumps(_c_ratio_coverage()), encoding="utf-8")
    frontier.write_text(json.dumps(_lambda_frontier()), encoding="utf-8")
    partition.write_text(json.dumps(_route_partition()), encoding="utf-8")
    priorities.write_text(json.dumps(_convergence_priorities()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_lambda_structural_handoff.py",
            "--c-ratio-coverage",
            str(c_ratio),
            "--lambda-frontier",
            str(frontier),
            "--route-partition",
            str(partition),
            "--convergence-priorities",
            str(priorities),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "lambda_structural_handoff_ready=True" in result.stdout
    assert "family_exclusion_proved_count=0" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["closure_quotient_promoted_to_lambda_proof"] is False


def test_write_json_writes_sorted_lambda_structural_handoff(tmp_path: Path) -> None:
    handoff = _handoff_module()
    out = tmp_path / "handoff.json"

    handoff.write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
