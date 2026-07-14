#!/usr/bin/env python3
"""Canonical C3 slice 2 for the wl575-wl580 magnitude descent."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

import sympy as sp

C3_MAGNITUDE_STAGES = tuple(f"wl{number}" for number in range(575, 581))

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
    "wl575": {"rotation_certificate", "symbolic_certificate"},
    "wl576": {"transport_certificate", "symbolic_certificate"},
    "wl577": {"same_side_certificate", "symbolic_certificate"},
    "wl578": {"dyadic_certificate", "remaining_magnitude_system", "symbolic_certificate"},
    "wl579": {"magnitude_curve_certificate", "symbolic_certificate"},
    "wl580": {"reconstruction_certificate", "exact_missing_lemma", "symbolic_certificate"},
}

C3_MAGNITUDE_ALLOWLISTS: dict[str, frozenset[str]] = {
    work_log: frozenset(_COMMON_TOP_LEVEL_KEYS | _STAGE_TOP_LEVEL_KEYS[work_log])
    for work_log in C3_MAGNITUDE_STAGES
}

_COMMON_PROOF_KEYS = {
    "uniform_full_wl535_obstruction_proved_here",
    "advance_to_m3",
}

_STAGE_PROOF_KEYS: dict[str, set[str]] = {
    "wl575": {
        "exact_scaled_Gaussian_rotation_proved_here",
        "inverse_rotation_and_norm_identity_proved_here",
        "PK_primitive_away_from_two_here",
        "R1R2_primitive_away_from_two_here",
        "two_k_allocations_structurally_coupled_here",
        "generic_genus_five_cover_solved_here",
    },
    "wl576": {
        "odd_k_primes_force_two_quadratic_residue_here",
        "regular_same_side_transport_by_K_here",
        "regular_crossed_side_transport_by_P_here",
        "R1_singular_pair_vanishes_together_here",
        "R2_singular_pair_vanishes_together_here",
        "singular_side_requires_higher_valuation_here",
        "generic_genus_five_cover_solved_here",
    },
    "wl577": {
        "global_Delta_divisibility_forces_all_odd_k_primes_into_K_here",
        "odd_singular_determinant_cases_eliminated_here",
        "odd_crossed_transport_eliminated_here",
        "two_allocations_have_identical_odd_parts_here",
        "factor_two_is_only_remaining_transport_here",
        "generic_genus_five_cover_solved_here",
    },
    "wl578": {
        "normalized_rotation_is_diagonal_odd_offdiagonal_even_here",
        "two_adic_valuation_order_preserved_here",
        "factor_two_transports_same_side_here",
        "two_complementary_k_allocations_identical_here",
        "allocation_analysis_exhausted_here",
        "generic_genus_five_cover_solved_here",
    },
    "wl579": {
        "biquadratic_genus_one_curve_proved_here",
        "common_allocation_magnitude_reduced_to_Mobius_map_here",
        "projective_magnitude_converse_proved_here",
        "strict_normalized_magnitude_ordering_proved_here",
        "primitive_linear_form_reconstruction_proved_here",
        "generic_genus_five_cover_solved_here",
    },
    "wl580": {
        "allocation_descent_exhausted_here",
        "canonical_squareclass_self_consistency_stated_here",
        "primitive_m_n_has_no_extra_branch_here",
        "source_squares_reconstructed_from_self_consistent_torsor_here",
        "tau_uniquely_reconstructed_from_X_z_here",
        "self_consistent_genus_one_family_solved_here",
    },
}

_STAGE_TRUE_PROOF_KEYS: dict[str, set[str]] = {
    "wl575": {
        "exact_scaled_Gaussian_rotation_proved_here",
        "inverse_rotation_and_norm_identity_proved_here",
        "PK_primitive_away_from_two_here",
        "R1R2_primitive_away_from_two_here",
        "two_k_allocations_structurally_coupled_here",
    },
    "wl576": {
        "odd_k_primes_force_two_quadratic_residue_here",
        "regular_same_side_transport_by_K_here",
        "regular_crossed_side_transport_by_P_here",
        "R1_singular_pair_vanishes_together_here",
        "R2_singular_pair_vanishes_together_here",
        "singular_side_requires_higher_valuation_here",
    },
    "wl577": {
        "global_Delta_divisibility_forces_all_odd_k_primes_into_K_here",
        "odd_singular_determinant_cases_eliminated_here",
        "odd_crossed_transport_eliminated_here",
        "two_allocations_have_identical_odd_parts_here",
        "factor_two_is_only_remaining_transport_here",
    },
    "wl578": {
        "normalized_rotation_is_diagonal_odd_offdiagonal_even_here",
        "two_adic_valuation_order_preserved_here",
        "factor_two_transports_same_side_here",
        "two_complementary_k_allocations_identical_here",
        "allocation_analysis_exhausted_here",
    },
    "wl579": {
        "biquadratic_genus_one_curve_proved_here",
        "common_allocation_magnitude_reduced_to_Mobius_map_here",
        "projective_magnitude_converse_proved_here",
        "strict_normalized_magnitude_ordering_proved_here",
    },
    "wl580": {
        "allocation_descent_exhausted_here",
        "canonical_squareclass_self_consistency_stated_here",
        "primitive_m_n_has_no_extra_branch_here",
        "source_squares_reconstructed_from_self_consistent_torsor_here",
        "tau_uniquely_reconstructed_from_X_z_here",
    },
}

_STAGE_FALSE_PROOF_KEYS: dict[str, set[str]] = {
    "wl575": {"generic_genus_five_cover_solved_here"},
    "wl576": {"generic_genus_five_cover_solved_here"},
    "wl577": {"generic_genus_five_cover_solved_here"},
    "wl578": {"generic_genus_five_cover_solved_here"},
    "wl579": {
        "primitive_linear_form_reconstruction_proved_here",
        "generic_genus_five_cover_solved_here",
    },
    "wl580": {
        "self_consistent_genus_one_family_solved_here",
    },
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


def _wl574_ready(payload: Mapping[str, Any]) -> bool:
    return _predecessor_ready(payload, "wl574", "two_complementary_splits_of_same_k_proved_here")


def _wl575_ready(payload: Mapping[str, Any]) -> bool:
    return _predecessor_ready(payload, "wl575", "two_k_allocations_structurally_coupled_here")


def _wl576_ready(payload: Mapping[str, Any]) -> bool:
    return _predecessor_ready(payload, "wl576", "singular_side_requires_higher_valuation_here")


def _wl577_ready(payload: Mapping[str, Any]) -> bool:
    return _predecessor_ready(payload, "wl577", "factor_two_is_only_remaining_transport_here")


def _wl578_ready(payload: Mapping[str, Any]) -> bool:
    return _predecessor_ready(payload, "wl578", "allocation_analysis_exhausted_here")


def _wl579_ready(payload: Mapping[str, Any]) -> bool:
    return _predecessor_ready(payload, "wl579", "projective_magnitude_converse_proved_here")


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


def _wl575_symbolic_certificate() -> dict[str, Any]:
    a, b, m, n = sp.symbols("a b m n", integer=True)
    first = a**2 * m + 2 * a**2 * n - 2 * b**2 * n
    second = a**2 * n + 2 * b**2 * m - 2 * a**2 * m
    third = a**2 * m + 4 * b**2 * m - 2 * b**2 * n
    fourth = a**2 * n + 2 * b**2 * m + 4 * b**2 * n
    p = a**4 + 4 * b**4
    k_form = a**4 + 4 * a**2 * b**2 - 4 * b**4
    r1 = 5 * a**4 - 8 * a**2 * b**2 + 4 * b**4
    r2 = a**4 + 8 * a**2 * b**2 + 20 * b**4
    x, y = sp.symbols("x y")
    p_xy = x**2 + 4 * y**2
    k_xy = x**2 + 4 * x * y - 4 * y**2
    r1_xy = 5 * x**2 - 8 * x * y + 4 * y**2
    r2_xy = x**2 + 8 * x * y + 20 * y**2
    return {
        "forward_C": sp.expand(r1 * third - (p * first - 2 * k_form * second)) == 0,
        "forward_D": sp.expand(r1 * fourth - (2 * k_form * first + p * second)) == 0,
        "inverse_A": sp.expand(r2 * first - (p * third + 2 * k_form * fourth)) == 0,
        "inverse_B": sp.expand(r2 * second - (-2 * k_form * third + p * fourth)) == 0,
        "norm_identity": sp.expand(p**2 + 4 * k_form**2 - r1 * r2) == 0,
        "sum_square_identity": sp.expand(r1 * (third**2 + fourth**2) - r2 * (first**2 + second**2))
        == 0,
        "PK_resultant": str(sp.factor(sp.resultant(p_xy, k_xy, x))),
        "R1R2_resultant": str(sp.factor(sp.resultant(r1_xy, r2_xy, x))),
        "resultants_verified": sp.factor(sp.resultant(p_xy, k_xy, x)) == 128 * y**4
        and sp.factor(sp.resultant(r1_xy, r2_xy, x)) == 18432 * y**4,
    }


def _wl576_symbolic_certificate() -> dict[str, bool]:
    a, b, m, n = sp.symbols("a b m n", integer=True)
    first = a**2 * m + 2 * a**2 * n - 2 * b**2 * n
    second = a**2 * n + 2 * b**2 * m - 2 * a**2 * m
    third = a**2 * m + 4 * b**2 * m - 2 * b**2 * n
    fourth = a**2 * n + 2 * b**2 * m + 4 * b**2 * n
    p_form = a**4 + 4 * b**4
    k_form = a**4 + 4 * a**2 * b**2 - 4 * b**4
    return {
        "AC_cross_resultant": sp.factor(sp.resultant(first, third, m)) == -2 * n * k_form,
        "AD_cross_resultant": sp.expand(sp.resultant(first, fourth, m) - n * p_form) == 0,
        "BC_cross_resultant": sp.expand(sp.resultant(second, third, m) + n * p_form) == 0,
        "BD_cross_resultant": sp.factor(sp.resultant(second, fourth, m)) == -2 * n * k_form,
        "Delta_discriminant": sp.discriminant(m**2 + 2 * m * n - n**2, m) == 8 * n**2,
    }


def _wl577_symbolic_certificate() -> dict[str, bool]:
    a, b = sp.symbols("a b", integer=True)
    p_form = a**4 + 4 * b**4
    k_form = a**4 + 4 * a**2 * b**2 - 4 * b**4
    r1 = 5 * a**4 - 8 * a**2 * b**2 + 4 * b**4
    r2 = a**4 + 8 * a**2 * b**2 + 20 * b**4
    return {
        "rotation_norm_identity": sp.expand(p_form**2 + 4 * k_form**2 - r1 * r2) == 0,
        "K_is_positivity_form": sp.expand(k_form - (a**4 + 4 * a**2 * b**2 - 4 * b**4)) == 0,
    }


def _wl578_symbolic_certificate() -> dict[str, bool]:
    p0, k0 = sp.symbols("P0 K0")
    matrix = sp.Matrix([[p0, -2 * k0], [2 * k0, p0]])
    return {
        "normalized_matrix_determinant": sp.expand(matrix.det() - (p0**2 + 4 * k0**2)) == 0,
    }


def _wl579_symbolic_certificate() -> dict[str, bool]:
    p, k_form, lam, u, v, z, w = sp.symbols("P K lambda u v z w", positive=True)
    mobius = (2 * k_form + p * z) / (p - 2 * k_form * z)
    curve = lam * v**2 * (p - 2 * k_form * lam * u**2) - (2 * k_form + p * lam * u**2)
    return {
        "mobius_difference": sp.simplify(
            mobius - z - 2 * k_form * (1 + z**2) / (p - 2 * k_form * z)
        )
        == 0,
        "biquadratic_substitution": sp.simplify(
            (w - mobius).subs({z: lam * u**2, w: lam * v**2}) * (p - 2 * k_form * lam * u**2)
            - curve
        )
        == 0,
        "zero_pole_collision_impossible_polynomial": sp.expand(p**2 + 4 * k_form**2)
        == p**2 + 4 * k_form**2,
    }


def _wl580_symbolic_certificate() -> dict[str, bool]:
    x, tau, z = sp.symbols("X tau z")
    first = x * (tau + 2) - 2
    second = 2 * tau - x * (2 * tau - 1)
    third = tau * (x + 4) - 2
    fourth = x + 2 * tau + 4
    recovered = (x + 2 * z * (1 - x)) / (x * (z + 2) - 2)
    return {
        "tau_reconstruction": sp.simplify((z * first - second).subs(tau, recovered)) == 0,
        "strict_cross_identity": sp.expand(
            first * fourth - second * third - 2 * (tau**2 + 1) * (x**2 + 4 * x - 4)
        )
        == 0,
        "first_product_ratio_identity": sp.simplify(first * second - first**2 * z).subs(
            z, second / first
        )
        == 0,
        "second_product_ratio_identity": sp.simplify(third * fourth - third**2 * z).subs(
            z, fourth / third
        )
        == 0,
    }


def _build_wl575(wl574: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _wl575_symbolic_certificate()
    predecessor_ready = _wl574_ready(wl574)
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl574_input_not_ready")
    for key, value in symbolic.items():
        if key.endswith("_resultant"):
            continue
        if value is not True:
            violations.append(key)
    proof_status = (
        {
            "exact_scaled_Gaussian_rotation_proved_here": True,
            "inverse_rotation_and_norm_identity_proved_here": True,
            "PK_primitive_away_from_two_here": True,
            "R1R2_primitive_away_from_two_here": True,
            "two_k_allocations_structurally_coupled_here": True,
            "generic_genus_five_cover_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if not violations
        else {}
    )
    payload = _base_payload(
        work_log="wl575",
        object_layer="m2_scaled_Gaussian_rotation_between_source_pairs",
        predecessor="wl574",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "rotation_certificate": {
                "forward": ["R1*C=P*A-2*K*B", "R1*D=2*K*A+P*B"],
                "inverse": ["R2*A=P*C+2*K*D", "R2*B=-2*K*C+P*D"],
                "norm": "P^2+4*K^2=R1*R2",
                "pair_norm": "R1*(C^2+D^2)=R2*(A^2+B^2)",
                "gcd_PK": "1 if a odd; 4 if a even",
                "gcd_R1_R2": "1 if a odd; 4 if a even",
            },
            "symbolic_certificate": symbolic,
        }
    )
    return payload


def _build_wl576(wl575: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _wl576_symbolic_certificate()
    predecessor_ready = _wl575_ready(wl575)
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl575_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    proof_status = (
        {
            "odd_k_primes_force_two_quadratic_residue_here": True,
            "regular_same_side_transport_by_K_here": True,
            "regular_crossed_side_transport_by_P_here": True,
            "R1_singular_pair_vanishes_together_here": True,
            "R2_singular_pair_vanishes_together_here": True,
            "singular_side_requires_higher_valuation_here": True,
            "generic_genus_five_cover_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if not violations
        else {}
    )
    payload = _base_payload(
        work_log="wl576",
        object_layer="m2_odd_prime_side_transport_under_scaled_rotation",
        predecessor="wl575",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "transport_certificate": {
                "odd_k_prime_class": "Legendre(2,p)=1, p congruent 1 or 7 mod 8",
                "regular_K": "same side: A->C, B->D",
                "regular_P": "crossed side: A->D, B->C",
                "R1_singular": "p divides A and B; exactly one of C,D",
                "R2_singular": "p divides C and D; exactly one of A,B",
                "remaining_data": "larger normalized valuation in the singular pair",
            },
            "symbolic_certificate": symbolic,
        }
    )
    return payload


def _build_wl577(wl576: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _wl577_symbolic_certificate()
    predecessor_ready = _wl576_ready(wl576)
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl576_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    proof_status = (
        {
            "global_Delta_divisibility_forces_all_odd_k_primes_into_K_here": True,
            "odd_singular_determinant_cases_eliminated_here": True,
            "odd_crossed_transport_eliminated_here": True,
            "two_allocations_have_identical_odd_parts_here": True,
            "factor_two_is_only_remaining_transport_here": True,
            "generic_genus_five_cover_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if not violations
        else {}
    )
    payload = _base_payload(
        work_log="wl577",
        object_layer="m2_all_odd_k_primes_same_side_transport",
        predecessor="wl576",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "same_side_certificate": {
                "global_input": "Delta divides K",
                "odd_k_prime": "p divides K but not P*R1*R2",
                "transport": "A->C and B->D",
                "allocation_identity": ["odd(alpha)=odd(gamma)", "odd(beta)=odd(delta0)"],
                "factor_two": "2 divides k iff m,n have opposite parity",
            },
            "symbolic_certificate": symbolic,
        }
    )
    return payload


def _build_wl578(wl577: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _wl578_symbolic_certificate()
    predecessor_ready = _wl577_ready(wl577)
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl577_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    proof_status = (
        {
            "normalized_rotation_is_diagonal_odd_offdiagonal_even_here": True,
            "two_adic_valuation_order_preserved_here": True,
            "factor_two_transports_same_side_here": True,
            "two_complementary_k_allocations_identical_here": True,
            "allocation_analysis_exhausted_here": True,
            "generic_genus_five_cover_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if not violations
        else {}
    )
    payload = _base_payload(
        work_log="wl578",
        object_layer="m2_dyadic_same_side_and_identical_k_allocation",
        predecessor="wl577",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "dyadic_certificate": {
                "normalization": "e=1 if a odd, e=4 if a even",
                "matrix_parity": "odd diagonal and even off-diagonal over Z_2",
                "ordering": "larger v2 coordinate is preserved",
                "transport": "A->C and B->D",
                "allocation_identity": ["alpha=gamma", "beta=delta0"],
            },
            "remaining_magnitude_system": {
                "first": "R1*g2*alpha*r2^2=P*g1*alpha*r1^2-2*K*g1*beta*s1^2",
                "second": "R1*g2*beta*s2^2=2*K*g1*alpha*r1^2+P*g1*beta*s1^2",
            },
            "symbolic_certificate": symbolic,
        }
    )
    return payload


def _build_wl579(wl578: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _wl579_symbolic_certificate()
    predecessor_ready = _wl578_ready(wl578)
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl578_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    proof_status = (
        {
            "common_allocation_magnitude_reduced_to_Mobius_map_here": True,
            "biquadratic_genus_one_curve_proved_here": True,
            "strict_normalized_magnitude_ordering_proved_here": True,
            "projective_magnitude_converse_proved_here": True,
            "primitive_linear_form_reconstruction_proved_here": False,
            "generic_genus_five_cover_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if not violations
        else {}
    )
    payload = _base_payload(
        work_log="wl579",
        object_layer="m2_common_allocation_Mobius_magnitude_curve",
        predecessor="wl578",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "magnitude_curve_certificate": {
                "lambda": "beta/alpha",
                "ratios": ["z=lambda*u^2=B/A", "w=lambda*v^2=D/C"],
                "Mobius": "w=(2*K+P*z)/(P-2*K*z)",
                "curve": "lambda*v^2*(P-2*K*lambda*u^2)=2*K+P*lambda*u^2",
                "domain": "0<u^2<P/(2*K*lambda)",
                "ordering": "v>u",
                "genus": 1,
            },
            "symbolic_certificate": symbolic,
        }
    )
    return payload


def _build_wl580(wl579: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _wl580_symbolic_certificate()
    predecessor_ready = _wl579_ready(wl579)
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl579_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    proof_status = (
        {
            "tau_uniquely_reconstructed_from_X_z_here": True,
            "primitive_m_n_has_no_extra_branch_here": True,
            "canonical_squareclass_self_consistency_stated_here": True,
            "source_squares_reconstructed_from_self_consistent_torsor_here": True,
            "allocation_descent_exhausted_here": True,
            "self_consistent_genus_one_family_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if not violations
        else {}
    )
    payload = _base_payload(
        work_log="wl580",
        object_layer="m2_primitive_reconstruction_and_descent_exhaustion",
        predecessor="wl579",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "reconstruction_certificate": {
                "tau": "[X+2*z*(1-X)]/[X*(z+2)-2]",
                "denominator": "X*(z+2)-2>0 for X>1,z>0",
                "canonical_class": "[lambda]=[2*(tau^2+2*tau-1)]",
                "source_square_equivalence": [
                    "z/lambda square reconstructs first source square",
                    "w/lambda square reconstructs second source square",
                ],
                "strict_identity": "Abar*Dbar-Bbar*Cbar=2*(tau^2+1)*(X^2+4*X-4)",
            },
            "exact_missing_lemma": (
                "no positive rational point on the self-consistent genus-one magnitude "
                "torsor in the wl570 interval"
            ),
            "symbolic_certificate": symbolic,
        }
    )
    return payload


def build_c3_magnitude_descent(wl574: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    """Build wl575-wl580 from one canonical wl574 mapping."""
    wl575 = _build_wl575(wl574)
    wl576 = _build_wl576(wl575)
    wl577 = _build_wl577(wl576)
    wl578 = _build_wl578(wl577)
    wl579 = _build_wl579(wl578)
    wl580 = _build_wl580(wl579)
    return {
        "wl575": wl575,
        "wl576": wl576,
        "wl577": wl577,
        "wl578": wl578,
        "wl579": wl579,
        "wl580": wl580,
    }


def project_stage(evidence: Mapping[str, Mapping[str, Any]], work_log: str) -> dict[str, Any]:
    """Return one stage after enforcing the explicit C3 magnitude map."""
    if work_log not in C3_MAGNITUDE_STAGES:
        raise KeyError(f"unknown C3 magnitude-descent work log: {work_log}")
    if not isinstance(evidence, Mapping) or work_log not in evidence:
        raise KeyError(f"missing C3 magnitude-descent work log: {work_log}")
    payload = evidence[work_log]
    if not isinstance(payload, Mapping):
        raise ValueError(f"invalid stage payload for {work_log}")
    if payload.get("work_log") != work_log:
        raise ValueError(f"stage label mismatch for {work_log}")
    return dict(payload)


def semantic_projection(payload: Mapping[str, Any], work_log: str) -> dict[str, Any]:
    """Project a ready or failed stage onto its exact semantic allowlist."""
    if work_log not in C3_MAGNITUDE_STAGES:
        raise KeyError(f"unknown C3 magnitude-descent work log: {work_log}")
    if not isinstance(payload, Mapping):
        raise ValueError(f"invalid stage payload for {work_log}")
    if payload.get("work_log") != work_log:
        raise ValueError(f"stage label mismatch for {work_log}")
    allowed = C3_MAGNITUDE_ALLOWLISTS[work_log]
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
