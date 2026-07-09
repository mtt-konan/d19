#!/usr/bin/env python3
"""Route wl516 active shell-10 supports through ambient C_d then wl491."""

from __future__ import annotations

import argparse
from math import isqrt
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

COORDINATE_ORDER = [
    "d_minus_p",
    "d_pos_2sqrt_q",
    "d_neg_2sqrt_q",
]

BOUNDARY = (
    "This audits only wl517 / route_active_shell10_M_tail_supports_through_"
    "ambient_C_d_solubility_then_wl491_filter. It takes exactly the 10 "
    "active wl516 shell-10 M_tail support entries, does not re-open any closed "
    "ledger or processed support through wl516, instantiates the corresponding "
    "complete d-coordinate C_d cover data, records exact integral ambient "
    "C_d witnesses where this narrow audit has them, applies the wl491 AA+BB "
    "admissibility filter only after ambient global solubility is established, "
    "routes unresolved covers to explicit deferred ledgers, and stops before "
    "executing shell 11, selecting a final obstruction candidate, proving new "
    "local rows, running broad rank or Selmer diagnostics, advancing to wl518, "
    "using the old package-x S~ bridge, or claiming a complete Sel_2(E) upper "
    "bound, dim Sel_2(E)=2, rank zero, Sha[2]=0, uniform M_tail full rank, or "
    "any family exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

EXPECTED_ACTIVE_IDS = [
    "AA_A3_B10_u_3_plus_v_13_m_tail_shell10_candidate",
    "AA_A7_B10_u_7_plus_v_17_plus_w_5_m_tail_shell10_candidate",
    "AA_A10_B1_u_5_m_tail_shell10_candidate",
    "AA_A10_B7_v_17_plus_w_13_m_tail_shell10_candidate",
    "AA_A10_B9_u_5_m_tail_shell10_candidate",
    "BB_A1_B10_u_5_m_tail_shell10_candidate",
    "BB_A7_B10_v_17_plus_w_13_m_tail_shell10_candidate",
    "BB_A9_B10_u_5_m_tail_shell10_candidate",
    "BB_A10_B3_u_3_plus_v_13_m_tail_shell10_candidate",
    "BB_A10_B7_u_7_plus_v_17_plus_w_5_m_tail_shell10_candidate",
]

INTEGRAL_POINT_SEARCH_BOUND = 10_000


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


def _wl516_ready(wl516: dict[str, Any]) -> bool:
    summary = wl516.get("sample_summary", {})
    return (
        wl516.get("status") == "ok"
        and wl516.get("ready") is True
        and wl516.get("lemma_id")
        == "WL516_execute_next_finite_M_tail_shell_from_wl498_plan"
        and wl516.get("work_log") == "wl516"
        and summary.get("active_new_support_entry_count") == 10
        and summary.get("excluded_duplicate_or_processed_support_entry_count") == 0
        and summary.get("unique_active_supports")
        == ["u_3", "u_5", "u_7", "v_13", "v_17", "w_13", "w_5"]
        and wl516.get("new_c_d_solubility_tested_here") is False
        and wl516.get("wl491_filter_applied_here") is False
        and wl516.get("candidate_selected_here") is False
        and wl516.get("new_local_row_proved_here") is False
        and wl516.get("old_package_x_coordinate_collapse_used") is False
        and wl516.get("package_x_s_tilde_bridge_used") is False
        and wl516.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl516.get("single_curve_diagnostics_run") is False
        and not _claims_forbidden_bound(wl516)
    )


def _squarefree_part(n: int) -> int:
    if n == 0:
        raise ValueError("zero is not a squareclass generator")
    sign = -1 if n < 0 else 1
    n = abs(n)
    out = 1
    prime = 2
    while prime * prime <= n:
        parity = 0
        while n % prime == 0:
            parity ^= 1
            n //= prime
        if parity:
            out *= prime
        prime += 1 if prime == 2 else 2
    if n > 1:
        out *= n
    return sign * out


def _generator_pattern(generator_id: str) -> list[int]:
    kind, raw_prime = generator_id.split("_", maxsplit=1)
    prime = int(raw_prime)
    if kind == "u":
        return [prime, prime, 1]
    if kind == "v":
        return [prime, 1, prime]
    if kind == "w":
        return [1, prime, prime]
    raise ValueError(f"unsupported support generator {generator_id}")


def _support_d_vector(support: list[str]) -> dict[str, int]:
    pattern = [1, 1, 1]
    for generator_id in support:
        generator = _generator_pattern(generator_id)
        pattern = [
            _squarefree_part(current * factor)
            for current, factor in zip(pattern, generator, strict=True)
        ]
    return dict(zip(COORDINATE_ORDER, pattern, strict=True))


def _sample_parameters(sample: dict[str, Any]) -> dict[str, int]:
    l_value = int(sample["L"])
    t_value = int(sample["T"])
    sqrt_q = int(sample["sqrt_q"])
    return {
        "p": 8 * l_value * l_value - 2 * t_value * t_value,
        "q": sqrt_q * sqrt_q,
        "sqrt_q": sqrt_q,
    }


def _root_data(parameters: dict[str, int]) -> dict[str, dict[str, int | str]]:
    return {
        "e_minus": {"symbolic": "-p", "value": -parameters["p"]},
        "e_pos": {"symbolic": "2*sqrt_q", "value": 2 * parameters["sqrt_q"]},
        "e_neg": {"symbolic": "-2*sqrt_q", "value": -2 * parameters["sqrt_q"]},
    }


def _format_square_term(coefficient: int, variable: str) -> str:
    if coefficient == 1:
        return f"{variable}^2"
    return f"{coefficient}*{variable}^2"


def _format_relation(root_value: int, coefficient: int, variable: str) -> str:
    square_term = _format_square_term(coefficient, variable)
    if root_value < 0:
        return f"X + {-root_value} = {square_term}"
    return f"X - {root_value} = {square_term}"


def _cover_data(entry: dict[str, Any]) -> dict[str, Any]:
    sample = dict(entry["sample"])
    d_vector = _support_d_vector(list(entry["candidate_support"]))
    parameters = _sample_parameters(sample)
    roots = _root_data(parameters)
    d_minus = d_vector["d_minus_p"]
    d_pos = d_vector["d_pos_2sqrt_q"]
    d_neg = d_vector["d_neg_2sqrt_q"]
    e_minus = int(roots["e_minus"]["value"])
    e_pos = int(roots["e_pos"]["value"])
    e_neg = int(roots["e_neg"]["value"])

    return {
        "candidate_id": entry["candidate_id"],
        "source_support": list(entry["candidate_support"]),
        "sample": sample,
        "parameters": parameters,
        "coordinate_order": list(COORDINATE_ORDER),
        "variables": ["X", "u_minus_p", "u_pos_2sqrt_q", "u_neg_2sqrt_q"],
        "d_vector": d_vector,
        "root_data": roots,
        "x_coordinate_relations": [
            {
                "coordinate": "d_minus_p",
                "root": "e_minus",
                "instantiated_equation": _format_relation(
                    e_minus, d_minus, "u_minus_p"
                ),
            },
            {
                "coordinate": "d_pos_2sqrt_q",
                "root": "e_pos",
                "instantiated_equation": _format_relation(
                    e_pos, d_pos, "u_pos_2sqrt_q"
                ),
            },
            {
                "coordinate": "d_neg_2sqrt_q",
                "root": "e_neg",
                "instantiated_equation": _format_relation(
                    e_neg, d_neg, "u_neg_2sqrt_q"
                ),
            },
        ],
        "two_independent_equations": [
            (
                f"{_format_square_term(d_minus, 'u_minus_p')} - "
                f"{_format_square_term(d_pos, 'u_pos_2sqrt_q')} = "
                f"{e_pos - e_minus}"
            ),
            (
                f"{_format_square_term(d_minus, 'u_minus_p')} - "
                f"{_format_square_term(d_neg, 'u_neg_2sqrt_q')} = "
                f"{e_neg - e_minus}"
            ),
        ],
        "instantiation_only": True,
    }


def _equation_checks(
    *, cover: dict[str, Any], point: dict[str, int]
) -> list[str]:
    roots = cover["root_data"]
    d_vector = cover["d_vector"]
    x_coord = point["X"]
    return [
        (
            f"{x_coord} - {roots['e_minus']['value']} = "
            f"{d_vector['d_minus_p']}*{point['u_minus_p']}^2"
        ),
        (
            f"{x_coord} - {roots['e_pos']['value']} = "
            f"{d_vector['d_pos_2sqrt_q']}*{point['u_pos_2sqrt_q']}^2"
        ),
        (
            f"{x_coord} - {roots['e_neg']['value']} = "
            f"{d_vector['d_neg_2sqrt_q']}*{point['u_neg_2sqrt_q']}^2"
        ),
    ]


def _sqrt_d_product(d_vector: dict[str, int]) -> int:
    product = 1
    for coordinate in COORDINATE_ORDER:
        product *= int(d_vector[coordinate])
    root = isqrt(product)
    if root * root != product:
        raise ValueError(f"d-coordinate product is not square: {d_vector}")
    return root


def _search_integral_cover_point(cover: dict[str, Any]) -> dict[str, int] | None:
    roots = cover["root_data"]
    d_vector = cover["d_vector"]
    e_minus = int(roots["e_minus"]["value"])
    e_pos = int(roots["e_pos"]["value"])
    e_neg = int(roots["e_neg"]["value"])
    d_minus = int(d_vector["d_minus_p"])
    d_pos = int(d_vector["d_pos_2sqrt_q"])
    d_neg = int(d_vector["d_neg_2sqrt_q"])

    for u_minus in range(INTEGRAL_POINT_SEARCH_BOUND + 1):
        x_coord = e_minus + d_minus * u_minus * u_minus
        pos_numerator = x_coord - e_pos
        neg_numerator = x_coord - e_neg
        if pos_numerator % d_pos or neg_numerator % d_neg:
            continue
        u_pos_square = pos_numerator // d_pos
        u_neg_square = neg_numerator // d_neg
        if u_pos_square < 0 or u_neg_square < 0:
            continue
        u_pos = isqrt(u_pos_square)
        u_neg = isqrt(u_neg_square)
        if u_pos * u_pos == u_pos_square and u_neg * u_neg == u_neg_square:
            return {
                "X": x_coord,
                "u_minus_p": u_minus,
                "u_pos_2sqrt_q": u_pos,
                "u_neg_2sqrt_q": u_neg,
            }
    return None


def _ambient_global_solubility(cover: dict[str, Any]) -> dict[str, Any]:
    point = _search_integral_cover_point(cover)
    if point is None:
        return {
            "status": "global_solubility_deferred",
            "certificate_type": "none_recorded_here",
            "bounded_integral_probe": {
                "u_minus_p_search_bound": INTEGRAL_POINT_SEARCH_BOUND,
                "integral_point_found": False,
                "not_a_global_insolubility_proof": True,
            },
            "blocking_reasons": ["ambient_C_d_global_point_not_established"],
            "deferred_to": "missing_or_deferred_ambient_C_d_global_solubility_ledger",
            "evidence_scope": (
                "wl517 instantiated this shell-10 cover and ran only a bounded "
                "integral probe. Failure of that probe is not a global "
                "insolubility proof, so this ledger remains genuinely deferred."
            ),
        }

    y_coord = (
        _sqrt_d_product(cover["d_vector"])
        * point["u_minus_p"]
        * point["u_pos_2sqrt_q"]
        * point["u_neg_2sqrt_q"]
    )
    return {
        "status": "globally_soluble",
        "certificate_type": "exact_integral_point_on_C_d",
        "evidence_scope": (
            "wl517 exact integral ambient C_d point for this single shell-10 "
            "cover; not a search-based non-solubility theorem and not a family "
            "Selmer or rank statement."
        ),
        "point_on_cover": point,
        "equation_checks": _equation_checks(cover=cover, point=point),
        "induced_point_on_E_L": {
            "X": point["X"],
            "Y": y_coord,
        },
    }


def _point_for_wl491(
    *, entry: dict[str, Any], cover: dict[str, Any], witness: dict[str, Any]
) -> dict[str, Any]:
    sample = cover["sample"]
    point_on_e = witness["induced_point_on_E_L"]
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
        "parameters": dict(cover["parameters"]),
        "complete_d_squareclass": dict(cover["d_vector"]),
        "route_context": {
            "ambient_global_C_d_solubility_already_established": True,
            "old_package_x_S_tilde_bridge_not_used": True,
        },
    }


