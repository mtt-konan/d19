#!/usr/bin/env python3
"""Search for explicit Qp local witnesses on residual cover quartics."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

Run = Callable[..., subprocess.CompletedProcess[str]]

MARKER = "SAGE_LOCAL_WITNESS_JSON "


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


def _sage_program(
    handoff: dict[str, Any],
    *,
    search_bound: int,
    max_denominator_power: int,
) -> str:
    covers = [
        {
            "index": int(cover["index"]),
            **{
                key: cover[key]
                for key in ("priority", "A", "B", "curve", "cover_index")
                if key in cover
            },
            "quartic": _sage_expr(str(cover["quartic"])),
        }
        for cover in handoff.get("target_covers", [])
    ]
    return f"""
import json
from sage.all import GF, PolynomialRing, QQ, ZZ, factor, inverse_mod, kronecker

covers = {json.dumps(covers)}
search_bound = {int(search_bound)}
max_denominator_power = {int(max_denominator_power)}

R = PolynomialRing(QQ, names=("x",))
x = R.gen()
Rx = PolynomialRing(QQ, names=("x",))
u = Rx.gen()
env_x = {{"x": u}}


def parse_quartic(raw):
    return R(eval(raw, {{"__builtins__": {{}}}}, env_x))


def bad_primes_for_quartic(f):
    bad = {{2}}
    lc = ZZ(f.leading_coefficient())
    disc = ZZ(f.discriminant())
    for prime, _exp in factor(abs(lc)):
        bad.add(int(prime))
    for prime, _exp in factor(abs(disc)):
        bad.add(int(prime))
    return sorted(bad)


def is_qp_square(value, p):
    value = QQ(value)
    if value == 0:
        return True
    valuation = int(value.valuation(p))
    if valuation % 2:
        return False
    unit = value / (QQ(p) ** valuation)
    numerator = ZZ(unit.numerator())
    denominator = ZZ(unit.denominator())
    if p == 2:
        return (numerator * inverse_mod(denominator, 8)) % 8 == 1
    unit_mod_p = (numerator % p) * inverse_mod(denominator % p, p) % p
    return kronecker(unit_mod_p, p) == 1


def find_witness(f, p):
    lc = QQ(f.leading_coefficient())
    if is_qp_square(lc, p):
        return {{"p": int(p), "status": "ok", "kind": "infinity"}}
    for exponent in range(max_denominator_power + 1):
        denominator = QQ(p) ** exponent
        for numerator in range(-search_bound, search_bound + 1):
            if exponent > 0 and numerator % p == 0:
                continue
            x_value = QQ(numerator) / denominator
            f_value = f(x_value)
            if is_qp_square(f_value, p):
                return {{
                    "p": int(p),
                    "status": "ok",
                    "kind": "finite",
                    "x": str(x_value),
                    "f_x": str(f_value),
                    "denominator_power": int(exponent),
                }}
    return {{
        "p": int(p),
        "status": "unresolved",
        "kind": "none-found",
        "search_bound": int(search_bound),
        "max_denominator_power": int(max_denominator_power),
    }}


def cover_row(cover):
    f = parse_quartic(cover["quartic"])
    bad_primes = bad_primes_for_quartic(f)
    witnesses = [find_witness(f, p) for p in bad_primes]
    row = {{
        "index": int(cover["index"]),
        "bad_primes": bad_primes,
        "witnesses": witnesses,
        "all_witnessed": all(row["status"] == "ok" for row in witnesses),
    }}
    for key in ("priority", "A", "B", "curve", "cover_index"):
        if key in cover:
            row[key] = cover[key]
    return row


