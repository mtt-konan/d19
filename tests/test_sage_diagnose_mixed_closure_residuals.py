from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.sage_diagnose_mixed_closure_residuals import diagnose_rows, write_jsonl


def test_diagnose_rows_records_selmer_and_torsion_diagnostics() -> None:
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
                'SAGE_DIAG_JSON {"rank_bounds":[0,2],"selmer_rank_pari":4,'
                '"selmer_rank_mwrank":4,"torsion_order":4,'
                '"torsion_invariants":[2,2],"torsion_two_dimension":2,'
                '"root_number":1,"conductor":10548872720}\n'
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

    results = diagnose_rows(rows, sage_executable="sage", timeout_seconds=30, run=fake_run)

    assert calls[0][:3] == ["sage", "-python", "-c"]
    assert results == [
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "input_rank": "0/2",
            "model": [0, 196194, 0, -699602500, -137257812885000],
            "status": "ok",
            "rank_bounds": [0, 2],
            "selmer_rank_pari": 4,
            "selmer_rank_mwrank": 4,
            "torsion_order": 4,
            "torsion_invariants": [2, 2],
            "torsion_two_dimension": 2,
            "root_number": 1,
            "conductor": 10548872720,
            "rank_plus_sha2_dimension": 2,
            "stdout_tail": [
                'SAGE_DIAG_JSON {"rank_bounds":[0,2],"selmer_rank_pari":4,'
                '"selmer_rank_mwrank":4,"torsion_order":4,'
                '"torsion_invariants":[2,2],"torsion_two_dimension":2,'
                '"root_number":1,"conductor":10548872720}'
            ],
            "stderr_tail": [],
        }
    ]


def test_diagnose_rows_can_request_probable_analytic_rank() -> None:
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
        return subprocess.CompletedProcess(
            cmd,
            0,
            stdout=(
                'SAGE_DIAG_JSON {"rank_bounds":[0,2],"selmer_rank_pari":4,'
                '"selmer_rank_mwrank":4,"torsion_order":4,'
                '"torsion_invariants":[2,2],"torsion_two_dimension":2,'
                '"root_number":1,"conductor":10548872720,'
                '"analytic_rank_pari":0}\n'
            ),
            stderr="",
        )

    results = diagnose_rows(
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
        timeout_seconds=30,
        run=fake_run,
        analytic_rank_algorithms=["pari"],
    )

    assert 'analytic_rank_algorithms = ["pari"]' in calls[0][3]
    assert results[0]["analytic_rank_pari"] == 0


def test_write_jsonl_writes_diagnostic_rows(tmp_path: Path) -> None:
    out_path = tmp_path / "diag.jsonl"

    write_jsonl(out_path, [{"status": "ok"}])

    assert out_path.read_text(encoding="utf-8") == '{"status": "ok"}\n'
