#!/usr/bin/env python3
"""Audit three cover families and certify the pure-v_ell route decision."""

from __future__ import annotations

import argparse
import importlib
import sys
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

try:
    wl585_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl585_m2_pure_v_ell_genus_seventeen_cover_and_combined_source_norm_elliptic_quotient"
    )
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    wl585_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl585_m2_pure_v_ell_genus_seventeen_cover_and_combined_source_norm_elliptic_quotient"
    )
    from json_io import load_json, write_json


REPRESENTATIVES = (
    {
        "role": "pure_v_base_family",
        "cover_family": "support=v_5|L=1|T=5|d=(5,1,5)",
        "support_family": "v_5",
        "L": 1,
        "T": 5,
        "d_vector": {
            "d_minus_p": 5,
            "d_neg_2sqrt_q": 5,
            "d_pos_2sqrt_q": 1,
        },
    },
    {
        "role": "pure_u_family",
        "cover_family": "support=u_7|L=7|T=9|d=(7,7,1)",
        "support_family": "u_7",
        "L": 7,
        "T": 9,
        "d_vector": {
            "d_minus_p": 7,
            "d_neg_2sqrt_q": 1,
            "d_pos_2sqrt_q": 7,
        },
    },
    {
        "role": "mixed_three_support_family",
        "cover_family": "support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85)",
        "support_family": "u_3+v_5+w_17",
        "L": 3,
        "T": 10,
        "d_vector": {
            "d_minus_p": 15,
            "d_neg_2sqrt_q": 85,
            "d_pos_2sqrt_q": 51,
        },
    },
)

GENERIC_CERTIFICATE_CANDIDATES = (
    "AA_A7_B2_u_7_m_tail_shell7_candidate",
    "AA_A3_B7_u_3_plus_v_5_plus_w_17_m_tail_shell7_candidate",
)


def _wl522_ready(payload: dict[str, Any]) -> bool:
    summary = payload.get("taxonomy_summary", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl522"
        and summary.get("globally_soluble_but_not_aa_bb_admissible_cover_family_count")
        == 15
        and summary.get("globally_soluble_but_not_aa_bb_admissible_entry_count")
        == 29
    )


def _wl527_ready(payload: dict[str, Any]) -> bool:
    decision = payload.get("proof_data_readiness_decision", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl527"
        and len(payload.get("cover_family_proof_data_inventory", [])) == 15
        and decision.get("ready_for_later_uniform_squareclass_proof_attempt")
        is False
        and decision.get("exact_missing_data_class")
        == "uniform_function_field_model_maps_and_squareclass_certificate"
    )


def _wl505_ready(payload: dict[str, Any]) -> bool:
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl505"
        and payload.get("route_summary", {}).get("wl491_filter_applied_count") == 8
    )


def _wl585_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    cover = payload.get("cover_certificate", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl585"
        and cover.get("cover_degree") == 16
        and cover.get("genus") == 17
        and proof.get("combined_rational_elliptic_quotient_proved_here") is True
        and proof.get("restricted_combined_elliptic_image_solved_here") is False
        and proof.get("uniform_full_wl535_obstruction_proved_here") is False
    )


def _row_map(payload: dict[str, Any], key: str) -> dict[str, dict[str, Any]]:
    return {row.get("cover_family", ""): row for row in payload.get(key, [])}


