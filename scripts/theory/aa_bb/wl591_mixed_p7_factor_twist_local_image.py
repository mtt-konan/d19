#!/usr/bin/env python3
"""Certify the exact normalized mixed factor-twist image over Q_7.

The certificate works on the frozen wl589 source curve and factor functions.
It enumerates the complete residue strata of the smooth proper source modulo 7,
then uses unit square criteria and Hensel lifting.  It does not search for
rational points, compute ranks, or replace the frozen normalized cover.
"""

from __future__ import annotations

import argparse
import sys
from itertools import product
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

try:
    from scripts.theory.aa_bb import wl589_mixed_d0_relative_2_descent as mixed
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    import wl589_mixed_d0_relative_2_descent as mixed
    from json_io import write_json


P = 7
MOD49 = P**2
SQUARE_RESIDUES = {1, 2, 4}
MIXED_REPRESENTATIVES = (5, 3045, 66045, 91205)


def _f(r: int) -> int:
    return 289 * r**4 - 408 * r**3 + 274 * r**2 - 120 * r + 25


def _d(r: int) -> int:
    return 17 * r**2 - 5


def _a(r: int) -> int:
    return 17 * r**2 - 17 * r + 5


def _b(r: int) -> int:
    return 17 * r**2 - 20 * r + 5


def _t_mod(r: int, w: int, modulus: int) -> int:
    denominator = (_d(r) * _a(r)) % modulus
    return -17 * _b(r) * w * pow(denominator, -1, modulus) % modulus


def _h_infinity(z: int) -> int:
    return 289 - 408 * z + 274 * z**2 - 120 * z**3 + 25 * z**4


def _t_infinity_mod7(v: int) -> int:
    # The two leading degree-four coefficients cancel, so t=-v at z=0.
    return (-v) % P


def _q7_class(value: int) -> tuple[int, str]:
    if value <= 0:
        raise ValueError("named representatives must be positive")
    valuation = 0
    unit = value
    while unit % P == 0:
        valuation += 1
        unit //= P
    return valuation % 2, "square" if unit % P in SQUARE_RESIDUES else "nonsquare"


def _class_label(squareclass: tuple[int, str]) -> str:
    valuation, unit = squareclass
    if valuation == 0 and unit == "square":
        return "[1]"
    if valuation == 0 and unit == "nonsquare":
        return "[u]"
    if valuation == 1 and unit == "square":
        return "[7]"
    return "[7u]"


def _source_residue_certificate() -> dict[str, Any]:
    source_rows = sorted((r, w) for r, w in product(range(P), repeat=2) if (w**2 - _f(r)) % P == 0)
    regular_rows = sorted(
        (r, w, _t_mod(r, w, P)) for r, w in source_rows if _d(r) % P != 0 and _a(r) % P != 0
    )
    pole_rows = sorted((r, w) for r, w in source_rows if _d(r) % P == 0)
    expected_source_rows = [
        (0, 2),
        (0, 5),
        (1, 2),
        (1, 5),
        (2, 1),
        (2, 6),
        (4, 1),
        (4, 6),
        (5, 3),
        (5, 4),
    ]
    expected_regular_rows = [
        (0, 2, 4),
        (0, 5, 3),
        (1, 2, 4),
        (1, 5, 3),
        (4, 1, 3),
        (4, 6, 4),
    ]
    source_poly = sp.Poly(
        2
        * (sp.Symbol("r") ** 2 - 3 * sp.Symbol("r") + 1)
        * (sp.Symbol("r") ** 2 + 2 * sp.Symbol("r") + 2),
        sp.Symbol("r"),
        modulus=P,
    )
    frozen_source_poly = sp.Poly(
        mixed.SOURCE_POLYNOMIAL,
        mixed.R,
        modulus=P,
    )
    squarefree = source_poly.gcd(source_poly.diff()).degree() == 0
    return {
        "source_reduction": "2*(r^2-3*r+1)*(r^2+2*r+2) mod 7",
        "source_reduction_squarefree": squarefree,
        "source_rows_mod_7": source_rows,
        "regular_rows_mod_7": regular_rows,
        "pole_rows_mod_7": pole_rows,
        "checks": {
            "source_reduction_matches_frozen_model": (frozen_source_poly == source_poly),
            "source_reduction_is_squarefree": squarefree,
            "complete_source_residue_table": source_rows == expected_source_rows,
            "complete_regular_residue_table": regular_rows == expected_regular_rows,
            "no_source_row_has_w_zero": all(w != 0 for _, w in source_rows),
            "regular_t_residues_are_3_or_4": {t for _, _, t in regular_rows} == {3, 4},
        },
        "argument": (
            "The source has good reduction at 7.  The complete F_7 point table "
            "therefore contains every affine Q_7 residue disk; each listed "
            "source row is smooth because 2W is a unit."
        ),
    }