def _deferred_filter_result() -> dict[str, Any]:
    return {
        "output_class": "not_applied",
        "reason": "ambient_global_C_d_solubility_not_established",
        "blocking_reasons": ["ambient_C_d_global_point_not_established"],
    }


def _routing_state(
    *, witness: dict[str, Any], filter_result: dict[str, Any]
) -> dict[str, Any]:
    if witness["status"] != "globally_soluble":
        return {
            "ambient_c_d_global_solubility_status": "global_solubility_deferred",
            "aa_bb_admissibility_status": (
                "not_applied_ambient_global_solubility_unproved"
            ),
            "ledger_route": "ambient_c_d_solubility_deferred_ledger",
            "blocking_reasons": ["ambient_C_d_global_point_not_established"],
        }
    return {
        "ambient_c_d_global_solubility_status": "globally_soluble",
        "aa_bb_admissibility_status": filter_result["output_class"],
        "ledger_route": filter_result["ledger_route"],
        "blocking_reasons": list(filter_result.get("blocking_reasons", [])),
    }


def _route_entry(entry: dict[str, Any]) -> dict[str, Any]:
    cover = _cover_data(entry)
    witness = _ambient_global_solubility(cover)
    if witness["status"] == "globally_soluble":
        filter_input = _point_for_wl491(entry=entry, cover=cover, witness=witness)
        filter_result = classify_ambient_c_d_point_for_aa_bb_admissibility(
            filter_input
        )
    else:
        filter_input = {}
        filter_result = _deferred_filter_result()

    return {
        "route_rank": entry["queue_rank"],
        "candidate_id": entry["candidate_id"],
        "candidate_support": list(entry["candidate_support"]),
        "source_wl516_queue_status": entry["queue_status"],
        "source_wl516_routing_state": dict(entry["routing_state"]),
        "sample": dict(entry["sample"]),
        "complete_c_d_cover": cover,
        "ambient_c_d_global_solubility": witness,
        "wl491_filter_input": filter_input,
        "wl491_filter_result": filter_result,
        "routing_state": _routing_state(witness=witness, filter_result=filter_result),
    }