def _representative_comparison(
    wl522: dict[str, Any], wl527: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[str]]:
    taxonomy = _row_map(wl522, "support_cover_taxonomy")
    inventory = _row_map(wl527, "cover_family_proof_data_inventory")
    rows: list[dict[str, Any]] = []
    violations: list[str] = []

    for expected in REPRESENTATIVES:
        cover_family = expected["cover_family"]
        tax = taxonomy.get(cover_family, {})
        inv = inventory.get(cover_family, {})
        summary = tax.get("cover_summary", {})
        available = inv.get("cover_family_model_availability", {}).get(
            "available_data", {}
        )
        valid = (
            tax.get("support_family") == expected["support_family"]
            and tax.get("classification")
            == "globally_soluble_but_not_aa_bb_admissible"
            and tax.get("failure_mode")
            == "common_source_aa_bb_admissibility_failure"
            and tax.get("entry_count") == 2
            and sorted(inv.get("source_sides_to_map", [])) == ["AA", "BB"]
            and summary.get("L") == expected["L"]
            and summary.get("T") == expected["T"]
            and summary.get("d_vector") == expected["d_vector"]
            and available.get("d_vector") == expected["d_vector"]
        )
        if not valid:
            violations.append(f"representative_mismatch:{cover_family}")
        post_wl527_model = expected["role"] == "pure_v_base_family"
        rows.append(
            {
                **expected,
                "taxonomy_verified": valid,
                "entry_count": tax.get("entry_count"),
                "source_sides": inv.get("source_sides_to_map", []),
                "wl527_model_status": inv.get(
                    "cover_family_model_availability", {}
                ).get("status"),
                "post_wl527_explicit_model_and_maps_available": post_wl527_model,
                "post_wl527_evidence": (
                    "wl528-wl585 pure-v_ell prototype and exact lifts"
                    if post_wl527_model
                    else "none; wl527 has only L,T,d labels"
                ),
                "uniform_squareclass_certificate_available": False,
            }
        )
    return rows, violations


def _quartic_read_only_review() -> dict[str, Any]:
    return {
        "review_only": True,
        "candidate": "parameter-prime quartic character of B/(2*r)",
        "positive_norm_formula": "theta_ell=Legendre(a,ell)",
        "negative_norm_formula": (
            "theta_ell=chi4_ell(-1)*Legendre(b,ell)"
        ),
        "sign_comparison": (
            "Legendre(a,ell)*Legendre(b,ell)=Legendre(2,ell)="
            "chi4_ell(-1)"
        ),
        "determined_values": {
            "ell_1_mod_8": "+1",
            "ell_5_mod_8_r_1_mod_8": "+1",
            "ell_5_mod_8_r_7_mod_8": "-1",
        },
        "dependency_set": ["ell_mod_8", "canonical_r_mod_8"],
        "verdict": "automatic_collapse_to_existing_gaussian_data",
        "independent_invariant": False,
        "wl588_permitted_by_stop_rule": False,
    }


def _fraction(value: Any) -> Fraction:
    return Fraction(str(value))


def _is_rational_square(value: Fraction) -> bool:
    return (
        value >= 0
        and isqrt(value.numerator) ** 2 == value.numerator
        and isqrt(value.denominator) ** 2 == value.denominator
    )


