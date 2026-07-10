#!/usr/bin/env python3
"""Build the wl528 single v_5 L=1 T=5 function-field prototype."""

from __future__ import annotations

import argparse
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any

import sympy as sp

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json


TARGET_CANDIDATE_IDS = [
    "AA_A1_B4_v_5_m_tail_refresh_candidate",
    "BB_A4_B1_v_5_m_tail_refresh_candidate",
]

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

BOUNDARY = (
    "This audits only wl528 / the first minimal function-field prototype for "
    "support=v_5|L=1|T=5|d=(5,1,5), represented by the wl495 "
    "AA_A1_B4 and BB_A4_B1 entries. It reconstructs one explicit cover model "
    "from existing complete-d equations, writes rational source-side maps and "
    "N,M as function-field elements, forms the opposite-side product, proves "
    "that product is nonsquare in the prototype function field by a rational "
    "specialization certificate, separates AA and BB symmetry, exceptional "
    "divisors, positivity, and specialization limits, and stops. It does not "
    "execute shell 11, compute new supports, touch another cover family, test "
    "new ambient C_d solubility, run broad rank or Selmer diagnostics, use the "
    "old package-x S~ bridge, prove a uniform cover-family obstruction, prove "
    "a complete Sel_2(E) upper bound, claim dim Sel_2(E)=2, rank zero, "
    "Sha[2]=0, uniform M_tail full rank, or family exclusion."
)


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl495_ready(wl495: dict[str, Any]) -> bool:
    summary = wl495.get("route_summary", {})
    return (
        wl495.get("status") == "ok"
        and wl495.get("ready") is True
        and wl495.get("work_log") == "wl495"
        and wl495.get("complete_c_d_cover_data_instantiated_here") is True
        and wl495.get("old_package_x_coordinate_collapse_used") is False
        and wl495.get("package_x_s_tilde_bridge_used") is False
        and wl495.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl495.get("single_curve_diagnostics_run") is False
        and summary.get("ambient_globally_soluble_count") == 4
        and summary.get("aa_bb_not_admissible_count") == 4
        and not _claims_forbidden_bound(wl495)
    )


def _target_entries(wl495: dict[str, Any]) -> list[dict[str, Any]]:
    by_id = {
        entry.get("candidate_id"): entry
        for entry in wl495.get("routed_refreshed_supports", [])
    }
    return [by_id[candidate_id] for candidate_id in TARGET_CANDIDATE_IDS if candidate_id in by_id]


def _same_target_cover(entries: list[dict[str, Any]]) -> bool:
    if len(entries) != 2:
        return False
    covers = [entry["complete_c_d_cover"] for entry in entries]
    samples = [cover["sample"] for cover in covers]
    return (
        all(entry["routing_state"]["aa_bb_admissibility_status"] == "not_admissible"
            for entry in entries)
        and all(entry["ambient_c_d_global_solubility"]["status"] == "globally_soluble"
                for entry in entries)
        and all(entry["candidate_support"] == ["v_5"] for entry in entries)
        and all(sample["L"] == 1 and sample["T"] == 5 for sample in samples)
        and {sample["side"] for sample in samples} == {"AA", "BB"}
        and {sample["A"] + sample["B"] for sample in samples} == {5}
        and all(cover["d_vector"] == {"d_minus_p": 5, "d_pos_2sqrt_q": 1, "d_neg_2sqrt_q": 5}
                for cover in covers)
        and all(cover["parameters"] == {"p": -42, "q": 841, "sqrt_q": 29}
                for cover in covers)
    )


def _is_rational_square(value: Fraction) -> bool:
    return (
        value >= 0
        and isqrt(value.numerator) ** 2 == value.numerator
        and isqrt(value.denominator) ** 2 == value.denominator
    )


def _sympy_reduces_to_zero(expr: sp.Expr, *, r: sp.Symbol, y: sp.Symbol) -> bool:
    function_field_rhs = 5 * r**4 - 264 * r**2 + 2000
    numerator = sp.together(expr).as_numer_denom()[0]
    remainder = sp.rem(
        sp.Poly(sp.expand(numerator), y),
        sp.Poly(y**2 - function_field_rhs, y),
    ).as_expr()
    return sp.factor(remainder) == 0


