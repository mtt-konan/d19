#!/usr/bin/env python3
# ruff: noqa: E402
"""Canonical D4 orchestration for the wl586 and wl593 route checkpoints.

The module consumes the tracked A0/A2/C3 evidence objects and composes the
five frozen D kernels through their dependency-aware entrypoints.  It keeps
the full certificates in memory for validation, while its serialized result
contains only the two semantic stage projections and small graph metadata.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb import (
    wl587_pure_u7_d0_relative_2_descent as pure_d0,
)
from scripts.theory.aa_bb import (
    wl589_mixed_d0_relative_2_descent as mixed_d0,
)
from scripts.theory.aa_bb import (
    wl590_p5_factor_twist_local_image_comparison as p5_kernel,
)
from scripts.theory.aa_bb import (
    wl591_mixed_p7_factor_twist_local_image as p7_kernel,
)
from scripts.theory.aa_bb import (
    wl592_mixed_p17_factor_twist_local_image as p17_kernel,
)
from scripts.theory.aa_bb.a1_certificates import build_a1, load_certificates
from scripts.theory.aa_bb.a2_evidence import (
    A2Evidence,
    build_a2,
    load_boundary_spec,
    project_a2,
)
from scripts.theory.aa_bb.c3_pure_v_ell import (
    C3Evidence,
    build_c3,
)
from scripts.theory.aa_bb.c3_pure_v_ell import (
    _strict_ready as strict_c3_ready,
)
from scripts.theory.aa_bb.c3_pure_v_ell import (
    project_stage as project_c3_stage,
)
from scripts.theory.aa_bb.c3_pure_v_ell import (
    semantic_projection as semantic_c3_projection,
)
from scripts.theory.aa_bb.consolidation_inputs import A0Bundle, load_a0

DEFAULT_DATA_DIR = ROOT / "data" / "theory" / "aa_bb" / "wl500"

D4_STAGES = ("wl586", "wl593")
KERNEL_ORDER = ("wl587", "wl589", "wl590", "wl591", "wl592")

WL586_ALLOWLIST = frozenset(
    {
        "work_log",
        "input_work_logs",
        "object_layer",
        "representative_selection_basis",
        "representative_cover_family_comparison",
        "cross_family_generic_squareclass_certificates",
        "generic_vs_uniform_boundary",
        "quartic_refinement_read_only_review",
        "invariant_tool_feasibility",
        "route_decision",
        "accepted_outcome",
        "certificate_scope",
        "shell11_executed_here",
        "new_supports_computed_here",
        "new_c_d_solubility_tested_here",
        "finite_search_used_as_progress",
        "equivalent_model_created_here",
        "quotient_created_here",
        "fixed_ell_rank_table_created_here",
        "advance_to_m3",
    }
)

WL593_ALLOWLIST = frozenset(
    {
        "work_log",
        "accepted_outcome",
        "input_work_logs",
        "object_layer",
        "local_image_quantifier",
        "fixed_input_comparison",
        "p5_comparison",
        "mixed_instance_chain",
        "frozen_boundaries",
        "conclusion",
        "proof_boundary",
        "verification",
    }
)

D4_ALLOWLISTS = {
    "wl586": WL586_ALLOWLIST,
    "wl593": WL593_ALLOWLIST,
}

_D0_DIGESTS = {
    "wl587": "e4406cc5bb66fc48f7fa5d002dee36791c1e222ea1a6a006a25eb8ef97a4aa7a",
    "wl589": "7bc1d1f2e63dff4886b1f26ac3f6191b31c5410e42bfbd3636a0269ad238fcaa",
}
_LOCAL_DIGESTS = {
    "wl590": "9e7a2e3c79046db502cb7d73cd5afce6125a6813edb7c751a03b5dc482a035d6",
    "wl591": "4cb74231e8a42615936b2a06d9e08755694c565db5c949466e27ce890b7cf943",
    "wl592": "1cb79e0e751e1c514ceb235131971e667640b7866a11c59bbf4d6d5e1817c507",
}

_WITNESS_IDS = frozenset(
    {
        "AA_A3_B7_u_3_plus_v_5_plus_w_17_m_tail_shell7_candidate",
        "AA_A6_B7_v_13_m_tail_shell7_candidate",
        "AA_A7_B2_u_7_m_tail_shell7_candidate",
        "AA_A7_B6_u_7_plus_v_13_plus_w_5_m_tail_shell7_candidate",
        "BB_A2_B7_u_7_m_tail_shell7_candidate",
        "BB_A6_B7_u_7_plus_v_13_plus_w_5_m_tail_shell7_candidate",
        "BB_A7_B3_u_3_plus_v_5_plus_w_17_m_tail_shell7_candidate",
        "BB_A7_B6_v_13_m_tail_shell7_candidate",
    }
)
_WITNESS_KEYS = frozenset(
    {
        "candidate_id",
        "candidate_support",
        "d_vector",
        "parameters",
        "point_on_E_L",
        "point_on_cover",
        "sample",
    }
)

REPRESENTATIVES = (
    {
        "role": "pure_v_base_family",
        "cover_family": "support=v_5|L=1|T=5|d=(5,1,5)",
        "support_family": "v_5",
        "L": 1,
        "T": 5,
        "d_vector": {
            "d_minus_p": 5,
            "d_neg_2sqrt_q": 5,
            "d_pos_2sqrt_q": 1,
        },
    },
    {
        "role": "pure_u_family",
        "cover_family": "support=u_7|L=7|T=9|d=(7,7,1)",
        "support_family": "u_7",
        "L": 7,
        "T": 9,
        "d_vector": {
            "d_minus_p": 7,
            "d_neg_2sqrt_q": 1,
            "d_pos_2sqrt_q": 7,
        },
    },
    {
        "role": "mixed_three_support_family",
        "cover_family": "support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85)",
        "support_family": "u_3+v_5+w_17",
        "L": 3,
        "T": 10,
        "d_vector": {
            "d_minus_p": 15,
            "d_neg_2sqrt_q": 85,
            "d_pos_2sqrt_q": 51,
        },
    },
)

GENERIC_CERTIFICATE_CANDIDATES = (
    "AA_A7_B2_u_7_m_tail_shell7_candidate",
    "AA_A3_B7_u_3_plus_v_5_plus_w_17_m_tail_shell7_candidate",
)

_EXPECTED_GENERIC = {
    GENERIC_CERTIFICATE_CANDIDATES[0]: {
        "cover_family": "support=u_7|L=7|T=9|d=(7,7,1)",
        "t_value": "69/4",
        "N_value": "105/8",
        "M_value": "-33/8",
        "opposite_product_value": "15172945/4096",
    },
    GENERIC_CERTIFICATE_CANDIDATES[1]: {
        "cover_family": "support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85)",
        "t_value": "17",
        "N_value": "27/2",
        "M_value": "-7/2",
        "opposite_product_value": "226625/16",
    },
}


@dataclass(frozen=True)
class D4Evidence:
    """In-memory D4 evidence with private kernel payloads for composition checks."""

    stages: dict[str, dict[str, Any]]
    kernels: dict[str, dict[str, Any]] = field(default_factory=dict, repr=False, compare=False)
    dependency_metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def __getitem__(self, work_log: str) -> dict[str, Any]:
        return self.stages[work_log]


def _payload_digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        dict(payload), sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def _failure(violations: list[str]) -> D4Evidence:
    unique = list(dict.fromkeys(violations)) or ["d4_validation_failed"]
    stages = {
        work_log: {
            "status": "issues",
            "ready": False,
            "work_log": work_log,
            "violations": unique.copy(),
        }
        for work_log in D4_STAGES
    }
    return D4Evidence(
        stages=stages,
        dependency_metadata={
            "protected_kernel_order": list(KERNEL_ORDER),
            "dependency_edges": {
                "wl590": ["wl587", "wl589"],
                "wl591": ["wl589"],
                "wl592": ["wl589"],
            },
        },
    )


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _root_data(parameters: Mapping[str, Any]) -> dict[str, int]:
    return {
        "e_minus": -int(parameters["p"]),
        "e_pos": 2 * int(parameters["sqrt_q"]),
        "e_neg": -2 * int(parameters["sqrt_q"]),
    }


def _validate_witness_rows(a0: A0Bundle) -> None:
    try:
        rows = a0.witnesses
    except (AttributeError, KeyError, TypeError) as exc:
        raise ValueError("a0_witnesses_missing") from exc
    if len(rows) != 8:
        raise ValueError("a0_witness_count")
    ids = [row.get("candidate_id") for row in rows if isinstance(row, Mapping)]
    if set(ids) != _WITNESS_IDS or len(ids) != len(set(ids)):
        raise ValueError("a0_witness_candidate_ids")
    selected = {row["candidate_id"]: row for row in rows}
    expected_selected = {
        "AA_A7_B2_u_7_m_tail_shell7_candidate": {
            "candidate_support": ["u_7"],
            "d_vector": {"d_minus_p": 7, "d_neg_2sqrt_q": 1, "d_pos_2sqrt_q": 7},
            "parameters": {"p": 230, "q": 76729, "sqrt_q": 277},
            "point_on_cover": {
                "X": 1562,
                "u_minus_p": 16,
                "u_neg_2sqrt_q": 46,
                "u_pos_2sqrt_q": 12,
            },
            "point_on_E_L": {"X": 1562, "Y": 61824},
            "sample": {
                "A": 7,
                "B": 2,
                "L": 7,
                "T": 9,
                "primitive": True,
                "side": "AA",
                "sqrt_q": 277,
            },
        },
        "AA_A3_B7_u_3_plus_v_5_plus_w_17_m_tail_shell7_candidate": {
            "candidate_support": ["u_3", "v_5", "w_17"],
            "d_vector": {"d_minus_p": 15, "d_neg_2sqrt_q": 85, "d_pos_2sqrt_q": 51},
            "parameters": {"p": -128, "q": 18496, "sqrt_q": 136},
            "point_on_cover": {
                "X": 1088,
                "u_minus_p": 8,
                "u_neg_2sqrt_q": 4,
                "u_pos_2sqrt_q": 4,
            },
            "point_on_E_L": {"X": 1088, "Y": 32640},
            "sample": {
                "A": 3,
                "B": 7,
                "L": 3,
                "T": 10,
                "primitive": True,
                "side": "AA",
                "sqrt_q": 136,
            },
        },
    }
    for row in rows:
        if not isinstance(row, Mapping) or set(row) != _WITNESS_KEYS:
            raise ValueError("a0_witness_shape")
        parameters = row["parameters"]
        d_vector = row["d_vector"]
        cover_point = row["point_on_cover"]
        curve_point = row["point_on_E_L"]
        support = row["candidate_support"]
        sample = row["sample"]
        if (
            not isinstance(support, list)
            or not support
            or not all(isinstance(value, str) for value in support)
            or not isinstance(parameters, Mapping)
            or set(parameters) != {"p", "q", "sqrt_q"}
            or not all(_is_int(parameters[key]) for key in parameters)
            or parameters["sqrt_q"] ** 2 != parameters["q"]
            or not isinstance(d_vector, Mapping)
            or set(d_vector) != {"d_minus_p", "d_neg_2sqrt_q", "d_pos_2sqrt_q"}
            or not all(_is_int(value) for value in d_vector.values())
            or not isinstance(cover_point, Mapping)
            or set(cover_point) != {"X", "u_minus_p", "u_neg_2sqrt_q", "u_pos_2sqrt_q"}
            or not all(_is_int(value) for value in cover_point.values())
            or not isinstance(curve_point, Mapping)
            or set(curve_point) != {"X", "Y"}
            or not all(_is_int(value) for value in curve_point.values())
            or curve_point["X"] != cover_point["X"]
            or not isinstance(sample, Mapping)
            or set(sample) != {"A", "B", "L", "T", "primitive", "side", "sqrt_q"}
            or not all(_is_int(sample[key]) for key in ("A", "B", "L", "T", "sqrt_q"))
            or sample["primitive"] is not True
            or not isinstance(sample["side"], str)
        ):
            raise ValueError(f"a0_witness_arithmetic:{row.get('candidate_id')}")
        product = d_vector["d_minus_p"] * d_vector["d_pos_2sqrt_q"] * d_vector["d_neg_2sqrt_q"]
        root = isqrt(product) if product >= 0 else -1
        equations_hold = (
            root >= 0
            and root * root == product
            and cover_point["X"] + parameters["p"]
            == d_vector["d_minus_p"] * cover_point["u_minus_p"] ** 2
            and cover_point["X"] - 2 * parameters["sqrt_q"]
            == d_vector["d_pos_2sqrt_q"] * cover_point["u_pos_2sqrt_q"] ** 2
            and cover_point["X"] + 2 * parameters["sqrt_q"]
            == d_vector["d_neg_2sqrt_q"] * cover_point["u_neg_2sqrt_q"] ** 2
            and curve_point["Y"]
            == root
            * cover_point["u_minus_p"]
            * cover_point["u_pos_2sqrt_q"]
            * cover_point["u_neg_2sqrt_q"]
        )
        if not equations_hold:
            raise ValueError(f"a0_witness_equations:{row.get('candidate_id')}")
    for candidate_id, expected in expected_selected.items():
        row = selected[candidate_id]
        if any(row[key] != value for key, value in expected.items()):
            raise ValueError(f"a0_selected_witness:{candidate_id}")


def _validate_a0(a0: Any) -> None:
    if not isinstance(a0, A0Bundle):
        raise ValueError("a0_type")
    try:
        counts = (len(a0.ledger), len(a0.witnesses), len(a0.taxonomy), len(a0.inventory))
    except (AttributeError, KeyError, TypeError) as exc:
        raise ValueError("a0_shape") from exc
    if counts != (43, 8, 22, 15):
        raise ValueError("a0_cardinality")
    if (
        not all(isinstance(row, Mapping) for row in a0.ledger)
        or len({row.get("candidate_id") for row in a0.ledger}) != 43
        or len({row.get("cover_family") for row in a0.taxonomy}) != 22
        or len({row.get("cover_family") for row in a0.inventory}) != 15
    ):
        raise ValueError("a0_row_identity")
    _validate_witness_rows(a0)


def _row_map(rows: Any, key: str) -> dict[str, Mapping[str, Any]]:
    if not isinstance(rows, list) or not all(isinstance(row, Mapping) for row in rows):
        raise ValueError(f"a2_{key}_rows")
    mapped = {str(row.get(key)): row for row in rows}
    if len(mapped) != len(rows):
        raise ValueError(f"a2_{key}_duplicates")
    return mapped


def _representative_rows(a2: A2Evidence) -> list[dict[str, Any]]:
    taxonomy = _row_map(list(a2.taxonomy), "cover_family")
    inventory = _row_map(list(a2.inventory), "cover_family")
    rows: list[dict[str, Any]] = []
    for expected in REPRESENTATIVES:
        cover_family = expected["cover_family"]
        tax = taxonomy.get(cover_family)
        inv = inventory.get(cover_family)
        if tax is None or inv is None:
            raise ValueError(f"a2_representative_missing:{cover_family}")
        summary = tax.get("cover_summary", {})
        model = inv.get("cover_family_model_availability", {})
        available = model.get("available_data", {})
        source_sides = inv.get("source_sides_to_map", [])
        valid = (
            tax.get("support_family") == expected["support_family"]
            and tax.get("classification") == "globally_soluble_but_not_aa_bb_admissible"
            and tax.get("failure_mode") == "common_source_aa_bb_admissibility_failure"
            and tax.get("entry_count") == 2
            and sorted(source_sides) == ["AA", "BB"]
            and summary.get("L") == expected["L"]
            and summary.get("T") == expected["T"]
            and summary.get("d_vector") == expected["d_vector"]
            and available.get("L") == expected["L"]
            and available.get("T") == expected["T"]
            and available.get("d_vector") == expected["d_vector"]
        )
        if not valid:
            raise ValueError(f"a2_representative_mismatch:{cover_family}")
        has_explicit_d = model.get("has_explicit_d_vector") is True
        model_status = (
            "label_and_l_t_d_vector_only_no_explicit_function_field_model"
            if has_explicit_d
            else "cover_label_only_missing_explicit_d_vector_and_equation"
        )
        is_pure_v = expected["role"] == "pure_v_base_family"
        rows.append(
            {
                **copy.deepcopy(expected),
                "taxonomy_verified": True,
                "entry_count": tax["entry_count"],
                "source_sides": copy.deepcopy(source_sides),
                "wl527_model_status": model_status,
                "post_wl527_explicit_model_and_maps_available": is_pure_v,
                "post_wl527_evidence": (
                    "wl528-wl585 pure-v_ell prototype and exact lifts"
                    if is_pure_v
                    else "none; wl527 has only L,T,d labels"
                ),
                "uniform_squareclass_certificate_available": False,
            }
        )
    return rows


def _validate_a2(a0: A0Bundle, a2: Any) -> None:
    if not isinstance(a2, A2Evidence):
        raise ValueError("a2_type")
    try:
        if (len(a2.ledger), len(a2.taxonomy), len(a2.inventory)) != (43, 22, 15):
            raise ValueError("a2_cardinality")
        if (
            list(a2.ledger) != list(a0.ledger)
            or list(a2.taxonomy) != list(a0.taxonomy)
            or list(a2.inventory) != list(a0.inventory)
        ):
            raise ValueError("a0_a2_projection_mismatch")
        wl522 = project_a2(a2, "wl522")
        wl527 = project_a2(a2, "wl527")
        taxonomy_summary = wl522["taxonomy_summary"]
        if (
            taxonomy_summary["globally_soluble_but_not_aa_bb_admissible_cover_family_count"] != 15
            or taxonomy_summary["globally_soluble_but_not_aa_bb_admissible_entry_count"] != 29
        ):
            raise ValueError("a2_wl522_summary")
        decision = wl527["proof_data_readiness_decision"]
        if (
            decision["ready_for_later_uniform_squareclass_proof_attempt"] is not False
            or decision["exact_missing_data_class"]
            != "uniform_function_field_model_maps_and_squareclass_certificate"
            or decision["uniform_lemma_proved_here"] is not False
            or decision["mathematical_uniform_lemma_refuted_here"] is not False
            or decision["finite_taxonomy_promoted_here"] is not False
        ):
            raise ValueError("a2_wl527_decision")
        _representative_rows(a2)
    except (KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, ValueError) and str(exc).startswith("a2_"):
            raise
        raise ValueError("a2_projection") from exc


def _validate_c3(c3: Any) -> dict[str, Any]:
    if not isinstance(c3, C3Evidence):
        raise ValueError("c3_type")
    try:
        if tuple(c3.stages) != tuple(f"wl{number}" for number in range(569, 586)):
            raise ValueError("c3_stage_order")
        if not strict_c3_ready(c3):
            raise ValueError("c3_not_ready")
        stage = project_c3_stage(c3, "wl585")
        semantic_c3_projection(stage, "wl585")
        if (
            stage["status"] != "ok"
            or stage["ready"] is not True
            or stage["violations"] != []
            or stage["work_log"] != "wl585"
            or stage["cover_certificate"]["cover_degree"] != 16
            or stage["cover_certificate"]["genus"] != 17
            or stage["proof_status"]["combined_rational_elliptic_quotient_proved_here"] is not True
            or stage["proof_status"]["restricted_combined_elliptic_image_solved_here"] is not False
            or stage["proof_status"]["uniform_full_wl535_obstruction_proved_here"] is not False
            or stage["advance_to_m3"] is not False
        ):
            raise ValueError("c3_wl585_boundary")
        return stage
    except (KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, ValueError) and str(exc).startswith("c3_"):
            raise
        raise ValueError("c3_projection") from exc


def _quartic_review() -> dict[str, Any]:
    return {
        "review_only": True,
        "candidate": "parameter-prime quartic character of B/(2*r)",
        "positive_norm_formula": "theta_ell=Legendre(a,ell)",
        "negative_norm_formula": "theta_ell=chi4_ell(-1)*Legendre(b,ell)",
        "sign_comparison": ("Legendre(a,ell)*Legendre(b,ell)=Legendre(2,ell)=chi4_ell(-1)"),
        "determined_values": {
            "ell_1_mod_8": "+1",
            "ell_5_mod_8_r_1_mod_8": "+1",
            "ell_5_mod_8_r_7_mod_8": "-1",
        },
        "dependency_set": ["ell_mod_8", "canonical_r_mod_8"],
        "verdict": "automatic_collapse_to_existing_gaussian_data",
        "independent_invariant": False,
        "wl588_permitted_by_stop_rule": False,
    }


def _is_rational_square(value: Fraction) -> bool:
    return (
        value >= 0
        and isqrt(value.numerator) ** 2 == value.numerator
        and isqrt(value.denominator) ** 2 == value.denominator
    )


def _generic_certificates(a0: A0Bundle) -> list[dict[str, Any]]:
    routed = {row["candidate_id"]: row for row in a0.witnesses}
    family_by_support = {
        expected["support_family"]: expected["cover_family"] for expected in REPRESENTATIVES
    }
    certificates: list[dict[str, Any]] = []
    for candidate_id in GENERIC_CERTIFICATE_CANDIDATES:
        row = routed[candidate_id]
        parameters = row["parameters"]
        roots = _root_data(parameters)
        d_vector = row["d_vector"]
        cover_point = row["point_on_cover"]
        curve_point = row["point_on_E_L"]
        d_product = d_vector["d_minus_p"] * d_vector["d_pos_2sqrt_q"] * d_vector["d_neg_2sqrt_q"]
        d_scale = isqrt(d_product)
        x_coord = cover_point["X"]
        y_coord = curve_point["Y"]
        denominator = 2 * (x_coord + parameters["p"])
        if denominator == 0:
            raise ValueError(f"generic_denominator:{candidate_id}")
        t = Fraction(y_coord, denominator)
        sample = row["sample"]
        n = (Fraction(sample["A"]) + Fraction(sample["B"]) + t) / 2
        m = Fraction(sample["A"]) + Fraction(sample["B"]) - n
        opposite_product = (n * n + sample["B"] ** 2) * (m * m + sample["B"] ** 2)
        roots_hold = (
            x_coord - roots["e_minus"] == d_vector["d_minus_p"] * cover_point["u_minus_p"] ** 2
            and x_coord - roots["e_pos"]
            == d_vector["d_pos_2sqrt_q"] * cover_point["u_pos_2sqrt_q"] ** 2
            and x_coord - roots["e_neg"]
            == d_vector["d_neg_2sqrt_q"] * cover_point["u_neg_2sqrt_q"] ** 2
            and y_coord
            == d_scale
            * cover_point["u_minus_p"]
            * cover_point["u_pos_2sqrt_q"]
            * cover_point["u_neg_2sqrt_q"]
        )
        geometrically_integral = (
            d_product != 0
            and roots["e_pos"] - roots["e_minus"] != 0
            and roots["e_neg"] - roots["e_minus"] != 0
            and roots["e_pos"] != roots["e_neg"]
        )
        minors = (
            4
            * d_vector["d_minus_p"]
            * d_vector["d_pos_2sqrt_q"]
            * cover_point["u_minus_p"]
            * cover_point["u_pos_2sqrt_q"],
            -4
            * d_vector["d_minus_p"]
            * d_vector["d_neg_2sqrt_q"]
            * cover_point["u_minus_p"]
            * cover_point["u_neg_2sqrt_q"],
            4
            * d_vector["d_pos_2sqrt_q"]
            * d_vector["d_neg_2sqrt_q"]
            * cover_point["u_pos_2sqrt_q"]
            * cover_point["u_neg_2sqrt_q"],
        )
        smooth = any(value != 0 for value in minors)
        expected = _EXPECTED_GENERIC[candidate_id]
        values_match = (
            str(t) == expected["t_value"]
            and str(n) == expected["N_value"]
            and str(m) == expected["M_value"]
            and str(opposite_product) == expected["opposite_product_value"]
        )
        certified = (
            sample["side"] == "AA"
            and d_scale * d_scale == d_product
            and roots_hold
            and geometrically_integral
            and denominator != 0
            and smooth
            and opposite_product > 0
            and not _is_rational_square(opposite_product)
            and values_match
        )
        if not certified:
            raise ValueError(f"generic_certificate:{candidate_id}")
        support = "+".join(row["candidate_support"])
        certificates.append(
            {
                "candidate_id": candidate_id,
                "cover_family": family_by_support.get(support, expected["cover_family"]),
                "function": "(N^2+B^2)*(M^2+B^2)",
                "t_value": str(t),
                "N_value": str(n),
                "M_value": str(m),
                "opposite_product_value": str(opposite_product),
                "smooth_nonexceptional_rational_specialization": smooth and denominator != 0,
                "geometrically_integral_biquadratic_cover": geometrically_integral,
                "value_is_rational_square": _is_rational_square(opposite_product),
                "function_field_squareclass": "nonsquare",
                "certified": certified,
            }
        )
    return certificates


def _tool_feasibility() -> list[dict[str, Any]]:
    return [
        {
            "tool": "parameter_prime_gaussian_characters",
            "families_with_inputs": ["pure_v_base_family"],
            "cross_family_ready": False,
            "independent_on_pure_v": False,
            "verdict": "route_dead",
            "reason": "all tested characters are functions of existing Gaussian data",
        },
        {
            "tool": "restricted_elliptic_image",
            "families_with_inputs": ["pure_v_base_family"],
            "cross_family_ready": False,
            "independent_on_pure_v": False,
            "verdict": "route_dead_as_current_quotient",
            "reason": "the required restricted image restores every original lift",
        },
        {
            "tool": "opposite_side_function_field_divisor_parity",
            "families_with_inputs": [
                "pure_v_base_family",
                "pure_u_family",
                "mixed_three_support_family",
            ],
            "cross_family_ready": True,
            "independent_on_pure_v": True,
            "verdict": "generic_nonsquare_only_not_uniform_point_obstruction",
            "reason": (
                "smooth specializations prove the function is nonsquare in "
                "two more function fields, but nonsquare functions can have "
                "square rational specializations"
            ),
        },
        {
            "tool": "point_level_common_source_nonsquare",
            "families_with_inputs": [
                "pure_v_base_family",
                "pure_u_family",
                "mixed_three_support_family",
            ],
            "cross_family_ready": True,
            "independent_on_pure_v": False,
            "verdict": "finite_signal_only",
            "reason": "pointwise failures do not define a uniform family invariant",
        },
    ]


def _build_wl586(a0: A0Bundle, a2: A2Evidence) -> dict[str, Any]:
    return {
        "status": "ok",
        "ready": True,
        "work_log": "wl586",
        "input_work_logs": ["wl505", "wl522", "wl527", "wl585"],
        "object_layer": "cross_family_route_truth_audit",
        "representative_selection_basis": [
            "pure v support with the only post-wl527 explicit prototype",
            "pure u support with both AA and BB point-level failures",
            "mixed u+v+w support with all three d coordinates nontrivial",
        ],
        "representative_cover_family_comparison": _representative_rows(a2),
        "cross_family_generic_squareclass_certificates": _generic_certificates(a0),
        "generic_vs_uniform_boundary": {
            "same_function_definition_on_two_cover_families": True,
            "function_field_nonsquare_on_two_cover_families": True,
            "all_rational_specializations_nonsquare_proved": False,
            "uniform_aa_bb_exclusion_invariant_proved": False,
            "reason": (
                "a nonsquare function-field element may specialize to a square; "
                "each square-specialization locus is a new double cover"
            ),
        },
        "quartic_refinement_read_only_review": _quartic_review(),
        "invariant_tool_feasibility": _tool_feasibility(),
        "route_decision": {
            "reenter_wl535_now": False,
            "pure_v_ell_equivalent_model_route": "route_dead",
            "pure_v_ell_parameter_character_route": "route_dead",
            "representative_only_divisor_parity_route": "route_dead_as_uniform_exclusion",
            "wl588_created": False,
            "cross_family_uniform_invariant_proved_here": False,
            "cross_family_generic_invariant_proved_here": True,
            "selected_next_route": "none_without_parameterized_family_level_input",
            "next_route_success_gate": "not_entered",
            "supporting_models_are_not_progress_by_themselves": True,
        },
        "accepted_outcome": "route_death_certificate",
        "certificate_scope": {
            "kills_all_possible_future_invariants": False,
            "kills_current_pure_v_equivalent_models": True,
            "kills_characters_derived_only_from_existing_gaussian_factors": True,
            "kills_unrestricted_fixed_ell_rank_tables": True,
            "kills_generic_nonsquare_as_uniform_exclusion": True,
            "proves_wl535": False,
            "finds_strict_counterexample": False,
            "proves_complete_selmer_upper_bound": False,
        },
        "shell11_executed_here": False,
        "new_supports_computed_here": False,
        "new_c_d_solubility_tested_here": False,
        "finite_search_used_as_progress": False,
        "equivalent_model_created_here": False,
        "quotient_created_here": False,
        "fixed_ell_rank_table_created_here": False,
        "advance_to_m3": False,
        "violations": [],
    }


def _ready(payload: Mapping[str, Any], work_log: str) -> bool:
    verification = payload.get("verification")
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == work_log
        and isinstance(verification, Mapping)
        and verification.get("violations") == []
    )


def _all_true(values: Any) -> bool:
    return (
        isinstance(values, Mapping)
        and bool(values)
        and all(value is True for value in values.values())
    )


def _contains_all(values: list[Any], needles: tuple[str, ...]) -> bool:
    text = " ".join(str(value) for value in values)
    return all(needle in text for needle in needles)


def _d0_snapshot(payload: Mapping[str, Any]) -> dict[str, Any]:
    source = payload["source_cover"]
    divisors = payload["divisors_and_branch_cover"]
    local = payload["local_exception_and_bad_fiber_data"]
    return {
        "base": source["base"],
        "scope": payload["scope"],
        "parameters": source["parameters"],
        "source_data": source["function_field"],
        "factor_data": {
            "factor_functions": divisors["factor_functions"],
            "factor_covering_equations": divisors["factor_covering_equations"],
        },
        "bad_prime_support": local["bad_fiber_set"]["S"],
        "aa_bb_exact_conditions": payload["aa_bb_lift"]["exact_conditions"],
    }


def _fixed_input_comparison(pure: Mapping[str, Any], mixed: Mapping[str, Any]) -> dict[str, Any]:
    bases = {
        "pure_u7": _d0_snapshot(pure),
        "mixed_u3_v5_w17": _d0_snapshot(mixed),
    }
    pure_source = pure["source_cover"]
    mixed_source = mixed["source_cover"]
    pure_divisors = pure["divisors_and_branch_cover"]
    mixed_divisors = mixed["divisors_and_branch_cover"]
    difference_checks = {
        "coefficient_data_differ": pure_source["parameters"] != mixed_source["parameters"],
        "source_data_differ": pure_source["function_field"] != mixed_source["function_field"],
        "factor_data_differ": (
            pure_divisors["factor_functions"] != mixed_divisors["factor_functions"]
            and pure_divisors["factor_covering_equations"]
            != mixed_divisors["factor_covering_equations"]
        ),
        "bad_prime_supports_differ": bases["pure_u7"]["bad_prime_support"]
        != bases["mixed_u3_v5_w17"]["bad_prime_support"],
    }
    return {"bases": bases, "difference_checks": difference_checks}


def _d0_checks(pure: Mapping[str, Any], mixed: Mapping[str, Any]) -> dict[str, bool]:
    pure_boundary = pure["proof_boundary"]
    mixed_boundary = mixed["proof_boundary"]
    return {
        "wl587_ready_fixed_input": _ready(pure, "wl587"),
        "wl589_ready_fixed_input": _ready(mixed, "wl589"),
        "wl587_base_is_Spec_Q": pure["source_cover"]["base"] == "Spec(Q)",
        "wl589_base_is_Spec_Q": mixed["source_cover"]["base"] == "Spec(Q)",
        "wl587_scope_is_fixed": pure["scope"] == "support=u_7|L=7|T=9|d=(7,7,1), R^2=P_op only",
        "wl589_scope_is_fixed": mixed["scope"]
        == "support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85), R^2=P_op only",
        "wl587_is_D0_not_family_theorem": (
            pure_boundary["D0_certificate_proved_here"] is True
            and pure_boundary["family_exclusion"] is False
            and pure_boundary["theorem_level_selmer_claim"] is False
        ),
        "wl589_is_D0_not_family_theorem": (
            mixed_boundary["D0_certificate_proved_here"] is True
            and mixed_boundary["family_exclusion"] is False
            and mixed_boundary["theorem_level_selmer_claim"] is False
        ),
    }


def _p5_comparison(payload: Mapping[str, Any]) -> dict[str, Any]:
    images = payload["local_images"]
    return {
        "prime": payload["prime"],
        "scope": payload["scope"],
        "pure_u7_image": images["pure_u7"],
        "mixed_u3_v5_w17_image": images["mixed_u3_v5_w17"],
        "images_disagree": images["pure_u7"] != images["mixed_u3_v5_w17"],
        "certificate_ready": _ready(payload, "wl590"),
    }


def _mixed_instance_chain(
    p5: Mapping[str, Any], p7: Mapping[str, Any], p17: Mapping[str, Any]
) -> dict[str, Any]:
    p5_mixed = p5["named_survivor_mapping"]["mixed_u3_v5_w17"]
    p7_mapping = p7["named_survivor_mapping"]
    return {
        "p5_survivors": p5_mixed["survive"],
        "p7_prime": p7["prime"],
        "p7_scope": p7["scope"],
        "p7_image": p7["local_image"],
        "p7_survivors": p7_mapping["survive"],
        "p17_prime": p17["prime"],
        "p17_scope": p17["scope"],
        "p17_image": p17["local_image"],
        "p17_target": p17["target_twist"],
        "p17_target_class": p17["target_twist_class"],
        "p17_target_in_image": p17["target_twist_in_image"],
        "instance_specific": (
            p7["scope"]
            == "frozen wl589 mixed cover support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85) at p=7 only"
            and p17["scope"]
            == "frozen wl589 mixed cover support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85) at p=17 only"
            and p7["object_layer"] == "normalized_mixed_Q7_relative_constant_factor_twist_image"
            and p17["object_layer"] == "normalized_mixed_Q17_relative_constant_factor_twist_image"
            and _ready(p7, "wl591")
            and _ready(p17, "wl592")
        ),
    }


def _frozen_boundary_certificate(
    pure: Mapping[str, Any],
    mixed: Mapping[str, Any],
    p5: Mapping[str, Any],
    p7: Mapping[str, Any],
    p17: Mapping[str, Any],
) -> dict[str, Any]:
    p5_pure_map = p5["fixed_cover_and_lift"]["pure_u7"]
    p5_mixed_map = p5["fixed_cover_and_lift"]["mixed_u3_v5_w17"]
    p7_maps = p7["proof_certificate"]["frozen_maps_certificate"]
    p17_maps = p17["proof_certificate"]["frozen_maps_certificate"]
    pure_conditions = p5_pure_map["aa_bb_conditions"]
    mixed_conditions = p5_mixed_map["aa_bb_conditions"]
    checks = {
        "wl587_exact_aa_bb_checks": _all_true(pure["aa_bb_lift"]["structural_checks"]),
        "wl589_exact_aa_bb_checks": _all_true(mixed["aa_bb_lift"]["structural_checks"]),
        "wl590_all_pole_infinity_factor_zero_checks": (
            _all_true(p5["verification"]["checks"])
            and _all_true(p5["proof_certificate"]["pure_u7"]["checks"])
            and _all_true(p5["proof_certificate"]["mixed_u3_v5_w17"]["checks"])
            and _contains_all(
                [p5["verification"]["strict_certificate"]],
                ("poles", "projective boundaries", "factor-zero", "AA+BB"),
            )
        ),
        "wl591_all_pole_infinity_factor_zero_checks": (
            _all_true(p7["verification"]["local_checks"])
            and _contains_all(
                [p7["strict_certificate"]],
                ("infinity", "D/A", "factor-zero", "fixed-cover R", "AA+BB"),
            )
        ),
        "wl592_all_pole_infinity_factor_zero_checks": (
            _all_true(p17["verification"]["local_checks"])
            and _contains_all(
                [p17["strict_certificate"]],
                ("infinity", "D/A", "factor-zero", "fixed cover R", "AA+BB"),
            )
        ),
        "wl590_fixed_cover_R_maps_retained": (
            p5_pure_map["identity_check"] is True
            and p5_mixed_map["identity_check"] is True
            and "R=d*a_plus*a_minus" in p5_pure_map["fixed_cover_map"]
            and "R=d*a_plus*a_minus" in p5_mixed_map["fixed_cover_map"]
        ),
        "wl591_fixed_cover_R_map_retained": (
            _all_true(p7_maps["checks"])
            and p7_maps["fixed_cover_equation"] == "R^2=(N^2+49)*(M^2+49)"
        ),
        "wl592_fixed_cover_R_map_retained": (
            _all_true(p17_maps["checks"])
            and p17_maps["fixed_cover_equation"] == "R^2=(N^2+49)*(M^2+49)"
        ),
        "wl590_positivity_and_aa_bb_retained": (
            _contains_all(
                pure_conditions,
                ("-9<t<9", "(N^2+49)*(M^2+49)=(Z/4)^2"),
            )
            and _contains_all(
                mixed_conditions,
                ("-10<t<10", "(N^2+9)*(M^2+9)=(Z/4)^2"),
            )
        ),
        "wl591_positivity_and_aa_bb_retained": _contains_all(
            p7_maps["exact_aa_bb_lift"],
            ("-10<t<10", "(N^2+9)*(M^2+9)=(Z/4)^2"),
        ),
        "wl592_positivity_and_aa_bb_retained": _contains_all(
            p17_maps["exact_aa_bb_lift"],
            ("-10<t<10", "(N^2+9)*(M^2+9)=(Z/4)^2"),
        ),
    }
    return {
        "checks": checks,
        "positivity_intervals": {
            "pure_u7": next(item for item in pure_conditions if item.startswith("-9<t<9")),
            "mixed_u3_v5_w17": next(
                item for item in mixed_conditions if item.startswith("-10<t<10")
            ),
        },
        "fixed_cover_equations": {
            "pure_u7": p5_pure_map["fixed_cover_map"].split(", ", 1)[1],
            "mixed_u3_v5_w17": p5_mixed_map["fixed_cover_map"].split(", ", 1)[1],
        },
        "aa_bb_source_products": {
            "pure_u7": pure_conditions[0],
            "mixed_u3_v5_w17": mixed_conditions[0],
        },
    }


def _build_wl593(
    pure: Mapping[str, Any],
    mixed: Mapping[str, Any],
    p5: Mapping[str, Any],
    p7: Mapping[str, Any],
    p17: Mapping[str, Any],
) -> dict[str, Any]:
    fixed_input_comparison = _fixed_input_comparison(pure, mixed)
    d0_checks = _d0_checks(pure, mixed)
    p5_comparison = _p5_comparison(p5)
    mixed_instance_chain = _mixed_instance_chain(p5, p7, p17)
    frozen_boundaries = _frozen_boundary_certificate(pure, mixed, p5, p7, p17)
    checks = {
        "only_frozen_wl587_wl589_wl590_wl591_wl592_inputs": list(KERNEL_ORDER)
        == ["wl587", "wl589", "wl590", "wl591", "wl592"],
        **d0_checks,
        **{
            f"input_difference_{name}": passed
            for name, passed in fixed_input_comparison["difference_checks"].items()
        },
        "p5_certificate_is_ready": p5_comparison["certificate_ready"],
        "p5_local_images_disagree": p5_comparison["images_disagree"]
        and p5_comparison["prime"] == 5
        and p5_comparison["scope"]
        == "p=5 local factor-twist images for frozen wl587 and wl589 only",
        "mixed_p7_p17_chain_is_instance_specific": mixed_instance_chain["instance_specific"],
        "mixed_chain_starts_with_exact_p5_survivors": mixed_instance_chain["p5_survivors"]
        == [5, 3045, 66045, 91205],
        "mixed_p7_keeps_only_91205": mixed_instance_chain["p7_survivors"] == [91205]
        and mixed_instance_chain["p7_image"] == ["[1]"],
        "mixed_p17_excludes_91205": (
            mixed_instance_chain["p17_target"] == 91205
            and mixed_instance_chain["p17_target_class"] == "[17u]"
            and mixed_instance_chain["p17_target_in_image"] is False
            and mixed_instance_chain["p17_image"] == ["[u]"]
        ),
        **{f"boundary_{name}": passed for name, passed in frozen_boundaries["checks"].items()},
    }
    violations = [name for name, passed in checks.items() if not passed]
    return {
        "status": "ok" if not violations else "issues",
        "ready": not violations,
        "work_log": "wl593",
        "accepted_outcome": "route_death_certificate",
        "input_work_logs": list(KERNEL_ORDER),
        "object_layer": "fixed_representative_factor_twist_local_image_generalization",
        "local_image_quantifier": (
            "For each frozen representative j, selected prime p, and [d] in "
            "Q_p^*/Q_p^{*2}, [d] is in I_{p,j} iff there exists a Q_p-point "
            "(c,a_plus,a_minus,R) on the already audited complete normalized "
            "factor-cover charts, including finite, pole, infinity, factor-zero, "
            "and R=0 charts, with d in Q_p^* and F_plus(c)=d*a_plus^2, "
            "F_minus(c)=d*a_minus^2, and R=d*a_plus*a_minus.  The real positivity "
            "interval and exact AA+BB source-product lift remain global boundaries "
            "and are not added as a p-adic filter."
        ),
        "fixed_input_comparison": fixed_input_comparison,
        "p5_comparison": p5_comparison,
        "mixed_instance_chain": mixed_instance_chain,
        "frozen_boundaries": frozen_boundaries,
        "conclusion": (
            "The current fixed-representative factor-twist local-image mechanism "
            "cannot be promoted from these fixed inputs alone; it requires new "
            "parameterized family-level coefficient/local-image input."
        ),
        "proof_boundary": {
            "all_relative_2_descent_impossible": False,
            "family_level_local_image_theorem": False,
            "new_parameterized_family_added": False,
            "new_prime_or_local_row_added": False,
            "new_equivalent_model_or_quotient_added": False,
            "rank_computation": False,
            "rational_point_search": False,
            "D2": False,
            "D5": False,
            "Selmer_claim": False,
        },
        "verification": {
            "checks": checks,
            "violations": violations,
            "strict_certificate": (
                "Only wl587/wl589 and wl590-wl592 are imported.  The certificate "
                "compares fixed Spec(Q) coefficient/source/factor data, the "
                "bad-prime supports, the p=5 image disagreement, and the "
                "mixed p=7,p=17 instance chain.  All audited pole, infinity, "
                "factor-zero, positivity, fixed-cover R, and AA+BB boundaries "
                "remain in scope; no family-level local-image input is supplied."
            ),
        },
    }


def _validate_kernel(name: str, payload: Any) -> None:
    if not isinstance(payload, Mapping):
        raise ValueError(f"kernel_payload_type:{name}")
    expected_work_log = name
    try:
        digest = _payload_digest(payload)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"kernel_payload_encoding:{name}") from exc
    expected_digest = _D0_DIGESTS.get(name, _LOCAL_DIGESTS.get(name))
    if digest != expected_digest:
        raise ValueError(f"kernel_payload_digest:{name}")
    if not _ready(payload, expected_work_log):
        raise ValueError(f"kernel_payload_not_ready:{name}")


def _default_kernels() -> dict[str, Callable[..., dict[str, Any]]]:
    return {
        "wl587": pure_d0.build_wl587_pure_u7_d0_relative_2_descent,
        "wl589": mixed_d0.build_wl589_mixed_d0_relative_2_descent,
        "wl590": p5_kernel.build_wl590_from_d0,
        "wl591": p7_kernel.build_wl591_from_mixed_d0,
        "wl592": p17_kernel.build_wl592_from_mixed_d0,
    }


def _injected_kernels(kernels: Any) -> dict[str, Callable[..., dict[str, Any]]]:
    if not isinstance(kernels, Mapping) or tuple(kernels) != KERNEL_ORDER:
        raise ValueError("kernel_injection_shape")
    functions = dict(kernels)
    if not all(callable(functions[name]) for name in KERNEL_ORDER):
        raise ValueError("kernel_injection_callable")
    return functions


def build_d4(
    *,
    a0: A0Bundle,
    a2: A2Evidence,
    c3: C3Evidence,
    kernels: Mapping[str, Callable[..., dict[str, Any]]] | None = None,
) -> D4Evidence:
    """Build D4 with one call per protected kernel and fail closed on drift."""

    try:
        _validate_a0(a0)
        _validate_a2(a0, a2)
        _validate_c3(c3)
        wl586 = _build_wl586(a0, a2)
    except Exception as exc:
        return _failure([str(exc) or "canonical_input_validation_failed"])

    try:
        functions = _default_kernels() if kernels is None else _injected_kernels(kernels)
        pure = functions["wl587"]()
        _validate_kernel("wl587", pure)
        mixed = functions["wl589"]()
        _validate_kernel("wl589", mixed)
        p5 = functions["wl590"](pure, mixed)
        _validate_kernel("wl590", p5)
        p7 = functions["wl591"](mixed)
        _validate_kernel("wl591", p7)
        p17 = functions["wl592"](mixed)
        _validate_kernel("wl592", p17)
        wl593 = _build_wl593(pure, mixed, p5, p7, p17)
        if wl593["status"] != "ok" or wl593["ready"] is not True:
            raise ValueError("wl593_semantic_validation")
    except Exception as exc:
        return _failure([str(exc) or "protected_kernel_validation_failed"])

    return D4Evidence(
        stages={"wl586": wl586, "wl593": wl593},
        kernels={"wl587": pure, "wl589": mixed, "wl590": p5, "wl591": p7, "wl592": p17},
        dependency_metadata={
            "protected_kernel_order": list(KERNEL_ORDER),
            "dependency_edges": {
                "wl590": ["wl587", "wl589"],
                "wl591": ["wl589"],
                "wl592": ["wl589"],
            },
            "d0_payloads_rebuilt_by_composition": False,
        },
    )


def _stages_for(evidence: D4Evidence | Mapping[str, Any]) -> Mapping[str, Any]:
    if isinstance(evidence, D4Evidence):
        return evidence.stages
    if isinstance(evidence, Mapping):
        stages = evidence.get("stages", evidence)
        if isinstance(stages, Mapping):
            return stages
    raise TypeError("D4 evidence must be a D4Evidence or mapping")


def project_stage(evidence: D4Evidence | Mapping[str, Any], work_log: str) -> dict[str, Any]:
    """Return one full D4 stage after enforcing exact order and labels."""

    if work_log not in D4_STAGES:
        raise KeyError(f"unknown D4 work log: {work_log}")
    stages = _stages_for(evidence)
    if tuple(stages) != D4_STAGES:
        raise KeyError("D4 stage set or order mismatch")
    payload = stages.get(work_log)
    if not isinstance(payload, Mapping):
        raise ValueError(f"invalid D4 stage payload for {work_log}")
    if payload.get("work_log") != work_log:
        raise ValueError(f"D4 stage label mismatch for {work_log}")
    return copy.deepcopy(dict(payload))


def semantic_projection(payload: Mapping[str, Any], work_log: str) -> dict[str, Any]:
    """Project a ready stage onto its explicit semantic allowlist."""

    if work_log not in D4_STAGES:
        raise KeyError(f"unknown D4 work log: {work_log}")
    if not isinstance(payload, Mapping):
        raise ValueError(f"invalid D4 stage payload for {work_log}")
    allowed = D4_ALLOWLISTS[work_log]
    unknown = set(payload) - allowed - {"status", "ready", "violations"}
    if unknown:
        raise ValueError(f"unallowlisted D4 fields for {work_log}: {sorted(unknown)}")
    missing = allowed - set(payload)
    if missing:
        raise ValueError(f"missing D4 fields for {work_log}: {sorted(missing)}")
    if (
        payload.get("status") != "ok"
        or payload.get("ready") is not True
        or payload.get("work_log") != work_log
    ):
        raise ValueError(f"D4 stage is not ready: {work_log}")
    if work_log == "wl586" and payload.get("violations") != []:
        raise ValueError("D4 stage is not ready: wl586")
    if work_log == "wl593" and "violations" in payload and payload["violations"] != []:
        raise ValueError("D4 stage is not ready: wl593")
    projected = {key: copy.deepcopy(payload[key]) for key in allowed if key != "verification"}
    if work_log == "wl593":
        verification = payload["verification"]
        if not isinstance(verification, Mapping):
            raise ValueError("invalid wl593 verification")
        if set(verification) != {"checks", "violations", "strict_certificate"}:
            raise ValueError("incomplete wl593 verification")
        if verification["violations"] != []:
            raise ValueError("D4 stage is not ready: wl593")
        checks = verification["checks"]
        if not isinstance(checks, Mapping) or not all(
            isinstance(value, bool) for value in checks.values()
        ):
            raise ValueError("invalid wl593 verification checks")
        projected["verification"] = {"checks": copy.deepcopy(dict(checks))}
    return {key: projected[key] for key in D4_ALLOWLISTS[work_log]}


def _is_ready(evidence: D4Evidence) -> bool:
    wl586 = evidence.stages.get("wl586", {})
    wl593 = evidence.stages.get("wl593", {})
    return (
        isinstance(wl586, Mapping)
        and wl586.get("status") == "ok"
        and wl586.get("ready") is True
        and wl586.get("violations") == []
        and isinstance(wl593, Mapping)
        and wl593.get("status") == "ok"
        and wl593.get("ready") is True
        and wl593.get("violations", []) == []
        and isinstance(wl593.get("verification"), Mapping)
        and wl593["verification"].get("violations") == []
    )


def _serialized(evidence: D4Evidence) -> dict[str, Any]:
    ready = _is_ready(evidence)
    if ready:
        stages = {
            work_log: semantic_projection(project_stage(evidence, work_log), work_log)
            for work_log in D4_STAGES
        }
    else:
        stages = {
            work_log: {
                key: copy.deepcopy(evidence.stages[work_log][key])
                for key in ("status", "ready", "work_log", "violations")
                if key in evidence.stages.get(work_log, {})
            }
            for work_log in D4_STAGES
        }
    return {
        "schema_version": 1,
        "stage_count": len(D4_STAGES),
        "status": "ok" if ready else "issues",
        "ready": ready,
        "stages": stages,
        "dependency_metadata": copy.deepcopy(evidence.dependency_metadata),
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    try:
        a0 = load_a0(args.data_dir)
        certificates = load_certificates(args.data_dir / "a1-certificates.v1.json")
        a1 = build_a1(a0, certificates)
        boundary_spec = load_boundary_spec(args.data_dir / "a2-boundary-spec.v1.json")
        a2 = build_a2(a0, a1, boundary_spec)
        c3 = build_c3()
        evidence = build_d4(a0=a0, a2=a2, c3=c3)
    except (OSError, KeyError, TypeError, ValueError) as exc:
        evidence = _failure([f"canonical_cli_input_failed:{type(exc).__name__}"])
    payload = _serialized(evidence)
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"stage_count={payload['stage_count']}")
    print(f"status={payload['status']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
