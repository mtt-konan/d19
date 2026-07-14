#!/usr/bin/env python3
"""Proof data for one Berry degree-six pullback.

The certificate is deliberately single-curve.  It checks the displayed Berry
row, the Kummer and fourth-distance equations, the projective boundary, the
Q(i) factorization, the exact realized twist support, and the arithmetic
branch-set stabilizer.  It does not search for rational points or claim a
Jacobian rank/decomposition.
"""

from __future__ import annotations

import argparse
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT))

try:
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    from json_io import write_json


t, a, b = sp.symbols("t a b")
IMAGINARY_I = sp.I


def berry_row() -> dict[str, sp.Expr]:
    """Return the visually transcribed degree-six Appendix Table 4 row."""
    return {
        "X": t**6 + 6 * t**5 + 29 * t**4 + 44 * t**3 - 13 * t**2 - 2 * t - 1,
        "Y": t**6 + 12 * t**5 + 21 * t**4 - 16 * t**3 - 21 * t**2 + 4 * t - 1,
        "Z": t**6 + 4 * t**5 + 7 * t**4 + 24 * t**3 + 39 * t**2 - 12 * t + 1,
        "T": 10 * t**5 + 40 * t**4 + 28 * t**3 - 24 * t**2 + 10 * t,
    }


def _homogenize_degree(
    poly: sp.Expr,
    variable: sp.Symbol,
    first: sp.Expr,
    second: sp.Expr,
    degree: int,
) -> sp.Expr:
    polynomial = sp.Poly(poly, variable)
    return sp.expand(
        sum(
            coefficient * first ** power[0] * second ** (degree - power[0])
            for power, coefficient in polynomial.terms()
        )
    )


def _conjugate_in_t(poly: sp.Expr) -> sp.Expr:
    return sp.expand(sp.conjugate(poly).xreplace({sp.conjugate(t): t}))


@lru_cache(maxsize=1)
def _branch_stabilizer_certificate() -> dict[str, Any]:
    """Compute the exact PGL2(Q(i)) stabilizer of the 12 branch points.

    Since g and its conjugate are irreducible and distinct over Q(i), a
    stabilizer either preserves g or swaps g with its conjugate.  The c=0 and
    c!=0 charts are normalized by d=1 and c=1 respectively.  The Groebner
    bases below are exact over Q(i), not numerical root matching.
    """
    row = berry_row()
    g = _g6(row)
    gbar = _conjugate_in_t(g)
    scale = sp.symbols("scale")
    mob_a, mob_b, mob_d = sp.symbols("mob_a mob_b mob_d")

    def homogeneous(poly: sp.Expr, first: sp.Expr, second: sp.Expr) -> sp.Expr:
        return _homogenize_degree(poly, t, first, second, 6)

    def basis_for(target: sp.Expr, chart: str) -> list[sp.Expr]:
        if chart == "affine":
            transformed = sp.expand(target.subs(t, mob_a * t + mob_b))
            variables = (scale, mob_b, mob_a)
        else:
            transformed = homogeneous(target, mob_a * t + mob_b, t + mob_d)
            variables = (scale, mob_d, mob_b, mob_a)
        polynomial = sp.Poly(sp.expand(transformed - scale * g), t)
        equations = [polynomial.coeff_monomial(t**k) for k in range(7)]
        basis = sp.groebner(equations, *variables, extension=IMAGINARY_I, order="lex")
        return [sp.expand(item.as_expr()) for item in basis.polys]

    bases = {
        "affine_preserve": basis_for(g, "affine"),
        "affine_swap": basis_for(gbar, "affine"),
        "non_affine_preserve": basis_for(g, "non_affine"),
        "non_affine_swap": basis_for(gbar, "non_affine"),
    }

    def has_exact(items: list[sp.Expr], expected: sp.Expr) -> bool:
        return any(sp.expand(item - expected) == 0 for item in items)

    affine_preserve = bases["affine_preserve"]
    affine_swap = bases["affine_swap"]
    non_affine_preserve = bases["non_affine_preserve"]
    non_affine_swap = bases["non_affine_swap"]
    checks = {
        "affine_preserve_forces_identity": (
            has_exact(affine_preserve, scale - mob_a)
            and has_exact(affine_preserve, mob_a * (mob_a - 1))
            and has_exact(affine_preserve, mob_a * mob_b)
        ),
        "affine_swap_has_no_nonzero_scale": has_exact(affine_swap, scale),
        "non_affine_preserve_has_no_nonzero_scale": has_exact(non_affine_preserve, scale),
        "non_affine_swap_has_no_nonzero_scale": has_exact(non_affine_swap, scale),
    }
    return {
        "checks": checks,
        "stabilizer_is_trivial_over_Qi": all(checks.values()),
        "basis": {name: [str(item) for item in items] for name, items in bases.items()},
        "normalization": {
            "c=0": "d=1",
            "c!=0": "c=1",
            "nonzero_scale_required": True,
        },
    }


