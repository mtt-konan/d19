#!/usr/bin/env python3
"""Probe small modular obstructions for the focus near-miss template."""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable, Sequence
from math import gcd, prod
from typing import Any

VARIABLES: tuple[str, ...] = ("u", "p", "q", "v", "r", "s", "w", "x", "y")
MODES: tuple[str, ...] = ("residue", "strict_residue_units")


def square_residues(modulus: int) -> set[int]:
    return {(value * value) % modulus for value in range(modulus)}


def _opposite_parity(left: int, right: int, modulus: int) -> bool:
    if modulus % 2 != 0:
        return True
    return (left + right) % 2 == 1


def residue_pair_can_lift_primitive(left: int, right: int, modulus: int) -> bool:
    return gcd(left, right, modulus) == 1


def _residue_primitive_pair(m_value: int, n_value: int, modulus: int) -> bool:
    return (
        residue_pair_can_lift_primitive(m_value, n_value, modulus)
        and _opposite_parity(m_value, n_value, modulus)
    )


def _strict_primitive_pair(m_value: int, n_value: int, modulus: int) -> bool:
    return (
        m_value % modulus != 0
        and n_value % modulus != 0
        and gcd(m_value, n_value, modulus) == 1
        and _opposite_parity(m_value, n_value, modulus)
    )


def _side_conditions(values: dict[str, int], modulus: int, mode: str) -> bool:
    if mode == "residue":
        return (
            _residue_primitive_pair(values["p"], values["q"], modulus)
            and _residue_primitive_pair(values["r"], values["s"], modulus)
            and _residue_primitive_pair(values["x"], values["y"], modulus)
        )
    if mode != "strict_residue_units":
        raise ValueError(f"unknown mode: {mode}")
    return (
        values["u"] % modulus != 0
        and values["v"] % modulus != 0
        and values["w"] % modulus != 0
        and _strict_primitive_pair(values["p"], values["q"], modulus)
        and _strict_primitive_pair(values["r"], values["s"], modulus)
        and _strict_primitive_pair(values["x"], values["y"], modulus)
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


def probe_modulus(
    modulus: int,
    *,
    sample_limit: int = 5,
    mode: str = "residue",
) -> dict[str, Any]:
    residues = square_residues(modulus)
    total_assignments = modulus ** len(VARIABLES)
    side_condition_pass = 0
    shared_constraint_pass = 0
    closure_pass = 0
    missing_square_pass = 0
    sample_survivors: list[dict[str, int]] = []

    for assignment in _assignments(modulus):
        if not _side_conditions(assignment, modulus, mode):
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
        "mode": mode,
        "sample_limit": sample_limit,
        "total_assignments": total_assignments,
        "side_condition_pass": side_condition_pass,
        "shared_constraint_pass": shared_constraint_pass,
        "closure_pass": closure_pass,
        "missing_square_pass": missing_square_pass,
        "missing_square_obstructed": closure_pass - missing_square_pass,
        "sample_survivors": sample_survivors,
    }


def probe_many(
    moduli: Sequence[int],
    *,
    sample_limit: int = 5,
    mode: str = "residue",
    include_crt_summary: bool = False,
) -> dict[str, Any]:
    if include_crt_summary:
        _require_crt_residue_mode(mode)
        _require_pairwise_coprime(moduli)
    rows = [
        probe_modulus(modulus, sample_limit=sample_limit, mode=mode)
        for modulus in moduli
    ]
    payload: dict[str, Any] = {
        "template": "focus_bucket_sum_ab_B_odd_odd_N1_even_even",
        "mode": mode,
        "moduli": rows,
    }
    if include_crt_summary:
        payload["crt_summary"] = crt_summary_from_rows(rows, mode=mode)
    return payload


def _require_pairwise_coprime(moduli: Sequence[int]) -> None:
    for left_index, left_modulus in enumerate(moduli):
        for right_modulus in moduli[left_index + 1 :]:
            if gcd(left_modulus, right_modulus) != 1:
                raise ValueError("CRT summary requires pairwise coprime moduli")


def _require_crt_residue_mode(mode: str) -> None:
    if mode != "residue":
        raise ValueError("CRT summary is only defined for residue mode")


def _require_matching_row_modes(rows: Sequence[dict[str, Any]], mode: str) -> None:
    row_modes = {row.get("mode") for row in rows}
    if row_modes != {mode}:
        raise ValueError("CRT summary row modes must match the requested mode")


def crt_summary_from_rows(
    rows: Sequence[dict[str, Any]],
    *,
    mode: str,
) -> dict[str, Any]:
    _require_crt_residue_mode(mode)
    _require_matching_row_modes(rows, mode)
    moduli = [int(row["modulus"]) for row in rows]
    _require_pairwise_coprime(moduli)
    combined_modulus = prod(moduli)
    total_assignments = prod(int(row["total_assignments"]) for row in rows)
    side_condition_pass = prod(int(row["side_condition_pass"]) for row in rows)
    shared_constraint_pass = prod(int(row["shared_constraint_pass"]) for row in rows)
    closure_pass = prod(int(row["closure_pass"]) for row in rows)
    missing_square_pass = prod(int(row["missing_square_pass"]) for row in rows)
    return {
        "kind": "count_level_crt_diagnostic",
        "mode": mode,
        "moduli": moduli,
        "combined_modulus": combined_modulus,
        "total_assignments": total_assignments,
        "side_condition_pass": side_condition_pass,
        "shared_constraint_pass": shared_constraint_pass,
        "closure_pass": closure_pass,
        "missing_square_pass": missing_square_pass,
        "missing_square_obstructed": closure_pass - missing_square_pass,
        "single_modulus_summaries": list(rows),
        "interpretation": (
            "Count-level CRT diagnostic only; this does not construct integer "
            "solutions or prove an obstruction."
        ),
    }


def crt_summary(
    moduli: Sequence[int],
    *,
    sample_limit: int = 5,
    mode: str = "residue",
) -> dict[str, Any]:
    _require_crt_residue_mode(mode)
    _require_pairwise_coprime(moduli)
    rows = [
        probe_modulus(modulus, sample_limit=sample_limit, mode=mode)
        for modulus in moduli
    ]
    return crt_summary_from_rows(rows, mode=mode)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("moduli", type=int, nargs="+")
    parser.add_argument("--sample-limit", type=int, default=5)
    parser.add_argument("--mode", choices=MODES, default="residue")
    parser.add_argument(
        "--crt-summary",
        action="store_true",
        help="include count-level CRT diagnostic for pairwise coprime moduli",
    )
    args = parser.parse_args(argv)

    payload = probe_many(
        args.moduli,
        sample_limit=args.sample_limit,
        mode=args.mode,
        include_crt_summary=args.crt_summary,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
