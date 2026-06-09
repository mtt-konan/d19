#!/usr/bin/env python3
"""Probe small modular obstructions for the focus near-miss template."""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable, Sequence
from math import gcd
from typing import Any

VARIABLES: tuple[str, ...] = ("u", "p", "q", "v", "r", "s", "w", "x", "y")


def square_residues(modulus: int) -> set[int]:
    return {(value * value) % modulus for value in range(modulus)}


def _opposite_parity(left: int, right: int, modulus: int) -> bool:
    if modulus % 2 != 0:
        return True
    return (left + right) % 2 == 1


def _primitive_pair(m_value: int, n_value: int, modulus: int) -> bool:
    return (
        m_value % modulus != 0
        and n_value % modulus != 0
        and gcd(m_value, n_value, modulus) == 1
        and _opposite_parity(m_value, n_value, modulus)
    )


def _side_conditions(values: dict[str, int], modulus: int) -> bool:
    return (
        values["u"] % modulus != 0
        and values["v"] % modulus != 0
        and values["w"] % modulus != 0
        and _primitive_pair(values["p"], values["q"], modulus)
        and _primitive_pair(values["r"], values["s"], modulus)
        and _primitive_pair(values["x"], values["y"], modulus)
    )


def _odd_leg(scale: int, m_value: int, n_value: int, modulus: int) -> int:
    return scale * (m_value * m_value - n_value * n_value) % modulus


def _even_leg(scale: int, m_value: int, n_value: int, modulus: int) -> int:
    return scale * (2 * m_value * n_value) % modulus


def _derived_values(values: dict[str, int], modulus: int) -> dict[str, int]:
    a_value = _odd_leg(values["u"], values["p"], values["q"], modulus)
    n1_left = _even_leg(values["u"], values["p"], values["q"], modulus)
    b_left = _odd_leg(values["v"], values["r"], values["s"], modulus)
    n1_right = _even_leg(values["v"], values["r"], values["s"], modulus)
    b_right = _odd_leg(values["w"], values["x"], values["y"], modulus)
    n2_value = _even_leg(values["w"], values["x"], values["y"], modulus)
    return {
        "A": a_value,
        "B_left": b_left,
        "B_right": b_right,
        "B": b_left,
        "N1_left": n1_left,
        "N1_right": n1_right,
        "N1": n1_left,
        "N2": n2_value,
    }


def _assignments(modulus: int) -> Iterable[dict[str, int]]:
    values = dict.fromkeys(VARIABLES, 0)

    def walk(index: int) -> Iterable[dict[str, int]]:
        if index == len(VARIABLES):
            yield dict(values)
            return
        name = VARIABLES[index]
        for residue in range(modulus):
            values[name] = residue
            yield from walk(index + 1)

    yield from walk(0)


def probe_modulus(modulus: int, *, sample_limit: int = 5) -> dict[str, Any]:
    residues = square_residues(modulus)
    total_assignments = modulus ** len(VARIABLES)
    side_condition_pass = 0
    shared_constraint_pass = 0
    closure_pass = 0
    missing_square_pass = 0
    sample_survivors: list[dict[str, int]] = []

    for assignment in _assignments(modulus):
        if not _side_conditions(assignment, modulus):
            continue
        side_condition_pass += 1
        derived = _derived_values(assignment, modulus)
        if derived["B_left"] != derived["B_right"]:
            continue
        if derived["N1_left"] != derived["N1_right"]:
            continue
        shared_constraint_pass += 1
        if (derived["N1"] + derived["N2"] - derived["A"] - derived["B"]) % modulus != 0:
            continue
        closure_pass += 1
        missing_value = (derived["A"] * derived["A"] + derived["N2"] * derived["N2"]) % modulus
        if missing_value not in residues:
            continue
        missing_square_pass += 1
        if len(sample_survivors) < sample_limit:
            sample_survivors.append(
                {
                    **assignment,
                    "A": derived["A"],
                    "B": derived["B"],
                    "N1": derived["N1"],
                    "N2": derived["N2"],
                    "missing_value": missing_value,
                }
            )

    return {
        "modulus": modulus,
        "sample_limit": sample_limit,
        "total_assignments": total_assignments,
        "side_condition_pass": side_condition_pass,
        "shared_constraint_pass": shared_constraint_pass,
        "closure_pass": closure_pass,
        "missing_square_pass": missing_square_pass,
        "missing_square_obstructed": closure_pass - missing_square_pass,
        "sample_survivors": sample_survivors,
    }


def probe_many(moduli: Sequence[int], *, sample_limit: int = 5) -> dict[str, Any]:
    return {
        "template": "focus_bucket_sum_ab_B_odd_odd_N1_even_even",
        "moduli": [
            probe_modulus(modulus, sample_limit=sample_limit)
            for modulus in moduli
        ],
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("moduli", type=int, nargs="+")
    parser.add_argument("--sample-limit", type=int, default=5)
    args = parser.parse_args(argv)

    payload = probe_many(args.moduli, sample_limit=args.sample_limit)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
