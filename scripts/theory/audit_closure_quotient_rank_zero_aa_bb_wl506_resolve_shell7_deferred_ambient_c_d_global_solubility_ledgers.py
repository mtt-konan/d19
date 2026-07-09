#!/usr/bin/env python3
"""Resolve wl505 deferred shell-7 ambient C_d global-solubility ledgers."""

from __future__ import annotations

import argparse
import sys
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

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
    "This audits only wl506 / resolve_shell7_deferred_ambient_C_d_global_"
    "solubility_ledgers. It takes wl505 as input, resolves exactly the four "
    "deferred shell-7 ambient C_d ledgers, does not re-open the eight shell-7 "
    "globally soluble but not AA+BB-admissible ledgers, does not re-open the "
    "two pure u_3 processed exclusions, applies wl491 only to the two entries "
    "whose ambient global C_d point is established here, routes the two w_5 "
    "entries to the ambient global-solubility refuted ledger, and stops before "
    "selecting a final obstruction candidate, proving local rows, running "
    "broad rank or Selmer diagnostics, advancing to wl507, using the old "
    "package-x S~ bridge, or claiming a complete Sel_2(E) upper bound, "
    "dim Sel_2(E)=2, rank zero, Sha[2]=0, uniform M_tail full rank, or any "
    "family exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

TARGET_DEFERRED_IDS = [
    "AA_A4_B7_w_5_m_tail_shell7_candidate",
    "AA_A7_B3_u_7_plus_w_37_m_tail_shell7_candidate",
    "BB_A3_B7_u_7_plus_w_37_m_tail_shell7_candidate",
    "BB_A7_B4_w_5_m_tail_shell7_candidate",
]

REFUTED_W5_IDS = [
    "AA_A4_B7_w_5_m_tail_shell7_candidate",
    "BB_A7_B4_w_5_m_tail_shell7_candidate",
]

SOLUBLE_U7_W37_IDS = [
    "AA_A7_B3_u_7_plus_w_37_m_tail_shell7_candidate",
    "BB_A3_B7_u_7_plus_w_37_m_tail_shell7_candidate",
]

W5_D_VECTOR = {
    "d_minus_p": 1,
    "d_pos_2sqrt_q": 5,
    "d_neg_2sqrt_q": 5,
}

W5_PARAMETERS = {
    "p": -114,
    "q": 34225,
    "sqrt_q": 185,
}

U7_W37_D_VECTOR = {
    "d_minus_p": 7,
    "d_pos_2sqrt_q": 259,
    "d_neg_2sqrt_q": 37,
}

U7_W37_PARAMETERS = {
    "p": 192,
    "q": 87616,
    "sqrt_q": 296,
}

