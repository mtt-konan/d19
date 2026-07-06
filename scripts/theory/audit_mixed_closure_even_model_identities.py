#!/usr/bin/env python3
"""Symbolically audit the AA/BB centered even model identities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import sympy as sp


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _centered_even_quartic_verified() -> bool:
    s, leg, t = sp.symbols("s leg t")
    n = (s + t) / 2
    p = 8 * leg**2 - 2 * s**2
    q = (s**2 + 4 * leg**2) ** 2
    left = 16 * (n**2 + leg**2) * ((s - n) ** 2 + leg**2)
    right = t**4 + p * t**2 + q
    return sp.simplify(left - right) == 0


def _quartic_to_elliptic_verified() -> bool:
    t, z, p, q = sp.symbols("t z p q")
    x_coord = 2 * (z + t**2)
    v_coord = 2 * t * (x_coord + p)
    elliptic = v_coord**2 - (
        x_coord**3 + p * x_coord**2 - 4 * q * x_coord - 4 * p * q
    )
    quartic_relation = z**2 - (t**4 + p * t**2 + q)
    _, remainder = sp.groebner([quartic_relation], z, t, p, q).reduce(
        sp.expand(elliptic)
    )
    return sp.simplify(remainder) == 0


def _elliptic_to_quartic_inverse_verified() -> bool:
    x_coord, v_coord, p, q = sp.symbols("x_coord v_coord p q")
    t = v_coord / (2 * (x_coord + p))
    z = x_coord / 2 - t**2
    quartic = z**2 - (t**4 + p * t**2 + q)
    elliptic_relation = v_coord**2 - (
        x_coord**3 + p * x_coord**2 - 4 * q * x_coord - 4 * p * q
    )
    numerator = sp.together(quartic).as_numer_denom()[0]
    _, remainder = sp.groebner([elliptic_relation], v_coord, x_coord, p, q).reduce(
        sp.expand(numerator)
    )
    return sp.simplify(remainder) == 0


def audit_identities() -> dict[str, Any]:
    identities = [
        {
            "name": "centered_even_quartic",
            "verified": _centered_even_quartic_verified(),
            "statement": (
                "16*(N^2+L^2)*((S-N)^2+L^2) becomes "
                "t^4 + p*t^2 + q under t=2*N-S"
            ),
        },
        {
            "name": "quartic_to_elliptic_map",
            "verified": _quartic_to_elliptic_verified(),
            "statement": (
                "X=2*(z+t^2), V=2*t*(X+p) sends "
                "z^2=t^4+p*t^2+q to V^2=X^3+p*X^2-4*q*X-4*p*q"
            ),
        },
        {
            "name": "elliptic_to_quartic_inverse",
            "verified": _elliptic_to_quartic_inverse_verified(),
            "statement": (
                "t=V/(2*(X+p)), z=X/2-t^2 sends the elliptic equation "
                "back to z^2=t^4+p*t^2+q when X+p is nonzero"
            ),
        },
    ]
    return {
        "identities": identities,
        "all_verified": all(bool(row["verified"]) for row in identities),
        "proof_boundary": (
            "This is a symbolic algebra audit of the model identities. "
            "It does not certify ranks or rational points."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_identities()
    write_json(args.out, audit)
    print(f"wrote even-model identity audit to {args.out}")
    print(f"all_verified={audit['all_verified']}")
    if args.strict and not audit["all_verified"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