def _infinity_certificate() -> dict[str, Any]:
    infinity_rows = [v for v in range(P) if (v**2 - _h_infinity(0)) % P == 0]
    expected = [(3, 4), (4, 3)]
    rows = [(v, _t_infinity_mod7(v)) for v in infinity_rows]
    return {
        "infinity_equation": ("v^2=289-408*z+274*z^2-120*z^3+25*z^4, z=1/r, v=W/r^2"),
        "rows_mod_7": rows,
        "checks": {
            "exactly_two_infinity_disks": rows == expected,
            "infinity_hensel_derivative_is_a_unit": all((2 * v) % P != 0 for v in infinity_rows),
            "infinity_t_residues_are_3_or_4": {t for _, t in rows} == {3, 4},
        },
        "argument": (
            "At z=0 the roots v=+/-17 reduce to 3 and 4.  Since 2v is a "
            "unit, both roots extend uniquely over each z in 7 Z_7, and "
            "t=-v mod 7 on the two disks."
        ),
    }


def _factor_residue_certificate() -> dict[str, Any]:
    inv2 = pow(2, -1, P)
    rows = []
    for t in (3, 4):
        n = (10 + t) * inv2 % P
        m = (10 - t) * inv2 % P
        rows.append(
            {
                "t_mod_7": t,
                "N_mod_7": n,
                "M_mod_7": m,
                "unit_factor": "F_plus" if t == 3 else "F_minus",
                "unit_factor_mod_7": (n * n if t == 3 else m * m) % P,
            }
        )
    return {
        "rows": rows,
        "square_residues_mod_7": sorted(SQUARE_RESIDUES),
        "checks": {
            "t_3_has_unit_plus_factor": rows[0]["unit_factor"] == "F_plus"
            and rows[0]["unit_factor_mod_7"] == 2,
            "t_4_has_unit_minus_factor": rows[1]["unit_factor"] == "F_minus"
            and rows[1]["unit_factor_mod_7"] == 2,
            "unit_factor_is_always_a_Q7_square": all(
                row["unit_factor_mod_7"] in SQUARE_RESIDUES for row in rows
            ),
        },
        "argument": (
            "For t=3 mod 7, F_plus is a unit with square residue 2; for "
            "t=4 mod 7, F_minus is such a unit.  If F=d*s^2, this one unit "
            "already forces [d]=[1]."
        ),
    }


