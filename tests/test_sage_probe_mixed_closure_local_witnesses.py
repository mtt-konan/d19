from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.sage_probe_mixed_closure_local_witnesses import (
    MARKER,
    _sage_program,
    probe_local_witnesses,
    write_json,
)


def test_probe_local_witnesses_parses_sage_marker(tmp_path: Path) -> None:
    handoff = {
        "A": 115,
        "B": 297,
        "curve": "AA",
        "target_covers": [{"index": 3, "quartic": "x^4 + 1"}],
    }
    marker_payload = {
        "all_bad_primes_witnessed": True,
        "covers": [
            {
                "index": 3,
                "bad_primes": [2, 5],
                "witnesses": [
                    {"p": 2, "status": "ok", "kind": "infinity"},
                    {"p": 5, "status": "ok", "kind": "finite", "x": "1"},
                ],
            }
        ],
    }

    def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=args,
            returncode=0,
            stdout="noise\n" + MARKER + json.dumps(marker_payload) + "\n",
            stderr="",
        )

    result = probe_local_witnesses(
        handoff,
        sage_executable="sage",
        timeout_seconds=30,
        search_bound=300,
        max_denominator_power=3,
        run=fake_run,
        dot_sage=tmp_path / "dot_sage",
    )

    assert result == {
        "A": 115,
        "B": 297,
        "curve": "AA",
        "status": "ok",
        "sage": marker_payload,
        "stdout_tail": ["noise", MARKER + json.dumps(marker_payload)],
        "stderr_tail": [],
        "boundary": (
            "This searches for explicit Qp local witnesses at the bad primes of "
            "stored residual covers. It does not prove that any residual cover "
            "has no rational point."
        ),
    }


def test_probe_local_witnesses_reports_timeout(tmp_path: Path) -> None:
    handoff = {"A": 115, "B": 297, "curve": "AA", "target_covers": []}

    def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        raise subprocess.TimeoutExpired(
            cmd=["sage"],
            timeout=5,
            output="partial stdout",
            stderr="partial stderr",
        )

    result = probe_local_witnesses(
        handoff,
        sage_executable="sage",
        timeout_seconds=5,
        search_bound=300,
        max_denominator_power=3,
        run=fake_run,
        dot_sage=tmp_path / "dot_sage",
    )

    assert result["status"] == "timeout"
    assert result["timeout_seconds"] == 5
    assert result["stdout_tail"] == ["partial stdout"]
    assert result["stderr_tail"] == ["partial stderr"]


def test_sage_program_contains_qp_square_search() -> None:
    program = _sage_program(
        {
            "target_covers": [
                {
                    "index": 1,
                    "quartic": "x^4 + 1",
                }
            ],
        },
        search_bound=20,
        max_denominator_power=2,
    )

    assert "is_qp_square" in program
    assert "bad_primes_for_quartic" in program
    assert "SAGE_LOCAL_WITNESS_JSON" in program


def test_write_json_writes_sorted_local_witnesses(tmp_path: Path) -> None:
    out = tmp_path / "local.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
