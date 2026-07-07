from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_mixed_closure_frontier_handoffs import (
    audit_frontier_handoffs,
    write_json,
)


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _priority_rows() -> list[dict[str, object]]:
    return [
        {
            "priority": 1,
            "A": 10,
            "B": 20,
            "curve": "AA",
            "cover_index": 4,
            "quartic": "4*x^4 + 1",
            "proof_status": "candidate-not-proof",
        },
        {
            "priority": 2,
            "A": 10,
            "B": 20,
            "curve": "AA",
            "cover_index": 3,
            "quartic": "3*x^4 + 1",
            "proof_status": "candidate-not-proof",
        },
        {
            "priority": 3,
            "A": 30,
            "B": 40,
            "curve": "BB",
            "cover_index": 5,
            "quartic": "5*x^4 + 1",
            "proof_status": "candidate-not-proof",
        },
        {
            "priority": 4,
            "A": 30,
            "B": 40,
            "curve": "BB",
            "cover_index": 4,
            "quartic": "4*x^4 + 2",
            "proof_status": "candidate-not-proof",
        },
        {
            "priority": 5,
            "A": 30,
            "B": 40,
            "curve": "BB",
            "cover_index": 3,
            "quartic": "3*x^4 + 2",
            "proof_status": "candidate-not-proof",
        },
        {
            "priority": 6,
            "A": 50,
            "B": 60,
            "curve": "BB",
            "cover_index": 6,
            "quartic": "6*x^4 + 1",
            "proof_status": "candidate-not-proof",
        },
        {
            "priority": 7,
            "A": 50,
            "B": 60,
            "curve": "BB",
            "cover_index": 7,
            "quartic": "7*x^4 + 1",
            "proof_status": "candidate-not-proof",
        },
    ]


def _target(
    *,
    a_value: int,
    b_value: int,
    curve: str,
    priorities: list[int],
    cover_indices: list[int],
    rank_bounds: list[int],
    frontier_type: str | None = None,
) -> dict[str, object]:
    target: dict[str, object] = {
        "A": a_value,
        "B": b_value,
        "curve": curve,
        "priorities": priorities,
        "cover_indices": cover_indices,
        "cover_count": len(cover_indices),
        "rank_bounds": rank_bounds,
        "candidate_not_proof": True,
        "diagnostic_status": "ok",
        "proof_queue_status": "sage-timeout",
    }
    if frontier_type:
        target["frontier_type"] = frontier_type
    return target


def _write_complete_group(
    handoff_dir: Path,
    *,
    name: str,
    a_value: int,
    b_value: int,
    curve: str,
    rank_bounds: list[int],
    covers: list[tuple[int, str]],
    proof_boundary: str = (
        "This handoff packages evidence. It does not prove that any cover "
        "has no rational point."
    ),
) -> None:
    handoff = {
        "A": a_value,
        "B": b_value,
        "curve": curve,
        "target_cover_indices": [index for index, _quartic in covers],
        "target_covers": [
            {"index": index, "quartic": quartic, "point_count": 0}
            for index, quartic in covers
        ],
        "strict_proof_status": "open",
        "proof_boundary": proof_boundary,
    }
    probe = {
        "A": a_value,
        "B": b_value,
        "curve": curve,
        "status": "ok",
        "sage": {
            "rank_bounds": rank_bounds,
            "rank_proof_status": "runtime-error",
            "covers": [
                {
                    "index": index,
                    "point_search_status": "ok",
                    "rational_point_count": 0,
                }
                for index, _quartic in covers
            ],
        },
    }
    map_verify = {
        "A": a_value,
        "B": b_value,
        "curve": curve,
        "status": "ok",
        "sage": {
            "all_verified": True,
            "covers": [
                {"index": index, "map_parse_status": "ok", "identity_verified": True}
                for index, _quartic in covers
            ],
        },
    }
    local_witnesses = {
        "A": a_value,
        "B": b_value,
        "curve": curve,
        "status": "ok",
        "sage": {
            "all_bad_primes_witnessed": True,
            "covers": [
                {
                    "index": index,
                    "bad_primes": [2, index],
                    "all_witnessed": True,
                    "witnesses": [
                        {"p": 2, "status": "ok", "kind": "finite", "x": "0"},
                        {"p": index, "status": "ok", "kind": "finite", "x": "1"},
                    ],
                }
                for index, _quartic in covers
            ],
        },
    }
    handoff_dir.mkdir(parents=True, exist_ok=True)
    _write_json(handoff_dir / f"{name}.json", handoff)
    (handoff_dir / f"{name}.sage").write_text("sage handoff\n", encoding="utf-8")
    (handoff_dir / f"{name}.magma").write_text("magma handoff\n", encoding="utf-8")
    _write_json(handoff_dir / f"{name}_sage_probe.json", probe)
    _write_json(handoff_dir / f"{name}_map_verify.json", map_verify)
    _write_json(handoff_dir / f"{name}_local_witnesses.json", local_witnesses)


