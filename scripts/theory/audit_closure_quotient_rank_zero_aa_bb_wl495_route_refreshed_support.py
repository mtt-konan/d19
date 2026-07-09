#!/usr/bin/env python3
"""Route wl494 refreshed supports through ambient C_d solubility then wl491."""

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
    "This audits only wl495 / route_refreshed_support_through_ambient_C_d_"
    "solubility_then_wl491_filter. It takes the active wl494 refreshed v_5 "
    "M_tail support entries, instantiates the corresponding complete "
    "d-coordinate C_d cover data, records exact global C_d witnesses only "
    "where this narrow audit has them, applies the wl491 AA+BB admissibility "
    "filter only after ambient global solubility is established, routes "
    "unfinished entries to deferred ledgers, and stops before proving new "
    "local rows, running broad rank or Selmer diagnostics, selecting a final "
    "obstruction candidate, advancing to wl496, using the old package-x S~ "
    "bridge, or claiming a complete Sel_2(E) upper bound, dim Sel_2(E)=2, "
    "rank zero, Sha[2]=0, or any family exclusion."
)

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


def _wl494_ready(wl494: dict[str, Any]) -> bool:
    summary = wl494.get("sample_summary", {})
    return (
        wl494.get("status") == "ok"
        and wl494.get("ready") is True
        and wl494.get("lemma_id") == "WL494_extend_or_refresh_M_tail_diagnostics"
        and wl494.get("work_log") == "wl494"
        and wl494.get("diagnostic_refresh_built_here") is True
        and summary.get("active_new_support_entry_count") == 6
        and summary.get("unique_active_supports") == ["v_5"]
        and wl494.get("new_m_tail_row_proved_here") is False
        and wl494.get("ambient_c_d_solubility_proved_for_new_candidate_here")
        is False
        and wl494.get("aa_bb_admissibility_proved_for_new_candidate_here") is False
        and wl494.get("old_package_x_coordinate_collapse_used") is False
        and wl494.get("package_x_s_tilde_bridge_used") is False
        and wl494.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl494.get("single_curve_diagnostics_run") is False
        and not _claims_forbidden_bound(wl494)
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


def _format_relation(root_value: int, coefficient: int, variable: str) -> str:
    if root_value < 0:
        return f"X + {-root_value} = {coefficient}*{variable}^2"
    return f"X - {root_value} = {coefficient}*{variable}^2"


def _format_square_term(coefficient: int, variable: str) -> str:
    if coefficient == 1:
        return f"{variable}^2"
    return f"{coefficient}*{variable}^2"


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


def _exact_global_witness(cover: dict[str, Any]) -> dict[str, Any]:
    sample = cover["sample"]
    d_vector = cover["d_vector"]
    l_value = int(sample["L"])
    t_value = int(sample["T"])
    if (
        list(d_vector.values()) == [5, 1, 5]
        and t_value == 5
        and l_value in {1, 2}
    ):
        u_pos_square = 16 * (5 - l_value * l_value)
        u_pos = isqrt(u_pos_square)
        if u_pos * u_pos == u_pos_square:
            point = {
                "X": 130 - 8 * l_value * l_value,
                "u_minus_p": 4,
                "u_pos_2sqrt_q": u_pos,
                "u_neg_2sqrt_q": 6,
            }
            y_coord = 5 * point["u_minus_p"] * point["u_pos_2sqrt_q"] * point["u_neg_2sqrt_q"]
            return {
                "status": "globally_soluble",
                "certificate_type": "exact_integral_point_on_C_d",
                "evidence_scope": (
                    "wl495 exact witness for v_5, T=5, L in {1,2}; "
                    "not a search-based non-solubility theorem"
                ),
                "point_on_cover": point,
                "equation_checks": _equation_checks(cover=cover, point=point),
                "induced_point_on_E_L": {
                    "X": point["X"],
                    "Y": y_coord,
                },
            }
    return {
        "status": "global_solubility_deferred",
        "certificate_type": "none_recorded_here",
        "blocking_reasons": ["ambient_C_d_global_point_not_established"],
        "deferred_to": "missing_or_deferred_ambient_C_d_global_solubility_ledger",
        "evidence_scope": (
            "wl495 instantiated the cover but did not find or prove an exact "
            "ambient global C_d point for this entry; no global insolubility "
            "proof is claimed."
        ),
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
    witness = _exact_global_witness(cover)
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
        "source_wl494_queue_status": entry["queue_status"],
        "sample": dict(entry["sample"]),
        "complete_c_d_cover": cover,
        "ambient_c_d_global_solubility": witness,
        "wl491_filter_input": filter_input,
        "wl491_filter_result": filter_result,
        "routing_state": _routing_state(witness=witness, filter_result=filter_result),
    }


def _route_summary(entries: list[dict[str, Any]]) -> dict[str, int]:
    witness_statuses = [
        entry["ambient_c_d_global_solubility"]["status"] for entry in entries
    ]
    filter_classes = [entry["wl491_filter_result"]["output_class"] for entry in entries]
    return {
        "active_refreshed_support_entry_count": len(entries),
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


def build_wl495_route_refreshed_support_through_ambient_c_d_solubility_then_wl491_filter(
    *,
    wl491: dict[str, Any],
    wl494: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl491_ready(wl491):
        violations.append("wl491_input_not_ready_or_not_scoped")
    if not _wl494_ready(wl494):
        violations.append("wl494_input_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    routed = (
        [_route_entry(entry) for entry in wl494.get("active_new_kernel_supports", [])]
        if status == "ok"
        else []
    )

    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl494 active refreshed M_tail supports plus wl491 filter",
        "pattern": "AA+BB",
        "lemma_id": (
            "WL495_route_refreshed_support_through_ambient_C_d_solubility_then_wl491_filter"
        ),
        "work_log": "wl495",
        "input_work_logs": ["wl491", "wl494"],
        "route_order": [
            "refreshed_M_tail_support",
            "instantiate_complete_d_coordinate_C_d_cover",
            "establish_or_defer_ambient_C_d_global_solubility",
            "apply_wl491_filter_only_to_established_global_points",
            "route_to_not_admissible_or_deferred_ledgers",
        ],
        "route_summary": _route_summary(routed),
        "routed_refreshed_supports": routed,
        "route_audit_built_here": status == "ok",
        "complete_c_d_cover_data_instantiated_here": status == "ok",
        "ambient_c_d_solubility_proved_for_some_refreshed_supports_here": (
            status == "ok"
            and any(
                entry["ambient_c_d_global_solubility"]["status"] == "globally_soluble"
                for entry in routed
            )
        ),
        "all_refreshed_supports_fully_routed_here": (
            status == "ok"
            and all(
                entry["ambient_c_d_global_solubility"]["status"] == "globally_soluble"
                for entry in routed
            )
        ),
        "candidate_selected_here": False,
        "new_m_tail_or_kernel_candidate_selected_here": False,
        "new_m_tail_row_proved_here": False,
        "new_local_row_proved_here": False,
        "broad_rank_or_selmer_diagnostics_run": False,
        "single_curve_diagnostics_run": False,
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
        "old_package_x_coordinate_collapse_used": False,
        "package_x_s_tilde_bridge_used": False,
        "search_count_used_as_progress": False,
        "advance_to_wl496": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "Resolve the deferred ambient C_d global-solubility ledgers for "
            "AA_A4_B1 and BB_A1_B4 v_5, or otherwise prove an exact "
            "refutation/admissible route, before selecting any final "
            "obstruction candidate."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl491", type=Path, required=True)
    parser.add_argument("--wl494", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl495_route_refreshed_support_through_ambient_c_d_solubility_then_wl491_filter(
        wl491=load_json(args.wl491),
        wl494=load_json(args.wl494),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl495 refreshed-support route audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(
        "ambient_globally_soluble_count="
        f"{audit['route_summary']['ambient_globally_soluble_count']}"
    )
    print(f"advance_to_wl496={audit['advance_to_wl496']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
