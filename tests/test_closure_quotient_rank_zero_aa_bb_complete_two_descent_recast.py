from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_complete_two_descent_recast import (
    BOUNDARY,
    audit_rank_zero_aa_bb_complete_two_descent_recast,
    write_json,
)


def _two_primary_reduction() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "point_level_two_primary_collapse": {
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
        },
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


def test_complete_two_descent_recast_identifies_source_model_and_coordinates() -> None:
    audit = audit_rank_zero_aa_bb_complete_two_descent_recast(
        two_primary_reduction=_two_primary_reduction(),
        product_relation=_product_relation(),
    )

    model = audit["full_rational_2_torsion_model"]
    coordinates = audit["complete_two_descent_coordinates"]

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert model["source_curve"] == (
        "E_L: Y^2 = (X-(-p))*(X-(2*sqrt_q))*(X-(-2*sqrt_q)) "
        "= (X+p)*(X^2 - 4*q)"
    )
    assert model["rational_two_torsion_points"] == [
        "O",
        "T_minus_p=(-p,0)",
        "T_pos_2sqrt_q=(2*sqrt_q,0)",
        "T_neg_2sqrt_q=(-2*sqrt_q,0)",
    ]
    assert model["e2_dimension"] == 2
    assert coordinates["coordinate_names"] == {
        "d_minus_p": "X-(-p)=X+p",
        "d_pos_2sqrt_q": "X-(2*sqrt_q)",
        "d_neg_2sqrt_q": "X-(-2*sqrt_q)=X+2*sqrt_q",
    }
    assert coordinates["ambient_relation"] == (
        "d_minus_p * d_pos_2sqrt_q * d_neg_2sqrt_q = 1 "
        "in Q*/Q*2"
    )
    assert coordinates["rank_bound_formula"] == (
        "rank E(Q) <= dim_F2 Sel_2(E) - dim_F2 E[2](Q) = dim_F2 Sel_2(E) - 2"
    )


def test_complete_two_descent_recast_does_not_promote_wl463_to_selmer_bound() -> None:
    audit = audit_rank_zero_aa_bb_complete_two_descent_recast(
        two_primary_reduction=_two_primary_reduction(),
        product_relation=_product_relation(),
    )

    assert audit["point_level_collapse_promoted_to_sel2_bound"] is False
    assert audit["forced_dim_sel2_eq_2"] is False
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["remaining_obstruction"] == {
        "kind": "pseudo-Selmer tail",
        "exact_obstruction": "S_tilde_dimension_not_forced_to_2",
        "why_not_unit_sign_only": (
            "the sign bit is one tail term, but the symbolic T-prime tail at "
            "ell | T, ell == 1 mod 4 also remains"
        ),
        "why_not_sha2_yet": (
            "Sha[2] becomes the primary route only after a proved rank-zero sample "
            "or theorem still has dim Sel_2(E)>2"
        ),
        "why_not_finite_ledger": (
            "the current blocker is a symbolic upper-bound tail, not a need for "
            "more point-level local-class enumeration"
        ),
        "missing_evidence": [
            "prove the archimedean sign tail has dimension 0 or account for it",
            "prove a joint local condition for primes ell | T with ell == 1 mod 4",
            "only if those tails survive, build the full C_d local solubility matrix",
            "linear algebra showing the surviving S~ or Sel_2(E) space is exactly the E[2] Kummer image",
        ],
    }
    assert audit["boundary"] == BOUNDARY