def _identity_checks() -> list[dict[str, Any]]:
    r, y = sp.symbols("r y")
    u_minus = (r**2 - 20) / (2 * r)
    u_pos = y / (2 * r)
    u_neg = (r**2 + 20) / (2 * r)
    x_coord = 42 + 5 * u_minus**2
    y_coord = 5 * u_minus * u_pos * u_neg
    t_value = y * (r**2 + 20) / (4 * r * (r**2 - 20))
    z_value = x_coord / 2 - t_value**2
    n_value = (5 + t_value) / 2
    m_value = (5 - t_value) / 2
    source_product = (n_value**2 + 1) * (m_value**2 + 1)

    checks = [
        (
            "X_minus_42_relation",
            "X - 42 = 5*u_minus_p^2",
            x_coord - 42 - 5 * u_minus**2,
        ),
        (
            "X_minus_58_relation",
            "X - 58 = u_pos_2sqrt_q^2",
            x_coord - 58 - u_pos**2,
        ),
        (
            "X_plus_58_relation",
            "X + 58 = 5*u_neg_2sqrt_q^2",
            x_coord + 58 - 5 * u_neg**2,
        ),
        (
            "centered_even_t_formula",
            "t = Y/(2*(X+p)) = y*(r^2+20)/(4*r*(r^2-20))",
            y_coord / (2 * (x_coord - 42)) - t_value,
        ),
        (
            "source_leg_one_product_square",
            "(N^2+1)(M^2+1) = (z/4)^2",
            source_product - (z_value / 4) ** 2,
        ),
    ]
    return [
        {
            "check_id": check_id,
            "identity": identity,
            "verified_in_function_field": _sympy_reduces_to_zero(expr, r=r, y=y),
        }
        for check_id, identity, expr in checks
    ]


def _json_fraction(value: Fraction) -> int | str:
    if value.denominator == 1:
        return value.numerator
    return f"{value.numerator}/{value.denominator}"


def _function_field_model(identity_checks: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "base_field": "Q",
        "function_field": "Q(r,y)/(y^2 - (5*r^4 - 264*r^2 + 2000))",
        "equation": "y^2 = 5*r^4 - 264*r^2 + 2000",
        "cover_parameter": "r = u_neg_2sqrt_q + u_minus_p",
        "cover_maps": {
            "u_minus_p": "(r^2 - 20)/(2*r)",
            "u_pos_2sqrt_q": "y/(2*r)",
            "u_neg_2sqrt_q": "(r^2 + 20)/(2*r)",
            "X": "42 + 5*((r^2 - 20)/(2*r))^2",
            "Y": "5*y*(r^4 - 400)/(8*r^3)",
        },
        "derived_from_complete_d_equations": [
            "X - 42 = 5*u_minus_p^2",
            "X - 58 = u_pos_2sqrt_q^2",
            "X + 58 = 5*u_neg_2sqrt_q^2",
            "5*u_minus_p^2 - u_pos_2sqrt_q^2 = 16",
            "u_minus_p^2 - u_neg_2sqrt_q^2 = -20",
        ],
        "identity_checks": identity_checks,
        "open_conditions_for_this_chart": [
            "r != 0",
            "r^2 != 20",
            "X+p != 0",
        ],
    }


def _source_side_maps() -> dict[str, Any]:
    t_formula = "y*(r^2+20)/(4*r*(r^2-20))"
    n_formula = f"(5 + {t_formula})/2"
    m_formula = f"(5 - {t_formula})/2"
    return {
        "shared_centered_even_map": {
            "t": t_formula,
            "z": "X/2 - t^2",
            "N": n_formula,
            "M": m_formula,
            "source_leg": 1,
            "source_product_square_identity": "(N^2+1)(M^2+1) = (z/4)^2",
        },
        "AA_source": {
            "candidate_id": "AA_A1_B4_v_5_m_tail_refresh_candidate",
            "A": 1,
            "B": 4,
            "L": 1,
            "source_product": "(N^2+A^2)(M^2+A^2)",
            "opposite_side_product": "(N^2+B^2)(M^2+B^2)",
        },
        "BB_source": {
            "candidate_id": "BB_A4_B1_v_5_m_tail_refresh_candidate",
            "A": 4,
            "B": 1,
            "L": 1,
            "source_product": "(N^2+B^2)(M^2+B^2)",
            "opposite_side_product": "(N^2+A^2)(M^2+A^2)",
        },
        "AA_BB_symmetry": (
            "Both selected entries use the same L=1 source product and the same "
            "opposite leg 4 product; only the label of the opposite AA/BB side changes."
        ),
    }


