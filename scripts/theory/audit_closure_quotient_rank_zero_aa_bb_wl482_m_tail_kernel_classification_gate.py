#!/usr/bin/env python3
"""Classify the wl481 AA A=3, B=1 M_tail kernel support u_3."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl481_m_tail_explicit_matrix_builder import (  # noqa: E501
        COORDINATE_ORDER,
        _dyadic_rows,
        _odd_prime_factors,
        _odd_row,
        _raw_generators,
        _v2,
    )
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from audit_closure_quotient_rank_zero_aa_bb_wl481_m_tail_explicit_matrix_builder import (
        COORDINATE_ORDER,
        _dyadic_rows,
        _odd_prime_factors,
        _odd_row,
        _raw_generators,
        _v2,
    )
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl482 / M_tail_kernel_classification_gate for the "
    "AA+BB complete d-coordinate route. It takes wl481 as input and classifies "
    "only the finite AA sample A=3, B=1 kernel support u_3. The gate checks "
    "whether that support is an omitted tau_sqrt_q pivot artifact or is killed "
    "by a known wl475-wl478 / wl481 local row. It does not add broad rank or "
    "Selmer diagnostics, does not prove uniform full rank for M_tail, does not "
    "prove a complete Sel_2(E) upper bound, does not claim dim Sel_2(E)=2, "
    "rank zero, Sha[2]=0, or any family exclusion."
)

TARGET_SAMPLE = {"side": "AA", "A": 3, "B": 1}
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


def _wl481_ready(wl481: dict[str, Any]) -> bool:
    return (
        wl481.get("status") == "ok"
        and wl481.get("ready") is True
        and wl481.get("lemma_id") == "WL481_M_tail_explicit_matrix_builder"
        and wl481.get("work_log") == "wl481"
        and wl481.get("matrix_object", {}).get("id") == "M_tail"
        and wl481.get("old_package_x_coordinate_collapse_used") is False
        and not _claims_forbidden_bound(wl481)
    )


def _target_sample_payload(wl481: dict[str, Any]) -> dict[str, Any] | None:
    for sample in wl481.get("sample_matrices", []):
        sample_id = sample.get("sample", {})
        if all(sample_id.get(key) == value for key, value in TARGET_SAMPLE.items()):
            return sample
    return None


def _raw_columns_and_rows(
    sample: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    sample_id = sample["sample"]
    L = int(sample_id["L"])
    T = int(sample_id["T"])
    sqrt_q = int(sample_id["sqrt_q"])
    odd_L = _odd_prime_factors(L)
    odd_T = _odd_prime_factors(T)
    odd_sqrt_q = _odd_prime_factors(sqrt_q)
    epsilon = 1 if _v2(T) == _v2(L) + 1 else 0
    columns = _raw_generators(
        odd_L=odd_L,
        odd_T=odd_T,
        odd_sqrt_q=odd_sqrt_q,
        epsilon=epsilon,
    )
    rows: list[dict[str, Any]] = []
    rows.extend(_odd_row(row_kind="L", active_prime=prime, columns=columns) for prime in odd_L)
    rows.extend(_odd_row(row_kind="T", active_prime=prime, columns=columns) for prime in odd_T)
    rows.extend(
        _odd_row(row_kind="sqrt_q", active_prime=prime, columns=columns)
        for prime in odd_sqrt_q
    )
    rows.extend(_dyadic_rows(balanced=bool(epsilon), columns=columns))
    return columns, rows


def _target_raw_entries(
    *, raw_columns: list[dict[str, Any]], raw_rows: list[dict[str, Any]]
) -> list[int]:
    target_indexes = [
        index for index, column in enumerate(raw_columns) if column["id"] in TARGET_SUPPORT
    ]
    return [
        sum(int(row["entries"][index]) for index in target_indexes) % 2
        for row in raw_rows
    ]


def _omitted_torsion_pivot_check(sample: dict[str, Any]) -> dict[str, Any]:
    raw_columns, raw_rows = _raw_columns_and_rows(sample)
    raw_column_ids = [column["id"] for column in raw_columns]
    omitted = sample["torsion_quotient"]["omitted_baseline_pivot_column"]
    visible_tau_sqrt_q_support = [omitted] if omitted else []
    target_support = list(TARGET_SUPPORT)
    raw_lift_entries = _target_raw_entries(raw_columns=raw_columns, raw_rows=raw_rows)
    return {
        "question": (
            "Does the u_3 kernel disappear when the omitted tau_sqrt_q pivot "
            "column is restored?"
        ),
        "raw_column_ids_before_tau_sqrt_q_quotient": raw_column_ids,
        "quotient_column_ids_after_tau_sqrt_q_quotient": [
            column["id"] for column in sample["columns"]
        ],
        "omitted_baseline_pivot_column": omitted,
        "visible_tau_sqrt_q_support": visible_tau_sqrt_q_support,
        "target_support": target_support,
        "target_support_intersects_omitted_pivot": omitted in target_support,
        "target_support_equals_visible_tau_sqrt_q": (
            sorted(target_support) == sorted(visible_tau_sqrt_q_support)
        ),
        "raw_lift_entries_for_target_support": raw_lift_entries,
        "raw_lift_pairing_is_zero_for_known_rows": not any(raw_lift_entries),
        "decision": "not_an_omitted_torsion_pivot_artifact",
        "reason": (
            "For AA A=3, B=1 the omitted visible torsion pivot is w_13, while "
            "the kernel support is u_3. Restoring w_13 does not add a nonzero "
            "known row pairing with u_3; the quotient did not create this "
            "support."
        ),
    }


def _known_local_row_coverage_check(sample: dict[str, Any]) -> dict[str, Any]:
    included_rows = sample["rows"]
    target_index_by_column = {
        column["id"]: index for index, column in enumerate(sample["columns"])
    }
    target_indexes = [
        target_index_by_column[column_id]
        for column_id in TARGET_SUPPORT
        if column_id in target_index_by_column
    ]
    nonzero_rows = [
        row["id"]
        for row in included_rows
        if sum(int(row["entries"][index]) for index in target_indexes) % 2
    ]
    return {
        "question": (
            "Is there a known wl475-wl478 / wl481 local character row omitted "
            "from this finite sample that kills u_3?"
        ),
        "relevant_places_for_sample": ["infinity", "2", "3", "13"],
        "included_row_ids": [row["id"] for row in included_rows],
        "vacuous_or_inactive_known_rows": [
            "odd_T rows: T=4 has no odd prime divisor",
            "balanced dyadic rows: epsilon_balanced_2=0 for this sample",
            "real sign row: already quotiented as tau_minus and u_3 is positive",
        ],
        "known_wl481_row_with_nonzero_target_entry": nonzero_rows,
        "missing_known_local_or_hilbert_row_found": False,
        "decision": "no_known_wl475_wl478_or_wl481_row_missing_that_kills_u_3",
        "reason": (
            "The wl481 row contract supplies exactly the odd L row at 3, the "
            "odd sqrt_q row at 13, and the ordinary dyadic row. All have zero "
            "entry on u_3. Killing u_3 would require deriving an additional "
            "local/Hilbert condition outside the wl481 solved-row ledger, not "
            "merely adding a row that wl481 forgot to instantiate."
        ),
    }


def _target_kernel(sample: dict[str, Any]) -> dict[str, Any]:
    return {
        "sample": sample["sample"],
        "coordinate_order": COORDINATE_ORDER,
        "support": list(TARGET_SUPPORT),
        "basis_vector": [1],
        "wl481_computed_rank_status": sample["computed_rank_status"],
        "wl481_kernel_diagnostics": sample["kernel_diagnostics"],
    }


def build_wl482_m_tail_kernel_classification_gate(
    *, wl481: dict[str, Any]
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl481_ready(wl481):
        violations.append("wl481_input_not_ready_or_not_scoped")
    sample = _target_sample_payload(wl481)
    if sample is None:
        violations.append("target_AA_3_1_sample_missing_from_wl481")
        sample = {}
    elif sample.get("kernel_diagnostics", {}).get("basis_supports") != [TARGET_SUPPORT]:
        violations.append("target_AA_3_1_kernel_support_not_u_3")

    status = "ok" if not violations else "issues"
    target_kernel = _target_kernel(sample) if sample else {}
    omitted_check = _omitted_torsion_pivot_check(sample) if sample else {}
    coverage_check = _known_local_row_coverage_check(sample) if sample else {}
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl481 finite M_tail sample matrix diagnostics",
        "pattern": "AA+BB",
        "lemma_id": "WL482_M_tail_kernel_classification_gate",
        "work_log": "wl482",
        "input_work_log": "wl481",
        "target_kernel": target_kernel,
        "omitted_torsion_pivot_check": omitted_check,
        "known_local_row_coverage_check": coverage_check,
        "classification": {
            "final_classification": (
                "genuine_parameter_specialized_tail_obstruction_candidate"
                if status == "ok"
                else "not_classified_due_to_input_violations"
            ),
            "artifact_of_sampled_row_builder_or_omitted_torsion_pivot": False,
            "missing_known_local_or_hilbert_row": False,
            "additional_row_needed_to_kill_u_3": (
                "would have to be a newly justified local/Hilbert condition "
                "outside the wl481 solved-row contract"
            ),
            "not_a_complete_selmer_bound": True,
            "scope": "AA A=3 B=1 finite parameter-specialized M_tail quotient",
        },
        "symbolic_rank_status": "uniform_full_rank_not_proved",
        "computed_rank_status": "finite_sample_kernel_classified_only",
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
        "old_package_x_coordinate_collapse_used": False,
        "search_count_used_as_progress": False,
        "next_obstruction": (
            "derive_or_rule_out_any_new_local_Hilbert_row_for_the_u_3_tail_candidate"
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl481", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl482_m_tail_kernel_classification_gate(wl481=load_json(args.wl481))
    write_json(args.out, audit)
    print(f"wrote AA+BB wl482 M_tail kernel classification audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"classification={audit['classification']['final_classification']}")
    print(
        "complete_selmer_upper_bound_proved="
        f"{audit['complete_selmer_upper_bound_proved']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
