#!/usr/bin/env python3
"""Audit torsion preimages for rank-zero residual cover candidates."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

Run = Callable[..., subprocess.CompletedProcess[str]]

MARKER = "SAGE_RANK0_TORSION_PREIMAGE_JSON "


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _row_key(row: dict[str, Any]) -> tuple[int, int, str]:
    return int(row["A"]), int(row["B"]), str(row["curve"])


def build_rank0_torsion_targets(
    *,
    cover_rows: list[dict[str, Any]],
    selmer_gap_ledger: dict[str, Any],
    gap_type: str,
) -> list[dict[str, Any]]:
    cover_rows_by_key = {_row_key(row): row for row in cover_rows}
    targets: list[dict[str, Any]] = []
    for ledger_row in selmer_gap_ledger.get("rows", []):
        if str(ledger_row.get("gap_type", "")) != gap_type:
            continue
        cover_row = cover_rows_by_key[_row_key(ledger_row)]
        covers_by_index = {
            int(cover["index"]): cover for cover in cover_row.get("covers", [])
        }
        cover_index = int(ledger_row["cover_index"])
        cover = covers_by_index[cover_index]
        targets.append(
            {
                "A": int(ledger_row["A"]),
                "B": int(ledger_row["B"]),
                "curve": str(ledger_row["curve"]),
                "weierstrass_model": cover_row["model"],
                "cover_index": cover_index,
                "quartic": str(cover["quartic"]),
                "covering_map_to_elliptic": str(
                    cover.get("covering_map_to_elliptic", "")
                ),
                "gap_type": str(ledger_row["gap_type"]),
            }
        )
    return targets


def _tail_lines(text: str | bytes | None, *, limit: int = 20) -> list[str]:
    if text is None:
        return []
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="replace")
    return text.splitlines()[-limit:]


def _sage_expr(raw: str) -> str:
    return raw.replace("^", "**")


def _sage_program(targets: list[dict[str, Any]]) -> str:
    sage_targets = [
        {
            **target,
            "quartic": _sage_expr(str(target["quartic"])),
            "covering_map_to_elliptic": _sage_expr(
                str(target["covering_map_to_elliptic"])
            ),
        }
        for target in targets
    ]
    return f"""
import json
from sage.all import EllipticCurve, PolynomialRing, QQ

targets = {json.dumps(sage_targets)}

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


def candidate_polynomial(frac, f):
    even, odd = reduce_mod_cover_relation(frac.numerator(), f)
    if odd == 0:
        return even
    if even == 0:
        return f * odd**2
    return even**2 - f * odd**2


def rational_y_values(value):
    value = QQ(value)
    if value < 0 or not value.is_square():
        return []
    root = value.sqrt()
    if root == 0:
        return [root]
    return [root, -root]


def finite_torsion_points(E):
    rows = []
    for point in E.torsion_points():
        if point[2] == 0:
            continue
        rows.append([str(QQ(point[0] / point[2])), str(QQ(point[1] / point[2]))])
    return rows


def audit_target(target):
    row = {{
        "A": int(target["A"]),
        "B": int(target["B"]),
        "curve": str(target["curve"]),
        "cover_index": int(target["cover_index"]),
        "gap_type": str(target["gap_type"]),
    }}
    try:
        f = parse_quartic(target["quartic"])
        X, Y = parse_map(target["covering_map_to_elliptic"])
        E = EllipticCurve(target["weierstrass_model"])
        leading = QQ(f.leading_coefficient())
        branch_roots = f.roots(QQ)
        torsion_preimages = []
        torsion_checks = []
        for x_raw, y_raw in finite_torsion_points(E):
            x0 = QQ(x_raw)
            y0 = QQ(y_raw)
            H = candidate_polynomial(X - K(x0), f)
            roots = [] if H == 0 else H.roots(QQ)
            hits = []
            for x_candidate, _multiplicity in roots:
                for y_candidate in rational_y_values(f(x_candidate)):
                    try:
                        if X(x=x_candidate, y=y_candidate) == x0 and Y(
                            x=x_candidate, y=y_candidate
                        ) == y0:
                            hit = [str(QQ(x_candidate)), str(QQ(y_candidate))]
                            hits.append(hit)
                            torsion_preimages.append(
                                {{"torsion_point": [x_raw, y_raw], "cover_point": hit}}
                            )
                    except Exception:
                        pass
            torsion_checks.append(
                {{
                    "torsion_point": [x_raw, y_raw],
                    "candidate_x_root_count": len(roots),
                    "preimage_count": len(hits),
                }}
            )
        row.update(
            {{
                "status": "ok",
                "has_rational_infinity": bool(leading.is_square()),
                "rational_branch_point_count": len(branch_roots),
                "finite_torsion_point_count": len(torsion_checks),
                "torsion_checks": torsion_checks,
                "torsion_preimage_count": len(torsion_preimages),
                "torsion_preimages": torsion_preimages,
                "no_torsion_preimage": bool(
                    not leading.is_square()
                    and len(branch_roots) == 0
                    and len(torsion_preimages) == 0
                ),
            }}
        )
    except Exception as exc:
        row.update(
            {{
                "status": "runtime-error",
                "error": str(exc).splitlines()[-1],
                "no_torsion_preimage": False,
            }}
        )
    return row


