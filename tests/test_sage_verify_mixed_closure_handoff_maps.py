from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.sage_verify_mixed_closure_handoff_maps import (
    MARKER,
    _sage_program,
    verify_handoff_maps,
    write_json,
)


def test_verify_handoff_maps_parses_sage_marker(tmp_path: Path) -> None:
    handoff = {
        "A": 115,
        "B": 297,
        "curve": "AA",
        "weierstrass_model": [0, 196194, 0, -699602500, -137257812885000],
        "target_covers": [
            {
                "index": 3,
                "quartic": "x^4 + 1",
                "covering_map_to_elliptic": "[x, y]",
            }
        ],
    }
    marker_payload = {
        "all_verified": True,
        "covers": [
            {
                "index": 3,
                "map_parse_status": "ok",
                "identity_verified": True,
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

    result = verify_handoff_maps(
        handoff,
        sage_executable="sage",
        timeout_seconds=30,
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
            "This verifies stored cover-to-elliptic rational maps against the "
            "Weierstrass equation. It does not prove that any residual cover has "
            "no rational point."
        ),
    }


def test_verify_handoff_maps_reports_timeout(tmp_path: Path) -> None:
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

    result = verify_handoff_maps(
        handoff,
        sage_executable="sage",
        timeout_seconds=5,
        run=fake_run,
        dot_sage=tmp_path / "dot_sage",
    )

    assert result["status"] == "timeout"
    assert result["timeout_seconds"] == 5
    assert result["stdout_tail"] == ["partial stdout"]
    assert result["stderr_tail"] == ["partial stderr"]


def test_sage_program_contains_quotient_reduction() -> None:
    program = _sage_program(
        {
            "weierstrass_model": [0, 0, 0, -1, 0],
            "target_covers": [
                {
                    "index": 1,
                    "quartic": "x^4 + 1",
                    "covering_map_to_elliptic": "[x^2, x*y]",
                }
            ],
        }
    )

    assert "reduce_mod_cover_relation" in program
    assert "y^2 = f(x)" in program
    assert "SAGE_HANDOFF_MAP_VERIFY_JSON" in program


def test_write_json_writes_sorted_map_verification(tmp_path: Path) -> None:
    out = tmp_path / "maps.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
