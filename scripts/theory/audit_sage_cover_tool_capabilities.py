#!/usr/bin/env python3
"""Audit Sage cover-level capabilities for residual genus-one quartics."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits Sage cover-level tool availability. Missing direct interfaces "
    "and bounded point searches are not no-point proofs."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _target(handoff: dict[str, Any]) -> dict[str, int | str]:
    return {
        "A": int(handoff.get("A", 0)),
        "B": int(handoff.get("B", 0)),
        "curve": str(handoff.get("curve", "")),
    }


def _sage_probe_script(handoff: dict[str, Any], out: Path) -> str:
    covers = [
        {"index": int(cover["index"]), "quartic": str(cover["quartic"])}
        for cover in handoff.get("target_covers", [])
    ]
    covers_json = json.dumps(covers)
    out_text = str(out)
    return f"""
from sage.all import *
import json

R = PolynomialRing(QQ, names=('x',))
x = R.gen()
covers = json.loads({covers_json!r})
rows = []
for cover in covers:
    f = R(cover["quartic"].replace("^", "**"))
    C = HyperellipticCurve(f, R(0))
    J = C.jacobian()
    rows.append({{
        "index": int(cover["index"]),
        "genus": int(C.genus()),
        "has_rational_points_method": hasattr(C, "rational_points"),
        "has_local_points_method": hasattr(C, "local_points"),
        "has_is_locally_solvable_method": hasattr(C, "is_locally_solvable"),
        "has_two_cover_descent_method": hasattr(C, "two_cover_descent"),
        "jacobian_has_rank_method": hasattr(J, "rank"),
        "jacobian_has_gens_method": hasattr(J, "gens"),
        "jacobian_has_elliptic_curve_method": hasattr(J, "elliptic_curve"),
    }})

Path = __import__("pathlib").Path
Path({out_text!r}).write_text(json.dumps({{"status": "ok", "covers": rows}}, sort_keys=True))
"""


def run_sage_probe(
    *,
    handoff: dict[str, Any],
    sage: str,
    timeout_seconds: int,
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="d19-cover-cap-") as tmp:
        tmp_path = Path(tmp)
        script = tmp_path / "probe.sage"
        out = tmp_path / "probe.json"
        script.write_text(_sage_probe_script(handoff, out), encoding="utf-8")
        try:
            result = subprocess.run(
                [sage, str(script)],
                text=True,
                capture_output=True,
                timeout=timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            return {
                "status": "timeout",
                "covers": [],
                "stdout": exc.stdout or "",
                "stderr": exc.stderr or "",
            }
        except OSError as exc:
            return {"status": "runtime-error", "covers": [], "stderr": str(exc)}
        if result.returncode != 0:
            return {
                "status": "runtime-error",
                "covers": [],
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        return json.loads(out.read_text(encoding="utf-8"))


def _cover_summary(row: dict[str, Any]) -> dict[str, Any]:
    has_local = bool(row.get("has_local_points_method")) or bool(
        row.get("has_is_locally_solvable_method")
    )
    has_two_cover_descent = bool(row.get("has_two_cover_descent_method"))
    return {
        "index": int(row.get("index", 0)),
        "genus": int(row.get("genus", -1)),
        "has_bounded_rational_points_method": bool(
            row.get("has_rational_points_method")
        ),
        "has_direct_local_solubility_method": has_local,
        "has_direct_two_cover_descent_method": has_two_cover_descent,
        "jacobian_has_rank_method": bool(row.get("jacobian_has_rank_method")),
        "jacobian_has_gens_method": bool(row.get("jacobian_has_gens_method")),
        "jacobian_has_elliptic_curve_method": bool(
            row.get("jacobian_has_elliptic_curve_method")
        ),
        "strict_certificate_ready": False,
        "proof_status": "sage-interface-not-proof",
    }


def audit_cover_capabilities(
    *,
    handoff: dict[str, Any],
    sage_probe: dict[str, Any],
) -> dict[str, Any]:
    if sage_probe.get("status") != "ok":
        return {
            "status": "issues",
            "ready": False,
            "target": _target(handoff),
            "cover_count": len(handoff.get("target_covers", [])),
            "genus_one_cover_count": 0,
            "sage_direct_no_point_capable_count": 0,
            "strict_certificate_ready_count": 0,
            "recommended_next_tool": "magma-or-specialized-cover-descent",
            "covers": [],
            "boundary": BOUNDARY,
        }
    covers = [_cover_summary(row) for row in sage_probe.get("covers", [])]
    direct_capable = [
        cover
        for cover in covers
        if cover["has_direct_local_solubility_method"]
        and cover["has_direct_two_cover_descent_method"]
    ]
    return {
        "status": "ok",
        "ready": True,
        "target": _target(handoff),
        "cover_count": len(covers),
        "genus_one_cover_count": sum(1 for cover in covers if cover["genus"] == 1),
        "sage_direct_no_point_capable_count": len(direct_capable),
        "strict_certificate_ready_count": 0,
        "recommended_next_tool": "magma-or-specialized-cover-descent",
        "covers": covers,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--sage", default="sage")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.handoff.is_file():
        audit = {
            "status": "issues",
            "ready": False,
            "target": {"A": 0, "B": 0, "curve": ""},
            "cover_count": 0,
            "genus_one_cover_count": 0,
            "sage_direct_no_point_capable_count": 0,
            "strict_certificate_ready_count": 0,
            "recommended_next_tool": "magma-or-specialized-cover-descent",
            "covers": [],
            "boundary": BOUNDARY,
        }
        write_json(args.out, audit)
        print(f"wrote Sage cover capability audit to {args.out}")
        print(f"status={audit['status']}")
        return 1 if args.strict else 0
    handoff = load_json(args.handoff)
    audit = audit_cover_capabilities(
        handoff=handoff,
        sage_probe=run_sage_probe(
            handoff=handoff,
            sage=args.sage,
            timeout_seconds=args.timeout,
        ),
    )
    write_json(args.out, audit)
    print(f"wrote Sage cover capability audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"cover_count={audit['cover_count']}")
    print(
        "sage_direct_no_point_capable_count="
        f"{audit['sage_direct_no_point_capable_count']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
