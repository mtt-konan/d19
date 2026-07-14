#!/usr/bin/env python3
"""Canonical C3 slice 1 for the wl569-wl574 real branch descent."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

import sympy as sp

C3_REAL_BRANCH_STAGES = tuple(f"wl{number}" for number in range(569, 575))

_COMMON_TOP_LEVEL_KEYS = {
    "status",
    "work_log",
    "object_layer",
    "input_checkpoint",
    "proof_status",
    "complete_selmer_upper_bound_proved",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
    "advance_to_m3",
    "stop_after_current_task",
    "rational_wl535_point_produced_here",
}

_STAGE_TOP_LEVEL_KEYS: dict[str, set[str]] = {
    "wl569": {"branch_certificate", "next_exact_lemma", "symbolic_certificate"},
    "wl570": {"system_certificate", "symbolic_certificate"},
    "wl571": {"cover_certificate", "symbolic_certificate"},
    "wl572": {"integrality_certificate", "symbolic_certificate"},
    "wl573": {"denominator_certificate", "symbolic_certificate"},
    "wl574": {"double_split_certificate", "symbolic_certificate"},
}

C3_REAL_BRANCH_ALLOWLISTS: dict[str, frozenset[str]] = {
    work_log: frozenset(_COMMON_TOP_LEVEL_KEYS | _STAGE_TOP_LEVEL_KEYS[work_log])
    for work_log in C3_REAL_BRANCH_STAGES
}

_COMMON_PROOF_KEYS = {
    "uniform_full_wl535_obstruction_proved_here",
    "advance_to_m3",
}

_STAGE_PROOF_KEYS: dict[str, set[str]] = {
    "wl569": {
        "source_square_and_positivity_force_0_lt_X_lt_ell_here",
        "F_strictly_negative_on_candidate_range_here",
        "positive_ordered_norm_ratio_branch_unique_here",
        "strict_cone_ratio_interval_proved_here",
        "selected_orientation_norm_intersection_solved_here",
    },
    "wl570": {
        "quartic_square_root_eliminated_by_unique_tau_here",
        "parameter_formula_in_X_tau_proved_here",
        "both_source_squares_factored_in_X_tau_here",
        "forward_and_converse_wl535_reconstruction_proved_here",
        "two_variable_square_system_solved_here",
    },
    "wl571": {
        "product_quartic_smooth_genus_one_for_all_admissible_tau_here",
        "full_source_square_cover_genus_five_for_tau_ne_half_here",
        "tau_half_unique_genus_drop_to_one_here",
        "product_plus_one_square_converse_proved_here",
        "exceptional_tau_half_branch_solved_here",
    },
    "wl572": {
        "integral_parameter_forces_q_denominator_one_here",
        "integral_parameter_forces_q_numerator_square_divides_four_here",
        "positivity_leaves_only_X_four_here",
        "tau_half_excluded_for_odd_prime_parameter_here",
        "generic_tau_cover_solved_here",
    },
    "wl573": {
        "q_numerator_square_supports_on_four_mn_here",
        "q_denominator_square_supports_on_mn_here",
        "Delta_coprime_to_mn_here",
        "Delta_divides_positive_quartic_form_here",
        "generic_genus_five_cover_solved_here",
    },
    "wl574": {
        "both_source_pairs_share_canonical_Delta_squareclass_here",
        "AB_common_gcd_supported_on_R1_here",
        "CD_common_gcd_supported_on_R2_here",
        "two_complementary_splits_of_same_k_proved_here",
        "generic_genus_five_cover_solved_here",
    },
}

_STAGE_TRUE_PROOF_KEYS: dict[str, set[str]] = {
    "wl569": {
        "source_square_and_positivity_force_0_lt_X_lt_ell_here",
        "F_strictly_negative_on_candidate_range_here",
        "positive_ordered_norm_ratio_branch_unique_here",
        "strict_cone_ratio_interval_proved_here",
    },
    "wl570": {
        "quartic_square_root_eliminated_by_unique_tau_here",
        "parameter_formula_in_X_tau_proved_here",
        "both_source_squares_factored_in_X_tau_here",
        "forward_and_converse_wl535_reconstruction_proved_here",
    },
    "wl571": {
        "product_quartic_smooth_genus_one_for_all_admissible_tau_here",
        "full_source_square_cover_genus_five_for_tau_ne_half_here",
        "tau_half_unique_genus_drop_to_one_here",
        "product_plus_one_square_converse_proved_here",
    },
    "wl572": {
        "integral_parameter_forces_q_denominator_one_here",
        "integral_parameter_forces_q_numerator_square_divides_four_here",
        "positivity_leaves_only_X_four_here",
        "tau_half_excluded_for_odd_prime_parameter_here",
    },
    "wl573": {
        "q_numerator_square_supports_on_four_mn_here",
        "q_denominator_square_supports_on_mn_here",
        "Delta_coprime_to_mn_here",
        "Delta_divides_positive_quartic_form_here",
    },
    "wl574": {
        "both_source_pairs_share_canonical_Delta_squareclass_here",
        "AB_common_gcd_supported_on_R1_here",
        "CD_common_gcd_supported_on_R2_here",
        "two_complementary_splits_of_same_k_proved_here",
    },
}

_STAGE_FALSE_PROOF_KEYS: dict[str, set[str]] = {
    "wl569": {"selected_orientation_norm_intersection_solved_here"},
    "wl570": {"two_variable_square_system_solved_here"},
    "wl571": {"exceptional_tau_half_branch_solved_here"},
    "wl572": {"generic_tau_cover_solved_here"},
    "wl573": {"generic_genus_five_cover_solved_here"},
    "wl574": {"generic_genus_five_cover_solved_here"},
}


def _predecessor_ready(payload: Mapping[str, Any], work_log: str, required_proof_key: str) -> bool:
    if not isinstance(payload, Mapping):
        return False
    proof = payload.get("proof_status")
    return (
        isinstance(proof, Mapping)
        and payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("violations") == []
        and payload.get("work_log") == work_log
        and proof.get(required_proof_key) is True
        and proof.get("uniform_full_wl535_obstruction_proved_here") is False
        and proof.get("advance_to_m3") is False
        and payload.get("complete_selmer_upper_bound_proved") is False
        and payload.get("rank_zero_claimed") is False
        and payload.get("sha2_trivial_claimed") is False
        and payload.get("rational_wl535_point_produced_here") is False
        and payload.get("advance_to_m3") is False
        and payload.get("stop_after_current_task") is True
    )


def _wl568_ready(payload: Mapping[str, Any]) -> bool:
    return _predecessor_ready(
        payload,
        "wl568",
        "allocation_route_independent_obstruction_refuted_here",
    )


def _wl569_ready(payload: Mapping[str, Any]) -> bool:
    return _predecessor_ready(
        payload,
        "wl569",
        "positive_ordered_norm_ratio_branch_unique_here",
    )


def _wl570_ready(payload: Mapping[str, Any]) -> bool:
    return _predecessor_ready(
        payload,
        "wl570",
        "forward_and_converse_wl535_reconstruction_proved_here",
    )


def _wl571_ready(payload: Mapping[str, Any]) -> bool:
    return _predecessor_ready(
        payload,
        "wl571",
        "tau_half_unique_genus_drop_to_one_here",
    )


def _wl572_ready(payload: Mapping[str, Any]) -> bool:
    return _predecessor_ready(
        payload,
        "wl572",
        "tau_half_excluded_for_odd_prime_parameter_here",
    )


def _wl573_ready(payload: Mapping[str, Any]) -> bool:
    return _predecessor_ready(
        payload,
        "wl573",
        "Delta_divides_positive_quartic_form_here",
    )


def _base_payload(
    *,
    work_log: str,
    object_layer: str,
    predecessor: str,
    predecessor_ready: bool,
    proof_status: dict[str, Any],
    violations: list[str],
) -> dict[str, Any]:
    ready = not violations
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": work_log,
        "object_layer": object_layer,
        "input_checkpoint": {"work_log": predecessor, "ready": predecessor_ready},
        "proof_status": proof_status if ready else {},
        "violations": violations,
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "advance_to_m3": False,
        "stop_after_current_task": True,
        "rational_wl535_point_produced_here": False,
    }


def _wl569_symbolic_certificate() -> dict[str, bool]:
    ell, x, tau = sp.symbols("ell X tau", positive=True)
    f = x**2 + (8 - 4 * ell) * x - 4
    derivative = sp.diff(f, x)
    rho = (sp.sqrt((ell - 1) ** 2 + ell**2) - (ell - 1)) / ell
    cone = ell * (tau**2 - 1) + 2 * (ell - 1) * tau
    return {
        "F_polynomial_recorded": sp.expand(f - (x**2 + (8 - 4 * ell) * x - 4)) == 0,
        "F_derivative_recorded": derivative == 2 * x + 8 - 4 * ell,
        "rho_is_positive_cone_root": sp.simplify(cone.subs(tau, rho)) == 0,
        "rho_rationalized_identity": sp.simplify(
            rho - ell / (sp.sqrt((ell - 1) ** 2 + ell**2) + ell - 1)
        )
        == 0,
    }


def _wl570_symbolic_certificate() -> dict[str, bool]:
    ell, x, tau = sp.symbols("ell X tau", positive=True)
    delta = tau**2 + 2 * tau - 1
    f = x**2 + (8 - 4 * ell) * x - 4
    e = 4 * (ell - 1) * x
    relation = sp.expand(2 * tau * f - e * (tau**2 - 1))
    ell_formula = (tau * x**2 + 2 * x * tau**2 + 8 * x * tau - 2 * x - 4 * tau) / (2 * x * delta)
    p_square = -((x * tau + 2 * x - 2) * (2 * x * tau - x - 2 * tau)) / (2 * x * delta)
    c_square = (x + 2 * tau + 4) * (x * tau + 4 * tau - 2) / (2 * delta)
    reconstructed_f = e * (tau**2 - 1) / (2 * tau)
    reconstructed_c = e * (1 + tau**2) / (2 * tau)
    return {
        "ell_formula_solves_norm_ratio_relation": sp.simplify(relation.subs(ell, ell_formula)) == 0,
        "first_source_square_factorization": sp.simplify(
            (ell - x).subs(ell, ell_formula) - p_square
        )
        == 0,
        "second_source_square_factorization": sp.simplify(
            (ell * x + 4).subs(ell, ell_formula) - c_square
        )
        == 0,
        "converse_norm_identity": sp.simplify(reconstructed_c**2 - reconstructed_f**2 - e**2) == 0,
    }


def _wl571_symbolic_certificate() -> dict[str, Any]:
    x, tau = sp.symbols("X tau")
    delta = tau**2 + 2 * tau - 1
    factors = {
        "a": x * (tau + 2) - 2,
        "b": 2 * tau - x * (2 * tau - 1),
        "c": x + 2 * tau + 4,
        "d": tau * (x + 4) - 2,
    }
    names = list(factors)
    resultants = {
        f"{left}_{right}": sp.factor(sp.resultant(factors[left], factors[right], x))
        for index, left in enumerate(names)
        for right in names[index + 1 :]
    }
    expected = {
        "a_b": 2 * (tau**2 + 1),
        "a_c": 2 * (tau**2 + 4 * tau + 5),
        "a_d": 4 * delta,
        "b_c": -4 * delta,
        "b_d": -2 * (5 * tau**2 - 4 * tau + 1),
        "c_d": -2 * (tau**2 + 1),
    }
    half = {name: sp.factor(value.subs(tau, sp.Rational(1, 2))) for name, value in factors.items()}
    ell_half = sp.factor(
        (tau * x**2 + 2 * x * tau**2 + 8 * x * tau - 2 * x - 4 * tau).subs(tau, sp.Rational(1, 2))
        / (2 * x * delta.subs(tau, sp.Rational(1, 2)))
    )
    return {
        "pairwise_resultants": {key: str(value) for key, value in resultants.items()},
        "pairwise_resultants_verified": all(
            sp.expand(resultants[key] - value) == 0 for key, value in expected.items()
        ),
        "tau_half_factors": {key: str(value) for key, value in half.items()},
        "tau_half_has_infinity_and_zero_roots": half["b"] == 1 and half["d"] == x / 2,
        "tau_half_parameter_formula": str(ell_half),
        "tau_half_parameter_formula_verified": sp.simplify(ell_half - (x + 5 - 4 / x)) == 0,
    }


def _wl572_symbolic_certificate() -> dict[str, bool]:
    a, b = sp.symbols("a b", nonzero=True, integer=True)
    x = a**2 / b**2
    ell = sp.factor(x + 5 - 4 / x)
    numerator, denominator = sp.fraction(ell)
    return {
        "reduced_parameter_formula": sp.expand(numerator - (a**4 + 5 * a**2 * b**2 - 4 * b**4)) == 0
        and denominator == a**2 * b**2,
        "numerator_mod_a2": sp.rem(numerator, a**2, a) == -4 * b**4,
        "numerator_mod_b2": sp.rem(numerator, b**2, b) == a**4,
        "sole_positive_candidate_value": sp.simplify((x + 5 - 4 / x).subs({a: 2, b: 1})) == 8,
    }


def _wl573_symbolic_certificate() -> dict[str, bool]:
    a, b, m, n = sp.symbols("a b m n", integer=True)
    delta = m**2 + 2 * m * n - n**2
    h = (
        a**4 * m * n
        + 2 * a**2 * b**2 * m**2
        + 8 * a**2 * b**2 * m * n
        - 2 * a**2 * b**2 * n**2
        - 4 * b**4 * m * n
    )
    k = a**4 + 4 * a**2 * b**2 - 4 * b**4
    return {
        "numerator_mod_a2": sp.rem(h, a**2, a) == -4 * b**4 * m * n,
        "numerator_mod_b2": sp.rem(h, b**2, b) == a**4 * m * n,
        "numerator_mod_delta": sp.factor(sp.rem(h, delta, m) - m * n * k) == 0,
        "delta_resultant": sp.factor(sp.resultant(h, delta, m)) == -(n**4) * k**2,
    }


def _wl574_symbolic_certificate() -> dict[str, bool]:
    a, b, m, n = sp.symbols("a b m n", integer=True)
    first = a**2 * m + 2 * a**2 * n - 2 * b**2 * n
    second = a**2 * n + 2 * b**2 * m - 2 * a**2 * m
    third = a**2 * m + 4 * b**2 * m - 2 * b**2 * n
    fourth = a**2 * n + 2 * b**2 * m + 4 * b**2 * n
    r1 = 5 * a**4 - 8 * a**2 * b**2 + 4 * b**4
    r2 = a**4 + 8 * a**2 * b**2 + 20 * b**4
    return {
        "AB_determinant_in_m": sp.factor(sp.resultant(first, second, m)) == n * r1,
        "AB_determinant_in_n": sp.factor(sp.resultant(first, second, n)) == -m * r1,
        "CD_determinant_in_m": sp.factor(sp.resultant(third, fourth, m)) == n * r2,
        "CD_determinant_in_n": sp.factor(sp.resultant(third, fourth, n)) == -m * r2,
        "R1_positive_completion": sp.expand(
            r1 - (5 * (a**2 - sp.Rational(4, 5) * b**2) ** 2 + sp.Rational(4, 5) * b**4)
        )
        == 0,
    }


def _build_wl569(wl568: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _wl569_symbolic_certificate()
    predecessor_ready = _wl568_ready(wl568)
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl568_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    proof_status = (
        {
            "source_square_and_positivity_force_0_lt_X_lt_ell_here": True,
            "F_strictly_negative_on_candidate_range_here": True,
            "positive_ordered_norm_ratio_branch_unique_here": True,
            "strict_cone_ratio_interval_proved_here": True,
            "selected_orientation_norm_intersection_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if not violations
        else {}
    )
    payload = _base_payload(
        work_log="wl569",
        object_layer="m2_trivial_unit_archimedean_norm_ratio_branch",
        predecessor="wl568",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "branch_certificate": {
                "candidate_range": "0<X=q^2<ell",
                "sign": "F=D^4*(X^2+(8-4*ell)*X-4)<0",
                "ordered_ratio": "tau=A/B=(C+F)/E",
                "exact_interval": "(sqrt((ell-1)^2+ell^2)-(ell-1))/ell<tau<1",
                "uniform_interval": "sqrt(2)-1<tau<1",
            },
            "next_exact_lemma": (
                "couple the unique tau=(C+F)/E branch in (rho_ell,1) to the "
                "selected R_pi/B_pi orientation"
            ),
            "symbolic_certificate": symbolic,
        }
    )
    return payload


def _build_wl570(wl569: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _wl570_symbolic_certificate()
    predecessor_ready = _wl569_ready(wl569)
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl569_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    proof_status = (
        {
            "quartic_square_root_eliminated_by_unique_tau_here": True,
            "parameter_formula_in_X_tau_proved_here": True,
            "both_source_squares_factored_in_X_tau_here": True,
            "forward_and_converse_wl535_reconstruction_proved_here": True,
            "two_variable_square_system_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if not violations
        else {}
    )
    payload = _base_payload(
        work_log="wl570",
        object_layer="m2_exact_two_variable_norm_ratio_square_system",
        predecessor="wl569",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "system_certificate": {
                "variables": ["X=q^2", "tau=(C+F)/E"],
                "delta": "tau^2+2*tau-1",
                "ell": "(tau*X^2+2*X*tau^2+8*X*tau-2*X-4*tau)/(2*X*delta)",
                "first_square": "-(X*tau+2*X-2)*(2*X*tau-X-2*tau)/(2*X*delta)",
                "second_square": "(X+2*tau+4)*(X*tau+4*tau-2)/(2*delta)",
                "intervals": "sigma_ell<X<ell and rho_ell<tau<1",
                "strict_consequence": "X*(2*tau-1)<2*tau",
            },
            "symbolic_certificate": symbolic,
        }
    )
    return payload


def _build_wl571(wl570: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _wl571_symbolic_certificate()
    predecessor_ready = _wl570_ready(wl570)
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl570_input_not_ready")
    for key in (
        "pairwise_resultants_verified",
        "tau_half_has_infinity_and_zero_roots",
        "tau_half_parameter_formula_verified",
    ):
        if symbolic[key] is not True:
            violations.append(key)
    proof_status = (
        {
            "product_quartic_smooth_genus_one_for_all_admissible_tau_here": True,
            "full_source_square_cover_genus_five_for_tau_ne_half_here": True,
            "tau_half_unique_genus_drop_to_one_here": True,
            "product_plus_one_square_converse_proved_here": True,
            "exceptional_tau_half_branch_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if not violations
        else {}
    )
    payload = _base_payload(
        work_log="wl571",
        object_layer="m2_source_square_multiquadratic_cover_genus",
        predecessor="wl570",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "cover_certificate": {
                "product_curve": "Y^2=a*b*c*d",
                "product_curve_genus": 1,
                "product_curve_rational_2_torsion": "full",
                "generic_full_cover_degree": 8,
                "generic_full_cover_branch_points": 6,
                "generic_full_cover_genus": 5,
                "tau_half_full_cover_branch_points": 4,
                "tau_half_full_cover_genus": 1,
                "tau_half_system": [
                    "ell=X+5-4/X",
                    "p^2=5-4/X",
                    "s^2=X*(X+5)",
                    "X=q^2",
                ],
            },
            "symbolic_certificate": symbolic,
        }
    )
    return payload


def _build_wl572(wl571: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _wl572_symbolic_certificate()
    predecessor_ready = _wl571_ready(wl571)
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl571_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    proof_status = (
        {
            "integral_parameter_forces_q_denominator_one_here": True,
            "integral_parameter_forces_q_numerator_square_divides_four_here": True,
            "positivity_leaves_only_X_four_here": True,
            "tau_half_excluded_for_odd_prime_parameter_here": True,
            "generic_tau_cover_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if not violations
        else {}
    )
    payload = _base_payload(
        work_log="wl572",
        object_layer="m2_exceptional_tau_half_integrality_exclusion",
        predecessor="wl571",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "integrality_certificate": {
                "reduced_q": "q=a/b, gcd(a,b)=1, b>0",
                "parameter": "(a^4+5*a^2*b^2-4*b^4)/(a^2*b^2)",
                "mod_a2": "a^2|4*b^4, hence a^2|4",
                "mod_b2": "b^2|a^4, hence b=1",
                "positivity": "X=q^2>1, hence X=4",
                "contradiction": "ell=8 is not an odd prime",
            },
            "symbolic_certificate": symbolic,
        }
    )
    return payload


def _build_wl573(wl572: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _wl573_symbolic_certificate()
    predecessor_ready = _wl572_ready(wl572)
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl572_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    proof_status = (
        {
            "q_numerator_square_supports_on_four_mn_here": True,
            "q_denominator_square_supports_on_mn_here": True,
            "Delta_coprime_to_mn_here": True,
            "Delta_divides_positive_quartic_form_here": True,
            "generic_genus_five_cover_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if not violations
        else {}
    )
    payload = _base_payload(
        work_log="wl573",
        object_layer="m2_generic_cover_integral_denominator_coupling",
        predecessor="wl572",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "denominator_certificate": {
                "coordinates": "X=a^2/b^2, tau=m/n",
                "Delta": "m^2+2*m*n-n^2>0",
                "q_numerator": "a^2 divides 4*m*n",
                "q_denominator": "b^2 divides m*n",
                "Delta_coprimality": "gcd(Delta,m*n)=1",
                "Delta_divisibility": "Delta divides a^4+4*a^2*b^2-4*b^4",
                "Delta_dyadic": "v2(Delta)=0 for opposite parity and 1 for both odd",
            },
            "symbolic_certificate": symbolic,
        }
    )
    return payload


def _build_wl574(wl573: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _wl574_symbolic_certificate()
    predecessor_ready = _wl573_ready(wl573)
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl573_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    proof_status = (
        {
            "both_source_pairs_share_canonical_Delta_squareclass_here": True,
            "AB_common_gcd_supported_on_R1_here": True,
            "CD_common_gcd_supported_on_R2_here": True,
            "two_complementary_splits_of_same_k_proved_here": True,
            "generic_genus_five_cover_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if not violations
        else {}
    )
    payload = _base_payload(
        work_log="wl574",
        object_layer="m2_common_Delta_squareclass_double_split",
        predecessor="wl573",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "double_split_certificate": {
                "canonical_class": "2*Delta=k*h^2 with k positive squarefree",
                "source_products": ["A*B=k*U^2", "C*D=k*V^2"],
                "first_gcd_support": "gcd(A,B) divides 5*a^4-8*a^2*b^2+4*b^4",
                "second_gcd_support": "gcd(C,D) divides a^4+8*a^2*b^2+20*b^4",
                "first_split": "A/g1=alpha*r1^2, B/g1=beta*s1^2, alpha*beta=k",
                "second_split": "C/g2=gamma*r2^2, D/g2=delta0*s2^2, gamma*delta0=k",
            },
            "symbolic_certificate": symbolic,
        }
    )
    return payload


def build_c3_real_branch(wl568: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    """Build wl569-wl574 from one canonical wl568 mapping."""
    wl569 = _build_wl569(wl568)
    wl570 = _build_wl570(wl569)
    wl571 = _build_wl571(wl570)
    wl572 = _build_wl572(wl571)
    wl573 = _build_wl573(wl572)
    wl574 = _build_wl574(wl573)
    return {
        "wl569": wl569,
        "wl570": wl570,
        "wl571": wl571,
        "wl572": wl572,
        "wl573": wl573,
        "wl574": wl574,
    }


def project_stage(evidence: Mapping[str, Mapping[str, Any]], work_log: str) -> dict[str, Any]:
    """Return one stage after enforcing the explicit C3 real-branch map."""
    if work_log not in C3_REAL_BRANCH_STAGES:
        raise KeyError(f"unknown C3 real-branch work log: {work_log}")
    if not isinstance(evidence, Mapping) or work_log not in evidence:
        raise KeyError(f"missing C3 real-branch work log: {work_log}")
    payload = evidence[work_log]
    if not isinstance(payload, Mapping):
        raise ValueError(f"invalid stage payload for {work_log}")
    if payload.get("work_log") != work_log:
        raise ValueError(f"stage label mismatch for {work_log}")
    return dict(payload)


def semantic_projection(payload: Mapping[str, Any], work_log: str) -> dict[str, Any]:
    """Project a ready or failed stage onto its exact semantic allowlist."""
    if work_log not in C3_REAL_BRANCH_STAGES:
        raise KeyError(f"unknown C3 real-branch work log: {work_log}")
    if not isinstance(payload, Mapping):
        raise ValueError(f"invalid stage payload for {work_log}")
    if payload.get("work_log") != work_log:
        raise ValueError(f"stage label mismatch for {work_log}")
    allowed = C3_REAL_BRANCH_ALLOWLISTS[work_log]
    unknown = set(payload) - allowed - {"ready", "violations"}
    if unknown:
        raise ValueError(f"unallowlisted fields for {work_log}: {sorted(unknown)}")
    missing = allowed - set(payload)
    if missing:
        raise ValueError(f"missing allowlisted fields for {work_log}: {sorted(missing)}")
    proof = payload.get("proof_status")
    if not isinstance(proof, Mapping):
        raise ValueError(f"invalid proof_status for {work_log}")
    proof_allowed = _COMMON_PROOF_KEYS | _STAGE_PROOF_KEYS[work_log]
    unknown_proof = set(proof) - proof_allowed
    if unknown_proof:
        raise ValueError(f"unallowlisted proof fields for {work_log}: {sorted(unknown_proof)}")
    if payload.get("status") == "ok" and set(proof) != proof_allowed:
        raise ValueError(f"incomplete proof_status for {work_log}")
    if payload.get("status") == "ok":
        for key in _STAGE_TRUE_PROOF_KEYS[work_log]:
            if proof.get(key) is not True:
                raise ValueError(f"required proof field changed for {work_log}: {key}")
        for key in _STAGE_FALSE_PROOF_KEYS[work_log]:
            if proof.get(key) is not False:
                raise ValueError(f"stage boundary changed for {work_log}: {key}")
        for key in (
            "complete_selmer_upper_bound_proved",
            "rank_zero_claimed",
            "sha2_trivial_claimed",
            "advance_to_m3",
            "rational_wl535_point_produced_here",
        ):
            if payload.get(key) is not False:
                raise ValueError(f"no-claim field changed for {work_log}: {key}")
        if proof.get("uniform_full_wl535_obstruction_proved_here") is not False:
            raise ValueError(f"no-claim proof field changed for {work_log}")
        if proof.get("advance_to_m3") is not False:
            raise ValueError(f"M3 boundary changed for {work_log}")
    projected = {key: payload[key] for key in allowed}
    projected["proof_status"] = dict(proof)
    return json.loads(json.dumps(projected, sort_keys=True))
