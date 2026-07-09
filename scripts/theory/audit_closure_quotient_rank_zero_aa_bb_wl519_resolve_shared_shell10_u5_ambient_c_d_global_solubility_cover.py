#!/usr/bin/env python3
"""Resolve the shared shell-10 u_5 ambient C_d global-solubility cover."""

from __future__ import annotations

import argparse
from fractions import Fraction
from pathlib import Path
from typing import Any

try:
    from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl491_ambient_c_d_to_aa_bb_admissibility_filter import (  # noqa: E501
        classify_ambient_c_d_point_for_aa_bb_admissibility,
    )
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from audit_closure_quotient_rank_zero_aa_bb_wl491_ambient_c_d_to_aa_bb_admissibility_filter import (  # noqa: E501
        classify_ambient_c_d_point_for_aa_bb_admissibility,
    )
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl519 / resolve_shared_shell10_u5_ambient_C_d_"
    "global_solubility_cover. It uses wl518 as the immediate route input and "
    "wl491 as the admissibility-filter contract, enters only the shared "
    "shell-10 u_5 cover L=10,T=19,d=(5,5,1), resolves that cover by an exact "
    "rational ambient C_d point, applies wl491 only after ambient global "
    "solubility is established, routes the two mirror entries to globally "
    "soluble but not AA+BB-admissible ledgers, and stops before shell 11, "
    "post-wl519 route choice, proof-level generalization, final candidate "
    "selection, broad rank or Selmer diagnostics, old package-x S~ use, or "
    "claiming a complete Sel_2(E) upper bound, dim Sel_2(E)=2, rank zero, "
    "Sha[2]=0, uniform M_tail full rank, or any family exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

DEFERRED_U5_IDS = [
    "AA_A10_B9_u_5_m_tail_shell10_candidate",
    "BB_A9_B10_u_5_m_tail_shell10_candidate",
]

EXPECTED_U5_D_VECTOR = {
    "d_minus_p": 5,
    "d_pos_2sqrt_q": 5,
    "d_neg_2sqrt_q": 1,
}

EXPECTED_SHARED_COVER = {
    "L": 10,
    "T": 19,
    "d_vector": dict(EXPECTED_U5_D_VECTOR),
    "elliptic_curve_model": "V^2 = (X + 78)*(X - 1522)*(X + 1522)",
}

EXPECTED_PARAMETERS = {"p": 78, "q": 579121, "sqrt_q": 761}

POINT_ON_COVER = {
    "X": "1260642/121",
    "u_minus_p": "504/11",
    "u_pos_2sqrt_q": "464/11",
    "u_neg_2sqrt_q": "1202/11",
}

POINT_ON_E_L = {
    "X": "1260642/121",
    "Y": "1405474560/1331",
}

REQUIRED_CLOSED_LEDGER_EXCLUSIONS = [
    "wl491_wl517_globally_soluble_not_admissible_ledgers",
    "wl500_shell5_u5_refuted_cover",
    "wl517_shell10_L10_T11_u5_not_admissible_cover",
    "wl514_shell9_u7_refuted_cover",
]


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl491_ready(wl491: dict[str, Any]) -> bool:
    return (
        wl491.get("status") == "ok"
        and wl491.get("ready") is True
        and wl491.get("lemma_id")
        == "WL491_reusable_ambient_C_d_to_AA_BB_admissibility_filter"
        and wl491.get("work_log") == "wl491"
        and wl491.get("admissibility_filter_defined_here") is True
        and wl491.get("old_package_x_coordinate_collapse_used") is False
        and wl491.get("package_x_s_tilde_bridge_used") is False
        and wl491.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl491.get("single_curve_diagnostics_run") is False
        and not _claims_forbidden_bound(wl491)
    )


