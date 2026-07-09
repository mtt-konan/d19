from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_h2_coordinate_equivalence import (
    BOUNDARY,
    audit_rank_zero_aa_bb_h2_coordinate_equivalence,
)


def _complete_two_descent_recast() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "pattern": "AA+BB",
        "complete_two_descent_coordinates": {
            "ambient_relation": (
                "d_minus_p * d_pos_2sqrt_q * d_neg_2sqrt_q = 1 "
                "in Q*/Q*2"
            ),
        },
        "isogeny_to_complete_coordinate_relation": {
            "x_minus_p": "d_pos_2sqrt_q * d_neg_2sqrt_q / d_minus_p",
            "x_pos_2sqrt_q": "d_minus_p * d_neg_2sqrt_q / d_pos_2sqrt_q",
            "x_neg_2sqrt_q": "d_minus_p * d_pos_2sqrt_q / d_neg_2sqrt_q",
        },
        "torsion_kummer_images": {
            "O": ["1", "1", "1"],
            "T_minus_p": [
                "(-p-2*sqrt_q)*(-p+2*sqrt_q)",
                "-p-2*sqrt_q",
                "-p+2*sqrt_q",
            ],
            "T_pos_2sqrt_q": [
                "2*sqrt_q+p",
                "(2*sqrt_q+p)*(4*sqrt_q)",
                "4*sqrt_q",
            ],
            "T_neg_2sqrt_q": [
                "-2*sqrt_q+p",
                "-4*sqrt_q",
                "(-2*sqrt_q+p)*(-4*sqrt_q)",
            ],
        },
    }


def _theorem_bridge() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "required_hypotheses": [
            {"id": "H1_complete_selmer_object", "status": "framed_not_proved"},
            {"id": "H2_coordinate_equivalence", "status": "partially_framed"},
            {"id": "H3_uniform_local_containment", "status": "missing"},
        ],
        "bridge_summary": {"complete_selmer_upper_bound_proved": False},
    }


def test_h2_coordinate_equivalence_is_refuted_by_squareclass_linear_algebra() -> None:
    audit = audit_rank_zero_aa_bb_h2_coordinate_equivalence(
        complete_two_descent_recast=_complete_two_descent_recast(),
        theorem_bridge=_theorem_bridge(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["h2_verdict"] == {
        "id": "H2_coordinate_equivalence",
        "status": "refuted",
        "coordinate_equivalence_proved": False,
        "coordinate_equivalence_refuted": True,
        "reason": (
            "On the complete-descent product-relation plane, each package "
            "x-coordinate is the same product d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q, "
            "hence the trivial squareclass. The package x-triple is therefore "
            "not an injective coordinate system for complete d-data."
        ),
    }
    assert audit["squareclass_linear_algebra"] == {
        "ambient_group": "V = Q*/Q*2, written additively over F2",
        "complete_d_relation": "d_minus_p + d_pos_2sqrt_q + d_neg_2sqrt_q = 0",
        "package_coordinate_rows": {
            "x_minus_p": [1, 1, 1],
            "x_pos_2sqrt_q": [1, 1, 1],
            "x_neg_2sqrt_q": [1, 1, 1],
        },
        "rank_on_complete_relation_plane": 0,
        "kernel_dimension_on_complete_relation_plane": 2,
        "injective_on_complete_d_data": False,
        "equivalent_squareclass_data": False,
        "image_on_complete_relation_plane": ["1", "1", "1"],
    }


def test_h2_torsion_and_exceptional_root_representatives_collapse_to_trivial_x() -> None:
    audit = audit_rank_zero_aa_bb_h2_coordinate_equivalence(
        complete_two_descent_recast=_complete_two_descent_recast(),
        theorem_bridge=_theorem_bridge(),
    )

    assert audit["torsion_and_exceptional_roots"] == {
        "standard_rule": (
            "At X=e_i, replace the vanishing d_i coordinate by the product of "
            "the two nonzero root differences."
        ),
        "torsion_representatives_checked": [
            "O",
            "T_minus_p",
            "T_pos_2sqrt_q",
            "T_neg_2sqrt_q",
        ],
        "package_x_image_for_each_torsion_representative": {
            "O": ["1", "1", "1"],
            "T_minus_p": ["1", "1", "1"],
            "T_pos_2sqrt_q": ["1", "1", "1"],
            "T_neg_2sqrt_q": ["1", "1", "1"],
        },
        "exceptional_root_cases_rescue_equivalence": False,
        "torsion_baseline_preserved_by_package_x_coordinates": False,
    }


def test_h2_records_counterexample_schema_without_claiming_selmer_upper_bound() -> None:
    audit = audit_rank_zero_aa_bb_h2_coordinate_equivalence(
        complete_two_descent_recast=_complete_two_descent_recast(),
        theorem_bridge=_theorem_bridge(),
    )

    assert audit["counterexample_schema"] == {
        "not_a_selmer_existence_claim": True,
        "two_distinct_complete_d_classes": [
            ["1", "1", "1"],
            ["alpha", "beta", "alpha*beta"],
        ],
        "same_package_x_image": ["1", "1", "1"],
        "why_sufficient_for_H2": (
            "H2 asks for coordinate equivalence, including torsion and root representatives; "
            "the transformation loses the two-dimensional complete d-plane before any C_d "
            "local-solubility matrix is built."
        ),
    }
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["do_not_proceed_to"] == ["H3_uniform_local_containment", "H4_mixed_rows_upgrade"]
    assert audit["boundary"] == BOUNDARY


def test_h2_requires_ready_inputs_and_existing_h2_hypothesis() -> None:
    recast = _complete_two_descent_recast()
    recast["ready"] = False
    bridge = _theorem_bridge()
    bridge["required_hypotheses"] = [{"id": "H3_uniform_local_containment"}]

    audit = audit_rank_zero_aa_bb_h2_coordinate_equivalence(
        complete_two_descent_recast=recast,
        theorem_bridge=bridge,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "complete_two_descent_recast_not_ready",
        "bridge_h2_hypothesis_missing",
    ]
    assert audit["h2_verdict"]["coordinate_equivalence_proved"] is False


def test_h2_coordinate_equivalence_cli_writes_audit(tmp_path: Path) -> None:
    recast = tmp_path / "recast.json"
    bridge = tmp_path / "bridge.json"
    out = tmp_path / "h2_coordinate_equivalence.json"
    recast.write_text(json.dumps(_complete_two_descent_recast()), encoding="utf-8")
    bridge.write_text(json.dumps(_theorem_bridge()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_h2_coordinate_equivalence.py",
            "--complete-two-descent-recast",
            str(recast),
            "--theorem-bridge",
            str(bridge),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "h2_status=refuted" in result.stdout
    assert "coordinate_equivalence_proved=False" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["h2_verdict"]["coordinate_equivalence_refuted"] is True