def _g6(row: dict[str, sp.Expr]) -> sp.Expr:
    return sp.expand(
        t**6
        + (-2 - 2 * IMAGINARY_I) * t**5
        + (-35 - 8 * IMAGINARY_I) * t**4
        + (-52 - 28 * IMAGINARY_I) * t**3
        + (19 - 40 * IMAGINARY_I) * t**2
        + (6 + 14 * IMAGINARY_I) * t
        - 1
    )


def build_certificate() -> dict[str, Any]:
    row = berry_row()
    X, Y, Z, T = (row[name] for name in ("X", "Y", "Z", "T"))
    f = sp.expand(X**2 + Z**2 - Y**2)
    expected_f = (
        t**12
        - 4 * t**11
        - 62 * t**10
        + 68 * t**9
        + 1647 * t**8
        + 4184 * t**7
        + 2716 * t**6
        - 376 * t**5
        + 623 * t**4
        - 788 * t**3
        + 194 * t**2
        - 12 * t
        + 1
    )
    g = _g6(row)
    gbar = _conjugate_in_t(g)
    A, B = sp.symbols("A B")
    homogeneous_row = {name: _homogenize_degree(poly, t, A, B, 6) for name, poly in row.items()}
    homogeneous_row["T"] = sp.expand(B * _homogenize_degree(T, t, A, B, 5))
    F = _homogenize_degree(f, t, A, B, 12)
    G = _homogenize_degree(g, t, A, B, 6)
    Gbar = _homogenize_degree(gbar, t, A, B, 6)

    h = t**4 + 12 * t**3 + 22 * t**2 - 4 * t + 1
    inverse_relation_1 = sp.expand((X - 2 * Y - Z) - t * (Z - X))
    inverse_relation_2 = sp.expand((-X + 3 * Y + 2 * Z + T) - t * (X - Y + T))
    node5_checks = {
        "Y_mod_h_zero": sp.rem(Y, h, t) == 0,
        "X_minus_Z_mod_h_zero": sp.rem(X - Z, h, t) == 0,
        "T_plus_Z_mod_h_zero": sp.rem(T + Z, h, t) == 0,
        "f_minus_2Z2_mod_h_zero": sp.rem(f - 2 * Z**2, h, t) == 0,
    }
    mod3_f = sp.Poly(f, t, modulus=3)
    mod3_gcd = sp.gcd(mod3_f, sp.Poly(sp.diff(f, t), t, modulus=3))
    gcd_coordinates = sp.gcd(sp.gcd(X, Y), sp.gcd(Z, T))
    f_factor_list = sp.factor_list(f)
    h_factor_list = sp.factor_list(h)
    g_factor_list = sp.factor_list(g, extension=IMAGINARY_I)
    gbar_factor_list = sp.factor_list(gbar, extension=IMAGINARY_I)
    stabilizer = _branch_stabilizer_certificate()

    checks = {
        "surface_equation": sp.expand(
            2 * (Y**4 + T**4) + X**4 + Z**4 - 2 * (X**2 + Z**2) * (Y**2 + T**2)
        )
        == 0,
        "fourth_distance_pullback": f == expected_f,
        "homogeneous_fourth_distance": (
            sp.expand(
                F
                - (
                    homogeneous_row["X"] ** 2
                    + homogeneous_row["Z"] ** 2
                    - homogeneous_row["Y"] ** 2
                )
            )
            == 0
        ),
        "homogeneous_Qi_factorization": sp.expand(F - G * Gbar) == 0,
        "degree_is_12": sp.degree(f, t) == 12,
        "f_irreducible_over_Q": (
            len(f_factor_list[1]) == 1
            and f_factor_list[1][0][1] == 1
            and sp.degree(f_factor_list[1][0][0], t) == 12
        ),
        "f_squarefree_over_Q": sp.gcd(f, sp.diff(f, t)) == 1,
        "f_squarefree_mod_3": mod3_gcd.as_expr() == 1,
        "g_squarefree": sp.gcd(g, sp.diff(g, t), extension=IMAGINARY_I) == 1,
        "gbar_squarefree": sp.gcd(gbar, sp.diff(gbar, t), extension=IMAGINARY_I) == 1,
        "factor_resultant_is_2_40": sp.resultant(g, gbar, t) == 2**40,
        "factor_gcd_is_one": sp.gcd(g, gbar, extension=IMAGINARY_I) == 1,
        "no_projective_basepoint": (
            gcd_coordinates == 1 and homogeneous_row["X"].subs({A: 1, B: 0}) == 1
        ),
        "inverse_relation_one": inverse_relation_1 == 0,
        "inverse_relation_two": inverse_relation_2 == 0,
        "node5_boundary": all(node5_checks.values()),
        "node5_parameter_has_no_Q_root": (
            len(h_factor_list[1]) == 1
            and h_factor_list[1][0][1] == 1
            and sp.degree(h_factor_list[1][0][0], t) == 4
        ),
        "T_zero_has_only_rational_root_zero": sp.ground_roots(T) == {sp.Integer(0): 1},
        "infinity_F_is_one": F.subs({A: 1, B: 0}) == 1,
        "zero_F_is_one": f.subs(t, 0) == 1,
        "branch_stabilizer_trivial": stabilizer["stabilizer_is_trivial_over_Qi"],
    }
    violations = [name for name, passed in checks.items() if passed is not True]
    return {
        "status": "ok" if not violations else "invalid",
        "ready": not violations,
        "task": "berry-sextic-pilot-feasibility-certificate",
        "outcome": "berry_sextic_pipeline_ready",
        "selected_curve": {
            "source": "Berry 1990 Appendix Table 4, degree 6 row",
            "body_reference": "Proposition 4.3/4.4 calls the same displayed table Table 5",
            "visual_pages": ["printed 528 (Table 4)", "printed 526 (Proposition 4.4)"],
            "visual_transcription_checked": True,
            "symbolic_substitution_checked": True,
            "degree": 6,
            "projection_description": (
                "Berry says this sextic is the projection of trope C7 from node 5"
            ),
            "coordinates": {name: str(poly) for name, poly in row.items()},
        },
        "surface": {
            "equation": "2*(Y^4+T^4)+X^4+Z^4=2*(X^2+Z^2)*(Y^2+T^2)",
            "fourth_distance_equation": "U^2+Y^2=X^2+Z^2",
            "pullback": str(f),
            "pullback_degree": 12,
            "smooth_projective_genus": 5,
            "squarefree_mod_3": "gcd(f mod 3, derivative mod 3)=1",
            "mod_3_factorization": str(sp.factor(f, modulus=3)),
        },
        "projective_and_degenerate_parameters": {
            "homogeneous_parameter": "(A:B), t=A/B",
            "homogeneous_coordinates": {name: str(poly) for name, poly in homogeneous_row.items()},
            "infinity_image": "(1:1:1:0), F(1,0)=1, W=+/-1",
            "zero_image": "(-1:-1:1:0), f(0)=1, U=+/-1",
            "node_preimages": {
                "t=1": "(1:0:1:1), f=8192=2^13, no rational U",
                "t=-1": "(1:0:-1:1), f=2048=2^11, no rational U",
                "t=0": "(1:1:-1:0) up to overall sign, f=1",
                "h(t)=0": "node (1:0:1:-1), f=2*Z^2; h has no rational root",
                "t=infinity": "(1:1:1:0)",
            },
            "node5_polynomial": str(h),
            "T_zero_factorization": str(sp.factor(T)),
            "rational_branch_parameters": "none because f is irreducible over Q",
            "known_rational_trivial_points": ["(t,U)=(0,+/-1)", "(infinity,W)= (+/-1)"],
            "basepoint_free": True,
        },
        "map_and_converse": {
            "relation_one": str(inverse_relation_1),
            "relation_two": str(inverse_relation_2),
            "generic_inverse": "t=(X-2*Y-Z)/(Z-X)",
            "switch_inverse": "t=(-X+3*Y+2*Z+T)/(X-Y+T) at t=1",
            "exceptional_normalization_fiber": "h(t)=0 maps to node 5; no rational h-root",
            "converse": (
                "Every rational parameter gives a surface point; U^2=f(t) is "
                "equivalent to the fourth equation, including infinity via F(A,B)"
            ),
        },
        "Q_i_factorization": {
            "g6": str(g),
            "conjugate_g6": str(gbar),
            "exact_identity": "f=g6*conjugate(g6)",
            "factorization_over_Qi": {
                "g_is_irreducible": (len(g_factor_list[1]) == 1 and g_factor_list[1][0][1] == 1),
                "gbar_is_irreducible": (
                    len(gbar_factor_list[1]) == 1 and gbar_factor_list[1][0][1] == 1
                ),
            },
            "gcd_common_root": "1",
            "resultant": "2^40",
            "tangency": (
                "gcd(g,g')=gcd(gbar,gbar')=1; f is squarefree, so no common-root or tangency branch"
            ),
            "squareclass_statement": (
                "No extra constant or square factor: monic squarefree f is exactly g6*conjugate(g6)"
            ),
        },
        "realized_support_descent": {
            "primitive_coordinates": "t=A/B with gcd(A,B)=1; G(A,B)=B^6*g6(A/B)",
            "norm_identity": "G(A,B)*conjugate(G(A,B))=F(A,B)=W^2 for every rational C-point",
            "resultant_support": "Res(g6,conjugate(g6))=2^40",
            "support_group": "<i>={1,i} in Q(i)^*/Q(i)^{*2}",
            "proof": [
                "At every Gaussian prime away from 2, a common divisor of "
                "G(A,B) and conjugate(G(A,B)) would give a common projective "
                "root and divide the resultant.",
                "Away from 2 only one conjugate factor can occur, and its "
                "exponent in the rational square norm is even.",
                "At 1+i, v_(1+i)(G*conjugate(G))=2*v_(1+i)(G), while "
                "v_(1+i)(W^2)=4*v_2(W), so v_(1+i)(G) is even; the only "
                "remaining squareclasses are the two unit classes 1 and i.",
            ],
            "covers": [
                {
                    "twist": "d=1",
                    "equation": "v^2=g6(t) over Q(i)",
                    "genus": 2,
                    "infinity": "two Q(i)-points",
                },
                {
                    "twist": "d=i",
                    "equation": "i*v^2=g6(t) over Q(i)",
                    "genus": 2,
                    "infinity": "no Q(i)-point at infinity because -i is not a Q(i)-square",
                },
            ],
            "literal_cover": {
                "equations": [
                    "d*v^2=g6(t)",
                    "conjugate(d)*w^2=conjugate(g6)(t)",
                ],
                "map": "U=v*w",
                "genus": 9,
                "reason": "degree-four V4 cover of P1 with twelve simple branch points",
            },
            "exact_obligation": (
                "For d in {1,i}, determine K-points on d*v^2=g6(t) with "
                "t in P^1(Q); recover U=+/-Norm_K/Q(v). Include the two "
                "projective charts and the node/factor-zero strata."
            ),
            "converse": (
                "Every rational point on C lifts to one of these two twist "
                "equations, and every such K-point with rational t gives a "
                "rational C-point by U=+/-v*conjugate(v)."
            ),
        },
        "quotient_and_jacobian_audit": {
            "branch_stabilizer": stabilizer,
            "genuine_Qi_PGL2_quotient": False,
            "polynomial_factorization_is_not_Jacobian_split": True,
            "sage_tool_boundary": (
                "Sage 10.9 exposes genus, Jacobian construction, and bounded "
                "rational_points, but no generic rank/decomposition/NS-stabilizer "
                "certificate for this genus-5 Jacobian."
            ),
            "rank_or_decomposition_obtained": False,
            "next_tool": (
                "specialized genus-2 arithmetic over Q(i), with rational t "
                "restriction; no rank claim is made here"
            ),
        },
        "verification": {"checks": checks, "violations": violations},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_certificate()
    if args.out is not None:
        write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"task={payload['task']}")
    print(f"ready={payload['ready']}")
    print(f"outcome={payload['outcome']}")
    print(f"violations={payload['verification']['violations']}")
    if args.strict and not payload["ready"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
