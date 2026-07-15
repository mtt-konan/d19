#!/usr/bin/env python3
"""Post-B0 feasibility certificate for the committed Berry sextic pilot.

The exact local and finite-field arithmetic in this certificate is independently
reproduced by ``berry_sextic_post_b0.sage``. This Python file keeps the reviewed
proof data and tool-capability result available to focused tests without making
Sage a runtime dependency of the ordinary test suite.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    from json_io import write_json


def _local_obstruction() -> dict[str, Any]:
    return {
        "field": "K_(1+i)=Q_2(i)",
        "uniformizer": "pi=1+i",
        "relations": ["pi^2=2*i", "2=-i*pi^2"],
        "square_unit_lemma": (
            "Every unit square is 1 modulo pi^2: if u=1+pi*a, then "
            "u^2=1+2*pi*a+pi^2*a^2 is congruent to 1 modulo pi^2."
        ),
        "twisted_affine_polynomial": "f(t)=(-i)*g6(t), so v^2=f(t)",
        "shift": "z=t+1",
        "shifted_coefficient_valuations_low_to_high": [11, 10, 8, 9, 3, 2, 0],
        "shifted_coefficient_unit_residues_mod_pi": [1, 1, 1, 1, 1, 1, 1],
        "valuation_partition": [
            {
                "condition": "v_pi(z)=0",
                "v_pi(f(t))": 0,
                "normalized_unit_mod_pi2": "1+pi",
            },
            {
                "condition": "v_pi(z)=1",
                "v_pi(f(t))": 6,
                "normalized_unit_mod_pi2": "1+pi",
            },
            {
                "condition": "v_pi(z)=2",
                "v_pi(f(t))": 13,
                "normalized_unit_mod_pi2": "not needed; odd valuation",
            },
            {
                "condition": "v_pi(z)>=3",
                "v_pi(f(t))": 11,
                "normalized_unit_mod_pi2": "not needed; odd valuation",
            },
        ],
        "v_pi_z_equals_2_polynomial": (
            "Q(u)=pi^(-11)*f(-1+pi^2*u)=i+(3+i)u+(1+i)u^2+(8+4*i)u^3+(2-3*i)u^4+(3+5*i)u^5+(1-i)u^6"
        ),
        "v_pi_z_equals_2_residue_table": [
            {"u_mod_pi3": "1", "v_pi(Q(u))": 2, "Q(u)/pi^2_mod_pi": 1},
            {"u_mod_pi3": "1+pi", "v_pi(Q(u))": 2, "Q(u)/pi^2_mod_pi": 1},
            {"u_mod_pi3": "1+pi^2", "v_pi(Q(u))": 2, "Q(u)/pi^2_mod_pi": 1},
            {
                "u_mod_pi3": "1+pi+pi^2",
                "v_pi(Q(u))": 2,
                "Q(u)/pi^2_mod_pi": 1,
            },
        ],
        "reciprocal_chart": {
            "coordinates": "x=1/t, w=v/t^3",
            "equation": "w^2=(-i)*g6_star(x)",
            "g6_star": ("1+(-2-2*i)x+(-35-8*i)x^2+(-52-28*i)x^3+(19-40*i)x^4+(6+14*i)x^5-x^6"),
            "domain": "v_pi(x)>=1 for v_pi(t)<0, with x=0 at infinity",
            "congruence": "(-i)*g6_star(x) is congruent to -i is congruent to 1+pi modulo pi^2",
            "valuation": 0,
        },
        "conclusion": (
            "C_i has no K_(1+i)-point. The finite branch/factor-zero case is "
            "included in the valuation partition, and x=0 is the explicit infinity chart."
        ),
    }


def _torsion_certificate() -> dict[str, Any]:
    rows = [
        {
            "rational_prime": 3,
            "prime_type": "inert",
            "q": 9,
            "N1": 8,
            "N2": 106,
            "J_C1": 76,
            "factor_C1": "2^2*19",
            "J_Ci": 76,
            "factor_Ci": "2^2*19",
        },
        {
            "rational_prime": 5,
            "prime_type": "split; use (5,i-2)",
            "q": 5,
            "N1_C1": 7,
            "N2_C1": 39,
            "J_C1": 39,
            "factor_C1": "3*13",
            "N1_Ci": 5,
            "N2_Ci": 39,
            "J_Ci": 27,
            "factor_Ci": "3^3",
        },
        {
            "rational_prime": 7,
            "prime_type": "inert",
            "q": 49,
            "N1": 58,
            "N2": 2448,
            "J_C1": 2857,
            "factor_C1": "2857",
            "J_Ci": 2857,
            "factor_Ci": "2857",
        },
        {
            "rational_prime": 13,
            "prime_type": "split; use (13,i-5)",
            "q": 13,
            "N1_C1": 10,
            "N2_C1": 188,
            "J_C1": 131,
            "factor_C1": "131",
            "N1_Ci": 18,
            "N2_Ci": 188,
            "J_Ci": 243,
            "factor_Ci": "3^5",
        },
        {
            "rational_prime": 17,
            "prime_type": "split; use (17,i-4)",
            "q": 17,
            "N1": 16,
            "N2": 342,
            "J_C1": 282,
            "factor_C1": "2*3*47",
            "J_Ci": 282,
            "factor_Ci": "2*3*47",
        },
        {
            "rational_prime": 29,
            "prime_type": "split; use (29,i-12)",
            "q": 29,
            "N1_C1": 35,
            "N2_C1": 895,
            "J_C1": 1031,
            "factor_C1": "1031",
            "N1_Ci": 25,
            "N2_Ci": 895,
            "J_Ci": 731,
            "factor_Ci": "17*43",
        },
        {
            "rational_prime": 37,
            "prime_type": "split; use (37,i-6)",
            "q": 37,
            "N1_C1": 56,
            "N2_C1": 1344,
            "J_C1": 2203,
            "factor_C1": "2203",
            "N1_Ci": 20,
            "N2_Ci": 1344,
            "J_Ci": 835,
            "factor_Ci": "5*167",
        },
    ]
    return {
        "proof_flags": (
            "Sage proof.all(True); exact finite-field count_points(2) and Jacobian.cardinality()"
        ),
        "point_count_formula": ("a1=q+1-N1; a2=(N2-q^2-1+a1^2)/2; #J(F_q)=q^2+1+a2-(q+1)*a1"),
        "good_reduction_reason": (
            "Every listed prime is outside the exact discriminant support {(1+i),(94*i-169)}."
        ),
        "rows": rows,
        "raw_gcd_all_rows": {"C_1": 1, "C_i": 1},
        "primary_safe_bound": {
            "method": (
                "For each ell, take min v_ell(#J(k_v)) only over rows whose "
                "residue characteristic is not ell."
            ),
            "C_1": 1,
            "C_i": 1,
        },
        "conclusion": "J_1(K)_tors=0 and J_i(K)_tors=0.",
    }


def _support_certificate() -> dict[str, Any]:
    return {
        "exact_discriminant": "Disc(g6)=(i-1)^75*(94*i-169)",
        "twist_discriminant": "Disc((-i)*g6)=(-i)^10*Disc(g6), with (-i)^10 a unit",
        "leading_coefficients": {"C_1": "1", "C_i": "-i"},
        "model_sufficient_finite_support": ["(1+i)", "(94*i-169)"],
        "minimality_claimed": False,
        "conservative_finite_support": [
            "(1+i)",
            "(94*i-169)",
            "(-94*i-169)",
        ],
        "extra_support_explanation": {
            "conjugate_prime": (
                "Only needed for the conjugate/Berry norm pullback, not either selected Jacobian."
            ),
            "leading_coefficient": (
                "Both leading coefficients are units, so they add no finite prime."
            ),
            "twist_unit": "i and -i are units, so the quadratic twist adds no finite prime.",
            "archimedean": (
                "The unique archimedean place is complex; it may be listed for "
                "bookkeeping, but H^1(C,mu_2)=0."
            ),
            "chart_primes": (
                "2,5,43,53 belong to optional rational chart-fiber separability "
                "and are not Jacobian 2-descent support."
            ),
        },
        "sufficiency_argument": (
            "Outside 2*Disc(g6)*leading_coefficient, the branch algebra is etale and "
            "the hyperelliptic model has good reduction. Divisor evaluation classes "
            "are unramified there, hence have even valuation and cannot add a Kummer "
            "support prime. This proves sufficiency, not minimality."
        ),
        "exact_base_field_squareclass_probe": {
            "command": "K.selmer_generators([(1+i),(94*i-169)],2,proof=True,orders=True)",
            "generators": ["i-1", "94*i-169", "i"],
            "orders": [2, 2, 2],
            "scope": (
                "Exact K^*/K^*2 S-squareclass computation only; not a Jacobian "
                "2-Selmer computation."
            ),
        },
    }


def _toolchain_certificate() -> dict[str, Any]:
    return {
        "sage": {
            "executable": "/usr/local/bin/sage",
            "version": "10.9 (2026-05-04)",
            "proof_flags": "proof.all(True) executed",
            "finite_field_jacobian_cardinality": "available and exact",
            "number_field_jacobian_cardinality": (
                "NotImplementedError: order computation is only implemented for "
                "Jacobians over finite fields"
            ),
            "number_field_methods_absent": [
                "C.two_descent",
                "J.two_descent",
                "J(K).torsion_subgroup",
                "J(K).selmer_group",
                "J.local_kummer_image",
                "C.local_points",
            ],
            "proof_flag_probe": (
                "J(K).rational_points(proof=True) rejects proof with TypeError; "
                "no point search was used."
            ),
            "available_exact_field_route": (
                "K.selmer_generators(..., proof=True, orders=True) only computes "
                "the base-field S-squareclass container."
            ),
        },
        "magma": {
            "executable_found": False,
            "probe": (
                "command -v magma Magma magma-cli magma64 and standard application/bin "
                "paths returned no executable"
            ),
            "route": (
                "No installed Magma route to probe; Sage Magma interface source "
                "alone is not a capability."
            ),
        },
        "public_magma_calculator": {
            "version": "2.29-8",
            "endpoint": "http://magma.maths.usyd.edu.au/xml/calculator.xml",
            "input_limit_bytes": 50_000,
            "time_limit_seconds": 60,
            "selected_curve_constructed": True,
            "intrinsics": {
                "TwoSelmerGroup": True,
                "TwoCoverDescent": True,
                "RankBounds": True,
                "LocalKummerImage": False,
            },
            "full_two_selmer_attempt": "service_timeout",
            "two_selmer_data_mode": (
                "rejects the Q(i) Jacobian because TwoSelmerGroupData requires "
                "the rationals as base field"
            ),
            "arithmetic_conclusion": None,
        },
        "arithmetic_blocker_promoted": False,
        "reason": (
            "The public exact TwoSelmerGroup attempt hit its service time limit "
            "before producing Selmer or local-image data, so there is no concrete "
            "unresolved dyadic local Kummer image to promote as a blocker."
        ),
    }


def build_post_b0_audit() -> dict[str, Any]:
    return {
        "status": "complete",
        "outcome": "post_b0_feasibility_audit",
        "accepted_b0_checkpoint": "dccbd9a",
        "stable_model_required_before_B1_B2": False,
        "local_obstruction": _local_obstruction(),
        "torsion": _torsion_certificate(),
        "support": _support_certificate(),
        "toolchain": _toolchain_certificate(),
        "next_smallest_step": (
            "Run the exact C_1 Jacobian TwoSelmerGroup input without the public "
            "60-second limit, or implement and certify its two local Kummer images "
            "before making any Selmer or point-classification claim."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    payload = build_post_b0_audit()
    if args.out is not None:
        write_json(args.out, payload)
    print("status=complete")
    print("task=berry-sextic-post-b0-feasibility")
    print("outcome=post_b0_feasibility_audit")
    print("C_i_local_at_(1+i)=obstructed")
    print("J_1_torsion_bound=1")
    print("J_i_torsion_bound=1")
    print("arithmetic_blocker_promoted=False")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
