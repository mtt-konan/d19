from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.sage_recheck_mixed_closure_residuals import recheck_rows, write_jsonl


def test_recheck_rows_runs_sage_with_limits_and_records_final_bounds() -> None:
    calls: list[list[str]] = []

    def fake_run(
        cmd: list[str],
        *,
        text: bool,
        capture_output: bool,
        timeout: int,
        check: bool,
    ) -> subprocess.CompletedProcess[str]:
        calls.append(cmd)
        assert text is True
        assert capture_output is True
        assert timeout == 30
        assert check is False
        return subprocess.CompletedProcess(
            cmd,
            0,
            stdout=(
                "verbose line ignored\n"
                'SAGE_RECHECK_JSON {"phase":"initial","rank_bounds":[0,2]}\n'
                'SAGE_RECHECK_JSON {"phase":"two_descent","second_limit":13,'
                '"rank_bounds":[0,0]}\n'
            ),
            stderr="",
        )

    rows = [
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "rank": "0/2",
            "model": [0, 196194, 0, -699602500, -137257812885000],
        }
    ]

    results = recheck_rows(
        rows,
        sage_executable="sage",
        second_limits=[13],
        timeout_seconds=30,
        run=fake_run,
    )

    assert len(calls) == 1
    assert calls[0][:3] == ["sage", "-python", "-c"]
    assert "second_limit=13" in calls[0][3]
    assert results == [
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "input_rank": "0/2",
            "model": [0, 196194, 0, -699602500, -137257812885000],
            "status": "ok",
            "returncode": 0,
            "initial_rank_bounds": [0, 2],
            "final_rank_bounds": [0, 0],
            "limits": [{"second_limit": 13, "rank_bounds": [0, 0]}],
            "stdout_tail": [
                "verbose line ignored",
                'SAGE_RECHECK_JSON {"phase":"initial","rank_bounds":[0,2]}',
                'SAGE_RECHECK_JSON {"phase":"two_descent","second_limit":13,'
                '"rank_bounds":[0,0]}',
            ],
            "stderr_tail": [],
        }
    ]


def test_write_jsonl_writes_one_result_per_line(tmp_path: Path) -> None:
    out_path = tmp_path / "sage.jsonl"

    write_jsonl(out_path, [{"status": "ok"}, {"status": "timeout"}])

    assert out_path.read_text(encoding="utf-8").splitlines() == [
        '{"status": "ok"}',
        '{"status": "timeout"}',
    ]


def test_recheck_rows_records_timeout_output_when_sage_returns_bytes() -> None:
    def fake_run(
        cmd: list[str],
        *,
        text: bool,
        capture_output: bool,
        timeout: int,
        check: bool,
    ) -> subprocess.CompletedProcess[str]:
        raise subprocess.TimeoutExpired(
            cmd,
            timeout,
            output=b"partial stdout\n",
            stderr=b"partial stderr\n",
        )

    results = recheck_rows(
        [
            {
                "A": 115,
                "B": 297,
                "curve": "AA",
                "rank": "0/2",
                "model": [0, 196194, 0, -699602500, -137257812885000],
            }
        ],
        sage_executable="sage",
        second_limits=[13],
        timeout_seconds=30,
        run=fake_run,
    )

    assert results[0]["status"] == "timeout"
    assert results[0]["stdout_tail"] == ["partial stdout"]
    assert results[0]["stderr_tail"] == ["partial stderr"]
