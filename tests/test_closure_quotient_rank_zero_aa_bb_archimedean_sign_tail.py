from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_archimedean_sign_tail import (
    BOUNDARY,
    audit_rank_zero_aa_bb_archimedean_sign_tail,
)


def _pseudo_selmer_container() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "pattern": "AA+BB",
        "pseudo_selmer_container": {
            "ambient_coordinates": [
                "d_minus_p",
                "d_pos_2sqrt_q",
                "d_neg_2sqrt_q",
            ]
        },
    }


def test_archimedean_sign_tail_orders_roots_and_keeps_only_real_intervals() -> None:
    audit = audit_rank_zero_aa_bb_archimedean_sign_tail(
        pseudo_selmer_container=_pseudo_selmer_container()
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["root_order_audit"] == {
        "parameters": {
            "T": "A+B",
            "L": "A on AA side, B on BB side",
            "p": "8*L^2 - 2*T^2",
            "sqrt_q": "T^2 + 4*L^2",
        },
        "ordered_roots": [
            "e_neg=-2*sqrt_q",
            "e_minus=-p",
            "e_pos=2*sqrt_q",
        ],
        "strict_inequality_proof": [
            "e_minus - e_neg = 4*T^2 > 0",
            "e_pos - e_minus = 16*L^2 > 0",
        ],
    }
    assert audit["real_sign_image"] == {
        "coordinate_order": [
            "d_minus_p",
            "d_pos_2sqrt_q",
            "d_neg_2sqrt_q",
        ],
        "product_relation_sign_classes": [
            ["+", "+", "+"],
            ["+", "-", "-"],
            ["-", "+", "-"],
            ["-", "-", "+"],
        ],
        "real_interval_sign_classes": [
            {
                "real_interval": "X > e_pos",
                "sign_class": ["+", "+", "+"],
            },
            {
                "real_interval": "e_neg < X < e_minus",
                "sign_class": ["-", "-", "+"],
            },
        ],
        "forbidden_by_real_place": [
            ["+", "-", "-"],
            ["-", "+", "-"],
        ],
        "surviving_nontrivial_sign_class": ["-", "-", "+"],
    }


def test_archimedean_sign_tail_has_no_extra_epsilon_beyond_torsion() -> None:
    audit = audit_rank_zero_aa_bb_archimedean_sign_tail(
        pseudo_selmer_container=_pseudo_selmer_container()
    )

    assert audit["torsion_sign_image"] == {
        "O": ["+", "+", "+"],
        "T_minus_p": ["-", "-", "+"],
        "T_pos_2sqrt_q": ["+", "+", "+"],
        "T_neg_2sqrt_q": ["-", "-", "+"],
        "distinct_torsion_sign_classes": [
            ["+", "+", "+"],
            ["-", "-", "+"],
        ],
    }
    assert audit["sign_tail"] == {
        "epsilon_sign": 0,
        "surviving_sign_classes": [
            ["+", "+", "+"],
            ["-", "-", "+"],
        ],
        "exact_surviving_nontrivial_class": {
            "sign_class": ["-", "-", "+"],
            "meaning": "d_minus_p<0, d_pos_2sqrt_q<0, d_neg_2sqrt_q>0",
            "already_torsion": True,
            "torsion_representatives": ["T_minus_p", "T_neg_2sqrt_q"],
        },
        "reason": (
            "The real local image has one nontrivial sign class, but that "
            "class is already the sign image of rational 2-torsion, so it "
            "does not add a pseudo-Selmer tail beyond the torsion baseline."
        ),
    }
    assert audit["dimension_bound_update"] == {
        "old_tail_terms": ["omega_{1 mod 4}(T)", "epsilon_sign"],
        "new_tail_terms": ["omega_{1 mod 4}(T)"],
        "epsilon_sign_values": [0],
        "upper_bound": "dim_F2 S~ <= 2 + omega_{1 mod 4}(T)",
        "forces_dim_2": False,
        "why_not_forced_dim_2": "The T-prime tail remains unresolved.",
    }
    assert audit["boundary"] == BOUNDARY
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0


def test_archimedean_sign_tail_requires_ready_pseudo_container() -> None:
    container = _pseudo_selmer_container()
    container["ready"] = False

    audit = audit_rank_zero_aa_bb_archimedean_sign_tail(
        pseudo_selmer_container=container
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["pseudo_selmer_container_not_ready"]


def test_archimedean_sign_tail_cli_writes_audit(tmp_path: Path) -> None:
    pseudo_container = tmp_path / "pseudo_container.json"
    out = tmp_path / "sign_tail.json"
    pseudo_container.write_text(json.dumps(_pseudo_selmer_container()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_archimedean_sign_tail.py",
            "--pseudo-selmer-container",
            str(pseudo_container),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "epsilon_sign=0" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["sign_tail"]["epsilon_sign"] == 0
