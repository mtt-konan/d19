#!/usr/bin/env python3
"""Audit the wl529 square-specialization locus for the wl528 prototype."""

from __future__ import annotations

import argparse
import importlib
import json
import os
import subprocess
import tempfile
from functools import lru_cache
from math import isqrt
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl528_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl528_v5_l1_t5_function_field_prototype"
    )
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    wl528_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl528_v5_l1_t5_function_field_prototype"
    )
    from json_io import load_json, write_json


MARKER = "WL529_SAGE_JSON "
TARGET_CANDIDATE_IDS = list(wl528_module.TARGET_CANDIDATE_IDS)
FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

BOUNDARY = (
    "This audits only wl529 / the specialization-square locus for the single "
    "wl528 prototype support=v_5|L=1|T=5|d=(5,1,5). It constructs the exact "
    "square-locus equation for (N^2+16)(M^2+16), clears denominators over the "
    "wl528 quartic, identifies the centered-even genus-one square-locus model, "
    "classifies its rational points by a single-curve elliptic certificate, "
    "checks whether any rational point survives the required nonexceptional "
    "positivity domain |t|<5 on the prototype quartic, and stops. It does not "
    "execute shell 11, compute new supports, touch another cover family, run "
    "broad rank or Selmer diagnostics, use the old package-x S~ bridge, prove "
    "a uniform cover-family obstruction, or claim a complete Sel_2(E) upper "
    "bound, rank zero, Sha[2]=0, uniform M_tail full rank, or family exclusion."
)


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl528_ready(wl528: dict[str, Any]) -> bool:
    proof = wl528.get("proof_status", {})
    return (
        wl528.get("status") == "ok"
        and wl528.get("ready") is True
        and wl528.get("work_log") == "wl528"
        and wl528.get("object_layer") == "single_cover_family_function_field_prototype"
        and proof.get("function_field_nonsquare_certificate_proved_here") is True
        and proof.get("uniform_cover_family_obstruction_proved_here") is False
        and wl528.get("prototype_scope", {}).get("candidate_ids") == TARGET_CANDIDATE_IDS
        and not _claims_forbidden_bound(wl528)
    )


def _sympy_reduces_to_zero(expr: sp.Expr, *, r: sp.Symbol, y: sp.Symbol) -> bool:
    function_field_rhs = 5 * r**4 - 264 * r**2 + 2000
    numerator = sp.together(expr).as_numer_denom()[0]
    remainder = sp.rem(
        sp.Poly(sp.expand(numerator), y),
        sp.Poly(y**2 - function_field_rhs, y),
    ).as_expr()
    return sp.factor(remainder) == 0


def _square_locus_identity_checks() -> list[dict[str, Any]]:
    r, y, t, u, X, Y = sp.symbols("r y t u X Y")
    t_value = y * (r**2 + 20) / (4 * r * (r**2 - 20))
    n_value = (5 + t_value) / 2
    m_value = (5 - t_value) / 2
    opposite_product = (n_value**2 + 16) * (m_value**2 + 16)
    t_square_relation = (
        16 * r**2 * (r**2 - 20) ** 2 * t_value**2
        - (r**2 + 20) ** 2 * (5 * r**4 - 264 * r**2 + 2000)
    )
    quartic_in_t = t**4 + 78 * t**2 + 7921
    checks = [
        (
            "exact_opposite_square_locus_identity",
            "16*(N^2+16)*(M^2+16) = (t^2+39)^2 + 6400",
            16 * opposite_product - ((t_value**2 + 39) ** 2 + 6400),
            True,
        ),
        (
            "cleared_denominator_t_square_relation",
            "16*r^2*(r^2-20)^2*t^2 = (r^2+20)^2*(5*r^4-264*r^2+2000)",
            t_square_relation,
            True,
        ),
        (
            "genus_one_elliptic_quotient_map",
            "Y=t*U, X=t^2 sends U^2=t^4+78*t^2+7921 to Y^2=X^3+78*X^2+7921*X",
            Y**2 - (X**3 + 78 * X**2 + 7921 * X),
            False,
        ),
    ]

    payload: list[dict[str, Any]] = []
    for check_id, identity, expr, reduce_on_wl528 in checks:
        if reduce_on_wl528:
            passed = _sympy_reduces_to_zero(expr, r=r, y=y)
        else:
            passed = sp.factor(
                expr.subs({X: t**2, Y: t * u}) - t**2 * (u**2 - quartic_in_t)
            ) == 0
        payload.append(
            {
                "check_id": check_id,
                "identity": identity,
                "verified": passed,
            }
        )

    quartic = sp.Poly(sp.expand(quartic_in_t), t)
    squarefree = sp.gcd(quartic, quartic.diff()) == 1
    payload.append(
        {
            "check_id": "square_locus_quartic_is_squarefree",
            "identity": "gcd(t^4+78*t^2+7921, 4*t*(t^2+39)) = 1",
            "verified": squarefree,
        }
    )
    return payload


