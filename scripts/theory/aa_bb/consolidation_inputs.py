"""Materialize and validate the canonical wl500 A0/B0 input projections.

The materializer has the only code path that knows about the ignored
``results/`` payloads.  Runtime loaders read only the tracked canonical files
and never search for or fall back to legacy results.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from collections import Counter
from math import isqrt
from pathlib import Path
from typing import Any, NoReturn

SCHEMA_VERSION = 1
BASELINE_COMMIT = "9b73cd4"

D_VECTOR_KEYS = ("d_minus_p", "d_pos_2sqrt_q", "d_neg_2sqrt_q")
ROOT_VALUE_KEYS = ("e_minus", "e_pos", "e_neg")
COVER_POINT_KEYS = ("X", "u_minus_p", "u_pos_2sqrt_q", "u_neg_2sqrt_q")
E_POINT_KEYS = ("X", "Y")

CANONICAL_FILES = {
    "a0-ledger": "a0-ledger.v1.json",
    "a0-witnesses": "a0-witnesses.v1.json",
    "a0-taxonomy": "a0-taxonomy.v1.json",
    "a0-inventory": "a0-inventory.v1.json",
    "b0-prototype-rows": "b0-prototype-rows.v1.json",
    "manifest": "manifest.v1.json",
}

A1_CERTIFICATES_FILE = "a1-certificates.v1.json"

A1_SOURCE_FILENAMES = {
    "wl500": (
        "closure_quotient_rank_zero_aa_bb_wl500_route_active_u5_m_tail_supports_"
        "through_ambient_c_d_solubility_then_wl491_filter.json"
    ),
    "wl506": (
        "closure_quotient_rank_zero_aa_bb_wl506_resolve_shell7_deferred_ambient_"
        "c_d_global_solubility_ledgers.json"
    ),
    "wl511": (
        "closure_quotient_rank_zero_aa_bb_wl511_route_active_shell9_m_tail_"
        "supports_through_ambient_c_d_solubility_then_wl491_filter.json"
    ),
    "wl512": (
        "closure_quotient_rank_zero_aa_bb_wl512_resolve_shell9_deferred_ambient_"
        "c_d_global_solubility_ledgers.json"
    ),
    "wl514": (
        "closure_quotient_rank_zero_aa_bb_wl514_resolve_remaining_shell9_u7_"
        "ambient_c_d_global_solubility_ledger.json"
    ),
    "wl517": (
        "closure_quotient_rank_zero_aa_bb_wl517_route_active_shell10_m_tail_"
        "supports_through_ambient_c_d_solubility_then_wl491_filter.json"
    ),
    "wl519": (
        "closure_quotient_rank_zero_aa_bb_wl519_resolve_shared_shell10_u5_"
        "ambient_c_d_global_solubility_cover.json"
    ),
}

A2_SOURCE_SUFFIXES = {
    500: "route_active_u5_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter",
    501: "post_wl500_route_choice_audit",
    502: "execute_next_finite_m_tail_shell_from_wl498_plan",
    503: "post_wl502_empty_shell_route_choice_audit",
    504: "execute_next_finite_m_tail_shell_from_wl498_plan",
    505: "route_active_shell7_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter",
    506: "resolve_shell7_deferred_ambient_c_d_global_solubility_ledgers",
    507: "post_wl506_route_choice_audit",
    508: "execute_next_finite_m_tail_shell_from_wl498_plan",
    509: "post_wl508_empty_shell_route_choice_audit",
    510: "execute_next_finite_m_tail_shell_from_wl498_plan",
    511: "route_active_shell9_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter",
    512: "resolve_shell9_deferred_ambient_c_d_global_solubility_ledgers",
    513: "post_wl512_route_choice_audit",
    514: "resolve_remaining_shell9_u7_ambient_c_d_global_solubility_ledger",
    515: "post_wl514_route_choice_audit",
    516: "execute_next_finite_m_tail_shell_from_wl498_plan",
    517: "route_active_shell10_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter",
    518: "support_family_synthesis_after_wl517",
    519: "resolve_shared_shell10_u5_ambient_c_d_global_solubility_cover",
    520: "post_wl519_route_choice_audit",
    521: "support_family_synthesis_after_wl519",
    522: "support_cover_taxonomy_to_lemma_candidate_checkpoint",
    523: "try_common_source_square_obstruction_lemma_candidate",
    524: "post_wl523_route_choice_audit",
    525: "attempt_uniform_cover_family_squareclass_obstruction_lemma",
    526: "post_wl525_route_choice_audit",
    527: "function_field_squareclass_proof_data_scope",
}

A2_DESTINATIONS = {
    500: "A1-COVER", 501: "A1-BOUNDARY", 502: "A1-SHELL",
    503: "A1-BOUNDARY", 504: "A1-SHELL", 505: "A1-COVER",
    506: "A1-COVER", 507: "A1-BOUNDARY", 508: "A1-SHELL",
    509: "A1-BOUNDARY", 510: "A1-SHELL", 511: "A1-COVER",
    512: "A1-COVER", 513: "A1-BOUNDARY", 514: "A1-COVER",
    515: "A1-BOUNDARY", 516: "A1-SHELL", 517: "A1-COVER",
    518: "A2-TAX", 519: "A1-COVER", 520: "A2-BOUNDARY",
    521: "A2-TAX", 522: "A2-TAX", 523: "A2-LEMMA",
    524: "A2-BOUNDARY", 525: "A2-BOUNDARY", 526: "A2-BOUNDARY",
    527: "A2-SCOPE",
}

SOURCE_FILENAMES = {
    "wl495": "closure_quotient_rank_zero_aa_bb_wl495_route_refreshed_support.json",
    "wl505": (
        "closure_quotient_rank_zero_aa_bb_wl505_route_active_shell7_m_tail_supports_"
        "through_ambient_c_d_solubility_then_wl491_filter.json"
    ),
    "wl521": ("closure_quotient_rank_zero_aa_bb_wl521_support_family_synthesis_after_wl519.json"),
    "wl522": (
        "closure_quotient_rank_zero_aa_bb_wl522_support_cover_taxonomy_to_lemma_candidate_checkpoint.json"
    ),
    "wl527": (
        "closure_quotient_rank_zero_aa_bb_wl527_function_field_squareclass_proof_data_scope.json"
    ),
}

SOURCE_PROVENANCE = {
    "wl495": {
        "source_worklog_path": (
            "docs/work-logs/archive/495-aa-bb-route-refreshed-support-through-"
            "ambient-c-d-solubility-then-wl491-filter.md"
        ),
        "source_script_path": (
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl495_route_refreshed_support.py"
        ),
        "source_test_paths": [
            "tests/test_closure_quotient_rank_zero_aa_bb_wl495_route_refreshed_support.py"
        ],
        "source_selector": (
            "$.routed_refreshed_supports[*] where candidate_id in "
            "[AA_A1_B4_v_5_m_tail_refresh_candidate, "
            "BB_A4_B1_v_5_m_tail_refresh_candidate]"
        ),
        "consumer_paths": [
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl528_"
            "v5_l1_t5_function_field_prototype.py",
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl529_v5_l1_t5_square_locus.py",
            "scripts/theory/aa_bb/consolidation_inputs.py",
        ],
        "source_result_path": (
            "results/closure_quotient_rank_zero_aa_bb_wl495_route_refreshed_support.json"
        ),
        "source_payload_sha256": "72f54c9b1f59c5865a755dba4f4698f262c05c79f3022fdd4b4fdae9c6fcbfbd",
        "source_payload_size": 33475,
    },
    "wl505": {
        "source_worklog_path": (
            "docs/work-logs/archive/505-route-active-shell7-m-tail-supports-"
            "through-ambient-c-d-solubility-then-wl491-filter.md"
        ),
        "source_script_path": (
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl505_"
            "route_active_shell7_m_tail_supports_through_ambient_c_d_solubility_"
            "then_wl491_filter.py"
        ),
        "source_test_paths": [
            "tests/test_closure_quotient_rank_zero_aa_bb_wl505_"
            "route_active_shell7_m_tail_supports.py"
        ],
        "source_selector": (
            "$.routed_active_shell7_supports[*] where "
            "ambient_c_d_global_solubility.status == globally_soluble"
        ),
        "consumer_paths": [
            "scripts/theory/aa_bb/wl586_route_selection.py",
            "tests/theory/aa_bb/test_wl586_route_selection.py",
            "scripts/theory/aa_bb/consolidation_inputs.py",
        ],
        "source_result_path": (
            "results/closure_quotient_rank_zero_aa_bb_wl505_"
            "route_active_shell7_m_tail_supports_through_ambient_c_d_solubility_"
            "then_wl491_filter.json"
        ),
        "source_payload_sha256": "8934b63d6f2965c16eea50f0c2f0f72b0169ae21a9082a424720a5e12a2a8c37",
        "source_payload_size": 71433,
    },
    "wl521": {
        "source_worklog_path": (
            "docs/work-logs/archive/521-support-family-synthesis-after-wl519.md"
        ),
        "source_script_path": (
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl521_"
            "support_family_synthesis_after_wl519.py"
        ),
        "source_test_paths": [
            "tests/test_closure_quotient_rank_zero_aa_bb_wl521_support_family_synthesis.py"
        ],
        "source_selector": "$.final_candidate_ledgers[*]",
        "consumer_paths": [
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl522_"
            "support_cover_taxonomy_to_lemma_candidate_checkpoint.py",
            "scripts/theory/aa_bb/consolidation_inputs.py",
        ],
        "source_result_path": (
            "results/closure_quotient_rank_zero_aa_bb_wl521_"
            "support_family_synthesis_after_wl519.json"
        ),
        "source_payload_sha256": "9eacf74f4d545a45ea2f2de4e96320d8e06512d598e6e6464a2a35ac7029e5a0",
        "source_payload_size": 59384,
    },
    "wl522": {
        "source_worklog_path": (
            "docs/work-logs/archive/522-support-cover-taxonomy-to-lemma-candidate-checkpoint.md"
        ),
        "source_script_path": (
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl522_"
            "support_cover_taxonomy_to_lemma_candidate_checkpoint.py"
        ),
        "source_test_paths": [
            "tests/test_closure_quotient_rank_zero_aa_bb_wl522_support_cover_taxonomy.py"
        ],
        "source_selector": "$.support_cover_taxonomy[*]",
        "consumer_paths": [
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl527_"
            "function_field_squareclass_proof_data_scope.py",
            "scripts/theory/aa_bb/wl586_route_selection.py",
            "tests/theory/aa_bb/test_wl586_route_selection.py",
            "scripts/theory/aa_bb/consolidation_inputs.py",
        ],
        "source_result_path": (
            "results/closure_quotient_rank_zero_aa_bb_wl522_"
            "support_cover_taxonomy_to_lemma_candidate_checkpoint.json"
        ),
        "source_payload_sha256": "d51875d4bdbe0bcc06fe14bd78f3cd9699b6e92171604a983a6a3d9ef6438bf5",
        "source_payload_size": 25377,
    },
    "wl527": {
        "source_worklog_path": "docs/work-logs/527-function-field-squareclass-proof-data-scope.md",
        "source_script_path": (
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl527_"
            "function_field_squareclass_proof_data_scope.py"
        ),
        "source_test_paths": [
            "tests/test_closure_quotient_rank_zero_aa_bb_wl527_"
            "function_field_squareclass_proof_data.py"
        ],
        "source_selector": "$.cover_family_proof_data_inventory[*]",
        "consumer_paths": [
            "scripts/theory/aa_bb/wl586_route_selection.py",
            "tests/theory/aa_bb/test_wl586_route_selection.py",
            "scripts/theory/aa_bb/consolidation_inputs.py",
        ],
        "source_result_path": (
            "results/closure_quotient_rank_zero_aa_bb_wl527_"
            "function_field_squareclass_proof_data_scope.json"
        ),
        "source_payload_sha256": "e673361dba3e379accf6e785e301bff65bcbcbbaa2f6903cad7492279a90638e",
        "source_payload_size": 54631,
    },
}

PROJECTION_SPECS = (
    ("a0-ledger", "wl521"),
    ("a0-witnesses", "wl505"),
    ("a0-taxonomy", "wl522"),
    ("a0-inventory", "wl527"),
    ("b0-prototype-rows", "wl495"),
)

EXPECTED_WITNESS_IDS = {
    "AA_A3_B7_u_3_plus_v_5_plus_w_17_m_tail_shell7_candidate",
    "AA_A6_B7_v_13_m_tail_shell7_candidate",
    "AA_A7_B2_u_7_m_tail_shell7_candidate",
    "AA_A7_B6_u_7_plus_v_13_plus_w_5_m_tail_shell7_candidate",
    "BB_A2_B7_u_7_m_tail_shell7_candidate",
    "BB_A6_B7_u_7_plus_v_13_plus_w_5_m_tail_shell7_candidate",
    "BB_A7_B3_u_3_plus_v_5_plus_w_17_m_tail_shell7_candidate",
    "BB_A7_B6_v_13_m_tail_shell7_candidate",
}

B0_TARGET_IDS = (
    "AA_A1_B4_v_5_m_tail_refresh_candidate",
    "BB_A4_B1_v_5_m_tail_refresh_candidate",
)

B0_EXPECTED_SAMPLES = {
    B0_TARGET_IDS[0]: {
        "A": 1,
        "B": 4,
        "L": 1,
        "T": 5,
        "primitive": True,
        "side": "AA",
        "sqrt_q": 29,
    },
    B0_TARGET_IDS[1]: {
        "A": 4,
        "B": 1,
        "L": 1,
        "T": 5,
        "primitive": True,
        "side": "BB",
        "sqrt_q": 29,
    },
}
B0_EXPECTED_LEDGER_ROUTE = "globally_soluble_but_not_aa_bb_admissible_ledger"
B0_EXPECTED_BLOCKING_REASONS = {
    "AA": ("BB_common_source_product_not_square", "M_not_positive"),
    "BB": ("AA_common_source_product_not_square", "M_not_positive"),
}

WL495_COMPATIBILITY_METADATA = {
    "status": "ok",
    "ready": True,
    "source": "wl494 active refreshed M_tail supports plus wl491 filter",
    "pattern": "AA+BB",
    "lemma_id": "WL495_route_refreshed_support_through_ambient_C_d_solubility_then_wl491_filter",
    "work_log": "wl495",
    "input_work_logs": ["wl491", "wl494"],
    "complete_c_d_cover_data_instantiated_here": True,
    "old_package_x_coordinate_collapse_used": False,
    "package_x_s_tilde_bridge_used": False,
    "broad_rank_or_selmer_diagnostics_run": False,
    "single_curve_diagnostics_run": False,
    "complete_selmer_upper_bound_proved": False,
    "dim_sel2_eq_2_claimed": False,
    "rank_zero_claimed": False,
    "sha2_trivial_claimed": False,
    "family_exclusion_proved_count": 0,
    "route_summary": {
        "ambient_globally_soluble_count": 4,
        "aa_bb_not_admissible_count": 4,
    },
}

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_COMMIT_RE = re.compile(r"^[0-9a-f]{7,40}$")


class ConsolidationInputError(ValueError):
    """Raised when a canonical input or explicit source projection is invalid."""


def _fail(message: str) -> NoReturn:
    raise ConsolidationInputError(message)


def _exact_keys(value: Any, expected: set[str], context: str) -> dict[str, Any]:
    if type(value) is not dict:
        _fail(f"{context}: expected object")
    actual = set(value)
    missing = sorted(expected - actual)
    unknown = sorted(actual - expected)
    if missing or unknown:
        parts = []
        if missing:
            parts.append(f"missing={missing}")
        if unknown:
            parts.append(f"unknown={unknown}")
        _fail(f"{context}: {' '.join(parts)}")
    return value


def _string(value: Any, context: str) -> str:
    if type(value) is not str:
        _fail(f"{context}: expected string")
    return value


def _integer(value: Any, context: str) -> int:
    if type(value) is not int:
        _fail(f"{context}: expected integer")
    return value


def _boolean(value: Any, context: str) -> bool:
    if type(value) is not bool:
        _fail(f"{context}: expected boolean")
    return value


def _list(value: Any, context: str) -> list[Any]:
    if type(value) is not list:
        _fail(f"{context}: expected array")
    return value


def _nullable_integer(value: Any, context: str) -> int | None:
    if value is None:
        return None
    return _integer(value, context)


def _strings(value: Any, context: str) -> list[str]:
    return [
        _string(item, f"{context}[{index}]") for index, item in enumerate(_list(value, context))
    ]


def _unique(values: list[str], context: str) -> None:
    if len(values) != len(set(values)):
        _fail(f"{context}: duplicate values")


def _d_vector(value: Any, context: str, *, allow_empty: bool = True) -> dict[str, int]:
    obj = _exact_keys(value, set() if value == {} and allow_empty else set(D_VECTOR_KEYS), context)
    if not obj and not allow_empty:
        _fail(f"{context}: empty vector")
    result = {}
    for key in D_VECTOR_KEYS:
        if key in obj:
            number = _integer(obj[key], f"{context}.{key}")
            if number <= 0:
                _fail(f"{context}.{key}: expected positive integer")
            result[key] = number
    return result


def _cover_summary(value: Any, context: str) -> dict[str, Any]:
    obj = _exact_keys(value, {"L", "T", "d_vector"}, context)
    return {
        "L": _integer(obj["L"], f"{context}.L"),
        "T": _integer(obj["T"], f"{context}.T"),
        "d_vector": _d_vector(obj["d_vector"], f"{context}.d_vector"),
    }


def _ledger_sample(value: Any, context: str) -> dict[str, Any]:
    obj = _exact_keys(value, {"A", "B", "L", "T", "side"}, context)
    side = obj["side"]
    if side is not None:
        side = _string(side, f"{context}.side")
    return {
        "A": _nullable_integer(obj["A"], f"{context}.A"),
        "B": _nullable_integer(obj["B"], f"{context}.B"),
        "L": _integer(obj["L"], f"{context}.L"),
        "T": _integer(obj["T"], f"{context}.T"),
        "side": side,
    }


def _witness_sample(value: Any, context: str) -> dict[str, Any]:
    obj = _exact_keys(value, {"A", "B", "L", "T", "primitive", "side", "sqrt_q"}, context)
    return {
        "A": _integer(obj["A"], f"{context}.A"),
        "B": _integer(obj["B"], f"{context}.B"),
        "L": _integer(obj["L"], f"{context}.L"),
        "T": _integer(obj["T"], f"{context}.T"),
        "primitive": _boolean(obj["primitive"], f"{context}.primitive"),
        "side": _string(obj["side"], f"{context}.side"),
        "sqrt_q": _integer(obj["sqrt_q"], f"{context}.sqrt_q"),
    }


def _parameters(value: Any, context: str) -> dict[str, int]:
    obj = _exact_keys(value, {"p", "q", "sqrt_q"}, context)
    return {
        "p": _integer(obj["p"], f"{context}.p"),
        "q": _integer(obj["q"], f"{context}.q"),
        "sqrt_q": _integer(obj["sqrt_q"], f"{context}.sqrt_q"),
    }


def _d_vector_full(value: Any, context: str) -> dict[str, int]:
    result = _d_vector(value, context, allow_empty=False)
    if set(result) != set(D_VECTOR_KEYS):
        _fail(f"{context}: incomplete vector")
    return result


def _point(value: Any, context: str) -> dict[str, int]:
    obj = _exact_keys(value, set(COVER_POINT_KEYS), context)
    return {key: _integer(obj[key], f"{context}.{key}") for key in COVER_POINT_KEYS}


def _e_point(value: Any, context: str) -> dict[str, int]:
    obj = _exact_keys(value, set(E_POINT_KEYS), context)
    return {key: _integer(obj[key], f"{context}.{key}") for key in E_POINT_KEYS}


def _validate_document(
    payload: Any,
    *,
    kind: str,
    row_count: int,
    row_validator: Any,
) -> dict[str, Any]:
    document = _exact_keys(payload, {"schema_version", "kind", "rows"}, kind)
    if _integer(document["schema_version"], f"{kind}.schema_version") != SCHEMA_VERSION:
        _fail(f"{kind}.schema_version: unsupported version")
    if _string(document["kind"], f"{kind}.kind") != kind:
        _fail(f"{kind}.kind: mismatch")
    rows = _list(document["rows"], f"{kind}.rows")
    if len(rows) != row_count:
        _fail(f"{kind}.rows: expected {row_count}, got {len(rows)}")
    for index, row in enumerate(rows):
        row_validator(row, f"{kind}.rows[{index}]")
    return document


def _validate_ledger_row(value: Any, context: str) -> None:
    row = _exact_keys(
        value,
        {
            "candidate_id",
            "support_family",
            "cover_family",
            "sample",
            "cover_summary",
            "classification",
            "ambient_c_d_global_solubility_status",
            "ledger_route",
            "source_work_log",
        },
        context,
    )
    _string(row["candidate_id"], f"{context}.candidate_id")
    _string(row["support_family"], f"{context}.support_family")
    _string(row["cover_family"], f"{context}.cover_family")
    _ledger_sample(row["sample"], f"{context}.sample")
    _cover_summary(row["cover_summary"], f"{context}.cover_summary")
    classification = _string(row["classification"], f"{context}.classification")
    if classification not in {
        "already_closed",
        "globally_soluble_but_not_aa_bb_admissible",
        "refuted",
    }:
        _fail(f"{context}.classification: unsupported value")
    ambient = row["ambient_c_d_global_solubility_status"]
    if ambient is not None:
        ambient = _string(ambient, f"{context}.ambient_c_d_global_solubility_status")
        if ambient not in {"globally_soluble", "globally_not_soluble"}:
            _fail(f"{context}.ambient_c_d_global_solubility_status: unsupported value")
    _string(row["ledger_route"], f"{context}.ledger_route")
    _string(row["source_work_log"], f"{context}.source_work_log")


def _validate_witness_row(value: Any, context: str) -> None:
    row = _exact_keys(
        value,
        {
            "candidate_id",
            "candidate_support",
            "sample",
            "parameters",
            "d_vector",
            "point_on_cover",
            "point_on_E_L",
        },
        context,
    )
    _string(row["candidate_id"], f"{context}.candidate_id")
    support = _strings(row["candidate_support"], f"{context}.candidate_support")
    _unique(support, f"{context}.candidate_support")
    _witness_sample(row["sample"], f"{context}.sample")
    _parameters(row["parameters"], f"{context}.parameters")
    _d_vector_full(row["d_vector"], f"{context}.d_vector")
    _point(row["point_on_cover"], f"{context}.point_on_cover")
    _e_point(row["point_on_E_L"], f"{context}.point_on_E_L")


def _validate_taxonomy_row(value: Any, context: str) -> None:
    row = _exact_keys(
        value,
        {
            "support_family",
            "cover_family",
            "classification",
            "failure_mode",
            "ambient_c_d_global_solubility_status",
            "lemma_candidate_status",
            "candidate_ids",
            "entry_count",
            "work_logs",
            "cover_summary",
            "blocking_reasons",
        },
        context,
    )
    for key in (
        "support_family",
        "cover_family",
        "classification",
        "failure_mode",
        "lemma_candidate_status",
    ):
        _string(row[key], f"{context}.{key}")
    ambient = _string(
        row["ambient_c_d_global_solubility_status"],
        f"{context}.ambient_c_d_global_solubility_status",
    )
    if ambient not in {
        "globally_soluble",
        "globally_not_soluble",
        "not_applicable_processed_m_tail_support",
    }:
        _fail(f"{context}.ambient_c_d_global_solubility_status: unsupported value")
    candidate_ids = _strings(row["candidate_ids"], f"{context}.candidate_ids")
    _unique(candidate_ids, f"{context}.candidate_ids")
    if _integer(row["entry_count"], f"{context}.entry_count") != len(candidate_ids):
        _fail(f"{context}.entry_count: mismatch")
    _strings(row["work_logs"], f"{context}.work_logs")
    _cover_summary(row["cover_summary"], f"{context}.cover_summary")
    _strings(row["blocking_reasons"], f"{context}.blocking_reasons")


def _validate_inventory_row(value: Any, context: str) -> None:
    row = _exact_keys(
        value,
        {
            "cover_family",
            "support_family",
            "classification",
            "failure_mode",
            "ambient_c_d_global_solubility_status",
            "lemma_candidate_status",
            "entry_count",
            "candidate_ids",
            "source_sides_to_map",
            "work_logs",
            "blocking_reasons_seen_at_point_level",
            "cover_family_model_availability",
            "rational_source_side_maps",
            "candidate_function_field_elements",
            "opposite_side_target",
            "exceptional_specialization_positivity_checklist",
            "missing_data_classes",
        },
        context,
    )
    for key in (
        "cover_family",
        "support_family",
        "classification",
        "failure_mode",
        "ambient_c_d_global_solubility_status",
        "lemma_candidate_status",
    ):
        _string(row[key], f"{context}.{key}")
    _integer(row["entry_count"], f"{context}.entry_count")
    candidate_ids = _strings(row["candidate_ids"], f"{context}.candidate_ids")
    _unique(candidate_ids, f"{context}.candidate_ids")
    _strings(row["source_sides_to_map"], f"{context}.source_sides_to_map")
    _strings(row["work_logs"], f"{context}.work_logs")
    _strings(
        row["blocking_reasons_seen_at_point_level"],
        f"{context}.blocking_reasons_seen_at_point_level",
    )

    model = _exact_keys(
        row["cover_family_model_availability"],
        {
            "has_cover_family_label",
            "has_l_t_parameters",
            "has_explicit_d_vector",
            "has_explicit_equation",
            "has_function_field_coordinates",
            "available_data",
        },
        f"{context}.cover_family_model_availability",
    )
    for key in (
        "has_cover_family_label",
        "has_l_t_parameters",
        "has_explicit_d_vector",
        "has_explicit_equation",
        "has_function_field_coordinates",
    ):
        _boolean(model[key], f"{context}.cover_family_model_availability.{key}")
    available = _exact_keys(
        model["available_data"],
        {"L", "T", "d_vector"},
        f"{context}.cover_family_model_availability.available_data",
    )
    _integer(available["L"], f"{context}.cover_family_model_availability.available_data.L")
    _integer(available["T"], f"{context}.cover_family_model_availability.available_data.T")
    _d_vector(
        available["d_vector"],
        f"{context}.cover_family_model_availability.available_data.d_vector",
    )

    maps = _exact_keys(
        row["rational_source_side_maps"],
        {"point_level_wl491_failures_available", "uniform_family_maps_available", "needed"},
        f"{context}.rational_source_side_maps",
    )
    _boolean(
        maps["point_level_wl491_failures_available"],
        f"{context}.rational_source_side_maps.point_level_wl491_failures_available",
    )
    _boolean(
        maps["uniform_family_maps_available"],
        f"{context}.rational_source_side_maps.uniform_family_maps_available",
    )
    _string(maps["needed"], f"{context}.rational_source_side_maps.needed")

    elements = _exact_keys(
        row["candidate_function_field_elements"],
        {
            "point_level_formula_template_only",
            "N_in_function_field_available",
            "M_in_function_field_available",
        },
        f"{context}.candidate_function_field_elements",
    )
    formulas = _exact_keys(
        elements["point_level_formula_template_only"],
        {"N", "M"},
        f"{context}.candidate_function_field_elements.point_level_formula_template_only",
    )
    _string(
        formulas["N"],
        f"{context}.candidate_function_field_elements.point_level_formula_template_only.N",
    )
    _string(
        formulas["M"],
        f"{context}.candidate_function_field_elements.point_level_formula_template_only.M",
    )
    _boolean(
        elements["N_in_function_field_available"],
        f"{context}.candidate_function_field_elements.N_in_function_field_available",
    )
    _boolean(
        elements["M_in_function_field_available"],
        f"{context}.candidate_function_field_elements.M_in_function_field_available",
    )

    target = _exact_keys(
        row["opposite_side_target"],
        {"AA_source_target", "BB_source_target", "certificate_needed"},
        f"{context}.opposite_side_target",
    )
    for key in ("AA_source_target", "BB_source_target", "certificate_needed"):
        _string(target[key], f"{context}.opposite_side_target.{key}")
    _strings(
        row["exceptional_specialization_positivity_checklist"],
        f"{context}.exceptional_specialization_positivity_checklist",
    )
    missing = _strings(row["missing_data_classes"], f"{context}.missing_data_classes")
    _unique(missing, f"{context}.missing_data_classes")


def _validate_b0_row(value: Any, context: str) -> None:
    row = _exact_keys(
        value,
        {
            "candidate_id",
            "candidate_support",
            "sample",
            "complete_d_cover",
            "ambient_witness",
            "routing",
        },
        context,
    )
    _string(row["candidate_id"], f"{context}.candidate_id")
    _strings(row["candidate_support"], f"{context}.candidate_support")
    _witness_sample(row["sample"], f"{context}.sample")
    cover = _exact_keys(
        row["complete_d_cover"],
        {"parameters", "d_vector", "root_values"},
        f"{context}.complete_d_cover",
    )
    _parameters(cover["parameters"], f"{context}.complete_d_cover.parameters")
    _d_vector_full(cover["d_vector"], f"{context}.complete_d_cover.d_vector")
    roots = _exact_keys(
        cover["root_values"], set(ROOT_VALUE_KEYS), f"{context}.complete_d_cover.root_values"
    )
    for key in ROOT_VALUE_KEYS:
        _integer(roots[key], f"{context}.complete_d_cover.root_values.{key}")
    witness = _exact_keys(
        row["ambient_witness"], {"point_on_cover", "point_on_E_L"}, f"{context}.ambient_witness"
    )
    _point(witness["point_on_cover"], f"{context}.ambient_witness.point_on_cover")
    _e_point(witness["point_on_E_L"], f"{context}.ambient_witness.point_on_E_L")
    routing = _exact_keys(
        row["routing"],
        {"ambient_status", "admissibility_status", "ledger_route", "blocking_reasons"},
        f"{context}.routing",
    )
    for key in ("ambient_status", "admissibility_status", "ledger_route"):
        _string(routing[key], f"{context}.routing.{key}")
    _strings(routing["blocking_reasons"], f"{context}.routing.blocking_reasons")


def _load_json_object(path: Path, context: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_bytes())
    except (OSError, json.JSONDecodeError) as exc:
        raise ConsolidationInputError(f"{context}: cannot read JSON: {exc}") from exc
    if type(value) is not dict:
        _fail(f"{context}: expected object")
    return value


def _canonical_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _write_canonical(path: Path, payload: dict[str, Any]) -> bytes:
    raw = _canonical_bytes(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return raw


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _read_source_payload(source_results_dir: Path, work_log: str) -> tuple[dict[str, Any], bytes]:
    """Read one explicitly named ignored result payload for materialization."""

    if work_log not in SOURCE_FILENAMES:
        _fail(f"unsupported source work log: {work_log}")
    path = Path(source_results_dir) / SOURCE_FILENAMES[work_log]
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ConsolidationInputError(f"{work_log}: source payload unavailable: {path}") from exc
    metadata = SOURCE_PROVENANCE[work_log]
    if (
        len(raw) != metadata["source_payload_size"]
        or _sha256(raw) != metadata["source_payload_sha256"]
    ):
        _fail(f"{work_log}: source payload provenance mismatch for {path}")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ConsolidationInputError(f"{work_log} source payload: invalid JSON") from exc
    if type(payload) is not dict:
        _fail(f"{work_log} source payload: expected object")
    return payload, raw


def _source_rows(
    payload: dict[str, Any], key: str, expected_count: int, work_log: str
) -> list[dict[str, Any]]:
    value = payload.get(key)
    rows = _list(value, f"{work_log}.{key}")
    if len(rows) != expected_count:
        _fail(f"{work_log}.{key}: expected {expected_count}, got {len(rows)}")
    for index, row in enumerate(rows):
        if type(row) is not dict:
            _fail(f"{work_log}.{key}[{index}]: expected object")
    return rows


def _project_cover_summary(value: Any, context: str) -> dict[str, Any]:
    summary = _exact_keys(value, {"L", "T", "d_vector"}, context)
    return {
        "L": summary["L"],
        "T": summary["T"],
        "d_vector": summary["d_vector"],
    }


def _project_ledger(payload: dict[str, Any]) -> dict[str, Any]:
    rows = _source_rows(payload, "final_candidate_ledgers", 43, "wl521")
    projected = []
    for row in rows:
        sample = row["sample"]
        summary = row["cover_summary"]
        projected.append(
            {
                "candidate_id": row["candidate_id"],
                "support_family": row["support_family"],
                "cover_family": row["cover_family"],
                "sample": {key: sample[key] for key in ("A", "B", "L", "T", "side")},
                "cover_summary": {
                    "L": summary["L"],
                    "T": summary["T"],
                    "d_vector": summary["d_vector"],
                },
                "classification": row["classification"],
                "ambient_c_d_global_solubility_status": row["ambient_c_d_global_solubility_status"],
                "ledger_route": row["ledger_route"],
                "source_work_log": row["source_work_log"],
            }
        )
    projected.sort(key=lambda row: row["candidate_id"])
    document = {"schema_version": SCHEMA_VERSION, "kind": "a0-ledger", "rows": projected}
    _validate_document(document, kind="a0-ledger", row_count=43, row_validator=_validate_ledger_row)
    _unique([row["candidate_id"] for row in projected], "a0-ledger.candidate_id")
    return document


def _project_witnesses(payload: dict[str, Any]) -> dict[str, Any]:
    rows = _source_rows(payload, "routed_active_shell7_supports", 12, "wl505")
    selected = []
    for row in rows:
        ambient = row.get("ambient_c_d_global_solubility")
        if type(ambient) is dict and ambient.get("status") == "globally_soluble":
            cover = row["complete_c_d_cover"]
            selected.append(
                {
                    "candidate_id": row["candidate_id"],
                    "candidate_support": list(row["candidate_support"]),
                    "sample": {
                        key: row["sample"][key]
                        for key in ("A", "B", "L", "T", "primitive", "side", "sqrt_q")
                    },
                    "parameters": {key: cover["parameters"][key] for key in ("p", "q", "sqrt_q")},
                    "d_vector": {key: cover["d_vector"][key] for key in D_VECTOR_KEYS},
                    "point_on_cover": {
                        key: ambient["point_on_cover"][key] for key in COVER_POINT_KEYS
                    },
                    "point_on_E_L": {
                        key: ambient["induced_point_on_E_L"][key] for key in E_POINT_KEYS
                    },
                }
            )
    selected.sort(key=lambda row: row["candidate_id"])
    document = {
        "schema_version": SCHEMA_VERSION,
        "kind": "a0-witnesses",
        "rows": selected,
    }
    _validate_document(
        document, kind="a0-witnesses", row_count=8, row_validator=_validate_witness_row
    )
    ids = [row["candidate_id"] for row in selected]
    _unique(ids, "a0-witnesses.candidate_id")
    if set(ids) != EXPECTED_WITNESS_IDS:
        _fail("a0-witnesses: selected witness ID set mismatch")
    return document


def _project_taxonomy(payload: dict[str, Any]) -> dict[str, Any]:
    rows = _source_rows(payload, "support_cover_taxonomy", 22, "wl522")
    projected = []
    for row in rows:
        projected.append(
            {
                "support_family": row["support_family"],
                "cover_family": row["cover_family"],
                "classification": row["classification"],
                "failure_mode": row["failure_mode"],
                "ambient_c_d_global_solubility_status": row["ambient_c_d_global_solubility_status"],
                "lemma_candidate_status": row["lemma_candidate_status"],
                "candidate_ids": sorted(row["candidate_ids"]),
                "entry_count": row["entry_count"],
                "work_logs": sorted(row["work_logs"], key=_work_log_key),
                "cover_summary": _project_cover_summary(
                    row["cover_summary"], "wl522.cover_summary"
                ),
                "blocking_reasons": sorted(row["blocking_reasons"]),
            }
        )
    projected.sort(key=lambda row: (row["support_family"], row["cover_family"]))
    document = {
        "schema_version": SCHEMA_VERSION,
        "kind": "a0-taxonomy",
        "rows": projected,
    }
    _validate_document(
        document, kind="a0-taxonomy", row_count=22, row_validator=_validate_taxonomy_row
    )
    _unique([row["cover_family"] for row in projected], "a0-taxonomy.cover_family")
    return document


def _project_inventory(payload: dict[str, Any]) -> dict[str, Any]:
    rows = _source_rows(payload, "cover_family_proof_data_inventory", 15, "wl527")
    projected = []
    for row in rows:
        model = row["cover_family_model_availability"]
        available = model["available_data"]
        maps = row["rational_source_side_maps"]
        elements = row["candidate_function_field_elements"]
        formulas = elements["point_level_formula_template_only"]
        target = row["opposite_side_target"]
        projected.append(
            {
                "cover_family": row["cover_family"],
                "support_family": row["support_family"],
                "classification": row["classification"],
                "failure_mode": row["failure_mode"],
                "ambient_c_d_global_solubility_status": row["ambient_c_d_global_solubility_status"],
                "lemma_candidate_status": row["lemma_candidate_status"],
                "entry_count": row["entry_count"],
                "candidate_ids": sorted(row["candidate_ids"]),
                "source_sides_to_map": sorted(row["source_sides_to_map"]),
                "work_logs": sorted(row["work_logs"], key=_work_log_key),
                "blocking_reasons_seen_at_point_level": sorted(
                    row["blocking_reasons_seen_at_point_level"]
                ),
                "cover_family_model_availability": {
                    "has_cover_family_label": model["has_cover_family_label"],
                    "has_l_t_parameters": model["has_l_t_parameters"],
                    "has_explicit_d_vector": model["has_explicit_d_vector"],
                    "has_explicit_equation": model["has_explicit_equation"],
                    "has_function_field_coordinates": model["has_function_field_coordinates"],
                    "available_data": {
                        "L": available["L"],
                        "T": available["T"],
                        "d_vector": available["d_vector"],
                    },
                },
                "rational_source_side_maps": {
                    "point_level_wl491_failures_available": maps[
                        "point_level_wl491_failures_available"
                    ],
                    "uniform_family_maps_available": maps["uniform_family_maps_available"],
                    "needed": maps["needed"],
                },
                "candidate_function_field_elements": {
                    "point_level_formula_template_only": {
                        "N": formulas["N"],
                        "M": formulas["M"],
                    },
                    "N_in_function_field_available": elements["N_in_function_field_available"],
                    "M_in_function_field_available": elements["M_in_function_field_available"],
                },
                "opposite_side_target": {
                    "AA_source_target": target["AA_source_target"],
                    "BB_source_target": target["BB_source_target"],
                    "certificate_needed": target["certificate_needed"],
                },
                "exceptional_specialization_positivity_checklist": list(
                    row["exceptional_specialization_positivity_checklist"]
                ),
                "missing_data_classes": list(row["missing_data_classes"]),
            }
        )
    projected.sort(key=lambda row: row["cover_family"])
    document = {
        "schema_version": SCHEMA_VERSION,
        "kind": "a0-inventory",
        "rows": projected,
    }
    _validate_document(
        document, kind="a0-inventory", row_count=15, row_validator=_validate_inventory_row
    )
    _unique([row["cover_family"] for row in projected], "a0-inventory.cover_family")
    return document


def _project_b0(payload: dict[str, Any]) -> dict[str, Any]:
    rows = _source_rows(payload, "routed_refreshed_supports", 6, "wl495")
    by_id = {}
    for row in rows:
        candidate_id = row["candidate_id"]
        if candidate_id in B0_TARGET_IDS:
            if candidate_id in by_id:
                _fail(f"wl495.routed_refreshed_supports: duplicate selected row {candidate_id}")
            by_id[candidate_id] = row
    if set(by_id) != set(B0_TARGET_IDS):
        _fail("b0-prototype-rows: selected wl495 ID set mismatch")
    projected = []
    for candidate_id in B0_TARGET_IDS:
        row = by_id[candidate_id]
        cover = row["complete_c_d_cover"]
        roots = cover["root_data"]
        ambient = row["ambient_c_d_global_solubility"]
        routing = row["routing_state"]
        projected.append(
            {
                "candidate_id": candidate_id,
                "candidate_support": list(row["candidate_support"]),
                "sample": {
                    key: row["sample"][key]
                    for key in ("A", "B", "L", "T", "primitive", "side", "sqrt_q")
                },
                "complete_d_cover": {
                    "parameters": {key: cover["parameters"][key] for key in ("p", "q", "sqrt_q")},
                    "d_vector": {key: cover["d_vector"][key] for key in D_VECTOR_KEYS},
                    "root_values": {key: roots[key]["value"] for key in ROOT_VALUE_KEYS},
                },
                "ambient_witness": {
                    "point_on_cover": {
                        key: ambient["point_on_cover"][key] for key in COVER_POINT_KEYS
                    },
                    "point_on_E_L": {
                        key: ambient["induced_point_on_E_L"][key] for key in E_POINT_KEYS
                    },
                },
                "routing": {
                    "ambient_status": routing["ambient_c_d_global_solubility_status"],
                    "admissibility_status": routing["aa_bb_admissibility_status"],
                    "ledger_route": routing["ledger_route"],
                    "blocking_reasons": sorted(row["wl491_filter_result"]["blocking_reasons"]),
                },
            }
        )
    document = {
        "schema_version": SCHEMA_VERSION,
        "kind": "b0-prototype-rows",
        "rows": projected,
    }
    _validate_document(
        document, kind="b0-prototype-rows", row_count=2, row_validator=_validate_b0_row
    )
    _validate_b0_invariants(document)
    return document


def _work_log_key(value: str) -> tuple[int, str]:
    match = re.fullmatch(r"wl(\d+)", value)
    return (int(match.group(1)), value) if match else (10**9, value)


def _validate_witness_equations(row: dict[str, Any], context: str) -> None:
    sample = row["sample"]
    params = row["parameters"]
    d_vector = row["d_vector"]
    point = row["point_on_cover"]
    e_point = row["point_on_E_L"]
    if params["sqrt_q"] != sample["sqrt_q"] or params["q"] != sample["sqrt_q"] ** 2:
        _fail(f"{context}: q/sqrt_q mismatch")
    if params["p"] != 8 * sample["L"] ** 2 - 2 * sample["T"] ** 2:
        _fail(f"{context}: p mismatch")
    if e_point["X"] != point["X"]:
        _fail(f"{context}: elliptic X mismatch")
    s = sample["sqrt_q"]
    equations = (
        (point["X"] + params["p"], d_vector["d_minus_p"], point["u_minus_p"]),
        (point["X"] - 2 * s, d_vector["d_pos_2sqrt_q"], point["u_pos_2sqrt_q"]),
        (point["X"] + 2 * s, d_vector["d_neg_2sqrt_q"], point["u_neg_2sqrt_q"]),
    )
    if any(left != coefficient * variable**2 for left, coefficient, variable in equations):
        _fail(f"{context}: cover coordinate equation mismatch")
    d_product = d_vector["d_minus_p"] * d_vector["d_pos_2sqrt_q"] * d_vector["d_neg_2sqrt_q"]
    scale = isqrt(d_product)
    if scale**2 != d_product:
        _fail(f"{context}: d-vector product is not a square")
    expected_y = scale * point["u_minus_p"] * point["u_pos_2sqrt_q"] * point["u_neg_2sqrt_q"]
    if e_point["Y"] != expected_y:
        _fail(f"{context}: elliptic Y product mismatch")


def _validate_a0_invariants(documents: dict[str, dict[str, Any]]) -> None:
    ledger = documents["a0-ledger"]["rows"]
    witnesses = documents["a0-witnesses"]["rows"]
    taxonomy = documents["a0-taxonomy"]["rows"]
    inventory = documents["a0-inventory"]["rows"]

    ledger_by_id = {row["candidate_id"]: row for row in ledger}
    if len(ledger_by_id) != 43:
        _fail("a0 cross-file: duplicate ledger candidate ID")
    taxonomy_by_family = {row["cover_family"]: row for row in taxonomy}
    if len(taxonomy_by_family) != 22:
        _fail("a0 cross-file: duplicate taxonomy cover family")
    taxonomy_ids = [candidate_id for row in taxonomy for candidate_id in row["candidate_ids"]]
    if (
        len(taxonomy_ids) != 43
        or len(set(taxonomy_ids)) != 43
        or set(taxonomy_ids) != set(ledger_by_id)
    ):
        _fail("a0 cross-file: taxonomy candidate union mismatch")

    for row in taxonomy:
        family_ids = row["candidate_ids"]
        ledger_rows = [ledger_by_id[candidate_id] for candidate_id in family_ids]
        if any(ledger_row["cover_family"] != row["cover_family"] for ledger_row in ledger_rows):
            _fail(f"a0 cross-file: taxonomy family mismatch {row['cover_family']}")
        if any(ledger_row["support_family"] != row["support_family"] for ledger_row in ledger_rows):
            _fail(f"a0 cross-file: taxonomy support mismatch {row['cover_family']}")
        if any(ledger_row["classification"] != row["classification"] for ledger_row in ledger_rows):
            _fail(f"a0 cross-file: taxonomy classification mismatch {row['cover_family']}")
        if any(ledger_row["cover_summary"] != row["cover_summary"] for ledger_row in ledger_rows):
            _fail(f"a0 cross-file: taxonomy cover summary mismatch {row['cover_family']}")
        expected_work_logs = sorted(
            {ledger_row["source_work_log"] for ledger_row in ledger_rows}, key=_work_log_key
        )
        if row["work_logs"] != expected_work_logs:
            _fail(f"a0 cross-file: taxonomy work-log mismatch {row['cover_family']}")

    classification_counts = Counter(row["classification"] for row in taxonomy)
    if classification_counts != Counter(
        {
            "already_closed": 2,
            "globally_soluble_but_not_aa_bb_admissible": 15,
            "refuted": 5,
        }
    ):
        _fail(f"a0 cross-file: taxonomy classification counts mismatch: {classification_counts}")
    entry_counts = Counter()
    for row in taxonomy:
        entry_counts[row["classification"]] += row["entry_count"]
    if entry_counts != Counter(
        {
            "already_closed": 4,
            "globally_soluble_but_not_aa_bb_admissible": 29,
            "refuted": 10,
        }
    ):
        _fail(f"a0 cross-file: taxonomy entry counts mismatch: {entry_counts}")

    inventory_by_family = {row["cover_family"]: row for row in inventory}
    expected_inventory_families = {
        row["cover_family"]
        for row in taxonomy
        if row["classification"] == "globally_soluble_but_not_aa_bb_admissible"
    }
    if set(inventory_by_family) != expected_inventory_families:
        _fail("a0 cross-file: inventory family set mismatch")
    for family, row in inventory_by_family.items():
        tax = taxonomy_by_family[family]
        if row["candidate_ids"] != tax["candidate_ids"] or row["entry_count"] != tax["entry_count"]:
            _fail(f"a0 cross-file: inventory candidate projection mismatch {family}")
        expected_sides = sorted(
            {candidate_id.split("_", 1)[0] for candidate_id in row["candidate_ids"]}
        )
        if row["source_sides_to_map"] != expected_sides:
            _fail(f"a0 cross-file: inventory source side mismatch {family}")
        available = row["cover_family_model_availability"]["available_data"]
        if (
            available["L"] != tax["cover_summary"]["L"]
            or available["T"] != tax["cover_summary"]["T"]
        ):
            _fail(f"a0 cross-file: inventory L/T mismatch {family}")
        if available["d_vector"] != tax["cover_summary"]["d_vector"]:
            _fail(f"a0 cross-file: inventory d-vector mismatch {family}")

    witness_ids = [row["candidate_id"] for row in witnesses]
    _unique(witness_ids, "a0-witnesses.candidate_id")
    if set(witness_ids) != EXPECTED_WITNESS_IDS:
        _fail("a0 cross-file: witness ID set mismatch")
    for index, row in enumerate(witnesses):
        context = f"a0-witnesses.rows[{index}]"
        _validate_witness_equations(row, context)
        ledger_row = ledger_by_id[row["candidate_id"]]
        sample = row["sample"]
        ledger_sample = ledger_row["sample"]
        if any(sample[key] != ledger_sample[key] for key in ("A", "B", "L", "T", "side")):
            _fail(f"{context}: sample differs from ledger")
        if "+".join(row["candidate_support"]) != ledger_row["support_family"]:
            _fail(f"{context}: support differs from ledger")
        if row["d_vector"] != ledger_row["cover_summary"]["d_vector"]:
            _fail(f"{context}: d-vector differs from ledger")


def _validate_b0_invariants(document: dict[str, Any]) -> None:
    rows = document["rows"]
    ids = [row["candidate_id"] for row in rows]
    if tuple(ids) != B0_TARGET_IDS:
        _fail("b0-prototype-rows: target order mismatch")
    for index, row in enumerate(rows):
        context = f"b0-prototype-rows.rows[{index}]"
        sample = row["sample"]
        cover = row["complete_d_cover"]
        roots = cover["root_values"]
        params = cover["parameters"]
        d_vector = cover["d_vector"]
        expected_sample = B0_EXPECTED_SAMPLES[row["candidate_id"]]
        if sample != expected_sample:
            _fail(f"{context}: sample identity mismatch")
        if row["candidate_support"] != ["v_5"]:
            _fail(f"{context}: support mismatch")
        if params != {"p": -42, "q": 841, "sqrt_q": 29}:
            _fail(f"{context}: parameters mismatch")
        if d_vector != {"d_minus_p": 5, "d_pos_2sqrt_q": 1, "d_neg_2sqrt_q": 5}:
            _fail(f"{context}: d-vector mismatch")
        if roots != {"e_minus": 42, "e_pos": 58, "e_neg": -58}:
            _fail(f"{context}: root values mismatch")
        _validate_witness_equations(
            {
                "sample": sample,
                "parameters": params,
                "d_vector": d_vector,
                "point_on_cover": row["ambient_witness"]["point_on_cover"],
                "point_on_E_L": row["ambient_witness"]["point_on_E_L"],
            },
            context,
        )
        if (
            row["routing"]["ambient_status"] != "globally_soluble"
            or row["routing"]["admissibility_status"] != "not_admissible"
        ):
            _fail(f"{context}: routing status mismatch")
        reasons = row["routing"]["blocking_reasons"]
        expected_reasons = B0_EXPECTED_BLOCKING_REASONS[sample["side"]]
        if tuple(sorted(reasons)) != tuple(sorted(expected_reasons)):
            _fail(f"{context}: routing blocking reasons mismatch")
        if row["routing"]["ledger_route"] != B0_EXPECTED_LEDGER_ROUTE:
            _fail(f"{context}: ledger route mismatch")


def _validate_b0_against_a0(a0: A0Bundle, b0: B0Document) -> None:
    ledger_by_id = {row["candidate_id"]: row for row in a0.ledger}
    for index, row in enumerate(b0.rows):
        context = f"a0/b0 cross-file.rows[{index}]"
        ledger_row = ledger_by_id.get(row["candidate_id"])
        if ledger_row is None:
            _fail(f"{context}: B0 candidate is absent from A0 ledger")
        sample = row["sample"]
        ledger_sample = ledger_row["sample"]
        if any(sample[key] != ledger_sample[key] for key in ("A", "B", "L", "T", "side")):
            _fail(f"{context}: B0 sample differs from A0 ledger")
        if row["candidate_support"] != [ledger_row["support_family"]]:
            _fail(f"{context}: B0 support differs from A0 ledger")
        cover = row["complete_d_cover"]
        ledger_summary = ledger_row["cover_summary"]
        if sample["L"] != ledger_summary["L"] or sample["T"] != ledger_summary["T"]:
            _fail(f"{context}: B0 sample differs from A0 cover summary")
        if cover["d_vector"] != ledger_summary["d_vector"]:
            _fail(f"{context}: B0 d-vector differs from A0 ledger")
        routing = row["routing"]
        if routing["ambient_status"] != ledger_row["ambient_c_d_global_solubility_status"]:
            _fail(f"{context}: B0 ambient status differs from A0 ledger")
        if ledger_row["classification"] != "globally_soluble_but_not_aa_bb_admissible":
            _fail(f"{context}: B0 classification differs from selected A0 ledger class")
        if routing["admissibility_status"] != "not_admissible":
            _fail(f"{context}: B0 admissibility status differs from A0 ledger class")
        if routing["ledger_route"] != ledger_row["ledger_route"]:
            _fail(f"{context}: B0 ledger route differs from A0 ledger")


def _ledger_summary(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(row["classification"] for row in rows)
    return {
        "aa_bb_admissible_entry_count": 0,
        "already_closed_entry_count": counts["already_closed"],
        "cover_family_count": len({row["cover_family"] for row in rows}),
        "final_candidate_ledger_entry_count": len(rows),
        "genuinely_deferred_entry_count": counts.get("genuinely_deferred", 0),
        "globally_soluble_but_not_aa_bb_admissible_entry_count": counts[
            "globally_soluble_but_not_aa_bb_admissible"
        ],
        "refuted_entry_count": counts["refuted"],
        "support_family_count": len({row["support_family"] for row in rows}),
    }


def _taxonomy_summary(
    rows: list[dict[str, Any]], ledger_rows: list[dict[str, Any]]
) -> dict[str, int]:
    failure_counts = Counter(row["failure_mode"] for row in rows)
    entry_counts = Counter()
    for row in rows:
        entry_counts[row["classification"]] += row["entry_count"]
    return {
        "aa_bb_admissible_cover_family_count": 0,
        "aa_bb_admissible_entry_count": 0,
        "already_closed_entry_count": entry_counts["already_closed"],
        "ambient_globally_not_soluble_cover_family_count": failure_counts[
            "ambient_globally_not_soluble"
        ],
        "ambient_globally_not_soluble_entry_count": entry_counts["refuted"],
        "cover_family_count": len(rows),
        "final_candidate_ledger_entry_count": len(ledger_rows),
        "genuinely_deferred_cover_family_count": failure_counts[
            "genuinely_deferred_ambient_c_d_solubility"
        ],
        "genuinely_deferred_entry_count": entry_counts.get("genuinely_deferred", 0),
        "globally_soluble_but_not_aa_bb_admissible_cover_family_count": failure_counts[
            "common_source_aa_bb_admissibility_failure"
        ],
        "globally_soluble_but_not_aa_bb_admissible_entry_count": entry_counts[
            "globally_soluble_but_not_aa_bb_admissible"
        ],
        "processed_or_duplicate_cover_family_count": failure_counts[
            "processed_or_duplicate_m_tail_support"
        ],
        "support_family_count": len({row["support_family"] for row in rows}),
        "taxonomy_row_count": len(rows),
    }


def _inventory_scope_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    complete = sum(row["cover_family_model_availability"]["has_explicit_d_vector"] for row in rows)
    return {
        "cover_families_missing_explicit_d_vector_count": len(rows) - complete,
        "cover_families_with_label_and_l_t_d_data_count": complete,
        "decision": (
            "Current wl522/wl526 data is not ready for a later uniform "
            "squareclass proof attempt. The exact missing class is explicit "
            "cover-family function-field models with rational source-side maps, "
            "N,M as function-field elements, and an opposite-side product "
            "squareclass or divisor-parity certificate with exceptional "
            "specialization and positivity separated."
        ),
        "exact_missing_data_class": (
            "uniform_function_field_model_maps_and_squareclass_certificate"
        ),
        "named_cover_family_count": len(rows),
        "named_entry_count": sum(row["entry_count"] for row in rows),
        "not_ready_cover_family_count": len(rows),
        "ready_cover_family_count": 0,
        "ready_for_later_uniform_squareclass_proof_attempt": False,
    }


def _missing_data_class_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    return dict(
        sorted(
            Counter(
                data_class for row in rows for data_class in row["missing_data_classes"]
            ).items()
        )
    )


def _root_data_from_values(values: dict[str, int]) -> dict[str, dict[str, int | str]]:
    return {
        "e_minus": {"symbolic": "-p", "value": values["e_minus"]},
        "e_pos": {"symbolic": "2*sqrt_q", "value": values["e_pos"]},
        "e_neg": {"symbolic": "-2*sqrt_q", "value": values["e_neg"]},
    }


def _inventory_compatibility_row(row: dict[str, Any]) -> dict[str, Any]:
    model = row["cover_family_model_availability"]
    if model["has_explicit_d_vector"]:
        model_status = "label_and_l_t_d_vector_only_no_explicit_function_field_model"
    else:
        model_status = "cover_label_only_missing_explicit_d_vector_and_equation"
    maps = row["rational_source_side_maps"]
    elements = row["candidate_function_field_elements"]
    target = row["opposite_side_target"]
    missing = list(row["missing_data_classes"])
    return {
        **copy.deepcopy(row),
        "cover_family_model_availability": {
            "status": model_status,
            **copy.deepcopy(model),
        },
        "rational_source_side_maps": {
            "status": "missing_uniform_maps",
            **copy.deepcopy(maps),
        },
        "candidate_function_field_elements": {
            "status": "missing_N_M_as_function_field_elements",
            **copy.deepcopy(elements),
        },
        "opposite_side_target": {
            "status": "formula_target_only_not_a_certificate",
            **copy.deepcopy(target),
        },
        "readiness": "not_ready_for_later_uniform_squareclass_proof_attempt",
        "missing_data_classes": missing,
    }


class A0Bundle:
    """Validated A0 bundle loaded from the four tracked canonical files."""

    def __init__(self, documents: dict[str, dict[str, Any]]) -> None:
        self.documents = documents

    def __getitem__(self, key: str) -> dict[str, Any]:
        return self.documents[key]

    @property
    def ledger(self) -> list[dict[str, Any]]:
        return self.documents["a0-ledger"]["rows"]

    @property
    def witnesses(self) -> list[dict[str, Any]]:
        return self.documents["a0-witnesses"]["rows"]

    @property
    def taxonomy(self) -> list[dict[str, Any]]:
        return self.documents["a0-taxonomy"]["rows"]

    @property
    def inventory(self) -> list[dict[str, Any]]:
        return self.documents["a0-inventory"]["rows"]

    def to_wl522_view(self) -> dict[str, Any]:
        return {
            "status": "ok",
            "ready": True,
            "work_log": "wl522",
            "ledger_summary": _ledger_summary(self.ledger),
            "final_candidate_ledgers": copy.deepcopy(self.ledger),
            "taxonomy_summary": _taxonomy_summary(self.taxonomy, self.ledger),
            "support_cover_taxonomy": copy.deepcopy(self.taxonomy),
        }

    def to_wl527_view(self) -> dict[str, Any]:
        return {
            "status": "ok",
            "ready": True,
            "work_log": "wl527",
            "scope_summary": _inventory_scope_summary(self.inventory),
            "missing_data_class_counts": _missing_data_class_counts(self.inventory),
            "cover_family_proof_data_inventory": [
                _inventory_compatibility_row(row) for row in self.inventory
            ],
            "proof_data_readiness_decision": {
                "ready_for_later_uniform_squareclass_proof_attempt": False,
                "uniform_lemma_proved_here": False,
                "mathematical_uniform_lemma_refuted_here": False,
                "finite_taxonomy_promoted_here": False,
                "exact_missing_data_class": (
                    "uniform_function_field_model_maps_and_squareclass_certificate"
                ),
            },
        }

    def to_wl586_inputs(self) -> dict[str, Any]:
        rows = []
        for witness in self.witnesses:
            params = witness["parameters"]
            roots = {
                "e_minus": -params["p"],
                "e_pos": 2 * params["sqrt_q"],
                "e_neg": -2 * params["sqrt_q"],
            }
            rows.append(
                {
                    "candidate_id": witness["candidate_id"],
                    "candidate_support": copy.deepcopy(witness["candidate_support"]),
                    "sample": copy.deepcopy(witness["sample"]),
                    "complete_c_d_cover": {
                        "parameters": copy.deepcopy(params),
                        "d_vector": copy.deepcopy(witness["d_vector"]),
                        "root_data": _root_data_from_values(roots),
                    },
                    "ambient_c_d_global_solubility": {
                        "status": "globally_soluble",
                        "point_on_cover": copy.deepcopy(witness["point_on_cover"]),
                        "induced_point_on_E_L": copy.deepcopy(witness["point_on_E_L"]),
                    },
                }
            )
        return {
            "status": "ok",
            "ready": True,
            "work_log": "wl505",
            "route_summary": {"wl491_filter_applied_count": len(rows)},
            "routed_active_shell7_supports": rows,
        }


class B0Document:
    """Validated B0 prototype rows loaded from the tracked canonical file."""

    def __init__(self, document: dict[str, Any]) -> None:
        self.document = document

    def __getitem__(self, key: str) -> Any:
        return self.document[key]

    @property
    def rows(self) -> list[dict[str, Any]]:
        return self.document["rows"]

    def to_wl528_view(self) -> dict[str, Any]:
        rows = []
        for row in self.rows:
            cover = row["complete_d_cover"]
            params = cover["parameters"]
            rows.append(
                {
                    "candidate_id": row["candidate_id"],
                    "candidate_support": copy.deepcopy(row["candidate_support"]),
                    "sample": copy.deepcopy(row["sample"]),
                    "complete_c_d_cover": {
                        "candidate_id": row["candidate_id"],
                        "coordinate_order": list(D_VECTOR_KEYS),
                        "d_vector": copy.deepcopy(cover["d_vector"]),
                        "instantiation_only": True,
                        "parameters": copy.deepcopy(params),
                        "root_data": _root_data_from_values(cover["root_values"]),
                        "sample": copy.deepcopy(row["sample"]),
                        "source_support": copy.deepcopy(row["candidate_support"]),
                        "variables": list(COVER_POINT_KEYS),
                    },
                    "ambient_c_d_global_solubility": {
                        "status": row["routing"]["ambient_status"],
                        "point_on_cover": copy.deepcopy(row["ambient_witness"]["point_on_cover"]),
                        "induced_point_on_E_L": copy.deepcopy(
                            row["ambient_witness"]["point_on_E_L"]
                        ),
                    },
                    "routing_state": {
                        "ambient_c_d_global_solubility_status": row["routing"]["ambient_status"],
                        "aa_bb_admissibility_status": row["routing"]["admissibility_status"],
                        "ledger_route": row["routing"]["ledger_route"],
                        "blocking_reasons": copy.deepcopy(row["routing"]["blocking_reasons"]),
                    },
                }
            )
        view = copy.deepcopy(WL495_COMPATIBILITY_METADATA)
        view["routed_refreshed_supports"] = rows
        return view


def _canonical_directory(path: Path) -> Path:
    candidate = Path(path)
    if "results" in candidate.parts:
        _fail(f"runtime loader refuses legacy results path: {candidate}")
    if candidate.is_dir():
        return candidate
    if candidate.name in set(CANONICAL_FILES.values()):
        return candidate.parent
    _fail(f"canonical input directory or known file required: {candidate}")


def _load_canonical_document(
    directory: Path, kind: str, row_count: int, validator: Any
) -> dict[str, Any]:
    path = directory / CANONICAL_FILES[kind]
    payload = _load_json_object(path, kind)
    return _validate_document(payload, kind=kind, row_count=row_count, row_validator=validator)


def load_a0(path: Path) -> A0Bundle:
    """Load all A0 canonical files from a directory or one known A0 file."""

    directory = _canonical_directory(Path(path))
    documents = {
        "a0-ledger": _load_canonical_document(directory, "a0-ledger", 43, _validate_ledger_row),
        "a0-witnesses": _load_canonical_document(
            directory, "a0-witnesses", 8, _validate_witness_row
        ),
        "a0-taxonomy": _load_canonical_document(
            directory, "a0-taxonomy", 22, _validate_taxonomy_row
        ),
        "a0-inventory": _load_canonical_document(
            directory, "a0-inventory", 15, _validate_inventory_row
        ),
    }
    _validate_a0_invariants(documents)
    return A0Bundle(documents)


def load_b0(path: Path) -> B0Document:
    """Load B0 canonical rows from a directory or the known B0 file."""

    directory = _canonical_directory(Path(path))
    document = _load_canonical_document(directory, "b0-prototype-rows", 2, _validate_b0_row)
    _validate_b0_invariants(document)
    return B0Document(document)


def _manifest_binding_specs() -> list[dict[str, Any]]:
    bindings = []
    for kind, work_log in PROJECTION_SPECS:
        provenance = SOURCE_PROVENANCE[work_log]
        bindings.append(
            {
                "canonical_path": CANONICAL_FILES[kind],
                "source_worklog": work_log,
                **copy.deepcopy(provenance),
            }
        )
    return bindings


def _validate_manifest(payload: Any) -> dict[str, Any]:
    manifest = _exact_keys(
        payload,
        {
            "schema_version", "kind", "materialization_kind", "baseline_commit",
            "bindings", "auxiliary_bindings",
        },
        "manifest",
    )
    if _integer(manifest["schema_version"], "manifest.schema_version") != SCHEMA_VERSION:
        _fail("manifest.schema_version: unsupported version")
    if _string(manifest["kind"], "manifest.kind") != "manifest":
        _fail("manifest.kind: mismatch")
    if (
        _string(manifest["materialization_kind"], "manifest.materialization_kind")
        != "a0_b0_canonical_projection"
    ):
        _fail("manifest.materialization_kind: mismatch")
    baseline = _string(manifest["baseline_commit"], "manifest.baseline_commit")
    if not _COMMIT_RE.fullmatch(baseline):
        _fail("manifest.baseline_commit: invalid commit id")
    if baseline != BASELINE_COMMIT:
        _fail(f"manifest.baseline_commit: expected {BASELINE_COMMIT}")
    bindings = _list(manifest["bindings"], "manifest.bindings")
    if len(bindings) != len(PROJECTION_SPECS):
        _fail("manifest.bindings: expected five bindings")
    expected_by_path = {
        CANONICAL_FILES[kind]: (kind, work_log) for kind, work_log in PROJECTION_SPECS
    }
    seen_paths = set()
    for index, binding_value in enumerate(bindings):
        context = f"manifest.bindings[{index}]"
        binding = _exact_keys(
            binding_value,
            {
                "canonical_path",
                "canonical_projection_sha256",
                "canonical_projection_size",
                "source_worklog",
                "source_worklog_path",
                "source_script_path",
                "source_test_paths",
                "source_result_path",
                "source_selector",
                "source_payload_sha256",
                "source_payload_size",
                "consumer_paths",
            },
            context,
        )
        path = _string(binding["canonical_path"], f"{context}.canonical_path")
        if path not in expected_by_path or path in seen_paths:
            _fail(f"{context}.canonical_path: unexpected or duplicate path")
        seen_paths.add(path)
        _kind, work_log = expected_by_path[path]
        provenance = SOURCE_PROVENANCE[work_log]
        if _string(binding["source_worklog"], f"{context}.source_worklog") != work_log:
            _fail(f"{context}.source_worklog: mismatch")
        for key in (
            "source_worklog_path",
            "source_script_path",
            "source_result_path",
            "source_selector",
        ):
            if _string(binding[key], f"{context}.{key}") != provenance[key]:
                _fail(f"{context}.{key}: provenance mismatch")
        if (
            _strings(binding["source_test_paths"], f"{context}.source_test_paths")
            != provenance["source_test_paths"]
        ):
            _fail(f"{context}.source_test_paths: provenance mismatch")
        if (
            _strings(binding["consumer_paths"], f"{context}.consumer_paths")
            != provenance["consumer_paths"]
        ):
            _fail(f"{context}.consumer_paths: provenance mismatch")
        source_hash = _string(binding["source_payload_sha256"], f"{context}.source_payload_sha256")
        if not _SHA256_RE.fullmatch(source_hash):
            _fail(f"{context}.source_payload_sha256: invalid hash")
        if source_hash != provenance["source_payload_sha256"]:
            _fail(f"{context}.source_payload_sha256: baseline mismatch")
        source_size = _integer(binding["source_payload_size"], f"{context}.source_payload_size")
        if source_size != provenance["source_payload_size"]:
            _fail(f"{context}.source_payload_size: baseline mismatch")
        projection_hash = _string(
            binding["canonical_projection_sha256"],
            f"{context}.canonical_projection_sha256",
        )
        if not _SHA256_RE.fullmatch(projection_hash):
            _fail(f"{context}.canonical_projection_sha256: invalid hash")
        if (
            _integer(binding["canonical_projection_size"], f"{context}.canonical_projection_size")
            < 0
        ):
            _fail(f"{context}.canonical_projection_size: invalid size")
    if seen_paths != set(expected_by_path):
        _fail("manifest.bindings: incomplete path set")
    auxiliary = _list(manifest["auxiliary_bindings"], "manifest.auxiliary_bindings")
    expected_auxiliary = {A1_CERTIFICATES_FILE, "a2-boundary-spec.v1.json"}
    if len(auxiliary) != 2:
        _fail("manifest.auxiliary_bindings: expected two bindings")
    auxiliary_paths = set()
    for index, value in enumerate(auxiliary):
        context = f"manifest.auxiliary_bindings[{index}]"
        binding = _exact_keys(
            value,
            {
                "canonical_path", "canonical_projection_sha256",
                "canonical_projection_size", "source_payloads",
            },
            context,
        )
        canonical_path = _string(binding["canonical_path"], f"{context}.canonical_path")
        if canonical_path not in expected_auxiliary or canonical_path in auxiliary_paths:
            _fail(f"{context}.canonical_path: unexpected or duplicate path")
        auxiliary_paths.add(canonical_path)
        projection_hash = _string(
            binding["canonical_projection_sha256"],
            f"{context}.canonical_projection_sha256",
        )
        if not _SHA256_RE.fullmatch(projection_hash):
            _fail(f"{context}.canonical_projection_sha256: invalid hash")
        projection_size = _integer(
            binding["canonical_projection_size"],
            f"{context}.canonical_projection_size",
        )
        if projection_size <= 0:
            _fail(f"{context}.canonical_projection_size: invalid size")
        source_payloads = binding["source_payloads"]
        if type(source_payloads) is not dict or not source_payloads:
            _fail(f"{context}.source_payloads: expected nonempty object")
        for work_log, source in source_payloads.items():
            if work_log not in {f"wl{number}" for number in range(500, 528)}:
                _fail(f"{context}.source_payloads: invalid work log")
            source = _exact_keys(source, {"path", "sha256", "size"}, f"{context}.{work_log}")
            _string(source["path"], f"{context}.{work_log}.path")
            if not _SHA256_RE.fullmatch(_string(source["sha256"], f"{context}.{work_log}.sha256")):
                _fail(f"{context}.{work_log}.sha256: invalid hash")
            if _integer(source["size"], f"{context}.{work_log}.size") <= 0:
                _fail(f"{context}.{work_log}.size: invalid size")
    if auxiliary_paths != expected_auxiliary:
        _fail("manifest.auxiliary_bindings: incomplete path set")
    return manifest


def load_manifest(path: Path, canonical_dir: Path | None = None) -> dict[str, Any]:
    """Load and verify a manifest against tracked canonical projection bytes."""

    manifest_path = Path(path)
    if "results" in manifest_path.parts:
        _fail(f"runtime loader refuses legacy results path: {manifest_path}")
    payload = _validate_manifest(_load_json_object(manifest_path, "manifest"))
    directory = Path(canonical_dir) if canonical_dir is not None else manifest_path.parent
    if "results" in directory.parts:
        _fail(f"runtime loader refuses legacy results path: {directory}")
    for binding in payload["bindings"]:
        canonical_path = directory / binding["canonical_path"]
        try:
            raw = canonical_path.read_bytes()
        except OSError as exc:
            raise ConsolidationInputError(
                f"manifest: canonical projection unavailable: {canonical_path}"
            ) from exc
        if (
            len(raw) != binding["canonical_projection_size"]
            or _sha256(raw) != binding["canonical_projection_sha256"]
        ):
            _fail(f"manifest: canonical projection hash mismatch: {canonical_path}")
    for binding in payload["auxiliary_bindings"]:
        canonical_path = directory / binding["canonical_path"]
        try:
            raw = canonical_path.read_bytes()
        except OSError as exc:
            raise ConsolidationInputError(
                f"manifest: auxiliary projection unavailable: {canonical_path}"
            ) from exc
        if (
            len(raw) != binding["canonical_projection_size"]
            or _sha256(raw) != binding["canonical_projection_sha256"]
        ):
            _fail(f"manifest: auxiliary projection hash mismatch: {canonical_path}")
    return payload


def _materialize_a0_documents(source_results_dir: Path) -> dict[str, dict[str, Any]]:
    wl505, _ = _read_source_payload(source_results_dir, "wl505")
    wl521, _ = _read_source_payload(source_results_dir, "wl521")
    wl522, _ = _read_source_payload(source_results_dir, "wl522")
    wl527, _ = _read_source_payload(source_results_dir, "wl527")
    documents = {
        "a0-ledger": _project_ledger(wl521),
        "a0-witnesses": _project_witnesses(wl505),
        "a0-taxonomy": _project_taxonomy(wl522),
        "a0-inventory": _project_inventory(wl527),
    }
    _validate_a0_invariants(
        {
            key: documents[key]
            for key in ("a0-ledger", "a0-witnesses", "a0-taxonomy", "a0-inventory")
        }
    )
    return documents


def materialize_a0(
    source_results_dir: Path, baseline_commit: str, output_dir: Path
) -> dict[str, Path]:
    """Materialize the four A0 projections from explicitly named source files."""

    if _string(baseline_commit, "baseline_commit") != BASELINE_COMMIT:
        _fail(f"baseline_commit: expected {BASELINE_COMMIT}")
    documents = _materialize_a0_documents(Path(source_results_dir))
    output = Path(output_dir)
    paths = {}
    for kind in ("a0-ledger", "a0-witnesses", "a0-taxonomy", "a0-inventory"):
        path = output / CANONICAL_FILES[kind]
        _write_canonical(path, documents[kind])
        paths[kind] = path
    load_a0(output)
    return paths


def materialize_b0(source_results_dir: Path, baseline_commit: str, output_dir: Path) -> Path:
    """Materialize the selected B0 prototype rows from the explicit wl495 file."""

    if _string(baseline_commit, "baseline_commit") != BASELINE_COMMIT:
        _fail(f"baseline_commit: expected {BASELINE_COMMIT}")
    source, _ = _read_source_payload(Path(source_results_dir), "wl495")
    document = _project_b0(source)
    path = Path(output_dir) / CANONICAL_FILES["b0-prototype-rows"]
    _write_canonical(path, document)
    load_b0(Path(output_dir))
    return path


def materialize_manifest(source_results_dir: Path, baseline_commit: str, output_dir: Path) -> Path:
    """Bind canonical bytes to the five explicit source payloads and selectors."""

    if _string(baseline_commit, "baseline_commit") != BASELINE_COMMIT:
        _fail(f"baseline_commit: expected {BASELINE_COMMIT}")
    source_metadata = {}
    for _, work_log in PROJECTION_SPECS:
        _, raw = _read_source_payload(Path(source_results_dir), work_log)
        source_metadata[work_log] = {
            "source_payload_sha256": _sha256(raw),
            "source_payload_size": len(raw),
        }
    output = Path(output_dir)
    a0 = load_a0(output)
    b0 = load_b0(output)
    _validate_b0_against_a0(a0, b0)
    bindings = []
    for kind, work_log in PROJECTION_SPECS:
        canonical_path = output / CANONICAL_FILES[kind]
        raw = canonical_path.read_bytes()
        provenance = SOURCE_PROVENANCE[work_log]
        bindings.append(
            {
                "canonical_path": CANONICAL_FILES[kind],
                "canonical_projection_sha256": _sha256(raw),
                "canonical_projection_size": len(raw),
                "source_worklog": work_log,
                "source_worklog_path": provenance["source_worklog_path"],
                "source_script_path": provenance["source_script_path"],
                "source_test_paths": copy.deepcopy(provenance["source_test_paths"]),
                "source_result_path": provenance["source_result_path"],
                "source_selector": provenance["source_selector"],
                "source_payload_sha256": source_metadata[work_log]["source_payload_sha256"],
                "source_payload_size": source_metadata[work_log]["source_payload_size"],
                "consumer_paths": copy.deepcopy(provenance["consumer_paths"]),
            }
        )
    a2_payload = _load_json_object(output / "a2-boundary-spec.v1.json", "a2-boundary-spec")
    auxiliary_bindings = []
    for filename, work_logs in (
        (A1_CERTIFICATES_FILE, tuple(A1_SOURCE_FILENAMES)),
        ("a2-boundary-spec.v1.json", tuple(a2_payload["source_payloads"])),
    ):
        raw = (output / filename).read_bytes()
        auxiliary_bindings.append(
            {
                "canonical_path": filename,
                "canonical_projection_sha256": _sha256(raw),
                "canonical_projection_size": len(raw),
                "source_payloads": {
                    work_log: copy.deepcopy(a2_payload["source_payloads"][work_log])
                    for work_log in work_logs
                },
            }
        )
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "kind": "manifest",
        "materialization_kind": "a0_b0_canonical_projection",
        "baseline_commit": baseline_commit,
        "bindings": bindings,
        "auxiliary_bindings": auxiliary_bindings,
    }
    _validate_manifest(manifest)
    path = output / CANONICAL_FILES["manifest"]
    _write_canonical(path, manifest)
    load_manifest(path, output)
    return path


def materialize_all(
    source_results_dir: Path, baseline_commit: str, output_dir: Path
) -> dict[str, Path]:
    """Materialize A0, B0, and the manifest in one explicit operation."""

    paths: dict[str, Path] = {}
    paths.update(materialize_a0(source_results_dir, baseline_commit, output_dir))
    paths["b0-prototype-rows"] = materialize_b0(source_results_dir, baseline_commit, output_dir)
    paths["a1-certificates"] = materialize_a1_certificates(source_results_dir, output_dir)
    paths["a2-boundary-spec"] = materialize_a2_boundary_spec(source_results_dir, output_dir)
    paths["manifest"] = materialize_manifest(source_results_dir, baseline_commit, output_dir)
    return paths


def materialize_a1_certificates(source_results_dir: Path, output_dir: Path) -> Path:
    """Project the 12 post-A0 cover certificates from explicit legacy payloads.

    This is parity/materialization code only.  Runtime A1 loading uses the
    tracked JSON and never consults ``results/``.
    """

    source_results_dir = Path(source_results_dir)
    payloads = {
        work_log: _load_json_object(source_results_dir / filename, work_log)
        for work_log, filename in A1_SOURCE_FILENAMES.items()
    }
    a0 = load_a0(Path(output_dir))

    def family_key(row: dict[str, Any]) -> tuple[int, int, tuple[int, int, int]]:
        sample = row["sample"]
        d = row["complete_c_d_cover"]["d_vector"]
        return sample["L"], sample["T"], tuple(d[key] for key in D_VECTOR_KEYS)

    aliases = {}
    for row in a0.taxonomy:
        summary = row["cover_summary"]
        if not summary["d_vector"]:
            continue
        d = summary["d_vector"]
        key = summary["L"], summary["T"], tuple(d[name] for name in D_VECTOR_KEYS)
        aliases[key] = list(row["candidate_ids"])

    selected: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    selected.append(("wl500", payloads["wl500"]["routed_active_u5_supports"][0], {}))
    selected.extend(
        ("wl506", row, {})
        for row in payloads["wl506"]["resolved_deferred_entries"]
        if row["candidate_id"].startswith("AA_")
    )
    selected.extend(
        ("wl511", row, {})
        for row in payloads["wl511"]["routed_active_shell9_supports"]
        if row["candidate_id"].startswith("AA_")
        and row["ambient_c_d_global_solubility"]["status"] == "globally_soluble"
    )
    selected.append(("wl512", payloads["wl512"]["classified_deferred_entries"][0], {}))
    wl514_row = copy.deepcopy(payloads["wl514"]["classified_u7_entries"][0])
    wl514_row["ambient_c_d_global_solubility"] = payloads["wl514"][
        "shared_cover_resolution_certificate"
    ]
    selected.append(("wl514", wl514_row, {}))
    selected.extend(
        ("wl517", row, {})
        for row in payloads["wl517"]["routed_active_shell10_supports"]
        if row["candidate_id"].startswith("AA_")
        and row["ambient_c_d_global_solubility"]["status"] == "globally_soluble"
    )
    selected.append(("wl519", payloads["wl519"]["classified_shell10_u5_entries"][0], {}))

    rows = []
    seen = set()
    for work_log, source, _ in selected:
        key = family_key(source)
        if key in seen:
            continue
        seen.add(key)
        cover = source["complete_c_d_cover"]
        certificate = source["ambient_c_d_global_solubility"]
        status = certificate["status"]
        d = {name: cover["d_vector"][name] for name in D_VECTOR_KEYS}
        row = {
            "certificate_id": f"{work_log}-L{key[0]}-T{key[1]}-d{'-'.join(map(str, key[2]))}",
            "source_work_log": work_log,
            "consumed_at": [work_log],
            "candidate_ids": aliases[key],
            "status": status,
            "certificate_type": certificate["certificate_type"],
            "parameters": {name: cover["parameters"][name] for name in ("p", "q", "sqrt_q")},
            "d_vector": d,
        }
        if status == "globally_soluble":
            row["point_on_cover"] = copy.deepcopy(certificate["point_on_cover"])
            row["point_on_E_L"] = copy.deepcopy(certificate["induced_point_on_E_L"])
            if "mordell_weil_point_source" in certificate:
                row["mordell_weil_point_source"] = copy.deepcopy(
                    certificate["mordell_weil_point_source"]
                )
        else:
            if certificate["certificate_type"] == "mordell_weil_sieve_no_lift_mod_17":
                sieve = certificate["mod_17_sieve"]
                mw = certificate["mordell_weil_certificate"]
                row["no_lift"] = {
                    "method": "mordell_weil_sieve_mod_17",
                    "rank": mw["rank"],
                    "generator": mw["generator"],
                    "prime": sieve["prime"],
                    "legendre_symbol_7": sieve["legendre_symbol_7_mod_17"],
                    "rational_reduction_image": sieve["rational_reduction_image"],
                    "local_lift_candidate_reductions": sieve["local_lift_candidate_reductions"],
                    "rational_image_intersection": sieve[
                        "rational_image_intersection_with_local_lift_candidates"
                    ],
                }
            else:
                rank = certificate["rank_zero_certificate"]
                row["no_lift"] = {
                    "method": "torsion_exhaustion",
                    "rank": rank["rank"],
                    "torsion_points": rank["torsion_points"],
                    "lift_checks": copy.deepcopy(certificate["cover_lift_checks"]),
                }
        rows.append(row)
    rows.sort(key=lambda row: row["certificate_id"])
    if len(rows) != 12:
        _fail(f"a1-certificates: expected 12 deduplicated rows, got {len(rows)}")
    document = {"schema_version": 1, "kind": "a1-certificates", "rows": rows}
    path = Path(output_dir) / A1_CERTIFICATES_FILE
    _write_canonical(path, document)
    return path


def _a2_cover_rows(number: int, payload: dict[str, Any]) -> list[dict[str, Any]]:
    keys = {
        500: "routed_active_u5_supports",
        505: "routed_active_shell7_supports",
        506: "resolved_deferred_entries",
        511: "routed_active_shell9_supports",
        512: "classified_deferred_entries",
        514: "classified_u7_entries",
        517: "routed_active_shell10_supports",
        519: "classified_shell10_u5_entries",
    }
    rows = copy.deepcopy(payload[keys[number]])
    if number == 514:
        for row in rows:
            row["ambient_c_d_global_solubility"] = copy.deepcopy(
                payload["shared_cover_resolution_certificate"]
            )
    projected = []
    for row in rows:
        cover = row["complete_c_d_cover"]
        ambient = row["ambient_c_d_global_solubility"]
        item = {
            "candidate_id": row["candidate_id"],
            "sample": copy.deepcopy(row["sample"]),
            "d_vector": copy.deepcopy(cover["d_vector"]),
            "ambient_status": ambient["status"],
            "certificate_type": ambient["certificate_type"],
        }
        if ambient["status"] == "globally_soluble":
            if number == 505:
                item["point_ref"] = f"a0:{row['candidate_id']}"
            else:
                sample = row["sample"]
                values = tuple(cover["d_vector"][key] for key in D_VECTOR_KEYS)
                item["point_ref"] = (
                    f"a1:wl{number}-L{sample['L']}-T{sample['T']}-"
                    f"d{'-'.join(map(str, values))}"
                )
        projected.append(item)
    return projected


def _a2_stage_projection(number: int, payload: dict[str, Any]) -> dict[str, Any]:
    destination = A2_DESTINATIONS[number]
    stage: dict[str, Any] = {"destination": destination}
    if destination == "A1-SHELL":
        stage["shell_bound"] = {502: 6, 504: 7, 508: 8, 510: 9, 516: 10}[number]
        return stage
    if destination == "A1-COVER":
        stage["candidate_rows"] = _a2_cover_rows(number, payload)
        summary = payload.get("route_summary") or payload.get("resolution_summary")
        if summary is not None:
            stage["stage_summary"] = copy.deepcopy(summary)
        return stage
    if number in {518, 521}:
        stage["ledger_summary"] = copy.deepcopy(payload["ledger_summary"])
        stage["ledger_rows"] = [
            {
                "candidate_id": row["candidate_id"],
                "classification": row["classification"],
                "source_work_log": row["source_work_log"],
            }
            for row in payload["final_candidate_ledgers"]
        ]
        return stage
    if number == 522:
        pattern = next(
            row
            for row in payload["lemma_candidate_patterns"]
            if row["pattern_id"]
            == "common_source_square_obstruction_across_not_admissible_cover_families"
        )
        stage.update(
            taxonomy_summary=copy.deepcopy(payload["taxonomy_summary"]),
            selected_next_gate=copy.deepcopy(payload["selected_next_gate"]),
            lemma_pattern=copy.deepcopy(pattern),
        )
        return stage
    if number == 523:
        for key in ("proof_decision", "wl522_taxonomy_application", "selected_next_gate"):
            stage[key] = copy.deepcopy(payload[key])
        return stage
    if number == 525:
        for key in (
            "attempt_decision",
            "finite_input_snapshot",
            "precise_failure_point",
            "proof_obligation_audit",
            "uniform_lemma_target",
        ):
            stage[key] = copy.deepcopy(payload[key])
        return stage
    if number == 527:
        stage["scope_summary"] = copy.deepcopy(payload["scope_summary"])
        stage["proof_data_readiness_decision"] = copy.deepcopy(
            payload["proof_data_readiness_decision"]
        )
        return stage
    stage["selected_next_gate"] = copy.deepcopy(payload["selected_next_gate"])
    summaries = {
        key: copy.deepcopy(value)
        for key, value in payload.items()
        if key.endswith("route_state_summary")
    }
    if summaries:
        stage["route_state_summaries"] = summaries
    if number == 526:
        stage["route_choices"] = sorted(payload["route_families"])
    return stage


def materialize_a2_boundary_spec(source_results_dir: Path, output_dir: Path) -> Path:
    """Materialize compact semantic projections for every wl500-wl527 stage."""

    stages = {}
    sources = {}
    for number, suffix in A2_SOURCE_SUFFIXES.items():
        filename = f"closure_quotient_rank_zero_aa_bb_wl{number}_{suffix}.json"
        path = Path(source_results_dir) / filename
        raw = path.read_bytes()
        payload = json.loads(raw)
        stages[f"wl{number}"] = _a2_stage_projection(number, payload)
        sources[f"wl{number}"] = {
            "path": f"results/{filename}",
            "sha256": _sha256(raw),
            "size": len(raw),
        }
    document = {
        "schema_version": 1,
        "kind": "a2-boundary-spec",
        "work_logs": {f"wl{number}": A2_DESTINATIONS[number] for number in range(500, 528)},
        "route_choices": stages["wl526"]["route_choices"],
        "no_claims": {
            "broad_rank_or_selmer_diagnostics_run": False,
            "complete_selmer_upper_bound_proved": False,
            "dim_sel2_eq_2_claimed": False,
            "family_exclusion_proved": False,
            "final_obstruction_candidate_selected": False,
            "new_local_row_proved": False,
            "rank_zero_claimed": False,
            "sha2_trivial_claimed": False,
            "uniform_m_tail_full_rank_claimed": False,
        },
        "source_payloads": sources,
        "stages": stages,
    }
    path = Path(output_dir) / "a2-boundary-spec.v1.json"
    _write_canonical(path, document)
    return path


def load_all(path: Path) -> tuple[A0Bundle, B0Document, dict[str, Any]]:
    """Load the complete canonical directory without consulting legacy results."""

    directory = _canonical_directory(Path(path))
    manifest = load_manifest(directory / CANONICAL_FILES["manifest"], directory)
    a0 = load_a0(directory)
    b0 = load_b0(directory)
    _validate_b0_against_a0(a0, b0)
    return a0, b0, manifest


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--baseline-commit", required=True)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    paths = materialize_all(args.results_dir, args.baseline_commit, args.output_dir)
    for name, path in paths.items():
        print(f"{name}={path}")
    print("status=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