cover_rows = [cover_row(cover) for cover in covers]
payload = {{
    "all_bad_primes_witnessed": bool(
        cover_rows and all(row["all_witnessed"] for row in cover_rows)
    ),
    "covers": cover_rows,
    "search_bound": int(search_bound),
    "max_denominator_power": int(max_denominator_power),
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
        "This searches for explicit Qp local witnesses at the bad primes of "
        "stored residual covers. It does not prove that any residual cover "
        "has no rational point."
    )


def probe_local_witnesses(
    handoff: dict[str, Any],
    *,
    sage_executable: str,
    timeout_seconds: int,
    search_bound: int,
    max_denominator_power: int,
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
            search_bound=search_bound,
            max_denominator_power=max_denominator_power,
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


def priority_rows_to_handoff(priorities: dict[str, Any]) -> dict[str, Any]:
    return {
        "A": 0,
        "B": 0,
        "curve": "priority-table",
        "target_covers": [
            {
                "index": int(row["priority"]),
                "priority": int(row["priority"]),
                "A": int(row["A"]),
                "B": int(row["B"]),
                "curve": str(row["curve"]),
                "cover_index": int(row["cover_index"]),
                "quartic": str(row["quartic"]),
            }
            for row in priorities.get("rows", [])
        ],
    }


def _bad_prime_totals(sage_payload: dict[str, Any]) -> tuple[int, int]:
    total = 0
    unresolved = 0
    for cover in sage_payload.get("covers", []):
        witnesses = cover.get("witnesses", [])
        total += len(witnesses)
        unresolved += sum(1 for witness in witnesses if witness.get("status") != "ok")
    return total, unresolved


def probe_priority_local_witnesses(
    priorities: dict[str, Any],
    *,
    sage_executable: str,
    timeout_seconds: int,
    search_bound: int,
    max_denominator_power: int,
    run: Run = subprocess.run,
    dot_sage: Path | None = None,
) -> dict[str, Any]:
    result = probe_local_witnesses(
        priority_rows_to_handoff(priorities),
        sage_executable=sage_executable,
        timeout_seconds=timeout_seconds,
        search_bound=search_bound,
        max_denominator_power=max_denominator_power,
        run=run,
        dot_sage=dot_sage,
    )
    candidate_cover_total = len(priorities.get("rows", []))
    result["candidate_cover_total"] = candidate_cover_total
    if "sage" in result:
        bad_prime_total, unresolved_total = _bad_prime_totals(result["sage"])
        result["bad_prime_check_total"] = bad_prime_total
        result["unresolved_bad_prime_total"] = unresolved_total
    else:
        result["bad_prime_check_total"] = 0
        result["unresolved_bad_prime_total"] = candidate_cover_total
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--handoff", type=Path)
    input_group.add_argument("--priorities", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--sage", default="sage")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--search-bound", type=int, default=300)
    parser.add_argument("--max-denominator-power", type=int, default=3)
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
    if args.priorities is not None:
        result = probe_priority_local_witnesses(
            load_json(args.priorities),
            sage_executable=args.sage,
            timeout_seconds=args.timeout,
            search_bound=args.search_bound,
            max_denominator_power=args.max_denominator_power,
            dot_sage=args.dot_sage,
        )
    else:
        result = probe_local_witnesses(
            load_json(args.handoff),
            sage_executable=args.sage,
            timeout_seconds=args.timeout,
            search_bound=args.search_bound,
            max_denominator_power=args.max_denominator_power,
            dot_sage=args.dot_sage,
        )
    write_json(args.out, result)
    print(f"wrote Sage local witness probe to {args.out}")
    print(f"status={result['status']}")
    all_witnessed = bool(result.get("sage", {}).get("all_bad_primes_witnessed", False))
    print(f"all_bad_primes_witnessed={all_witnessed}")
    if "candidate_cover_total" in result:
        print(f"candidate_cover_total={result['candidate_cover_total']}")
        print(f"bad_prime_check_total={result['bad_prime_check_total']}")
        print(f"unresolved_bad_prime_total={result['unresolved_bad_prime_total']}")
    if args.strict and not (result["status"] == "ok" and all_witnessed):
        return 1
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
