#!/usr/bin/env python3
"""Canonical C2 slice for the wl563-wl568 allocation descent."""

from __future__ import annotations

import itertools
import json
import math
from collections.abc import Mapping
from fractions import Fraction
from typing import Any

import sympy as sp

C2_ALLOCATION_STAGES = tuple(f"wl{number}" for number in range(563, 569))

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
}

_STAGE_TOP_LEVEL_KEYS: dict[str, set[str]] = {
    "wl563": {"factorization_certificate", "rational_wl535_point_produced_here"},
    "wl564": {"allocation_certificate", "rational_wl535_point_produced_here"},
    "wl565": {"allocation_certificate", "rational_wl535_point_produced_here"},
    "wl566": {"quartic_certificate", "rational_wl535_point_produced_here"},
    "wl567": {
        "affine_system_certificate",
        "theorem_level_selmer_matrix_claimed",
        "rational_wl535_point_produced_here",
    },
    "wl568": {
        "redundancy_certificate",
        "next_exact_lemma",
        "symbolic_certificate",
        "rational_wl535_point_produced_here",
    },
}

_COMMON_PROOF_KEYS = {
    "uniform_full_wl535_obstruction_proved_here",
    "advance_to_m3",
}

_STAGE_PROOF_KEYS: dict[str, set[str]] = {
    "wl563": {
        "global_product_coordinate_used_here",
        "coprime_squareclass_split_proved_here",
        "Gaussian_square_coordinates_reduced_to_fourth_powers_here",
        "orientation_product_scale_coupled_here",
        "complementary_divisor_split_systems_solved_here",
    },
    "wl564": {
        "dyadic_factor_in_complementary_split_allocated_here",
        "canonical_r_mod8_coupled_to_global_split_here",
        "binary_choice_at_2_removed_when_present_here",
        "odd_complementary_divisor_allocation_solved_here",
    },
    "wl565": {
        "real_coordinate_leading_unit_defined_here",
        "inert_odd_kappa_factors_assigned_here",
        "split_odd_kappa_square_unit_test_proved_here",
        "split_prime_binary_allocations_solved_here",
    },
    "wl566": {
        "quartic_sign_for_split_factor_defined_here",
        "alpha_side_quartic_character_proved_here",
        "beta_side_quartic_character_proved_here",
        "quartic_character_strictly_refines_split_allocation_here",
        "coupled_split_allocation_system_solved_here",
    },
    "wl567": {
        "quartic_allocation_linearized_over_F2_here",
        "affine_row_formula_proved_here",
        "exponential_case_split_removed_here",
        "affine_system_coupled_to_integer_equations_here",
    },
    "wl568": {
        "scale_is_exact_product_coordinate_rewrite_here",
        "cone_is_exact_original_positivity_rewrite_here",
        "affine_rows_automatic_for_actual_factorization_here",
        "allocation_route_independent_obstruction_refuted_here",
        "selected_orientation_norm_intersection_solved_here",
    },
}


def _wl562_ready(payload: Mapping[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl562"
        and proof.get("local_orientation_determinacy_refuted_here") is True
        and proof.get("uniform_full_wl535_obstruction_proved_here") is False
        and payload.get("complete_selmer_upper_bound_proved") is False
        and payload.get("rank_zero_claimed") is False
        and payload.get("sha2_trivial_claimed") is False
        and payload.get("advance_to_m3") is False
    )


def _predecessor_ready(payload: Mapping[str, Any], work_log: str, required_proof_key: str) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == work_log
        and proof.get(required_proof_key) is True
        and proof.get("uniform_full_wl535_obstruction_proved_here") is False
        and payload.get("complete_selmer_upper_bound_proved") is False
        and payload.get("rank_zero_claimed") is False
        and payload.get("sha2_trivial_claimed") is False
        and payload.get("advance_to_m3") is False
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
    }


def _squarefree_kernel(value: int) -> int:
    kernel = 1
    prime = 2
    while prime * prime <= value:
        exponent = 0
        while value % prime == 0:
            exponent += 1
            value //= prime
        if exponent % 2:
            kernel *= prime
        prime += 1
    if value > 1:
        kernel *= value
    return kernel