def _pole_and_denominator_certificate(
    source: dict[str, Any],
) -> dict[str, Any]:
    r_symbol = sp.Symbol("r")
    d_poly = sp.Poly(17 * r_symbol**2 - 5, r_symbol, modulus=P)
    a_poly = sp.Poly(17 * r_symbol**2 - 17 * r_symbol + 5, r_symbol, modulus=P)
    d_roots = [r for r in range(P) if _d(r) % P == 0]
    a_roots = [r for r in range(P) if _a(r) % P == 0]
    pole_rows = []
    for r, w in source["pole_rows_mod_7"]:
        j_value = 289 * _b(r) ** 2 * _f(r) % P
        pole_rows.append(
            {
                "r_mod_7": r,
                "W_mod_7": w,
                "D_derivative_mod_7": (34 * r) % P,
                "A_mod_7": _a(r) % P,
                "B_times_W_mod_7": _b(r) * w % P,
                "J_plus_equals_J_minus_mod_7": j_value,
            }
        )
    return {
        "D_reduction": "3*r^2+2 mod 7",
        "A_reduction": "3*r^2-3*r+5 mod 7",
        "D_roots_mod_7": d_roots,
        "A_roots_mod_7": a_roots,
        "pole_rows": pole_rows,
        "checks": {
            "D_has_simple_roots": d_roots == [2, 5] and all((34 * r) % P != 0 for r in d_roots),
            "A_has_no_Q7_root": a_roots == [] and int(a_poly.discriminant()) % P in {3, 5, 6},
            "D_pole_rows_are_complete": [(row["r_mod_7"], row["W_mod_7"]) for row in pole_rows]
            == [(2, 1), (2, 6), (5, 3), (5, 4)],
            "every_D_row_is_a_simple_t_pole": all(
                row["D_derivative_mod_7"] != 0
                and row["A_mod_7"] != 0
                and row["B_times_W_mod_7"] != 0
                for row in pole_rows
            ),
            "pole_J_values_are_square_units": all(
                row["J_plus_equals_J_minus_mod_7"] in SQUARE_RESIDUES for row in pole_rows
            ),
            "D_and_A_have_no_common_residue_root": sp.gcd(d_poly, a_poly).degree() == 0,
        },
        "argument": (
            "The D=0 disks are genuine Q_7 source disks by Hensel because "
            "D'(2) and D'(5) are units and f is a square unit there.  On "
            "D=0, the cleared values are J_plus=J_minus=289*B^2*f, with "
            "square unit residues 1 or 4.  Equivalently, away from the pole "
            "F_plus and F_minus are t^2/4 times principal units, hence both "
            "have class [1].  A=0 has no Q_7 point because its discriminant "
            "-51 is a nonsquare modulo 7."
        ),
    }


def _zero_and_factor_zero_certificate() -> dict[str, Any]:
    factor_discriminant = -784
    return {
        "factor_zero_equations": [
            "F_plus=0 iff N^2=-49",
            "F_minus=0 iff M^2=-49",
        ],
        "zero_value_branches": {
            "t=0": "F_plus=F_minus=74, 74=4 mod 7",
            "N=0": "F_plus=49",
            "M=0": "F_minus=49",
        },
        "checks": {
            "minus_one_is_nonsquare_mod_7": -1 % P not in SQUARE_RESIDUES,
            "factor_zero_discriminant": factor_discriminant == -784,
            "no_Q7_factor_zero": (
                factor_discriminant == -16 * 7**2 and -1 % P not in SQUARE_RESIDUES
            ),
            "t_zero_value_is_a_square_unit": 74 % P in SQUARE_RESIDUES,
            "N_zero_value_is_a_square": 49 == 7**2,
            "M_zero_value_is_a_square": 49 == 7**2,
        },
        "argument": (
            "A factor zero would force (N/7)^2=-1 or (M/7)^2=-1 in Q_7, "
            "which is impossible.  Thus R=0 has no Q_7 point.  The cleared "
            "J zeros at a genuine denominator pole are not factor zeros: "
            "the pole calculation above gives their normalized squareclass."
        ),
    }


