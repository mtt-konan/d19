#!/usr/bin/env python3
"""Canonical parameterized local-table engine for wl536-wl538."""

from __future__ import annotations

from typing import Any

# --- wl536 local table ---

WL536_BOUNDARY = (
    "This proves one direct local obstruction inside the exact wl535 "
    "q-root-coordinate square/quartic proposition: if ell is an odd prime with "
    "ell ≡ 5 mod 7, then the wl535 rational system has no solution. It removes "
    "that residue class from the remaining pure-v_ell M2 search. It does not "
    "solve the complementary residue classes, does not produce a counterexample, "
    "and does not enter M3."
)


def _wl535_ready_wl536(wl535: dict[str, Any]) -> bool:
    proof = wl535.get("proof_status", {})
    return (
        wl535.get("status") == "ok"
        and wl535.get("ready") is True
        and wl535.get("work_log") == "wl535"
        and wl535.get("object_layer")
        == "m2_q_root_coordinate_square_quartic_obstruction_after_wl534"
        and proof.get("wl534_reduced_to_q_root_coordinate_exact_obstruction_here") is True
        and proof.get("representation_choice_and_chart_removed_from_statement_here") is True
        and proof.get("remaining_problem_is_direct_q_root_square_quartic_obstruction") is True
        and proof.get("uniform_infinite_subfamily_exclusion_proved_here") is False
        and proof.get("strict_counterexample_found_here") is False
        and wl535.get("advance_to_m3") is False
    )


def _square_residues_mod_7_wl536() -> list[int]:
    return sorted({(x * x) % 7 for x in range(7)})


def _g_mod_7_for_ell_5_wl536(q_square_mod_7: int) -> int:
    q = q_square_mod_7 % 7
    return (q**4 + 4 * q**3 + 5 * q + 2) % 7


def _local_obstruction_data_wl536() -> dict[str, Any]:
    square_residues = _square_residues_mod_7_wl536()
    entries: list[dict[str, Any]] = []

    for q_square_mod_7 in square_residues:
        ell_minus_q_square = (5 - q_square_mod_7) % 7
        ell_q_square_plus_4 = (5 * q_square_mod_7 + 4) % 7
        g_value = _g_mod_7_for_ell_5_wl536(q_square_mod_7)

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
                "ell_minus_q_square_is_square_mod_7": ell_minus_q_square in square_residues,
                "ell_q_square_plus_4_mod_7": ell_q_square_plus_4,
                "ell_q_square_plus_4_is_square_mod_7": ell_q_square_plus_4 in square_residues,
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
                ("Write p=P/D and q=Q/D in lowest terms, so P^2+Q^2 = ell*D^2 with gcd(P,Q,D)=1."),
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


def _build_wl536(wl535: dict[str, Any]) -> dict[str, Any]:
    obstruction = _local_obstruction_data_wl536()

    violations: list[str] = []
    if not _wl535_ready_wl536(wl535):
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
                ("V^2 = q^8 + (16-8*ell)q^6 + (32*ell^2-96*ell+72)q^4 + (32*ell-64)q^2 + 16"),
            ],
            "touches_only_M2_for_the_wl535_pure_family": True,
        },
        "input_checkpoint": {
            "work_log": "wl535",
            "ready": _wl535_ready_wl536(wl535),
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
        "boundary": WL536_BOUNDARY,
        "uniform_infinite_subfamily_exclusion_proved_here": False,
        "strict_counterexample_found_here": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "advance_to_m3": False,
        "stop_after_current_task": True,
    }


# --- wl537 local table ---

WL537_BOUNDARY = (
    "This proves only the direct 11-adic obstruction ell congruent to 10 mod 11 "
    "inside the exact wl535 system, equivalently the infinite prime class ell "
    "congruent to 21 mod 44. It does not solve the complementary classes, prove "
    "a complete Selmer bound, or enter M3."
)