PROCESSED_U3_EXCLUSION_IDS = [
    "AA_A6_B7_u_3_m_tail_shell7_candidate",
    "BB_A7_B6_u_3_m_tail_shell7_candidate",
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


def _wl505_ready(wl505: dict[str, Any]) -> bool:
    summary = wl505.get("route_summary", {})
    return (
        wl505.get("status") == "ok"
        and wl505.get("ready") is True
        and wl505.get("lemma_id")
        == (
            "WL505_route_active_shell7_M_tail_supports_through_ambient_C_d_"
            "solubility_then_wl491_filter"
        )
        and wl505.get("work_log") == "wl505"
        and summary.get("active_shell7_support_entry_count") == 12
        and summary.get("ambient_globally_soluble_count") == 8
        and summary.get("ambient_global_solubility_deferred_count") == 4
        and summary.get("aa_bb_filter_deferred_count") == 4
        and wl505.get("all_active_shell7_supports_fully_routed_here") is False
        and wl505.get("candidate_selected_here") is False
        and wl505.get("new_m_tail_row_proved_here") is False
        and wl505.get("new_local_row_proved_here") is False
        and wl505.get("old_package_x_coordinate_collapse_used") is False
        and wl505.get("package_x_s_tilde_bridge_used") is False
        and wl505.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl505.get("single_curve_diagnostics_run") is False
        and not _claims_forbidden_bound(wl505)
    )


def _format_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _sqrt_fraction(value: Fraction) -> Fraction:
    root_num = isqrt(value.numerator)
    root_den = isqrt(value.denominator)
    if root_num * root_num != value.numerator or root_den * root_den != value.denominator:
        raise ValueError(f"not a rational square: {value}")
    return Fraction(root_num, root_den)


def _curve_add(
    point_p: tuple[Fraction, Fraction] | None,
    point_q: tuple[Fraction, Fraction] | None,
    *,
    a2: int,
    a4: int,
) -> tuple[Fraction, Fraction] | None:
    if point_p is None:
        return point_q
    if point_q is None:
        return point_p

    x1, y1 = point_p
    x2, y2 = point_q
    if x1 == x2 and y1 == -y2:
        return None
    if point_p == point_q:
        slope = (3 * x1 * x1 + 2 * a2 * x1 + a4) / (2 * y1)
    else:
        slope = (y2 - y1) / (x2 - x1)
    x3 = slope * slope - a2 - x1 - x2
    y3 = -(y1 + slope * (x3 - x1))
    return x3, y3


def _curve_neg(
    point: tuple[Fraction, Fraction] | None,
) -> tuple[Fraction, Fraction] | None:
    if point is None:
        return None
    return point[0], -point[1]


def _curve_mul(
    scalar: int,
    point: tuple[Fraction, Fraction],
    *,
    a2: int,
    a4: int,
) -> tuple[Fraction, Fraction] | None:
    if scalar < 0:
        return _curve_mul(-scalar, _curve_neg(point), a2=a2, a4=a4)
    result: tuple[Fraction, Fraction] | None = None
    addend: tuple[Fraction, Fraction] | None = point
    while scalar:
        if scalar & 1:
            result = _curve_add(result, addend, a2=a2, a4=a4)
        addend = _curve_add(addend, addend, a2=a2, a4=a4)
        scalar >>= 1
    return result


def _u7_w37_point_on_curve() -> tuple[Fraction, Fraction]:
    generator = (Fraction(-304), Fraction(5376))
    torsion_translate = (Fraction(-592), Fraction(0))
    multiple = _curve_mul(-49, generator, a2=192, a4=-350464)
    point = _curve_add(multiple, torsion_translate, a2=192, a4=-350464)
    if point is None:
        raise ValueError("u7+w37 Mordell-Weil expression unexpectedly gave O")
    return point


def _u7_w37_point_on_cover() -> dict[str, str]:
    x_coord, y_coord = _u7_w37_point_on_curve()
    u_minus = _sqrt_fraction((x_coord + 192) / 7)
    u_pos = _sqrt_fraction((x_coord - 592) / 259)
    u_neg = _sqrt_fraction((x_coord + 592) / 37)
    if 259 * u_minus * u_pos * u_neg != y_coord:
        raise ValueError("u7+w37 cover product does not induce the E_L point")
    return {
        "X": _format_fraction(x_coord),
        "u_minus_p": _format_fraction(u_minus),
        "u_pos_2sqrt_q": _format_fraction(u_pos),
        "u_neg_2sqrt_q": _format_fraction(u_neg),
    }


def _w5_refutation_certificate() -> dict[str, Any]:
    lift_checks = [
        {
            "torsion_point": "O",
            "lift_exists": False,
            "checked_equation": (
                "at infinity: u_minus_p^2 = "
                "5*u_pos_2sqrt_q^2 = 5*u_neg_2sqrt_q^2"
            ),
            "blocking_reason": "5_is_not_a_rational_square",
        },
        {
            "torsion_point": "(-370,0)",
            "lift_exists": False,
            "checked_equation": "X - 114 = -484 = u_minus_p^2",
            "blocking_reason": "negative_rational_cannot_be_square",
        },
        {
            "torsion_point": "(114,0)",
            "lift_exists": False,
            "checked_equation": "X - 370 = -256 = 5*u_pos_2sqrt_q^2",
            "blocking_reason": "negative_rational_cannot_be_square",
        },
        {
            "torsion_point": "(370,0)",
            "lift_exists": False,
            "checked_equation": "X + 370 = 740 = 5*u_neg_2sqrt_q^2",
            "blocking_reason": "148_is_not_a_rational_square",
        },
    ]
    return {
        "status": "globally_not_soluble",
        "certificate_type": "targeted_mordell_weil_torsion_lift_refutation",
        "certificate_scope": (
            "The two w_5 wl505 deferred entries have the same instantiated "
            "ambient C_d cover with L=4,T=11,d=(1,5,5). This certificate is "
            "for that single cover only; it is not a family Selmer or "
            "rank-zero theorem."
        ),
        "cover_equations": [
            "X - 114 = u_minus_p^2",
            "X - 370 = 5*u_pos_2sqrt_q^2",
            "X + 370 = 5*u_neg_2sqrt_q^2",
        ],
        "elliptic_curve_model": {
            "equation": "V^2 = (X - 114)*(X - 370)*(X + 370)",
            "expanded_equation": "V^2 = X^3 - 114*X^2 - 136900*X + 15606600",
        },
        "cover_to_elliptic_curve_map": {
            "X": "same X-coordinate",
            "V": "5*u_minus_p*u_pos_2sqrt_q*u_neg_2sqrt_q",
            "reason": (
                "The product of the three cover equations is "
                "V^2=(X-114)(X-370)(X+370)."
            ),
        },
        "rank_zero_certificate": {
            "rank": 0,
            "torsion_points": ["O", "(-370,0)", "(114,0)", "(370,0)"],
            "scope": "single instantiated curve E_{L=4,T=11}, not a family theorem",
        },
        "cover_lift_checks": lift_checks,
        "cover_lift_summary": {
            "torsion_point_count_checked": len(lift_checks),
            "torsion_lift_count": len(
                [check for check in lift_checks if check["lift_exists"]]
            ),
            "point_at_infinity_lift_exists": False,
            "affine_torsion_lift_count": 0,
        },
        "conclusion": (
            "Since the recorded Mordell-Weil certificate gives only the listed "
            "torsion points on E_{L=4,T=11}, and none lifts to the d=(1,5,5) "
            "cover, the instantiated ambient C_d cover has no rational point."
        ),
    }


def _u7_w37_solubility_certificate() -> dict[str, Any]:
    point_on_cover = _u7_w37_point_on_cover()
    x_coord = Fraction(point_on_cover["X"])
    u_minus = Fraction(point_on_cover["u_minus_p"])
    u_pos = Fraction(point_on_cover["u_pos_2sqrt_q"])
    u_neg = Fraction(point_on_cover["u_neg_2sqrt_q"])
    y_coord = 259 * u_minus * u_pos * u_neg
    return {
        "status": "globally_soluble",
        "certificate_type": "targeted_mordell_weil_cover_lift_certificate",
        "certificate_scope": (
            "The two u_7+w_37 wl505 deferred entries have the same "
            "instantiated ambient C_d cover with L=7,T=10,d=(7,259,37). "
            "This is a single-cover global-solubility certificate, not a "
            "family Selmer or rank theorem."
        ),
        "cover_equations": [
            "X + 192 = 7*u_minus_p^2",
            "X - 592 = 259*u_pos_2sqrt_q^2",
            "X + 592 = 37*u_neg_2sqrt_q^2",
        ],
        "elliptic_curve_model": {
            "equation": "V^2 = (X + 192)*(X - 592)*(X + 592)",
            "expanded_equation": "V^2 = X^3 + 192*X^2 - 350464*X - 67289088",
        },
        "cover_to_elliptic_curve_map": {
            "X": "same X-coordinate",
            "V": "259*u_minus_p*u_pos_2sqrt_q*u_neg_2sqrt_q",
            "reason": (
                "The product of the three cover equations is "
                "V^2=(X+192)(X-592)(X+592)."
            ),
        },
        "mordell_weil_point_source": {
            "curve_generator": "G=(-304,5376)",
            "torsion_translate": "T=(-592,0)",
            "point_expression": "-49*G + T",
            "curve_rank_scope": (
                "single instantiated curve E_{L=7,T=10}, not a family theorem"
            ),
        },
        "point_on_cover": point_on_cover,
        "equation_checks": [
            {
                "equation": "X + 192 = 7*u_minus_p^2",
                "passed": x_coord + 192 == 7 * u_minus * u_minus,
            },
            {
                "equation": "X - 592 = 259*u_pos_2sqrt_q^2",
                "passed": x_coord - 592 == 259 * u_pos * u_pos,
            },
            {
                "equation": "X + 592 = 37*u_neg_2sqrt_q^2",
                "passed": x_coord + 592 == 37 * u_neg * u_neg,
            },
        ],
        "induced_point_on_E_L": {
            "X": _format_fraction(x_coord),
            "Y": _format_fraction(y_coord),
        },
        "cover_lift_summary": {
            "cover_equation_count_checked": 3,
            "cover_equations_all_satisfied": True,
            "point_on_E_L_matches_cover_product": True,
        },
    }


def _not_applied_filter_result() -> dict[str, Any]:
    return {
        "output_class": "not_applied",
        "reason": "ambient_C_d_global_solubility_refuted",
        "blocking_reasons": ["ambient_C_d_has_no_rational_point"],
    }


def _refuted_routing_state() -> dict[str, Any]:
    return {
        "ambient_c_d_global_solubility_status": "globally_not_soluble",
        "aa_bb_admissibility_status": (
            "not_applied_ambient_global_solubility_refuted"
        ),
        "ledger_route": "ambient_c_d_global_solubility_refuted_ledger",
        "blocking_reasons": ["ambient_C_d_has_no_rational_point"],
    }


def _point_for_wl491(
    *, entry: dict[str, Any], certificate: dict[str, Any]
) -> dict[str, Any]:
    sample = entry["sample"]
    point_on_e = certificate["induced_point_on_E_L"]
    return {
        "candidate_id": entry["candidate_id"],
        "quotient": sample["side"],
        "A": sample["A"],
        "B": sample["B"],
        "L": sample["L"],
        "point_on_E_L": {
            "X": point_on_e["X"],
            "Y": point_on_e["Y"],
        },
        "parameters": dict(entry["complete_c_d_cover"]["parameters"]),
        "complete_d_squareclass": dict(entry["complete_c_d_cover"]["d_vector"]),
        "route_context": {
            "ambient_global_C_d_solubility_already_established": True,
            "old_package_x_S_tilde_bridge_not_used": True,
        },
    }


def _soluble_routing_state(filter_result: dict[str, Any]) -> dict[str, Any]:
    return {
        "ambient_c_d_global_solubility_status": "globally_soluble",
        "aa_bb_admissibility_status": filter_result["output_class"],
        "ledger_route": filter_result["ledger_route"],
        "blocking_reasons": list(filter_result.get("blocking_reasons", [])),
    }


def _target_deferred_entries(wl505: dict[str, Any]) -> list[dict[str, Any]]:
    entries = [
        entry
        for entry in wl505.get("routed_active_shell7_supports", [])
        if entry.get("candidate_id") in TARGET_DEFERRED_IDS
    ]
    return sorted(entries, key=lambda entry: TARGET_DEFERRED_IDS.index(entry["candidate_id"]))


def _is_w5_target(entry: dict[str, Any]) -> bool:
    return (
        entry.get("candidate_id") in REFUTED_W5_IDS
        and entry.get("candidate_support") == ["w_5"]
        and entry.get("complete_c_d_cover", {}).get("d_vector") == W5_D_VECTOR
        and entry.get("complete_c_d_cover", {}).get("parameters") == W5_PARAMETERS
        and entry.get("ambient_c_d_global_solubility", {}).get("status")
        == "global_solubility_deferred"
        and entry.get("wl491_filter_result", {}).get("output_class") == "not_applied"
    )


def _is_u7_w37_target(entry: dict[str, Any]) -> bool:
    return (
        entry.get("candidate_id") in SOLUBLE_U7_W37_IDS
        and entry.get("candidate_support") == ["u_7", "w_37"]
        and entry.get("complete_c_d_cover", {}).get("d_vector") == U7_W37_D_VECTOR
        and entry.get("complete_c_d_cover", {}).get("parameters") == U7_W37_PARAMETERS
        and entry.get("ambient_c_d_global_solubility", {}).get("status")
        == "global_solubility_deferred"
        and entry.get("wl491_filter_result", {}).get("output_class") == "not_applied"
    )


def _resolved_entry(entry: dict[str, Any]) -> dict[str, Any]:
    base = {
        "route_rank": entry["route_rank"],
        "candidate_id": entry["candidate_id"],
        "candidate_support": list(entry["candidate_support"]),
        "source_wl505_routing_state": dict(entry["routing_state"]),
        "sample": dict(entry["sample"]),
        "complete_c_d_cover": dict(entry["complete_c_d_cover"]),
    }
    if entry["candidate_id"] in REFUTED_W5_IDS:
        return {
            **base,
            "ambient_c_d_global_solubility": _w5_refutation_certificate(),
            "wl491_filter_input": {},
            "wl491_filter_result": _not_applied_filter_result(),
            "routing_state": _refuted_routing_state(),
        }

    certificate = _u7_w37_solubility_certificate()
    filter_input = _point_for_wl491(entry=entry, certificate=certificate)
    filter_result = classify_ambient_c_d_point_for_aa_bb_admissibility(filter_input)
    return {
        **base,
        "ambient_c_d_global_solubility": certificate,
        "wl491_filter_input": filter_input,
        "wl491_filter_result": filter_result,
        "routing_state": _soluble_routing_state(filter_result),
    }


def _resolution_summary(entries: list[dict[str, Any]]) -> dict[str, int]:
    witness_statuses = [
        entry["ambient_c_d_global_solubility"]["status"] for entry in entries
    ]
    filter_classes = [entry["wl491_filter_result"]["output_class"] for entry in entries]
    return {
        "wl505_deferred_entry_count": len(entries),
        "explicitly_classified_entry_count": len(entries),
        "ambient_globally_soluble_count": witness_statuses.count("globally_soluble"),
        "ambient_global_solubility_refuted_count": witness_statuses.count(
            "globally_not_soluble"
        ),
        "ambient_global_solubility_still_deferred_count": witness_statuses.count(
            "global_solubility_deferred"
        ),
        "wl491_filter_applied_count": len(
            [output for output in filter_classes if output != "not_applied"]
        ),
        "aa_bb_admissible_count": filter_classes.count("admissible"),
        "aa_bb_not_admissible_count": filter_classes.count("not_admissible"),
        "aa_bb_missing_pullback_data_count": filter_classes.count(
            "missing_pullback_data"
        ),
        "aa_bb_filter_not_applied_count": filter_classes.count("not_applied"),
    }


def build_wl506_resolve_shell7_deferred_ambient_c_d_global_solubility_ledgers(
    *,
    wl491: dict[str, Any],
    wl505: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl491_ready(wl491):
        violations.append("wl491_input_not_ready_or_not_scoped")
    if not _wl505_ready(wl505):
        violations.append("wl505_input_not_ready_or_not_scoped")

    target_entries = _target_deferred_entries(wl505)
    if [entry.get("candidate_id") for entry in target_entries] != TARGET_DEFERRED_IDS:
        violations.append("wl505_target_deferred_entries_missing_or_out_of_order")
    if any(
        not (_is_w5_target(entry) or _is_u7_w37_target(entry))
        for entry in target_entries
    ):
        violations.append("wl505_target_deferred_entries_not_matching_expected_covers")
    if (
        wl505.get("processed_exclusions_not_reopened")
        != PROCESSED_U3_EXCLUSION_IDS
    ):
        violations.append("wl505_processed_u3_exclusions_not_preserved")

    status = "ok" if not violations else "issues"
    resolved = [_resolved_entry(entry) for entry in target_entries] if status == "ok" else []

    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl505 deferred shell-7 ambient C_d global-solubility ledgers",
        "pattern": "AA+BB",
        "lemma_id": (
            "WL506_resolve_shell7_deferred_ambient_C_d_global_solubility_ledgers"
        ),
        "work_log": "wl506",
        "input_work_logs": ["wl491", "wl505"],
        "target_deferred_candidate_ids": list(TARGET_DEFERRED_IDS),
        "do_not_reopen_candidate_ids": {
            "shell7_globally_soluble_not_admissible_from_wl505": [
                entry["candidate_id"]
                for entry in wl505.get("routed_active_shell7_supports", [])
                if entry.get("ambient_c_d_global_solubility", {}).get("status")
                == "globally_soluble"
            ],
            "shell7_processed_u3_exclusions_from_wl505": list(
                wl505.get("processed_exclusions_not_reopened", [])
            ),
        },
        "shell7_globally_soluble_not_admissible_reopened_count": 0,
        "shell7_processed_u3_exclusions_reopened_count": 0,
        "resolution_method": {
            "kind": "targeted_single_cover_certificates",
            "w5_cover": "L=4,T=11,d=(1,5,5) refuted by torsion-lift certificate",
            "u7_w37_cover": (
                "L=7,T=10,d=(7,259,37) solved by an exact "
                "Mordell-Weil cover-lift point"
            ),
            "wl491_filter_policy": (
                "applied only to entries with ambient C_d global solubility "
                "established here"
            ),
            "new_local_row_added": False,
            "broad_family_rank_or_selmer_diagnostic": False,
        },
        "resolution_summary": _resolution_summary(resolved),
        "resolved_deferred_entries": resolved,
        "resolved_wl505_deferred_ledgers_here": status == "ok",
        "all_wl505_deferred_entries_resolved_here": (
            status == "ok"
            and len(resolved) == len(TARGET_DEFERRED_IDS)
            and all(
                entry["ambient_c_d_global_solubility"]["status"]
                != "global_solubility_deferred"
                for entry in resolved
            )
        ),
        "candidate_selected_here": False,
        "new_m_tail_or_kernel_candidate_selected_here": False,
        "new_m_tail_row_proved_here": False,
        "new_local_row_proved_here": False,
        "targeted_single_cover_mordell_weil_certificate_used_here": status == "ok",
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
        "advance_to_wl507": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "wl506 closes the four wl505 deferred ambient C_d ledgers, but does "
            "not select a final obstruction candidate, prove a local row, run "
            "theorem-level Selmer diagnostics, or choose the next roadmap step."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl491", type=Path, required=True)
    parser.add_argument("--wl505", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl506_resolve_shell7_deferred_ambient_c_d_global_solubility_ledgers(
        wl491=load_json(args.wl491),
        wl505=load_json(args.wl505),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl506 shell7 deferred-ledger resolution audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(
        "ambient_globally_soluble_count="
        f"{audit['resolution_summary']['ambient_globally_soluble_count']}"
    )
    print(
        "ambient_global_solubility_refuted_count="
        f"{audit['resolution_summary']['ambient_global_solubility_refuted_count']}"
    )
    print(f"advance_to_wl507={audit['advance_to_wl507']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