def _wl518_ready(wl518: dict[str, Any]) -> bool:
    selected = wl518.get("selected_next_gate", {})
    return (
        wl518.get("status") == "ok"
        and wl518.get("ready") is True
        and wl518.get("lemma_id") == "WL518_support_family_synthesis_after_wl517"
        and wl518.get("work_log") == "wl518"
        and wl518.get("input_work_log") == "wl517"
        and wl518.get("resolved_shell10_deferred_covers_here") is False
        and wl518.get("new_c_d_solubility_tested_here") is False
        and wl518.get("shell11_executed_here") is False
        and wl518.get("candidate_selected_here") is False
        and wl518.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl518.get("family_rank_or_selmer_diagnostics_run") is False
        and wl518.get("old_package_x_coordinate_collapse_used") is False
        and wl518.get("package_x_s_tilde_bridge_used") is False
        and selected.get("gate")
        == "resolve_shared_shell10_u5_ambient_C_d_global_solubility_cover"
        and selected.get("entered_here") is False
        and selected.get("candidate_ids") == DEFERRED_U5_IDS
        and selected.get("shared_cover") == "L=10,T=19,d=(5,5,1)"
        and selected.get("shared_cover_summary", {}).get("d_vector")
        == EXPECTED_U5_D_VECTOR
        and selected.get("wl491_filter_allowed_only_after_global_solubility") is True
        and wl518.get("genuinely_deferred_cover_families", [])
        and wl518["genuinely_deferred_cover_families"][0].get("candidate_ids")
        == DEFERRED_U5_IDS
        and not _claims_forbidden_bound(wl518)
    )


def _as_fraction(value: str) -> Fraction:
    return Fraction(value)


def _format_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _equation_checks_hold() -> bool:
    x_coord = _as_fraction(POINT_ON_COVER["X"])
    u_minus = _as_fraction(POINT_ON_COVER["u_minus_p"])
    u_pos = _as_fraction(POINT_ON_COVER["u_pos_2sqrt_q"])
    u_neg = _as_fraction(POINT_ON_COVER["u_neg_2sqrt_q"])
    return (
        x_coord + 78 == 5 * u_minus * u_minus
        and x_coord - 1522 == 5 * u_pos * u_pos
        and x_coord + 1522 == u_neg * u_neg
        and 5 * u_minus * u_pos * u_neg == _as_fraction(POINT_ON_E_L["Y"])
    )


def _global_point_certificate() -> dict[str, Any]:
    return {
        "status": "globally_soluble",
        "certificate_type": "exact_rational_point_on_C_d",
        "certificate_scope": (
            "This resolves only the shared shell-10 u_5 ambient C_d cover "
            "with L=10,T=19,d=(5,5,1). It is not a family Selmer, rank-zero, "
            "or uniform M_tail theorem."
        ),
        "cover_equations": [
            "X + 78 = 5*u_minus_p^2",
            "X - 1522 = 5*u_pos_2sqrt_q^2",
            "X + 1522 = u_neg_2sqrt_q^2",
        ],
        "elliptic_curve_model": {
            "equation": EXPECTED_SHARED_COVER["elliptic_curve_model"],
            "expanded_equation": (
                "V^2 = X^3 + 78*X^2 - 2316484*X - 180685752"
            ),
        },
        "cover_to_elliptic_curve_map": {
            "X": "same X-coordinate",
            "V": "5*u_minus_p*u_pos_2sqrt_q*u_neg_2sqrt_q",
            "reason": (
                "The product of the three cover equations is "
                "V^2=(X+78)(X-1522)(X+1522)."
            ),
        },
        "point_on_cover": dict(POINT_ON_COVER),
        "equation_checks": [
            "1260642/121 - -78 = 5*(504/11)^2",
            "1260642/121 - 1522 = 5*(464/11)^2",
            "1260642/121 - -1522 = (1202/11)^2",
        ],
        "induced_point_on_E_L": dict(POINT_ON_E_L),
        "mordell_weil_context": {
            "curve": "V^2 = X^3 + 78*X^2 - 2316484*X - 180685752",
            "point_used": "(1260642/121, 1405474560/1331)",
            "sage_context": (
                "This point is a visible rational point on the instantiated "
                "elliptic curve; no Mordell-Weil no-lift exhaustion is needed "
                "because the cover is globally soluble."
            ),
            "not_needed_for_non_solubility": True,
        },
        "conclusion": (
            "The displayed rational point satisfies all three C_d equations, "
            "so the shared shell-10 u_5 ambient cover is globally soluble."
        ),
    }


