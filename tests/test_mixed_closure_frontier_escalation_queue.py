from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_mixed_closure_frontier_escalation_queue import (
    audit_escalation_queue,
    write_json,
)


def _strictification_queue() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "target_count": 3,
        "cover_count": 7,
        "strict_certificate_ready_count": 0,
        "candidate_not_proof": True,
        "targets": [
            {
                "A": 1625,
                "B": 5643,
                "curve": "AA",
                "track": "rank-zero-rank-proof",
                "cover_indices": [3, 4],
                "cover_count": 2,
                "priorities": [5, 7],
                "rank_bounds": [0, 2],
                "required_strict_evidence": [
                    "strict elliptic rank proof closing rank_bounds to [0,0]",
                    "or a cover-level no-rational-point certificate for every listed cover",
                ],
                "nonproof_evidence": ["sage-timeout", "rank-bounds-not-closed"],
                "strict_certificate_ready": False,
            },
            {
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "track": "rank-one-sha2-separation",
                "cover_indices": [3, 4, 5],
                "cover_count": 3,
                "priorities": [8, 10, 22],
                "rank_bounds": [1, 3],
                "required_strict_evidence": [
                    "visible rank-one generator plus separation of the residual Sha[2] class",
                    "or a cover-level no-rational-point certificate for every listed cover",
                ],
                "nonproof_evidence": ["sage-timeout", "rank-bounds-not-closed"],
                "strict_certificate_ready": False,
            },
            {
                "A": 1449,
                "B": 12155,
                "curve": "BB",
                "track": "even-gap4-deeper-descent",
                "cover_indices": [3, 4],
                "cover_count": 2,
                "priorities": [11, 15],
                "rank_bounds": [0, 4],
                "required_strict_evidence": [
                    "deeper descent or independent Sha[2] obstruction",
                    "or a cover-level no-rational-point certificate for every listed cover",
                ],
                "nonproof_evidence": ["sage-timeout", "rank-bounds-not-closed"],
                "strict_certificate_ready": False,
            },
        ],
    }


def _attempt_audit() -> dict[str, object]:
    return {
        "status": "ok",
        "attempt_count": 5,
        "target_count_with_attempts": 1,
        "strict_certificate_ready_count": 0,
        "candidate_not_proof": True,
        "attempt_status_counts": {
            "rank-method-open-not-proof": 1,
            "rank-method-timeout-not-proof": 1,
        },
        "missing_files": [],
        "violations": [],
    }


def _next_action_audit() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "rank_zero_target_count": 1,
        "rank_zero_batch_target_count": 1,
        "cheap_rank_method_target_hopping_exhausted": True,
        "rank_zero_rank_method_target_hopping_exhausted": True,
        "strict_certificate_ready_count": 0,
        "recommended_mainline": "escalate-beyond-cheap-rank-methods",
        "violations": [],
    }


def test_escalation_queue_records_strict_routes_after_rank_methods_exhausted() -> None:
    audit = audit_escalation_queue(
        strictification_queue=_strictification_queue(),
        attempt_audit=_attempt_audit(),
        next_action_audit=_next_action_audit(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["target_count"] == 3
    assert audit["cover_count"] == 7
    assert audit["strict_certificate_ready_count"] == 0
    assert audit["rank_zero_rank_method_target_hopping_exhausted"] is True
    assert audit["route_counts"] == {
        "even-gap4-deeper-descent-or-cover-descent": 1,
        "rank-one-generator-sha2-separation-or-cover-descent": 1,
        "rank-zero-external-rank-proof-or-cover-descent": 1,
    }
    assert audit["targets"][0] == {
        "A": 1625,
        "B": 5643,
        "curve": "AA",
        "track": "rank-zero-rank-proof",
        "cover_indices": [3, 4],
        "cover_count": 2,
        "priorities": [5, 7],
        "rank_bounds": [0, 2],
        "primary_escalation_route": (
            "external strict rank proof, then cover-level no-point certificates"
        ),
        "rank_method_attempt_status": "exhausted-without-proof",
        "required_strict_evidence": [
            "strict elliptic rank proof closing rank_bounds to [0,0]",
            "or a cover-level no-rational-point certificate for every listed cover",
        ],
        "nonproof_evidence_not_promotable": [
            "sage-timeout",
            "rank-bounds-not-closed",
        ],
        "strict_certificate_ready": False,
        "candidate_not_proof": True,
    }
    assert audit["proof_status"] == "escalation-queue-not-proof"


def test_escalation_queue_reports_missing_rank_method_exhaustion() -> None:
    next_action = _next_action_audit()
    next_action["rank_zero_rank_method_target_hopping_exhausted"] = False

    audit = audit_escalation_queue(
        strictification_queue=_strictification_queue(),
        attempt_audit=_attempt_audit(),
        next_action_audit=next_action,
    )

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert audit["violations"] == [
        {
            "name": "next_action_audit",
            "field": "rank_zero_rank_method_target_hopping_exhausted",
            "expected": True,
            "actual": False,
        }
    ]


def test_escalation_queue_cli_strict_exits_nonzero_on_issues(tmp_path: Path) -> None:
    strictification_path = tmp_path / "strictification.json"
    attempt_path = tmp_path / "attempt.json"
    next_action_path = tmp_path / "next_action.json"
    out = tmp_path / "escalation.json"
    strictification_path.write_text(
        json.dumps(_strictification_queue()) + "\n", encoding="utf-8"
    )
    attempt_path.write_text(json.dumps(_attempt_audit()) + "\n", encoding="utf-8")
    next_action = _next_action_audit()
    next_action["status"] = "issues"
    next_action_path.write_text(json.dumps(next_action) + "\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_mixed_closure_frontier_escalation_queue.py",
            "--strictification-queue",
            str(strictification_path),
            "--attempt-audit",
            str(attempt_path),
            "--next-action-audit",
            str(next_action_path),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "status=issues" in result.stdout


def test_write_json_writes_sorted_escalation_queue(tmp_path: Path) -> None:
    out = tmp_path / "escalation.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
