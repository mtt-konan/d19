from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_two_primary_reduction import (
    BOUNDARY,
    audit_rank_zero_aa_bb_two_primary_reduction,
    write_json,
)


def _family_obligations() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "groups": [
            {
                "pattern": "AA+BB",
                "candidate_class_count": 43,
                "model_count": 86,
                "model_counts_by_curve": {"AA": 43, "BB": 43},
            }
        ],
    }


def _product_relation() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "common_source_relation": (
            "x_minus_p * x_pos_2sqrt_q * x_neg_2sqrt_q = "
            "(X-(-p))*(X-(2*sqrt_q))*(X-(-2*sqrt_q)) = Y^2"
        ),
    }


def test_aa_bb_two_primary_reduction_records_conditional_gap_shrink() -> None:
    audit = audit_rank_zero_aa_bb_two_primary_reduction(
        family_obligations=_family_obligations(),
        product_relation=_product_relation(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["pattern"] == "AA+BB"
    assert audit["candidate_class_count"] == 43
    assert audit["model_count"] == 86
    assert audit["common_source_product_relation_available"] is True
    assert audit["odd_prime_support_for_actual_points_trivial"] is True
    assert audit["remaining_gap_kind"] == "Selmer-layer lift of point-level collapse"
    assert audit["remaining_gap_components"] == [
        "lift common-source compatibility to the Selmer layer",
        "dyadic local condition",
        "unit/sign classes",
    ]
    assert audit["next_theorem_target"] == (
        "Prove the AA+BB Selmer-layer lift: every relevant Selmer candidate "
        "satisfies the common-source two-primary compatibility whose "
        "point-level collapse leaves only (1,1,1)."
    )
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["boundary"] == BOUNDARY


def test_aa_bb_two_primary_reduction_records_point_level_collapse() -> None:
    audit = audit_rank_zero_aa_bb_two_primary_reduction(
        family_obligations=_family_obligations(),
        product_relation=_product_relation(),
    )

    assert audit["point_level_two_primary_collapse"] == {
        "source": "wl460-wl463",
        "scope": "genuine AA+BB common-source rational points",
        "remaining_triples": [
            {
                "x_minus_p": "1",
                "x_pos_2sqrt_q": "1",
                "x_neg_2sqrt_q": "1",
            }
        ],
        "nontrivial_triple_count": 0,
        "selmer_lift_proved": False,
    }
    assert audit["next_theorem_target"] == (
        "Prove the AA+BB Selmer-layer lift: every relevant Selmer candidate "
        "satisfies the common-source two-primary compatibility whose "
        "point-level collapse leaves only (1,1,1)."
    )
    assert audit["remaining_gap_kind"] == "Selmer-layer lift of point-level collapse"


def test_aa_bb_two_primary_reduction_requires_ready_inputs() -> None:
    family_obligations = _family_obligations()
    family_obligations["ready"] = False
    product_relation = _product_relation()
    product_relation["common_source_relation"] = "missing"

    audit = audit_rank_zero_aa_bb_two_primary_reduction(
        family_obligations=family_obligations,
        product_relation=product_relation,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "family_obligations_not_ready",
        "common_source_relation_missing",
    ]


def test_aa_bb_two_primary_reduction_cli_writes_audit(tmp_path: Path) -> None:
    family_obligations = tmp_path / "family_obligations.json"
    product_relation = tmp_path / "product_relation.json"
    out = tmp_path / "aa_bb_two_primary.json"
    family_obligations.write_text(json.dumps(_family_obligations()), encoding="utf-8")
    product_relation.write_text(json.dumps(_product_relation()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_two_primary_reduction.py",
            "--family-obligations",
            str(family_obligations),
            "--product-relation",
            str(product_relation),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "candidate_class_count=43" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["odd_prime_support_for_actual_points_trivial"] is True


def test_write_json_writes_sorted_aa_bb_two_primary_reduction(tmp_path: Path) -> None:
    out = tmp_path / "aa_bb_two_primary.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