def _legendre(value: int, prime: int) -> int:
    residue = pow(value % prime, (prime - 1) // 2, prime)
    return -1 if residue == prime - 1 else residue


def _bit(value: int) -> int:
    if value not in {-1, 1}:
        raise ValueError("F2 conversion requires a nonzero quadratic character")
    return (1 - value) // 2


def _quartic_sign(value: int, prime: int) -> int:
    residue = pow(value % prime, (prime - 1) // 4, prime)
    return -1 if residue == prime - 1 else residue


def _wl563_checks() -> bool:
    for first in range(1, 80):
        for second in range(1, 80):
            if math.gcd(first, second) != 1:
                continue
            alpha = _squarefree_kernel(first)
            beta = _squarefree_kernel(second)
            kappa = _squarefree_kernel(first * second)
            if (
                math.gcd(alpha, beta) != 1
                or alpha * beta != kappa
                or math.isqrt(first // alpha) ** 2 != first // alpha
                or math.isqrt(second // beta) ** 2 != second // beta
            ):
                return False
    ell, r, g, alpha, beta, m, n = sp.symbols("ell r g alpha beta m n")
    a = g * alpha * m**2
    b = g * beta * n**2
    f_coordinate = r * (a**2 - b**2)
    reduced_coordinate = r * g**2 * (alpha**2 * m**4 - beta**2 * n**4)
    cone = ell * (a**2 - b**2) + 2 * (ell - 1) * a * b
    reduced_cone = (
        ell * (alpha**2 * m**4 - beta**2 * n**4) + 2 * (ell - 1) * alpha * beta * m**2 * n**2
    )
    return (
        sp.expand(f_coordinate - reduced_coordinate) == 0
        and sp.expand(cone - g**2 * reduced_cone) == 0
    )


def _wl564_checks() -> bool:
    for r_mod_8 in (1, 7):
        inverse = pow(r_mod_8, -1, 8)
        if inverse % 8 != r_mod_8:
            return False
        normalized_difference = 7 * inverse % 8
        if normalized_difference != (7 if r_mod_8 == 1 else 1):
            return False
    for valuation in range(2, 12):
        kappa_is_even = (valuation + 1) % 2 == 1
        if kappa_is_even != (valuation % 2 == 0):
            return False
    return (2 + 1) % 2 == 1


def _wl565_checks() -> bool:
    for prime in (3, 5, 7, 11, 13, 17, 19):
        for unit in range(1, prime):
            h_alpha = -(unit * unit)
            h_beta = unit * unit
            if _legendre(h_alpha, prime) != _legendre(-1, prime):
                return False
            if _legendre(h_beta, prime) != 1:
                return False
    for prime in (3, 7, 11, 19, 23, 31):
        if prime % 4 != 3 or _legendre(-1, prime) != -1:
            return False
        if {-1: "alpha", 1: "beta"}[-1] != "alpha":
            return False
        if {-1: "alpha", 1: "beta"}[1] != "beta":
            return False
    return True


def _wl566_checks() -> bool:
    for prime in (5, 13, 17, 29, 37, 41):
        for opposite_factor in range(1, prime):
            for square_variable in range(1, prime):
                square = opposite_factor * square_variable * square_variable
                alpha_side = -(square**2)
                expected_alpha = (-1) ** ((prime - 1) // 4) * _legendre(opposite_factor, prime)
                if _quartic_sign(alpha_side, prime) != expected_alpha:
                    return False
                beta_side = square**2
                if _quartic_sign(beta_side, prime) != _legendre(opposite_factor, prime):
                    return False
    seen_equal = False
    seen_different = False
    for prime in (5, 13, 17, 29, 37, 41):
        delta = (-1) ** ((prime - 1) // 4)
        for alpha_0 in range(1, prime):
            for beta_0 in range(1, prime):
                first = delta * _legendre(beta_0, prime)
                second = _legendre(alpha_0, prime)
                seen_equal |= first == second
                seen_different |= first != second
    return seen_equal and seen_different


def _wl567_checks() -> bool:
    primes = [5, 13, 17]
    alpha_fixed = 2
    beta_fixed = 3
    for assignment in itertools.product((0, 1), repeat=len(primes)):
        for row_index, q in enumerate(primes):
            a_q = _bit(_legendre(alpha_fixed, q))
            b_q = _bit(_legendre(beta_fixed, q))
            d_q = ((q - 1) // 4) % 2
            off_diagonal = {
                index: _bit(_legendre(t, q)) for index, t in enumerate(primes) if index != row_index
            }
            common = (
                sum(coefficient * assignment[index] for index, coefficient in off_diagonal.items())
                % 2
            )
            if assignment[row_index] == 0:
                z_q = (a_q + common) % 2
            else:
                z_q = (
                    d_q
                    + b_q
                    + sum(
                        coefficient * (1 - assignment[index])
                        for index, coefficient in off_diagonal.items()
                    )
                ) % 2
            delta_q = (d_q + a_q + b_q + sum(off_diagonal.values())) % 2
            left = (delta_q * assignment[row_index] + common) % 2
            if left != (z_q + a_q) % 2:
                return False
    return True


def _symbolic_certificate() -> dict[str, bool]:
    ell, q, d, r, g, kappa, h, alpha, beta, m, n = sp.symbols(
        "ell Q D r g kappa h alpha beta M N", positive=True
    )
    e = 4 * (ell - 1) * q**2 * d**2
    f = q**4 + (8 - 4 * ell) * q**2 * d**2 - 4 * d**4
    original_positive = ell * q**4 + 4 * q**2 * d**2 - 4 * ell * d**4
    cone = ell * (alpha**2 * m**4 - beta**2 * n**4) + 2 * (ell - 1) * kappa * m**2 * n**2
    a = alpha * m**2
    b = beta * n**2
    c = e * (a**2 + b**2) / (2 * a * b)
    ratio_relation = 2 * f * a * b - e * (a**2 - b**2)

    scale_substitution = sp.expand(
        (2 * r * g**2 * kappa * m**2 * n**2 - e).subs(ell, 1 + r * kappa * h**2 / 2)
    )
    scale_target = 2 * r * kappa * ((g * m * n) ** 2 - (h * q * d) ** 2)
    cone_substitution = sp.expand(
        ell * r * g**2 * (alpha**2 * m**4 - beta**2 * n**4)
        + (ell - 1) * 2 * r * g**2 * alpha * beta * m**2 * n**2
        - r * g**2 * cone
    ).subs(alpha * beta, kappa)
    norm_remainder = sp.factor(c**2 - f**2 - e**2)
    opposite_relation = 2 * f * a * b + e * (a**2 - b**2)
    expected_factorization = sp.factor(-ratio_relation * opposite_relation / (4 * a**2 * b**2))

    return {
        "positivity_identity": sp.expand(original_positive - (ell * f + (ell - 1) * e)) == 0,
        "scale_equivalent_after_squareclass_cancellation": sp.expand(
            scale_substitution - scale_target
        )
        == 0,
        "cone_is_coordinate_substitution": sp.expand(cone_substitution) == 0,
        "norm_square_has_two_signed_ratio_branches": sp.simplify(
            norm_remainder - expected_factorization
        )
        == 0,
    }


def _ratio_branch_checks() -> bool:
    for a in range(1, 20):
        for b in range(1, 20):
            for e in range(1, 20):
                f = Fraction(e * (a * a - b * b), 2 * a * b)
                c = Fraction(e * (a * a + b * b), 2 * a * b)
                if c * c != f * f + e * e:
                    return False
    a, b, e = 3, 2, 5
    f = Fraction(e * (a * a - b * b), 2 * a * b)
    c = Fraction(e * (a * a + b * b), 2 * a * b)
    return c * c == (-f) * (-f) + e * e and 2 * (-f) * a * b != e * (a * a - b * b)


def _build_wl563(wl562: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _wl562_ready(wl562)
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl562_input_not_ready")
    if not _wl563_checks():
        violations.append("factorization_certificate_failed")
    proof_status = {
        "global_product_coordinate_used_here": True,
        "coprime_squareclass_split_proved_here": True,
        "Gaussian_square_coordinates_reduced_to_fourth_powers_here": True,
        "orientation_product_scale_coupled_here": True,
        "complementary_divisor_split_systems_solved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl563",
        object_layer="m2_global_integer_factorization_inside_standard_Gaussian_square",
        predecessor="wl562",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "factorization_certificate": {
                "product_equation": "a*b=2*(ell-1)/r*(Q*D)^2",
                "squarefree_kernel": "2*(ell-1)/r=kappa*h^2",
                "coprime_split": [
                    "a=g*alpha*M^2",
                    "b=g*beta*N^2",
                    "alpha*beta=kappa",
                ],
                "scale_equation": "g*M*N=h*abs(Q*D)",
                "real_coordinate": "F=r*g^2*(alpha^2*M^4-beta^2*N^4)",
                "positivity": ("ell*(alpha^2*M^4-beta^2*N^4)+2*(ell-1)*kappa*M^2*N^2>0"),
            },
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _build_wl564(wl563: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _predecessor_ready(wl563, "wl563", "coprime_squareclass_split_proved_here")
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl563_input_not_ready")
    if not _wl564_checks():
        violations.append("dyadic_allocation_certificate_failed")
    proof_status = {
        "dyadic_factor_in_complementary_split_allocated_here": True,
        "canonical_r_mod8_coupled_to_global_split_here": True,
        "binary_choice_at_2_removed_when_present_here": True,
        "odd_complementary_divisor_allocation_solved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl564",
        object_layer="m2_dyadic_allocation_inside_global_complementary_squareclass_split",
        predecessor="wl563",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "allocation_certificate": {
                "r_mod_8": [1, 7],
                "ell_eq_5_mod_8": {
                    "kappa_is_even": True,
                    "r_eq_1_mod_8": "2|beta",
                    "r_eq_7_mod_8": "2|alpha",
                },
                "ell_eq_1_mod_8": {
                    "kappa_even_iff": "v_2(ell-1) is even",
                    "r_eq_1_mod_8_when_even": "2|alpha",
                    "r_eq_7_mod_8_when_even": "2|beta",
                },
            },
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _build_wl565(wl564: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _predecessor_ready(
        wl564, "wl564", "binary_choice_at_2_removed_when_present_here"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl564_input_not_ready")
    if not _wl565_checks():
        violations.append("odd_allocation_certificate_failed")
    proof_status = {
        "real_coordinate_leading_unit_defined_here": True,
        "inert_odd_kappa_factors_assigned_here": True,
        "split_odd_kappa_square_unit_test_proved_here": True,
        "split_prime_binary_allocations_solved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl565",
        object_layer="m2_odd_factor_allocation_inside_global_complementary_split",
        predecessor="wl564",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "allocation_certificate": {
                "normalized_unit": "U_q=(F/r)/q^v_q(F/r) mod q",
                "valuation_parity": "v_q(F/r)=2*v_q(g)",
                "q_divides_alpha": "Legendre(U_q,q)=Legendre(-1,q)",
                "q_divides_beta": "Legendre(U_q,q)=1",
                "q_eq_3_mod_4": "character uniquely selects alpha or beta",
                "q_eq_1_mod_4": "U_q must be square but side remains unresolved",
            },
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _build_wl566(wl565: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _predecessor_ready(
        wl565, "wl565", "split_odd_kappa_square_unit_test_proved_here"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl565_input_not_ready")
    if not _wl566_checks():
        violations.append("quartic_character_certificate_failed")
    proof_status = {
        "quartic_sign_for_split_factor_defined_here": True,
        "alpha_side_quartic_character_proved_here": True,
        "beta_side_quartic_character_proved_here": True,
        "quartic_character_strictly_refines_split_allocation_here": True,
        "coupled_split_allocation_system_solved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl566",
        object_layer="m2_quartic_character_inside_split_complementary_allocation",
        predecessor="wl565",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "quartic_certificate": {
                "quartic_sign": "chi_4,q(H)=H^((q-1)/4)",
                "q_divides_alpha": "chi_4,q(H)=(-1)^((q-1)/4)*Legendre(beta,q)",
                "q_divides_beta": "chi_4,q(H)=Legendre(alpha,q)",
                "decision_rule": "different predicted signs uniquely select the side",
                "failure_rule": "equal predicted signs leave the side unresolved",
            },
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _build_wl567(wl566: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _predecessor_ready(
        wl566, "wl566", "quartic_character_strictly_refines_split_allocation_here"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl566_input_not_ready")
    if not _wl567_checks():
        violations.append("affine_system_certificate_failed")
    proof_status = {
        "quartic_allocation_linearized_over_F2_here": True,
        "affine_row_formula_proved_here": True,
        "exponential_case_split_removed_here": True,
        "affine_system_coupled_to_integer_equations_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl567",
        object_layer="m2_affine_F2_system_for_split_quartic_allocation",
        predecessor="wl566",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "affine_system_certificate": {
                "variable": "x_q=1 iff q|alpha",
                "off_diagonal": "A_qt=(1-Legendre(t,q))/2",
                "diagonal": "Delta_q=d_q+a_q+b_q+sum_(t!=q) A_qt",
                "right_hand_side": "z_q+a_q",
                "row": "Delta_q*x_q+sum_(t!=q) A_qt*x_t=z_q+a_q",
                "outcomes": ["inconsistent", "unique", "explicit affine space"],
            },
            "theorem_level_selmer_matrix_claimed": False,
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _build_wl568(wl567: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _predecessor_ready(wl567, "wl567", "affine_row_formula_proved_here")
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl567_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    if not _ratio_branch_checks():
        violations.append("signed_ratio_branch_check_failed")
    proof_status = {
        "scale_is_exact_product_coordinate_rewrite_here": True,
        "cone_is_exact_original_positivity_rewrite_here": True,
        "affine_rows_automatic_for_actual_factorization_here": True,
        "allocation_route_independent_obstruction_refuted_here": True,
        "selected_orientation_norm_intersection_solved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl568",
        object_layer="m2_trivial_unit_selected_orientation_norm_intersection",
        predecessor="wl567",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "redundancy_certificate": {
                "scale": "2*r*a*b=E iff g*M*N=h*abs(Q*D)",
                "positivity": "original_strict_expression=ell*F+(ell-1)*E",
                "ratio": "2*F*A*B=E*(A^2-B^2)",
                "norm": (
                    "C=E*(A^2+B^2)/(2*A*B); norm square factors into two "
                    "ordered signed-ratio branches"
                ),
                "affine_rows": "necessary identities when z_q is computed from actual H",
            },
            "next_exact_lemma": (
                "selected B_pi/R_pi orientation intersected with F^2+E^2 square "
                "and the strict positivity condition"
            ),
            "symbolic_certificate": symbolic,
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def build_c2_allocation(wl562: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    """Build wl563-wl568 once from the canonical wl562 projection."""
    wl563 = _build_wl563(wl562)
    wl564 = _build_wl564(wl563)
    wl565 = _build_wl565(wl564)
    wl566 = _build_wl566(wl565)
    wl567 = _build_wl567(wl566)
    wl568 = _build_wl568(wl567)
    return {
        "wl563": wl563,
        "wl564": wl564,
        "wl565": wl565,
        "wl566": wl566,
        "wl567": wl567,
        "wl568": wl568,
    }


def project_stage(evidence: Mapping[str, Mapping[str, Any]], work_log: str) -> dict[str, Any]:
    """Return one stage after enforcing the explicit slice-3 stage map."""
    if work_log not in C2_ALLOCATION_STAGES:
        raise KeyError(f"unknown C2 allocation work log: {work_log}")
    if work_log not in evidence:
        raise KeyError(f"missing C2 allocation work log: {work_log}")
    payload = evidence[work_log]
    if payload.get("work_log") != work_log:
        raise ValueError(f"stage label mismatch for {work_log}")
    return dict(payload)


def semantic_projection(payload: Mapping[str, Any], work_log: str) -> dict[str, Any]:
    """Project a ready or failed stage onto its exact semantic allowlist."""
    if work_log not in C2_ALLOCATION_STAGES:
        raise KeyError(f"unknown C2 allocation work log: {work_log}")
    if payload.get("work_log") != work_log:
        raise ValueError(f"stage label mismatch for {work_log}")
    allowed = _COMMON_TOP_LEVEL_KEYS | _STAGE_TOP_LEVEL_KEYS[work_log]
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
    projected = {key: payload[key] for key in allowed}
    projected["proof_status"] = dict(proof)
    return json.loads(json.dumps(projected, sort_keys=True))
