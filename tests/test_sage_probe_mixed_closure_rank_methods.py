from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.sage_probe_mixed_closure_rank_methods import (
    MARKER,
    _sage_method_program,
    probe_rank_methods,
    write_json,
)


def _handoff() -> dict[str, object]:
    return {
        "A": 1625,
        "B": 5643,
        "curve": "AA",
        "weierstrass_model": [
            0,
            58105074,
            0,
            -27891601562500,
            -1620643572767578125000,
        ],
    }


def test_probe_rank_methods_records_individual_method_results(tmp_path: Path) -> None:
    payloads = {
        "rank_bounds": {"status": "ok", "rank_bounds": [0, 2]},
        "rank_proof": {
            "status": "runtime-error",
            "error": "rank not provably correct",
        },
    }

    def fake_run(
        cmd: list[str],
        **_kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        method = cmd[-1].split("method = ")[1].splitlines()[0].strip().strip('"')
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=0,
            stdout=MARKER + json.dumps(payloads[method]) + "\n",
            stderr="",
        )

    result = probe_rank_methods(
        _handoff(),
        methods=["rank_bounds", "rank_proof"],
        sage_executable="sage",
        timeout_seconds=20,
        two_descent_second_limit=13,
        run=fake_run,
        dot_sage=tmp_path / "dot_sage",
    )

    assert result == {
        "A": 1625,
        "B": 5643,
        "curve": "AA",
        "status": "ok",
        "timeout_seconds": 20,
        "method_status_counts": {
            "rank_bounds:ok": 1,
            "rank_proof:runtime-error": 1,
        },
        "method_results": [
            {"method": "rank_bounds", "status": "ok", "rank_bounds": [0, 2]},
            {
                "method": "rank_proof",
                "status": "runtime-error",
                "error": "rank not provably correct",
            },
        ],
        "rank_zero_proof_candidate": False,
        "boundary": (
            "This probes Sage rank methods separately. Timeouts, runtime "
            "errors, open rank bounds, and bounded method limits are not proofs."
        ),
    }


def test_probe_rank_methods_records_timeout_for_one_method(tmp_path: Path) -> None:
    def fake_run(
        cmd: list[str],
        **_kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        method = cmd[-1].split("method = ")[1].splitlines()[0].strip().strip('"')
        if method == "rank_proof":
            raise subprocess.TimeoutExpired(cmd=cmd, timeout=9, output="partial")
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=0,
            stdout=MARKER + json.dumps({"status": "ok", "rank_bounds": [0, 2]}) + "\n",
            stderr="",
        )

    result = probe_rank_methods(
        _handoff(),
        methods=["rank_bounds", "rank_proof"],
        sage_executable="sage",
        timeout_seconds=9,
        two_descent_second_limit=None,
        run=fake_run,
        dot_sage=tmp_path / "dot_sage",
    )

    assert result["method_status_counts"] == {
        "rank_bounds:ok": 1,
        "rank_proof:timeout": 1,
    }
    assert result["method_results"][1] == {
        "method": "rank_proof",
        "status": "timeout",
        "timeout_seconds": 9,
        "stdout_tail": ["partial"],
        "stderr_tail": [],
    }
    assert result["rank_zero_proof_candidate"] is False


def test_probe_rank_methods_marks_rank_zero_proof_candidate(tmp_path: Path) -> None:
    def fake_run(
        cmd: list[str],
        **_kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=0,
            stdout=MARKER + json.dumps({"status": "ok", "rank": 0}) + "\n",
            stderr="",
        )

    result = probe_rank_methods(
        _handoff(),
        methods=["rank_proof"],
        sage_executable="sage",
        timeout_seconds=9,
        two_descent_second_limit=None,
        run=fake_run,
        dot_sage=tmp_path / "dot_sage",
    )

    assert result["rank_zero_proof_candidate"] is True
    assert result["method_status_counts"] == {"rank_proof:ok": 1}


def test_sage_method_program_includes_two_descent_second_limit() -> None:
    program = _sage_method_program(
        model=[0, 1, 0, -1, 0],
        method="two_descent",
        two_descent_second_limit=20,
    )

    assert 'method = "two_descent"' in program
    assert "two_descent_second_limit = 20" in program


def test_sage_method_program_supports_pari_ellrank() -> None:
    program = _sage_method_program(
        model=[0, 1, 0, -1, 0],
        method="pari_ellrank",
        two_descent_second_limit=None,
    )

    assert 'method = "pari_ellrank"' in program
    assert "pari('ellrank')" in program
    assert 'payload["rank_bounds"]' in program


def test_write_json_writes_sorted_rank_method_probe(tmp_path: Path) -> None:
    out = tmp_path / "probe.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
