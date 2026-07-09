#!/usr/bin/env python3
"""Audit H2: complete d-coordinates versus three package x-coordinates."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only H2_coordinate_equivalence for the AA+BB complete "
    "2-descent route. It does not build the full C_d local matrix, does not "
    "enter H3/H4, and proves no complete Sel_2(E) upper bound, rank zero, "
    "Sha[2]=0, or family exclusion."
)

H2_VERDICT = {
    "id": "H2_coordinate_equivalence",
    "status": "refuted",
    "coordinate_equivalence_proved": False,
    "coordinate_equivalence_refuted": True,
    "reason": (
        "On the complete-descent product-relation plane, each package "
        "x-coordinate is the same product d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q, "
        "hence the trivial squareclass. The package x-triple is therefore "
        "not an injective coordinate system for complete d-data."
    ),
}

PACKAGE_COORDINATE_ROWS = {
    "x_minus_p": [1, 1, 1],
    "x_pos_2sqrt_q": [1, 1, 1],
    "x_neg_2sqrt_q": [1, 1, 1],
}

RELATION_PLANE_BASIS = [
    [1, 1, 0],
    [1, 0, 1],
]

SQUARECLASS_LINEAR_ALGEBRA = {
    "ambient_group": "V = Q*/Q*2, written additively over F2",
    "complete_d_relation": "d_minus_p + d_pos_2sqrt_q + d_neg_2sqrt_q = 0",
    "package_coordinate_rows": PACKAGE_COORDINATE_ROWS,
    "rank_on_complete_relation_plane": 0,
    "kernel_dimension_on_complete_relation_plane": 2,
    "injective_on_complete_d_data": False,
    "equivalent_squareclass_data": False,
    "image_on_complete_relation_plane": ["1", "1", "1"],
}

NORMAL_POINT_AUDIT = {
    "complete_coordinates": [
        "d_minus_p = X+p",
        "d_pos_2sqrt_q = X-2*sqrt_q",
        "d_neg_2sqrt_q = X+2*sqrt_q",
    ],
    "product_relation": "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q = Y^2 = 1 in Q*/Q*2",
    "package_translation": {
        "x_minus_p": (
            "d_pos_2sqrt_q*d_neg_2sqrt_q/d_minus_p = "
            "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q"
        ),
        "x_pos_2sqrt_q": (
            "d_minus_p*d_neg_2sqrt_q/d_pos_2sqrt_q = "
            "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q"
        ),
        "x_neg_2sqrt_q": (
            "d_minus_p*d_pos_2sqrt_q/d_neg_2sqrt_q = "
            "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q"
        ),
    },
    "package_x_image_for_every_nonroot_complete_d_tuple": ["1", "1", "1"],
    "normal_points_rescue_equivalence": False,
}

TORSION_REPRESENTATIVE_ORDER = [
    "O",
    "T_minus_p",
    "T_pos_2sqrt_q",
    "T_neg_2sqrt_q",
]

COUNTEREXAMPLE_SCHEMA = {
    "not_a_selmer_existence_claim": True,
    "two_distinct_complete_d_classes": [
        ["1", "1", "1"],
        ["alpha", "beta", "alpha*beta"],
    ],
    "same_package_x_image": ["1", "1", "1"],
    "why_sufficient_for_H2": (
        "H2 asks for coordinate equivalence, including torsion and root representatives; "
        "the transformation loses the two-dimensional complete d-plane before any C_d "
        "local-solubility matrix is built."
    ),
}


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


def _has_h2_hypothesis(theorem_bridge: dict[str, Any]) -> bool:
    return any(
        item.get("id") == "H2_coordinate_equivalence"
        for item in theorem_bridge.get("required_hypotheses", [])
    )


def _has_complete_product_relation(complete_two_descent_recast: dict[str, Any]) -> bool:
    relation = str(
        complete_two_descent_recast.get("complete_two_descent_coordinates", {}).get(
            "ambient_relation", ""
        )
    )
    return (
        "d_minus_p * d_pos_2sqrt_q * d_neg_2sqrt_q" in relation
        and "Q*/Q*2" in relation
    )


def _has_package_coordinate_translation(complete_two_descent_recast: dict[str, Any]) -> bool:
    relation = complete_two_descent_recast.get("isogeny_to_complete_coordinate_relation", {})
    return all(name in relation for name in PACKAGE_COORDINATE_ROWS)


def _torsion_and_exceptional_roots(
    complete_two_descent_recast: dict[str, Any],
) -> dict[str, Any]:
    torsion_images = complete_two_descent_recast.get("torsion_kummer_images", {})
    representatives = [
        name for name in TORSION_REPRESENTATIVE_ORDER if name in torsion_images
    ]
    return {
        "standard_rule": (
            "At X=e_i, replace the vanishing d_i coordinate by the product of "
            "the two nonzero root differences."
        ),
        "torsion_representatives_checked": representatives,
        "package_x_image_for_each_torsion_representative": {
            name: ["1", "1", "1"] for name in representatives
        },
        "exceptional_root_cases_rescue_equivalence": False,
        "torsion_baseline_preserved_by_package_x_coordinates": False,
    }


def _rank_rows_over_relation_plane() -> int:
    row_images = []
    for row in PACKAGE_COORDINATE_ROWS.values():
        row_images.append(
            tuple(
                sum(a * b for a, b in zip(row, basis, strict=True)) % 2
                for basis in RELATION_PLANE_BASIS
            )
        )
    nonzero_rows = {image for image in row_images if image != (0, 0)}
    return len(nonzero_rows)


def audit_rank_zero_aa_bb_h2_coordinate_equivalence(
    *,
    complete_two_descent_recast: dict[str, Any],
    theorem_bridge: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(complete_two_descent_recast):
        violations.append("complete_two_descent_recast_not_ready")
    if not _ready(theorem_bridge):
        violations.append("theorem_bridge_not_ready")
    if not _has_h2_hypothesis(theorem_bridge):
        violations.append("bridge_h2_hypothesis_missing")
    if not _has_complete_product_relation(complete_two_descent_recast):
        violations.append("complete_product_relation_missing")
    if not _has_package_coordinate_translation(complete_two_descent_recast):
        violations.append("package_coordinate_translation_missing")

    linear_algebra = dict(SQUARECLASS_LINEAR_ALGEBRA)
    linear_algebra["rank_on_complete_relation_plane"] = _rank_rows_over_relation_plane()
    linear_algebra["kernel_dimension_on_complete_relation_plane"] = (
        len(RELATION_PLANE_BASIS) - linear_algebra["rank_on_complete_relation_plane"]
    )

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl464-wl468",
        "pattern": "AA+BB",
        "h2_verdict": H2_VERDICT,
        "squareclass_linear_algebra": linear_algebra,
        "normal_point_audit": NORMAL_POINT_AUDIT,
        "torsion_and_exceptional_roots": _torsion_and_exceptional_roots(
            complete_two_descent_recast
        ),
        "counterexample_schema": COUNTEREXAMPLE_SCHEMA,
        "h3_uniform_local_containment_entered": False,
        "h4_mixed_rows_upgrade_entered": False,
        "full_c_d_matrix_built": False,
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "search_count_used_as_progress": False,
        "do_not_proceed_to": ["H3_uniform_local_containment", "H4_mixed_rows_upgrade"],
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--complete-two-descent-recast", type=Path, required=True)
    parser.add_argument("--theorem-bridge", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_h2_coordinate_equivalence(
        complete_two_descent_recast=load_json(args.complete_two_descent_recast),
        theorem_bridge=load_json(args.theorem_bridge),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB H2 coordinate-equivalence audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"h2_status={audit['h2_verdict']['status']}")
    print(
        "coordinate_equivalence_proved="
        f"{audit['h2_verdict']['coordinate_equivalence_proved']}"
    )
    print(
        "complete_selmer_upper_bound_proved="
        f"{audit['complete_selmer_upper_bound_proved']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
