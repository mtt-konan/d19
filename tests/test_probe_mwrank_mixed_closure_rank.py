from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.probe_mwrank_mixed_closure_rank import (
    build_mwrank_stdin,
    parse_mwrank_output,
    probe_from_handoff,
    resolve_mwrank_args,
    write_json,
)


def test_parse_mwrank_output_records_open_rank_bounds() -> None:
    output = """
    Summary of results:
            0 <= rank(E) <= 2
    The rank has not been completely determined,
    only a lower bound of 0 and an upper bound of 2.
    """

    parsed = parse_mwrank_output(output)

    assert parsed == {
        "rank_bounds": [0, 2],
        "rank_proved": False,
        "rank_zero_proof_candidate": False,
        "status": "open-rank-bounds-not-proof",
    }


def test_parse_mwrank_output_records_rank_zero_candidate_only_when_closed() -> None:
    output = "Summary of results:\n\t0 <= rank(E) <= 0\n"

    parsed = parse_mwrank_output(output)

    assert parsed == {
        "rank_bounds": [0, 0],
        "rank_proved": True,
        "rank_zero_proof_candidate": True,
        "status": "rank-zero-proof-candidate",
    }


def test_build_mwrank_stdin_uses_handoff_weierstrass_model() -> None:
    handoff = {
        "A": 1625,
        "B": 5643,
        "curve": "AA",
        "weierstrass_model": [0, 58105074, 0, -27891601562500, -1],
    }

    assert (
        build_mwrank_stdin(handoff)
        == "[0,58105074,0,-27891601562500,-1]\n0\n"
    )


def test_resolve_mwrank_args_uses_custom_args_without_default_prefix() -> None:
    assert resolve_mwrank_args(None) == ["-q", "-v", "1"]
    assert resolve_mwrank_args(["-q", "-v", "0", "-b", "20"]) == [
        "-q",
        "-v",
        "0",
        "-b",
        "20",
    ]


def test_probe_from_handoff_with_fake_runner_keeps_timeout_nonproof() -> None:
    handoff = {
        "A": 1625,
        "B": 5643,
        "curve": "AA",
        "weierstrass_model": [0, 58105074, 0, -27891601562500, -1],
    }

    def fake_runner(*, stdin_text: str, timeout_seconds: int) -> dict[str, object]:
        assert stdin_text == "[0,58105074,0,-27891601562500,-1]\n0\n"
        assert timeout_seconds == 7
        return {"status": "timeout", "stdout": "", "stderr": "", "returncode": None}

    probe = probe_from_handoff(
        handoff=handoff,
        sage="sage",
        timeout_seconds=7,
        mwrank_args=["-q", "-v", "0"],
        runner=fake_runner,
    )

    assert probe == {
        "status": "timeout",
        "target": {"A": 1625, "B": 5643, "curve": "AA"},
        "weierstrass_model": [0, 58105074, 0, -27891601562500, -1],
        "mwrank_args": ["-q", "-v", "0"],
        "rank_bounds": [],
        "rank_proved": False,
        "rank_zero_proof_candidate": False,
        "proof_status": "timeout-not-proof",
        "stdout": "",
        "stderr": "",
        "returncode": None,
        "boundary": (
            "This mwrank probe is a strictification attempt. Open rank bounds, "
            "timeouts, and runtime errors are not proofs."
        ),
    }


def test_probe_mwrank_cli_strict_exits_nonzero_on_missing_model(
    tmp_path: Path,
) -> None:
    handoff = tmp_path / "handoff.json"
    out = tmp_path / "probe.json"
    handoff.write_text('{"A":1,"B":2,"curve":"AA"}\n', encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/probe_mwrank_mixed_closure_rank.py",
            "--handoff",
            str(handoff),
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
    assert "status=invalid-input" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["proof_status"] == (
        "invalid-input-not-proof"
    )


def test_write_json_writes_sorted_mwrank_probe(tmp_path: Path) -> None:
    out = tmp_path / "probe.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
