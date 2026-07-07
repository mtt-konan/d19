#!/usr/bin/env python3
"""Probe Sage rank methods separately for a mixed-closure handoff."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any

Run = Callable[..., subprocess.CompletedProcess[str]]

MARKER = "SAGE_RANK_METHOD_JSON "
DEFAULT_METHODS = (
    "rank_bounds",
    "rank_proof",
    "selmer_rank",
    "pari_ellrank",
    "two_descent",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _tail_lines(text: str | bytes | None, *, limit: int = 20) -> list[str]:
    if text is None:
        return []
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="replace")
    return text.splitlines()[-limit:]


def _parse_marker(stdout: str) -> dict[str, Any] | None:
    for line in stdout.splitlines():
        if line.startswith(MARKER):
            return json.loads(line[len(MARKER) :])
    return None


def _boundary() -> str:
    return (
        "This probes Sage rank methods separately. Timeouts, runtime errors, "
        "open rank bounds, and bounded method limits are not proofs."
    )


def _sage_method_program(
    *,
    model: list[int],
    method: str,
    two_descent_second_limit: int | None,
) -> str:
    limit_literal = (
        "None"
        if two_descent_second_limit is None
        else str(int(two_descent_second_limit))
    )
    return f"""
import json
from sage.all import EllipticCurve, pari

model = {json.dumps(model)}
method = {json.dumps(method)}
two_descent_second_limit = {limit_literal}

E = EllipticCurve(model)
payload = {{"status": "ok"}}
try:
    if method == "rank_bounds":
        bounds = E.rank_bounds()
        payload["rank_bounds"] = [int(bounds[0]), int(bounds[1])]
    elif method == "rank_proof":
        payload["rank"] = int(E.rank(proof=True))
    elif method == "rank_probable":
        payload["rank"] = int(E.rank(proof=False))
    elif method == "selmer_rank":
        payload["selmer_rank"] = int(E.selmer_rank())
    elif method == "pari_ellrank":
        pari_curve = pari("ellinit")(model)
        ellrank = pari('ellrank')(pari_curve)
        values = [ellrank[i] for i in range(len(ellrank))]
        payload["ellrank"] = [str(value) for value in values]
        payload["rank_bounds"] = [int(values[0]), int(values[1])]
        payload["sha2_lower"] = int(values[2])
    elif method == "two_descent":
        if two_descent_second_limit is None:
            result = E.two_descent(verbose=False)
            payload["second_limit"] = None
        else:
            result = E.two_descent(
                verbose=False,
                second_limit=int(two_descent_second_limit),
            )
            payload["second_limit"] = int(two_descent_second_limit)
        payload["result"] = bool(result)
    else:
        payload["status"] = "unknown-method"
        payload["method"] = method
except Exception as exc:
    payload = {{
        "status": "runtime-error",
        "error": str(exc).splitlines()[-1],
    }}
print({MARKER!r} + json.dumps(payload, separators=(",", ":")), flush=True)
"""


def _method_result(
    *,
    handoff: dict[str, Any],
    method: str,
    sage_executable: str,
    timeout_seconds: int,
    two_descent_second_limit: int | None,
    run: Run,
    env: dict[str, str],
) -> dict[str, Any]:
    cmd = [
        sage_executable,
        "-python",
        "-c",
        _sage_method_program(
            model=[int(value) for value in handoff["weierstrass_model"]],
            method=method,
            two_descent_second_limit=two_descent_second_limit,
        ),
    ]
    try:
        completed = run(
            cmd,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
            env=env,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "method": method,
            "status": "timeout",
            "timeout_seconds": timeout_seconds,
            "stdout_tail": _tail_lines(exc.stdout),
            "stderr_tail": _tail_lines(exc.stderr),
        }

    marker = _parse_marker(completed.stdout)
    if completed.returncode != 0 or marker is None:
        return {
            "method": method,
            "status": "sage-error",
            "returncode": int(completed.returncode),
            "stdout_tail": _tail_lines(completed.stdout),
            "stderr_tail": _tail_lines(completed.stderr),
        }
    return {"method": method, **marker}


def _rank_zero_proof_candidate(method_results: list[dict[str, Any]]) -> bool:
    return any(
        result.get("method") == "rank_proof"
        and result.get("status") == "ok"
        and int(result.get("rank", -1)) == 0
        for result in method_results
    )


def probe_rank_methods(
    handoff: dict[str, Any],
    *,
    methods: list[str],
    sage_executable: str,
    timeout_seconds: int,
    two_descent_second_limit: int | None,
    run: Run = subprocess.run,
    dot_sage: Path | None = None,
) -> dict[str, Any]:
    env = os.environ.copy()
    if dot_sage is not None:
        env["DOT_SAGE"] = str(dot_sage)

    method_results = [
        _method_result(
            handoff=handoff,
            method=method,
            sage_executable=sage_executable,
            timeout_seconds=timeout_seconds,
            two_descent_second_limit=two_descent_second_limit,
            run=run,
            env=env,
        )
        for method in methods
    ]
    return {
        "A": int(handoff["A"]),
        "B": int(handoff["B"]),
        "curve": str(handoff["curve"]),
        "status": "ok",
        "timeout_seconds": int(timeout_seconds),
        "method_status_counts": dict(
            sorted(
                Counter(
                    f"{result.get('method')}:{result.get('status')}"
                    for result in method_results
                ).items()
            )
        ),
        "method_results": method_results,
        "rank_zero_proof_candidate": _rank_zero_proof_candidate(method_results),
        "boundary": _boundary(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--sage", default="sage")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--method", action="append", default=[])
    parser.add_argument("--two-descent-second-limit", type=int, default=None)
    parser.add_argument(
        "--dot-sage",
        type=Path,
        default=Path("/private/tmp/d19-dot-sage"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = probe_rank_methods(
        load_json(args.handoff),
        methods=list(args.method or DEFAULT_METHODS),
        sage_executable=args.sage,
        timeout_seconds=args.timeout,
        two_descent_second_limit=args.two_descent_second_limit,
        dot_sage=args.dot_sage,
    )
    write_json(args.out, result)
    print(f"wrote Sage rank-method probe to {args.out}")
    print(f"status={result['status']}")
    print(f"method_status_counts={result['method_status_counts']}")
    print(f"rank_zero_proof_candidate={result['rank_zero_proof_candidate']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