def _generic_squareclass_certificates(
    wl505: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    routed = {
        row.get("candidate_id"): row
        for row in wl505.get("routed_active_shell7_supports", [])
    }
    certificates: list[dict[str, Any]] = []
    violations: list[str] = []
    for candidate_id in GENERIC_CERTIFICATE_CANDIDATES:
        row = routed.get(candidate_id, {})
        cover = row.get("complete_c_d_cover", {})
        witness = row.get("ambient_c_d_global_solubility", {}).get(
            "point_on_cover", {}
        )
        sample = row.get("sample", {})
        params = cover.get("parameters", {})
        roots = cover.get("root_data", {})
        d_vector = cover.get("d_vector", {})
        d0 = int(d_vector.get("d_minus_p", 0))
        dp = int(d_vector.get("d_pos_2sqrt_q", 0))
        dn = int(d_vector.get("d_neg_2sqrt_q", 0))
        u0 = int(witness.get("u_minus_p", 0))
        up = int(witness.get("u_pos_2sqrt_q", 0))
        un = int(witness.get("u_neg_2sqrt_q", 0))
        x_coord = int(witness.get("X", 0))
        y_coord = int(
            row.get("ambient_c_d_global_solubility", {})
            .get("induced_point_on_E_L", {})
            .get("Y", 0)
        )
        d_product = d0 * dp * dn
        d_scale = isqrt(d_product) if d_product >= 0 else 0
        d_product_square = d_scale * d_scale == d_product
        e0 = int(roots.get("e_minus", {}).get("value", 0))
        ep = int(roots.get("e_pos", {}).get("value", 0))
        en = int(roots.get("e_neg", {}).get("value", 0))
        equations_hold = (
            x_coord - e0 == d0 * u0 * u0
            and x_coord - ep == dp * up * up
            and x_coord - en == dn * un * un
        )
        y_map_holds = y_coord == d_scale * u0 * up * un
        geometrically_integral_cover = (
            d0 * dp * dn != 0
            and ep - e0 != 0
            and en - e0 != 0
            and ep != en
        )
        denominator = 2 * (x_coord + int(params.get("p", 0)))
        denominator_nonzero = denominator != 0
        t = Fraction(y_coord, denominator) if denominator_nonzero else Fraction(0)
        a = Fraction(int(sample.get("A", 0)))
        b = Fraction(int(sample.get("B", 0)))
        n = (a + b + t) / 2
        m = a + b - n
        opposite_leg = b
        opposite_product = (n * n + opposite_leg**2) * (
            m * m + opposite_leg**2
        )
        jacobian_minors = (
            4 * d0 * dp * u0 * up,
            -4 * d0 * dn * u0 * un,
            4 * dp * dn * up * un,
        )
        smooth_point = any(value != 0 for value in jacobian_minors)
        certified = (
            sample.get("side") == "AA"
            and d_product_square
            and equations_hold
            and y_map_holds
            and geometrically_integral_cover
            and denominator_nonzero
            and smooth_point
            and opposite_product > 0
            and not _is_rational_square(opposite_product)
        )
        if not certified:
            violations.append(f"generic_squareclass_certificate_failed:{candidate_id}")
        certificates.append(
            {
                "candidate_id": candidate_id,
                "cover_family": next(
                    expected["cover_family"]
                    for expected in REPRESENTATIVES
                    if expected["support_family"]
                    == "+".join(row.get("candidate_support", []))
                    or expected["support_family"]
                    == "_".join(row.get("candidate_support", []))
                ),
                "function": "(N^2+B^2)*(M^2+B^2)",
                "t_value": str(t),
                "N_value": str(n),
                "M_value": str(m),
                "opposite_product_value": str(opposite_product),
                "smooth_nonexceptional_rational_specialization": smooth_point
                and denominator_nonzero,
                "geometrically_integral_biquadratic_cover": (
                    geometrically_integral_cover
                ),
                "value_is_rational_square": _is_rational_square(opposite_product),
                "function_field_squareclass": "nonsquare",
                "certified": certified,
            }
        )
    return certificates, violations


def _tool_feasibility() -> list[dict[str, Any]]:
    return [
        {
            "tool": "parameter_prime_gaussian_characters",
            "families_with_inputs": ["pure_v_base_family"],
            "cross_family_ready": False,
            "independent_on_pure_v": False,
            "verdict": "route_dead",
            "reason": "all tested characters are functions of existing Gaussian data",
        },
        {
            "tool": "restricted_elliptic_image",
            "families_with_inputs": ["pure_v_base_family"],
            "cross_family_ready": False,
            "independent_on_pure_v": False,
            "verdict": "route_dead_as_current_quotient",
            "reason": "the required restricted image restores every original lift",
        },
        {
            "tool": "opposite_side_function_field_divisor_parity",
            "families_with_inputs": [
                "pure_v_base_family",
                "pure_u_family",
                "mixed_three_support_family",
            ],
            "cross_family_ready": True,
            "independent_on_pure_v": True,
            "verdict": "generic_nonsquare_only_not_uniform_point_obstruction",
            "reason": (
                "smooth specializations prove the function is nonsquare in "
                "two more function fields, but nonsquare functions can have "
                "square rational specializations"
            ),
        },
        {
            "tool": "point_level_common_source_nonsquare",
            "families_with_inputs": [
                "pure_v_base_family",
                "pure_u_family",
                "mixed_three_support_family",
            ],
            "cross_family_ready": True,
            "independent_on_pure_v": False,
            "verdict": "finite_signal_only",
            "reason": "pointwise failures do not define a uniform family invariant",
        },
    ]


def build_wl586_cross_family_truth_audit_and_pure_v_ell_route_death(
    *, wl505: dict[str, Any], wl522: dict[str, Any], wl527: dict[str, Any]
) -> dict[str, Any]:
    wl585 = (
        wl585_module.build_wl585_m2_pure_v_ell_genus_seventeen_cover_and_combined_source_norm_elliptic_quotient()
    )
    violations: list[str] = []
    if not _wl505_ready(wl505):
        violations.append("wl505_input_not_ready")
    if not _wl522_ready(wl522):
        violations.append("wl522_input_not_ready")
    if not _wl527_ready(wl527):
        violations.append("wl527_input_not_ready")
    if not _wl585_ready(wl585):
        violations.append("wl585_input_not_ready")
    comparison, comparison_violations = _representative_comparison(wl522, wl527)
    violations.extend(comparison_violations)
    generic_certificates, generic_violations = _generic_squareclass_certificates(
        wl505
    )
    violations.extend(generic_violations)
    review = _quartic_read_only_review()
    if review["verdict"] != "automatic_collapse_to_existing_gaussian_data":
        violations.append("quartic_review_did_not_collapse")
    ready = not violations
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl586",
        "input_work_logs": ["wl505", "wl522", "wl527", "wl585"],
        "object_layer": "cross_family_route_truth_audit",
        "representative_selection_basis": [
            "pure v support with the only post-wl527 explicit prototype",
            "pure u support with both AA and BB point-level failures",
            "mixed u+v+w support with all three d coordinates nontrivial",
        ],
        "representative_cover_family_comparison": comparison,
        "cross_family_generic_squareclass_certificates": generic_certificates,
        "generic_vs_uniform_boundary": {
            "same_function_definition_on_two_cover_families": True,
            "function_field_nonsquare_on_two_cover_families": True,
            "all_rational_specializations_nonsquare_proved": False,
            "uniform_aa_bb_exclusion_invariant_proved": False,
            "reason": (
                "a nonsquare function-field element may specialize to a square; "
                "each square-specialization locus is a new double cover"
            ),
        },
        "quartic_refinement_read_only_review": review,
        "invariant_tool_feasibility": _tool_feasibility(),
        "route_decision": {
            "reenter_wl535_now": False,
            "pure_v_ell_equivalent_model_route": "route_dead",
            "pure_v_ell_parameter_character_route": "route_dead",
            "representative_only_divisor_parity_route": (
                "route_dead_as_uniform_exclusion"
            ),
            "wl588_created": False,
            "cross_family_uniform_invariant_proved_here": False,
            "cross_family_generic_invariant_proved_here": True,
            "selected_next_route": "none_without_parameterized_family_level_input",
            "next_route_success_gate": "not_entered",
            "supporting_models_are_not_progress_by_themselves": True,
        },
        "accepted_outcome": "route_death_certificate",
        "certificate_scope": {
            "kills_all_possible_future_invariants": False,
            "kills_current_pure_v_equivalent_models": True,
            "kills_characters_derived_only_from_existing_gaussian_factors": True,
            "kills_unrestricted_fixed_ell_rank_tables": True,
            "kills_generic_nonsquare_as_uniform_exclusion": True,
            "proves_wl535": False,
            "finds_strict_counterexample": False,
            "proves_complete_selmer_upper_bound": False,
        },
        "shell11_executed_here": False,
        "new_supports_computed_here": False,
        "new_c_d_solubility_tested_here": False,
        "finite_search_used_as_progress": False,
        "equivalent_model_created_here": False,
        "quotient_created_here": False,
        "fixed_ell_rank_table_created_here": False,
        "advance_to_m3": False,
        "violations": violations,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl505", type=Path, required=True)
    parser.add_argument("--wl522", type=Path, required=True)
    parser.add_argument("--wl527", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl586_cross_family_truth_audit_and_pure_v_ell_route_death(
        wl505=load_json(args.wl505),
        wl522=load_json(args.wl522),
        wl527=load_json(args.wl527),
    )
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    print(f"accepted_outcome={payload['accepted_outcome']}")
    print(f"reenter_wl535_now={payload['route_decision']['reenter_wl535_now']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