cover_rows = [audit_target(target) for target in targets]
payload = {{
    "target_cover_count": len(cover_rows),
    "no_torsion_preimage_count": sum(
        1 for row in cover_rows if row.get("no_torsion_preimage") is True
    ),
    "failed_cover_count": sum(
        1 for row in cover_rows if row.get("no_torsion_preimage") is not True
    ),
    "all_no_torsion_preimages": bool(
        cover_rows and all(row.get("no_torsion_preimage") is True for row in cover_rows)
    ),
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
        "This checks torsion preimages on residual covers conditional on "
        "the associated elliptic curve having rank zero. It is not an "
        "unconditional no-point proof."
    )


def audit_rank0_torsion_preimages(
    *,
    cover_rows: list[dict[str, Any]],
    selmer_gap_ledger: dict[str, Any],
    gap_type: str,
    sage_executable: str,
    timeout_seconds: int,
    run: Run = subprocess.run,
    dot_sage: Path | None = None,
) -> dict[str, Any]:
    targets = build_rank0_torsion_targets(
        cover_rows=cover_rows,
        selmer_gap_ledger=selmer_gap_ledger,
        gap_type=gap_type,
    )
    env = os.environ.copy()
    if dot_sage is not None:
        env["DOT_SAGE"] = str(dot_sage)

    cmd = [sage_executable, "-python", "-c", _sage_program(targets)]
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
            "status": "timeout",
            "gap_type": gap_type,
            "target_cover_count": len(targets),
            "timeout_seconds": timeout_seconds,
            "stdout_tail": _tail_lines(exc.stdout),
            "stderr_tail": _tail_lines(exc.stderr),
            "boundary": _boundary(),
        }

    marker = _parse_marker(completed.stdout)
    result: dict[str, Any] = {
        "status": "ok"
        if completed.returncode == 0
        and marker is not None
        and marker.get("all_no_torsion_preimages") is True
        else "sage-error",
        "gap_type": gap_type,
        "target_cover_count": len(targets),
        "stdout_tail": _tail_lines(completed.stdout),
        "stderr_tail": _tail_lines(completed.stderr),
        "boundary": _boundary(),
    }
    if marker is not None:
        result.update(
            {
                "all_no_torsion_preimages": bool(
                    marker.get("all_no_torsion_preimages", False)
                ),
                "no_torsion_preimage_count": int(
                    marker.get("no_torsion_preimage_count", 0)
                ),
                "failed_cover_count": int(marker.get("failed_cover_count", 0)),
                "sage": marker,
            }
        )
    else:
        result.update(
            {
                "all_no_torsion_preimages": False,
                "no_torsion_preimage_count": 0,
                "failed_cover_count": len(targets),
                "error": "Sage marker not found",
            }
        )
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--covers", type=Path, required=True)
    parser.add_argument("--selmer-gap-ledger", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--gap-type", default="rank0-sha2-gap2")
    parser.add_argument("--sage", default="sage")
    parser.add_argument("--timeout", type=int, default=120)
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
    result = audit_rank0_torsion_preimages(
        cover_rows=load_jsonl(args.covers),
        selmer_gap_ledger=load_json(args.selmer_gap_ledger),
        gap_type=args.gap_type,
        sage_executable=args.sage,
        timeout_seconds=args.timeout,
        dot_sage=args.dot_sage,
    )
    write_json(args.out, result)
    print(f"wrote rank-zero torsion preimage audit to {args.out}")
    print(f"status={result['status']}")
    print(f"target_cover_count={result['target_cover_count']}")
    print(f"all_no_torsion_preimages={result['all_no_torsion_preimages']}")
    if args.strict and result["status"] != "ok":
        return 1
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
