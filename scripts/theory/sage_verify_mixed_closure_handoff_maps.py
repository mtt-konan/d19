#!/usr/bin/env python3
"""Verify stored mixed-closure cover-to-elliptic maps with Sage."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

Run = Callable[..., subprocess.CompletedProcess[str]]

MARKER = "SAGE_HANDOFF_MAP_VERIFY_JSON "


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


def _sage_expr(raw: str) -> str:
    return raw.replace("^", "**")


def _sage_program(handoff: dict[str, Any]) -> str:
    covers = [
        {
            "index": int(cover["index"]),
            "quartic": _sage_expr(str(cover["quartic"])),
            "covering_map_to_elliptic": _sage_expr(
                str(cover.get("covering_map_to_elliptic", ""))
            ),
        }
        for cover in handoff.get("target_covers", [])
    ]
    return f"""
import json
from sage.all import PolynomialRing, QQ

model = {json.dumps(handoff["weierstrass_model"])}
covers = {json.dumps(covers)}

Rxy = PolynomialRing(QQ, names=("x", "y"))
x, y = Rxy.gens()
K = Rxy.fraction_field()
Kx = K(x)
Ky = K(y)
Rx = PolynomialRing(QQ, names=("x",))
u = Rx.gen()
env_xy = {{"x": Kx, "y": Ky}}
env_x = {{"x": u}}


def parse_map(raw):
    value = eval(raw, {{"__builtins__": {{}}}}, env_xy)
    if len(value) != 2:
        raise ValueError("covering map must have two coordinates")
    return K(value[0]), K(value[1])


def parse_quartic(raw):
    return Rx(eval(raw, {{"__builtins__": {{}}}}, env_x))


def reduce_mod_cover_relation(poly, f):
    # Reduce modulo the cover relation y^2 = f(x).
    poly = Rxy(poly)
    even = Rx(0)
    odd = Rx(0)
    for exponents, coeff in poly.dict().items():
        x_power, y_power = exponents
        term = Rx(coeff) * (u ** int(x_power)) * (f ** int(y_power // 2))
        if int(y_power) % 2 == 0:
            even += term
        else:
            odd += term
    return even, odd


def verify_cover(cover):
    row = {{"index": int(cover["index"])}}
    try:
        f = parse_quartic(cover["quartic"])
        X, Y = parse_map(cover["covering_map_to_elliptic"])
        a1, a2, a3, a4, a6 = [QQ(value) for value in model]
        residual = Y**2 + a1*X*Y + a3*Y - (X**3 + a2*X**2 + a4*X + a6)
        numerator = residual.numerator()
        even, odd = reduce_mod_cover_relation(numerator, f)
        row.update(
            {{
                "map_parse_status": "ok",
                "identity_verified": bool(even == 0 and odd == 0),
                "residual_even_degree": int(even.degree()) if even != 0 else -1,
                "residual_odd_degree": int(odd.degree()) if odd != 0 else -1,
            }}
        )
    except Exception as exc:
        row.update(
            {{
                "map_parse_status": "runtime-error",
                "identity_verified": False,
                "error": str(exc).splitlines()[-1],
            }}
        )
    return row


cover_rows = [verify_cover(cover) for cover in covers]
payload = {{
    "all_verified": bool(cover_rows and all(row["identity_verified"] for row in cover_rows)),
    "covers": cover_rows,
}}
print({MARKER!r} + json.dumps(payload, separators=(",", ":")), flush=True)
"""


def _parse_marker(stdout: str) -> dict[str, Any] | None:
    for line in stdout.splitlines():
        if line.startswith(MARKER):
            return json.loads(line[len(MARKER) :])
    return None


def _boundary() -> str:
    return (
        "This verifies stored cover-to-elliptic rational maps against the "
        "Weierstrass equation. It does not prove that any residual cover has "
        "no rational point."
    )


def verify_handoff_maps(
    handoff: dict[str, Any],
    *,
    sage_executable: str,
    timeout_seconds: int,
    run: Run = subprocess.run,
    dot_sage: Path | None = None,
) -> dict[str, Any]:
    env = os.environ.copy()
    if dot_sage is not None:
        env["DOT_SAGE"] = str(dot_sage)

    cmd = [sage_executable, "-python", "-c", _sage_program(handoff)]
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
    parser.add_argument(
        "--dot-sage",
        type=Path,
        default=Path("/private/tmp/d19-dot-sage"),
        help="Writable DOT_SAGE directory for sandboxed Sage runs.",
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = verify_handoff_maps(
        load_json(args.handoff),
        sage_executable=args.sage,
        timeout_seconds=args.timeout,
        dot_sage=args.dot_sage,
    )
    write_json(args.out, result)
    print(f"wrote Sage handoff map verification to {args.out}")
    print(f"status={result['status']}")
    all_verified = bool(result.get("sage", {}).get("all_verified", False))
    print(f"all_verified={all_verified}")
    if args.strict and not (result["status"] == "ok" and all_verified):
        return 1
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
