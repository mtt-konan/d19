#!/usr/bin/env python3
"""Instantiate the wl485 explicit C_d cover equations for the u_3 candidate."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl485 / explicit_C_d_cover_equation_instantiation for "
    "the AA+BB complete d-coordinate route. It takes wl484 as input and writes "
    "the concrete C_d cover equations for the AA A=3, B=1 u_3 candidate "
    "d=(3,3,1), including root data, X-coordinate relations, the three "
    "difference equations, and a two-equation independent presentation. It "
    "records only a narrow local-solubility checklist for the next gate at "
    "infinity, 2, 3, and 13. It does not decide local or global solubility, "
    "does not run broad rank or Selmer diagnostics, does not prove an "
    "obstruction, does not prove a complete Sel_2(E) upper bound, and does "
    "not claim dim Sel_2(E)=2, rank zero, Sha[2]=0, or any family exclusion."
)

COORDINATE_ORDER = [
    "d_minus_p",
    "d_pos_2sqrt_q",
    "d_neg_2sqrt_q",
]
RELEVANT_PLACES = ["infinity", "2", "3", "13"]
TARGET_CANDIDATE_ID = "AA_A3_B1_u_3_complete_d_candidate"
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


def _wl484_ready(wl484: dict[str, Any]) -> bool:
    datum = wl484.get("obstruction_candidate_datum", {})
    gate = wl484.get("next_obstruction_workflow_gate", {})
    return (
        wl484.get("status") == "ok"
        and wl484.get("ready") is True
        and wl484.get("lemma_id") == "WL484_u3_obstruction_route_entry_audit"
        and wl484.get("work_log") == "wl484"
        and wl484.get("input_work_log") == "wl483"
        and datum.get("id") == TARGET_CANDIDATE_ID
        and datum.get("coordinate_order") == COORDINATE_ORDER
        and datum.get("d_vector_pattern") == "(3,3,1)"
        and datum.get("relevant_places") == RELEVANT_PLACES
        and gate.get("selected_gate") == "explicit_C_d_cover_local_global_solubility"
        and wl484.get("old_package_x_coordinate_collapse_used") is False
        and wl484.get("explicit_c_d_cover_solved_here") is False
        and wl484.get("obstruction_proved_here") is False
        and not _claims_forbidden_bound(wl484)
    )


def _sample(wl484: dict[str, Any]) -> dict[str, Any]:
    return dict(wl484["obstruction_candidate_datum"]["sample"])


def _cover_equations(wl484: dict[str, Any]) -> dict[str, Any]:
    datum = wl484["obstruction_candidate_datum"]
    sample = _sample(wl484)
    p = int(sample["p"])
    sqrt_q = int(sample["sqrt_q"])
    d_vector = dict(datum["d_vector"])
    e_minus = -p
    e_pos = 2 * sqrt_q
    e_neg = -2 * sqrt_q

    return {
        "candidate_id": datum["id"],
        "curve_model": datum["curve_model"],
        "sample": sample,
        "coordinate_order": COORDINATE_ORDER,
        "variables": ["X", "u_minus_p", "u_pos_2sqrt_q", "u_neg_2sqrt_q"],
        "d_vector": d_vector,
        "root_data": {
            "e_minus": {"symbolic": "-p", "value": e_minus},
            "e_pos": {"symbolic": "2*sqrt_q", "value": e_pos},
            "e_neg": {"symbolic": "-2*sqrt_q", "value": e_neg},
        },
        "x_coordinate_relations": [
            {
                "coordinate": "d_minus_p",
                "root": "e_minus",
                "general_equation": "X - e_minus = d_minus_p*u_minus_p^2",
                "instantiated_equation": "X + 40 = 3*u_minus_p^2",
            },
            {
                "coordinate": "d_pos_2sqrt_q",
                "root": "e_pos",
                "general_equation": (
                    "X - e_pos = d_pos_2sqrt_q*u_pos_2sqrt_q^2"
                ),
                "instantiated_equation": "X - 104 = 3*u_pos_2sqrt_q^2",
            },
            {
                "coordinate": "d_neg_2sqrt_q",
                "root": "e_neg",
                "general_equation": (
                    "X - e_neg = d_neg_2sqrt_q*u_neg_2sqrt_q^2"
                ),
                "instantiated_equation": "X + 104 = u_neg_2sqrt_q^2",
            },
        ],
        "three_difference_equations": [
            {
                "id": "minus_minus_pos",
                "general_equation": (
                    "d_minus_p*u_minus_p^2 - "
                    "d_pos_2sqrt_q*u_pos_2sqrt_q^2 = e_pos - e_minus"
                ),
                "instantiated_equation": (
                    "3*u_minus_p^2 - 3*u_pos_2sqrt_q^2 = 144"
                ),
            },
            {
                "id": "minus_minus_neg",
                "general_equation": (
                    "d_minus_p*u_minus_p^2 - "
                    "d_neg_2sqrt_q*u_neg_2sqrt_q^2 = e_neg - e_minus"
                ),
                "instantiated_equation": (
                    "3*u_minus_p^2 - u_neg_2sqrt_q^2 = -64"
                ),
            },
            {
                "id": "pos_minus_neg",
                "general_equation": (
                    "d_pos_2sqrt_q*u_pos_2sqrt_q^2 - "
                    "d_neg_2sqrt_q*u_neg_2sqrt_q^2 = e_neg - e_pos"
                ),
                "instantiated_equation": (
                    "3*u_pos_2sqrt_q^2 - u_neg_2sqrt_q^2 = -208"
                ),
            },
        ],
        "two_independent_equations": [
            "3*u_minus_p^2 - 3*u_pos_2sqrt_q^2 = 144",
            "3*u_minus_p^2 - u_neg_2sqrt_q^2 = -64",
        ],
        "normalized_independent_equations": [
            "u_minus_p^2 - u_pos_2sqrt_q^2 = 48",
            "3*u_minus_p^2 - u_neg_2sqrt_q^2 = -64",
        ],
        "dependency_check": {
            "dependent_equation": "pos_minus_neg",
            "derived_as": "minus_minus_neg - minus_minus_pos",
            "rhs_check": "-64 - 144 = -208",
            "solubility_decided_here": False,
        },
    }


def _local_checklist() -> list[dict[str, Any]]:
    return [
        {
            "place": "infinity",
            "scope": "real place for the instantiated two-equation cover",
            "next_check": (
                "Decide whether the two independent equations have an R-point, "
                "equivalently whether an admissible real X satisfies the three "
                "X-coordinate square relations."
            ),
            "prior_row_status": (
                "wl483 records no new justified real row killing u_3."
            ),
            "status": "not_checked_here",
            "local_solubility_decided_here": False,
        },
        {
            "place": "2",
            "scope": "Q_2 place in the wl478 ordinary even-sqrt_q stratum",
            "next_check": (
                "Run a direct Q_2 solubility check for the full instantiated "
                "cover, not just the already-recorded squareclass row."
            ),
            "prior_row_status": (
                "wl483 records the ordinary dyadic row as already accounted for "
                "and not killing u_3."
            ),
            "status": "not_checked_here",
            "local_solubility_decided_here": False,
        },
        {
            "place": "3",
            "scope": "Q_3 place at the active odd L-prime",
            "next_check": (
                "Run a direct Q_3 solubility check for the two independent "
                "equations with d_minus_p=d_pos_2sqrt_q=3."
            ),
            "prior_row_status": (
                "wl483 records the wl475 odd L row at 3 as already accounted "
                "for and not killing u_3."
            ),
            "status": "not_checked_here",
            "local_solubility_decided_here": False,
        },
        {
            "place": "13",
            "scope": "Q_13 place at the odd sqrt_q-prime",
            "next_check": (
                "Run a direct Q_13 solubility check for the full instantiated "
                "cover and the root separations involving sqrt_q=52."
            ),
            "prior_row_status": (
                "wl483 records the wl477 odd sqrt_q row at 13 as already "
                "accounted for and not killing u_3."
            ),
            "status": "not_checked_here",
            "local_solubility_decided_here": False,
        },
    ]


def build_wl485_explicit_cd_cover_equation_instantiation(
    *, wl484: dict[str, Any]
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl484_ready(wl484):
        violations.append("wl484_input_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl484 explicit_C_d_cover_local_global_solubility gate",
        "pattern": "AA+BB",
        "lemma_id": "WL485_explicit_C_d_cover_equation_instantiation",
        "work_log": "wl485",
        "input_work_log": "wl484",
        "explicit_c_d_cover": _cover_equations(wl484) if status == "ok" else {},
        "relevant_places": list(RELEVANT_PLACES),
        "narrow_local_solubility_checklist_for_next_gate": (
            _local_checklist() if status == "ok" else []
        ),
        "equation_instantiation_only": True,
        "local_solubility_decided_here": False,
        "global_solubility_decided_here": False,
        "obstruction_proved_here": False,
        "explicit_c_d_cover_solved_here": False,
        "symbolic_rank_status": "not_computed_here",
        "computed_rank_status": "not_run_equation_instantiation_only",
        "broad_rank_or_selmer_diagnostics_run": False,
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
    parser.add_argument("--wl484", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl485_explicit_cd_cover_equation_instantiation(
        wl484=load_json(args.wl484)
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl485 explicit C_d cover equations to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"local_solubility_decided_here={audit['local_solubility_decided_here']}")
    print(f"global_solubility_decided_here={audit['global_solubility_decided_here']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
