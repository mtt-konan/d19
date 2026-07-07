from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_mixed_closure_residual_frontier_strategy import (
    audit_frontier_strategy,
    write_json,
)


def test_audit_frontier_strategy_marks_short_sage_route_exhausted_without_proof() -> None:
    rank_zero_queue = {
        "status": "ok",
        "rank_zero_frontier_cover_count": 4,
        "rank_zero_frontier_target_count": 2,
        "closed_rank_zero_target_count": 0,
        "target_status_counts": {"sage-timeout": 2},
        "targets": [
            {
                "A": 1625,
                "B": 5643,
                "curve": "AA",
                "priorities": [5, 7],
                "cover_indices": [3, 4],
                "rank_proof_queue_status": "sage-timeout",
                "sage_recheck_timeout_seconds": 600,
            },
            {
                "A": 567,
                "B": 3757,
                "curve": "BB",
                "priorities": [6, 21],
                "cover_indices": [3, 4],
                "rank_proof_queue_status": "sage-timeout",
                "sage_recheck_timeout_seconds": 120,
            },
        ],
    }
    non_rankzero_queue = {
        "status": "ok",
        "non_rankzero_frontier_cover_count": 3,
        "non_rankzero_frontier_target_count": 2,
        "target_type_counts": {
            "even-rank-gap4-needs-deeper-descent": 1,
            "rank1-needs-visible-generator-or-descent": 1,
        },
        "target_status_counts": {"sage-timeout": 2},
        "targets": [
            {
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "frontier_type": "rank1-needs-visible-generator-or-descent",
                "proof_queue_status": "sage-timeout",
            },
            {
                "A": 1449,
                "B": 12155,
                "curve": "BB",
                "frontier_type": "even-rank-gap4-needs-deeper-descent",
                "proof_queue_status": "sage-timeout",
            },
        ],
    }

    audit = audit_frontier_strategy(
        rank_zero_queue=rank_zero_queue,
        non_rankzero_queue=non_rankzero_queue,
    )

    assert audit == {
        "status": "ok",
        "short_sage_retry_status": "exhausted-without-proof",
        "short_sage_retry_target_count": 4,
        "short_sage_retry_timeout_target_count": 4,
        "strict_promotion_count": 0,
        "candidate_not_proof": True,
        "rank_zero_strategy_status": {
            "cover_count": 4,
            "target_count": 2,
            "closed_target_count": 0,
            "untried_target_count": 0,
            "all_targets_timed_out": True,
            "target_status_counts": {"sage-timeout": 2},
            "proof_status": "rank-proof-frontier-not-proof",
        },
        "non_rankzero_strategy_status": {
            "cover_count": 3,
            "target_count": 2,
            "all_targets_timed_out": True,
            "target_status_counts": {"sage-timeout": 2},
            "target_type_counts": {
                "even-rank-gap4-needs-deeper-descent": 1,
                "rank1-needs-visible-generator-or-descent": 1,
            },
            "proof_status": "non-rankzero-frontier-not-proof",
        },
        "next_strategy_counts": {
            "even_gap4_deeper_descent_or_sha2_obstruction": 1,
            "external_rank_proof_or_cover_level_descent": 2,
            "rank1_generator_or_sha2_separation": 1,
        },
        "first_external_rank_target": {
            "A": 1625,
            "B": 5643,
            "curve": "AA",
            "priorities": [5, 7],
            "cover_indices": [3, 4],
            "has_long_sage_timeout": True,
            "max_timeout_seconds": 600,
        },
        "next_actions": [
            (
                "Stop treating short Sage rechecks as a remaining queue; every "
                "recorded frontier target has timed out."
            ),
            (
                "For rank-zero targets, use an external rank proof or a cover-level "
                "descent/Sha[2] obstruction before promoting any residual cover."
            ),
            (
                "For non-rank-zero targets, separate the visible rank contribution "
                "or produce a deeper independent 2-cover obstruction."
            ),
        ],
        "boundary": (
            "This audit summarizes proof-work routing after Sage retries. "
            "Timeouts are not proofs and do not certify that any residual cover "
            "has no rational point."
        ),
    }


def test_frontier_strategy_cli_writes_json(tmp_path: Path) -> None:
    rank_zero = tmp_path / "rank_zero.json"
    non_rankzero = tmp_path / "non_rankzero.json"
    out = tmp_path / "strategy.json"
    rank_zero.write_text(
        json.dumps(
            {
                "status": "ok",
                "rank_zero_frontier_cover_count": 2,
                "rank_zero_frontier_target_count": 1,
                "closed_rank_zero_target_count": 0,
                "target_status_counts": {"not-retried": 1},
                "targets": [
                    {
                        "A": 1,
                        "B": 2,
                        "curve": "AA",
                        "priorities": [1],
                        "cover_indices": [3],
                        "rank_proof_queue_status": "not-retried",
                    }
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    non_rankzero.write_text(
        json.dumps(
            {
                "status": "ok",
                "non_rankzero_frontier_cover_count": 0,
                "non_rankzero_frontier_target_count": 0,
                "target_type_counts": {},
                "target_status_counts": {},
                "targets": [],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_mixed_closure_residual_frontier_strategy.py",
            "--rank-zero-queue",
            str(rank_zero),
            "--non-rankzero-queue",
            str(non_rankzero),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "short_sage_retry_status=still-has-untried-targets" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["short_sage_retry_status"] == (
        "still-has-untried-targets"
    )


def test_write_json_writes_sorted_frontier_strategy(tmp_path: Path) -> None:
    out = tmp_path / "strategy.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
