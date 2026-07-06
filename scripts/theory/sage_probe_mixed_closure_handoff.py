#!/usr/bin/env python3
"""Run a bounded Sage probe for a mixed-closure residual handoff."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

Run = Callable[..., subprocess.CompletedProcess[str]]

MARKER = "SAGE_HANDOFF_PROBE_JSON "


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


def _sage_quartic(quartic: str) -> str:
    return quartic.replace("^", "**")


def _sage_program(
    handoff: dict[str, Any],
    *,
    point_search_bound: int,
    two_descent_second_limit: int | None,
) -> str:
    covers = [
        {"index": int(cover["index"]), "quartic": _sage_quartic(str(cover["quartic"]))}
        for cover in handoff.get("target_covers", [])
    ]
    two_descent_literal = (
        "None" if two_descent_second_limit is None else str(int(two_descent_second_limit))
    )
    return f"""
import json
from sage.all import EllipticCurve, HyperellipticCurve, PolynomialRing, QQ

model = {json.dumps(handoff["weierstrass_model"])}
covers = {json.dumps(covers)}
point_search_bound = {int(point_search_bound)}
two_descent_second_limit = {two_descent_literal}


def torsion_two_dimension(invariants):
    return sum(1 for value in invariants if int(value) % 2 == 0)


payload = {{}}
E = EllipticCurve(model)
bounds = E.rank_bounds()
payload["rank_bounds"] = [int(bounds[0]), int(bounds[1])]
try:
    payload["rank_proof"] = int(E.rank(proof=True))
    payload["rank_proof_status"] = "ok"
except Exception as exc:
    payload["rank_proof_status"] = "runtime-error"
    payload["rank_proof_error"] = str(exc).splitlines()[-1]

try:
    payload["rank_probable"] = int(E.rank(proof=False))
except Exception as exc:
    payload["rank_probable_error"] = str(exc).splitlines()[-1]

payload["selmer_rank"] = int(E.selmer_rank())
torsion = E.torsion_subgroup()
invariants = [int(value) for value in torsion.invariants()]
payload["torsion_invariants"] = invariants
payload["torsion_two_dimension"] = int(torsion_two_dimension(invariants))

if two_descent_second_limit is not None:
    try:
        result = E.two_descent(verbose=False, second_limit=int(two_descent_second_limit))
        payload["two_descent"] = {{
            "status": "ok",
            "result": bool(result),
            "second_limit": int(two_descent_second_limit),
        }}
    except Exception as exc:
        payload["two_descent"] = {{
            "status": "runtime-error",
            "error": str(exc).splitlines()[-1],
            "second_limit": int(two_descent_second_limit),
        }}

R = PolynomialRing(QQ, names=("x",))
x = R.gen()
cover_payloads = []
for cover in covers:
    f = R(cover["quartic"])
    C = HyperellipticCurve(f, R(0))
    try:
        points = C.rational_points(bound=point_search_bound)
        point_strings = [str(point) for point in points]
        point_status = "ok"
    except Exception as exc:
        point_strings = []
        point_status = "runtime-error"
        point_error = str(exc).splitlines()[-1]
    row = {{
        "index": int(cover["index"]),
        "genus": int(C.genus()),
        "point_search_bound": int(point_search_bound),
        "rational_point_count": len(point_strings),
        "rational_points": point_strings,
        "point_search_status": point_status,
    }}
    if point_status != "ok":
        row["point_search_error"] = point_error
    cover_payloads.append(row)
payload["covers"] = cover_payloads
print({MARKER!r} + json.dumps(payload, separators=(",", ":")), flush=True)
"""


def _parse_marker(stdout: str) -> dict[str, Any] | None:
    for line in stdout.splitlines():
        if line.startswith(MARKER):
            return json.loads(line[len(MARKER) :])
    return None


def _boundary() -> str:
    return (
        "This is a Sage probe of a residual handoff. A failed proof-rank "
        "attempt or bounded cover search is diagnostic evidence, not a "
        "proof that the cover has no rational point."
    )


def probe_handoff(
    handoff: dict[str, Any],
    *,
    sage_executable: str,
    timeout_seconds: int,
    point_search_bound: int,
    two_descent_second_limit: int | None,
    run: Run = subprocess.run,
    dot_sage: Path | None = None,
) -> dict[str, Any]:
    env = os.environ.copy()
    if dot_sage is not None:
        env["DOT_SAGE"] = str(dot_sage)

    cmd = [
        sage_executable,
        "-python",
        "-c",
        _sage_program(
            handoff,
            point_search_bound=point_search_bound,
            two_descent_second_limit=two_descent_second_limit,
        ),
    ]
    base = {
        "A": int(handoff["A"]),
        "B": int(handoff["B"]),
        "curve": str(handoff["curve"]),
    }
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
            **base,
            "status": "timeout",
            "timeout_seconds": timeout_seconds,
            "stdout_tail": _tail_lines(exc.stdout),
            "stderr_tail": _tail_lines(exc.stderr),
            "boundary": _boundary(),
        }

    marker = _parse_marker(completed.stdout)
    result: dict[str, Any] = {
        **base,
        "status": "ok" if completed.returncode == 0 and marker is not None else "sage-error",
        "stdout_tail": _tail_lines(completed.stdout),
        "stderr_tail": _tail_lines(completed.stderr),
        "boundary": _boundary(),
    }
    if marker is not None:
        result["sage"] = marker
    else:
        result["error"] = "Sage marker not found"
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--sage", default="sage")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--point-search-bound", type=int, default=100)
    parser.add_argument("--two-descent-second-limit", type=int, default=None)
    parser.add_argument(
        "--dot-sage",
        type=Path,
        default=Path("/private/tmp/d19-dot-sage"),
        help="Writable DOT_SAGE directory for sandboxed Sage runs.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = probe_handoff(
        load_json(args.handoff),
        sage_executable=args.sage,
        timeout_seconds=args.timeout,
        point_search_bound=args.point_search_bound,
        two_descent_second_limit=args.two_descent_second_limit,
        dot_sage=args.dot_sage,
    )
    write_json(args.out, result)
    print(f"wrote Sage handoff probe to {args.out}")
    print(f"status={result['status']}")
    if result["status"] == "ok" and "sage" in result:
        sage = result["sage"]
        print(f"rank_bounds={sage.get('rank_bounds')}")
        print(f"rank_proof_status={sage.get('rank_proof_status')}")
        cover_point_counts = [
            row.get("rational_point_count") for row in sage.get("covers", [])
        ]
        print(f"cover_point_counts={cover_point_counts}")
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