def test_complete_two_descent_recast_translates_existing_constraints_as_untransferred() -> None:
    audit = audit_rank_zero_aa_bb_complete_two_descent_recast(
        two_primary_reduction=_two_primary_reduction(),
        product_relation=_product_relation(),
    )

    translation = audit["existing_constraint_translation"]
    coordinate_relation = audit["isogeny_to_complete_coordinate_relation"]

    assert coordinate_relation == {
        "x_minus_p": "d_pos_2sqrt_q * d_neg_2sqrt_q / d_minus_p",
        "x_pos_2sqrt_q": "d_minus_p * d_neg_2sqrt_q / d_pos_2sqrt_q",
        "x_neg_2sqrt_q": "d_minus_p * d_pos_2sqrt_q / d_neg_2sqrt_q",
        "product": (
            "x_minus_p * x_pos_2sqrt_q * x_neg_2sqrt_q "
            "= d_minus_p * d_pos_2sqrt_q * d_neg_2sqrt_q = 1"
        ),
        "audit_warning": (
            "The wl457-wl463 constraints are stated in these three isogeny target "
            "coordinates. In complete 2-descent the product/common-source relation "
            "is built into Selmer membership, but the cheap next step is the "
            "pseudo-Selmer S~ dimension audit before the full C_d matrix."
        ),
    }

    assert translation["odd_prime_formal_lift_inputs"] == [
        {
            "kernel": "kernel_minus_p",
            "source": "wl458",
            "isogeny_package_constraint": "no odd-prime valuation support",
            "complete_descent_effect": "not transferred to d_minus_p,d_pos_2sqrt_q,d_neg_2sqrt_q",
        },
        {
            "kernel": "kernel_pos_2sqrt_q",
            "source": "wl459",
            "isogeny_package_constraint": "support only from ell | T with ell == 1 mod 4",
            "complete_descent_effect": "not transferred to a complete 2-cover local condition",
        },
        {
            "kernel": "kernel_neg_2sqrt_q",
            "source": "wl457",
            "isogeny_package_constraint": "no odd-prime valuation support",
            "complete_descent_effect": "not transferred to d_minus_p,d_pos_2sqrt_q,d_neg_2sqrt_q",
        },
    ]
    assert translation["dyadic_inputs"][2] == {
        "source": "wl462-wl463",
        "statement": "common-source rational points collapse to (1,1,1)",
        "complete_descent_effect": "compatible with complete descent, but not a Sel_2(E) condition",
    }
    assert translation["translation_verdict"] == (
        "The existing constraints constrain point-level or independent "
        "dual-isogeny package coordinates. They do not yet fill the complete "
        "2-descent local matrix for the d_i coordinates."
    )


def test_complete_two_descent_recast_completion_audit_covers_requested_tasks() -> None:
    audit = audit_rank_zero_aa_bb_complete_two_descent_recast(
        two_primary_reduction=_two_primary_reduction(),
        product_relation=_product_relation(),
    )

    assert audit["completion_audit"] == [
        {
            "task": "identify_full_rational_2_torsion_model",
            "status": "satisfied_as_recast",
            "evidence": "FULL_RATIONAL_2_TORSION_MODEL",
        },
        {
            "task": "write_complete_2_descent_coordinates_and_product_relation",
            "status": "satisfied_as_recast",
            "evidence": "COMPLETE_TWO_DESCENT_COORDINATES",
        },
        {
            "task": "translate_odd_prime_and_dyadic_constraints",
            "status": "satisfied_as_audit",
            "evidence": "EXISTING_CONSTRAINT_TRANSLATION",
        },
        {
            "task": "audit_whether_constraints_force_dim_sel2_eq_2",
            "status": "not_proved",
            "evidence": "forced_dim_sel2_eq_2=false",
        },
        {
            "task": "report_exact_remaining_obstruction",
            "status": "satisfied_as_audit",
            "evidence": "REMAINING_OBSTRUCTION.kind=pseudo-Selmer tail",
        },
    ]


def test_complete_two_descent_recast_requires_ready_inputs() -> None:
    two_primary = _two_primary_reduction()
    two_primary["ready"] = False
    product_relation = _product_relation()
    product_relation["common_source_relation"] = "missing"

    audit = audit_rank_zero_aa_bb_complete_two_descent_recast(
        two_primary_reduction=two_primary,
        product_relation=product_relation,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "two_primary_reduction_ready",
        "product_relation_ready",
    ]


def test_complete_two_descent_recast_cli_writes_audit(tmp_path: Path) -> None:
    two_primary = tmp_path / "two_primary.json"
    product_relation = tmp_path / "product_relation.json"
    out = tmp_path / "complete_two_descent_recast.json"
    two_primary.write_text(json.dumps(_two_primary_reduction()), encoding="utf-8")
    product_relation.write_text(json.dumps(_product_relation()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_complete_two_descent_recast.py",
            "--two-primary-reduction",
            str(two_primary),
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

    assert "forced_dim_sel2_eq_2=False" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["remaining_obstruction"]["kind"] == "pseudo-Selmer tail"


def test_write_json_writes_sorted_complete_two_descent_recast(tmp_path: Path) -> None:
    out = tmp_path / "complete_two_descent_recast.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
