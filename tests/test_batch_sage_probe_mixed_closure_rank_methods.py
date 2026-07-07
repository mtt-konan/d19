from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.batch_sage_probe_mixed_closure_rank_methods import (
    batch_probe_rank_methods,
    write_json,
)
from scripts.theory.sage_probe_mixed_closure_rank_methods import MARKER


def _queue() -> dict[str, object]:
    return {
        "status": "ok",
        "targets": [
            {
                "A": 1625,
                "B": 5643,
                "curve": "AA",
                "track": "rank-zero-rank-proof",
                "priorities": [5, 7],
                "cover_indices": [3, 4],
            },
            {
                "A": 209,
                "B": 5355,
                "curve": "BB",
                "track": "rank-one-sha2-separation",
                "priorities": [8, 10, 22],
                "cover_indices": [3, 4, 5],
            },
            {
                "A": 567,
                "B": 3757,
                "curve": "BB",
                "track": "rank-zero-rank-proof",
                "priorities": [6, 21],
                "cover_indices": [3, 4],
            },
        ],
    }


def _handoff_audit() -> dict[str, object]:
    return {
        "status": "ok",
        "groups": [
            {
                "name": "priority_005_1625_5643_AA_covers_4_3",
                "target": {"A": 1625, "B": 5643, "curve": "AA"},
            },
            {
                "name": "priority_008_209_5355_BB_covers_5_4_3",
                "target": {"A": 209, "B": 5355, "curve": "BB"},
            },
            {
                "name": "priority_006_567_3757_BB_covers_4_3",
                "target": {"A": 567, "B": 3757, "curve": "BB"},
            },
        ],
    }


def _write_handoff(path: Path, *, a_value: int, b_value: int, curve: str) -> None:
    write_json(
        path,
        {
            "A": a_value,
            "B": b_value,
            "curve": curve,
            "weierstrass_model": [0, 1, 0, -1, 0],
        },
    )


def test_batch_probe_rank_methods_selects_rank_zero_targets_in_queue_order(
    tmp_path: Path,
) -> None:
    handoff_dir = tmp_path / "handoffs"
    handoff_dir.mkdir()
    _write_handoff(
        handoff_dir / "priority_005_1625_5643_AA_covers_4_3.json",
        a_value=1625,
        b_value=5643,
        curve="AA",
    )
    _write_handoff(
        handoff_dir / "priority_006_567_3757_BB_covers_4_3.json",
        a_value=567,
        b_value=3757,
        curve="BB",
    )

    def fake_run(
        cmd: list[str],
        **_kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        method = cmd[-1].split("method = ")[1].splitlines()[0].strip().strip('"')
        payload = (
            {"status": "ok", "rank_bounds": [0, 2]}
            if method == "rank_bounds"
            else {"status": "ok", "selmer_rank": 4}
        )
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=0,
            stdout=MARKER + json.dumps(payload) + "\n",
            stderr="",
        )

    result = batch_probe_rank_methods(
        strictification_queue=_queue(),
        handoff_audit=_handoff_audit(),
        handoff_dir=handoff_dir,
        methods=["rank_bounds", "selmer_rank"],
        tracks=["rank-zero-rank-proof"],
        limit=2,
        sage_executable="sage",
        timeout_seconds=11,
        two_descent_second_limit=None,
        run=fake_run,
        dot_sage=tmp_path / "dot_sage",
    )

    assert result["status"] == "ok"
    assert result["target_count"] == 2
    assert result["rank_zero_proof_candidate_count"] == 0
    assert result["method_status_counts"] == {
        "rank_bounds:ok": 2,
        "selmer_rank:ok": 2,
    }
    assert [target["name"] for target in result["targets"]] == [
        "priority_005_1625_5643_AA_covers_4_3",
        "priority_006_567_3757_BB_covers_4_3",
    ]
    assert result["targets"][0]["track"] == "rank-zero-rank-proof"
    assert result["targets"][0]["probe"]["method_status_counts"] == {
        "rank_bounds:ok": 1,
        "selmer_rank:ok": 1,
    }


def test_batch_probe_rank_methods_reports_missing_handoff(tmp_path: Path) -> None:
    result = batch_probe_rank_methods(
        strictification_queue=_queue(),
        handoff_audit=_handoff_audit(),
        handoff_dir=tmp_path / "handoffs",
        methods=["rank_bounds"],
        tracks=["rank-zero-rank-proof"],
        limit=1,
        sage_executable="sage",
        timeout_seconds=11,
        two_descent_second_limit=None,
        run=subprocess.run,
        dot_sage=tmp_path / "dot_sage",
    )

    assert result["status"] == "issues"
    assert result["missing_files"] == [
        {
            "name": "priority_005_1625_5643_AA_covers_4_3",
            "path": str(
                tmp_path
                / "handoffs"
                / "priority_005_1625_5643_AA_covers_4_3.json"
            ),
        }
    ]
    assert result["target_count"] == 0


def test_batch_probe_rank_methods_cli_help_runs_from_repo_root() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/theory/batch_sage_probe_mixed_closure_rank_methods.py",
            "--help",
        ],
        text=True,
        capture_output=True,
        check=False,
        cwd=ROOT,
    )

    assert completed.returncode == 0
    assert "Batch Sage rank-method probes" in completed.stdout
