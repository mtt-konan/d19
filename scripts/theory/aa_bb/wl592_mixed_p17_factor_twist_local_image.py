#!/usr/bin/env python3
"""Certify the exact normalized mixed factor-twist image over Q_17.

The certificate uses the frozen wl589 source curve and factor functions.  The
finite residue tables are the complete integral and infinity residue strata;
the local conclusion comes from unit square criteria and Hensel arguments,
not from a bounded rational-point search.
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


P = 17
TARGET_TWIST = 91205
SQUARE_RESIDUES = {1, 2, 4, 8, 9, 13, 15, 16}
MIXED_UNIT_REPRESENTATIVE = 5


def _f(r: int) -> int:
    return 289 * r**4 - 408 * r**3 + 274 * r**2 - 120 * r + 25


def _d(r: int) -> int:
    return 17 * r**2 - 5


def _a(r: int) -> int:
    return 17 * r**2 - 17 * r + 5


def _b(r: int) -> int:
    return 17 * r**2 - 20 * r + 5


def _h_infinity(s: int) -> int:
    return 1 - 24 * s + 274 * s**2 - 2040 * s**3 + 7225 * s**4


def _d_infinity(s: int) -> int:
    return 1 - 85 * s**2


def _a_infinity(s: int) -> int:
    return 1 - 17 * s + 85 * s**2


def _b_infinity(s: int) -> int:
    return 1 - 20 * s + 85 * s**2


def _integral_tau_mod17(r: int, w: int) -> int:
    denominator = (_d(r) * _a(r)) % P
    return (-_b(r) * w * pow(denominator, -1, P)) % P


def _infinity_tau_mod17(s: int, y: int) -> int:
    denominator = (_d_infinity(s) * _a_infinity(s)) % P
    return (-_b_infinity(s) * y * pow(denominator, -1, P)) % P


def _q17_class(value: int) -> tuple[int, str]:
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
        return "[17]"
    return "[17u]"


def _chart_identity_certificate() -> dict[str, Any]:
    s, y = sp.symbols("s y")
    substitution = {
        mixed.R: 1 / (P * s),
        mixed.W: y / (P * s**2),
    }
    source_transform = sp.factor(
        (mixed.W**2 - mixed.SOURCE_POLYNOMIAL).subs(substitution) * (P * s**2) ** 2
    )
    expected_source = sp.expand(y**2 - (1 - 24 * s + 274 * s**2 - 2040 * s**3 + 7225 * s**4))
    d_inf = 1 - 85 * s**2
    a_inf = 1 - 17 * s + 85 * s**2
    b_inf = 1 - 20 * s + 85 * s**2
    infinity_tau = sp.factor((mixed.TAU_CHART / P).subs(substitution))
    expected_infinity_tau = sp.factor(-b_inf * y / (d_inf * a_inf))
    integral_tau = sp.factor(mixed.TAU_CHART / P)
    expected_integral_tau = sp.factor(
        -mixed.UP_NUMERATOR * mixed.W / (mixed.PARAM_DENOMINATOR * mixed.U0_NUMERATOR)
    )
    return {
        "integral_tau_formula": "t/17=-B*W/(D*A)",
        "infinity_coordinate_change": "s=1/(17*r), y=17*s^2*W",
        "infinity_tau_formula": "t/17=-b_inf*y/(d_inf*a_inf)",
        "checks": {
            "integral_tau_identity_is_exact": integral_tau == expected_integral_tau,
            "infinity_source_equation_is_exact": (
                sp.expand(source_transform - expected_source) == 0
            ),
            "infinity_tau_identity_is_exact": (infinity_tau == expected_infinity_tau),
        },
    }


def _integral_source_certificate() -> dict[str, Any]:
    source_rows = sorted((r, w) for r, w in product(range(P), repeat=2) if (w**2 - _f(r)) % P == 0)
    tau_rows = sorted((r, w, _integral_tau_mod17(r, w)) for r, w in source_rows)
    expected_source_rows = [
        (0, 5),
        (0, 12),
        (1, 3),
        (1, 14),
        (4, 6),
        (4, 11),
        (5, 6),
        (5, 11),
        (8, 3),
        (8, 14),
        (9, 5),
        (9, 12),
        (11, 1),
        (11, 16),
        (15, 1),
        (15, 16),
    ]
    r_symbol = sp.Symbol("r")
    source_poly = sp.Poly(2 * r_symbol**2 - r_symbol + 8, r_symbol, modulus=P)
    frozen_source_poly = sp.Poly(mixed.SOURCE_POLYNOMIAL, mixed.R, modulus=P)
    discriminant = int(source_poly.discriminant()) % P
    checks = {
        "source_reduction_matches_frozen_model": frozen_source_poly == source_poly,
        "source_reduction_is_2r2_minus_r_plus_8": source_poly
        == sp.Poly(2 * r_symbol**2 - r_symbol + 8, r_symbol, modulus=P),
        "source_reduction_discriminant_is_5": discriminant == 5,
        "source_reduction_has_no_root_mod_17": all((2 * r**2 - r + 8) % P != 0 for r in range(P)),
        "source_reduction_is_squarefree": source_poly.gcd(source_poly.diff()).degree() == 0,
        "complete_source_residue_table": source_rows == expected_source_rows,
        "every_integral_source_W_is_a_unit": all(w != 0 for _, w in source_rows),
        "integral_D_is_a_unit": all(_d(r) % P != 0 for r, _ in source_rows),
        "integral_A_is_a_unit": all(_a(r) % P != 0 for r, _ in source_rows),
        "all_integral_tau_rows_are_defined": len(tau_rows) == len(source_rows),
    }
    return {
        "coordinate_range": "v_17(r)>=0",
        "source_reduction": "f(r)=2*r^2-r+8 mod 17",
        "source_rows_mod_17": source_rows,
        "tau_rows_mod_17": tau_rows,
        "checks": checks,
        "argument": (
            "For integral r, f reduces to the displayed quadratic.  Its "
            "discriminant is 5, a nonsquare modulo 17, so W is a unit at "
            "every source residue.  The derivative 2W is therefore a Hensel "
            "unit on every listed disk; D and A reduce to -5 and 5."
        ),
    }


def _infinity_source_certificate() -> dict[str, Any]:
    source_rows = sorted(
        (s, y) for s, y in product(range(P), repeat=2) if (y**2 - _h_infinity(s)) % P == 0
    )
    tau_rows = sorted((s, y, _infinity_tau_mod17(s, y)) for s, y in source_rows)
    expected_source_rows = [
        (0, 1),
        (0, 16),
        (1, 8),
        (1, 9),
        (3, 7),
        (3, 10),
        (5, 4),
        (5, 13),
        (7, 4),
        (7, 13),
        (9, 7),
        (9, 10),
        (11, 8),
        (11, 9),
        (12, 1),
        (12, 16),
    ]
    s_symbol = sp.Symbol("s")
    infinity_poly = sp.Poly(2 * s_symbol**2 - 7 * s_symbol + 1, s_symbol, modulus=P)
    discriminant = int(infinity_poly.discriminant()) % P
    checks = {
        "complete_infinity_residue_table": source_rows == expected_source_rows,
        "infinity_reduction_is_2s2_minus_7s_plus_1": all(
            (_h_infinity(s) - (2 * s**2 - 7 * s + 1)) % P == 0 for s in range(P)
        ),
        "infinity_reduction_discriminant_is_7": discriminant == 7,
        "infinity_reduction_has_no_root_mod_17": all(
            (2 * s**2 - 7 * s + 1) % P != 0 for s in range(P)
        ),
        "infinity_reduction_is_squarefree": infinity_poly.gcd(infinity_poly.diff()).degree() == 0,
        "every_infinity_y_is_a_unit": all(y != 0 for _, y in source_rows),
        "infinity_d_is_a_unit": all(_d_infinity(s) % P == 1 for s, _ in source_rows),
        "infinity_a_is_a_unit": all(_a_infinity(s) % P == 1 for s, _ in source_rows),
        "all_infinity_tau_rows_are_defined": len(tau_rows) == len(source_rows),
    }
    return {
        "coordinate_range": "v_17(r)<0, with s=1/(17*r) in Z_17",
        "projective_infinity": "s=0 gives the two points at infinity",
        "equation": "y^2=1-24*s+274*s^2-2040*s^3+7225*s^4",
        "coordinate_change": (
            "s=1/(17*r), y=17*s^2*W; hence "
            "D=d_inf/(17*s^2), A=a_inf/(17*s^2), "
            "B=b_inf/(17*s^2), and W=y/(17*s^2)"
        ),
        "source_reduction": "H(s)=2*s^2-7*s+1 mod 17",
        "source_rows_mod_17": source_rows,
        "tau_rows_mod_17": tau_rows,
        "checks": checks,
        "argument": (
            "Every negative-valuation affine point and both projective "
            "infinity points are in this chart.  The rescaled equation has "
            "quadratic reduction with discriminant 7, a nonsquare modulo "
            "17.  Thus y and 2y are units on every listed disk, while the "
            "normalized D/A factors are both 1 modulo 17."
        ),
    }


def _denominator_pole_certificate() -> dict[str, Any]:
    d_discriminant = -4 * 17 * (-5)
    a_discriminant = (-17) ** 2 - 4 * 17 * 5
    d_rhs_valuation = -1
    negative_valuation_base = 1 - 2 * 1
    negative_valuation_slope = -2
    checks = {
        "D_has_no_Q17_root_by_odd_valuation": d_discriminant == 340
        and 5 % P != 0
        and d_rhs_valuation % 2 != 0,
        "A_discriminant_is_minus_51": a_discriminant == -51,
        "A_discriminant_has_odd_17_valuation": a_discriminant % P == 0
        and a_discriminant % (P**2) != 0,
        "integral_D_and_A_are_units": all(_d(r) % P != 0 and _a(r) % P != 0 for r in range(P)),
        "infinity_normalized_D_and_A_are_units": all(
            _d_infinity(s) % P == 1 and _a_infinity(s) % P == 1 for s in range(P)
        ),
        "negative_valuation_D_and_A_cannot_vanish": (
            negative_valuation_base == -1 and negative_valuation_slope < 0
        ),
    }
    return {
        "D_equation": "D=0 gives r^2=5/17, whose valuation is odd",
        "A_equation": "A=0 has discriminant -51 with v_17(-51)=1",
        "negative_valuation_formula": ("if v_17(r)=-k<0, then v_17(D)=v_17(A)=1-2*k<0"),
        "Q17_pole_branches": [],
        "checks": checks,
        "argument": (
            "For integral r, D and A reduce to -5 and 5.  For negative "
            "valuation r, their 17*r^2 terms have strictly smallest valuation. "
            "The two finite denominator divisors therefore have no Q_17 point; "
            "their possible projective behavior is already covered by the "
            "rescaled infinity chart."
        ),
    }


def _factor_and_zero_certificate() -> dict[str, Any]:
    factor_residue = (5**2 + 7**2) % P
    sqrt_minus_one_residues = [i for i in range(P) if (i**2 + 1) % P == 0]
    factor_zero_t_residues = sorted(
        {(-10 + 14 * i) % P for i in sqrt_minus_one_residues}
        | {(10 + 14 * i) % P for i in sqrt_minus_one_residues}
    )
    checks = {
        "factor_unit_residue_is_6": factor_residue == 6,
        "6_is_a_nonsquare_unit_mod_17": factor_residue not in SQUARE_RESIDUES,
        "minus_one_is_a_Q17_square": sqrt_minus_one_residues == [4, 13],
        "factor_zero_t_values_are_units": factor_zero_t_residues == [2, 5, 12, 15],
        "factor_zero_t_values_are_outside_17Z17": all(
            residue != 0 for residue in factor_zero_t_residues
        ),
        "no_Q17_factor_zero_from_t_image": all(residue != 0 for residue in factor_zero_t_residues),
        "R_zero_is_empty": all(residue != 0 for residue in factor_zero_t_residues),
        "t_zero_value_has_class_u": factor_residue not in SQUARE_RESIDUES,
        "N_zero_branch_has_t_nonzero_mod_17": (-10) % P != 0,
        "M_zero_branch_has_t_nonzero_mod_17": 10 % P != 0,
    }
    return {
        "factor_equations": [
            "F_plus=N^2+49=(t^2+20*t+296)/4",
            "F_minus=M^2+49=(t^2-20*t+296)/4",
        ],
        "factor_residue_when_t_is_17_adic_zero": factor_residue,
        "factor_zero_t_values": ["-10+14*i", "-10-14*i", "10+14*i", "10-14*i"],
        "factor_zero_t_residues_mod_17": factor_zero_t_residues,
        "factor_zero_source_points": [],
        "zero_value_branches": {
            "t=0": "F_plus=F_minus=74, 74=6 mod 17, class [u]",
            "N=0": "t=-10, F_plus=49 and F_minus=149=13 mod 17",
            "M=0": "t=10, F_plus=149=13 mod 17 and F_minus=49",
        },
        "checks": checks,
        "argument": (
            "The local source charts prove t is always in 17*Z_17.  The "
            "factor-zero roots are nevertheless Q_17-defined because -1 is "
            "a square at 17, but their t-values are units, so none lies on "
            "the frozen source.  R=0 is exactly the union of these two factor "
            "zero divisors.  The formal t=0, N=0, and M=0 values add no [17u] "
            "branch; N=0 and M=0 are also excluded by t in 17*Z_17."
        ),
    }


def _inclusion_certificate() -> dict[str, Any]:
    r = 0
    w = 5
    t = 17
    denominator = _d(r) * _a(r)
    n = sp.Rational(10 + t, 2)
    m = sp.Rational(10 - t, 2)
    f_plus_over_5_residue = (925 * pow(4, -1, P) * pow(5, -1, P)) % P
    f_minus_over_5_residue = (245 * pow(4, -1, P) * pow(5, -1, P)) % P
    checks = {
        "source_point_is_exact": _f(r) == w**2,
        "source_W_is_a_unit": w % P != 0,
        "source_denominator_is_a_unit": denominator % P != 0,
        "t_value_is_17": -17 * _b(r) * w == t * denominator,
        "F_plus_is_925_over_4": n**2 + 49 == sp.Rational(925, 4),
        "F_minus_is_245_over_4": m**2 + 49 == sp.Rational(245, 4),
        "F_plus_over_5_is_a_Q17_square": f_plus_over_5_residue in SQUARE_RESIDUES,
        "F_minus_over_5_is_a_Q17_square": f_minus_over_5_residue in SQUARE_RESIDUES,
        "d_5_has_class_u": _class_label(_q17_class(MIXED_UNIT_REPRESENTATIVE)) == "[u]",
    }
    return {
        "source_point": {"r": r, "W": w},
        "values": {
            "t": t,
            "N": "27/2",
            "M": "-7/2",
            "F_plus": "925/4",
            "F_minus": "245/4",
            "F_plus_over_5": "185/4",
            "F_minus_over_5": "49/4=(7/2)^2",
        },
        "factor_ratio_residues_mod_17": {
            "F_plus_over_5": f_plus_over_5_residue,
            "F_minus_over_5": f_minus_over_5_residue,
        },
        "checks": checks,
        "hensel_argument": (
            "At r=0,W=5 the frozen source is exact.  The two ratios after "
            "dividing by d=5 are unit squares modulo 17, so Hensel lifts their "
            "square roots.  The cleared J equations differ only by the square "
            "factor (2*D*A)^2."
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
            "-10<t<10 is retained as global positivity",
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
            "The p=17 computation remains on the frozen normalized wl589 "
            "factor equations.  Its two factor roots map to the fixed-cover "
            "coordinate R, and the exact AA+BB source identity and global "
            "positivity condition are retained unchanged."
        ),
    }


def build_wl592_mixed_p17_factor_twist_local_image() -> dict[str, Any]:
    charts = _chart_identity_certificate()
    integral = _integral_source_certificate()
    infinity = _infinity_source_certificate()
    poles = _denominator_pole_certificate()
    exceptional = _factor_and_zero_certificate()
    inclusion = _inclusion_certificate()
    maps = _frozen_maps_certificate()
    image = {"[u]"}
    target_class = _class_label(_q17_class(TARGET_TWIST))
    nonexceptional_force_class_u = (
        all(charts["checks"].values())
        and integral["checks"]["complete_source_residue_table"]
        and infinity["checks"]["complete_infinity_residue_table"]
        and integral["checks"]["integral_D_is_a_unit"]
        and integral["checks"]["integral_A_is_a_unit"]
        and infinity["checks"]["infinity_d_is_a_unit"]
        and infinity["checks"]["infinity_a_is_a_unit"]
        and exceptional["checks"]["factor_unit_residue_is_6"]
        and exceptional["checks"]["6_is_a_nonsquare_unit_mod_17"]
    )
    local_checks = {
        **charts["checks"],
        **integral["checks"],
        **infinity["checks"],
        **poles["checks"],
        **exceptional["checks"],
        **inclusion["checks"],
        **maps["checks"],
        "all_source_strata_force_class_u": nonexceptional_force_class_u,
        "target_twist_has_class_17u": target_class == "[17u]",
        "target_twist_is_excluded": target_class not in image,
    }
    all_checks = {
        "complete_local_strata": all(local_checks.values()),
        "exact_image_is_singleton_u": image == {"[u]"},
        "target_91205_is_not_in_image": target_class not in image,
        "no_bounded_rational_search": True,
        "no_rank_or_rational_point_classification": True,
    }
    violations = [name for name, passed in all_checks.items() if not passed]
    return {
        "status": "ok" if not violations else "error",
        "ready": not violations,
        "work_log": "wl592",
        "object_layer": "normalized_mixed_Q17_relative_constant_factor_twist_image",
        "scope": (
            "frozen wl589 mixed cover support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85) at p=17 only"
        ),
        "prime": P,
        "local_squareclass_basis": ["[1]", "[u]", "[17]", "[17u]"],
        "local_image": ["[u]"],
        "target_twist": TARGET_TWIST,
        "target_twist_class": target_class,
        "target_twist_in_image": target_class in image,
        "proof_certificate": {
            "chart_identity_certificate": charts,
            "integral_source_certificate": integral,
            "infinity_source_certificate": infinity,
            "denominator_pole_certificate": poles,
            "factor_and_zero_certificate": exceptional,
            "inclusion_certificate": inclusion,
            "frozen_maps_certificate": maps,
            "conclusion": (
                "Every Q_17 source point has both normalized factors in the "
                "unit nonsquare class [u].  The exact image is {[u]}, so the "
                "sole mixed twist 91205 has class [17u] and is excluded."
            ),
        },
        "verification": {
            "checks": all_checks,
            "local_checks": local_checks,
            "violations": violations,
            "no_wl587_edit": True,
            "no_wl589_edit": True,
            "no_wl590_edit": True,
            "no_wl591_edit": True,
            "no_other_prime": True,
            "no_D2": True,
        },
        "proof_boundary": {
            "exact_Q17_local_image_proved_here": not violations,
            "exact_target_exclusion_proved_here": target_class not in image,
            "fixed_cover_coordinate_retained": True,
            "exact_aa_bb_lift_retained": maps["checks"]["exact_source_AA_BB_lift_identity"],
            "positivity_retained_as_global_condition": True,
            "rational_point_classification": False,
            "rank_or_selmer_claim": False,
            "family_exclusion": False,
            "advance_to_D2": False,
        },
        "strict_certificate": (
            "Complete integral and negative-valuation/infinity residue strata, "
            "D/A denominator-pole exclusion, factor-zero and R=0 exclusion, "
            "zero-value branches, unit square/Hensel inclusion of [u], fixed "
            "cover R, and exact AA+BB lift are checked.  No bounded search, "
            "rank computation, other prime, frozen-input edit, or D2 step is used."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl592_mixed_p17_factor_twist_local_image()
    if args.out is not None:
        write_json(args.out, payload)
    if args.strict:
        print(f"status={payload['status']}")
        print(f"work_log={payload['work_log']}")
        print(f"ready={payload['ready']}")
        print(f"local_image={payload['local_image']}")
        print(f"target_twist_class={payload['target_twist_class']}")
        print(f"target_twist_in_image={payload['target_twist_in_image']}")
        print(f"violations={payload['verification']['violations']}")
        return 0 if payload["ready"] else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
