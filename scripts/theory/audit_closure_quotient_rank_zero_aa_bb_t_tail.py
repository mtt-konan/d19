#!/usr/bin/env python3
"""Audit the ell | T, ell == 1 mod 4 tail in the AA+BB pseudo-container."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only the odd T-prime valuation tail in the AA+BB complete "
    "2-descent pseudo-Selmer container S~. It proves no full Sel_2(E) upper "
    "bound, rank zero, Sha[2]=0, or family exclusion."
)

LOCAL_VALUATION_LEDGER = {
    "prime_scope": "odd primes ell | T with ell == 1 mod 4",
    "coordinate_order": [
        "x_minus_p",
        "x_pos_2sqrt_q",
        "x_neg_2sqrt_q",
    ],
    "known_support_rows": [
        {
            "source": "wl458",
            "coordinate": "x_minus_p",
            "valuation_mod_2": 0,
            "reason": "AA+BB minus-p odd-prime support is killed",
        },
        {
            "source": "wl459",
            "coordinate": "x_pos_2sqrt_q",
            "valuation_mod_2": "candidate_tail_bit",
            "reason": "only this coordinate had possible ell | T, ell == 1 mod 4 support",
        },
        {
            "source": "wl457",
            "coordinate": "x_neg_2sqrt_q",
            "valuation_mod_2": 0,
            "reason": "AA+BB neg-2sqrt-q odd-prime support is killed",
        },
    ],
    "product_relation": "x_minus_p*x_pos_2sqrt_q*x_neg_2sqrt_q=1 in Q*/Q*2",
    "parity_equation": "0 + tail_bit + 0 = 0 in F2",
    "tail_bit": 0,
}

T_TAIL = {
    "status": "killed",
    "tail_dimension": 0,
    "surviving_classes_mod_torsion": [],
    "reason": (
        "At each odd prime ell | T with ell == 1 mod 4, the AA+BB support "
        "ledger leaves a possible odd valuation in only x_pos_2sqrt_q. The "
        "product relation forces the sum of the three valuation parities to be "
        "zero, so that single remaining tail bit must vanish."
    ),
}

DIMENSION_BOUND_UPDATE = {
    "old_tail_terms": ["omega_{1 mod 4}(T)"],
    "new_tail_terms": [],
    "torsion_baseline_dimension": 2,
    "upper_bound": "dim_F2 S~ <= 2",
    "pseudo_selmer_container_forces_torsion_baseline": True,
    "complete_selmer_bound_proved": False,
    "why_not_complete_selmer_bound": (
        "This is a cheap AA+BB pseudo-container valuation ledger, not the full "
        "complete C_d local-solubility matrix for a single curve."
    ),
}


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


def audit_rank_zero_aa_bb_t_tail(*, sign_tail_audit: dict[str, Any]) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(sign_tail_audit):
        violations.append("sign_tail_audit_not_ready")
    if sign_tail_audit.get("sign_tail", {}).get("epsilon_sign") != 0:
        violations.append("archimedean_sign_tail_not_killed")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl466",
        "pattern": "AA+BB",
        "local_valuation_ledger": LOCAL_VALUATION_LEDGER,
        "t_tail": T_TAIL,
        "dimension_bound_update": DIMENSION_BOUND_UPDATE,
        "route_decision": {
            "decision": "T_tail_killed_in_pseudo_container",
            "requires_joint_C_d_local_conditions_for_this_tail": False,
            "next_action": "stop_after_T_tail_audit",
            "stop_condition_observed": (
                "The only remaining symbolic T-prime tail in S~ has zero dimension "
                "by the product-relation valuation ledger."
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
    parser.add_argument("--sign-tail-audit", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_t_tail(sign_tail_audit=load_json(args.sign_tail_audit))
    write_json(args.out, audit)
    print(f"wrote AA+BB T-tail audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"t_tail_status={audit['t_tail']['status']}")
    print(f"t_tail_dimension={audit['t_tail']['tail_dimension']}")
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
