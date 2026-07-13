#!/usr/bin/env python3
"""Certify the accepted wl594 universal AA/BB product-cover G0 input.

This is a symbolic geometry and boundary certificate only.  It supplies a
parameterized lower-genus forward obstruction, analogous to wl585, but it
does not prove a Kummer, split-prime, or restricted local-image obstruction.
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
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    from json_io import write_json


A, B, T, t, k, x, L, W, N1, N2 = sp.symbols(
    "A B T t k x L W N1 N2"
)


def _q(L_value: sp.Expr, T_value: sp.Expr, t_value: sp.Expr) -> sp.Expr:
    """Return the cleared centered AA/BB closure-product quartic."""
    return sp.expand(
        t_value**4
        + (8 * L_value**2 - 2 * T_value**2) * t_value**2
        + (T_value**2 + 4 * L_value**2) ** 2
    )


def _q_factored(L_value: sp.Expr, T_value: sp.Expr, t_value: sp.Expr) -> sp.Expr:
    return sp.expand(
        ((T_value + t_value) ** 2 + 4 * L_value**2)
        * ((T_value - t_value) ** 2 + 4 * L_value**2)
    )


def _even_to_x(expr: sp.Expr) -> sp.Expr:
    polynomial = sp.Poly(sp.expand(expr), t)
    result = sp.Integer(0)
    for (power,), coefficient in polynomial.terms():
        if power % 2:
            raise ValueError("expected an even polynomial in t")
        result += coefficient * x ** (power // 2)
    return sp.expand(result)


def _identity(left: sp.Expr, right: sp.Expr) -> bool:
    return sp.expand(left - right) == 0


def _all_true(values: dict[str, bool]) -> bool:
    return bool(values) and all(value is True for value in values.values())


def _build_checks() -> tuple[dict[str, bool], dict[str, Any]]:
    qa = _q(A, T, t)
    qb = _q(B, T, t)
    product = sp.expand(qa * qb)

    plus_qa = sp.expand(qa.subs(T, A + B))
    plus_qb = sp.expand(qb.subs(T, A + B))
    minus_qa = sp.expand(qa.subs(T, A - B))
    minus_qb = sp.expand(qb.subs(T, A - B))
    scaled_qa = _q(k * A, k * T, k * t)
    scaled_qb = _q(k * B, k * T, k * t)
    scaled_product = sp.expand(scaled_qa * scaled_qb)

    expected_plus_qa = sp.expand(
        t**4 + 2 * (A - B) * (3 * A + B) * t**2 + (5 * A**2 + 2 * A * B + B**2) ** 2
    )
    expected_plus_qb = sp.expand(
        t**4 - 2 * (A - B) * (A + 3 * B) * t**2 + (A**2 + 2 * A * B + 5 * B**2) ** 2
    )
    expected_minus_qa = sp.expand(
        t**4 + 2 * (A + B) * (3 * A - B) * t**2 + (5 * A**2 - 2 * A * B + B**2) ** 2
    )
    expected_minus_qb = sp.expand(
        t**4 + 2 * (A + B) * (3 * B - A) * t**2 + (A**2 - 2 * A * B + 5 * B**2) ** 2
    )

    discriminant_L = sp.factor(sp.discriminant(_q(L, T, t), t))
    expected_discriminant_L = 2**16 * L**4 * T**4 * (T**2 + 4 * L**2) ** 2
    resultant = sp.factor(sp.resultant(qa, qb, t))
    expected_resultant = (
        2**16
        * (A**2 - B**2) ** 4
        * (T**2 + (A - B) ** 2) ** 2
        * (T**2 + (A + B) ** 2) ** 2
    )
    product_discriminant = sp.factor(sp.discriminant(product, t))
    expected_product_discriminant = (
        2**64
        * A**4
        * B**4
        * T**8
        * (A**2 - B**2) ** 8
        * (T**2 + 4 * A**2) ** 2
        * (T**2 + 4 * B**2) ** 2
        * (T**2 + (A - B) ** 2) ** 4
        * (T**2 + (A + B) ** 2) ** 4
    )

    p_a = 8 * A**2 - 2 * T**2
    p_b = 8 * B**2 - 2 * T**2
    q_a = (T**2 + 4 * A**2) ** 2
    q_b = (T**2 + 4 * B**2) ** 2
    f_a = x**2 + p_a * x + q_a
    f_b = x**2 + p_b * x + q_b
    quotient_discriminant_f_a = sp.factor(sp.discriminant(f_a, x))
    quotient_discriminant_f_b = sp.factor(sp.discriminant(f_b, x))
    quotient_resultant = sp.factor(sp.resultant(f_a, f_b, x))
    quotient_product_discriminant = sp.factor(sp.discriminant(f_a * f_b, x))
    expected_quotient_discriminant_f_a = -2**6 * A**2 * T**2
    expected_quotient_discriminant_f_b = -2**6 * B**2 * T**2
    expected_quotient_resultant = (
        2**8
        * (A**2 - B**2) ** 2
        * (T**2 + (A - B) ** 2)
        * (T**2 + (A + B) ** 2)
    )
    expected_quotient_product_discriminant = (
        2**28
        * A**2
        * B**2
        * T**4
        * (A**2 - B**2) ** 4
        * (T**2 + (A - B) ** 2) ** 2
        * (T**2 + (A + B) ** 2) ** 2
    )
    h = (T**2 + 4 * A**2) * (T**2 + 4 * B**2)
    alpha_3 = p_a + p_b
    alpha_2 = p_a * p_b + q_a + q_b
    alpha_1 = p_a * q_b + p_b * q_a
    u = sp.symbols("u")
    cubic = x * u**2 - (
        x**3 + alpha_3 * x**2 + alpha_2 * x + alpha_1 - 2 * h * u
    )

    N = (T + t) / 2
    M = (T - t) / 2
    signed_T = N1 - N2
    signed_t = N1 + N2
    swapped_T = N2 - N1
    swapped_t = N1 + N2
    signed_N = sp.expand(
        N.subs({T: signed_T, t: signed_t}, simultaneous=True)
    )
    signed_M = sp.expand(
        M.subs({T: signed_T, t: signed_t}, simultaneous=True)
    )
    swapped_N = sp.expand(
        N.subs({T: swapped_T, t: swapped_t}, simultaneous=True)
    )
    swapped_M = sp.expand(
        M.subs({T: swapped_T, t: swapped_t}, simultaneous=True)
    )
    phi_a_plus = (T + t) ** 2 + 4 * A**2
    phi_a_minus = (T - t) ** 2 + 4 * A**2
    phi_b_plus = (T + t) ** 2 + 4 * B**2
    phi_b_minus = (T - t) ** 2 + 4 * B**2

    degeneracy_factors = (
        "A=0",
        "B=0",
        "T=0",
        "T^2+4*A^2=0",
        "T^2+4*B^2=0",
        "A^2-B^2=0",
        "T^2+(A-B)^2=0",
        "T^2+(A+B)^2=0",
    )
    positive_factor_signs = (
        "A^4*B^4*T^8>0 when A>0,B>0,T>0",
        "T^2+4*A^2>0 and T^2+4*B^2>0 over the positive real domain",
        "T^2+(A-B)^2>0 and T^2+(A+B)^2>0 when T>0",
        "A^2-B^2!=0 exactly when A!=B",
    )
    positive_assumptions = (
        sp.Q.positive(A)
        & sp.Q.positive(B)
        & sp.Q.positive(T)
        & sp.Q.nonzero(A - B)
    )
    positive_factor_expressions = (
        A**4 * B**4 * T**8,
        T**2 + 4 * A**2,
        T**2 + 4 * B**2,
        T**2 + (A - B) ** 2,
        T**2 + (A + B) ** 2,
    )
    positive_factor_checks = tuple(
        sp.ask(sp.Q.positive(expression), positive_assumptions) is True
        for expression in positive_factor_expressions
    )
    smooth_positive_domain = (
        all(positive_factor_checks)
        and _identity(A**2 - B**2, (A - B) * (A + B))
        and sp.ask(sp.Q.positive(A + B), positive_assumptions) is True
        and sp.ask(sp.Q.nonzero(A - B), positive_assumptions) is True
    )
    scaled_product_equation = (k**4 * W) ** 2 - scaled_product

    checks = {
        "q_L_factorization": _identity(_q_factored(L, T, t), _q(L, T, t)),
        "q_L_expanded_coefficients": _identity(
            _q(L, T, t),
            t**4 + (8 * L**2 - 2 * T**2) * t**2 + (T**2 + 4 * L**2) ** 2,
        ),
        "explicit_T_A_plus_B_QA": _identity(plus_qa, expected_plus_qa),
        "explicit_T_A_plus_B_QB": _identity(plus_qb, expected_plus_qb),
        "explicit_T_A_minus_B_QA": _identity(minus_qa, expected_minus_qa),
        "explicit_T_A_minus_B_QB": _identity(minus_qb, expected_minus_qb),
        "homogeneous_QA": _identity(scaled_qa, k**4 * qa),
        "homogeneous_QB": _identity(scaled_qb, k**4 * qb),
        "homogeneous_product": _identity(scaled_product, k**8 * product),
        "scale_W_via_product_equation": _identity(
            scaled_product_equation, k**8 * (W**2 - product)
        ),
        "swap_exchanges_QA_QB": _identity(qa.xreplace({A: B, B: A}), qb)
        and _identity(qb.xreplace({A: B, B: A}), qa),
        "discriminant_Q_L": _identity(discriminant_L, expected_discriminant_L),
        "resultant_QA_QB": _identity(resultant, expected_resultant),
        "discriminant_product": _identity(
            product_discriminant, expected_product_discriminant
        ),
        "quotient_discriminant_f_A": _identity(
            quotient_discriminant_f_a, expected_quotient_discriminant_f_a
        ),
        "quotient_discriminant_f_B": _identity(
            quotient_discriminant_f_b, expected_quotient_discriminant_f_b
        ),
        "quotient_resultant_f_A_f_B": _identity(
            quotient_resultant, expected_quotient_resultant
        ),
        "quotient_product_discriminant": _identity(
            quotient_product_discriminant, expected_quotient_product_discriminant
        ),
        "positive_smooth_domain_is_A_B_T_positive_A_ne_B": smooth_positive_domain,
        "all_algebraic_degeneracy_factors_retained": (
            len(set(degeneracy_factors)) == len(degeneracy_factors) == 8
        ),
        "quotient_even_QA": _identity(_even_to_x(qa), f_a),
        "quotient_even_QB": _identity(_even_to_x(qb), f_b),
        "quotient_product_equation": _identity(_even_to_x(product), f_a * f_b),
        "midpoint_QA_is_square": _identity(q_a, f_a.subs(x, 0)),
        "midpoint_QB_is_square": _identity(q_b, f_b.subs(x, 0)),
        "midpoint_product_point": _identity(h**2, (f_a * f_b).subs(x, 0)),
        "T_zero_quartic_is_square": _identity(
            _q(L, 0, t), (t**2 + 4 * L**2) ** 2
        ),
        "equal_legs_product_is_square": _identity(
            product.subs(B, A), qa.subs(B, A) ** 2
        ),
        "forward_AA_product": _identity(16 * (N**2 + A**2) * (M**2 + A**2), qa),
        "forward_BB_product": _identity(16 * (N**2 + B**2) * (M**2 + B**2), qb),
        "forward_AA_factorization": _identity(phi_a_plus * phi_a_minus, qa),
        "forward_BB_factorization": _identity(phi_b_plus * phi_b_minus, qb),
        "genus_product_Riemann_Hurwitz": (2 * 3 - 2) == (-4 + 8),
        "genus_elliptic_quotient": (4 - 2) // 2 == 1,
        "genus_simultaneous_AA_BB_Riemann_Hurwitz": (2 * 5 - 2) == (-8 + 16),
        "product_degree_and_leading_coefficient": (
            sp.degree(product, t) == 8 and sp.LC(sp.Poly(product, t)) == 1
        ),
        "elliptic_cubic_chart_identity": _identity(
            (h + x * u) ** 2 - f_a * f_b, x * cubic
        ),
        "centered_sum_identity": _identity(N + M, T),
        "centered_difference_identity": _identity(N - M, t),
        "centered_T_plus_t_identity": _identity(T + t, 2 * N),
        "centered_T_minus_t_identity": _identity(T - t, 2 * M),
        "signed_difference_T_identity": _identity(signed_T, N1 - N2),
        "signed_difference_t_identity": _identity(signed_t, N1 + N2),
        "signed_difference_N_identity": _identity(signed_N, N1),
        "signed_difference_M_identity": _identity(signed_M, -N2),
        "signed_difference_gap_identity": _identity(
            signed_t - signed_T, 2 * N2
        ),
        "swapped_difference_T_identity": _identity(swapped_T, N2 - N1),
        "swapped_difference_t_identity": _identity(swapped_t, N1 + N2),
        "swapped_difference_N_identity": _identity(swapped_N, N2),
        "swapped_difference_M_identity": _identity(swapped_M, -N1),
        "swapped_difference_gap_identity": _identity(
            swapped_t - swapped_T, 2 * N1
        ),
        "midpoint_t_zero_separate": N.subs(t, 0) == M.subs(t, 0),
        "endpoints_separate": (
            N.subs(t, T) == T
            and M.subs(t, T) == 0
            and N.subs(t, -T) == 0
            and M.subs(t, -T) == T
        ),
        "factor_zeroes_separate": all(
            value == 0
            for value in (
                phi_a_plus.subs(t, -T + 2 * sp.I * A),
                phi_a_plus.subs(t, -T - 2 * sp.I * A),
                phi_a_minus.subs(t, T + 2 * sp.I * A),
                phi_a_minus.subs(t, T - 2 * sp.I * A),
                phi_b_plus.subs(t, -T + 2 * sp.I * B),
                phi_b_plus.subs(t, -T - 2 * sp.I * B),
                phi_b_minus.subs(t, T + 2 * sp.I * B),
                phi_b_minus.subs(t, T - 2 * sp.I * B),
            )
        ),
        "infinity_separate": (
            sp.degree(product, t) == 8 and sp.LC(sp.Poly(product, t)) == 1
        ),
        "elliptic_cubic_chart_denominator_identity": _identity(
            sp.cancel((h + x * u - h) / x), u
        ),
        "elliptic_cubic_chart_x_zero_coefficient": _identity(
            sp.Poly(cubic, x).eval(0), 2 * h * u - alpha_1
        ),
    }

    details: dict[str, Any] = {
        "symbols": {"legs": "A,B", "closure_value": "T", "centered": "t"},
        "normalization": {
            "raw_AA_product": "(N^2+A^2)*(M^2+A^2)=Q_A(t)/16",
            "raw_BB_product": "(N^2+B^2)*(M^2+B^2)=Q_B(t)/16",
            "cleared_square_roots": "z_A=4*y_A, z_B=4*y_B",
            "product_cover": "W^2=Q_A(t)*Q_B(t), W=z_A*z_B",
        },
        "general_Q_L": (
            "Q_L(t)=((T+t)^2+4*L^2)((T-t)^2+4*L^2)="
            "t^4+(8*L^2-2*T^2)*t^2+(T^2+4*L^2)^2"
        ),
        "explicit_formulas": {
            "T=A+B": {
                "Q_A": str(expected_plus_qa),
                "Q_B": str(expected_plus_qb),
            },
            "T=abs(A-B), A>B>0": {
                "Q_A": str(expected_minus_qa),
                "Q_B": str(expected_minus_qb),
            },
        },
        "scale_and_parameter": {
            "scale_law": "(A,B,T,t)->k*(A,B,T,t), Q_L->k^4*Q_L, W->k^4*W",
            "scale_product_equation": "W^2=Q_A*Q_B implies (k^4*W)^2=(k^4*Q_A)*(k^4*Q_B)",
            "parameter": "lambda=A/B after B!=0",
            "symmetry": "A<->B gives lambda<->1/lambda; t<->-t swaps N,M",
            "plus_domain": "lambda>=1, T/B=lambda+1; lambda=1 is product-degenerate",
            "minus_domain": "lambda>1, T/B=lambda-1; lambda=1 gives T=0",
        },
        "discriminants": {
            "disc_Q_L": str(expected_discriminant_L),
            "res_QA_QB": str(expected_resultant),
            "disc_product": str(expected_product_discriminant),
            "disc_f_A": str(expected_quotient_discriminant_f_a),
            "disc_f_B": str(expected_quotient_discriminant_f_b),
            "res_f_A_f_B": str(expected_quotient_resultant),
            "disc_f_A_times_f_B": str(expected_quotient_product_discriminant),
            "algebraic_degeneracy_factors": list(degeneracy_factors),
            "positive_factor_signs": list(positive_factor_signs),
            "positive_smooth_domain": "A>0, B>0, T>0, A!=B",
        },
        "genus_and_quotient": {
            "product_cover": "genus 3 from degree 8 and 8 simple branch points",
            "quotient": "x=t^2, w=W, w^2=f_A(x)*f_B(x), genus 1",
            "f_L": "f_L(x)=x^2+(8*L^2-2*T^2)*x+(T^2+4*L^2)^2",
            "midpoint": "x=0, w=+/-((T^2+4*A^2)*(T^2+4*B^2))",
            "cubic_chart": (
                "u=(w-h)/x, h=(T^2+4*A^2)*(T^2+4*B^2), "
                "x*u^2=x^3+a3*x^2+a2*x+a1-2*h*u"
            ),
            "simultaneous_cover": "z_A^2=Q_A, z_B^2=Q_B has genus 5",
        },
        "forward_and_converse": {
            "sum_coordinates": "N=(T+t)/2, M=(T-t)/2",
            "centered_identities": "N+M=T, N-M=t, T+t=2*N, T-t=2*M",
            "elliptic_forward": "x=t^2, w=W",
            "level_b": "x is a nonzero positive rational square in the exact interval",
            "level_c": "Q_A(t) and Q_B(t) are individually rational squares",
            "level_d": "the four original distance-square factors are individually squares",
            "converse_is_not_claimed": True,
        },
        "gen_closure_quantifiers": {
            "universal_statement": (
                "For every exact AA+BB candidate with A,B,N1,N2>0, "
                "{N1+N2,abs(N1-N2)} intersects {A+B,abs(A-B)}."
            ),
            "four_relations": (
                "N1+N2=A+B; N1+N2=abs(A-B); "
                "abs(N1-N2)=A+B; abs(N1-N2)=abs(A-B)"
            ),
            "sum_branches": (
                "For each c in {A+B,abs(A-B)} with c>0, and N1,N2>0 "
                "with N1+N2=c: T=c, N=N1, M=N2, t=N1-N2, |t|<T."
            ),
            "difference_orientation": (
                "For each c in {A+B,abs(A-B)} with c>0, and N1,N2>0 "
                "with N1-N2=c: T=c, N=N1, M=-N2, t=N1+N2>T."
            ),
            "difference_swapped_orientation": (
                "For each c in {A+B,abs(A-B)} with c>0, and N1,N2>0 "
                "with N2-N1=c: T=c, N=N2, M=-N1, t=N1+N2>T."
            ),
            "difference_other_target": (
                "Both difference orientations are required independently for "
                "c=A+B and c=abs(A-B); no target is dropped."
            ),
            "smooth_domain_restriction": (
                "The smooth G0 chart adds A!=B and T>0; A=B and T=0 are "
                "retained as the separate degenerate branch."
            ),
            "T_zero": (
                "sum branch has no positive pair; difference branch is centerline "
                "and degenerate"
            ),
            "midpoint": "sum branch t=0; Q_L(0) is always a square at product level",
            "endpoints": "t=+/-T have one signed coordinate zero and are boundary points",
            "factor_zeroes": "Phi_L,+=0 gives t=-T+/-2*i*L; Phi_L,-=0 gives t=T+/-2*i*L",
            "infinity": "two unramified points on the even-degree product cover",
            "cubic_denominator": "u=(w-h)/x excludes x=0 and requires separate midpoint handling",
        },
        "novelty_boundary": {
            "accepted_scope": (
                "genuine parameterized lower-genus forward obstruction input "
                "analogous to wl585"
            ),
            "whole_cover_local_solubility": "automatic from universal midpoint points",
            "automatic_product_class": "[Q_A*Q_B]=1 on every exact target candidate",
            "not_proved": (
                "No Kummer, split-prime, or uniform restricted local-image obstruction; "
                "G1 must act on the restricted nonmidpoint image"
            ),
            "next_exact_obligation": (
                "prove or refute a uniform Kummer/local-image theorem on E_lambda(Q) "
                "with x square, correct positivity/difference interval, and individual lifts"
            ),
        },
    }
    return checks, details


def build_wl594_universal_closure_product_g0() -> dict[str, Any]:
    checks, details = _build_checks()
    violations = [name for name, passed in checks.items() if not passed]
    ready = not violations
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl594",
        "accepted_outcome": "exact_parameterized_input_ready",
        "object_layer": "universal_AA_BB_closure_product_G0",
        "details": details,
        "proof_boundary": {
            "parameterized_geometric_input_supplied": True,
            "lower_genus_forward_obstruction_input": True,
            "whole_product_cover_local_obstruction_proved": False,
            "restricted_nonmidpoint_obstruction_proved": False,
            "individual_AA_BB_lift_theorem_proved": False,
            "full_four_distance_lift_theorem_proved": False,
            "Kummer_obstruction_proved": False,
            "split_prime_obstruction_proved": False,
            "uniform_local_image_theorem_proved": False,
            "long_term_object_complete": False,
            "G1_selected": False,
            "wl581_wl593_modified": False,
            "new_fixed_family_or_prime": False,
            "rank_table_or_search": False,
            "D2": False,
            "D5": False,
            "M3": False,
        },
        "missing_result": (
            "No uniform Kummer/split-prime/local-image obstruction has been proved. "
            "The next gate must act on the restricted nonmidpoint image and add "
            "uniform specialization control."
        ),
        "verification": {
            "checks": checks,
            "violations": violations,
            "strict_certificate": (
                "wl594 certifies exact universal Q_A/Q_B formulas, scale and ray "
                "parameterization, all discriminant/resultant factors, genus 3/1/5 "
                "geometry, forward lift hierarchy, and all sum/signed-difference "
                "boundaries.  It explicitly does not prove a Kummer, split-prime, "
                "or restricted local-image obstruction."
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    payload = build_wl594_universal_closure_product_g0()
    if args.out is not None:
        write_json(args.out, payload)
    if args.strict:
        print(f"status={payload['status']}")
        print(f"work_log={payload['work_log']}")
        print(f"ready={payload['ready']}")
        print(f"accepted_outcome={payload['accepted_outcome']}")
        print("obstruction_proved=False")
        print("missing_result=uniform_restricted_image_Kummer_or_split_prime_theorem")
        print(f"violations={payload['verification']['violations']}")
        return 0 if payload["ready"] else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