def _square_locus_models() -> dict[str, Any]:
    return {
        "t_parameter": "t = y*(r^2+20)/(4*r*(r^2-20))",
        "positivity_domain": "|t| < 5",
        "positive_source_condition": "N=(5+t)/2 > 0 and M=(5-t)/2 > 0",
        "square_locus_affine_curve": {
            "variables": ["t", "U"],
            "definition": "U^2 = t^4 + 78*t^2 + 7921",
            "note": "Here U = 4*s, so U^2 = 16*(N^2+16)(M^2+16).",
        },
        "cleared_denominator_relation_over_wl528_quartic": (
            "16*r^2*(r^2-20)^2*t^2 = (r^2+20)^2*(5*r^4-264*r^2+2000)"
        ),
        "projective_intersection_of_quadrics": [
            "V*Z = T^2 + 39*Z^2",
            "U^2 = V^2 + 6400*Z^2",
        ],
        "square_locus_and_elliptic_quotient": {
            "square_locus": "U^2 = t^4 + 78*t^2 + 7921",
            "elliptic_quotient": "Y^2 = X^3 + 78*X^2 + 7921*X",
            "degree_two_map": "X = t^2, Y = t*U",
            "point_classification_rule": (
                "D(Q) maps into E(Q) with X a rational square; this map is "
                "not asserted to be a birational equivalence"
            ),
        },
    }


def _sage_program() -> str:
    return f"""
import json
from sage.all import EllipticCurve, QQ

def qq_is_square(value):
    return bool(
        value >= 0
        and value.numerator().is_square()
        and value.denominator().is_square()
    )

E = EllipticCurve([0, 78, 0, 7921, 0])
torsion_points = []
square_x_values = []
for point in E.torsion_points():
    if point.is_zero():
        torsion_points.append({{"kind": "infinity"}})
        continue
    x_value = QQ(point[0])
    y_value = QQ(point[1])
    record = {{
        "x": str(x_value),
        "y": str(y_value),
        "x_is_rational_square": qq_is_square(x_value),
    }}
    torsion_points.append(record)
    if record["x_is_rational_square"]:
        square_x_values.append(record["x"])

payload = {{
    "status": "ok",
    "rank": int(E.rank(proof=True)),
    "rank_method": "E.rank(proof=True)",
    "rank_is_proved": True,
    "torsion_invariants": [int(value) for value in E.torsion_subgroup().invariants()],
    "torsion_points": torsion_points,
    "square_x_values": square_x_values,
}}
print({MARKER!r} + json.dumps(payload, separators=(",", ":")), flush=True)
"""


def _parse_marker(stdout: str) -> dict[str, Any] | None:
    for line in stdout.splitlines():
        if line.startswith(MARKER):
            return json.loads(line[len(MARKER) :])
    return None


