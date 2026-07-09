from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl522_support_cover_taxonomy_to_lemma_candidate_checkpoint import (  # noqa: E501
    build_wl522_support_cover_taxonomy_to_lemma_candidate_checkpoint,
    load_wl491_to_wl521_payloads,
)


def _wl522() -> dict[str, object]:
    return build_wl522_support_cover_taxonomy_to_lemma_candidate_checkpoint(
        ledger_payloads=load_wl491_to_wl521_payloads(ROOT / "results")
    )


def _row_by_cover(audit: dict[str, object], cover_family: str) -> dict[str, object]:
    rows = audit["support_cover_taxonomy"]
    assert isinstance(rows, list)
    for row in rows:
        assert isinstance(row, dict)
        if row["cover_family"] == cover_family:
            return row
    raise AssertionError(f"missing cover family {cover_family}")


def test_wl522_builds_stable_taxonomy_summary_from_wl521_without_new_route_work() -> None:
    audit = _wl522()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL522_support_cover_taxonomy_to_lemma_candidate_checkpoint"
    assert audit["work_log"] == "wl522"
    assert audit["input_work_log"] == "wl521"
    assert audit["input_work_logs"] == [f"wl{index}" for index in range(491, 522)]
    assert audit["taxonomy_summary"] == {
        "final_candidate_ledger_entry_count": 43,
        "support_family_count": 13,
        "cover_family_count": 22,
        "taxonomy_row_count": 22,
        "ambient_globally_not_soluble_entry_count": 10,
        "globally_soluble_but_not_aa_bb_admissible_entry_count": 29,
        "already_closed_entry_count": 4,
        "genuinely_deferred_entry_count": 0,
        "aa_bb_admissible_entry_count": 0,
        "ambient_globally_not_soluble_cover_family_count": 5,
        "globally_soluble_but_not_aa_bb_admissible_cover_family_count": 15,
        "processed_or_duplicate_cover_family_count": 2,
        "genuinely_deferred_cover_family_count": 0,
        "aa_bb_admissible_cover_family_count": 0,
    }
    assert audit["classification_order"] == [
        "ambient_globally_not_soluble",
        "globally_soluble_but_not_aa_bb_admissible",
        "processed_or_duplicate_m_tail_support",
    ]


def test_wl522_taxonomy_distinguishes_refutation_from_common_source_failure() -> None:
    audit = _wl522()

    refuted_u5 = _row_by_cover(audit, "support=u_5|L=5|T=8|d=(5,5,1)")
    assert refuted_u5["classification"] == "refuted"
    assert refuted_u5["failure_mode"] == "ambient_globally_not_soluble"
    assert refuted_u5["ambient_c_d_global_solubility_status"] == "globally_not_soluble"
    assert refuted_u5["lemma_candidate_status"] == "dead_end"

    soluble_u5 = _row_by_cover(audit, "support=u_5|L=10|T=19|d=(5,5,1)")
    assert soluble_u5["classification"] == "globally_soluble_but_not_aa_bb_admissible"
    assert soluble_u5["failure_mode"] == "common_source_aa_bb_admissibility_failure"
    assert soluble_u5["ambient_c_d_global_solubility_status"] == "globally_soluble"
    assert soluble_u5["candidate_ids"] == [
        "AA_A10_B9_u_5_m_tail_shell10_candidate",
        "BB_A9_B10_u_5_m_tail_shell10_candidate",
    ]
    assert soluble_u5["blocking_reasons"] == [
        "AA_common_source_product_not_square",
        "BB_common_source_product_not_square",
        "M_not_positive",
    ]
    assert soluble_u5["lemma_candidate_status"] == "theorem-candidate"

    processed_u3 = _row_by_cover(audit, "support=u_3|L=3|T=11|d=(?,?,?)")
    assert processed_u3["failure_mode"] == "processed_or_duplicate_m_tail_support"
    assert processed_u3["lemma_candidate_status"] == "data-only"


def test_wl522_extracts_one_next_common_source_lemma_candidate() -> None:
    audit = _wl522()

    patterns = {pattern["pattern_id"]: pattern for pattern in audit["lemma_candidate_patterns"]}
    assert patterns["common_source_square_obstruction_across_not_admissible_cover_families"][
        "candidate_status"
    ] == "theorem-candidate"
    assert patterns["common_source_square_obstruction_across_not_admissible_cover_families"][
        "cover_family_count"
    ] == 15
    assert patterns["mixed_refuted_not_admissible_same_support_families"][
        "candidate_status"
    ] == "data-only"
    assert patterns["ambient_globally_not_soluble_cover_families"][
        "candidate_status"
    ] == "dead_end"

    selected = audit["selected_next_proof_level_lemma_candidate"]
    assert selected == {
        "status": "named_lemma_candidate_isolated",
        "lemma_candidate_id": (
            "common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families"
        ),
        "candidate_status": "theorem-candidate",
        "entered_here": False,
        "proof_level_work_done_here": False,
        "why_this_one": (
            "Every globally soluble non-admissible cover family in the wl491-wl521 "
            "taxonomy fails the opposite AA/BB common-source square check; this is "
            "the only reusable pattern that is not already an ambient refutation "
            "or processed M_tail duplicate."
        ),
    }


def test_wl522_stops_without_shell11_or_forbidden_selmer_claims() -> None:
    audit = _wl522()

    assert audit["shell11_executed_here"] is False
    assert audit["m_tail_diagnostics_extended_here"] is False
    assert audit["new_supports_computed_here"] is False
    assert audit["new_c_d_solubility_tested_here"] is False
    assert audit["wl491_filter_applied_to_new_point_here"] is False
    assert audit["candidate_selected_here"] is False
    assert audit["final_obstruction_candidate_selected_here"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["uniform_m_tail_full_rank_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["advance_to_wl523"] is False
    assert audit["stop_after_current_task"] is True


def test_wl522_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl522.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl522_support_cover_taxonomy_to_lemma_candidate_checkpoint.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--ledger-dir",
            str(ROOT / "results"),
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
    assert "work_log=wl522" in result.stdout
    assert (
        "selected_lemma=common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families"
        in result.stdout
    )
    assert "shell11_executed_here=False" in result.stdout
    assert payload["work_log"] == "wl522"
    assert payload["selected_next_proof_level_lemma_candidate"]["entered_here"] is False
