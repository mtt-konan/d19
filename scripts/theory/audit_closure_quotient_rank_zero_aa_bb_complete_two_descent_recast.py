#!/usr/bin/env python3
"""Recast wl463 as a complete 2-descent audit for the AA+BB target."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This recasts the wl463 point-level two-primary collapse as a complete "
    "2-descent question. It identifies the source curve, Sel_2 squareclass "
    "coordinates, and the next pseudo-Selmer upper-bound audit. It does not "
    "prove a Selmer rank upper bound, rank zero, or any lambda-family exclusion."
)

ROOT_LABELS = ["minus_p", "pos_2sqrt_q", "neg_2sqrt_q"]

FULL_RATIONAL_2_TORSION_MODEL = {
    "parameters": {
        "T": "A+B",
        "L": "one-sided leg, L=A on the AA side and L=B on the BB side",
        "p": "8*L^2 - 2*T^2",
        "sqrt_q": "T^2 + 4*L^2",
    },
    "source_curve": (
        "E_L: Y^2 = (X-(-p))*(X-(2*sqrt_q))*(X-(-2*sqrt_q)) "
        "= (X+p)*(X^2 - 4*q)"
    ),
    "rational_two_torsion_points": [
        "O",
        "T_minus_p=(-p,0)",
        "T_pos_2sqrt_q=(2*sqrt_q,0)",
        "T_neg_2sqrt_q=(-2*sqrt_q,0)",
    ],
    "e2_dimension": 2,
    "kernel_roots": {
        "kernel_minus_p": "-p",
        "kernel_pos_2sqrt_q": "2*sqrt_q",
        "kernel_neg_2sqrt_q": "-2*sqrt_q",
    },
}

COMPLETE_TWO_DESCENT_COORDINATES = {
    "coordinate_names": {
        "d_minus_p": "X-(-p)=X+p",
        "d_pos_2sqrt_q": "X-(2*sqrt_q)",
        "d_neg_2sqrt_q": "X-(-2*sqrt_q)=X+2*sqrt_q",
    },
    "ambient_relation": (
        "d_minus_p * d_pos_2sqrt_q * d_neg_2sqrt_q = 1 "
        "in Q*/Q*2"
    ),
    "selmer_membership_test": [
        "choose squareclasses d_i satisfying the product relation",
        "test local solubility of the corresponding 2-covering C_d at every relevant place",
        "quotient by the standard complete-descent equivalence to obtain Sel_2(E)",
    ],
    "covering_equations": [
        "d_minus_p*u_minus_p^2 = X+p",
        "d_pos_2sqrt_q*u_pos_2sqrt_q^2 = X-2*sqrt_q",
        "d_neg_2sqrt_q*u_neg_2sqrt_q^2 = X+2*sqrt_q",
    ],
    "difference_equations": [
        "d_minus_p*u_minus_p^2 - d_pos_2sqrt_q*u_pos_2sqrt_q^2 = p+2*sqrt_q",
        "d_minus_p*u_minus_p^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = p-2*sqrt_q",
        "d_pos_2sqrt_q*u_pos_2sqrt_q^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = -4*sqrt_q",
    ],
    "rank_bound_formula": (
        "rank E(Q) <= dim_F2 Sel_2(E) - dim_F2 E[2](Q) = dim_F2 Sel_2(E) - 2"
    ),
    "rank_zero_target": "prove dim_F2 Sel_2(E)=2, i.e. only the E[2] Kummer image survives",
}

ISOGENY_TO_COMPLETE_COORDINATE_RELATION = {
    "x_minus_p": "d_pos_2sqrt_q * d_neg_2sqrt_q / d_minus_p",
    "x_pos_2sqrt_q": "d_minus_p * d_neg_2sqrt_q / d_pos_2sqrt_q",
    "x_neg_2sqrt_q": "d_minus_p * d_pos_2sqrt_q / d_neg_2sqrt_q",
    "product": (
        "x_minus_p * x_pos_2sqrt_q * x_neg_2sqrt_q "
        "= d_minus_p * d_pos_2sqrt_q * d_neg_2sqrt_q = 1"
    ),
    "audit_warning": (
        "The wl457-wl463 constraints are stated in these three isogeny target "
        "coordinates. In complete 2-descent the product/common-source relation "
        "is built into Selmer membership, but the cheap next step is the "
        "pseudo-Selmer S~ dimension audit before the full C_d matrix."
    ),
}

TORSION_KUMMER_IMAGES = {
    "O": ["1", "1", "1"],
    "T_minus_p": [
        "(-p-2*sqrt_q)*(-p+2*sqrt_q)",
        "-p-2*sqrt_q",
        "-p+2*sqrt_q",
    ],
    "T_pos_2sqrt_q": [
        "2*sqrt_q+p",
        "(2*sqrt_q+p)*(4*sqrt_q)",
        "4*sqrt_q",
    ],
    "T_neg_2sqrt_q": [
        "-2*sqrt_q+p",
        "-4*sqrt_q",
        "(-2*sqrt_q+p)*(-4*sqrt_q)",
    ],
}

EXISTING_CONSTRAINT_TRANSLATION = {
    "odd_prime_formal_lift_inputs": [
        {
            "kernel": "kernel_minus_p",
            "source": "wl458",
            "isogeny_package_constraint": "no odd-prime valuation support",
            "complete_descent_effect": "not transferred to d_minus_p,d_pos_2sqrt_q,d_neg_2sqrt_q",
        },
        {
            "kernel": "kernel_pos_2sqrt_q",
            "source": "wl459",
            "isogeny_package_constraint": "support only from ell | T with ell == 1 mod 4",
            "complete_descent_effect": "not transferred to a complete 2-cover local condition",
        },
        {
            "kernel": "kernel_neg_2sqrt_q",
            "source": "wl457",
            "isogeny_package_constraint": "no odd-prime valuation support",
            "complete_descent_effect": "not transferred to d_minus_p,d_pos_2sqrt_q,d_neg_2sqrt_q",
        },
    ],
    "dyadic_inputs": [
        {
            "source": "wl460",
            "statement": "opposite-mod-4 branch forces x_minus_p in {1}",
            "complete_descent_effect": (
                "point/local quotient-coordinate fact; not a C_d local solubility row"
            ),
        },
        {
            "source": "wl461",
            "statement": "same-mod-4 branch has local x_minus_p class 2",
            "complete_descent_effect": "shows one-kernel singleton target is false",
        },
        {
            "source": "wl462-wl463",
            "statement": "common-source rational points collapse to (1,1,1)",
            "complete_descent_effect": (
                "compatible with complete descent, but not a Sel_2(E) condition"
            ),
        },
    ],
    "translation_verdict": (
        "The existing constraints constrain point-level or independent "
        "dual-isogeny package coordinates. They do not yet fill the complete "
        "2-descent local matrix for the d_i coordinates."
    ),
}

REMAINING_OBSTRUCTION = {
    "kind": "pseudo-Selmer tail",
    "exact_obstruction": "S_tilde_dimension_not_forced_to_2",
    "why_not_unit_sign_only": (
        "the sign bit is one tail term, but the symbolic T-prime tail at "
        "ell | T, ell == 1 mod 4 also remains"
    ),
    "why_not_sha2_yet": (
        "Sha[2] becomes the primary route only after a proved rank-zero sample "
        "or theorem still has dim Sel_2(E)>2"
    ),
    "why_not_finite_ledger": (
        "the current blocker is a symbolic upper-bound tail, not a need for "
        "more point-level local-class enumeration"
    ),
    "missing_evidence": [
        "prove the archimedean sign tail has dimension 0 or account for it",
        "prove a joint local condition for primes ell | T with ell == 1 mod 4",
        "only if those tails survive, build the full C_d local solubility matrix",
        (
            "linear algebra showing the surviving S~ or Sel_2(E) space is exactly "
            "the E[2] Kummer image"
        ),
    ],
}


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


def _point_level_collapse_ready(two_primary_reduction: dict[str, Any]) -> bool:
    collapse = two_primary_reduction.get("point_level_two_primary_collapse", {})
    return (
        collapse.get("source") == "wl460-wl463"
        and collapse.get("selmer_lift_proved") is False
        and collapse.get("nontrivial_triple_count") == 0
        and collapse.get("remaining_triples")
        == [
            {
                "x_minus_p": "1",
                "x_pos_2sqrt_q": "1",
                "x_neg_2sqrt_q": "1",
            }
        ]
    )


def _product_relation_ready(product_relation: dict[str, Any]) -> bool:
    relation = str(product_relation.get("common_source_relation", ""))
    return (
        _ready(product_relation)
        and "x_minus_p * x_pos_2sqrt_q * x_neg_2sqrt_q" in relation
        and "Y^2" in relation
    )


def audit_rank_zero_aa_bb_complete_two_descent_recast(
    *,
    two_primary_reduction: dict[str, Any],
    product_relation: dict[str, Any],
) -> dict[str, Any]:
    checks = {
        "two_primary_reduction_ready": _ready(two_primary_reduction),
        "point_level_collapse_ready": _point_level_collapse_ready(two_primary_reduction),
        "product_relation_ready": _product_relation_ready(product_relation),
    }
    violations = [name for name, passed in checks.items() if not passed]
    status = "ok" if not violations else "issues"

    completion_audit = [
        {
            "task": "identify_full_rational_2_torsion_model",
            "status": "satisfied_as_recast",
            "evidence": "FULL_RATIONAL_2_TORSION_MODEL",
        },
        {
            "task": "write_complete_2_descent_coordinates_and_product_relation",
            "status": "satisfied_as_recast",
            "evidence": "COMPLETE_TWO_DESCENT_COORDINATES",
        },
        {
            "task": "translate_odd_prime_and_dyadic_constraints",
            "status": "satisfied_as_audit",
            "evidence": "EXISTING_CONSTRAINT_TRANSLATION",
        },
        {
            "task": "audit_whether_constraints_force_dim_sel2_eq_2",
            "status": "not_proved",
            "evidence": "forced_dim_sel2_eq_2=false",
        },
        {
            "task": "report_exact_remaining_obstruction",
            "status": "satisfied_as_audit",
            "evidence": "REMAINING_OBSTRUCTION.kind=pseudo-Selmer tail",
        },
    ]

    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl463",
        "pattern": "AA+BB",
        "full_rational_2_torsion_model": FULL_RATIONAL_2_TORSION_MODEL,
        "complete_two_descent_coordinates": COMPLETE_TWO_DESCENT_COORDINATES,
        "isogeny_to_complete_coordinate_relation": ISOGENY_TO_COMPLETE_COORDINATE_RELATION,
        "torsion_kummer_images": TORSION_KUMMER_IMAGES,
        "existing_constraint_translation": EXISTING_CONSTRAINT_TRANSLATION,
        "point_level_collapse_promoted_to_sel2_bound": False,
        "forced_dim_sel2_eq_2": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "remaining_obstruction": REMAINING_OBSTRUCTION,
        "completion_audit": completion_audit,
        "checks": checks,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--two-primary-reduction", type=Path, required=True)
    parser.add_argument("--product-relation", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_complete_two_descent_recast(
        two_primary_reduction=load_json(args.two_primary_reduction),
        product_relation=load_json(args.product_relation),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB complete 2-descent recast audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"forced_dim_sel2_eq_2={audit['forced_dim_sel2_eq_2']}")
    print(f"remaining_obstruction={audit['remaining_obstruction']['kind']}")
    print(
        "selmer_rank_upper_bound_proved_count="
        f"{audit['selmer_rank_upper_bound_proved_count']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
