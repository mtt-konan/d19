#!/usr/bin/env python3
"""Audit the route impact of the wl486 global point on the u_3 C_d cover."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl487 / route_impact_of_global_point for the AA+BB "
    "complete d-coordinate route. It takes wl486 as input, records that the "
    "explicit integral point refutes only the specific u_3 interpretation as "
    "a locally soluble globally pointless obstruction, compares the induced "
    "point against the visible rational E_L[2](Q) complete d-coordinate "
    "baseline, and records M_tail/global-obstruction route impact. It does "
    "not run broad rank or Selmer diagnostics, does not prove a complete "
    "Sel_2(E) upper bound, and does not claim dim Sel_2(E)=2, rank zero, "
    "Sha[2]=0, full Mordell-Weil torsion, or any family exclusion."
)

COORDINATE_ORDER = [
    "d_minus_p",
    "d_pos_2sqrt_q",
    "d_neg_2sqrt_q",
]
TARGET_CANDIDATE_ID = "AA_A3_B1_u_3_complete_d_candidate"
FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

P = 40
SQRT_Q = 52
Q = SQRT_Q * SQRT_Q
POINT_ON_COVER = {
    "X": 152,
    "u_minus_p": 8,
    "u_pos_2sqrt_q": 4,
    "u_neg_2sqrt_q": 16,
}
POINT_ON_E = {"X": 152, "Y": 1536}


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl486_ready(wl486: dict[str, Any]) -> bool:
    gate = wl486.get("local_solubility_gate", {})
    witness = gate.get("global_solubility_witness", {})
    return (
        wl486.get("status") == "ok"
        and wl486.get("ready") is True
        and wl486.get("lemma_id") == "WL486_local_solubility_gate"
        and wl486.get("work_log") == "wl486"
        and wl486.get("input_work_log") == "wl485"
        and gate.get("candidate_id") == TARGET_CANDIDATE_ID
        and gate.get("coordinate_order") == COORDINATE_ORDER
        and gate.get("d_vector")
        == {
            "d_minus_p": 3,
            "d_pos_2sqrt_q": 3,
            "d_neg_2sqrt_q": 1,
        }
        and gate.get("next_gate") == "route_impact_of_global_point"
        and witness.get("status") == "globally_soluble"
        and witness.get("point_on_cover") == POINT_ON_COVER
        and witness.get("induced_point_on_E_L", {}).get("X") == POINT_ON_E["X"]
        and witness.get("induced_point_on_E_L", {}).get("Y") == POINT_ON_E["Y"]
        and wl486.get("candidate_obstruction_refuted_here") is True
        and wl486.get("explicit_c_d_cover_solved_here") is True
        and wl486.get("old_package_x_coordinate_collapse_used") is False
        and wl486.get("broad_rank_or_selmer_diagnostics_run") is False
        and not _claims_forbidden_bound(wl486)
    )


def _squareclass(n: int) -> int:
    if n == 0:
        return 0
    sign = -1 if n < 0 else 1
    n = abs(n)
    result = 1
    factor = 2
    while factor * factor <= n:
        exponent = 0
        while n % factor == 0:
            n //= factor
            exponent += 1
        if exponent % 2 == 1:
            result *= factor
        factor += 1 if factor == 2 else 2
    if n > 1:
        result *= n
    return sign * result


def _x_minus_roots() -> dict[str, int]:
    x = POINT_ON_E["X"]
    return {
        "X_plus_p": x + P,
        "X_minus_2sqrt_q": x - 2 * SQRT_Q,
        "X_plus_2sqrt_q": x + 2 * SQRT_Q,
    }


def _point_squareclass_tuple() -> list[int]:
    differences = _x_minus_roots()
    return [
        _squareclass(differences["X_plus_p"]),
        _squareclass(differences["X_minus_2sqrt_q"]),
        _squareclass(differences["X_plus_2sqrt_q"]),
    ]


def _point_arithmetic_ok() -> bool:
    differences = _x_minus_roots()
    x = POINT_ON_E["X"]
    y = POINT_ON_E["Y"]
    return (
        differences["X_plus_p"] == 3 * POINT_ON_COVER["u_minus_p"] ** 2
        and differences["X_minus_2sqrt_q"]
        == 3 * POINT_ON_COVER["u_pos_2sqrt_q"] ** 2
        and differences["X_plus_2sqrt_q"]
        == POINT_ON_COVER["u_neg_2sqrt_q"] ** 2
        and y * y == (x + P) * (x * x - 4 * Q)
        and _point_squareclass_tuple() == [3, 3, 1]
    )


def _torsion_baseline_squareclasses() -> dict[str, list[int]]:
    t_minus_p = [
        (-P - 2 * SQRT_Q) * (-P + 2 * SQRT_Q),
        -P - 2 * SQRT_Q,
        -P + 2 * SQRT_Q,
    ]
    t_pos_2sqrt_q = [
        2 * SQRT_Q + P,
        (2 * SQRT_Q + P) * (4 * SQRT_Q),
        4 * SQRT_Q,
    ]
    t_neg_2sqrt_q = [
        -2 * SQRT_Q + P,
        -4 * SQRT_Q,
        (-2 * SQRT_Q + P) * (-4 * SQRT_Q),
    ]
    return {
        "O": [1, 1, 1],
        "T_minus_p": [_squareclass(n) for n in t_minus_p],
        "T_pos_2sqrt_q": [_squareclass(n) for n in t_pos_2sqrt_q],
        "T_neg_2sqrt_q": [_squareclass(n) for n in t_neg_2sqrt_q],
    }


def _refutation_scope(wl486: dict[str, Any]) -> dict[str, Any]:
    gate = wl486["local_solubility_gate"]
    return {
        "candidate_id": gate["candidate_id"],
        "d_vector": dict(gate["d_vector"]),
        "refuted_interpretation": (
            "this_specific_u3_as_locally_soluble_globally_pointless_obstruction"
        ),
        "refuted_here": True,
        "global_point_on_this_cover": True,
        "does_not_refute": [
            "M_tail_uniform_full_rank_missing_as_a_general_route_gap",
            "existence_of_other_complete_d_coordinate_obstructions",
            "need_for_a_complete_Selmer_upper_bound",
        ],
    }


def _global_point_classification() -> dict[str, Any]:
    point_tuple = _point_squareclass_tuple()
    baseline = _torsion_baseline_squareclasses()
    roots = [-P, 2 * SQRT_Q, -2 * SQRT_Q]
    return {
        "curve_model": "E_L: Y^2=(X+p)*(X^2-4*q)",
        "parameters": {"p": P, "q": Q, "sqrt_q": SQRT_Q},
        "point_on_cover": dict(POINT_ON_COVER),
        "point_on_E_L": dict(POINT_ON_E),
        "exact_checks": {
            "x_minus_roots": _x_minus_roots(),
            "cover_relations": [
                "192 = 3*8^2",
                "48 = 3*4^2",
                "256 = 1*16^2",
            ],
            "curve_equation": "1536^2 = (152+40)*(152^2 - 4*2704)",
        },
        "complete_d_squareclass": {
            "coordinate_order": list(COORDINATE_ORDER),
            "representative": {
                "d_minus_p": point_tuple[0],
                "d_pos_2sqrt_q": point_tuple[1],
                "d_neg_2sqrt_q": point_tuple[2],
            },
            "product_relation_square": "3*3*1 = 3^2",
        },
        "visible_two_torsion_baseline_comparison": {
            "baseline_source": "wl474 D3 rational E_L[2](Q) baseline",
            "baseline_squareclass_representatives": baseline,
            "point_squareclass_tuple": point_tuple,
            "matches_visible_two_torsion_baseline": point_tuple
            in baseline.values(),
            "not_a_visible_two_torsion_point_checks": {
                "Y_nonzero": POINT_ON_E["Y"] != 0,
                "X_not_equal_to_roots": POINT_ON_E["X"] not in roots,
            },
        },
        "classification": "non_torsion_candidate_not_visible_two_torsion_baseline",
        "full_mordell_weil_torsion_decided_here": False,
        "rank_decided_here": False,
    }


def _route_impact() -> dict[str, Any]:
    return {
        "m_tail_status_after_global_point": (
            "u3_no_longer_available_as_global_obstruction_candidate"
        ),
        "m_tail_full_rank_rescue_reopened_here": False,
        "new_local_or_hilbert_row_found_here": False,
        "global_obstruction_routing_status": (
            "current_explicit_C_d_obstruction_route_refuted_by_global_point"
        ),
        "ledger_update": (
            "mark d=(3,3,1) as globally soluble with a non-baseline "
            "complete d-coordinate point candidate; do not count it as an "
            "obstruction or as Selmer upper-bound progress"
        ),
    }


def _next_narrow_gate() -> dict[str, Any]:
    return {
        "gate": "select_next_complete_d_coordinate_route_after_u3_global_point",
        "entry_condition": (
            "wl487 has marked the AA A=3,B=1 u_3 cover globally soluble and "
            "not a visible E_L[2](Q) baseline point"
        ),
        "allowed_next_actions": [
            "remove_this_u3_cover_from_the_obstruction_candidate_ledger",
            "choose_the_next_single_complete_d_coordinate_candidate_or_row_gap",
            "keep_M_tail_and_global_obstruction_ledgers_separate",
        ],
        "forbidden_next_actions_here": [
            "run_broad_rank_or_selmer_diagnostics",
            "claim_complete_selmer_upper_bound",
            "claim_rank_zero_or_sha2_triviality",
            "claim_family_exclusion",
        ],
        "entered_here": False,
    }


def build_wl487_route_impact_of_global_point(
    *, wl486: dict[str, Any]
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl486_ready(wl486):
        violations.append("wl486_input_not_ready_or_not_scoped")
    if not _point_arithmetic_ok():
        violations.append("global_point_arithmetic_check_failed")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl486 local solubility gate and global witness",
        "pattern": "AA+BB",
        "lemma_id": "WL487_route_impact_of_global_point",
        "work_log": "wl487",
        "input_work_log": "wl486",
        "refutation_scope": _refutation_scope(wl486) if status == "ok" else {},
        "global_point_classification": (
            _global_point_classification() if status == "ok" else {}
        ),
        "route_impact": _route_impact() if status == "ok" else {},
        "next_narrow_gate": _next_narrow_gate(),
        "local_solubility_decided_here": False,
        "global_solubility_decided_here": False,
        "candidate_obstruction_refuted_here": status == "ok",
        "obstruction_proved_here": False,
        "explicit_c_d_cover_solved_here": False,
        "symbolic_rank_status": "u3_global_point_recorded_no_rank_conclusion",
        "computed_rank_status": "not_run_route_impact_only",
        "broad_rank_or_selmer_diagnostics_run": False,
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
        "old_package_x_coordinate_collapse_used": False,
        "search_count_used_as_progress": False,
        "stop_after_current_task": True,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl486", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl487_route_impact_of_global_point(wl486=load_json(args.wl486))
    write_json(args.out, audit)
    print(f"wrote AA+BB wl487 route impact audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    if audit["status"] == "ok":
        classification = audit["global_point_classification"]["classification"]
        print(f"classification={classification}")
        print(
            "m_tail_status_after_global_point="
            f"{audit['route_impact']['m_tail_status_after_global_point']}"
        )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