def _point_for_wl491(candidate_id: str) -> dict[str, Any]:
    quotient = "AA" if candidate_id.startswith("AA_") else "BB"
    a_value, b_value = (10, 9) if quotient == "AA" else (9, 10)
    return {
        "candidate_id": candidate_id,
        "quotient": quotient,
        "A": a_value,
        "B": b_value,
        "L": 10,
        "point_on_E_L": dict(POINT_ON_E_L),
        "parameters": dict(EXPECTED_PARAMETERS),
        "complete_d_squareclass": dict(EXPECTED_U5_D_VECTOR),
        "route_context": {
            "ambient_global_C_d_solubility_already_established": True,
            "old_package_x_S_tilde_bridge_not_used": True,
        },
    }


def _routing_state(filter_result: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_route": filter_result["ledger_route"],
        "ambient_c_d_global_solubility_status": "globally_soluble",
        "aa_bb_admissibility_status": filter_result["output_class"],
        "candidate_selected": False,
    }


def _classified_entries(certificate: dict[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for candidate_id in DEFERRED_U5_IDS:
        filter_input = _point_for_wl491(candidate_id)
        filter_result = classify_ambient_c_d_point_for_aa_bb_admissibility(
            filter_input
        )
        entries.append(
            {
                "candidate_id": candidate_id,
                "candidate_support": ["u_5"],
                "sample": {
                    "A": filter_input["A"],
                    "B": filter_input["B"],
                    "L": 10,
                    "T": 19,
                    "side": filter_input["quotient"],
                    "primitive": True,
                    "sqrt_q": 761,
                },
                "complete_c_d_cover": {
                    "d_vector": dict(EXPECTED_U5_D_VECTOR),
                    "parameters": dict(EXPECTED_PARAMETERS),
                    "cover_equations": list(certificate["cover_equations"]),
                    "elliptic_curve_model": EXPECTED_SHARED_COVER[
                        "elliptic_curve_model"
                    ],
                },
                "ambient_c_d_global_solubility": certificate,
                "wl491_filter_input": filter_input,
                "wl491_filter_result": filter_result,
                "routing_state": _routing_state(filter_result),
            }
        )
    return entries


def _resolution_summary(entries: list[dict[str, Any]]) -> dict[str, int]:
    filter_classes = [entry["wl491_filter_result"]["output_class"] for entry in entries]
    return {
        "wl518_remaining_deferred_candidate_count": 2,
        "shared_cover_count_resolved_here": 1,
        "classified_candidate_entry_count": len(entries),
        "ambient_globally_soluble_count": len(entries),
        "ambient_global_solubility_refuted_count": 0,
        "exact_ambient_point_certificate_count": 1,
        "wl491_filter_applied_count": len(entries),
        "aa_bb_admissible_count": filter_classes.count("admissible"),
        "aa_bb_not_admissible_count": filter_classes.count("not_admissible"),
    }


def build_wl519_resolve_shared_shell10_u5_ambient_c_d_global_solubility_cover(
    *,
    wl491: dict[str, Any],
    wl518: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl491_ready(wl491):
        violations.append("wl491_input_not_ready_or_not_scoped")
    if not _wl518_ready(wl518):
        violations.append("wl518_input_not_ready_or_not_scoped")

    certificate = _global_point_certificate()
    if not _equation_checks_hold():
        violations.append("exact_rational_point_does_not_satisfy_cover_equations")

    status = "ok" if not violations else "issues"
    classified_entries = _classified_entries(certificate) if status == "ok" else []
    if status == "ok" and any(
        entry["wl491_filter_result"].get("output_class") != "not_admissible"
        for entry in classified_entries
    ):
        violations.append("wl491_did_not_route_both_entries_to_not_admissible")
        status = "issues"
        classified_entries = []

    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl518 selected shared shell-10 u_5 ambient C_d cover plus wl491 filter",
        "pattern": "AA+BB",
        "lemma_id": (
            "WL519_resolve_shared_shell10_u5_ambient_C_d_global_solubility_cover"
        ),
        "work_log": "wl519",
        "input_work_logs": ["wl491", "wl518"],
        "resolved_shell10_deferred_covers_here": status == "ok",
        "resolution_summary": (
            _resolution_summary(classified_entries) if status == "ok" else {}
        ),
        "resolved_candidate_ids": list(DEFERRED_U5_IDS) if status == "ok" else [],
        "resolved_shared_cover": dict(EXPECTED_SHARED_COVER) if status == "ok" else {},
        "shared_cover_resolution_certificate": certificate if status == "ok" else {},
        "classified_shell10_u5_entries": classified_entries,
        "closed_ledger_do_not_reopen": list(REQUIRED_CLOSED_LEDGER_EXCLUSIONS),
        "closed_ledgers_reopened_count": 0,
        "shell10_not_admissible_ledgers_reopened_count": 0,
        "shell10_refuted_ledgers_reopened_count": 0,
        "wl491_filter_applied_to_new_point_here": status == "ok",
        "candidate_selected_here": False,
        "post_wl519_route_choice_made_here": False,
        "new_m_tail_or_kernel_candidate_selected_here": False,
        "new_m_tail_row_proved_here": False,
        "new_local_row_proved_here": False,
        "new_shell_or_grid_refreshed_here": False,
        "m_tail_diagnostics_extended_here": False,
        "new_supports_computed_here": False,
        "new_c_d_solubility_tested_here": status == "ok",
        "ambient_c_d_global_solubility_proved_here": status == "ok",
        "broad_rank_or_selmer_diagnostics_run": False,
        "family_rank_or_selmer_diagnostics_run": False,
        "single_curve_diagnostics_run": False,
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "uniform_m_tail_full_rank_claimed": False,
        "family_exclusion_proved_count": 0,
        "old_package_x_coordinate_collapse_used": False,
        "package_x_s_tilde_bridge_used": False,
        "search_count_used_as_progress": False,
        "shell11_executed_here": False,
        "advance_to_wl520": False,
        "stop_after_current_task": True,
        "remaining_gap": (
            "The wl518 selected shared shell-10 u_5 cover is globally soluble "
            "but both mirror entries fail wl491. The post-wl519 route choice "
            "is not made here."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
        "fraction_sanity_check": {
            "X_plus_78": _format_fraction(_as_fraction(POINT_ON_COVER["X"]) + 78),
            "X_minus_1522": _format_fraction(
                _as_fraction(POINT_ON_COVER["X"]) - 1522
            ),
            "X_plus_1522": _format_fraction(
                _as_fraction(POINT_ON_COVER["X"]) + 1522
            ),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl491", type=Path, required=True)
    parser.add_argument("--wl518", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl519_resolve_shared_shell10_u5_ambient_c_d_global_solubility_cover(
        wl491=load_json(args.wl491),
        wl518=load_json(args.wl518),
    )
    write_json(args.out, audit)
    summary = audit.get("resolution_summary", {})
    print(f"wrote AA+BB wl519 shared shell-10 u5 cover audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(
        "ambient_globally_soluble_count="
        f"{summary.get('ambient_globally_soluble_count', 0)}"
    )
    print(
        "aa_bb_not_admissible_count="
        f"{summary.get('aa_bb_not_admissible_count', 0)}"
    )
    print(
        "post_wl519_route_choice_made_here="
        f"{audit['post_wl519_route_choice_made_here']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