def _wl536_ready_wl537(wl536: dict[str, Any]) -> bool:
    proof = wl536.get("proof_status", {})
    return (
        wl536.get("status") == "ok"
        and wl536.get("ready") is True
        and wl536.get("work_log") == "wl536"
        and proof.get("wl535_residue_class_ell_eq_5_mod_7_excluded_here") is True
        and proof.get("uniform_full_wl535_obstruction_proved_here") is False
        and wl536.get("advance_to_m3") is False
    )


def _square_residues_wl537(modulus: int) -> list[int]:
    return sorted({(x * x) % modulus for x in range(modulus)})


def _g_mod_11_for_ell_10_wl537(q_square: int) -> int:
    r = q_square % 11
    return (r**4 + 2 * r**3 + 2 * r**2 + 3 * r + 5) % 11


def _local_obstruction_data_wl537() -> dict[str, Any]:
    squares = _square_residues_wl537(11)
    entries: list[dict[str, Any]] = []
    for r in squares:
        ell_minus = (10 - r) % 11
        ell_q_plus_4 = (10 * r + 4) % 11
        g_value = _g_mod_11_for_ell_10_wl537(r)
        failures: list[str] = []
        if ell_minus not in squares:
            failures.append("ell-q^2 is a nonsquare mod 11")
        if ell_q_plus_4 not in squares:
            failures.append("ell*q^2+4 is a nonsquare mod 11")
        if g_value not in squares:
            failures.append("G_ell(q^2) is a nonsquare mod 11")
        entries.append(
            {
                "q_square_mod_11": r,
                "ell_minus_q_square_mod_11": ell_minus,
                "ell_q_square_plus_4_mod_11": ell_q_plus_4,
                "G_ell_q_square_mod_11": g_value,
                "failure_reasons": failures,
                "survives_all_mod_11_square_conditions": not failures,
            }
        )
    survivors = [
        entry["q_square_mod_11"]
        for entry in entries
        if entry["survives_all_mod_11_square_conditions"]
    ]
    return {
        "local_prime": 11,
        "target_ell_residue_mod_11": 10,
        "square_residues_mod_11": squares,
        "g_ell_mod_11_specialization": ("G_ell(Q) ≡ Q^4 + 2*Q^3 + 2*Q^2 + 3*Q + 5 (mod 11)"),
        "integrality_lemma": {
            "minus_one_is_nonsquare_mod_11": True,
            "statement": (
                "If 11 does not divide ell and p^2+q^2=ell with p,q rational, "
                "then p and q are 11-adic integers."
            ),
        },
        "q_square_residue_cases": entries,
        "surviving_q_square_residues_mod_11": survivors,
        "obstruction_proved": survivors == [],
    }


