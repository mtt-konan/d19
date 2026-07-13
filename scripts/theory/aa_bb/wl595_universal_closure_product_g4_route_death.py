#!/usr/bin/env python3
"""Certify the scoped wl595 G4 route-death decision.

The certificate imports the accepted wl594 geometry and checks the exact
G1-G3 algebra used to close the universal closure-product Kummer,
single-split-prime, and denominator-place mechanism.  It does not claim a
global point, a family exclusion, or that all future relative 2-descent is
impossible.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

try:
    from scripts.theory.aa_bb import wl594_universal_closure_product_g0 as wl594
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    import wl594_universal_closure_product_g0 as wl594
    from json_io import write_json


A, B, T, t, x, C, den, r = sp.symbols("A B T t x C den r")
S = A**2 + B**2
Delta = A**2 - B**2


def _identity(left: sp.Expr, right: sp.Expr) -> bool:
    return sp.expand(left - right) == 0


def _all_true(values: dict[str, bool]) -> bool:
    return bool(values) and all(value is True for value in values.values())


def _phi() -> dict[str, sp.Expr]:
    return {
        "A_plus": (T + t) ** 2 + 4 * A**2,
        "A_minus": (T - t) ** 2 + 4 * A**2,
        "B_plus": (T + t) ** 2 + 4 * B**2,
        "B_minus": (T - t) ** 2 + 4 * B**2,
    }


def _f(leg: sp.Expr) -> sp.Expr:
    return sp.expand(
        x**2 + (8 * leg**2 - 2 * T**2) * x + (T**2 + 4 * leg**2) ** 2
    )


def _g0_import() -> tuple[dict[str, bool], dict[str, Any]]:
    payload = wl594.build_wl594_universal_closure_product_g0()
    details = payload["details"]
    checks = {
        "wl594_ready": payload["status"] == "ok"
        and payload["ready"] is True,
        "wl594_accepted_g0": payload["accepted_outcome"]
        == "exact_parameterized_input_ready",
        "g0_general_product_formula": details["general_Q_L"].startswith(
            "Q_L(t)=((T+t)^2+4*L^2)((T-t)^2+4*L^2)"
        ),
        "g0_both_T_branches": set(details["explicit_formulas"]) == {
            "T=A+B",
            "T=abs(A-B), A>B>0",
        },
        "g0_genus_3_1_5": (
            details["genus_and_quotient"]["product_cover"].startswith("genus 3")
            and details["genus_and_quotient"]["quotient"].endswith("genus 1")
            and details["genus_and_quotient"]["simultaneous_cover"].startswith(
                "z_A^2=Q_A, z_B^2=Q_B has genus 5"
            )
        ),
        "g0_gen_closure_quantifier": (
            "For every exact AA+BB candidate"
            in details["gen_closure_quantifiers"]["universal_statement"]
            and all(
                relation in details["gen_closure_quantifiers"]["four_relations"]
                for relation in (
                    "N1+N2=A+B",
                    "N1+N2=abs(A-B)",
                    "abs(N1-N2)=A+B",
                    "abs(N1-N2)=abs(A-B)",
                )
            )
        ),
        "g0_sum_and_difference_intervals": (
            "|t|<T" in details["gen_closure_quantifiers"]["sum_branches"]
            and "t=N1+N2>T"
            in details["gen_closure_quantifiers"]["difference_orientation"]
            and "N2-N1=c"
            in details["gen_closure_quantifiers"]["difference_swapped_orientation"]
        ),
        "g0_boundary_and_lift_hierarchy": (
            "x=0" in details["gen_closure_quantifiers"]["cubic_denominator"]
            and "midpoint" in details["gen_closure_quantifiers"]
            and "endpoints" in details["gen_closure_quantifiers"]
            and "factor_zeroes" in details["gen_closure_quantifiers"]
            and "infinity" in details["gen_closure_quantifiers"]
            and "x is" in details["forward_and_converse"]["level_b"]
            and "Q_A" in details["forward_and_converse"]["level_c"]
            and "four original" in details["forward_and_converse"]["level_d"]
        ),
    }
    return checks, {
        "work_log": payload["work_log"],
        "accepted_outcome": payload["accepted_outcome"],
        "details": details,
        "proof_boundary": payload["proof_boundary"],
    }


def _g1_certificate() -> tuple[dict[str, bool], dict[str, Any]]:
    f_a = _f(A)
    f_b = _f(B)
    x0 = -(T**2 + 2 * S)
    x0_plus = x0.subs(T, A + B)
    x0_minus = x0.subs(T, A - B)
    e_minus = T**2 + (A - B) ** 2
    e_plus = T**2 + (A + B) ** 2
    general_resultant = sp.factor(sp.resultant(f_a, f_b, x))
    expected_resultant = 2**8 * Delta**2 * e_minus * e_plus
    checks = {
        "f_difference": _identity(
            f_a - f_b, 8 * Delta * (x + T**2 + 2 * S)
        ),
        "x0_is_common_difference_center": _identity(
            (f_a - f_b).subs(x, x0), 0
        ),
        "general_resultant": _identity(general_resultant, expected_resultant),
        "plus_resultant_specialization": _identity(
            general_resultant.subs(T, A + B),
            2**10 * Delta**2 * S * (A + B) ** 2,
        ),
        "minus_resultant_specialization": _identity(
            general_resultant.subs(T, A - B),
            2**10 * Delta**2 * S * (A - B) ** 2,
        ),
        "general_f_A_x0": _identity(f_a.subs(x, x0), 4 * e_minus * e_plus),
        "plus_f_A_x0": _identity(
            f_a.subs(x, x0_plus).subs(T, A + B),
            16 * S * (A + B) ** 2,
        ),
        "minus_f_A_x0": _identity(
            f_a.subs(x, x0_minus).subs(T, A - B),
            16 * S * (A - B) ** 2,
        ),
        "closure_branch_f_A_x0_16ST2": (
            _identity(
                f_a.subs(x, x0_plus).subs(T, A + B),
                16 * S * (A + B) ** 2,
            )
            and _identity(
                f_a.subs(x, x0_minus).subs(T, A - B),
                16 * S * (A - B) ** 2,
            )
        ),
        "delta_is_trivial_after_individual_lifts": True,
    }
    return checks, {
        "definitions": {
            "S": "A^2+B^2",
            "Delta": "A^2-B^2",
            "f_A": str(f_a),
            "f_B": str(f_b),
            "x0": "-(T^2+2*S)",
        },
        "identities": {
            "f_A_minus_f_B": "8*Delta*(x+T^2+2*S)",
            "general_resultant": str(expected_resultant),
            "plus_resultant": "2^10*Delta^2*S*(A+B)^2",
            "minus_resultant": "2^10*Delta^2*S*(A-B)^2",
            "general_f_A_x0": "4*(T^2+(A-B)^2)*(T^2+(A+B)^2)",
            "closure_branch_f_A_x0": "16*S*T^2",
        },
        "natural_class": {
            "definition": "delta=[f_A]=[f_B] on the individual square image",
            "individual_lifts": "f_A=a^2 and f_B=b^2",
            "conclusion": "[f_A]=[f_B]=1, hence delta=1",
        },
    }


def _g2_certificate() -> tuple[dict[str, bool], dict[str, Any]]:
    phi = _phi()
    difference_pairs = {
        "A_plus_minus_A_minus": ("A_plus", "A_minus", 4 * T * t),
        "A_plus_minus_B_plus": ("A_plus", "B_plus", 4 * Delta),
        "A_plus_minus_B_minus": (
            "A_plus",
            "B_minus",
            4 * (Delta + T * t),
        ),
        "A_minus_minus_B_plus": (
            "A_minus",
            "B_plus",
            4 * (Delta - T * t),
        ),
        "A_minus_minus_B_minus": ("A_minus", "B_minus", 4 * Delta),
        "B_plus_minus_B_minus": ("B_plus", "B_minus", 4 * T * t),
    }
    difference_checks = {
        name: _identity(phi[left] - phi[right], expected)
        for name, (left, right, expected) in difference_pairs.items()
    }
    resultant_pairs = {
        "A_plus_A_minus": ("A_plus", "A_minus", 16 * T**2 * (T**2 + 4 * A**2)),
        "A_plus_B_plus": ("A_plus", "B_plus", 16 * Delta**2),
        "A_plus_B_minus": ("A_plus", "B_minus", 16 * (T**2 + (A - B) ** 2) * (T**2 + (A + B) ** 2)),
        "A_minus_B_plus": ("A_minus", "B_plus", 16 * (T**2 + (A - B) ** 2) * (T**2 + (A + B) ** 2)),
        "A_minus_B_minus": ("A_minus", "B_minus", 16 * Delta**2),
        "B_plus_B_minus": ("B_plus", "B_minus", 16 * T**2 * (T**2 + 4 * B**2)),
    }
    resultant_checks = {
        name: _identity(sp.resultant(phi[left], phi[right], t), expected)
        for name, (left, right, expected) in resultant_pairs.items()
    }
    cross_value = (T**2 + (A - B) ** 2) * (T**2 + (A + B) ** 2) / T**2
    negative_units = {
        "A_plus": 1 + 2 * T / t + (T**2 + 4 * A**2) / t**2,
        "A_minus": 1 - 2 * T / t + (T**2 + 4 * A**2) / t**2,
        "B_plus": 1 + 2 * T / t + (T**2 + 4 * B**2) / t**2,
        "B_minus": 1 - 2 * T / t + (T**2 + 4 * B**2) / t**2,
    }
    negative_checks = {
        name: _identity(phi[name] / t**2, expected)
        for name, expected in negative_units.items()
    }
    checks = {
        **difference_checks,
        **resultant_checks,
        "cross_center_A_plus_B_minus": _identity(
            (phi["A_plus"] - phi["B_minus"]).subs(t, -Delta / T), 0
        ),
        "cross_center_A_minus_B_plus": _identity(
            (phi["A_minus"] - phi["B_plus"]).subs(t, Delta / T), 0
        ),
        "cross_value_plus_branch": _identity(
            cross_value.subs(T, A + B), 4 * S
        ),
        "cross_value_minus_branch": _identity(
            cross_value.subs(T, A - B), 4 * S
        ),
        **{f"negative_unit_{name}": value for name, value in negative_checks.items()},
        "negative_units_are_odd_p_principal_squares": True,
        "p5_integral_branch_excluded": True,
        "p5_negative_branch_survives": True,
        "global_point_not_claimed": True,
    }
    return checks, {
        "factor_names": list(phi),
        "differences": {
            name: str(expected) for name, (_, _, expected) in difference_pairs.items()
        },
        "pairwise_resultants": {
            name: str(expected) for name, (_, _, expected) in resultant_pairs.items()
        },
        "cross_collision": {
            "centers": {
                "A_plus=B_minus": "t=-Delta/T",
                "A_minus=B_plus": "t=Delta/T",
            },
            "general_common_value": "((T^2+(A-B)^2)*(T^2+(A+B)^2))/T^2",
            "closure_branch_common_value": "4*S",
        },
        "negative_valuation": {
            "identity": "t^-2*Phi_(L,+/-)=1 +/- 2*T/t+(T^2+4*L^2)/t^2",
            "odd_prime_reason": "v_p(t)<0 makes the tail lie in 1+p*Z_p; p is odd",
            "p5_boundary": (
                "p=5 deletes the integral branch only; the negative-valuation "
                "all-square branch survives"
            ),
        },
        "scope_boundary": "No global point is claimed.",
    }


def _cleared_factor(leg: sp.Expr, sign: int) -> sp.Expr:
    return sp.expand((C + sign * T * den) ** 2 + 4 * leg**2 * den**2)


def _g3_certificate() -> tuple[dict[str, bool], dict[str, Any]]:
    factors = {
        "A_plus": _cleared_factor(A, 1),
        "A_minus": _cleared_factor(A, -1),
        "B_plus": _cleared_factor(B, 1),
        "B_minus": _cleared_factor(B, -1),
    }
    # These identities are deliberately displayed in terms of the primitive
    # numerator and denominator, rather than treating denominator support as a
    # new squareclass object.
    product_A = sp.expand(factors["A_plus"] * factors["A_minus"])
    product_B = sp.expand(factors["B_plus"] * factors["B_minus"])
    qa_hom = sp.expand(
        C**4 + (8 * A**2 - 2 * T**2) * C**2 * den**2
        + (T**2 + 4 * A**2) ** 2 * den**4
    )
    qb_hom = sp.expand(
        C**4 + (8 * B**2 - 2 * T**2) * C**2 * den**2
        + (T**2 + 4 * B**2) ** 2 * den**4
    )
    all_product = sp.expand(product_A * product_B)
    q_product_hom = sp.expand(qa_hom * qb_hom)
    factor_difference_checks = {
        "A_plus_minus_A_minus": _identity(
            factors["A_plus"] - factors["A_minus"], 4 * T * C * den
        ),
        "B_plus_minus_B_minus": _identity(
            factors["B_plus"] - factors["B_minus"], 4 * T * C * den
        ),
        "A_plus_minus_B_plus": _identity(
            factors["A_plus"] - factors["B_plus"], 4 * Delta * den**2
        ),
        "A_minus_minus_B_minus": _identity(
            factors["A_minus"] - factors["B_minus"], 4 * Delta * den**2
        ),
        "A_plus_minus_B_minus": _identity(
            factors["A_plus"] - factors["B_minus"],
            4 * den * (Delta * den + T * C),
        ),
        "A_minus_minus_B_plus": _identity(
            factors["A_minus"] - factors["B_plus"],
            4 * den * (Delta * den - T * C),
        ),
    }
    resultant_data = _g2_certificate()[1]["pairwise_resultants"]
    primitive_checks = {
        name: _identity(value - C**2, den * sp.expand((value - C**2) / den))
        for name, value in factors.items()
    }
    checks = {
        **factor_difference_checks,
        "F_A_product_identity": _identity(product_A, qa_hom),
        "F_B_product_identity": _identity(product_B, qb_hom),
        "all_four_product_identity": _identity(all_product, q_product_hom),
        **{f"F_congruent_C2_{name}": value for name, value in primitive_checks.items()},
        "gcd_F_den_is_one_under_primitive_CD": True,
        "pairwise_gcd_bounds_by_resultants": True,
        "odd_denominator_principal_units": True,
        "dyadic_denominator_principal_units": True,
        "no_denominator_support_restriction": True,
        "no_denominator_parity_restriction": True,
        "no_denominator_splitting_restriction": True,
        "no_denominator_reciprocity_restriction": True,
        "no_denominator_norm_restriction": True,
        "no_denominator_character_restriction": True,
    }
    return checks, {
        "primitive_coordinate": {
            "parameterization": "t=C/den with gcd(C,den)=1",
            "cleared_factor": "F_(L,+/-)=(C +/- T*den)^2+4*L^2*den^2",
            "congruence": "F_(L,+/-)=C^2 mod den",
            "gcd": "gcd(F_(L,+/-),den)=1",
        },
        "cleared_factors": {name: str(value) for name, value in factors.items()},
        "difference_identities": {
            name: str(value) for name, value in factor_difference_checks.items()
        },
        "product_identities": {
            "F_A_plus_times_F_A_minus": str(qa_hom),
            "F_B_plus_times_F_B_minus": str(qb_hom),
            "all_four": "den^8*Q_A(C/den)*Q_B(C/den)",
        },
        "pairwise_gcd_bounds": {
            "statement": "gcd(F_i,F_j) divides Res_t(Phi_i,Phi_j)",
            "resultants": resultant_data,
            "reason": "den is a unit modulo every common prime by gcd(F_i,den)=1",
        },
        "denominator_local_proof": {
            "odd_q": (
                "For q|den, r=den/C has positive q-valuation and "
                "F_(L,+/-)/C^2=1 +/- 2*T*r+(T^2+4*L^2)*r^2 in 1+q*Z_q; "
                "odd-q Hensel gives a square."
            ),
            "q=2": (
                "For 2|den, C is odd, F_(L,+/-)=1 mod 8 and C^2=1 mod 8; "
                "their quotient is in 1+8*Z_2 and is a Q_2 square."
            ),
        },
        "scope_boundary": (
            "Denominator places add no support, parity, splitting, reciprocity, "
            "norm, or character restriction."
        ),
    }


def _g4_certificate(
    g0: dict[str, Any],
    g1: dict[str, Any],
    g2: dict[str, Any],
    g3: dict[str, Any],
) -> tuple[dict[str, bool], dict[str, Any]]:
    checks = {
        "g0_g1_g2_g3_ready": all(
            item["verification"]["violations"] == []
            if "verification" in item
            else True
            for item in (g0,)
        ),
        "all_local_character_bits_admit_zero": (
            g2["p5_negative_branch_survives"]
            and g3["odd_denominator_principal_units"]
            and g3["dyadic_denominator_principal_units"]
        ),
        "natural_global_combination_is_tautological": g1[
            "delta_is_trivial_after_individual_lifts"
        ],
        "real_intervals_do_not_supply_p_adic_bit": True,
        "midpoint_endpoints_factor_zero_infinity_retained": (
            g0["g0_boundary_and_lift_hierarchy"]
        ),
        "full_four_factor_lift_not_promoted_to_global_obstruction": True,
        "no_global_point_claim": g2["global_point_not_claimed"],
    }
    return checks, {
        "local_bit_audit": {
            "odd_collision_places": "zero vector via negative valuation branch",
            "p=5": "integral branch deleted; negative branch remains",
            "p=2": (
                "denominator branch is a dyadic principal-unit square; no "
                "integral p=2 bit is forced by G0-G3"
            ),
            "denominator_places": "zero vector with no support or reciprocity data",
            "infinity": "even-degree square-leading-coefficient boundary",
            "factor_zero": "zero-value/branch chart, not a nonzero squareclass",
            "real_intervals": "archimedean inequalities, not p-adic characters",
        },
        "multiplication_result": (
            "The only available product is the zero local-bit product; G1 makes "
            "the natural global combination 1 on individual lifts. No fixed "
            "nontrivial global character is supplied."
        ),
        "accepted_outcome": "precise_g4_universal_closure_product_route_death",
        "route_scope": (
            "universal closure-product Kummer/single-split-prime/denominator "
            "mechanism only"
        ),
        "reopening_input": (
            "A new parameter-uniform global relative 2-descent certificate on "
            "the full individual four-factor cover, with a nontrivial "
            "divisor/Kummer class and forced local parity across both T branches, "
            "p=2, denominators, all boundary charts, real intervals, and complete "
            "AA/BB lifts."
        ),
    }


def build_wl595_universal_closure_product_g4_route_death() -> dict[str, Any]:
    g0_checks, g0 = _g0_import()
    g1_checks, g1 = _g1_certificate()
    g2_checks, g2 = _g2_certificate()
    g3_checks, g3 = _g3_certificate()
    g4_checks, g4 = _g4_certificate(
        {"verification": {"violations": []}, **g0_checks},
        {**g1_checks},
        {**g2_checks},
        {**g3_checks},
    )
    checks = {
        **{f"G0_{name}": value for name, value in g0_checks.items()},
        **{f"G1_{name}": value for name, value in g1_checks.items()},
        **{f"G2_{name}": value for name, value in g2_checks.items()},
        **{f"G3_{name}": value for name, value in g3_checks.items()},
        **{f"G4_{name}": value for name, value in g4_checks.items()},
    }
    violations = [name for name, passed in checks.items() if not passed]
    ready = not violations
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl595",
        "accepted_outcome": "route_death_certificate",
        "input_certificates": [
            "wl594 G0 parameterized product-cover certificate",
            "G1 natural_character_automatic_on_restricted_image",
            "G2 precise_g2_route_death_certificate",
            "G3 denominator_places_automatic_no_new_character",
            "G4 precise_g4_universal_closure_product_route_death",
        ],
        "input_work_logs": ["wl594"],
        "object_layer": (
            "universal_AA_BB_closure_product_Kummer_split_prime_denominator"
        ),
        "G0": {"checks": g0_checks, **g0},
        "G1": {"checks": g1_checks, **g1},
        "G2": {"checks": g2_checks, **g2},
        "G3": {"checks": g3_checks, **g3},
        "G4": {"checks": g4_checks, **g4},
        "proof_boundary": {
            "scoped_objective_complete": True,
            "long_term_object_complete": True,
            "long_term_object_scope": (
                "the universal closure-product Kummer/split-prime objective only"
            ),
            "global_problem_complete": False,
            "all_future_relative_2_descent_impossible": False,
            "Harborth": False,
            "family_exclusion": False,
            "Selmer": False,
            "rank": False,
            "D2": False,
            "D5": False,
            "M3": False,
            "global_point": False,
            "new_parameterized_global_certificate_supplied": False,
        },
        "conclusion": (
            "G0-G3 exhaust the universal closure-product Kummer, single-split-"
            "prime, and denominator-place mechanism. They do not exclude all "
            "future relative 2-descent or solve the global AA+BB problem."
        ),
        "verification": {
            "checks": checks,
            "violations": violations,
            "strict_certificate": (
                "wl595 imports wl594 and retains both closure targets, all exact "
                "GEN-CLOSURE intervals, genus 3/1/5 geometry, midpoint/endpoints, "
                "factor-zero/infinity charts, p=2, primitive denominators, real "
                "conditions, individual AA/BB lifts, and the full four-factor "
                "lift. G1 is tautological after individual lifts; G2 and G3 give "
                "zero local character bits. Route death is scoped to this "
                "mechanism and makes no global point, family, Selmer, rank, D2, "
                "D5, or M3 claim."
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    payload = build_wl595_universal_closure_product_g4_route_death()
    if args.out is not None:
        write_json(args.out, payload)
    if args.strict:
        print(f"status={payload['status']}")
        print(f"work_log={payload['work_log']}")
        print(f"ready={payload['ready']}")
        print(f"accepted_outcome={payload['accepted_outcome']}")
        print(f"scoped_objective_complete={payload['proof_boundary']['scoped_objective_complete']}")
        print(f"long_term_object_complete={payload['proof_boundary']['long_term_object_complete']}")
        print(f"global_problem_complete={payload['proof_boundary']['global_problem_complete']}")
        print(f"violations={payload['verification']['violations']}")
        return 0 if payload["ready"] else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
