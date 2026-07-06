from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory import sage_recheck_mixed_closure_residuals as sage_recheck

recheck_rows = sage_recheck.recheck_rows
write_jsonl = sage_recheck.write_jsonl


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
        clock=iter([1.0, 4.0]).__next__,
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
            "elapsed_seconds": 3.0,
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


def test_filter_uncertain_rows_keeps_curve_subset_and_explicit_targets() -> None:
    rows = [
        {"A": 1, "B": 2, "curve": "AA"},
        {"A": 1, "B": 2, "curve": "AB"},
        {"A": 3, "B": 4, "curve": "BB"},
        {"A": 5, "B": 6, "curve": "BA"},
    ]

    filtered = sage_recheck.filter_uncertain_rows(
        rows,
        curves=["AA", "BB"],
        targets=[sage_recheck.parse_curve_target("3,4,BB")],
    )

    assert filtered == [{"A": 3, "B": 4, "curve": "BB"}]


def test_recheck_rows_records_elapsed_seconds() -> None:
    ticks = iter([10.0, 12.5])

    def fake_run(
        cmd: list[str],
        *,
        text: bool,
        capture_output: bool,
        timeout: int,
        check: bool,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            cmd,
            0,
            stdout='SAGE_RECHECK_JSON {"phase":"initial","rank_bounds":[0,2]}\n',
            stderr="",
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
        clock=lambda: next(ticks),
    )

    assert results[0]["elapsed_seconds"] == 2.5
