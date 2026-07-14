#!/usr/bin/env python3
"""Exact p=5 local images for the frozen wl587 and wl589 factor covers.

The proof is a residue-stratum certificate on the two frozen source curves.
It does not search for rational points and it does not alter either D0 input.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Mapping
from itertools import product
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

try:
    from scripts.theory.aa_bb import wl587_pure_u7_d0_relative_2_descent as pure
    from scripts.theory.aa_bb import wl589_mixed_d0_relative_2_descent as mixed
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    import wl587_pure_u7_d0_relative_2_descent as pure
    import wl589_mixed_d0_relative_2_descent as mixed
    from json_io import write_json


P = 5
MOD25 = P**2
MOD625 = P**4

PURE_SURVIVORS = [
    1,
    97,
    105,
    265,
    1113,
    1385,
    5817,
    10185,
    14681,
    25705,
    107961,
    134345,
    564249,
    1424057,
    1541505,
    149525985,
]
MIXED_SURVIVORS = [
    5,
    21,
    29,
    37,
    85,
    357,
    493,
    629,
    3045,
    3885,
    5365,
    22533,
    51765,
    66045,
    91205,
    383061,
]

_PURE_D0_SHA256 = "e4406cc5bb66fc48f7fa5d002dee36791c1e222ea1a6a006a25eb8ef97a4aa7a"
_MIXED_D0_SHA256 = "7bc1d1f2e63dff4886b1f26ac3f6191b31c5410e42bfbd3636a0269ad238fcaa"


def _require_d0_payload(
    payload: Any,
    *,
    work_log: str,
    expected_sha256: str,
) -> None:
    if not isinstance(payload, Mapping):
        raise ValueError(f"invalid {work_log} predecessor payload")
    try:
        encoded = json.dumps(
            dict(payload), sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode()
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid {work_log} predecessor payload") from exc
    if hashlib.sha256(encoded).hexdigest() != expected_sha256:
        raise ValueError(f"{work_log} predecessor does not match the frozen D0 certificate")


def _unit_square_mod5(value: int) -> bool:
    return value % P in (1, 4)


def _square_mod25(value: int) -> bool:
    return value % MOD25 in {(root * root) % MOD25 for root in range(MOD25)}


def _q5_class(value: int) -> tuple[int, str]:
    if value <= 0:
        raise ValueError("named real/Q2 survivors must be positive")
    valuation = 0
    unit = value
    while unit % P == 0:
        valuation += 1
        unit //= P
    return valuation % 2, "square" if _unit_square_mod5(unit) else "nonsquare"


def _class_label(squareclass: tuple[int, str]) -> str:
    valuation, unit = squareclass
    if valuation == 0 and unit == "square":
        return "[1]"
    if valuation == 0 and unit == "nonsquare":
        return "[u]"
    if valuation == 1 and unit == "square":
        return "[5]"
    return "[5u]"


def _v5(value: int) -> int:
    if value == 0:
        raise ValueError("valuation of zero is not used in a nonzero factor row")
    value = abs(value)
    valuation = 0
    while value % P == 0:
        value //= P
        valuation += 1
    return valuation


def _pure_f(r: int) -> int:
    return 7 * r**4 + 2864 * r**2 + 87808


def _pure_t_mod25(r: int, w: int) -> int:
    numerator = w * (r**2 - 112)
    denominator = 4 * r * (r**2 + 112)
    return numerator * pow(denominator % MOD25, -1, MOD25) % MOD25


def _mixed_f(r: int) -> int:
    return 289 * r**4 - 408 * r**3 + 274 * r**2 - 120 * r + 25


def _mixed_t_mod25(r: int, w: int) -> int:
    numerator = -17 * (17 * r**2 - 20 * r + 5) * w
    denominator = (17 * r**2 - 5) * (17 * r**2 - 17 * r + 5)
    return numerator * pow(denominator % MOD25, -1, MOD25) % MOD25


def _mixed_zero_chart_g(x: int) -> int:
    return 1 - 24 * x + 274 * x**2 - 2040 * x**3 + 7225 * x**4


def _mixed_zero_chart_t_mod25(x: int, y: int) -> int:
    numerator = -17 * (85 * x**2 - 20 * x + 1) * y
    denominator = (85 * x**2 - 1) * (85 * x**2 - 17 * x + 1)
    return numerator * pow(denominator % MOD25, -1, MOD25) % MOD25


def _mixed_infinity_h(z: int) -> int:
    return 289 - 408 * z + 274 * z**2 - 120 * z**3 + 25 * z**4


def _mixed_infinity_t_mod25(z: int, v: int) -> int:
    numerator = -17 * (17 - 20 * z + 5 * z**2) * v
    denominator = (17 - 5 * z**2) * (17 - 17 * z + 5 * z**2)
    return numerator * pow(denominator % MOD25, -1, MOD25) % MOD25


def _pure_residue_certificate() -> dict[str, Any]:
    expected = {
        (1, 2): 14,
        (1, 3): 11,
        (2, 1): 14,
        (2, 4): 11,
        (3, 1): 11,
        (3, 4): 14,
        (4, 2): 11,
        (4, 3): 14,
    }
    residue_rows = []
    for (r0, w0), expected_t in expected.items():
        lifts = []
        for r1, w1 in product(range(P), repeat=2):
            r = r0 + P * r1
            w = w0 + P * w1
            if (w**2 - _pure_f(r)) % MOD25 == 0:
                lifts.append(_pure_t_mod25(r, w))
        residue_rows.append(
            {
                "r_mod_5": r0,
                "W_mod_5": w0,
                "lift_count_mod_25": len(lifts),
                "t_mod_25": sorted(set(lifts)),
                "expected_t_mod_25": expected_t,
            }
        )
    all_source_rows = {
        (r, w) for r, w in product(range(P), repeat=2) if (w**2 - _pure_f(r)) % P == 0
    }
    expected_rows = set(expected)
    checks = {
        "all_F5_source_rows_are_listed": all_source_rows == expected_rows,
        "every_row_has_five_smooth_lifts": all(
            row["lift_count_mod_25"] == P for row in residue_rows
        ),
        "t_mod_25_table_is_exact": all(
            row["t_mod_25"] == [row["expected_t_mod_25"]] for row in residue_rows
        ),
        "no_affine_r_zero_source_point": not _square_mod25(_pure_f(0)),
        "no_pure_pole_r_square": not _unit_square_mod5((-112) % P),
        "no_pure_Q5_infinity": not _unit_square_mod5(7),
    }
    return {
        "strata": residue_rows,
        "pole_and_boundary_argument": [
            "r=0 has f(0)=3 mod 5, so it has no Q5 point",
            "r^2+112=0 would give r^2=3 mod 5, impossible",
            "the infinity equation has leading squareclass 7=2 mod 5, impossible",
        ],
        "checks": checks,
    }


def _mixed_regular_certificate() -> dict[str, Any]:
    expected = {
        (2, 1): 17,
        (2, 4): 8,
        (3, 2): 8,
        (3, 3): 17,
        (4, 1): 17,
        (4, 4): 8,
    }
    rows = []
    for (r0, w0), expected_t in expected.items():
        lifts = []
        for r1, w1 in product(range(P), repeat=2):
            r = r0 + P * r1
            w = w0 + P * w1
            if (w**2 - _mixed_f(r)) % MOD25 == 0:
                lifts.append(_mixed_t_mod25(r, w))
        rows.append(
            {
                "r_mod_5": r0,
                "W_mod_5": w0,
                "lift_count_mod_25": len(lifts),
                "t_mod_25": sorted(set(lifts)),
                "expected_t_mod_25": expected_t,
            }
        )
    source_rows = {(r, w) for r, w in product(range(P), repeat=2) if (w**2 - _mixed_f(r)) % P == 0}
    expected_rows = set(expected) | {(0, 0), (1, 0)}
    return {
        "strata": rows,
        "checks": {
            "regular_F5_rows_are_exact": source_rows == expected_rows,
            "every_regular_row_has_five_lifts": all(row["lift_count_mod_25"] == P for row in rows),
            "regular_t_mod_25_table_is_exact": all(
                row["t_mod_25"] == [row["expected_t_mod_25"]] for row in rows
            ),
        },
    }


def _mixed_zero_chart_certificate() -> dict[str, Any]:
    expected = {
        (0, 1): 17,
        (0, 4): 8,
        (1, 1): 8,
        (1, 4): 17,
        (2, 2): 17,
        (2, 3): 8,
        (4, 2): 8,
        (4, 3): 17,
    }
    rows = []
    for (x0, y0), expected_t in expected.items():
        lifts = []
        for x1, y1 in product(range(P), repeat=2):
            x = x0 + P * x1
            y = y0 + P * y1
            if (y**2 - _mixed_zero_chart_g(x)) % MOD25 == 0:
                lifts.append(_mixed_zero_chart_t_mod25(x, y))
        rows.append(
            {
                "x_mod_5": x0,
                "y_mod_5": y0,
                "lift_count_mod_25": len(lifts),
                "t_mod_25": sorted(set(lifts)),
                "expected_t_mod_25": expected_t,
            }
        )
    x3_values = {_mixed_zero_chart_g(3 + P * x1) % MOD25 for x1 in range(P)}
    source_rows = {
        (x, y) for x, y in product(range(P), repeat=2) if (y**2 - _mixed_zero_chart_g(x)) % P == 0
    }
    square_residues_mod25 = {(root * root) % MOD25 for root in range(MOD25)}
    return {
        "strata": rows,
        "x_mod_5_equals_3_values_mod_25": sorted(x3_values),
        "checks": {
            "all_zero_chart_F5_rows_are_listed": (source_rows == set(expected) | {(3, 0)}),
            "every_nonexceptional_zero_chart_row_has_five_lifts": all(
                row["lift_count_mod_25"] == P for row in rows
            ),
            "zero_chart_t_mod_25_table_is_exact": all(
                row["t_mod_25"] == [row["expected_t_mod_25"]] for row in rows
            ),
            "x_mod_5_equals_3_has_no_source_lift": x3_values == {15}
            and 15 not in square_residues_mod25,
        },
    }


def _mixed_infinity_certificate() -> dict[str, Any]:
    expected = {2: 8, 3: 17}
    infinity_rows = {v for v in range(P) if (v**2 - _mixed_infinity_h(0)) % P == 0}
    rows = []
    for v0, expected_t in expected.items():
        lifts = []
        for z1, v1 in product(range(P), repeat=2):
            z = P * z1
            v = v0 + P * v1
            if (v**2 - _mixed_infinity_h(z)) % MOD25 == 0:
                lifts.append(_mixed_infinity_t_mod25(z, v))
        rows.append(
            {
                "v_mod_5": v0,
                "lift_count_mod_25": len(lifts),
                "t_mod_25": sorted(set(lifts)),
                "expected_t_mod_25": expected_t,
            }
        )
    return {
        "strata": rows,
        "checks": {
            "all_infinity_F5_rows_are_listed": infinity_rows == set(expected),
            "both_infinity_disks_are_smooth": all(row["lift_count_mod_25"] == P for row in rows),
            "infinity_t_mod_25_table_is_exact": all(
                row["t_mod_25"] == [row["expected_t_mod_25"]] for row in rows
            ),
        },
    }


def _mixed_exception_certificate() -> dict[str, Any]:
    r1_values = {(_mixed_f(1 + P * x) // P) % P for x in range(P)}
    a_root_x_values = [x for x in range(P) if (85 * x**2 - 17 * x + 1) % P == 0]
    return {
        "r_mod_5_equals_1_source_obstruction": sorted(r1_values),
        "A_over_5_mod_5_root": a_root_x_values,
        "checks": {
            "r_mod_5_equals_1_has_no_source_point": r1_values == {2} and not _square_mod25(5 * 2),
            "D_equals_zero_has_no_Q5_root": _v5(5) == 1 and 17 % P != 0,
            "A_equals_zero_has_no_source_point": (
                a_root_x_values == [3]
                and _mixed_zero_chart_g(3) % MOD25 == 15
                and not _square_mod25(15)
            ),
        },
        "argument": [
            "D=0 gives r^2=5/17, whose valuation is odd",
            "A=0 reduces to r=1 or r=0; the r=1 branch is already impossible",
            "on r=5*x with A=0 one has x=3 mod 5 and f(r)=25*g(x)=15 mod 25 times 25",
        ],
    }


def _factor_zero_certificate(module: Any) -> dict[str, Any]:
    source_equation = module.W**2 - module.SOURCE_POLYNOMIAL
    resultant_plus = sp.resultant(source_equation, module.J_PLUS, module.W)
    resultant_minus = sp.resultant(source_equation, module.J_MINUS, module.W)
    content_plus, primitive_plus = sp.primitive(resultant_plus, module.R)
    content_minus, primitive_minus = sp.primitive(resultant_minus, module.R)
    denominator_resultant_nonzero = (
        sp.resultant(primitive_plus, module.T_DENOMINATOR, module.R) != 0
    )
    roots_mod25 = [r for r in range(MOD25) if int(primitive_plus.subs(module.R, r)) % MOD25 == 0]
    if module is pure:
        return {
            "resultant_content": int(content_plus),
            "primitive_resultant_mod_5": str(sp.factor(primitive_plus, modulus=P)),
            "primitive_resultant_roots_mod_25": roots_mod25,
            "checks": {
                "plus_and_minus_resultants_match": primitive_plus == primitive_minus,
                "pure_factor_zero_has_no_mod_25_root": roots_mod25 == [],
                "pure_factor_zero_branch_is_Q5_empty": roots_mod25 == [],
                "factor_zero_is_disjoint_from_poles": denominator_resultant_nonzero,
            },
            "argument": (
                "A finite pure factor zero is a Q5 root of the exact resultant. "
                "Its primitive resultant has no root modulo 25, so Hensel lifting "
                "cannot produce a Q5 factor-zero point."
            ),
        }

    coefficient_w = sp.diff(module.J_PLUS, module.W)
    constant_j = module.J_PLUS.subs(module.W, 0)
    coefficient_w_mod5 = int((coefficient_w / P).subs(module.R, 2)) % P
    constant_j_mod5 = int((constant_j / P).subs(module.R, 2)) % P
    w_mod5 = (-constant_j_mod5 * pow(coefficient_w_mod5, -1, P)) % P
    t_mod5 = (
        -17
        * (17 * 2**2 - 20 * 2 + 5)
        * w_mod5
        * pow(
            ((17 * 2**2 - 5) * (17 * 2**2 - 17 * 2 + 5)) % P,
            -1,
            P,
        )
        % P
    )
    primitive_mod5 = sp.factor(primitive_plus, modulus=P)
    expected_mod5 = sp.factor(
        2
        * module.R**8
        * (module.R - 2)
        * (module.R + 1)
        * (module.R + 2)
        * (module.R**2 - 2 * module.R - 1)
        * (module.R**2 + 2 * module.R - 2),
        modulus=P,
    )
    root_value_mod5 = int(primitive_plus.subs(module.R, 2)) % P
    root_derivative_mod5 = int(sp.diff(primitive_plus, module.R).subs(module.R, 2)) % P
    resultant_reconstruction = (
        sp.factor(resultant_plus - (constant_j**2 - coefficient_w**2 * module.SOURCE_POLYNOMIAL))
        == 0
    )
    plus_nonzero_factor_unit = (-2 * t_mod5) % P
    minus_zero_t_mod5 = (-t_mod5) % P
    minus_nonzero_factor_unit = (2 * minus_zero_t_mod5) % P
    hensel_hypotheses = (
        root_value_mod5 == 0
        and root_derivative_mod5 != 0
        and coefficient_w_mod5 != 0
        and resultant_reconstruction
    )
    return {
        "resultant_content": int(content_plus),
        "primitive_resultant_mod_5": str(primitive_mod5),
        "resultant_minus_matches": primitive_plus == primitive_minus
        and content_plus == content_minus,
        "hensel_root_residue": 2,
        "hensel_root_value_mod_5": root_value_mod5,
        "hensel_root_derivative_mod_5": root_derivative_mod5,
        "plus_zero_nonzero_factor_unit_mod_5": plus_nonzero_factor_unit,
        "minus_zero_nonzero_factor_unit_mod_5": minus_nonzero_factor_unit,
        "checks": {
            "mixed_primitive_resultant_mod_5_is_exact": (primitive_mod5 == expected_mod5),
            "mixed_resultant_root_is_simple_mod_5": (
                root_value_mod5 == 0 and root_derivative_mod5 == 1
            ),
            "factor_linear_coefficient_has_exact_5_factor": all(
                int(coefficient) % P == 0
                for coefficient in sp.Poly(coefficient_w, module.R).all_coeffs()
            ),
            "factor_constant_coefficient_has_exact_5_factor": all(
                int(coefficient) % P == 0
                for coefficient in sp.Poly(constant_j, module.R).all_coeffs()
            ),
            "normalized_linear_coefficient_is_unit_at_root": (coefficient_w_mod5 != 0),
            "resultant_reconstructs_source_after_linear_factor_map": (resultant_reconstruction),
            "factor_zero_chart_denominator_is_a_unit_at_root": (
                int((mixed.PARAM_DENOMINATOR * mixed.U0_NUMERATOR).subs(mixed.R, 2)) % P != 0
            ),
            "factor_zero_branch_exists_by_Hensel": hensel_hypotheses,
            "plus_zero_residue_has_t_equals_2": w_mod5 == 1 and t_mod5 == 2,
            "factor_zero_is_disjoint_from_poles": denominator_resultant_nonzero,
            "minus_factor_zero_branch_is_W_involution": (
                sp.factor(module.J_MINUS.subs(module.W, -module.W) - module.J_PLUS) == 0
            ),
            "nonzero_factor_at_plus_zero_has_class_5": (
                _unit_square_mod5(plus_nonzero_factor_unit)
            ),
            "nonzero_factor_at_minus_zero_has_class_5": (
                _unit_square_mod5(minus_nonzero_factor_unit)
            ),
        },
        "argument": (
            "For the mixed family the primitive resultant has a simple root r=2 mod 5. "
            "Both coefficients of J_plus=a(r)*W+b(r) are divisible by 5, while a/5 "
            "is a unit at r=2. Hensel gives r in Q5 and W=-b/a in Z5 with J_plus=0; "
            "J_minus follows by W -> -W. At F_plus=0, F_minus=-10*t, and at "
            "F_minus=0, F_plus=10*t. The factor-zero roots have t=2 or 3 mod 5, "
            "so the nonzero factor divided by 5 is 1 or 4 mod 5, hence class [5]."
        ),
    }


def _factor_valuation_certificate() -> dict[str, Any]:
    def pure_h_plus(t: int) -> int:
        return t**2 + 18 * t + 97

    def pure_h_minus(t: int) -> int:
        return t**2 - 18 * t + 97

    def mixed_h_plus(t: int) -> int:
        return t**2 + 20 * t + 296

    def mixed_h_minus(t: int) -> int:
        return t**2 - 20 * t + 296

    pure_rows = {
        11: (_v5(pure_h_plus(11)), _v5(pure_h_minus(11))),
        14: (_v5(pure_h_plus(14)), _v5(pure_h_minus(14))),
    }
    mixed_rows = {
        8: (_v5(mixed_h_plus(8)), _v5(mixed_h_minus(8))),
        17: (_v5(mixed_h_plus(17)), _v5(mixed_h_minus(17))),
    }
    return {
        "pure": {
            "t_mod_25_rows": pure_rows,
            "checks": {
                "t=11_has_factor_valuations_0_1": pure_rows[11] == (0, 1),
                "t=14_has_factor_valuations_1_0": pure_rows[14] == (1, 0),
            },
            "argument": (
                "For t=11+25*z or 14+25*z the displayed residues modulo 25 are fixed, "
                "so the valuation pair is exactly (0,1) or (1,0)."
            ),
        },
        "mixed": {
            "t_mod_25_rows": mixed_rows,
            "checks": {
                "t=8_has_low_plus_valuation_one": mixed_rows[8][0] == 1,
                "t=17_has_low_minus_valuation_one": mixed_rows[17][1] == 1,
                "low_plus_unit_is_square": ((mixed_h_plus(8) // P) * pow(4, -1, P) % P in (1, 4)),
                "low_minus_unit_is_square": (
                    (mixed_h_minus(17) // P) * pow(4, -1, P) % P in (1, 4)
                ),
            },
            "argument": (
                "At t=8 mod 25, F_plus has exact valuation one and square unit; "
                "at t=17 mod 25, F_minus has exact valuation one and square unit. "
                "The other factor has valuation at least two. Equal factor squareclasses "
                "therefore force the other valuation to be odd and force the common class [5]."
            ),
        },
    }


def _mixed_inclusion_certificate() -> dict[str, Any]:
    r = 4
    w_mod = 276
    t_mod = 67
    f_value = _mixed_f(r)
    denominator = (17 * r**2 - 5) * (17 * r**2 - 17 * r + 5)
    t_value = (
        -17 * (17 * r**2 - 20 * r + 5) * w_mod * pow(denominator % MOD625, -1, MOD625) % MOD625
    )
    h_plus = t_mod**2 + 20 * t_mod + 296
    h_minus = t_mod**2 - 20 * t_mod + 296
    return {
        "source_residue": {
            "r": r,
            "W_mod_625": w_mod,
            "t_mod_625": t_value,
            "f(r)": f_value,
        },
        "factor_values_at_residue": {
            "H_plus": h_plus,
            "H_minus": h_minus,
            "H_plus_over_5^3_mod_5": (h_plus // P**3) % P,
            "H_minus_over_5_mod_5": (h_minus // P) % P,
        },
        "checks": {
            "source_Hensel_residue_is_exact": ((w_mod**2 - f_value) % MOD625 == 0),
            "source_denominator_is_a_5adic_unit": denominator % P != 0,
            "t_mod_625_is_67": t_value == t_mod,
            "plus_factor_has_valuation_three": _v5(h_plus) == 3,
            "minus_factor_has_valuation_one": _v5(h_minus) == 1,
            "both_F_over_5_have_squareclasses": (
                (h_plus // P**3) * pow(4, -1, P) % P in (1, 4)
                and (h_minus // P) * pow(4, -1, P) % P in (1, 4)
            ),
        },
        "hensel_argument": (
            "2*W is a unit at W=276 mod 5, so W^2=f(4) has a unique Q5 lift. "
            "For t=67 mod 625, H_plus/5^3 and H_minus/5 are both 4 mod 5; "
            "Hensel's square criterion gives F_plus/5 and F_minus/5 squares."
        ),
    }


def _frozen_map_certificate() -> dict[str, Any]:
    pure_identity = all(
        pure._reduce_source(expr - (2 * pure.T_DENOMINATOR) ** 2 * factor) == 0
        for expr, factor in [
            (pure.J_PLUS, pure.F_PLUS),
            (pure.J_MINUS, pure.F_MINUS),
        ]
    )
    mixed_identity = all(
        mixed._reduce_source(expr - (2 * mixed.T_DENOMINATOR) ** 2 * factor) == 0
        for expr, factor in [
            (mixed.J_PLUS, mixed.F_PLUS),
            (mixed.J_MINUS, mixed.F_MINUS),
        ]
    )
    return {
        "pure_u7": {
            "source_equation": "W^2=7*r^4+2864*r^2+87808",
            "factor_equations": "J_plus=d*s_plus^2, J_minus=d*s_minus^2",
            "normalized_factor_map": (
                "a_plus=s_plus/(2*T_denominator), a_minus=s_minus/(2*T_denominator), "
                "T_denominator=4*r*(r^2+112)"
            ),
            "fixed_cover_map": "R=d*a_plus*a_minus, R^2=(N^2+4)*(M^2+4)",
            "aa_bb_conditions": [
                "(N^2+49)*(M^2+49)=(Z/4)^2",
                "-9<t<9",
                "AA/BB source leg=7 and opposite leg=2",
            ],
            "source_leg": 7,
            "opposite_leg": 2,
            "identity_check": pure_identity,
        },
        "mixed_u3_v5_w17": {
            "source_equation": ("W^2=289*r^4-408*r^3+274*r^2-120*r+25"),
            "factor_equations": "J_plus=d*s_plus^2, J_minus=d*s_minus^2",
            "normalized_factor_map": (
                "a_plus=s_plus/(2*T_denominator), a_minus=s_minus/(2*T_denominator), "
                "T_denominator=(17*r^2-5)*(17*r^2-17*r+5)"
            ),
            "fixed_cover_map": "R=d*a_plus*a_minus, R^2=(N^2+49)*(M^2+49)",
            "aa_bb_conditions": [
                "(N^2+9)*(M^2+9)=(Z/4)^2",
                "-10<t<10",
                "AA/BB source leg=3 and opposite leg=7",
            ],
            "source_leg": 3,
            "opposite_leg": 7,
            "identity_check": mixed_identity,
        },
    }


def _named_mapping(values: list[int], allowed: set[tuple[int, str]]) -> dict[str, Any]:
    rows = [
        {
            "d": value,
            "Q5_class": _class_label(_q5_class(value)),
            "survives": _q5_class(value) in allowed,
        }
        for value in values
    ]
    return {
        "rows": rows,
        "survive": [row["d"] for row in rows if row["survives"]],
        "deleted": [row["d"] for row in rows if not row["survives"]],
        "all_named_values_are_distinct": len(values) == len(set(values)),
    }


def build_wl590_from_d0(
    pure_payload: Mapping[str, Any], mixed_payload: Mapping[str, Any]
) -> dict[str, Any]:
    _require_d0_payload(
        pure_payload,
        work_log="wl587",
        expected_sha256=_PURE_D0_SHA256,
    )
    _require_d0_payload(
        mixed_payload,
        work_log="wl589",
        expected_sha256=_MIXED_D0_SHA256,
    )
    pure_residues = _pure_residue_certificate()
    mixed_regular = _mixed_regular_certificate()
    mixed_zero = _mixed_zero_chart_certificate()
    mixed_infinity = _mixed_infinity_certificate()
    mixed_exceptions = _mixed_exception_certificate()
    pure_zero = _factor_zero_certificate(pure)
    mixed_zero_factor = _factor_zero_certificate(mixed)
    valuations = _factor_valuation_certificate()
    inclusion = _mixed_inclusion_certificate()
    maps = _frozen_map_certificate()

    pure_checks = {
        **pure_residues["checks"],
        **pure_zero["checks"],
        **valuations["pure"]["checks"],
        "pure_factor_identity_is_exact": maps["pure_u7"]["identity_check"],
        "no_common_factor_valuation_parity": all(
            left % 2 != right % 2 for left, right in valuations["pure"]["t_mod_25_rows"].values()
        ),
    }
    mixed_t_classes = {
        row["t_mod_25"][0]
        for certificate in [mixed_regular, mixed_zero, mixed_infinity]
        for row in certificate["strata"]
    }
    mixed_checks = {
        **mixed_regular["checks"],
        **mixed_zero["checks"],
        **mixed_infinity["checks"],
        **mixed_exceptions["checks"],
        **mixed_zero_factor["checks"],
        **valuations["mixed"]["checks"],
        **inclusion["checks"],
        "mixed_factor_identity_is_exact": maps["mixed_u3_v5_w17"]["identity_check"],
        "all_nonpole_source_t_classes_are_8_or_17_mod_25": mixed_t_classes == {8, 17},
        "only_common_mixed_class_is_5": (
            mixed_t_classes == {8, 17}
            and valuations["mixed"]["checks"]["low_plus_unit_is_square"]
            and valuations["mixed"]["checks"]["low_minus_unit_is_square"]
            and mixed_zero_factor["checks"]["nonzero_factor_at_plus_zero_has_class_5"]
            and mixed_zero_factor["checks"]["nonzero_factor_at_minus_zero_has_class_5"]
        ),
    }
    named = {
        "pure_u7": _named_mapping(PURE_SURVIVORS, set()),
        "mixed_u3_v5_w17": _named_mapping(MIXED_SURVIVORS, {(1, "square")}),
    }
    all_checks = {
        "pure_proof": all(pure_checks.values()),
        "mixed_proof": all(mixed_checks.values()),
        "pure_named_mapping": named["pure_u7"]["all_named_values_are_distinct"],
        "mixed_named_mapping": named["mixed_u3_v5_w17"]["all_named_values_are_distinct"],
        "exact_fixed_cover_and_lift_maps": all(row["identity_check"] for row in maps.values()),
    }
    violations = [name for name, passed in all_checks.items() if not passed]
    return {
        "status": "ok" if not violations else "error",
        "ready": not violations,
        "work_log": "wl590",
        "scope": "p=5 local factor-twist images for frozen wl587 and wl589 only",
        "prime": P,
        "local_squareclass_basis": ["[1]", "[u]", "[5]", "[5u]"],
        "local_images": {
            "pure_u7": [],
            "mixed_u3_v5_w17": ["[5]"],
        },
        "named_survivor_mapping": named,
        "proof_certificate": {
            "pure_u7": {
                "checks": pure_checks,
                "source_residue_certificate": pure_residues,
                "factor_zero_certificate": pure_zero,
                "valuation_certificate": valuations["pure"],
                "conclusion": (
                    "Every Q5 source point has t=11 or 14 mod 25, giving factor "
                    "valuation pairs (0,1) or (1,0); the pure p=5 local image is empty."
                ),
            },
            "mixed_u3_v5_w17": {
                "checks": mixed_checks,
                "regular_source_certificate": mixed_regular,
                "zero_chart_certificate": mixed_zero,
                "infinity_certificate": mixed_infinity,
                "exception_certificate": mixed_exceptions,
                "factor_zero_certificate": mixed_zero_factor,
                "valuation_certificate": valuations["mixed"],
                "inclusion_certificate": inclusion,
                "conclusion": (
                    "Every Q5 factor-cover point has common class [5], and the "
                    "displayed Hensel residue supplies [5]; hence I_5,m={[5]}."
                ),
            },
        },
        "fixed_cover_and_lift": maps,
        "verification": {
            "checks": all_checks,
            "violations": violations,
            "strict_certificate": (
                "All p=5 valuation/residue strata, poles, projective boundaries, "
                "factor-zero branches, Hensel inclusion, named mappings, and frozen "
                "AA+BB maps are checked; no height or rational-point search is used."
            ),
        },
    }


def build_wl590_p5_factor_twist_local_image_comparison() -> dict[str, Any]:
    return build_wl590_from_d0(
        pure.build_wl587_pure_u7_d0_relative_2_descent(),
        mixed.build_wl589_mixed_d0_relative_2_descent(),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl590_p5_factor_twist_local_image_comparison()
    if args.out is not None:
        write_json(args.out, payload)
    if args.strict:
        print(f"status={payload['status']}")
        print(f"work_log={payload['work_log']}")
        print(f"ready={payload['ready']}")
        print(f"violations={payload['verification']['violations']}")
        return 0 if payload["ready"] else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