@lru_cache(maxsize=1)
def _sage_genus_one_certificate() -> dict[str, Any]:
    env = os.environ.copy()
    with (
        tempfile.TemporaryDirectory(prefix="d19-wl529-dot-sage-", dir="/private/tmp") as dot_sage,
        tempfile.TemporaryDirectory(prefix="d19-wl529-tmp-", dir="/private/tmp") as tmpdir,
    ):
        env["DOT_SAGE"] = dot_sage
        env["TMPDIR"] = tmpdir
        completed = subprocess.run(
            ["sage", "-python", "-c", _sage_program()],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
    marker = _parse_marker(completed.stdout)
    if completed.returncode != 0 or marker is None:
        return {
            "status": "sage_error",
            "returncode": int(completed.returncode),
            "stdout_tail": completed.stdout.splitlines()[-20:],
            "stderr_tail": completed.stderr.splitlines()[-20:],
        }
    return marker


def _t_zero_preimage_analysis() -> dict[str, Any]:
    r, x = sp.symbols("r x")
    quartic_rhs = 5 * r**4 - 264 * r**2 + 2000
    quadratic = sp.Poly(5 * x**2 - 264 * x + 2000, x)
    discriminant = int(sp.discriminant(quadratic.as_expr(), x))
    discriminant_factorization = {
        str(prime): int(exponent)
        for prime, exponent in sp.factorint(abs(discriminant)).items()
    }
    discriminant_is_square = (
        discriminant >= 0 and isqrt(discriminant) ** 2 == discriminant
    )
    substitution_verified = (
        sp.expand(quartic_rhs.subs(r**2, x)) == quadratic.as_expr()
    )
    t_zero_forces_y_zero = True  # r^2 + 20 > 0 for every rational r.
    certificate_verified = (
        t_zero_forces_y_zero
        and substitution_verified
        and discriminant == 29696
        and discriminant_factorization == {"2": 10, "29": 1}
        and not discriminant_is_square
    )
    return {
        "candidate_t_value": 0,
        "derived_r2_equation": "5*x^2 - 264*x + 2000 = 0 with x = r^2",
        "t_zero_forces_y_zero": t_zero_forces_y_zero,
        "quadratic_substitution_verified": substitution_verified,
        "quadratic_discriminant_computed": True,
        "discriminant": discriminant,
        "discriminant_factorization": discriminant_factorization,
        "discriminant_is_rational_square": discriminant_is_square,
        "r2_roots": [
            "(132 - 16*sqrt(29))/5",
            "(132 + 16*sqrt(29))/5",
        ],
        "certificate_verified": certificate_verified,
        "rational_preimage_exists_on_wl528_quartic": (
            False if certificate_verified else None
        ),
        "logic": (
            "At nonexceptional points, t=0 forces y=0 and therefore "
            "5*r^4-264*r^2+2000=0. Writing x=r^2 gives a quadratic whose "
            "discriminant is 2^10*29, not a rational square, so no rational "
            "r survives."
        ),
    }


def _rational_point_analysis(
    sage_certificate: dict[str, Any],
) -> dict[str, Any]:
    t_zero = _t_zero_preimage_analysis()
    square_x_values = sage_certificate.get("square_x_values", [])
    point_classification_closed = (
        sage_certificate.get("status") == "ok"
        and sage_certificate.get("rank") == 0
        and sage_certificate.get("rank_method") == "E.rank(proof=True)"
        and sage_certificate.get("rank_is_proved") is True
        and sage_certificate.get("torsion_invariants") == [4]
        and square_x_values == ["0"]
    )
    preimage_excluded = (
        t_zero.get("certificate_verified") is True
        and t_zero.get("rational_preimage_exists_on_wl528_quartic") is False
    )
    return {
        "positivity_domain": "|t| < 5",
        "positive_source_condition": "N=(5+t)/2 > 0 and M=(5-t)/2 > 0",
        "elliptic_curve_rational_point_summary": (
            "Any rational square specialization on the genus-one square-locus "
            "maps to E(Q) with X=t^2 a rational square."
        ),
        "affine_square_locus_rational_t_candidates": [0] if point_classification_closed else [],
        "affine_square_locus_rational_points": [
            {"t": 0, "U": 89},
            {"t": 0, "U": -89},
        ]
        if point_classification_closed
        else [],
        "t_zero_preimage_analysis": t_zero,
        "nonexceptional_positive_square_specializations_exist": False
        if point_classification_closed and preimage_excluded
        else None,
        "conclusion": (
            "The genus-one square-locus has only t=0 over Q, and t=0 has no "
            "rational preimage on the wl528 quartic. Therefore the selected "
            "prototype has no rational square specialization in the required "
            "nonexceptional positivity domain."
        )
        if point_classification_closed and preimage_excluded
        else "Genus-one rational point classification did not isolate only t=0.",
    }


def build_wl529_v5_l1_t5_square_locus(*, wl495: dict[str, Any]) -> dict[str, Any]:
    violations: list[str] = []

    wl528 = wl528_module.build_wl528_v5_l1_t5_function_field_prototype(wl495=wl495)
    if not _wl528_ready(wl528):
        violations.append("wl528_input_not_ready_or_not_scoped")

    identity_checks = _square_locus_identity_checks()
    if not all(check["verified"] is True for check in identity_checks):
        violations.append("square_locus_identity_check_failed")

    sage_certificate = _sage_genus_one_certificate()
    sage_ok = (
        sage_certificate.get("status") == "ok"
        and sage_certificate.get("rank") == 0
        and sage_certificate.get("rank_method") == "E.rank(proof=True)"
        and sage_certificate.get("rank_is_proved") is True
        and sage_certificate.get("torsion_invariants") == [4]
        and sage_certificate.get("square_x_values") == ["0"]
    )
    if not sage_ok:
        violations.append("genus_one_rational_point_certificate_failed")

    rational_point_analysis = _rational_point_analysis(sage_certificate)
    if (
        rational_point_analysis.get("t_zero_preimage_analysis", {}).get(
            "certificate_verified"
        )
        is not True
    ):
        violations.append("t_zero_preimage_certificate_failed")
    if (
        rational_point_analysis.get("nonexceptional_positive_square_specializations_exist")
        is not False
    ):
        violations.append("nonexceptional_positive_square_specialization_not_closed")

    status = "ok" if not violations else "issues"
    proof_status = (
        {
            "square_locus_constructed_here": True,
            "generic_function_field_nonsquare_carried_from_wl528": True,
            "divisor_parity_certificate_proved_here": False,
            "divisor_parity_only_proves_generic_nonsquareness": True,
            "genus_one_rational_point_certificate_proved_here": sage_ok,
            "nonexceptional_positive_square_specialization_absent": (
                rational_point_analysis.get("nonexceptional_positive_square_specializations_exist")
                is False
            ),
            "one_family_positive_square_obstruction_proved_here": (
                rational_point_analysis.get("nonexceptional_positive_square_specializations_exist")
                is False
            ),
            "uniform_cover_family_obstruction_proved_here": False,
            "ready_as_reviewable_single_family_square_locus": True,
            "ready_as_uniform_cover_family_theorem": False,
            "exact_remaining_gap": (
                "None for this one-family nonexceptional positivity-domain "
                "square-locus analysis. The wider uniform cover-family theorem "
                "remains outside the wl529 stop condition."
            ),
        }
        if status == "ok"
        else {}
    )

    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl528 prototype plus single-curve genus-one square-locus analysis",
        "pattern": "AA+BB",
        "lemma_id": "WL529_v5_l1_t5_square_locus",
        "work_log": "wl529",
        "input_work_logs": ["wl528", "wl495"],
        "object_layer": "single_cover_family_square_specialization_locus",
        "prototype_scope": {
            "support": "v_5",
            "L": 1,
            "T": 5,
            "d_vector": {"d_minus_p": 5, "d_pos_2sqrt_q": 1, "d_neg_2sqrt_q": 5},
            "candidate_ids": TARGET_CANDIDATE_IDS,
            "touches_only_one_cover_family": True,
        },
        "selected_wl495_entries": wl528.get("selected_wl495_entries", []) if status == "ok" else [],
        "wl528_prototype_status": {
            "status": wl528.get("status"),
            "function_field_nonsquare_certificate_proved_here": wl528.get("proof_status", {}).get(
                "function_field_nonsquare_certificate_proved_here"
            ),
            "exact_remaining_gap_from_wl528": wl528.get("proof_status", {}).get(
                "exact_remaining_gap"
            ),
        },
        "square_locus_models": _square_locus_models(),
        "identity_checks": identity_checks,
        "genus_one_certificate": sage_certificate,
        "rational_point_analysis": rational_point_analysis,
        "boundary_note": (
            "Divisor parity only proves generic nonsquareness of the function-field "
            "element. By itself it cannot rule out every rational specialization "
            "landing on a square value; wl529 closes that pointwise gap for this "
            "one family by classifying the square-locus rational points."
        ),
        "proof_status": proof_status,
        "violations": violations,
        "boundary": BOUNDARY,
        "shell11_executed_here": False,
        "m_tail_diagnostics_extended_here": False,
        "new_supports_computed_here": False,
        "new_c_d_solubility_tested_here": False,
        "wl491_filter_applied_to_new_point_here": False,
        "broad_rank_or_selmer_diagnostics_run": False,
        "old_package_x_coordinate_collapse_used": False,
        "package_x_s_tilde_bridge_used": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "uniform_m_tail_full_rank_claimed": False,
        "family_exclusion_proved_count": 0,
        "advance_to_next_cover_family": False,
        "advance_to_next_roadmap_step": False,
        "stop_after_current_task": True,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--wl495",
        type=Path,
        default=Path("results/closure_quotient_rank_zero_aa_bb_wl495_route_refreshed_support.json"),
        help="Input wl495 refreshed-support JSON.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("results/closure_quotient_rank_zero_aa_bb_wl529_v5_l1_t5_square_locus.json"),
        help="Output path for the wl529 square-locus audit JSON.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit nonzero if the build status is not ok.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    wl495 = load_json(args.wl495)
    payload = build_wl529_v5_l1_t5_square_locus(wl495=wl495)
    write_json(args.out, payload)
    print(
        "status={status} work_log={work_log} "
        "one_family_positive_square_obstruction_proved_here={obstruction} "
        "uniform_cover_family_obstruction_proved_here={uniform} "
        "shell11_executed_here={shell11}".format(
            status=payload["status"],
            work_log=payload["work_log"],
            obstruction=payload.get("proof_status", {}).get(
                "one_family_positive_square_obstruction_proved_here"
            ),
            uniform=payload.get("proof_status", {}).get(
                "uniform_cover_family_obstruction_proved_here"
            ),
            shell11=payload["shell11_executed_here"],
        )
    )
    if args.strict and payload["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