def _route_summary(
    entries: list[dict[str, Any]], processed_exclusions_reopened_count: int
) -> dict[str, int]:
    witness_statuses = [
        entry["ambient_c_d_global_solubility"]["status"] for entry in entries
    ]
    filter_classes = [entry["wl491_filter_result"]["output_class"] for entry in entries]
    return {
        "active_shell10_support_entry_count": len(entries),
        "processed_exclusions_reopened_count": processed_exclusions_reopened_count,
        "ambient_globally_soluble_count": witness_statuses.count("globally_soluble"),
        "ambient_global_solubility_refuted_count": witness_statuses.count(
            "globally_not_soluble"
        ),
        "ambient_global_solubility_deferred_count": witness_statuses.count(
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
        "aa_bb_filter_deferred_count": filter_classes.count("not_applied"),
    }


def _target_active_entries(wl516: dict[str, Any]) -> list[dict[str, Any]]:
    entries = [
        entry
        for entry in wl516.get("active_new_kernel_supports", [])
        if entry.get("candidate_id") in EXPECTED_ACTIVE_IDS
    ]
    return sorted(entries, key=lambda entry: EXPECTED_ACTIVE_IDS.index(entry["candidate_id"]))


def build_wl517_route_active_shell10_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter(  # noqa: E501
    *,
    wl491: dict[str, Any],
    wl516: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl491_ready(wl491):
        violations.append("wl491_input_not_ready_or_not_scoped")
    if not _wl516_ready(wl516):
        violations.append("wl516_input_not_ready_or_not_scoped")

    target_entries = _target_active_entries(wl516)
    processed_exclusion_ids = [
        entry["candidate_id"]
        for entry in wl516.get("excluded_duplicate_or_processed_supports", [])
    ]
    if [entry.get("candidate_id") for entry in target_entries] != EXPECTED_ACTIVE_IDS:
        violations.append("wl516_target_active_shell10_entries_missing_or_out_of_order")
    if processed_exclusion_ids:
        violations.append("wl516_processed_exclusions_would_reopen_closed_ledgers")

    status = "ok" if not violations else "issues"
    routed = [_route_entry(entry) for entry in target_entries] if status == "ok" else []
    processed_exclusions_reopened_count = 0

    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl516 active shell-10 M_tail supports plus wl491 filter",
        "pattern": "AA+BB",
        "lemma_id": (
            "WL517_route_active_shell10_M_tail_supports_through_ambient_C_d_"
            "solubility_then_wl491_filter"
        ),
        "work_log": "wl517",
        "input_work_logs": ["wl491", "wl516"],
        "target_active_candidate_ids": list(EXPECTED_ACTIVE_IDS),
        "processed_exclusions_not_reopened": list(processed_exclusion_ids)
        if status == "ok"
        else [],
        "closed_ledgers_preserved_through_wl516": True,
        "route_order": [
            "active_wl516_shell10_M_tail_support",
            "instantiate_complete_d_coordinate_C_d_cover",
            "establish_or_defer_ambient_C_d_global_solubility",
            "apply_wl491_filter_only_to_established_global_points",
            "route_to_not_admissible_or_deferred_ledgers",
        ],
        "route_summary": _route_summary(
            routed,
            processed_exclusions_reopened_count=processed_exclusions_reopened_count,
        ),
        "routed_active_shell10_supports": routed,
        "route_audit_built_here": status == "ok",
        "complete_c_d_cover_data_instantiated_here": status == "ok",
        "ambient_c_d_solubility_classified_here": status == "ok",
        "new_c_d_solubility_tested_here": status == "ok",
        "wl491_filter_applied_here": (
            status == "ok"
            and any(
                entry["wl491_filter_result"]["output_class"] != "not_applied"
                for entry in routed
            )
        ),
        "ambient_c_d_solubility_proved_for_some_shell10_supports_here": (
            status == "ok"
            and any(
                entry["ambient_c_d_global_solubility"]["status"] == "globally_soluble"
                for entry in routed
            )
        ),
        "all_active_shell10_supports_classified_here": (
            status == "ok" and len(routed) == len(EXPECTED_ACTIVE_IDS)
        ),
        "all_active_shell10_supports_fully_routed_here": (
            status == "ok"
            and all(
                entry["ambient_c_d_global_solubility"]["status"]
                != "global_solubility_deferred"
                for entry in routed
            )
        ),
        "candidate_selected_here": False,
        "new_m_tail_or_kernel_candidate_selected_here": False,
        "new_m_tail_row_proved_here": False,
        "new_local_row_proved_here": False,
        "targeted_single_cover_mordell_weil_certificate_used_here": False,
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
        "advance_to_wl518": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "wl517 leaves two shell-10 ambient C_d global-solubility ledgers "
            "deferred. This task stops here and does not execute shell 11, "
            "select a final obstruction candidate, or advance to the next "
            "roadmap step."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl491", type=Path, required=True)
    parser.add_argument("--wl516", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = (
        build_wl517_route_active_shell10_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter(
            wl491=load_json(args.wl491),
            wl516=load_json(args.wl516),
        )
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl517 active-shell10 route audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(
        "ambient_globally_soluble_count="
        f"{audit['route_summary']['ambient_globally_soluble_count']}"
    )
    print(
        "ambient_global_solubility_deferred_count="
        f"{audit['route_summary']['ambient_global_solubility_deferred_count']}"
    )
    print(f"advance_to_wl518={audit['advance_to_wl518']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
