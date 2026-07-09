from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl514_resolve_remaining_shell9_u7_ambient_c_d_global_solubility_ledger import (  # noqa: E501
    build_wl514_resolve_remaining_shell9_u7_ambient_c_d_global_solubility_ledger,
)
from tests.test_closure_quotient_rank_zero_aa_bb_wl513_post_wl512_route_choice import (
    _wl513,
)


def _wl514() -> dict[str, object]:
    return build_wl514_resolve_remaining_shell9_u7_ambient_c_d_global_solubility_ledger(
        wl513=_wl513(),
    )


def test_wl514_resolves_exactly_the_shared_shell9_u7_cover_by_no_lift_certificate() -> None:
    audit = _wl514()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == (
        "WL514_resolve_remaining_shell9_u7_ambient_C_d_global_solubility_ledger"
    )
    assert audit["work_log"] == "wl514"
    assert audit["input_work_log"] == "wl513"
    assert audit["resolved_remaining_shell9_u7_ledger_here"] is True
    assert audit["resolution_summary"] == {
        "wl513_remaining_deferred_candidate_count": 2,
        "shared_cover_count_resolved_here": 1,
        "classified_candidate_entry_count": 2,
        "ambient_globally_soluble_count": 0,
        "ambient_global_solubility_refuted_count": 2,
        "exhaustive_no_lift_certificate_count": 1,
        "wl491_filter_applied_count": 0,
        "aa_bb_admissible_count": 0,
        "aa_bb_filter_not_applied_count": 2,
    }
    assert audit["resolved_candidate_ids"] == [
        "AA_A7_B9_u_7_m_tail_shell9_candidate",
        "BB_A9_B7_u_7_m_tail_shell9_candidate",
    ]
    assert audit["resolved_shared_cover"] == {
        "L": 7,
        "T": 16,
        "d_vector": {
            "d_minus_p": 7,
            "d_pos_2sqrt_q": 7,
            "d_neg_2sqrt_q": 1,
        },
        "elliptic_curve_model": "V^2 = (X + 120)*(X - 904)*(X + 904)",
    }


def test_wl514_certificate_exhausts_the_rank_one_mordell_weil_image_mod_17() -> None:
    audit = _wl514()
    certificate = audit["shared_cover_resolution_certificate"]

    assert certificate["status"] == "globally_not_soluble"
    assert certificate["certificate_type"] == "mordell_weil_sieve_no_lift_mod_17"
    assert certificate["cover_equations"] == [
        "X + 120 = 7*u_minus_p^2",
        "X - 904 = 7*u_pos_2sqrt_q^2",
        "X + 904 = u_neg_2sqrt_q^2",
    ]
    assert certificate["mordell_weil_certificate"] == {
        "rank": 1,
        "generator": "(1032,16896)",
        "torsion_points": ["O", "(-904,0)", "(-120,0)", "(904,0)"],
        "exhaustive_description": "E(Q)=<G> + E(Q)[2] for G=(1032,16896)",
        "scope": "single instantiated curve E_{L=7,T=16}, not a family theorem",
    }
    sieve = certificate["mod_17_sieve"]
    assert sieve["prime"] == 17
    assert sieve["good_reduction"] is True
    assert sieve["legendre_symbol_7_mod_17"] == -1
    assert sieve["generator_reduction"] == "(12,15)"
    assert sieve["generator_order_mod_17"] == 6
    assert sieve["rational_reduction_image_size"] == 12
    assert sieve["local_lift_candidate_reductions"] == [
        "(6,6)",
        "(6,11)",
        "(10,7)",
        "(10,10)",
        "(13,8)",
        "(13,9)",
    ]
    assert sieve["rational_image_intersection_with_local_lift_candidates"] == []
    assert sieve["point_at_infinity_lift_blocked_reason"] == (
        "7_is_not_a_square_mod_17"
    )


def test_wl514_routes_both_u7_ledgers_to_refuted_without_applying_wl491() -> None:
    audit = _wl514()

    assert [entry["candidate_id"] for entry in audit["classified_u7_entries"]] == [
        "AA_A7_B9_u_7_m_tail_shell9_candidate",
        "BB_A9_B7_u_7_m_tail_shell9_candidate",
    ]
    for entry in audit["classified_u7_entries"]:
        assert entry["candidate_support"] == ["u_7"]
        assert entry["ambient_c_d_global_solubility"]["status"] == (
            "globally_not_soluble"
        )
        assert entry["wl491_filter_result"] == {
            "output_class": "not_applied",
            "reason": "ambient_C_d_global_solubility_refuted",
            "blocking_reasons": ["ambient_C_d_has_no_rational_point"],
        }
        assert entry["routing_state"] == {
            "ledger_route": "ambient_c_d_global_solubility_refuted_ledger",
            "ambient_c_d_global_solubility_status": "globally_not_soluble",
            "wl491_filter_applied": False,
            "candidate_selected": False,
        }


def test_wl514_stops_without_forbidden_work_or_next_route_choice() -> None:
    audit = _wl514()

    assert audit["shell10_executed_here"] is False
    assert audit["post_wl514_route_choice_made_here"] is False
    assert audit["candidate_selected_here"] is False
    assert audit["new_m_tail_or_kernel_candidate_selected_here"] is False
    assert audit["new_m_tail_row_proved_here"] is False
    assert audit["new_local_row_proved_here"] is False
    assert audit["new_shell_or_grid_refreshed_here"] is False
    assert audit["m_tail_diagnostics_extended_here"] is False
    assert audit["new_supports_computed_here"] is False
    assert audit["wl491_filter_applied_to_new_point_here"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["family_rank_or_selmer_diagnostics_run"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["uniform_m_tail_full_rank_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["advance_to_wl515"] is False
    assert audit["stop_after_current_task"] is True


def test_wl514_cli_writes_result_json(tmp_path: Path) -> None:
    wl513_path = tmp_path / "wl513.json"
    out = tmp_path / "wl514.json"
    wl513_path.write_text(json.dumps(_wl513()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl514_resolve_remaining_shell9_u7_ambient_c_d_global_solubility_ledger.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl513",
            str(wl513_path),
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
    assert "work_log=wl514" in result.stdout
    assert "ambient_global_solubility_refuted_count=2" in result.stdout
    assert "wl491_filter_applied_count=0" in result.stdout
    assert "post_wl514_route_choice_made_here=False" in result.stdout
    assert payload["work_log"] == "wl514"
