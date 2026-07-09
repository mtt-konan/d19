from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl512_resolve_shell9_deferred_ambient_c_d_global_solubility_ledgers import (  # noqa: E501
    build_wl512_resolve_shell9_deferred_ambient_c_d_global_solubility_ledgers,
)
from tests.test_closure_quotient_rank_zero_aa_bb_wl511_route_active_shell9_m_tail_supports import (
    _wl491_input,
    _wl511,
)


def _wl512() -> dict[str, object]:
    return build_wl512_resolve_shell9_deferred_ambient_c_d_global_solubility_ledgers(
        wl491=_wl491_input(),
        wl511=_wl511(),
    )


def test_wl512_classifies_exactly_the_four_wl511_deferred_shell9_ledgers() -> None:
    audit = _wl512()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == (
        "WL512_resolve_shell9_deferred_ambient_C_d_global_solubility_ledgers"
    )
    assert audit["work_log"] == "wl512"
    assert audit["input_work_logs"] == ["wl491", "wl511"]
    assert audit["resolution_summary"] == {
        "wl511_deferred_entry_count": 4,
        "explicitly_classified_entry_count": 4,
        "ambient_globally_soluble_count": 0,
        "ambient_global_solubility_refuted_count": 2,
        "ambient_global_solubility_still_deferred_count": 2,
        "wl491_filter_applied_count": 0,
        "aa_bb_admissible_count": 0,
        "aa_bb_not_admissible_count": 0,
        "aa_bb_missing_pullback_data_count": 0,
        "aa_bb_filter_not_applied_count": 4,
    }
    assert [entry["candidate_id"] for entry in audit["classified_deferred_entries"]] == [
        "AA_A4_B9_v_13_m_tail_shell9_candidate",
        "AA_A7_B9_u_7_m_tail_shell9_candidate",
        "BB_A9_B4_v_13_m_tail_shell9_candidate",
        "BB_A9_B7_u_7_m_tail_shell9_candidate",
    ]
    assert audit["shell9_globally_soluble_not_admissible_reopened_count"] == 0
    assert audit["closed_ledgers_reopened_count"] == 0


def test_wl512_refutes_the_two_v13_deferred_ledgers_without_wl491() -> None:
    audit = _wl512()
    refuted = [
        entry
        for entry in audit["classified_deferred_entries"]
        if entry["candidate_support"] == ["v_13"]
    ]

    assert [entry["candidate_id"] for entry in refuted] == [
        "AA_A4_B9_v_13_m_tail_shell9_candidate",
        "BB_A9_B4_v_13_m_tail_shell9_candidate",
    ]
    for entry in refuted:
        assert entry["complete_c_d_cover"]["d_vector"] == {
            "d_minus_p": 13,
            "d_pos_2sqrt_q": 1,
            "d_neg_2sqrt_q": 13,
        }
        certificate = entry["ambient_c_d_global_solubility"]
        assert certificate["status"] == "globally_not_soluble"
        assert certificate["certificate_type"] == (
            "targeted_mordell_weil_torsion_lift_refutation"
        )
        assert certificate["rank_zero_certificate"] == {
            "rank": 0,
            "torsion_points": ["O", "(-466,0)", "(210,0)", "(466,0)"],
            "scope": "single instantiated curve E_{L=4,T=13}, not a family theorem",
        }
        assert certificate["cover_lift_summary"] == {
            "torsion_point_count_checked": 4,
            "torsion_lift_count": 0,
            "point_at_infinity_lift_exists": False,
            "affine_torsion_lift_count": 0,
        }
        assert entry["wl491_filter_result"]["output_class"] == "not_applied"
        assert entry["routing_state"]["ledger_route"] == (
            "ambient_c_d_global_solubility_refuted_ledger"
        )


def test_wl512_keeps_the_two_u7_ledgers_deferred_with_explicit_reason() -> None:
    audit = _wl512()
    deferred = [
        entry
        for entry in audit["classified_deferred_entries"]
        if entry["candidate_support"] == ["u_7"]
    ]

    assert [entry["candidate_id"] for entry in deferred] == [
        "AA_A7_B9_u_7_m_tail_shell9_candidate",
        "BB_A9_B7_u_7_m_tail_shell9_candidate",
    ]
    for entry in deferred:
        assert entry["complete_c_d_cover"]["d_vector"] == {
            "d_minus_p": 7,
            "d_pos_2sqrt_q": 7,
            "d_neg_2sqrt_q": 1,
        }
        certificate = entry["ambient_c_d_global_solubility"]
        assert certificate["status"] == "global_solubility_deferred"
        assert certificate["certificate_type"] == "none_recorded_here"
        assert certificate["deferred_reason"] == (
            "rank_one_ambient_curve_has_no_exhaustive_cover_lift_certificate_here"
        )
        assert certificate["bounded_mordell_weil_probe"]["not_a_global_insolubility_proof"] is True
        assert entry["wl491_filter_result"] == {
            "output_class": "not_applied",
            "reason": "ambient_global_C_d_solubility_not_established",
            "blocking_reasons": ["ambient_C_d_global_point_not_established"],
        }
        assert entry["routing_state"]["ledger_route"] == (
            "ambient_c_d_solubility_deferred_ledger"
        )


def test_wl512_stops_without_candidate_selection_or_forbidden_claims() -> None:
    audit = _wl512()

    assert audit["classified_wl511_deferred_ledgers_here"] is True
    assert audit["all_wl511_deferred_entries_resolved_here"] is False
    assert audit["candidate_selected_here"] is False
    assert audit["new_m_tail_row_proved_here"] is False
    assert audit["new_local_row_proved_here"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["family_rank_or_selmer_diagnostics_run"] is False
    assert audit["single_curve_diagnostics_run"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["uniform_m_tail_full_rank_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["shell10_executed_here"] is False
    assert audit["advance_to_wl513"] is False
    assert audit["stop_after_current_task"] is True


def test_wl512_cli_writes_result_json(tmp_path: Path) -> None:
    wl491 = tmp_path / "wl491.json"
    wl511 = tmp_path / "wl511.json"
    out = tmp_path / "wl512.json"
    wl491.write_text(json.dumps(_wl491_input()), encoding="utf-8")
    wl511.write_text(json.dumps(_wl511()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl512_resolve_shell9_deferred_ambient_c_d_global_solubility_ledgers.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl491",
            str(wl491),
            "--wl511",
            str(wl511),
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
    assert "work_log=wl512" in result.stdout
    assert "ambient_global_solubility_refuted_count=2" in result.stdout
    assert "ambient_global_solubility_still_deferred_count=2" in result.stdout
    assert "advance_to_wl513=False" in result.stdout
    assert payload["work_log"] == "wl512"