def _check_result(check_id: str, passed: bool, evidence: dict[str, Any]) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "passed": passed,
        "evidence": evidence,
    }


def _computed_specialization() -> dict[str, Fraction]:
    r_value = Fraction(10)
    y_value = Fraction(160)
    u_minus = (r_value**2 - 20) / (2 * r_value)
    u_pos = y_value / (2 * r_value)
    u_neg = (r_value**2 + 20) / (2 * r_value)
    x_coord = 42 + 5 * u_minus**2
    y_coord = 5 * y_value * (r_value**4 - 400) / (8 * r_value**3)
    t_value = y_value * (r_value**2 + 20) / (4 * r_value * (r_value**2 - 20))
    n_value = (5 + t_value) / 2
    m_value = (5 - t_value) / 2
    product = (n_value**2 + 16) * (m_value**2 + 16)
    product_from_t = ((t_value**2 + 89) ** 2 - 100 * t_value**2) / 16
    return {
        "r": r_value,
        "y": y_value,
        "u_minus_p": u_minus,
        "u_pos_2sqrt_q": u_pos,
        "u_neg_2sqrt_q": u_neg,
        "X": x_coord,
        "Y": y_coord,
        "t": t_value,
        "N": n_value,
        "M": m_value,
        "opposite_product": product,
        "opposite_product_from_t": product_from_t,
    }


def _specialization_json(values: dict[str, Fraction]) -> dict[str, int | str]:
    return {
        key: _json_fraction(values[key])
        for key in [
            "r",
            "y",
            "u_minus_p",
            "u_pos_2sqrt_q",
            "u_neg_2sqrt_q",
            "X",
            "Y",
            "t",
            "N",
            "M",
        ]
    }


def _entry_matches_cover_point(entry: dict[str, Any], values: dict[str, Fraction]) -> bool:
    point = entry["ambient_c_d_global_solubility"]["point_on_cover"]
    return point == {
        "X": int(values["X"]),
        "u_minus_p": int(values["u_minus_p"]),
        "u_pos_2sqrt_q": int(values["u_pos_2sqrt_q"]),
        "u_neg_2sqrt_q": int(values["u_neg_2sqrt_q"]),
    }


def _entry_matches_e_point(entry: dict[str, Any], values: dict[str, Fraction]) -> bool:
    point = entry["ambient_c_d_global_solubility"]["induced_point_on_E_L"]
    return point == {
        "X": int(values["X"]),
        "Y": int(values["Y"]),
    }