def _build_wl537(wl536: dict[str, Any]) -> dict[str, Any]:
    local = _local_obstruction_data_wl537()
    violations: list[str] = []
    if not _wl536_ready_wl537(wl536):
        violations.append("wl536_input_not_ready")
    if local["obstruction_proved"] is not True:
        violations.append("mod_11_local_obstruction_not_complete")
    ready = not violations
    proof_status = (
        {
            "wl535_residue_class_ell_eq_10_mod_11_excluded_here": True,
            "local_prime_11_integrality_obstruction_proved_here": True,
            "equivalent_prime_class_ell_eq_21_mod_44": True,
            "uniform_full_wl535_obstruction_proved_here": False,
            "strict_counterexample_found_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl537",
        "object_layer": "m2_q_root_coordinate_mod_11_local_obstruction_inside_wl535",
        "input_checkpoint": {"work_log": "wl536", "ready": _wl536_ready_wl537(wl536)},
        "local_obstruction": {
            "statement": (
                "If ell is an odd prime with ell ≡ 1 mod 4 and ell ≡ 10 mod 11, "
                "then the exact wl535 rational system has no solution."
            ),
            "mod_11_case_table": local,
            "removed_prime_class_mod_44": 21,
            "infinite_prime_subfamily_reason": (
                "gcd(21,44)=1, so Dirichlet's theorem gives infinitely many primes "
                "ell congruent to 21 mod 44."
            ),
        },
        "proof_status": proof_status,
        "violations": violations,
        "boundary": WL537_BOUNDARY,
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "advance_to_m3": False,
        "stop_after_current_task": True,
    }


# --- wl538 local table ---


def _wl537_ready_wl538(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl537"
        and proof.get("local_prime_11_integrality_obstruction_proved_here") is True
        and proof.get("uniform_full_wl535_obstruction_proved_here") is False
        and payload.get("advance_to_m3") is False
    )


def _square_residues_wl538(modulus: int) -> list[int]:
    return sorted({x * x % modulus for x in range(modulus)})


def _g_mod_19_for_ell_15_wl538(r: int) -> int:
    return (r**4 + 10 * r**3 + 18 * r**2 + 17 * r + 16) % 19


def _local_obstruction_data_wl538() -> dict[str, Any]:
    squares = _square_residues_wl538(19)
    cases: list[dict[str, Any]] = []
    for r in squares:
        values = ((15 - r) % 19, (15 * r + 4) % 19, _g_mod_19_for_ell_15_wl538(r))
        labels = (
            "ell-q^2 is a nonsquare mod 19",
            "ell*q^2+4 is a nonsquare mod 19",
            "G_ell(q^2) is a nonsquare mod 19",
        )
        failures = [
            label for value, label in zip(values, labels, strict=True) if value not in squares
        ]
        cases.append(
            {
                "q_square_mod_19": r,
                "ell_minus_q_square_mod_19": values[0],
                "ell_q_square_plus_4_mod_19": values[1],
                "G_ell_q_square_mod_19": values[2],
                "failure_reasons": failures,
                "survives_all_mod_19_square_conditions": not failures,
            }
        )
    survivors = [
        case["q_square_mod_19"] for case in cases if case["survives_all_mod_19_square_conditions"]
    ]
    return {
        "local_prime": 19,
        "target_ell_residue_mod_19": 15,
        "square_residues_mod_19": squares,
        "g_ell_mod_19_specialization": ("G_ell(Q) ≡ Q^4 + 10*Q^3 + 18*Q^2 + 17*Q + 16 (mod 19)"),
        "minus_one_is_nonsquare_mod_19": True,
        "q_square_residue_cases": cases,
        "surviving_q_square_residues_mod_19": survivors,
        "obstruction_proved": survivors == [],
    }


def _build_wl538(wl537: dict[str, Any]) -> dict[str, Any]:
    local = _local_obstruction_data_wl538()
    violations: list[str] = []
    if not _wl537_ready_wl538(wl537):
        violations.append("wl537_input_not_ready")
    if local["obstruction_proved"] is not True:
        violations.append("mod_19_local_obstruction_not_complete")
    ready = not violations
    proof_status = (
        {
            "wl535_residue_class_ell_eq_15_mod_19_excluded_here": True,
            "local_prime_19_integrality_obstruction_proved_here": True,
            "equivalent_prime_class_ell_eq_53_mod_76": True,
            "uniform_full_wl535_obstruction_proved_here": False,
            "strict_counterexample_found_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl538",
        "object_layer": "m2_q_root_coordinate_mod_19_local_obstruction_inside_wl535",
        "input_checkpoint": {"work_log": "wl537", "ready": _wl537_ready_wl538(wl537)},
        "local_obstruction": {
            "statement": (
                "For odd prime ell congruent to 1 mod 4 and 15 mod 19, the exact "
                "wl535 rational system has no solution."
            ),
            "mod_19_case_table": local,
            "removed_prime_class_mod_76": 53,
            "infinite_prime_subfamily_reason": (
                "gcd(53,76)=1, so Dirichlet's theorem gives infinitely many primes "
                "ell congruent to 53 mod 76."
            ),
        },
        "proof_status": proof_status,
        "violations": violations,
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "advance_to_m3": False,
        "stop_after_current_task": True,
    }


def build_local_stages(wl535: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Compute the three independent local tables with explicit stage inputs."""
    wl536 = _build_wl536(wl535)
    wl537 = _build_wl537(wl536)
    wl538 = _build_wl538(wl537)
    return {"wl536": wl536, "wl537": wl537, "wl538": wl538}
