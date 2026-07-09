#!/usr/bin/env python3
"""Resolve the remaining shell-9 u_7 ambient C_d global-solubility ledger."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl514 / resolve_remaining_shell9_u7_ambient_C_d_"
    "global_solubility_ledger. It uses wl513 as input, enters only the "
    "selected remaining shell-9 u_7 cover at L=7,T=16,d=(7,7,1), resolves "
    "that shared cover by an exhaustive Mordell-Weil-sieve no-lift "
    "certificate modulo 17, routes the two u_7 ledgers to ambient globally "
    "not soluble, and stops before applying wl491, executing shell 10, "
    "making the post-wl514 route choice, selecting a final obstruction "
    "candidate, proving local rows beyond the one cover certificate, running "
    "broad rank or Selmer diagnostics, using the old package-x S~ bridge, or "
    "claiming a complete Sel_2(E) upper bound, dim Sel_2(E)=2, rank zero, "
    "Sha[2]=0, uniform M_tail full rank, or any family exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

DEFERRED_U7_IDS = [
    "AA_A7_B9_u_7_m_tail_shell9_candidate",
    "BB_A9_B7_u_7_m_tail_shell9_candidate",
]

EXPECTED_U7_D_VECTOR = {
    "d_minus_p": 7,
    "d_pos_2sqrt_q": 7,
    "d_neg_2sqrt_q": 1,
}

EXPECTED_SHARED_COVER = {
    "L": 7,
    "T": 16,
    "d_vector": dict(EXPECTED_U7_D_VECTOR),
    "elliptic_curve_model": "V^2 = (X + 120)*(X - 904)*(X + 904)",
}

REQUIRED_CLOSED_LEDGER_EXCLUSIONS = [
    "u_3_processed_or_deprioritized_after_wl493_wl491",
    "bounded_v_5_entries_disposed_by_wl495_wl496",
    "shell5_u_5_entries_refuted_by_wl500",
    "shell6_empty_diagnostic_output_from_wl502",
    "shell7_entries_disposed_by_wl505_wl506",
    "shell8_pure_u_3_processed_exclusions_from_wl508",
    "shell9_globally_soluble_not_admissible_ledgers_from_wl511",
    "shell9_v_13_deferred_ledgers_refuted_by_wl512",
]

Point = tuple[int, int] | None
P = 17
A2 = 120
A4 = -817216
G = (1032 % P, 16896 % P)
TORSION_REDUCTIONS: list[Point] = [
    None,
    (-904 % P, 0),
    (-120 % P, 0),
    (904 % P, 0),
]


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl513_ready(wl513: dict[str, Any]) -> bool:
    selected = wl513.get("selected_next_gate", {})
    return (
        wl513.get("status") == "ok"
        and wl513.get("ready") is True
        and wl513.get("lemma_id") == "WL513_post_wl512_route_choice_audit"
        and wl513.get("work_log") == "wl513"
        and wl513.get("input_work_log") == "wl512"
        and wl513.get("remaining_deferred_candidate_ids") == DEFERRED_U7_IDS
        and wl513.get("remaining_deferred_shared_cover") == EXPECTED_SHARED_COVER
        and selected.get("gate")
        == "resolve_remaining_shell9_u7_ambient_C_d_global_solubility_ledgers"
        and selected.get("entered_here") is False
        and selected.get("candidate_ids") == DEFERRED_U7_IDS
        and selected.get("shell10_executed_here") is False
        and selected.get("wl491_filter_allowed_only_after_global_solubility") is True
        and wl513.get("shell9_not_admissible_ledgers_reopened_count") == 0
        and wl513.get("shell9_v13_refuted_ledgers_reopened_count") == 0
        and wl513.get("closed_ledgers_reopened_count") == 0
        and wl513.get("new_c_d_solubility_tested_here") is False
        and wl513.get("wl491_filter_applied_to_new_point_here") is False
        and wl513.get("shell10_executed_here") is False
        and wl513.get("advance_to_wl514") is False
        and wl513.get("old_package_x_coordinate_collapse_used") is False
        and wl513.get("package_x_s_tilde_bridge_used") is False
        and wl513.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl513.get("family_rank_or_selmer_diagnostics_run") is False
        and not _claims_forbidden_bound(wl513)
    )


def _inv(value: int, prime: int = P) -> int:
    return pow(value % prime, prime - 2, prime)


def _legendre(value: int, prime: int = P) -> int:
    residue = value % prime
    if residue == 0:
        return 0
    return 1 if pow(residue, (prime - 1) // 2, prime) == 1 else -1


def _add_points(left: Point, right: Point, prime: int = P) -> Point:
    if left is None:
        return right
    if right is None:
        return left

    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and (y1 + y2) % prime == 0:
        return None

    if left == right:
        slope = (3 * x1 * x1 + 2 * A2 * x1 + A4) * _inv(2 * y1, prime)
    else:
        slope = (y2 - y1) * _inv(x2 - x1, prime)
    slope %= prime
    intercept = (y1 - slope * x1) % prime
    x3 = (slope * slope - A2 - x1 - x2) % prime
    y3 = (-(slope * x3 + intercept)) % prime
    return (x3, y3)


def _multiply_point(point: Point, multiple: int, prime: int = P) -> Point:
    result: Point = None
    addend = point
    n = multiple
    while n:
        if n & 1:
            result = _add_points(result, addend, prime)
        addend = _add_points(addend, addend, prime)
        n >>= 1
    return result


def _point_order(point: Point, prime: int = P) -> int:
    running: Point = None
    for order in range(1, 3 * prime + 100):
        running = _add_points(running, point, prime)
        if running is None:
            return order
    raise ValueError("point order search bound exceeded")


def _point_to_str(point: Point) -> str:
    return "O" if point is None else f"({point[0]},{point[1]})"


def _has_mod_17_cover_lift(point: Point) -> bool:
    if point is None:
        return _legendre(7) == 1
    x, _y = point
    square_tests = [
        (x + 120) * _inv(7),
        (x - 904) * _inv(7),
        x + 904,
    ]
    return all(_legendre(value) >= 0 for value in square_tests)


def _curve_points_mod_17() -> list[Point]:
    points: list[Point] = [None]
    for x in range(P):
        rhs = (x + 120) * (x - 904) * (x + 904)
        for y in range(P):
            if y * y % P == rhs % P:
                points.append((x, y))
    return points


def _rational_reduction_image() -> list[Point]:
    generator_order = _point_order(G)
    image: set[Point] = set()
    for multiple in range(generator_order):
        n_g = _multiply_point(G, multiple)
        for torsion in TORSION_REDUCTIONS:
            image.add(_add_points(n_g, torsion))
    return sorted(image, key=lambda point: (-1, -1) if point is None else point)


def _mod_17_sieve() -> dict[str, Any]:
    rational_image = _rational_reduction_image()
    local_lift_candidates = [
        point for point in _curve_points_mod_17() if _has_mod_17_cover_lift(point)
    ]
    intersection = [
        point for point in rational_image if point in set(local_lift_candidates)
    ]
    return {
        "prime": P,
        "good_reduction": True,
        "reduction_model": "y^2=(x+1)*(x-3)*(x+3) over F_17",
        "square_residues_mod_17": [
            residue for residue in range(P) if _legendre(residue) >= 0
        ],
        "legendre_symbol_7_mod_17": _legendre(7),
        "generator_reduction": _point_to_str(G),
        "generator_order_mod_17": _point_order(G),
        "torsion_reductions": [_point_to_str(point) for point in TORSION_REDUCTIONS],
        "rational_reduction_image_size": len(rational_image),
        "rational_reduction_image": [_point_to_str(point) for point in rational_image],
        "local_lift_candidate_reductions": [
            _point_to_str(point) for point in local_lift_candidates
        ],
        "rational_image_intersection_with_local_lift_candidates": [
            _point_to_str(point) for point in intersection
        ],
        "point_at_infinity_lift_blocked_reason": "7_is_not_a_square_mod_17",
        "conclusion": (
            "Every rational point on E reduces into the listed "
            "<G>+E[2] image modulo 17, but none of those reductions satisfies "
            "the three d=(7,7,1) squareclass lift conditions; the point at "
            "infinity is also blocked because 7 is not a square modulo 17."
        ),
    }


def _no_lift_certificate() -> dict[str, Any]:
    return {
        "status": "globally_not_soluble",
        "certificate_type": "mordell_weil_sieve_no_lift_mod_17",
        "certificate_scope": (
            "This resolves only the shared shell-9 u_7 ambient C_d cover with "
            "L=7,T=16,d=(7,7,1). It is not a family Selmer, rank-zero, or "
            "uniform M_tail theorem."
        ),
        "cover_equations": [
            "X + 120 = 7*u_minus_p^2",
            "X - 904 = 7*u_pos_2sqrt_q^2",
            "X + 904 = u_neg_2sqrt_q^2",
        ],
        "elliptic_curve_model": {
            "equation": "V^2 = (X + 120)*(X - 904)*(X + 904)",
            "expanded_equation": "V^2 = X^3 + 120*X^2 - 817216*X - 98065920",
        },
        "cover_to_elliptic_curve_map": {
            "X": "same X-coordinate",
            "V": "7*u_minus_p*u_pos_2sqrt_q*u_neg_2sqrt_q",
            "reason": (
                "The product of the three cover equations is "
                "V^2=(X+120)(X-904)(X+904)."
            ),
        },
        "mordell_weil_certificate": {
            "rank": 1,
            "generator": "(1032,16896)",
            "torsion_points": ["O", "(-904,0)", "(-120,0)", "(904,0)"],
            "exhaustive_description": "E(Q)=<G> + E(Q)[2] for G=(1032,16896)",
            "scope": "single instantiated curve E_{L=7,T=16}, not a family theorem",
        },
        "mod_17_sieve": _mod_17_sieve(),
        "conclusion": (
            "The Mordell-Weil certificate makes the modulo-17 image exhaustive "
            "for E(Q), and the modulo-17 squareclass sieve has empty "
            "intersection with the possible d=(7,7,1) cover lifts. Therefore "
            "the instantiated ambient C_d cover has no rational point."
        ),
    }


def _not_applied_filter_result_for_refuted() -> dict[str, Any]:
    return {
        "output_class": "not_applied",
        "reason": "ambient_C_d_global_solubility_refuted",
        "blocking_reasons": ["ambient_C_d_has_no_rational_point"],
    }


def _refuted_routing_state() -> dict[str, Any]:
    return {
        "ledger_route": "ambient_c_d_global_solubility_refuted_ledger",
        "ambient_c_d_global_solubility_status": "globally_not_soluble",
        "wl491_filter_applied": False,
        "candidate_selected": False,
    }


def _classified_u7_entries(certificate: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": candidate_id,
            "candidate_support": ["u_7"],
            "sample": {"L": 7, "T": 16},
            "complete_c_d_cover": {
                "d_vector": dict(EXPECTED_U7_D_VECTOR),
                "parameters": {"p": -120, "q": 204304, "sqrt_q": 452},
                "cover_equations": list(certificate["cover_equations"]),
            },
            "ambient_c_d_global_solubility": certificate,
            "wl491_filter_result": _not_applied_filter_result_for_refuted(),
            "routing_state": _refuted_routing_state(),
        }
        for candidate_id in DEFERRED_U7_IDS
    ]


def _resolution_summary() -> dict[str, int]:
    return {
        "wl513_remaining_deferred_candidate_count": 2,
        "shared_cover_count_resolved_here": 1,
        "classified_candidate_entry_count": 2,
        "ambient_globally_soluble_count": 0,
        "ambient_global_solubility_refuted_count": 2,
        "exhaustive_no_lift_certificate_count": 1,
        "wl491_filter_applied_count": 0,
        "aa_bb_admissible_count": 0,
        "aa_bb_filter_not_applied_count": 2,
    }


def build_wl514_resolve_remaining_shell9_u7_ambient_c_d_global_solubility_ledger(
    *,
    wl513: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl513_ready(wl513):
        violations.append("wl513_input_not_ready_or_not_scoped")

    certificate = _no_lift_certificate()
    sieve = certificate["mod_17_sieve"]
    if sieve["rational_image_intersection_with_local_lift_candidates"] != []:
        violations.append("mod_17_sieve_did_not_exclude_all_rational_reductions")
    if sieve["legendre_symbol_7_mod_17"] != -1:
        violations.append("mod_17_infinity_lift_not_blocked")

    status = "ok" if not violations else "issues"
    classified_entries = _classified_u7_entries(certificate) if status == "ok" else []
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl513 selected shell-9 u_7 ambient C_d cover",
        "pattern": "AA+BB",
        "lemma_id": (
            "WL514_resolve_remaining_shell9_u7_ambient_C_d_global_solubility_ledger"
        ),
        "work_log": "wl514",
        "input_work_log": "wl513",
        "resolved_remaining_shell9_u7_ledger_here": status == "ok",
        "resolution_summary": _resolution_summary() if status == "ok" else {},
        "resolved_candidate_ids": list(DEFERRED_U7_IDS) if status == "ok" else [],
        "resolved_shared_cover": dict(EXPECTED_SHARED_COVER) if status == "ok" else {},
        "shared_cover_resolution_certificate": certificate if status == "ok" else {},
        "classified_u7_entries": classified_entries,
        "closed_ledger_do_not_reopen": list(REQUIRED_CLOSED_LEDGER_EXCLUSIONS),
        "shell9_not_admissible_ledgers_reopened_count": 0,
        "shell9_v13_refuted_ledgers_reopened_count": 0,
        "closed_ledgers_reopened_count": 0,
        "wl491_filter_applied_to_new_point_here": False,
        "candidate_selected_here": False,
        "post_wl514_route_choice_made_here": False,
        "new_m_tail_or_kernel_candidate_selected_here": False,
        "new_m_tail_row_proved_here": False,
        "new_local_row_proved_here": False,
        "new_shell_or_grid_refreshed_here": False,
        "m_tail_diagnostics_extended_here": False,
        "new_supports_computed_here": False,
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
        "shell10_executed_here": False,
        "advance_to_wl515": False,
        "stop_after_current_task": True,
        "remaining_gap": (
            "The selected wl513 gate is resolved. The next route choice after "
            "all shell-9 deferred ambient C_d ledgers have been classified is "
            "not made here."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl513", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl514_resolve_remaining_shell9_u7_ambient_c_d_global_solubility_ledger(
        wl513=load_json(args.wl513),
    )
    write_json(args.out, audit)
    summary = audit.get("resolution_summary", {})
    print(f"wrote AA+BB wl514 shell-9 u7 ambient C_d audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(
        "ambient_global_solubility_refuted_count="
        f"{summary.get('ambient_global_solubility_refuted_count', 0)}"
    )
    print(f"wl491_filter_applied_count={summary.get('wl491_filter_applied_count', 0)}")
    print(
        "post_wl514_route_choice_made_here="
        f"{audit['post_wl514_route_choice_made_here']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
