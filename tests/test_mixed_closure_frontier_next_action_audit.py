from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_mixed_closure_frontier_next_actions import (
    audit_next_actions,
    write_json,
)


def _queue() -> dict[str, object]:
    return {
        "status": "ok",
        "target_count": 3,
        "targets": [
            {
                "A": 1625,
                "B": 5643,
                "curve": "AA",
                "track": "rank-zero-rank-proof",
                "priorities": [5, 7],
                "cover_indices": [3, 4],
                "rank_bounds": [0, 2],
                "max_timeout_seconds": 600,
            },
            {
                "A": 567,
                "B": 3757,
                "curve": "BB",
                "track": "rank-zero-rank-proof",
                "priorities": [6, 21],
                "cover_indices": [3, 4],
                "rank_bounds": [0, 2],
                "max_timeout_seconds": 120,
            },
            {
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "track": "rank-one-sha2-separation",
                "priorities": [8, 10, 22],
                "cover_indices": [3, 4, 5],
                "rank_bounds": [1, 3],
            },
        ],
    }


def _attempt_audit() -> dict[str, object]:
    return {
        "status": "ok",
        "attempt_count": 4,
        "target_count_with_attempts": 2,
        "strict_certificate_ready_count": 0,
        "attempt_status_counts": {
            "rank-method-open-not-proof": 2,
            "rank-method-timeout-not-proof": 1,
            "timeout-not-proof": 1,
        },
    }


def _batch_rank_methods() -> dict[str, object]:
    return {
        "status": "ok",
        "target_count": 2,
        "method_status_counts": {
            "pari_ellrank:ok": 2,
            "rank_bounds:ok": 2,
            "selmer_rank:ok": 2,
        },
        "rank_zero_proof_candidate_count": 0,
        "targets": [
            {
                "A": 1625,
                "B": 5643,
                "curve": "AA",
                "track": "rank-zero-rank-proof",
                "probe": {
                    "method_status_counts": {
                        "pari_ellrank:ok": 1,
                        "rank_bounds:ok": 1,
                        "selmer_rank:ok": 1,
                    },
                    "rank_zero_proof_candidate": False,
                },
            },
            {
                "A": 567,
                "B": 3757,
                "curve": "BB",
                "track": "rank-zero-rank-proof",
                "probe": {
                    "method_status_counts": {
                        "pari_ellrank:ok": 1,
                        "rank_bounds:ok": 1,
                        "selmer_rank:ok": 1,
                    },
                    "rank_zero_proof_candidate": False,
                },
            },
        ],
    }


def test_audit_next_actions_marks_cheap_rank_methods_exhausted() -> None:
    audit = audit_next_actions(
        strictification_queue=_queue(),
        attempt_audit=_attempt_audit(),
        batch_rank_methods=_batch_rank_methods(),
    )

    assert audit["status"] == "ok"
    assert audit["rank_zero_target_count"] == 2
    assert audit["rank_zero_batch_target_count"] == 2
    assert audit["cheap_rank_method_target_hopping_exhausted"] is True
    assert audit["rank_zero_rank_method_target_hopping_exhausted"] is True
    assert audit["strict_certificate_ready_count"] == 0
    assert audit["recommended_mainline"] == "escalate-beyond-cheap-rank-methods"
    assert audit["rank_zero_next_actions"] == {
        "rank_method_attempt_target_count": 2,
        "rank_method_attempt_status": "exhausted-without-proof",
        "required_strict_evidence": [
            "strict elliptic rank proof closing rank_bounds to [0,0]",
            "or a cover-level no-rational-point certificate for every listed cover",
        ],
        "next_action": (
            "Stop rank-method target hopping; use stronger descent, an external "
            "rank proof, or cover-level no-rational-point certificates."
        ),
    }
    assert audit["non_rankzero_next_actions"] == [
        {
            "A": 209,
            "B": 5355,
            "curve": "BB",
            "track": "rank-one-sha2-separation",
            "next_action": (
                "Find a visible rank-one generator and separate the residual "
                "Sha[2] class, or prove every listed cover has no rational point."
            ),
        }
    ]


def test_audit_next_actions_marks_rank_method_target_hopping_exhausted() -> None:
    attempt = _attempt_audit()
    attempt["target_count_with_attempts"] = 2

    audit = audit_next_actions(
        strictification_queue=_queue(),
        attempt_audit=attempt,
        batch_rank_methods=_batch_rank_methods(),
    )

    assert audit["rank_zero_rank_method_target_hopping_exhausted"] is True
    assert audit["rank_zero_next_actions"] == {
        "rank_method_attempt_target_count": 2,
        "rank_method_attempt_status": "exhausted-without-proof",
        "required_strict_evidence": [
            "strict elliptic rank proof closing rank_bounds to [0,0]",
            "or a cover-level no-rational-point certificate for every listed cover",
        ],
        "next_action": (
            "Stop rank-method target hopping; use stronger descent, an external "
            "rank proof, or cover-level no-rational-point certificates."
        ),
    }


def test_audit_next_actions_reports_incomplete_batch_coverage() -> None:
    batch = _batch_rank_methods()
    batch["targets"] = batch["targets"][:1]  # type: ignore[index]
    batch["target_count"] = 1

    audit = audit_next_actions(
        strictification_queue=_queue(),
        attempt_audit=_attempt_audit(),
        batch_rank_methods=batch,
    )

    assert audit["status"] == "issues"
    assert audit["cheap_rank_method_target_hopping_exhausted"] is False
    assert audit["violations"] == [
        {
            "name": "batch_rank_methods",
            "field": "rank_zero_target_coverage",
            "expected": 2,
            "actual": 1,
        }
    ]


def test_frontier_next_action_cli_strict_exits_nonzero_on_issues(
    tmp_path: Path,
) -> None:
    queue_path = tmp_path / "queue.json"
    attempt_path = tmp_path / "attempt.json"
    batch_path = tmp_path / "batch.json"
    out = tmp_path / "next.json"
    queue_path.write_text(json.dumps(_queue()) + "\n", encoding="utf-8")
    attempt_path.write_text(json.dumps(_attempt_audit()) + "\n", encoding="utf-8")
    batch = _batch_rank_methods()
    batch["status"] = "issues"
    batch_path.write_text(json.dumps(batch) + "\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_mixed_closure_frontier_next_actions.py",
            "--strictification-queue",
            str(queue_path),
            "--attempt-audit",
            str(attempt_path),
            "--batch-rank-methods",
            str(batch_path),
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


def test_write_json_writes_sorted_next_action_audit(tmp_path: Path) -> None:
    out = tmp_path / "next.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
