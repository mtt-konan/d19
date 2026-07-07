from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.summarize_mixed_closure_frontier_strictification import (
    build_strictification_queue,
    write_json,
)


def _rank_zero_target(
    *,
    a_value: int,
    b_value: int,
    priority: int,
    timeout_seconds: int,
) -> dict[str, object]:
    return {
        "A": a_value,
        "B": b_value,
        "curve": "AA",
        "priorities": [priority, priority + 1],
        "cover_indices": [3, 4],
        "cover_count": 2,
        "rank_bounds": [0, 2],
        "rank_proof_queue_status": "sage-timeout",
        "sage_recheck_timeout_seconds": timeout_seconds,
        "candidate_not_proof": True,
    }


def _non_rankzero_target(
    *,
    a_value: int,
    b_value: int,
    priorities: list[int],
    cover_indices: list[int],
    rank_bounds: list[int],
    frontier_type: str,
) -> dict[str, object]:
    return {
        "A": a_value,
        "B": b_value,
        "curve": "BB",
        "frontier_type": frontier_type,
        "priorities": priorities,
        "cover_indices": cover_indices,
        "cover_count": len(cover_indices),
        "rank_bounds": rank_bounds,
        "proof_queue_status": "sage-timeout",
        "candidate_not_proof": True,
    }


def _handoff_audit() -> dict[str, object]:
    return {
        "status": "ok",
        "handoff_group_count": 4,
        "target_cover_count": 9,
        "map_verified_group_count": 4,
        "local_witnessed_group_count": 4,
        "bounded_probe_group_count": 4,
        "strict_promotion_count": 0,
        "candidate_not_proof": True,
        "missing_files": [],
        "violations": [],
    }


def _rank_zero_queue() -> dict[str, object]:
    return {
        "status": "ok",
        "rank_zero_frontier_cover_count": 4,
        "rank_zero_frontier_target_count": 2,
        "closed_rank_zero_target_count": 0,
        "targets": [
            _rank_zero_target(
                a_value=100,
                b_value=200,
                priority=5,
                timeout_seconds=600,
            ),
            _rank_zero_target(
                a_value=300,
                b_value=400,
                priority=9,
                timeout_seconds=120,
            ),
        ],
    }


def _non_rankzero_queue() -> dict[str, object]:
    return {
        "status": "ok",
        "non_rankzero_frontier_cover_count": 5,
        "non_rankzero_frontier_target_count": 2,
        "targets": [
            _non_rankzero_target(
                a_value=500,
                b_value=600,
                priorities=[8, 10, 22],
                cover_indices=[3, 4, 5],
                rank_bounds=[1, 3],
                frontier_type="rank1-needs-visible-generator-or-descent",
            ),
            _non_rankzero_target(
                a_value=700,
                b_value=800,
                priorities=[11, 15],
                cover_indices=[5, 6],
                rank_bounds=[0, 4],
                frontier_type="even-rank-gap4-needs-deeper-descent",
            ),
        ],
    }


def test_build_strictification_queue_orders_targets_and_keeps_boundary() -> None:
    queue = build_strictification_queue(
        rank_zero_queue=_rank_zero_queue(),
        non_rankzero_queue=_non_rankzero_queue(),
        frontier_handoff_audit=_handoff_audit(),
    )

    assert queue["status"] == "ok"
    assert queue["ready"] is True
    assert queue["target_count"] == 4
    assert queue["cover_count"] == 9
    assert queue["strict_certificate_ready_count"] == 0
    assert queue["candidate_not_proof"] is True
    assert queue["track_counts"] == {
        "even-gap4-deeper-descent": 1,
        "rank-one-sha2-separation": 1,
        "rank-zero-rank-proof": 2,
    }
    assert queue["first_target"] == {
        "A": 100,
        "B": 200,
        "curve": "AA",
        "track": "rank-zero-rank-proof",
        "priorities": [5, 6],
        "cover_indices": [3, 4],
    }
    assert [target["track"] for target in queue["targets"]] == [
        "rank-zero-rank-proof",
        "rank-one-sha2-separation",
        "rank-zero-rank-proof",
        "even-gap4-deeper-descent",
    ]
    assert queue["targets"][0]["strict_certificate_ready"] is False
    assert queue["targets"][0]["required_strict_evidence"] == [
        "strict elliptic rank proof closing rank_bounds to [0,0]",
        "or a cover-level no-rational-point certificate for every listed cover",
    ]
    assert "bounded-search-zero-points" in queue["targets"][0]["nonproof_evidence"]
    assert queue["targets"][1]["required_strict_evidence"] == [
        "visible rank-one generator plus separation of the residual Sha[2] class",
        "or a cover-level no-rational-point certificate for every listed cover",
    ]
    assert queue["targets"][3]["required_strict_evidence"] == [
        "deeper descent or independent Sha[2] obstruction",
        "or a cover-level no-rational-point certificate for every listed cover",
    ]
    assert "does not prove" in queue["boundary"]


def test_build_strictification_queue_reports_handoff_audit_issues() -> None:
    handoff_audit = _handoff_audit()
    handoff_audit["status"] = "issues"
    handoff_audit["violations"] = [{"field": "proof_boundary"}]

    queue = build_strictification_queue(
        rank_zero_queue=_rank_zero_queue(),
        non_rankzero_queue=_non_rankzero_queue(),
        frontier_handoff_audit=handoff_audit,
    )

    assert queue["status"] == "issues"
    assert queue["ready"] is False
    assert queue["blocking_issues"] == ["frontier-handoff-audit-issues"]


def test_strictification_queue_cli_strict_exits_nonzero_when_not_ready(
    tmp_path: Path,
) -> None:
    rank_zero = tmp_path / "rank_zero.json"
    non_rankzero = tmp_path / "non_rankzero.json"
    handoff_audit = tmp_path / "handoff_audit.json"
    out = tmp_path / "strictification.json"
    rank_zero.write_text(json.dumps(_rank_zero_queue()) + "\n", encoding="utf-8")
    non_rankzero.write_text(json.dumps(_non_rankzero_queue()) + "\n", encoding="utf-8")
    bad_handoff = _handoff_audit()
    bad_handoff["strict_promotion_count"] = 1
    handoff_audit.write_text(json.dumps(bad_handoff) + "\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/summarize_mixed_closure_frontier_strictification.py",
            "--rank-zero-queue",
            str(rank_zero),
            "--non-rankzero-queue",
            str(non_rankzero),
            "--frontier-handoff-audit",
            str(handoff_audit),
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
    assert json.loads(out.read_text(encoding="utf-8"))["blocking_issues"] == [
        "frontier-handoff-audit-issues"
    ]


def test_write_json_writes_sorted_strictification_queue(tmp_path: Path) -> None:
    out = tmp_path / "queue.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
