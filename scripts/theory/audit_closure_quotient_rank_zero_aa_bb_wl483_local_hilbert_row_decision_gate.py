#!/usr/bin/env python3
"""Decide whether a justified local/Hilbert row kills the wl482 u_3 tail."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl483 / local_Hilbert_row_decision_gate for the AA+BB "
    "complete d-coordinate route. It takes wl482 as input and decides only "
    "whether the currently defined complete C_d local-solubility framework "
    "provides a mathematically justified additional local/Hilbert character "
    "row at infinity, 2, 3, or 13 that kills the AA A=3, B=1 u_3 tail "
    "candidate. It does not run broad rank or Selmer diagnostics, does not "
    "prove an obstruction, does not prove a complete Sel_2(E) upper bound, "
    "does not claim dim Sel_2(E)=2, rank zero, Sha[2]=0, or any family "
    "exclusion."
)

TARGET_SUPPORT = ["u_3"]
FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl482_ready(wl482: dict[str, Any]) -> bool:
    return (
        wl482.get("status") == "ok"
        and wl482.get("ready") is True
        and wl482.get("lemma_id") == "WL482_M_tail_kernel_classification_gate"
        and wl482.get("work_log") == "wl482"
        and wl482.get("input_work_log") == "wl481"
        and wl482.get("target_kernel", {}).get("support") == TARGET_SUPPORT
        and wl482.get("classification", {}).get("final_classification")
        == "genuine_parameter_specialized_tail_obstruction_candidate"
        and wl482.get("classification", {}).get("missing_known_local_or_hilbert_row")
        is False
        and wl482.get("old_package_x_coordinate_collapse_used") is False
        and not _claims_forbidden_bound(wl482)
    )


def _place_decision_checks() -> list[dict[str, Any]]:
    no_new_lemma = (
        "No source lemma in the current complete C_d local-solubility ledger "
        "justifies adding an independent row here."
    )
    return [
        {
            "place": "infinity",
            "current_framework_status": (
                "real sign row already quotiented as tau_minus; u_3 has positive "
                "real support"
            ),
            "already_accounted_row": "real_sign_tau_minus",
            "candidate_new_row": None,
            "source_lemma_obligation": (
                "A new real C_d local-solubility character independent of the "
                "tau_minus visible torsion quotient with nonzero u_3 entry."
            ),
            "source_lemma_satisfied": False,
            "row_available": False,
            "kills_u_3": False,
            "reason": no_new_lemma,
        },
        {
            "place": "2",
            "current_framework_status": (
                "ordinary wl478 Q_2 row already instantiated and has zero u_3 entry"
            ),
            "already_accounted_row": "dyadic_ordinary_d_neg_2sqrt_q_sign_character",
            "candidate_new_row": None,
            "source_lemma_obligation": (
                "A strengthened wl478-style Q_2 squareclass or Hilbert row in "
                "the ordinary v2(sqrt_q) even stratum with nonzero u_3 entry."
            ),
            "source_lemma_satisfied": False,
            "row_available": False,
            "kills_u_3": False,
            "reason": no_new_lemma,
        },
        {
            "place": "3",
            "current_framework_status": (
                "wl475 odd L row at 3 already instantiated and has zero u_3 entry"
            ),
            "already_accounted_row": "odd_L_3_equal_d_minus_p_d_pos_2sqrt_q",
            "candidate_new_row": None,
            "source_lemma_obligation": (
                "An odd-prime local/Hilbert row at the active L-prime 3 beyond "
                "the wl475 equality row, well-defined for C_d and nonzero on u_3."
            ),
            "source_lemma_satisfied": False,
            "row_available": False,
            "kills_u_3": False,
            "reason": no_new_lemma,
        },
        {
            "place": "13",
            "current_framework_status": (
                "wl477 odd sqrt_q row at 13 already instantiated and has zero "
                "u_3 entry"
            ),
            "already_accounted_row": "odd_sqrt_q_13_equal_d_pos_2sqrt_q_d_neg_2sqrt_q",
            "candidate_new_row": None,
            "source_lemma_obligation": (
                "An odd-prime local/Hilbert row at the sqrt_q-prime 13 beyond "
                "the wl477 equality row, well-defined for C_d and nonzero on u_3."
            ),
            "source_lemma_satisfied": False,
            "row_available": False,
            "kills_u_3": False,
            "reason": no_new_lemma,
        },
    ]


def build_wl483_local_hilbert_row_decision_gate(
    *, wl482: dict[str, Any]
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl482_ready(wl482):
        violations.append("wl482_input_not_ready_or_not_scoped")

    target_kernel = wl482.get("target_kernel", {})
    place_checks = _place_decision_checks()
    row_available = any(check["row_available"] and check["kills_u_3"] for check in place_checks)
    status = "ok" if not violations else "issues"

    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl482 u_3 tail candidate and wl475-wl478/wl481 row ledger",
        "pattern": "AA+BB",
        "lemma_id": "WL483_local_Hilbert_row_decision_gate",
        "work_log": "wl483",
        "input_work_log": "wl482",
        "target_kernel": target_kernel,
        "relevant_places": ["infinity", "2", "3", "13"],
        "place_decision_checks": place_checks,
        "new_row_source_lemma_obligation": {
            "required_if_yes": (
                "A complete C_d local-solubility lemma at one of infinity, 2, 3, "
                "or 13 giving a well-defined Hilbert/character row whose u_3 entry "
                "is 1 and whose row is not already part of wl475-wl478/wl481."
            ),
            "satisfied_now": row_available,
            "satisfied_by": None,
        },
        "decision": {
            "decision": (
                "additional_local_hilbert_character_row_available"
                if row_available
                else "no_justified_additional_local_hilbert_character_row_available"
            ),
            "additional_local_hilbert_row_available": row_available,
            "row_that_kills_u_3": None,
            "source_lemma_obligation_satisfied": row_available,
            "route_must_pivot_to_obstruction_handling": not row_available,
            "reason": (
                "The current complete C_d row contract has already accounted for "
                "the real sign quotient, the wl478 ordinary dyadic row, the wl475 "
                "odd L row at 3, and the wl477 odd sqrt_q row at 13. Each has zero "
                "u_3 entry or is already quotiented, and no solved lemma supplies "
                "an additional independent row at these places."
            ),
        },
        "wl481_wl482_change": {
            "wl481_matrix_changed": False,
            "wl482_classification_changed": False,
            "reason": "No new justified row was found, so wl481 and wl482 remain unchanged.",
        },
        "obstruction_pivot": {
            "next_route_status": "pivot_to_obstruction_handling",
            "examples_not_proved_here": [
                "explicit C_d cover local/global solubility for the u_3 class",
                "Cassels-Tate pairing or second descent",
                "L-value or analytic-rank evidence",
            ],
            "obstruction_proved_here": False,
        },
        "symbolic_rank_status": "uniform_full_rank_not_proved",
        "computed_rank_status": "finite_sample_kernel_decision_only",
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
        "old_package_x_coordinate_collapse_used": False,
        "search_count_used_as_progress": False,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl482", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl483_local_hilbert_row_decision_gate(wl482=load_json(args.wl482))
    write_json(args.out, audit)
    print(f"wrote AA+BB wl483 local/Hilbert row decision audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"decision={audit['decision']['decision']}")
    print(
        "complete_selmer_upper_bound_proved="
        f"{audit['complete_selmer_upper_bound_proved']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