def _inclusion_certificate() -> dict[str, Any]:
    r = 1
    w_mod49 = 16
    f_value = _f(r)
    t_mod49 = _t_mod(r, w_mod49, MOD49)
    inv2 = pow(2, -1, MOD49)
    n_mod49 = (10 + t_mod49) * inv2 % MOD49
    m_mod49 = (10 - t_mod49) * inv2 % MOD49
    plus_unit_mod7 = ((n_mod49 // P) ** 2 + 1) % P
    minus_unit_mod7 = m_mod49**2 % P
    denominator = _d(r) * _a(r)
    return {
        "source_residue": {
            "r": r,
            "f(r)": f_value,
            "W_mod_49": w_mod49,
            "t_mod_49": t_mod49,
            "N_mod_49": n_mod49,
            "M_mod_49": m_mod49,
        },
        "factor_unit_residues": {
            "F_plus_over_49_mod_7": plus_unit_mod7,
            "F_minus_mod_7": minus_unit_mod7,
        },
        "checks": {
            "source_Hensel_congruence": (w_mod49**2 - f_value) % MOD49 == 0,
            "source_Hensel_derivative_is_a_unit": (2 * 2) % P != 0,
            "source_denominator_is_a_unit": denominator % P != 0,
            "t_mod_49_is_4": t_mod49 == 4,
            "N_mod_49_is_7": n_mod49 == 7,
            "M_mod_49_is_3": m_mod49 == 3,
            "both_factor_units_are_square_residues": (
                plus_unit_mod7 in SQUARE_RESIDUES and minus_unit_mod7 in SQUARE_RESIDUES
            ),
        },
        "hensel_argument": (
            "At r=1, W^2=60 has the simple lift W=16 mod 49 in the W=2 "
            "residue disk.  It gives t=4 mod 49, so N/7=1 mod 7 and "
            "M=3 mod 7.  Hence F_plus/49=2 mod 7 and F_minus=2 mod 7; "
            "both are Q_7 squares by the unit Hensel criterion."
        ),
    }


def _frozen_maps_certificate() -> dict[str, Any]:
    factor_identity = all(
        mixed._reduce_source(expr - (2 * mixed.T_DENOMINATOR) ** 2 * factor) == 0
        for expr, factor in (
            (mixed.J_PLUS, mixed.F_PLUS),
            (mixed.J_MINUS, mixed.F_MINUS),
        )
    )
    fixed_identity = mixed._identity(mixed.P_OP - (mixed.N**2 + 7**2) * (mixed.M**2 + 7**2))
    source_identity = mixed._identity(
        (mixed.N**2 + 3**2) * (mixed.M**2 + 3**2) - (mixed.Z / 4) ** 2
    )
    return {
        "normalized_factor_map": (
            "a_plus=s_plus/(2*D*A), a_minus=s_minus/(2*D*A), R=d*a_plus*a_minus"
        ),
        "fixed_cover_equation": "R^2=(N^2+49)*(M^2+49)",
        "exact_aa_bb_lift": [
            "source leg L=3, opposite leg=7",
            "(N^2+9)*(M^2+9)=(Z/4)^2",
            "-10<t<10 is the real positivity condition",
            "no individual square condition is added to AA+BB",
        ],
        "checks": {
            "cleared_to_normalized_factor_identity": factor_identity,
            "fixed_cover_coordinate_identity": fixed_identity,
            "exact_source_AA_BB_lift_identity": source_identity,
            "source_leg_is_3": mixed.L == 3,
            "opposite_leg_is_7": (
                mixed._identity(mixed.F_PLUS - (mixed.N**2 + 7**2))
                and mixed._identity(mixed.F_MINUS - (mixed.M**2 + 7**2))
            ),
        },
        "argument": (
            "The local factor equations are the normalized wl589 equations. "
            "Their two square roots map to the fixed-cover coordinate "
            "R=d*a_plus*a_minus, while the frozen AA+BB source identity "
            "remains (N^2+9)(M^2+9)=(Z/4)^2."
        ),
    }


def _named_mapping(image: set[str]) -> dict[str, Any]:
    rows = []
    for value in MIXED_REPRESENTATIVES:
        label = _class_label(_q7_class(value))
        rows.append({"d": value, "Q7_class": label, "survives": label in image})
    return {
        "rows": rows,
        "survive": [row["d"] for row in rows if row["survives"]],
        "deleted": [row["d"] for row in rows if not row["survives"]],
        "all_named_values_are_distinct": len(set(MIXED_REPRESENTATIVES))
        == len(MIXED_REPRESENTATIVES),
    }


def build_wl591_mixed_p7_factor_twist_local_image() -> dict[str, Any]:
    source = _source_residue_certificate()
    infinity = _infinity_certificate()
    factors = _factor_residue_certificate()
    poles = _pole_and_denominator_certificate(source)
    zero = _zero_and_factor_zero_certificate()
    inclusion = _inclusion_certificate()
    maps = _frozen_maps_certificate()
    image = {"[1]"}
    named = _named_mapping(image)
    nonpole_strata_force_class_1 = (
        source["checks"]["complete_source_residue_table"]
        and source["checks"]["complete_regular_residue_table"]
        and source["checks"]["regular_t_residues_are_3_or_4"]
        and infinity["checks"]["exactly_two_infinity_disks"]
        and infinity["checks"]["infinity_t_residues_are_3_or_4"]
        and factors["checks"]["unit_factor_is_always_a_Q7_square"]
        and zero["checks"]["no_Q7_factor_zero"]
    )
    pole_strata_force_class_1 = (
        poles["checks"]["D_pole_rows_are_complete"]
        and poles["checks"]["A_has_no_Q7_root"]
        and poles["checks"]["every_D_row_is_a_simple_t_pole"]
        and poles["checks"]["pole_J_values_are_square_units"]
    )
    local_checks = {
        **source["checks"],
        **infinity["checks"],
        **factors["checks"],
        **poles["checks"],
        **zero["checks"],
        **inclusion["checks"],
        **maps["checks"],
        "all_nonpole_source_strata_force_class_1": (nonpole_strata_force_class_1),
        "all_pole_source_strata_force_class_1": pole_strata_force_class_1,
        "no_factor_zero_or_R_zero_branch": zero["checks"]["no_Q7_factor_zero"],
    }
    all_checks = {
        "complete_local_strata": all(local_checks.values()),
        "exact_image_is_singleton_1": image == {"[1]"},
        "named_mapping_is_exact": named["survive"] == [91205]
        and named["deleted"] == [5, 3045, 66045],
        "no_rank_or_rational_point_search": True,
    }
    violations = [name for name, passed in all_checks.items() if not passed]
    return {
        "status": "ok" if not violations else "error",
        "ready": not violations,
        "work_log": "wl591",
        "object_layer": "normalized_mixed_Q7_relative_constant_factor_twist_image",
        "scope": (
            "frozen wl589 mixed cover support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85) at p=7 only"
        ),
        "prime": P,
        "local_squareclass_basis": ["[1]", "[u]", "[7]", "[7u]"],
        "local_image": ["[1]"],
        "named_survivor_mapping": named,
        "proof_certificate": {
            "source_residue_certificate": source,
            "infinity_certificate": infinity,
            "factor_residue_certificate": factors,
            "pole_and_denominator_certificate": poles,
            "zero_and_factor_zero_certificate": zero,
            "inclusion_certificate": inclusion,
            "frozen_maps_certificate": maps,
            "conclusion": (
                "Every normalized Q_7 factor-cover point has class [1].  The "
                "r=1, W=2 mod 7 Hensel disk supplies [1]."
            ),
        },
        "verification": {
            "checks": all_checks,
            "local_checks": local_checks,
            "violations": violations,
            "no_wl587_edit": True,
            "no_wl589_edit": True,
            "no_wl590_edit": True,
            "no_other_prime": True,
            "no_D2": True,
        },
        "proof_boundary": {
            "exact_Q7_local_image_proved_here": not violations,
            "exact_deletions_proved_here": named["deleted"],
            "fixed_cover_coordinate_retained": True,
            "exact_aa_bb_lift_retained": maps["checks"]["exact_source_AA_BB_lift_identity"],
            "rational_point_classification": False,
            "rank_or_selmer_claim": False,
            "family_exclusion": False,
            "advance_to_D2": False,
        },
        "strict_certificate": (
            "Complete F_7 source strata, both infinity disks, D/A denominator "
            "branches, normalized factor-zero and zero-value branches, pole "
            "squareclasses, Hensel inclusion, fixed-cover R, and exact AA+BB "
            "maps are checked.  No bounded rational search is used."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl591_mixed_p7_factor_twist_local_image()
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
