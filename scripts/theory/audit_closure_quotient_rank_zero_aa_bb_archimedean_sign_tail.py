#!/usr/bin/env python3
"""Audit the real-place sign tail in the AA+BB pseudo-Selmer container."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only the archimedean sign row for the AA+BB complete "
    "2-descent pseudo-Selmer container. It proves no Selmer rank upper bound, "
    "rank zero, Sha[2]=0, or family exclusion."
)

ROOT_ORDER_AUDIT = {
    "parameters": {
        "T": "A+B",
        "L": "A on AA side, B on BB side",
        "p": "8*L^2 - 2*T^2",
        "sqrt_q": "T^2 + 4*L^2",
    },
    "ordered_roots": [
        "e_neg=-2*sqrt_q",
        "e_minus=-p",
        "e_pos=2*sqrt_q",
    ],
    "strict_inequality_proof": [
        "e_minus - e_neg = 4*T^2 > 0",
        "e_pos - e_minus = 16*L^2 > 0",
    ],
}

REAL_SIGN_IMAGE = {
    "coordinate_order": ["d_minus_p", "d_pos_2sqrt_q", "d_neg_2sqrt_q"],
    "product_relation_sign_classes": [
        ["+", "+", "+"],
        ["+", "-", "-"],
        ["-", "+", "-"],
        ["-", "-", "+"],
    ],
    "real_interval_sign_classes": [
        {
            "real_interval": "X > e_pos",
            "sign_class": ["+", "+", "+"],
        },
        {
            "real_interval": "e_neg < X < e_minus",
            "sign_class": ["-", "-", "+"],
        },
    ],
    "forbidden_by_real_place": [
        ["+", "-", "-"],
        ["-", "+", "-"],
    ],
    "surviving_nontrivial_sign_class": ["-", "-", "+"],
}

TORSION_SIGN_IMAGE = {
    "O": ["+", "+", "+"],
    "T_minus_p": ["-", "-", "+"],
    "T_pos_2sqrt_q": ["+", "+", "+"],
    "T_neg_2sqrt_q": ["-", "-", "+"],
    "distinct_torsion_sign_classes": [
        ["+", "+", "+"],
        ["-", "-", "+"],
    ],
}

SIGN_TAIL = {
    "epsilon_sign": 0,
    "surviving_sign_classes": [
        ["+", "+", "+"],
        ["-", "-", "+"],
    ],
    "exact_surviving_nontrivial_class": {
        "sign_class": ["-", "-", "+"],
        "meaning": "d_minus_p<0, d_pos_2sqrt_q<0, d_neg_2sqrt_q>0",
        "already_torsion": True,
        "torsion_representatives": ["T_minus_p", "T_neg_2sqrt_q"],
    },
    "reason": (
        "The real local image has one nontrivial sign class, but that "
        "class is already the sign image of rational 2-torsion, so it "
        "does not add a pseudo-Selmer tail beyond the torsion baseline."
    ),
}

DIMENSION_BOUND_UPDATE = {
    "old_tail_terms": ["omega_{1 mod 4}(T)", "epsilon_sign"],
    "new_tail_terms": ["omega_{1 mod 4}(T)"],
    "epsilon_sign_values": [0],
    "upper_bound": "dim_F2 S~ <= 2 + omega_{1 mod 4}(T)",
    "forces_dim_2": False,
    "why_not_forced_dim_2": "The T-prime tail remains unresolved.",
}


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


def audit_rank_zero_aa_bb_archimedean_sign_tail(
    *,
    pseudo_selmer_container: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(pseudo_selmer_container):
        violations.append("pseudo_selmer_container_not_ready")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl465",
        "pattern": "AA+BB",
        "root_order_audit": ROOT_ORDER_AUDIT,
        "real_sign_image": REAL_SIGN_IMAGE,
        "torsion_sign_image": TORSION_SIGN_IMAGE,
        "sign_tail": SIGN_TAIL,
        "dimension_bound_update": DIMENSION_BOUND_UPDATE,
        "route_decision": {
            "decision": "T_tail_remaining",
            "next_action": "kill or account for the ell | T, ell == 1 mod 4 tail",
            "stop_condition_observed": (
                "This audit stops after the archimedean sign row and does not "
                "build the T-tail or C_d matrix."
            ),
        },
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pseudo-selmer-container", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_archimedean_sign_tail(
        pseudo_selmer_container=load_json(args.pseudo_selmer_container),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB archimedean sign-tail audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"epsilon_sign={audit['sign_tail']['epsilon_sign']}")
    print(f"upper_bound={audit['dimension_bound_update']['upper_bound']}")
    print(
        "selmer_rank_upper_bound_proved_count="
        f"{audit['selmer_rank_upper_bound_proved_count']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
