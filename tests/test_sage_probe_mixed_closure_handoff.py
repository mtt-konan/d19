from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.sage_probe_mixed_closure_handoff import (
    MARKER,
    _sage_program,
    probe_handoff,
    write_json,
)


def test_probe_handoff_parses_sage_marker(tmp_path: Path) -> None:
    handoff = {
        "A": 115,
        "B": 297,
        "curve": "AA",
        "weierstrass_model": [0, 196194, 0, -699602500, -137257812885000],
        "target_covers": [
            {
                "index": 3,
                "quartic": "41*x^4 + 10812*x^3 + 27981*x^2 - 54060*x + 1025",
            }
        ],
    }
    marker_payload = {
        "rank_bounds": [0, 2],
        "rank_proof_status": "runtime-error",
        "rank_proof_error": "rank not provably correct",
        "rank_probable": 0,
        "selmer_rank": 4,
        "torsion_two_dimension": 2,
        "two_descent": {"status": "ok", "result": False, "second_limit": 13},
        "covers": [
            {
                "index": 3,
                "genus": 1,
                "point_search_bound": 10,
                "rational_point_count": 0,
                "rational_points": [],
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

    result = probe_handoff(
        handoff,
        sage_executable="sage",
        timeout_seconds=30,
        point_search_bound=10,
        two_descent_second_limit=13,
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
            "This is a Sage probe of a residual handoff. A failed proof-rank "
            "attempt or bounded cover search is diagnostic evidence, not a "
            "proof that the cover has no rational point."
        ),
    }


def test_probe_handoff_reports_timeout(tmp_path: Path) -> None:
    handoff = {
        "A": 115,
        "B": 297,
        "curve": "AA",
        "weierstrass_model": [0, 196194, 0, -699602500, -137257812885000],
        "target_covers": [],
    }

    def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        raise subprocess.TimeoutExpired(
            cmd=["sage"],
            timeout=5,
            output="partial stdout",
            stderr="partial stderr",
        )

    result = probe_handoff(
        handoff,
        sage_executable="sage",
        timeout_seconds=5,
        point_search_bound=10,
        two_descent_second_limit=None,
        run=fake_run,
        dot_sage=tmp_path / "dot_sage",
    )

    assert result["status"] == "timeout"
    assert result["timeout_seconds"] == 5
    assert result["stdout_tail"] == ["partial stdout"]
    assert result["stderr_tail"] == ["partial stderr"]


def test_sage_program_uses_python_none_for_missing_two_descent_limit() -> None:
    program = _sage_program(
        {
            "weierstrass_model": [0, 196194, 0, -699602500, -137257812885000],
            "target_covers": [],
        },
        point_search_bound=10,
        two_descent_second_limit=None,
    )

    assert "two_descent_second_limit = None" in program
    assert "two_descent_second_limit = null" not in program


def test_write_json_writes_sorted_probe(tmp_path: Path) -> None:
    out = tmp_path / "probe.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