def _write_complete_fixture(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    priorities_path = tmp_path / "priorities.json"
    rank_zero_path = tmp_path / "rank_zero.json"
    non_rankzero_path = tmp_path / "non_rankzero.json"
    handoff_dir = tmp_path / "handoffs"
    _write_json(priorities_path, {"rows": _priority_rows()})
    _write_json(
        rank_zero_path,
        {
            "status": "ok",
            "rank_zero_frontier_cover_count": 2,
            "rank_zero_frontier_target_count": 1,
            "targets": [
                _target(
                    a_value=10,
                    b_value=20,
                    curve="AA",
                    priorities=[1, 2],
                    cover_indices=[3, 4],
                    rank_bounds=[0, 2],
                )
            ],
        },
    )
    _write_json(
        non_rankzero_path,
        {
            "status": "ok",
            "non_rankzero_frontier_cover_count": 5,
            "non_rankzero_frontier_target_count": 2,
            "targets": [
                _target(
                    a_value=30,
                    b_value=40,
                    curve="BB",
                    priorities=[3, 4, 5],
                    cover_indices=[3, 4, 5],
                    rank_bounds=[1, 3],
                    frontier_type="rank1-needs-visible-generator-or-descent",
                ),
                _target(
                    a_value=50,
                    b_value=60,
                    curve="BB",
                    priorities=[6, 7],
                    cover_indices=[6, 7],
                    rank_bounds=[0, 4],
                    frontier_type="even-rank-gap4-needs-deeper-descent",
                ),
            ],
        },
    )
    _write_complete_group(
        handoff_dir,
        name="priority_001_10_20_AA_covers_4_3",
        a_value=10,
        b_value=20,
        curve="AA",
        rank_bounds=[0, 2],
        covers=[(4, "4*x^4 + 1"), (3, "3*x^4 + 1")],
    )
    _write_complete_group(
        handoff_dir,
        name="priority_003_30_40_BB_covers_5_4_3",
        a_value=30,
        b_value=40,
        curve="BB",
        rank_bounds=[1, 3],
        covers=[(5, "5*x^4 + 1"), (4, "4*x^4 + 2"), (3, "3*x^4 + 2")],
    )
    _write_complete_group(
        handoff_dir,
        name="priority_006_50_60_BB_covers_6_7",
        a_value=50,
        b_value=60,
        curve="BB",
        rank_bounds=[0, 4],
        covers=[(6, "6*x^4 + 1"), (7, "7*x^4 + 1")],
    )
    return priorities_path, rank_zero_path, non_rankzero_path, handoff_dir


def test_audit_frontier_handoffs_marks_ready_when_all_frontier_packages_align(
    tmp_path: Path,
) -> None:
    priorities_path, rank_zero_path, non_rankzero_path, handoff_dir = (
        _write_complete_fixture(tmp_path)
    )

    audit = audit_frontier_handoffs(
        rank_zero_queue=json.loads(rank_zero_path.read_text(encoding="utf-8")),
        non_rankzero_queue=json.loads(non_rankzero_path.read_text(encoding="utf-8")),
        priorities=json.loads(priorities_path.read_text(encoding="utf-8")),
        handoff_dir=handoff_dir,
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["handoff_group_count"] == 3
    assert audit["target_cover_count"] == 7
    assert audit["rank_zero_group_count"] == 1
    assert audit["non_rankzero_group_count"] == 2
    assert audit["map_verified_group_count"] == 3
    assert audit["local_witnessed_group_count"] == 3
    assert audit["bounded_probe_group_count"] == 3
    assert audit["strict_promotion_count"] == 0
    assert audit["candidate_not_proof"] is True
    assert audit["missing_files"] == []
    assert audit["violations"] == []
    assert [group["name"] for group in audit["groups"]] == [
        "priority_001_10_20_AA_covers_4_3",
        "priority_003_30_40_BB_covers_5_4_3",
        "priority_006_50_60_BB_covers_6_7",
    ]
    assert audit["groups"][0]["proof_status"] == "handoff-not-proof"
    assert audit["groups"][1]["rank_bounds"] == [1, 3]
    assert audit["groups"][2]["frontier_type"] == "even-rank-gap4-needs-deeper-descent"
    assert "does not prove" in audit["boundary"]


def test_audit_frontier_handoffs_reports_bad_proof_boundary(tmp_path: Path) -> None:
    _priorities_path, rank_zero_path, non_rankzero_path, handoff_dir = (
        _write_complete_fixture(tmp_path)
    )
    _write_complete_group(
        handoff_dir,
        name="priority_001_10_20_AA_covers_4_3",
        a_value=10,
        b_value=20,
        curve="AA",
        rank_bounds=[0, 2],
        covers=[(4, "4*x^4 + 1"), (3, "3*x^4 + 1")],
        proof_boundary="This file closes the cover.",
    )

    audit = audit_frontier_handoffs(
        rank_zero_queue=json.loads(rank_zero_path.read_text(encoding="utf-8")),
        non_rankzero_queue=json.loads(non_rankzero_path.read_text(encoding="utf-8")),
        priorities={"rows": _priority_rows()},
        handoff_dir=handoff_dir,
    )

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert audit["strict_promotion_count"] == 0
    assert audit["violations"] == [
        {
            "name": "priority_001_10_20_AA_covers_4_3",
            "field": "proof_boundary",
            "expected": "contains 'does not prove'",
            "actual": "This file closes the cover.",
        }
    ]


def test_frontier_handoff_audit_cli_strict_exits_nonzero_when_not_ready(
    tmp_path: Path,
) -> None:
    priorities_path, rank_zero_path, non_rankzero_path, handoff_dir = (
        _write_complete_fixture(tmp_path)
    )
    (handoff_dir / "priority_003_30_40_BB_covers_5_4_3_map_verify.json").unlink()
    out = tmp_path / "audit.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_mixed_closure_frontier_handoffs.py",
            "--rank-zero-queue",
            str(rank_zero_path),
            "--non-rankzero-queue",
            str(non_rankzero_path),
            "--priorities",
            str(priorities_path),
            "--handoff-dir",
            str(handoff_dir),
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
    assert json.loads(out.read_text(encoding="utf-8"))["missing_files"] == [
        {
            "name": "priority_003_30_40_BB_covers_5_4_3",
            "kind": "map_verify",
            "path": str(
                handoff_dir / "priority_003_30_40_BB_covers_5_4_3_map_verify.json"
            ),
        }
    ]


def test_write_json_writes_sorted_frontier_handoff_audit(tmp_path: Path) -> None:
    out = tmp_path / "audit.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
