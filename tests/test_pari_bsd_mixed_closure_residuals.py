from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.pari_bsd_mixed_closure_residuals import diagnose_rows, write_jsonl


def test_diagnose_rows_records_bsd_conditional_diagnostics() -> None:
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
                'PARI_BSD_JSON {"root_number":1,"ellrank_lower":0,'
                '"ellrank_upper":2,"ellrank_sha2_lower":0,'
                '"analytic_rank":0,"analytic_leading_value":"4.72955644264359",'
                '"bsd_factor":"0.295597277665225"}\n'
            ),
            stderr="PARI stack size set\n",
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

    results = diagnose_rows(
        rows,
        python_executable=sys.executable,
        timeout_seconds=30,
        stack_bytes=268435456,
        run=fake_run,
    )

    assert calls[0][:3] == [sys.executable, "-c", calls[0][2]]
    assert "pari.allocatemem(268435456)" in calls[0][2]
    assert results == [
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "input_rank": "0/2",
            "model": [0, 196194, 0, -699602500, -137257812885000],
            "status": "ok",
            "root_number": 1,
            "ellrank_lower": 0,
            "ellrank_upper": 2,
            "ellrank_sha2_lower": 0,
            "analytic_rank": 0,
            "analytic_leading_value": "4.72955644264359",
            "bsd_factor": "0.295597277665225",
            "evidence_level": "bsd-conditional-diagnostic",
            "stdout_tail": [
                'PARI_BSD_JSON {"root_number":1,"ellrank_lower":0,'
                '"ellrank_upper":2,"ellrank_sha2_lower":0,'
                '"analytic_rank":0,"analytic_leading_value":"4.72955644264359",'
                '"bsd_factor":"0.295597277665225"}'
            ],
            "stderr_tail": ["PARI stack size set"],
        }
    ]


def test_diagnose_rows_records_timeout() -> None:
    def fake_run(
        cmd: list[str],
        *,
        text: bool,
        capture_output: bool,
        timeout: int,
        check: bool,
    ) -> subprocess.CompletedProcess[str]:
        raise subprocess.TimeoutExpired(cmd, timeout, output=b"partial", stderr=b"slow")

    rows = [
        {
            "A": 209,
            "B": 5355,
            "curve": "BB",
            "rank": "1/3",
            "model": [0, 1, 0, -2, -3],
        }
    ]

    results = diagnose_rows(
        rows,
        python_executable=sys.executable,
        timeout_seconds=5,
        stack_bytes=268435456,
        run=fake_run,
    )

    assert results == [
        {
            "A": 209,
            "B": 5355,
            "curve": "BB",
            "input_rank": "1/3",
            "model": [0, 1, 0, -2, -3],
            "status": "timeout",
            "timeout_seconds": 5,
            "evidence_level": "no-bsd-diagnostic",
            "stdout_tail": ["partial"],
            "stderr_tail": ["slow"],
        }
    ]


def test_write_jsonl_writes_bsd_rows(tmp_path: Path) -> None:
    out_path = tmp_path / "bsd.jsonl"

    write_jsonl(out_path, [{"status": "ok"}])

    assert out_path.read_text(encoding="utf-8") == '{"status": "ok"}\n'
