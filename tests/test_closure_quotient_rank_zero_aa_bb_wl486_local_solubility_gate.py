from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl481_m_tail_explicit_matrix_builder import (  # noqa: E501
    build_wl481_m_tail_audit,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl482_m_tail_kernel_classification_gate import (  # noqa: E501
    build_wl482_m_tail_kernel_classification_gate,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl483_local_hilbert_row_decision_gate import (  # noqa: E501
    build_wl483_local_hilbert_row_decision_gate,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl484_u3_obstruction_route_entry_audit import (  # noqa: E501
    build_wl484_u3_obstruction_route_entry_audit,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl485_explicit_cd_cover_equation_instantiation import (  # noqa: E501
    build_wl485_explicit_cd_cover_equation_instantiation,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl486_local_solubility_gate import (
    build_wl486_local_solubility_gate,
)


def _wl480_input() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D4_AA_BB_uniform_matrix_rank_bound_audit",
        "work_log": "wl480",
        "d4_status": "uniform_dim2_bound_not_forced_by_solved_rows",
        "complete_d_coordinate_order": [
            "d_minus_p",
            "d_pos_2sqrt_q",
            "d_neg_2sqrt_q",
        ],
        "local_character_matrix": {"id": "M_tail"},
        "surviving_obstruction": {"id": "M_tail_uniform_full_rank_missing"},
        "old_package_x_coordinate_collapse_used": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _wl485_input() -> dict[str, object]:
    wl481 = build_wl481_m_tail_audit(wl480=_wl480_input())
    wl482 = build_wl482_m_tail_kernel_classification_gate(wl481=wl481)
    wl483 = build_wl483_local_hilbert_row_decision_gate(wl482=wl482)
    wl484 = build_wl484_u3_obstruction_route_entry_audit(wl483=wl483)
    return build_wl485_explicit_cd_cover_equation_instantiation(wl484=wl484)


def test_wl486_records_local_solubility_at_exact_relevant_places() -> None:
    audit = build_wl486_local_solubility_gate(wl485=_wl485_input())
    gate = audit["local_solubility_gate"]
    certificates = gate["place_certificates"]

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL486_local_solubility_gate"
    assert audit["work_log"] == "wl486"
    assert audit["input_work_log"] == "wl485"
    assert audit["relevant_places"] == ["infinity", "2", "3", "13"]
    assert [item["place"] for item in certificates] == [
        "infinity",
        "2",
        "3",
        "13",
    ]
    assert all(item["status"] == "locally_soluble" for item in certificates)
    assert gate["candidate_survives_local_gate"] is True
    assert gate["next_gate"] == "route_impact_of_global_point"


def test_wl486_real_and_dyadic_certificates_are_explicit_local_points() -> None:
    audit = build_wl486_local_solubility_gate(wl485=_wl485_input())
    certs = {
        item["place"]: item
        for item in audit["local_solubility_gate"]["place_certificates"]
    }
    point = {"X": 152, "u_minus_p": 8, "u_pos_2sqrt_q": 4, "u_neg_2sqrt_q": 16}

    assert certs["infinity"] == {
        "place": "infinity",
        "field": "R",
        "status": "locally_soluble",
        "certificate_type": "explicit_real_point",
        "point": point,
        "equation_checks": [
            "152 + 40 = 3*8^2 = 192",
            "152 - 104 = 3*4^2 = 48",
            "152 + 104 = 16^2 = 256",
        ],
    }
    assert certs["2"] == {
        "place": "2",
        "field": "Q_2",
        "status": "locally_soluble",
        "certificate_type": "exact_integral_2_adic_point",
        "point": point,
        "modular_lift_certificate": {
            "method": "exact_zero_over_Z_embeds_in_Q_2",
            "verified_moduli": [2, 4, 8, 16, 32],
            "hensel_regular_minor_required": False,
            "reason": (
                "The displayed integer tuple satisfies the three C_d square "
                "relations exactly, so its reductions are compatible modulo "
                "2^n for every n. This same tuple is also a global integral "
                "point, recorded separately below."
            ),
        },
    }


def test_wl486_records_global_integral_point_when_local_certificate_is_global() -> None:
    audit = build_wl486_local_solubility_gate(wl485=_wl485_input())
    witness = audit["local_solubility_gate"]["global_solubility_witness"]

    assert audit["global_solubility_decided_here"] is True
    assert audit["global_solubility_summary"] == (
        "globally_soluble_integral_point_found_during_local_gate"
    )
    assert audit["candidate_obstruction_refuted_here"] is True
    assert audit["explicit_c_d_cover_solved_here"] is True
    assert witness == {
        "status": "globally_soluble",
        "certificate_type": "explicit_integral_point_on_C_d",
        "point_on_cover": {
            "X": 152,
            "u_minus_p": 8,
            "u_pos_2sqrt_q": 4,
            "u_neg_2sqrt_q": 16,
        },
        "equation_checks": [
            "152 + 40 = 3*8^2 = 192",
            "152 - 104 = 3*4^2 = 48",
            "152 + 104 = 16^2 = 256",
        ],
        "induced_point_on_E_L": {
            "X": 152,
            "Y": 1536,
            "check": "1536^2 = (152+40)*(152^2 - 4*2704)",
        },
        "route_impact": (
            "The u_3 candidate is not a Sha-style locally-soluble globally-"
            "pointless obstruction; it is represented by a rational point."
        ),
    }


def test_wl486_odd_prime_hensel_certificates_are_nonsingular() -> None:
    audit = build_wl486_local_solubility_gate(wl485=_wl485_input())
    certs = {
        item["place"]: item
        for item in audit["local_solubility_gate"]["place_certificates"]
    }

    assert certs["3"] == {
        "place": "3",
        "field": "Q_3",
        "status": "locally_soluble",
        "certificate_type": "hensel_lift_from_mod_p",
        "residue_modulus": 3,
        "residue_point": {
            "X": 2,
            "u_minus_p": 1,
            "u_pos_2sqrt_q": 1,
            "u_neg_2sqrt_q": 1,
        },
        "equations_mod_p": [
            "u_minus_p^2 - u_pos_2sqrt_q^2 - 48 == 0 mod 3",
            "3*u_minus_p^2 - u_neg_2sqrt_q^2 + 64 == 0 mod 3",
        ],
        "jacobian_minor": {
            "rows": [
                "u_minus_p^2 - u_pos_2sqrt_q^2 - 48",
                "3*u_minus_p^2 - u_neg_2sqrt_q^2 + 64",
            ],
            "columns": ["u_minus_p", "u_neg_2sqrt_q"],
            "determinant_mod_p": 2,
            "nonzero": True,
        },
    }
    assert certs["13"] == {
        "place": "13",
        "field": "Q_13",
        "status": "locally_soluble",
        "certificate_type": "hensel_lift_from_mod_p",
        "residue_modulus": 13,
        "residue_point": {
            "X": 9,
            "u_minus_p": 8,
            "u_pos_2sqrt_q": 4,
            "u_neg_2sqrt_q": 3,
        },
        "equations_mod_p": [
            "u_minus_p^2 - u_pos_2sqrt_q^2 - 48 == 0 mod 13",
            "3*u_minus_p^2 - u_neg_2sqrt_q^2 + 64 == 0 mod 13",
        ],
        "jacobian_minor": {
            "rows": [
                "u_minus_p^2 - u_pos_2sqrt_q^2 - 48",
                "3*u_minus_p^2 - u_neg_2sqrt_q^2 + 64",
            ],
            "columns": ["u_minus_p", "u_neg_2sqrt_q"],
            "determinant_mod_p": 8,
            "nonzero": True,
        },
    }


def test_wl486_keeps_theorem_boundary_flags_after_global_witness() -> None:
    audit = build_wl486_local_solubility_gate(wl485=_wl485_input())

    assert audit["local_solubility_decided_here"] is True
    assert audit["local_solubility_summary"] == "locally_soluble_at_all_relevant_places"
    assert audit["global_solubility_decided_here"] is True
    assert audit["obstruction_proved_here"] is False
    assert audit["candidate_obstruction_refuted_here"] is True
    assert audit["explicit_c_d_cover_solved_here"] is True
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["boundary"].startswith(
        "This audits only wl486 / local_solubility_gate"
    )


def test_wl486_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl486.json"
    wl485 = tmp_path / "wl485.json"
    wl485.write_text(json.dumps(_wl485_input()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl486_local_solubility_gate.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl485",
            str(wl485),
            "--out",
            str(out),
            "--strict",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert payload["work_log"] == "wl486"
    assert payload["input_work_log"] == "wl485"
    assert payload["local_solubility_decided_here"] is True
    assert payload["global_solubility_decided_here"] is True
    assert payload["local_solubility_gate"]["candidate_survives_local_gate"] is True
