#!/usr/bin/env python3
"""Audit the exact mod-7 local obstruction inside wl535."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl535_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl535_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction"
    )
    from json_io import write_json


BOUNDARY = (
    "This proves one direct local obstruction inside the exact wl535 "
    "q-root-coordinate square/quartic proposition: if ell is an odd prime with "
    "ell ≡ 5 mod 7, then the wl535 rational system has no solution. It removes "
    "that residue class from the remaining pure-v_ell M2 search. It does not "
    "solve the complementary residue classes, does not produce a counterexample, "
    "and does not enter M3."
)


def _wl535_ready(wl535: dict[str, Any]) -> bool:
    proof = wl535.get("proof_status", {})
    return (
        wl535.get("status") == "ok"
        and wl535.get("ready") is True
        and wl535.get("work_log") == "wl535"
        and wl535.get("object_layer")
        == "m2_q_root_coordinate_square_quartic_obstruction_after_wl534"
        and proof.get("wl534_reduced_to_q_root_coordinate_exact_obstruction_here")
        is True
        and proof.get("representation_choice_and_chart_removed_from_statement_here")
        is True
        and proof.get("remaining_problem_is_direct_q_root_square_quartic_obstruction")
        is True
        and proof.get("uniform_infinite_subfamily_exclusion_proved_here") is False
        and proof.get("strict_counterexample_found_here") is False
        and wl535.get("advance_to_m3") is False
    )


def _square_residues_mod_7() -> list[int]:
    return sorted({(x * x) % 7 for x in range(7)})


def _g_mod_7_for_ell_5(q_square_mod_7: int) -> int:
    q = q_square_mod_7 % 7
    return (q**4 + 4 * q**3 + 5 * q + 2) % 7


def _local_obstruction_data() -> dict[str, Any]:
    square_residues = _square_residues_mod_7()
    entries: list[dict[str, Any]] = []

    for q_square_mod_7 in square_residues:
        ell_minus_q_square = (5 - q_square_mod_7) % 7
        ell_q_square_plus_4 = (5 * q_square_mod_7 + 4) % 7
        g_value = _g_mod_7_for_ell_5(q_square_mod_7)

        failure_reasons: list[str] = []
        if ell_minus_q_square not in square_residues:
            failure_reasons.append("ell-q^2 is a nonsquare mod 7")
        if ell_q_square_plus_4 not in square_residues:
            failure_reasons.append("ell*q^2+4 is a nonsquare mod 7")
        if g_value not in square_residues:
            failure_reasons.append("G_ell(q^2) is a nonsquare mod 7")

        entries.append(
            {
                "q_square_mod_7": q_square_mod_7,
                "ell_minus_q_square_mod_7": ell_minus_q_square,
                "ell_minus_q_square_is_square_mod_7": ell_minus_q_square
                in square_residues,
                "ell_q_square_plus_4_mod_7": ell_q_square_plus_4,
                "ell_q_square_plus_4_is_square_mod_7": ell_q_square_plus_4
                in square_residues,
                "G_ell_q_square_mod_7": g_value,
                "G_ell_q_square_is_square_mod_7": g_value in square_residues,
                "survives_all_mod_7_square_conditions": not failure_reasons,
                "failure_reasons": failure_reasons,
            }
        )

    survivors = [
        entry["q_square_mod_7"]
        for entry in entries
        if entry["survives_all_mod_7_square_conditions"] is True
    ]

    return {
        "local_prime": 7,
        "target_ell_residue_mod_7": 5,
        "square_residues_mod_7": square_residues,
        "g_ell_mod_7_specialization": "G_ell(Q) ≡ Q^4 + 4*Q^3 + 5*Q + 2 (mod 7)",
        "integrality_lemma": {
            "statement": (
                "If 7 does not divide ell and p^2+q^2=ell with p,q rational, then p and "
                "q are 7-adic integers."
            ),
            "proof_outline": [
                (
                    "Write p=P/D and q=Q/D in lowest terms, so P^2+Q^2 = ell*D^2 with "
                    "gcd(P,Q,D)=1."
                ),
                (
                    "If 7 divides D, then P^2+Q^2 ≡ 0 (mod 7). Because -1 is a nonsquare "
                    "mod 7, this forces P ≡ Q ≡ 0 (mod 7)."
                ),
                "That contradicts gcd(P,Q,D)=1, so 7 does not divide D.",
                (
                    "Then q^2, ell-q^2, ell*q^2+4, and G_ell(q^2) all reduce mod 7 as "
                    "honest square classes."
                ),
            ],
            "minus_one_is_nonsquare_mod_7": True,
        },
        "q_square_residue_cases": entries,
        "surviving_q_square_residues_mod_7": survivors,
        "obstruction_proved": survivors == [],
    }


def build_wl536_m2_pure_v_ell_mod_7_local_obstruction() -> dict[str, Any]:
    wl535 = wl535_module.build_wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction()
    obstruction = _local_obstruction_data()

    violations: list[str] = []
    if not _wl535_ready(wl535):
        violations.append("wl535_input_not_ready")
    if obstruction["obstruction_proved"] is not True:
        violations.append("mod_7_local_obstruction_not_complete")

    status = "ok" if not violations else "issues"
    ready = status == "ok"
    proof_status = (
        {
            "wl535_residue_class_ell_eq_5_mod_7_excluded_here": True,
            "local_prime_7_integrality_obstruction_proved_here": True,
            "remaining_problem_shrunk_to_complementary_prime_classes": True,
            "uniform_full_wl535_obstruction_proved_here": False,
            "strict_counterexample_found_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )

    return {
        "status": status,
        "ready": ready,
        "work_log": "wl536",
        "object_layer": "m2_q_root_coordinate_mod_7_local_obstruction_inside_wl535",
        "family_scope": {
            "support": "v_ell",
            "L": 1,
            "T": "ell",
            "d_vector": {
                "d_minus_p": "ell",
                "d_pos_2sqrt_q": 1,
                "d_neg_2sqrt_q": "ell",
            },
            "parameter_restrictions": [
                "ell is an odd prime with ell ≡ 1 mod 4",
                "ell ≡ 5 mod 7",
                "q is rational",
                "ell-q^2 is a rational square",
                "ell*q^2+4 is a rational square",
                "ell*q^4+4*q^2-4*ell is positive",
                (
                    "V^2 = q^8 + (16-8*ell)q^6 + (32*ell^2-96*ell+72)q^4 "
                    "+ (32*ell-64)q^2 + 16"
                ),
            ],
            "touches_only_M2_for_the_wl535_pure_family": True,
        },
        "input_checkpoint": {
            "work_log": "wl535",
            "ready": _wl535_ready(wl535),
            "handoff": "wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction_stop",
        },
        "local_obstruction": {
            "statement": (
                "If ell is an odd prime with ell ≡ 1 mod 4 and ell ≡ 5 mod 7, then the "
                "exact wl535 rational system has no solution."
            ),
            "why_the_reduction_is_valid": [
                (
                    "Because 7 ≡ 3 mod 4, -1 is a nonsquare mod 7. So any rational "
                    "solution of p^2+q^2=ell with 7 not dividing ell is automatically "
                    "7-adically integral in p and q."
                ),
                (
                    "Then ell-q^2, ell*q^2+4, and G_ell(q^2) must all reduce to square "
                    "classes mod 7."
                ),
                (
                    "For ell ≡ 5 mod 7, every possible residue q^2 mod 7 is eliminated "
                    "by one of those square tests."
                ),
            ],
            "mod_7_case_table": obstruction,
            "remaining_prime_classes_mod_28": [1, 9, 13, 17, 25],
            "removed_prime_class_mod_28": 5,
            "infinite_prime_subfamily_reason": (
                "gcd(5,28)=1, so Dirichlet's theorem gives infinitely many primes "
                "ell congruent to 5 mod 28."
            ),
        },
        "proof_status": proof_status,
        "violations": violations,
        "boundary": BOUNDARY,
        "uniform_infinite_subfamily_exclusion_proved_here": False,
        "strict_counterexample_found_here": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "advance_to_m3": False,
        "stop_after_current_task": True,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(
            "results/closure_quotient_rank_zero_aa_bb_wl536_m2_pure_v_ell_mod_7_local_obstruction.json"
        ),
        help="Output path for the wl536 mod-7 local-obstruction audit JSON.",
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_wl536_m2_pure_v_ell_mod_7_local_obstruction()
    write_json(args.out, payload)
    print(f"wrote wl536 mod-7 local-obstruction audit to {args.out}")
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    if args.strict and payload["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