def _certificate_prerequisite_checks(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    values = _computed_specialization()
    r_value = values["r"]
    y_value = values["y"]
    quartic_rhs = 5 * r_value**4 - 264 * r_value**2 + 2000
    derivative_r = -(20 * r_value**3 - 528 * r_value)
    derivative_y = 2 * y_value
    open_denominators = {
        "r": r_value,
        "r^2 - 20": r_value**2 - 20,
        "X+p": values["X"] - 42,
    }
    product = values["opposite_product"]
    expected_specialized_values = {
        "t": Fraction(6),
        "N": Fraction(11, 2),
        "M": Fraction(-1, 2),
    }
    expected_product = Fraction(12025, 16)

    return [
        _check_result(
            "specialization_lies_on_quartic",
            y_value**2 == quartic_rhs,
            {
                "y^2": _json_fraction(y_value**2),
                "quartic_rhs": _json_fraction(quartic_rhs),
            },
        ),
        _check_result(
            "specialization_is_smooth",
            derivative_r != 0 or derivative_y != 0,
            {
                "dF_dr": _json_fraction(derivative_r),
                "dF_dy": _json_fraction(derivative_y),
            },
        ),
        _check_result(
            "chart_open_denominators_nonzero",
            all(value != 0 for value in open_denominators.values()),
            {
                key: _json_fraction(value)
                for key, value in open_denominators.items()
            },
        ),
        _check_result(
            "maps_to_recorded_cover_point",
            len(entries) == 2
            and all(_entry_matches_cover_point(entry, values) for entry in entries),
            {"computed_cover_point": {
                key: _json_fraction(values[key])
                for key in ["X", "u_minus_p", "u_pos_2sqrt_q", "u_neg_2sqrt_q"]
            }},
        ),
        _check_result(
            "maps_to_recorded_e_point",
            len(entries) == 2 and all(_entry_matches_e_point(entry, values) for entry in entries),
            {"computed_e_point": {
                "X": _json_fraction(values["X"]),
                "Y": _json_fraction(values["Y"]),
            }},
        ),
        _check_result(
            "specialized_t_n_m_match_recorded_values",
            all(values[key] == expected for key, expected in expected_specialized_values.items()),
            {
                key: _json_fraction(values[key])
                for key in ["t", "N", "M"]
            },
        ),
        _check_result(
            "opposite_product_matches_recorded_value",
            product == expected_product and product == values["opposite_product_from_t"],
            {
                "from_N_M": _json_fraction(product),
                "from_t": _json_fraction(values["opposite_product_from_t"]),
            },
        ),
        _check_result(
            "opposite_product_regular_and_nonzero_at_specialization",
            all(value != 0 for value in open_denominators.values()) and product != 0,
            {"opposite_product": _json_fraction(product)},
        ),
        _check_result(
            "specialized_value_is_not_rational_square",
            not _is_rational_square(product),
            {"specialized_value": _json_fraction(product)},
        ),
    ]


def _opposite_product_certificate(entries: list[dict[str, Any]]) -> dict[str, Any]:
    values = _computed_specialization()
    value = values["opposite_product"]
    prerequisite_checks = _certificate_prerequisite_checks(entries)
    prerequisites_passed = all(check["passed"] for check in prerequisite_checks)
    return {
        "opposite_leg": 4,
        "opposite_product_in_t": "((t^2 + 89)^2 - 100*t^2)/16",
        "opposite_product_in_N_M": "(N^2+16)(M^2+16)",
        "function_field_nonsquare_certificate": {
            "status": "proved" if prerequisites_passed else "failed_prerequisite",
            "certificate_type": "rational_specialization_to_nonsquare_value",
            "specialization": _specialization_json(values),
            "certificate_prerequisite_checks": prerequisite_checks,
            "smooth_at_specialization": any(
                check["check_id"] == "specialization_is_smooth" and check["passed"]
                for check in prerequisite_checks
            ),
            "nonexceptional_at_specialization": any(
                check["check_id"] == "chart_open_denominators_nonzero" and check["passed"]
                for check in prerequisite_checks
            ),
            "regular_nonzero_at_specialization": any(
                check["check_id"] == "opposite_product_regular_and_nonzero_at_specialization"
                and check["passed"]
                for check in prerequisite_checks
            ),
            "specialized_value": _json_fraction(value),
            "specialized_value_is_rational_square": _is_rational_square(value),
            "squareclass_reason": "12025/16 = 5^2*13*37 / 2^4 has odd 13 and 37 valuations",
            "logic": (
                "If the opposite product were a square in the function field, "
                "then at this smooth rational point where it is regular and "
                "nonzero, its residue would be a rational square. The recorded "
                "specialization gives 12025/16, not a rational square."
            ),
        },
        "divisor_parity_certificate": {
            "status": "not_proved_here",
            "reason": (
                "The prototype proves nonsquareness by specialization, not by a "
                "full divisor-parity computation of the product divisor."
            ),
        },
    }


def build_wl528_v5_l1_t5_function_field_prototype(
    *, wl495: dict[str, Any]
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl495_ready(wl495):
        violations.append("wl495_input_not_ready_or_not_scoped")

    entries = _target_entries(wl495)
    if len(entries) != 2:
        violations.append("target_candidate_pair_not_found_in_wl495")
    elif not _same_target_cover(entries):
        violations.append("target_candidate_pair_does_not_share_expected_cover")

    identity_checks = _identity_checks()
    identities_passed = all(
        check["verified_in_function_field"] is True for check in identity_checks
    )
    if not identities_passed:
        violations.append("function_field_identity_check_failed")

    opposite_product = _opposite_product_certificate(entries)
    certificate = opposite_product["function_field_nonsquare_certificate"]
    certificate_prerequisites_passed = certificate["status"] == "proved"
    if not certificate_prerequisites_passed:
        violations.append("specialization_certificate_prerequisite_failed")

    status = "ok" if not violations else "issues"
    proof_status = (
        {
            "prototype_model_built_here": True,
            "rational_source_side_maps_derived_here": True,
            "N_M_as_function_field_elements_derived_here": True,
            "opposite_side_product_formed_here": True,
            "function_field_nonsquare_certificate_proved_here": certificate["status"] == "proved",
            "divisor_parity_certificate_proved_here": False,
            "uniform_specialization_survival_proved_here": False,
            "uniform_cover_family_obstruction_proved_here": False,
            "ready_as_reviewable_single_prototype": True,
            "ready_as_uniform_cover_family_theorem": False,
            "exact_remaining_gap": (
                "Need a specialization-survival or divisor-parity argument showing "
                "that the opposite-side squareclass obstruction holds for every "
                "nonexceptional rational point in the required positivity domain; "
                "this prototype only proves the product is nonsquare as a function "
                "field element."
            ),
        }
        if status == "ok"
        else {}
    )

    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl527 selected missing proof-data gap plus wl495 complete-d equations",
        "pattern": "AA+BB",
        "lemma_id": "WL528_v5_l1_t5_function_field_prototype",
        "work_log": "wl528",
        "input_work_logs": ["wl527", "wl495"],
        "object_layer": "single_cover_family_function_field_prototype",
        "prototype_scope": {
            "support": "v_5",
            "L": 1,
            "T": 5,
            "d_vector": {"d_minus_p": 5, "d_pos_2sqrt_q": 1, "d_neg_2sqrt_q": 5},
            "candidate_ids": list(TARGET_CANDIDATE_IDS),
            "touches_only_one_cover_family": True,
        },
        "selected_wl495_entries": entries if status == "ok" else [],
        "function_field_model": _function_field_model(identity_checks) if status == "ok" else {},
        "source_side_maps_and_N_M": _source_side_maps() if status == "ok" else {},
        "opposite_side_product": opposite_product if status == "ok" else {},
        "exceptional_divisors_and_positivity": (
            {
                "poles_or_undefined_loci": [
                    "r = 0 for the chosen cover chart",
                    "r^2 = 20 where X+p = 0 and the centered-even t map is undefined",
                ],
                "zero_loci_not_fully_classified_here": [
                    "zeros of the opposite-side product",
                    "zeros of N, M, and source/opposite product factors",
                ],
                "positivity_status": (
                    "The recorded rational specialization has N=11/2 and M=-1/2, "
                    "so M positivity fails at that point. This is separated from "
                    "the squareclass nonsquare certificate."
                ),
                "specialization_status": (
                    "The nonsquare certificate uses one smooth nonexceptional "
                    "rational specialization. It does not prove all rational "
                    "specializations in the family are nonsquare."
                ),
            }
            if status == "ok"
            else {}
        ),
        "proof_status": proof_status,
        "all_function_field_identity_checks_passed": identities_passed,
        "all_specialization_certificate_prerequisites_passed": certificate_prerequisites_passed,
        "failed_function_field_identity_checks": [
            check
            for check in identity_checks
            if check["verified_in_function_field"] is not True
        ],
        "failed_specialization_certificate_prerequisite_checks": [
            check
            for check in certificate["certificate_prerequisite_checks"]
            if check["passed"] is not True
        ],
        "function_field_models_built_here": status == "ok",
        "function_field_squareclass_certificate_proved_here": status == "ok"
        and certificate["status"] == "proved",
        "uniform_cover_family_lemma_proved_here": False,
        "shell11_executed_here": False,
        "m_tail_diagnostics_extended_here": False,
        "new_supports_computed_here": False,
        "new_c_d_solubility_tested_here": False,
        "wl491_filter_applied_to_new_point_here": False,
        "final_obstruction_candidate_selected_here": False,
        "candidate_selected_here": False,
        "broad_rank_or_selmer_diagnostics_run": False,
        "family_rank_or_selmer_diagnostics_run": False,
        "single_curve_diagnostics_run": False,
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "uniform_m_tail_full_rank_claimed": False,
        "family_exclusion_proved_count": 0,
        "old_package_x_coordinate_collapse_used": False,
        "package_x_s_tilde_bridge_used": False,
        "advance_to_next_cover_family": False,
        "advance_to_next_roadmap_step": False,
        "stop_after_current_task": True,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl495", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl528_v5_l1_t5_function_field_prototype(
        wl495=load_json(args.wl495),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl528 v5 L=1 T=5 prototype to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    proof = audit.get("proof_status", {})
    print(
        "function_field_nonsquare_certificate_proved_here="
        f"{proof.get('function_field_nonsquare_certificate_proved_here')}"
    )
    print(
        "uniform_cover_family_obstruction_proved_here="
        f"{proof.get('uniform_cover_family_obstruction_proved_here')}"
    )
    print(f"shell11_executed_here={audit['shell11_executed_here']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
