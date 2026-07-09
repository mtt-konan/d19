from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl519_resolve_shared_shell10_u5_ambient_c_d_global_solubility_cover import (  # noqa: E501
    build_wl519_resolve_shared_shell10_u5_ambient_c_d_global_solubility_cover,
)
from tests.test_closure_quotient_rank_zero_aa_bb_wl510_execute_next_finite_m_tail_shell_from_wl498_plan import (  # noqa: E501
    _wl491_input,
)


def _wl518_input() -> dict[str, object]:
    return json.loads(
        (
            ROOT
            / "results/"
            "closure_quotient_rank_zero_aa_bb_wl518_support_family_synthesis_after_wl517.json"
        ).read_text(encoding="utf-8")
    )


def _wl519() -> dict[str, object]:
    return build_wl519_resolve_shared_shell10_u5_ambient_c_d_global_solubility_cover(
        wl491=_wl491_input(),
        wl518=_wl518_input(),
    )


def test_wl519_resolves_exactly_the_shared_shell10_u5_cover() -> None:
    audit = _wl519()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert (
        audit["lemma_id"]
        == "WL519_resolve_shared_shell10_u5_ambient_C_d_global_solubility_cover"
    )
    assert audit["work_log"] == "wl519"
    assert audit["input_work_logs"] == ["wl491", "wl518"]
    assert audit["resolved_candidate_ids"] == [
        "AA_A10_B9_u_5_m_tail_shell10_candidate",
        "BB_A9_B10_u_5_m_tail_shell10_candidate",
    ]
    assert audit["resolved_shared_cover"] == {
        "L": 10,
        "T": 19,
        "d_vector": {
            "d_minus_p": 5,
            "d_pos_2sqrt_q": 5,
            "d_neg_2sqrt_q": 1,
        },
        "elliptic_curve_model": "V^2 = (X + 78)*(X - 1522)*(X + 1522)",
    }
    assert audit["resolution_summary"] == {
        "wl518_remaining_deferred_candidate_count": 2,
        "shared_cover_count_resolved_here": 1,
        "classified_candidate_entry_count": 2,
        "ambient_globally_soluble_count": 2,
        "ambient_global_solubility_refuted_count": 0,
        "exact_ambient_point_certificate_count": 1,
        "wl491_filter_applied_count": 2,
        "aa_bb_admissible_count": 0,
        "aa_bb_not_admissible_count": 2,
    }


def test_wl519_records_the_exact_rational_ambient_point_certificate() -> None:
    audit = _wl519()
    certificate = audit["shared_cover_resolution_certificate"]

    assert certificate["status"] == "globally_soluble"
    assert certificate["certificate_type"] == "exact_rational_point_on_C_d"
    assert certificate["point_on_cover"] == {
        "X": "1260642/121",
        "u_minus_p": "504/11",
        "u_pos_2sqrt_q": "464/11",
        "u_neg_2sqrt_q": "1202/11",
    }
    assert certificate["induced_point_on_E_L"] == {
        "X": "1260642/121",
        "Y": "1405474560/1331",
    }
    assert certificate["equation_checks"] == [
        "1260642/121 - -78 = 5*(504/11)^2",
        "1260642/121 - 1522 = 5*(464/11)^2",
        "1260642/121 - -1522 = (1202/11)^2",
    ]
    assert certificate["mordell_weil_context"]["point_used"] == (
        "(1260642/121, 1405474560/1331)"
    )
    assert certificate["mordell_weil_context"]["not_needed_for_non_solubility"] is True


def test_wl519_applies_wl491_and_routes_both_entries_to_not_admissible_ledgers() -> None:
    audit = _wl519()
    entries = audit["classified_shell10_u5_entries"]

    assert [entry["candidate_id"] for entry in entries] == [
        "AA_A10_B9_u_5_m_tail_shell10_candidate",
        "BB_A9_B10_u_5_m_tail_shell10_candidate",
    ]
    assert [entry["wl491_filter_result"]["output_class"] for entry in entries] == [
        "not_admissible",
        "not_admissible",
    ]
    assert entries[0]["wl491_filter_result"]["blocking_reasons"] == [
        "BB_common_source_product_not_square",
        "M_not_positive",
    ]
    assert entries[1]["wl491_filter_result"]["blocking_reasons"] == [
        "AA_common_source_product_not_square",
        "M_not_positive",
    ]
    for entry in entries:
        assert entry["routing_state"] == {
            "ledger_route": "globally_soluble_but_not_aa_bb_admissible_ledger",
            "ambient_c_d_global_solubility_status": "globally_soluble",
            "aa_bb_admissibility_status": "not_admissible",
            "candidate_selected": False,
        }


def test_wl519_stops_without_forbidden_work_or_next_route() -> None:
    audit = _wl519()

    assert audit["resolved_shell10_deferred_covers_here"] is True
    assert audit["wl491_filter_applied_to_new_point_here"] is True
    assert audit["shell11_executed_here"] is False
    assert audit["candidate_selected_here"] is False
    assert audit["post_wl519_route_choice_made_here"] is False
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
    assert audit["advance_to_wl520"] is False
    assert audit["stop_after_current_task"] is True


def test_wl519_cli_writes_result_json(tmp_path: Path) -> None:
    wl491 = tmp_path / "wl491.json"
    wl518 = tmp_path / "wl518.json"
    out = tmp_path / "wl519.json"
    wl491.write_text(json.dumps(_wl491_input()), encoding="utf-8")
    wl518.write_text(json.dumps(_wl518_input()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl519_resolve_shared_shell10_u5_ambient_c_d_global_solubility_cover.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl491",
            str(wl491),
            "--wl518",
            str(wl518),
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
    assert "work_log=wl519" in result.stdout
    assert "ambient_globally_soluble_count=2" in result.stdout
    assert "aa_bb_not_admissible_count=2" in result.stdout
    assert "post_wl519_route_choice_made_here=False" in result.stdout
    assert payload["work_log"] == "wl519"
