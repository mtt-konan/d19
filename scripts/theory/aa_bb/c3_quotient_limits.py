#!/usr/bin/env python3
"""Canonical C3 slice 3 for the wl581-wl585 quotient limits."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

import sympy as sp

C3_QUOTIENT_STAGES = tuple(f"wl{number}" for number in range(581, 586))

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
    "wl581": {"quotient_certificate", "symbolic_certificate"},
    "wl582": {"descent_certificate", "symbolic_certificate"},
    "wl583": {"fiber_product_certificate", "symbolic_certificate"},
    "wl584": {"intersection_certificate", "symbolic_certificate"},
    "wl585": {"cover_certificate", "symbolic_certificate"},
}

C3_QUOTIENT_ALLOWLISTS: dict[str, frozenset[str]] = {
    work_log: frozenset(_COMMON_TOP_LEVEL_KEYS | _STAGE_TOP_LEVEL_KEYS[work_log])
    for work_log in C3_QUOTIENT_STAGES
}

_COMMON_PROOF_KEYS = {
    "uniform_full_wl535_obstruction_proved_here",
    "advance_to_m3",
}

_STAGE_PROOF_KEYS: dict[str, set[str]] = {
    "wl581": {
        "genus_two_character_quotient_proved_here",
        "quadratic_elliptic_quotient_over_q_i_proved_here",
        "restricted_affine_candidate_image_proved_here",
        "restricted_elliptic_image_locus_solved_here",
    },
    "wl582": {
        "nonbranch_forward_and_inverse_bijection_proved_here",
        "q_i_real_coordinate_locus_split_here",
        "quadratic_lift_obstruction_shown_automatic_here",
        "rational_genus_two_lift_reconstructed_here",
        "wl581_unrestricted_elliptic_route_exhausted_here",
    },
    "wl583": {
        "exceptional_tau_half_preserved_and_not_reopened_here",
        "full_cover_fiber_product_equivalence_proved_here",
        "individual_source_squares_retained_on_torsor_here",
        "source_square_torsor_genus_one_proved_here",
        "square_x_pullback_independent_and_connected_here",
        "unramified_degree_two_map_to_product_elliptic_proved_here",
        "square_x_torsor_points_solved_here",
    },
    "wl584": {
        "final_norm_discriminant_equivalence_proved_here",
        "fixed_ell_source_curve_genus_one_proved_here",
        "prime_coupled_torsor_source_identities_proved_here",
        "square_x_source_cover_genus_one_proved_here",
        "unrestricted_source_elliptic_route_exhausted_here",
        "final_norm_intersection_solved_here",
    },
    "wl585": {
        "combined_rational_elliptic_quotient_proved_here",
        "combined_source_norm_genus_three_quotient_proved_here",
        "fixed_ell_full_cover_genus_seventeen_proved_here",
        "norm_bearing_character_quotients_classified_here",
        "selected_tau_interval_equivalent_to_positivity_here",
        "restricted_combined_elliptic_image_solved_here",
    },
}

_STAGE_TRUE_PROOF_KEYS: dict[str, set[str]] = {
    "wl581": {
        "genus_two_character_quotient_proved_here",
        "quadratic_elliptic_quotient_over_q_i_proved_here",
        "restricted_affine_candidate_image_proved_here",
    },
    "wl582": {
        "nonbranch_forward_and_inverse_bijection_proved_here",
        "q_i_real_coordinate_locus_split_here",
        "quadratic_lift_obstruction_shown_automatic_here",
        "rational_genus_two_lift_reconstructed_here",
        "wl581_unrestricted_elliptic_route_exhausted_here",
    },
    "wl583": {
        "exceptional_tau_half_preserved_and_not_reopened_here",
        "full_cover_fiber_product_equivalence_proved_here",
        "individual_source_squares_retained_on_torsor_here",
        "source_square_torsor_genus_one_proved_here",
        "square_x_pullback_independent_and_connected_here",
        "unramified_degree_two_map_to_product_elliptic_proved_here",
    },
    "wl584": {
        "final_norm_discriminant_equivalence_proved_here",
        "fixed_ell_source_curve_genus_one_proved_here",
        "prime_coupled_torsor_source_identities_proved_here",
        "square_x_source_cover_genus_one_proved_here",
        "unrestricted_source_elliptic_route_exhausted_here",
    },
    "wl585": {
        "combined_rational_elliptic_quotient_proved_here",
        "combined_source_norm_genus_three_quotient_proved_here",
        "fixed_ell_full_cover_genus_seventeen_proved_here",
        "norm_bearing_character_quotients_classified_here",
        "selected_tau_interval_equivalent_to_positivity_here",
    },
}

_STAGE_FALSE_PROOF_KEYS: dict[str, set[str]] = {
    "wl581": {"restricted_elliptic_image_locus_solved_here"},
    "wl582": set(),
    "wl583": {"square_x_torsor_points_solved_here"},
    "wl584": {"final_norm_intersection_solved_here"},
    "wl585": {"restricted_combined_elliptic_image_solved_here"},
}

_PREDECESSOR_TRUE_PROOF_KEYS: dict[str, set[str]] = {
    "wl580": {
        "allocation_descent_exhausted_here",
        "canonical_squareclass_self_consistency_stated_here",
        "primitive_m_n_has_no_extra_branch_here",
        "source_squares_reconstructed_from_self_consistent_torsor_here",
        "tau_uniquely_reconstructed_from_X_z_here",
    },
    **_STAGE_TRUE_PROOF_KEYS,
}

_PREDECESSOR_FALSE_PROOF_KEYS: dict[str, set[str]] = {
    "wl580": {"self_consistent_genus_one_family_solved_here"},
    **_STAGE_FALSE_PROOF_KEYS,
}


def _predecessor_ready(payload: Mapping[str, Any], work_log: str) -> bool:
    if not isinstance(payload, Mapping) or work_log not in _PREDECESSOR_TRUE_PROOF_KEYS:
        return False
    proof = payload.get("proof_status")
    expected_proof = (
        _COMMON_PROOF_KEYS
        | _PREDECESSOR_TRUE_PROOF_KEYS[work_log]
        | _PREDECESSOR_FALSE_PROOF_KEYS[work_log]
    )
    return (
        isinstance(proof, Mapping)
        and set(proof) == expected_proof
        and payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("violations") == []
        and payload.get("work_log") == work_log
        and all(proof.get(key) is True for key in _PREDECESSOR_TRUE_PROOF_KEYS[work_log])
        and all(proof.get(key) is False for key in _PREDECESSOR_FALSE_PROOF_KEYS[work_log])
        and proof.get("uniform_full_wl535_obstruction_proved_here") is False
        and proof.get("advance_to_m3") is False
        and payload.get("complete_selmer_upper_bound_proved") is False
        and payload.get("rank_zero_claimed") is False
        and payload.get("sha2_trivial_claimed") is False
        and payload.get("rational_wl535_point_produced_here") is False
        and payload.get("advance_to_m3") is False
        and payload.get("stop_after_current_task") is True
    )


def _wl580_ready(payload: Mapping[str, Any]) -> bool:
    return _predecessor_ready(payload, "wl580")


def _wl581_ready(payload: Mapping[str, Any]) -> bool:
    return _predecessor_ready(payload, "wl581")


def _wl582_ready(payload: Mapping[str, Any]) -> bool:
    return _predecessor_ready(payload, "wl582")


def _wl583_ready(payload: Mapping[str, Any]) -> bool:
    return _predecessor_ready(payload, "wl583")


def _wl584_ready(payload: Mapping[str, Any]) -> bool:
    return _predecessor_ready(payload, "wl584")


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


def _reduce_reciprocal_invariant(expr: sp.Expr, x: sp.Symbol, s: sp.Symbol) -> sp.Expr:
    """Reduce a Laurent expression using 1/x=(x-s)/4 and x^2=s*x+4."""
    expanded = sp.expand(expr)
    polynomial = 0
    for term in sp.Add.make_args(expanded):
        exponent = int(term.as_powers_dict().get(x, 0))
        coefficient = term / x**exponent
        replacement = x**exponent if exponent >= 0 else ((x - s) / 4) ** (-exponent)
        polynomial += coefficient * replacement
    return sp.rem(
        sp.Poly(sp.expand(polynomial), x),
        sp.Poly(x**2 - s * x - 4, x),
    ).as_expr()


def _wl581_symbolic_certificate() -> dict[str, bool]:
    x, tau, s = sp.symbols("X tau S")
    i = sp.I
    delta = tau**2 + 2 * tau - 1
    a = x * (tau + 2) - 2
    b = 2 * tau - x * (2 * tau - 1)
    c = x + 2 * tau + 4
    d = tau * (x + 4) - 2
    transform = -4 / x
    h = x * a * b * c * d
    transformed = {
        "a": sp.simplify(a.subs(x, transform) + 2 * c / x),
        "b": sp.simplify(b.subs(x, transform) - 2 * d / x),
        "c": sp.simplify(c.subs(x, transform) - 2 * a / x),
        "d": sp.simplify(d.subs(x, transform) + 2 * b / x),
    }
    quotient_rhs = -(
        (s - 4 * i)
        * ((tau + 2) * s + 2 * tau**2 + 8 * tau + 6)
        * ((2 * tau**2 - tau) * s + 6 * tau**2 - 8 * tau + 2)
    )
    invariant_y_square = h * (x - 2 * i) ** 2 / x**4
    reduced_y_square = _reduce_reciprocal_invariant(invariant_y_square, x, s)
    cubic_discriminant = sp.factor(sp.discriminant(quotient_rhs, s))
    expected_discriminant = sp.factor(
        256
        * (tau - i) ** 2
        * (tau + i) ** 2
        * ((1 - 2 * i) * tau + i) ** 4
        * (tau + 2 + i) ** 4
        * delta**2
    )
    return {
        "candidate_product_maps_to_genus_two_curve": sp.simplify(
            (2 * x * delta) ** 2 * (a * b / (2 * x * delta)) * (c * d / (2 * delta)) - h
        )
        == 0,
        "four_linear_factors_pair_under_reciprocal_map": all(
            value == 0 for value in transformed.values()
        ),
        "genus_two_polynomial_transform_ratio": sp.simplify(h.subs(x, transform) / h + 64 / x**6)
        == 0,
        "quadratic_lift_is_an_involution": sp.simplify((8 * i / transform**3) * (8 * i / x**3) - 1)
        == 0,
        "base_quotient_coordinate_is_invariant": sp.simplify(
            transform - 4 / transform - (x - 4 / x)
        )
        == 0,
        "elliptic_y_coordinate_is_invariant": sp.simplify(
            (8 * i / x**3) * (transform - 2 * i) / transform**2 - (x - 2 * i) / x**2
        )
        == 0,
        "elliptic_quotient_equation": sp.simplify(reduced_y_square - quotient_rhs) == 0,
        "elliptic_quotient_cubic_discriminant": sp.simplify(
            cubic_discriminant - expected_discriminant
        )
        == 0,
        "rational_quadratic_lift_discriminant": sp.expand((x - 4 / x) ** 2 + 16 - (x + 4 / x) ** 2)
        == 0,
    }


def _wl582_symbolic_certificate() -> dict[str, bool]:
    x, tau, s, a_part, b_part, z = sp.symbols("X tau S A B Z", nonzero=True)
    i = sp.I
    first = x * (tau + 2) - 2
    second = 2 * tau - x * (2 * tau - 1)
    third = x + 2 * tau + 4
    fourth = tau * (x + 4) - 2
    l1 = (tau + 2) * s + 2 * tau**2 + 8 * tau + 6
    l2 = (2 * tau**2 - tau) * s + 6 * tau**2 - 8 * tau + 2
    reconstructed_x = -2 * a_part / b_part
    reconstructed_z = a_part * reconstructed_x
    s_from_parts = 2 * (b_part**2 - a_part**2) / (a_part * b_part)
    quotient_rhs = (-s + 4 * i) * l1 * l2
    invariant_rhs = first * second * third * fourth * (x - 2 * i) ** 2 / x**3
    forward_a = z / x
    forward_b = -2 * z / x**2
    root_l1 = -(2 * tau**2 + 8 * tau + 6) / (tau + 2)
    root_l2 = -(6 * tau**2 - 8 * tau + 2) / (2 * tau**2 - tau)
    root_a = 2 / (tau + 2)
    root_c = -2 * (tau + 2)
    root_b = 2 * tau / (2 * tau - 1)
    root_d = 2 / tau - 4
    return {
        "real_imaginary_elimination_relation": sp.simplify(
            (-s * (a_part * b_part / 2)) - (a_part**2 - b_part**2)
        ).subs(s, s_from_parts)
        == 0,
        "rational_x_reconstructs_s": sp.simplify(
            (reconstructed_x - 4 / reconstructed_x) - s_from_parts
        )
        == 0,
        "quadratic_lift_square_is_automatic": sp.simplify(
            s_from_parts**2 + 16 - (reconstructed_x + 4 / reconstructed_x) ** 2
        )
        == 0,
        "elliptic_y_reconstructs_from_x_z": sp.simplify(
            reconstructed_z * (reconstructed_x - 2 * i) / reconstructed_x**2 - (a_part + i * b_part)
        )
        == 0,
        "quotient_rhs_matches_genus_two_rhs": sp.simplify(
            quotient_rhs.subs(s, x - 4 / x) - invariant_rhs
        )
        == 0,
        "forward_inverse_recovers_x": sp.simplify(-2 * forward_a / forward_b - x) == 0,
        "forward_inverse_recovers_z": sp.simplify(forward_a * x - z) == 0,
        "first_two_torsion_orbit_sum": sp.simplify(root_a + root_c - root_l1) == 0,
        "first_two_torsion_orbit_product": sp.simplify(root_a * root_c + 4) == 0,
        "second_two_torsion_orbit_sum": sp.simplify(root_b + root_d - root_l2) == 0,
        "second_two_torsion_orbit_product": sp.simplify(root_b * root_d + 4) == 0,
    }


def _wl583_symbolic_certificate() -> dict[str, bool]:
    x, tau, q, p, source_s, u, v = sp.symbols("X tau q p s U V", nonzero=True)
    delta = tau**2 + 2 * tau - 1
    first = x * (tau + 2) - 2
    second = 2 * tau - x * (2 * tau - 1)
    third = x + 2 * tau + 4
    fourth = tau * (x + 4) - 2
    u_square = first * second / (2 * delta)
    v_square = third * fourth / (2 * delta)
    product_y = 2 * delta * u * v
    zero_values = [
        first.subs(x, 0),
        second.subs(x, 0),
        third.subs(x, 0),
        fourth.subs(x, 0),
    ]
    leading_values = [
        sp.Poly(first, x).LC(),
        sp.Poly(second, x).LC(),
        sp.Poly(third, x).LC(),
        sp.Poly(fourth, x).LC(),
    ]
    half_substitutions = {
        "u_square": sp.factor(u_square.subs(tau, sp.Rational(1, 2))),
        "v_square": sp.factor(v_square.subs(tau, sp.Rational(1, 2))),
    }
    return {
        "candidate_maps_to_first_torsor_square": sp.simplify(
            sp.expand((q * p) ** 2 - u_square)
            .subs(p**2, first * second / (2 * x * delta))
            .subs(q**2, x)
        )
        == 0,
        "candidate_maps_to_second_torsor_square": sp.simplify(
            sp.expand(source_s**2 - v_square).subs(source_s**2, third * fourth / (2 * delta))
        )
        == 0,
        "torsor_product_maps_to_product_elliptic": sp.simplify(
            sp.expand(product_y**2 - first * second * third * fourth)
            .subs(u**2, u_square)
            .subs(v**2, v_square)
        )
        == 0,
        "converse_first_source_square": sp.simplify(
            sp.expand((u / q) ** 2 - first * second / (2 * x * delta))
            .subs(u**2, u_square)
            .subs(q**2, x)
        )
        == 0,
        "zero_fiber_factor_values": zero_values == [-2, 2 * tau, 2 * tau + 4, 4 * tau - 2],
        "infinity_leading_factor_values": leading_values == [tau + 2, 1 - 2 * tau, 1, tau],
        "exceptional_half_first_torsor_equation": half_substitutions["u_square"] == 5 * x - 4,
        "exceptional_half_second_torsor_equation": half_substitutions["v_square"] == x * (x + 5),
    }


def _wl584_symbolic_certificate() -> dict[str, bool]:
    ell, x, tau = sp.symbols("ell X tau", nonzero=True)
    delta = tau**2 + 2 * tau - 1
    first = x * (tau + 2) - 2
    second = 2 * tau - x * (2 * tau - 1)
    third = x + 2 * tau + 4
    fourth = tau * (x + 4) - 2
    ell_formula = (tau * x**2 + 2 * x * tau**2 + 8 * x * tau - 2 * x - 4 * tau) / (2 * x * delta)
    u_square = first * second / (2 * delta)
    v_square = third * fourth / (2 * delta)
    f = x**2 + (8 - 4 * ell) * x - 4
    e = 4 * (ell - 1) * x
    parameter_relation = sp.expand(e * tau**2 - 2 * f * tau - e)
    g = sp.expand(f**2 + e**2)
    return {
        "first_torsor_square_becomes_source_curve": sp.simplify(u_square - x * (ell_formula - x))
        == 0,
        "second_torsor_square_becomes_source_curve": sp.simplify(v_square - (ell_formula * x + 4))
        == 0,
        "universal_difference_identity": sp.simplify(v_square - u_square - x**2 - 4) == 0,
        "parameter_formula_is_norm_quadratic": sp.simplify(
            parameter_relation.subs(ell, ell_formula)
        )
        == 0,
        "norm_quadratic_discriminant": sp.discriminant(e * tau**2 - 2 * f * tau - e, tau) == 4 * g,
        "positive_norm_root": sp.simplify(
            (e * tau**2 - 2 * f * tau - e).subs(tau, (f + sp.symbols("C")) / e)
            - (sp.symbols("C") ** 2 - g) / e
        )
        == 0,
    }


def _wl585_symbolic_certificate() -> dict[str, bool]:
    ell, x, tau, s = sp.symbols("ell X tau S", nonzero=True)
    f = x**2 + (8 - 4 * ell) * x - 4
    e = 4 * (ell - 1) * x
    positivity = ell * x**2 + 4 * x - 4 * ell
    cone_after_norm_relation = ell * (2 * tau * f / e) + 2 * (ell - 1) * tau
    g = sp.expand(f**2 + e**2)
    source_product = x * (ell - x) * (ell * x + 4)
    combined = sp.expand(source_product * g)
    transform = -4 / x
    quotient_rhs = (ell**2 - ell * s - 4) * (
        s**2 + (16 - 8 * ell) * s + 32 * ell**2 - 96 * ell + 80
    )
    reduced_combined = _reduce_reciprocal_invariant(combined / x**4, x, s)
    g_discriminant = sp.factor(sp.discriminant(g, x))
    expected_g_discriminant = sp.factor(
        2**26 * (ell - 2) ** 2 * (ell - 1) ** 4 * ((ell - 1) ** 2 + 1)
    )
    quotient_discriminant = sp.factor(sp.discriminant(quotient_rhs, s))
    expected_quotient_discriminant = sp.factor(
        -64 * (ell - 1) ** 2 * (5 * ell**2 - 8 * ell + 4) ** 4
    )
    boundary_factor = 5 * ell**2 - 8 * ell + 4
    return {
        "cone_sign_equals_positivity_sign": sp.simplify(
            cone_after_norm_relation - tau * positivity / (2 * (ell - 1) * x)
        )
        == 0,
        "g_quartic_discriminant": sp.simplify(g_discriminant - expected_g_discriminant) == 0,
        "g_nonzero_at_zero": sp.simplify(g.subs(x, 0) - 16) == 0,
        "g_nonzero_at_ell": sp.factor(g.subs(x, ell) - boundary_factor**2) == 0,
        "g_nonzero_at_negative_four_over_ell": sp.factor(
            g.subs(x, -4 / ell) - 16 * boundary_factor**2 / ell**4
        )
        == 0,
        "g_reciprocal_identity": sp.simplify(g.subs(x, transform) - 16 * g / x**4) == 0,
        "source_product_reciprocal_identity": sp.simplify(
            source_product.subs(x, transform) - 16 * source_product / x**4
        )
        == 0,
        "combined_genus_three_reciprocal_identity": sp.simplify(
            combined.subs(x, transform) - 256 * combined / x**8
        )
        == 0,
        "combined_elliptic_quotient_equation": sp.simplify(reduced_combined - quotient_rhs) == 0,
        "combined_elliptic_quotient_discriminant": sp.simplify(
            quotient_discriminant - expected_quotient_discriminant
        )
        == 0,
        "quadratic_lift_discriminant": sp.expand((x - 4 / x) ** 2 + 16 - (x + 4 / x) ** 2) == 0,
    }


def _build_wl581(wl580: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _wl581_symbolic_certificate()
    violations: list[str] = []
    if not _wl580_ready(wl580):
        violations.append("wl580_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "genus_two_character_quotient_proved_here": True,
            "quadratic_elliptic_quotient_over_q_i_proved_here": True,
            "restricted_affine_candidate_image_proved_here": True,
            "restricted_elliptic_image_locus_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl581",
        "object_layer": "m2_genus_two_character_and_q_i_elliptic_quotient",
        "input_checkpoint": {"work_log": "wl580", "ready": _wl580_ready(wl580)},
        "quotient_certificate": {
            "genus_two_curve": "Z^2=X*a*b*c*d",
            "genus_two_branch_count": 6,
            "base_involution": "X->-4/X",
            "quadratic_lift": "(X,Z)->(-4/X,8*i*Z/X^3)",
            "elliptic_coordinates": ["S=X-4/X", "Y=Z*(X-2*i)/X^2"],
            "candidate_image_restrictions": [
                "tau rational in the exact wl570 interval",
                "S rational and S^2+16 a nonzero rational square",
                "positive quadratic lift X is the original rational square",
                "Y nonzero",
                "ell=L(X,tau) is the original odd prime",
            ],
        },
        "symbolic_certificate": symbolic,
        "proof_status": proof_status,
        "violations": violations,
        "rational_wl535_point_produced_here": False,
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "advance_to_m3": False,
        "stop_after_current_task": True,
    }


def _build_wl582(wl581: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _wl582_symbolic_certificate()
    violations: list[str] = []
    if not _wl581_ready(wl581):
        violations.append("wl581_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "q_i_real_coordinate_locus_split_here": True,
            "rational_genus_two_lift_reconstructed_here": True,
            "nonbranch_forward_and_inverse_bijection_proved_here": True,
            "quadratic_lift_obstruction_shown_automatic_here": True,
            "wl581_unrestricted_elliptic_route_exhausted_here": True,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl582",
        "object_layer": "m2_q_i_elliptic_rational_locus_descent_equivalence",
        "input_checkpoint": {"work_log": "wl581", "ready": _wl581_ready(wl581)},
        "descent_certificate": {
            "elliptic_split": ["A^2-B^2=-S*L", "A*B=2*L"],
            "inverse": ["X=-2*A/B", "Z=A*X"],
            "automatic_square": "S^2+16=(X+4/X)^2",
            "remaining_independent_conditions": [
                "X is a positive rational square in the exact interval",
                "the two source products are individually rational squares",
                "ell=L(X,tau) is the required odd prime",
            ],
        },
        "symbolic_certificate": symbolic,
        "proof_status": proof_status,
        "violations": violations,
        "rational_wl535_point_produced_here": False,
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "advance_to_m3": False,
        "stop_after_current_task": True,
    }


def _build_wl583(wl582: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _wl583_symbolic_certificate()
    violations: list[str] = []
    if not _wl582_ready(wl582):
        violations.append("wl582_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "individual_source_squares_retained_on_torsor_here": True,
            "source_square_torsor_genus_one_proved_here": True,
            "unramified_degree_two_map_to_product_elliptic_proved_here": True,
            "full_cover_fiber_product_equivalence_proved_here": True,
            "square_x_pullback_independent_and_connected_here": True,
            "exceptional_tau_half_preserved_and_not_reopened_here": True,
            "square_x_torsor_points_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl583",
        "object_layer": "m2_source_square_genus_one_torsor_and_square_x_fiber_product",
        "input_checkpoint": {"work_log": "wl582", "ready": _wl582_ready(wl582)},
        "fiber_product_certificate": {
            "torsor": ["U^2=a*b/(2*delta)", "V^2=c*d/(2*delta)"],
            "product_elliptic_map": "Y=2*delta*U*V",
            "full_cover": "T_tau fiber product with q^2=X",
            "generic_branch_supports": [
                "{0,infinity}",
                "{root(a),root(b)}",
                "{root(c),root(d)}",
            ],
            "generic_genera": {"torsor": 1, "full_cover": 5},
            "remaining_conditions": [
                "X is a positive rational square in the exact interval",
                "ell=L(X,tau) is the required odd prime",
            ],
        },
        "symbolic_certificate": symbolic,
        "proof_status": proof_status,
        "violations": violations,
        "rational_wl535_point_produced_here": False,
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "advance_to_m3": False,
        "stop_after_current_task": True,
    }


def _build_wl584(wl583: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _wl584_symbolic_certificate()
    violations: list[str] = []
    if not _wl583_ready(wl583):
        violations.append("wl583_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "prime_coupled_torsor_source_identities_proved_here": True,
            "fixed_ell_source_curve_genus_one_proved_here": True,
            "square_x_source_cover_genus_one_proved_here": True,
            "final_norm_discriminant_equivalence_proved_here": True,
            "unrestricted_source_elliptic_route_exhausted_here": True,
            "final_norm_intersection_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl584",
        "object_layer": "m2_prime_coupled_source_elliptic_and_final_norm_intersection",
        "input_checkpoint": {"work_log": "wl583", "ready": _wl583_ready(wl583)},
        "intersection_certificate": {
            "source_curve": ["U^2=X*(ell-X)", "V^2=ell*X+4"],
            "source_curve_genus": 1,
            "source_boundary_points": ["(0,0,2)", "(0,0,-2)"],
            "square_x_source_cover_genus": 1,
            "norm_quadratic": "E*tau^2-2*F*tau-E=0",
            "norm_discriminant": "4*G_ell(X)",
            "live_intersection": [
                "square-X source genus-one point",
                "G_ell(X) square with selected tau root",
                "exact positive interval",
                "ell odd prime congruent 1 mod 4",
            ],
        },
        "symbolic_certificate": symbolic,
        "proof_status": proof_status,
        "violations": violations,
        "rational_wl535_point_produced_here": False,
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "advance_to_m3": False,
        "stop_after_current_task": True,
    }


def _build_wl585(wl584: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _wl585_symbolic_certificate()
    violations: list[str] = []
    if not _wl584_ready(wl584):
        violations.append("wl584_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "selected_tau_interval_equivalent_to_positivity_here": True,
            "fixed_ell_full_cover_genus_seventeen_proved_here": True,
            "norm_bearing_character_quotients_classified_here": True,
            "combined_source_norm_genus_three_quotient_proved_here": True,
            "combined_rational_elliptic_quotient_proved_here": True,
            "restricted_combined_elliptic_image_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl585",
        "object_layer": "m2_genus_seventeen_cover_and_combined_elliptic_quotient",
        "input_checkpoint": {"work_log": "wl584", "ready": _wl584_ready(wl584)},
        "cover_certificate": {
            "squareclasses": ["X", "ell-X", "ell*X+4", "G_ell(X)"],
            "branch_count": 8,
            "cover_degree": 16,
            "genus": 17,
            "norm_bearing_quotient_genera": {
                "genus_1": 1,
                "genus_2": 6,
                "genus_3": 1,
            },
            "combined_quotient": "W^2=X*(ell-X)*(ell*X+4)*G_ell(X)",
            "elliptic_coordinates": ["S=X-4/X", "Z=W/X^2"],
            "candidate_image_restrictions": [
                "S^2+16 is a rational square",
                "positive quadratic lift X is a rational square",
                "sigma_ell<X<ell",
                "individual source and norm squareclasses lift",
            ],
        },
        "symbolic_certificate": symbolic,
        "proof_status": proof_status,
        "violations": violations,
        "rational_wl535_point_produced_here": False,
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "advance_to_m3": False,
        "stop_after_current_task": True,
    }


def build_c3_quotient_limits(wl580: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    """Build wl581-wl585 from one canonical wl580 mapping."""
    wl581 = _build_wl581(wl580)
    wl582 = _build_wl582(wl581)
    wl583 = _build_wl583(wl582)
    wl584 = _build_wl584(wl583)
    wl585 = _build_wl585(wl584)
    return {
        "wl581": wl581,
        "wl582": wl582,
        "wl583": wl583,
        "wl584": wl584,
        "wl585": wl585,
    }


def project_stage(evidence: Mapping[str, Mapping[str, Any]], work_log: str) -> dict[str, Any]:
    """Return one stage after enforcing the explicit C3 quotient map."""
    if work_log not in C3_QUOTIENT_STAGES:
        raise KeyError(f"unknown C3 quotient-limits work log: {work_log}")
    if not isinstance(evidence, Mapping) or work_log not in evidence:
        raise KeyError(f"missing C3 quotient-limits work log: {work_log}")
    payload = evidence[work_log]
    if not isinstance(payload, Mapping):
        raise ValueError(f"invalid stage payload for {work_log}")
    if payload.get("work_log") != work_log:
        raise ValueError(f"stage label mismatch for {work_log}")
    return dict(payload)


def semantic_projection(payload: Mapping[str, Any], work_log: str) -> dict[str, Any]:
    """Project a ready or failed stage onto its exact semantic allowlist."""
    if work_log not in C3_QUOTIENT_STAGES:
        raise KeyError(f"unknown C3 quotient-limits work log: {work_log}")
    if not isinstance(payload, Mapping):
        raise ValueError(f"invalid stage payload for {work_log}")
    if payload.get("work_log") != work_log:
        raise ValueError(f"stage label mismatch for {work_log}")
    allowed = C3_QUOTIENT_ALLOWLISTS[work_log]
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
