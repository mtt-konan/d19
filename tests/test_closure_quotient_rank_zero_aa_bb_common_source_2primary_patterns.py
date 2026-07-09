from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_common_source_2primary_patterns import (
    BOUNDARY,
    audit_rank_zero_aa_bb_common_source_2primary_patterns,
    write_json,
)


def _two_primary_reduction() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "candidate_class_count": 43,
        "odd_prime_support_for_actual_points_trivial": True,
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


def test_aa_bb_common_source_2primary_patterns_reduce_to_finite_cube() -> None:
    audit = audit_rank_zero_aa_bb_common_source_2primary_patterns(
        two_primary_reduction=_two_primary_reduction(),
        product_relation=_product_relation(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["pattern"] == "AA+BB"
    assert audit["candidate_class_count"] == 43
    assert audit["q2_squareclass_universe_size"] == 8
    assert audit["naive_q2_kernel_triple_pattern_count"] == 512
    assert audit["common_source_squareclass_subgroup_generators"] == ["-1", "2"]
    assert audit["common_source_squareclass_subgroup_size"] == 4
    assert audit["common_source_kernel_triple_pattern_count"] == 16
    assert audit["pattern_reduction_factor_vs_naive_q2_box"] == 32
    assert audit["common_source_pattern_rows"][:4] == [
        {
            "x_minus_p": "1",
            "x_pos_2sqrt_q": "1",
            "x_neg_2sqrt_q": "1",
            "product_squareclass": "1",
        },
        {
            "x_minus_p": "1",
            "x_pos_2sqrt_q": "-1",
            "x_neg_2sqrt_q": "-1",
            "product_squareclass": "1",
        },
        {
            "x_minus_p": "1",
            "x_pos_2sqrt_q": "2",
            "x_neg_2sqrt_q": "2",
            "product_squareclass": "1",
        },
        {
            "x_minus_p": "1",
            "x_pos_2sqrt_q": "-2",
            "x_neg_2sqrt_q": "-2",
            "product_squareclass": "1",
        },
    ]
    assert audit["product_square_relation_retained"] is True
    assert audit["remaining_filter_layer"] == (
        "dyadic local image and Selmer-lift compatibility"
    )
    assert audit["next_target"] == (
        "Rule out the finite 2-primary common-source patterns at the Selmer "
        "level for AA+BB."
    )
    assert audit["boundary"] == BOUNDARY


def test_aa_bb_common_source_2primary_patterns_require_ready_inputs() -> None:
    two_primary_reduction = _two_primary_reduction()
    two_primary_reduction["odd_prime_support_for_actual_points_trivial"] = False
    product_relation = _product_relation()
    product_relation["ready"] = False

    audit = audit_rank_zero_aa_bb_common_source_2primary_patterns(
        two_primary_reduction=two_primary_reduction,
        product_relation=product_relation,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "two_primary_reduction_not_ready",
        "product_relation_not_ready",
    ]


def test_aa_bb_common_source_2primary_patterns_cli_writes_audit(
    tmp_path: Path,
) -> None:
    two_primary_reduction = tmp_path / "two_primary_reduction.json"
    product_relation = tmp_path / "product_relation.json"
    out = tmp_path / "aa_bb_2primary_patterns.json"
    two_primary_reduction.write_text(
        json.dumps(_two_primary_reduction()), encoding="utf-8"
    )
    product_relation.write_text(json.dumps(_product_relation()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_common_source_2primary_patterns.py",
            "--two-primary-reduction",
            str(two_primary_reduction),
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

    assert "common_source_kernel_triple_pattern_count=16" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["common_source_squareclass_subgroup_size"] == 4


def test_write_json_writes_sorted_aa_bb_common_source_2primary_patterns(
    tmp_path: Path,
) -> None:
    out = tmp_path / "aa_bb_2primary_patterns.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
