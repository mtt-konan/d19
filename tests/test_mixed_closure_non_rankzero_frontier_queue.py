from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.summarize_mixed_closure_non_rankzero_frontier import (
    build_non_rankzero_frontier_queue,
    load_jsonl,
    write_json,
)


def test_build_non_rankzero_frontier_queue_groups_rank1_and_even_gap_targets() -> None:
    open_frontier = {
        "rows": [
            {
                "priority": 8,
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "cover_index": 5,
                "gap_type": "rank1-sha2-gap2-open",
                "frontier_type": "rank1-needs-visible-generator-or-descent",
            },
            {
                "priority": 10,
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "cover_index": 4,
                "gap_type": "rank1-sha2-gap2-open",
                "frontier_type": "rank1-needs-visible-generator-or-descent",
            },
            {
                "priority": 11,
                "A": 1449,
                "B": 12155,
                "curve": "BB",
                "cover_index": 5,
                "gap_type": "even-rank-sha2-gap4-open",
                "frontier_type": "even-rank-gap4-needs-deeper-descent",
            },
        ]
    }
    diagnostics = [
        {
            "A": 209,
            "B": 5355,
            "curve": "BB",
            "status": "ok",
            "model": [0, 1, 0, -2, -3],
            "rank_bounds": [1, 3],
            "rank_plus_sha2_dimension": 3,
            "root_number": -1,
            "conductor": 101,
            "torsion_two_dimension": 2,
        },
        {
            "A": 1449,
            "B": 12155,
            "curve": "BB",
            "status": "ok",
            "model": [0, 2, 0, -3, -4],
            "rank_bounds": [0, 4],
            "rank_plus_sha2_dimension": 4,
            "root_number": 1,
            "conductor": 202,
            "torsion_two_dimension": 2,
        },
    ]

    queue = build_non_rankzero_frontier_queue(
        open_frontier_audit=open_frontier,
        diagnostics=diagnostics,
        sage_rechecks=[],
    )

    assert queue == {
        "status": "ok",
        "non_rankzero_frontier_cover_count": 3,
        "non_rankzero_frontier_target_count": 2,
        "target_type_counts": {
            "even-rank-gap4-needs-deeper-descent": 1,
            "rank1-needs-visible-generator-or-descent": 1,
        },
        "target_status_counts": {"even-gap4-open": 1, "rank1-open": 1},
        "targets": [
            {
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "frontier_type": "rank1-needs-visible-generator-or-descent",
                "gap_type": "rank1-sha2-gap2-open",
                "priorities": [8, 10],
                "cover_indices": [4, 5],
                "cover_count": 2,
                "diagnostic_status": "ok",
                "model": [0, 1, 0, -2, -3],
                "rank_bounds": [1, 3],
                "rank_plus_sha2_dimension": 3,
                "root_number": -1,
                "conductor": 101,
                "torsion_two_dimension": 2,
                "sage_recheck_status": None,
                "sage_recheck_final_rank_bounds": None,
                "sage_recheck_second_limits": [],
                "proof_queue_status": "rank1-open",
                "next_step": (
                    "find a visible rank-one generator and isolate the residual "
                    "Sha[2] class"
                ),
                "candidate_not_proof": True,
            },
            {
                "A": 1449,
                "B": 12155,
                "curve": "BB",
                "frontier_type": "even-rank-gap4-needs-deeper-descent",
                "gap_type": "even-rank-sha2-gap4-open",
                "priorities": [11],
                "cover_indices": [5],
                "cover_count": 1,
                "diagnostic_status": "ok",
                "model": [0, 2, 0, -3, -4],
                "rank_bounds": [0, 4],
                "rank_plus_sha2_dimension": 4,
                "root_number": 1,
                "conductor": 202,
                "torsion_two_dimension": 2,
                "sage_recheck_status": None,
                "sage_recheck_final_rank_bounds": None,
                "sage_recheck_second_limits": [],
                "proof_queue_status": "even-gap4-open",
                "next_step": "run deeper descent or produce an independent Sha[2] obstruction",
                "candidate_not_proof": True,
            },
        ],
        "boundary": (
            "This queue groups the non-rank-zero residual frontier by elliptic "
            "target. It is a proof-work queue, not a no-point certificate."
        ),
    }


def test_non_rankzero_frontier_queue_records_sage_recheck_status_without_proof_claim() -> None:
    queue = build_non_rankzero_frontier_queue(
        open_frontier_audit={
            "rows": [
                {
                    "priority": 8,
                    "A": 209,
                    "B": 5355,
                    "curve": "BB",
                    "cover_index": 5,
                    "gap_type": "rank1-sha2-gap2-open",
                    "frontier_type": "rank1-needs-visible-generator-or-descent",
                }
            ]
        },
        diagnostics=[
            {
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "status": "ok",
                "model": [0, 1, 0, -2, -3],
                "rank_bounds": [1, 3],
                "rank_plus_sha2_dimension": 3,
                "root_number": -1,
                "conductor": 101,
                "torsion_two_dimension": 2,
            }
        ],
        sage_rechecks=[
            {
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "status": "ok",
                "final_rank_bounds": [1, 1],
                "limits": [{"second_limit": 20, "rank_bounds": [1, 1]}],
            }
        ],
    )

    target = queue["targets"][0]
    assert queue["target_status_counts"] == {"rank-bounds-closed": 1}
    assert target["sage_recheck_status"] == "ok"
    assert target["sage_recheck_final_rank_bounds"] == [1, 1]
    assert target["sage_recheck_second_limits"] == [20]
    assert target["proof_queue_status"] == "rank-bounds-closed"
    assert target["next_step"] == (
        "use the closed rank bounds only as diagnostics; still prove the "
        "residual cover obstruction separately"
    )
    assert target["candidate_not_proof"] is True


def test_non_rankzero_frontier_queue_cli_writes_json(tmp_path: Path) -> None:
    frontier = tmp_path / "frontier.json"
    diagnostics = tmp_path / "diagnostics.jsonl"
    out = tmp_path / "queue.json"
    frontier.write_text(
        json.dumps(
            {
                "rows": [
                    {
                        "priority": 8,
                        "A": 209,
                        "B": 5355,
                        "curve": "BB",
                        "cover_index": 5,
                        "gap_type": "rank1-sha2-gap2-open",
                        "frontier_type": "rank1-needs-visible-generator-or-descent",
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
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "status": "ok",
                "model": [0, 1, 0, -2, -3],
                "rank_bounds": [1, 3],
                "rank_plus_sha2_dimension": 3,
                "root_number": -1,
                "conductor": 101,
                "torsion_two_dimension": 2,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/summarize_mixed_closure_non_rankzero_frontier.py",
            "--open-frontier-audit",
            str(frontier),
            "--diagnostics",
            str(diagnostics),
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
    assert "non_rankzero_frontier_target_count=1" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "non_rankzero_frontier_cover_count"
    ] == 1


def test_load_jsonl_ignores_blank_lines(tmp_path: Path) -> None:
    path = tmp_path / "rows.jsonl"
    path.write_text('{"a": 1}\n\n{"b": 2}\n', encoding="utf-8")

    assert load_jsonl(path) == [{"a": 1}, {"b": 2}]


def test_write_json_writes_sorted_non_rankzero_frontier_queue(tmp_path: Path) -> None:
    out = tmp_path / "queue.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
