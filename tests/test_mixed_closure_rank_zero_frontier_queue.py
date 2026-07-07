from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.summarize_mixed_closure_rank_zero_frontier import (
    build_rank_zero_frontier_queue,
    load_jsonl,
    write_json,
)


def test_build_rank_zero_frontier_queue_groups_covers_by_rank_target() -> None:
    open_frontier = {
        "rows": [
            {
                "priority": 5,
                "A": 1625,
                "B": 5643,
                "curve": "AA",
                "cover_index": 4,
                "frontier_type": "rank-zero-needs-rank-proof",
            },
            {
                "priority": 7,
                "A": 1625,
                "B": 5643,
                "curve": "AA",
                "cover_index": 3,
                "frontier_type": "rank-zero-needs-rank-proof",
            },
            {
                "priority": 8,
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "cover_index": 5,
                "frontier_type": "rank1-needs-visible-generator-or-descent",
            },
        ]
    }
    diagnostics = [
        {
            "A": 1625,
            "B": 5643,
            "curve": "AA",
            "status": "ok",
            "model": [0, 1, 0, -2, -3],
            "rank_bounds": [0, 2],
            "rank_plus_sha2_dimension": 2,
            "root_number": 1,
            "conductor": 100,
            "torsion_two_dimension": 2,
        }
    ]
    sage_rechecks = [
        {
            "A": 1625,
            "B": 5643,
            "curve": "AA",
            "status": "timeout",
            "final_rank_bounds": None,
            "limits": [{"second_limit": 13, "rank_bounds": [0, 2]}],
            "timeout_seconds": 120,
            "elapsed_seconds": 120.25,
        }
    ]

    queue = build_rank_zero_frontier_queue(
        open_frontier_audit=open_frontier,
        diagnostics=diagnostics,
        sage_rechecks=sage_rechecks,
    )

    assert queue == {
        "status": "ok",
        "rank_zero_frontier_cover_count": 2,
        "rank_zero_frontier_target_count": 1,
        "closed_rank_zero_target_count": 0,
        "target_status_counts": {"sage-timeout": 1},
        "targets": [
            {
                "A": 1625,
                "B": 5643,
                "curve": "AA",
                "priorities": [5, 7],
                "cover_indices": [3, 4],
                "cover_count": 2,
                "diagnostic_status": "ok",
                "model": [0, 1, 0, -2, -3],
                "rank_bounds": [0, 2],
                "rank_plus_sha2_dimension": 2,
                "root_number": 1,
                "conductor": 100,
                "torsion_two_dimension": 2,
                "sage_recheck_status": "timeout",
                "sage_recheck_final_rank_bounds": None,
                "sage_recheck_second_limits": [13],
                "sage_recheck_timeout_seconds": 120,
                "sage_recheck_elapsed_seconds": 120.25,
                "rank_proof_queue_status": "sage-timeout",
                "next_step": "retry rank proof with stronger descent tooling or external CAS",
                "candidate_not_proof": True,
            }
        ],
        "boundary": (
            "This queue groups rank-zero residual covers by elliptic rank target. "
            "It records proof attempts, but does not prove rank zero."
        ),
    }


def test_rank_zero_frontier_queue_marks_closed_rank_zero_rechecks() -> None:
    queue = build_rank_zero_frontier_queue(
        open_frontier_audit={
            "rows": [
                {
                    "priority": 1,
                    "A": 1,
                    "B": 2,
                    "curve": "AA",
                    "cover_index": 3,
                    "frontier_type": "rank-zero-needs-rank-proof",
                }
            ]
        },
        diagnostics=[
            {
                "A": 1,
                "B": 2,
                "curve": "AA",
                "status": "ok",
                "model": [0, 0, 0, -1, 0],
                "rank_bounds": [0, 2],
                "rank_plus_sha2_dimension": 2,
                "root_number": 1,
                "conductor": 11,
                "torsion_two_dimension": 2,
            }
        ],
        sage_rechecks=[
            {
                "A": 1,
                "B": 2,
                "curve": "AA",
                "status": "ok",
                "final_rank_bounds": [0, 0],
                "limits": [{"second_limit": 20, "rank_bounds": [0, 0]}],
            }
        ],
    )

    assert queue["closed_rank_zero_target_count"] == 1
    assert queue["target_status_counts"] == {"rank-zero-proved": 1}
    assert queue["targets"][0]["rank_proof_queue_status"] == "rank-zero-proved"
    assert queue["targets"][0]["next_step"] == (
        "rerun torsion-preimage audit under the new strict rank-zero proof"
    )


def test_rank_zero_frontier_queue_cli_writes_json(tmp_path: Path) -> None:
    frontier = tmp_path / "frontier.json"
    diagnostics = tmp_path / "diagnostics.jsonl"
    recheck = tmp_path / "recheck.jsonl"
    out = tmp_path / "queue.json"
    frontier.write_text(
        json.dumps(
            {
                "rows": [
                    {
                        "priority": 5,
                        "A": 1625,
                        "B": 5643,
                        "curve": "AA",
                        "cover_index": 4,
                        "frontier_type": "rank-zero-needs-rank-proof",
                    }
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )
    diagnostics.write_text(
        json.dumps(
            {
                "A": 1625,
                "B": 5643,
                "curve": "AA",
                "status": "ok",
                "model": [0, 1, 0, -2, -3],
                "rank_bounds": [0, 2],
                "rank_plus_sha2_dimension": 2,
                "root_number": 1,
                "conductor": 100,
                "torsion_two_dimension": 2,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    recheck.write_text("", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/summarize_mixed_closure_rank_zero_frontier.py",
            "--open-frontier-audit",
            str(frontier),
            "--diagnostics",
            str(diagnostics),
            "--sage-recheck",
            str(recheck),
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
    assert "rank_zero_frontier_target_count=1" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "rank_zero_frontier_cover_count"
    ] == 1


def test_load_jsonl_ignores_blank_lines(tmp_path: Path) -> None:
    path = tmp_path / "rows.jsonl"
    path.write_text('{"a": 1}\n\n{"b": 2}\n', encoding="utf-8")

    assert load_jsonl(path) == [{"a": 1}, {"b": 2}]


def test_write_json_writes_sorted_rank_zero_frontier_queue(tmp_path: Path) -> None:
    out = tmp_path / "queue.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
