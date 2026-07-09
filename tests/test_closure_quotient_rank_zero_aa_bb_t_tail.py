from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_t_tail import (
    BOUNDARY,
    audit_rank_zero_aa_bb_t_tail,
)


def _sign_tail_audit() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "pattern": "AA+BB",
        "dimension_bound_update": {
            "new_tail_terms": ["omega_{1 mod 4}(T)"],
            "upper_bound": "dim_F2 S~ <= 2 + omega_{1 mod 4}(T)",
            "forces_dim_2": False,
        },
        "sign_tail": {"epsilon_sign": 0},
    }


def test_t_tail_is_killed_by_valuation_parity_ledger() -> None:
    audit = audit_rank_zero_aa_bb_t_tail(sign_tail_audit=_sign_tail_audit())

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["local_valuation_ledger"] == {
        "prime_scope": "odd primes ell | T with ell == 1 mod 4",
        "coordinate_order": [
            "x_minus_p",
            "x_pos_2sqrt_q",
            "x_neg_2sqrt_q",
        ],
        "known_support_rows": [
            {
                "source": "wl458",
                "coordinate": "x_minus_p",
                "valuation_mod_2": 0,
                "reason": "AA+BB minus-p odd-prime support is killed",
            },
            {
                "source": "wl459",
                "coordinate": "x_pos_2sqrt_q",
                "valuation_mod_2": "candidate_tail_bit",
                "reason": "only this coordinate had possible ell | T, ell == 1 mod 4 support",
            },
            {
                "source": "wl457",
                "coordinate": "x_neg_2sqrt_q",
                "valuation_mod_2": 0,
                "reason": "AA+BB neg-2sqrt-q odd-prime support is killed",
            },
        ],
        "product_relation": "x_minus_p*x_pos_2sqrt_q*x_neg_2sqrt_q=1 in Q*/Q*2",
        "parity_equation": "0 + tail_bit + 0 = 0 in F2",
        "tail_bit": 0,
    }
    assert audit["t_tail"]["status"] == "killed"
    assert audit["t_tail"]["tail_dimension"] == 0
    assert audit["t_tail"]["surviving_classes_mod_torsion"] == []


def test_t_tail_updates_pseudo_selmer_dimension_without_overclaiming_selmer() -> None:
    audit = audit_rank_zero_aa_bb_t_tail(sign_tail_audit=_sign_tail_audit())

    assert audit["dimension_bound_update"] == {
        "old_tail_terms": ["omega_{1 mod 4}(T)"],
        "new_tail_terms": [],
        "torsion_baseline_dimension": 2,
        "upper_bound": "dim_F2 S~ <= 2",
        "pseudo_selmer_container_forces_torsion_baseline": True,
        "complete_selmer_bound_proved": False,
        "why_not_complete_selmer_bound": (
            "This is a cheap AA+BB pseudo-container valuation ledger, not the full "
            "complete C_d local-solubility matrix for a single curve."
        ),
    }
    assert audit["route_decision"] == {
        "decision": "T_tail_killed_in_pseudo_container",
        "requires_joint_C_d_local_conditions_for_this_tail": False,
        "next_action": "stop_after_T_tail_audit",
        "stop_condition_observed": (
            "The only remaining symbolic T-prime tail in S~ has zero dimension "
            "by the product-relation valuation ledger."
        ),
    }
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["boundary"] == BOUNDARY


def test_t_tail_requires_ready_sign_tail_audit() -> None:
    sign_tail = _sign_tail_audit()
    sign_tail["ready"] = False

    audit = audit_rank_zero_aa_bb_t_tail(sign_tail_audit=sign_tail)

    assert audit["status"] == "issues"
    assert audit["violations"] == ["sign_tail_audit_not_ready"]


def test_t_tail_cli_writes_audit(tmp_path: Path) -> None:
    sign_tail = tmp_path / "sign_tail.json"
    out = tmp_path / "t_tail.json"
    sign_tail.write_text(json.dumps(_sign_tail_audit()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_t_tail.py",
            "--sign-tail-audit",
            str(sign_tail),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "t_tail_status=killed" in result.stdout
    assert "upper_bound=dim_F2 S~ <= 2" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["t_tail"]["tail_dimension"] == 0
