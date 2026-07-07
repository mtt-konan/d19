#!/usr/bin/env python3
"""Probe a mixed-closure residual target with Sage's bundled mwrank."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This mwrank probe is a strictification attempt. Open rank bounds, "
    "timeouts, and runtime errors are not proofs."
)

Runner = Callable[..., dict[str, object]]


def resolve_mwrank_args(values: list[str] | None) -> list[str]:
    return list(values) if values else ["-q", "-v", "1"]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_mwrank_stdin(handoff: dict[str, Any]) -> str:
    model = handoff.get("weierstrass_model")
    if not isinstance(model, list) or len(model) != 5:
        raise ValueError("handoff missing five-term weierstrass_model")
    return "[" + ",".join(str(int(value)) for value in model) + "]\n0\n"


def parse_mwrank_output(output: str) -> dict[str, object]:
    match = None
    for candidate in re.finditer(r"(\d+)\s*<=\s*rank(?:\(E\))?\s*<=\s*(\d+)", output):
        match = candidate
    if match is None:
        return {
            "rank_bounds": [],
            "rank_proved": False,
            "rank_zero_proof_candidate": False,
            "status": "rank-bounds-missing-not-proof",
        }
    lower = int(match.group(1))
    upper = int(match.group(2))
    rank_proved = lower == upper
    rank_zero_proof_candidate = rank_proved and lower == 0
    if rank_zero_proof_candidate:
        status = "rank-zero-proof-candidate"
    elif rank_proved:
        status = "rank-proved-nonzero-not-target"
    else:
        status = "open-rank-bounds-not-proof"
    return {
        "rank_bounds": [lower, upper],
        "rank_proved": rank_proved,
        "rank_zero_proof_candidate": rank_zero_proof_candidate,
        "status": status,
    }


def _run_mwrank(
    *,
    sage: str,
    mwrank_args: list[str],
    stdin_text: str,
    timeout_seconds: int,
) -> dict[str, object]:
    command = "mwrank " + " ".join(mwrank_args)
    try:
        result = subprocess.run(
            [sage, "-sh", "-c", command],
            input=stdin_text,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "status": "timeout",
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "returncode": None,
        }
    except OSError as exc:
        return {
            "status": "runtime-error",
            "stdout": "",
            "stderr": str(exc),
            "returncode": None,
        }
    return {
        "status": "ok" if result.returncode == 0 else "runtime-error",
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
    }


def _target(handoff: dict[str, Any]) -> dict[str, int | str]:
    return {
        "A": int(handoff.get("A", 0)),
        "B": int(handoff.get("B", 0)),
        "curve": str(handoff.get("curve", "")),
    }


def probe_from_handoff(
    *,
    handoff: dict[str, Any],
    sage: str,
    timeout_seconds: int,
    mwrank_args: list[str],
    runner: Runner | None = None,
) -> dict[str, Any]:
    model = handoff.get("weierstrass_model")
    if not isinstance(model, list) or len(model) != 5:
        return {
            "status": "invalid-input",
            "target": _target(handoff),
            "weierstrass_model": model if isinstance(model, list) else [],
            "mwrank_args": mwrank_args,
            "rank_bounds": [],
            "rank_proved": False,
            "rank_zero_proof_candidate": False,
            "proof_status": "invalid-input-not-proof",
            "stdout": "",
            "stderr": "handoff missing five-term weierstrass_model",
            "returncode": None,
            "boundary": BOUNDARY,
        }
    stdin_text = build_mwrank_stdin(handoff)
    run = runner or (
        lambda *, stdin_text, timeout_seconds: _run_mwrank(
            sage=sage,
            mwrank_args=mwrank_args,
            stdin_text=stdin_text,
            timeout_seconds=timeout_seconds,
        )
    )
    run_result = run(stdin_text=stdin_text, timeout_seconds=timeout_seconds)
    if run_result.get("status") != "ok":
        return {
            "status": run_result.get("status", "runtime-error"),
            "target": _target(handoff),
            "weierstrass_model": [int(value) for value in model],
            "mwrank_args": mwrank_args,
            "rank_bounds": [],
            "rank_proved": False,
            "rank_zero_proof_candidate": False,
            "proof_status": f"{run_result.get('status', 'runtime-error')}-not-proof",
            "stdout": str(run_result.get("stdout", "")),
            "stderr": str(run_result.get("stderr", "")),
            "returncode": run_result.get("returncode"),
            "boundary": BOUNDARY,
        }
    parsed = parse_mwrank_output(str(run_result.get("stdout", "")))
    return {
        "status": "ok",
        "target": _target(handoff),
        "weierstrass_model": [int(value) for value in model],
        "mwrank_args": mwrank_args,
        "rank_bounds": parsed["rank_bounds"],
        "rank_proved": parsed["rank_proved"],
        "rank_zero_proof_candidate": parsed["rank_zero_proof_candidate"],
        "proof_status": parsed["status"],
        "stdout": str(run_result.get("stdout", "")),
        "stderr": str(run_result.get("stderr", "")),
        "returncode": run_result.get("returncode"),
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--sage", default="sage")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument(
        "--mwrank-arg",
        action="append",
        default=None,
        help="Argument passed to mwrank. Repeat for multiple arguments.",
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    probe = probe_from_handoff(
        handoff=load_json(args.handoff),
        sage=args.sage,
        timeout_seconds=args.timeout,
        mwrank_args=resolve_mwrank_args(args.mwrank_arg),
    )
    write_json(args.out, probe)
    print(f"wrote mwrank mixed-closure rank probe to {args.out}")
    print(f"status={probe['status']}")
    print(f"proof_status={probe['proof_status']}")
    print(f"rank_zero_proof_candidate={probe['rank_zero_proof_candidate']}")
    if args.strict and probe["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
