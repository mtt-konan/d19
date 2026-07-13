from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb.a1_certificates import build_a1, load_certificates, project_a1
from scripts.theory.aa_bb.a2_evidence import build_a2, load_boundary_spec, project_a2
from scripts.theory.aa_bb.consolidation_inputs import (
    CANONICAL_FILES,
    load_a0,
    materialize_a1_certificates,
)

DATA = ROOT / "data/theory/aa_bb/wl500"
RESULTS = ROOT / "results"
RESULT_PREFIX = "closure_quotient_rank_zero_aa_bb"

SHELL_FILES = {
    number: (
        f"closure_quotient_rank_zero_aa_bb_wl{number}_execute_next_finite_"
        "m_tail_shell_from_wl498_plan.json"
    )
    for number in (502, 504, 508, 510, 516)
}


def _legacy(filename: str) -> dict[str, object]:
    return json.loads((RESULTS / filename).read_text(encoding="utf-8"))


def test_all_shell_rank_kernel_projections_match_legacy_results() -> None:
    a0 = load_a0(DATA)
    a1 = build_a1(a0, load_certificates(DATA / "a1-certificates.v1.json"))
    for work_log, filename in SHELL_FILES.items():
        old = _legacy(filename)
        new = project_a1(a1, f"wl{work_log}")
        assert new["sample_summary"] == old["sample_summary"]
        assert new["rank_kernel_summary_by_sample"] == old["rank_kernel_summary_by_sample"]


def test_a0_a1_a2_cardinality_route_and_no_claim_parity() -> None:
    a0 = load_a0(DATA)
    a1 = build_a1(a0, load_certificates(DATA / "a1-certificates.v1.json"))
    spec = load_boundary_spec(DATA / "a2-boundary-spec.v1.json")
    a2 = build_a2(a0, a1, spec)
    projection = project_a2(a2, "wl527")
    summary = projection["global_summary"]
    assert (
        summary["ledger_entry_count"],
        summary["support_family_count"],
        summary["cover_family_count"],
    ) == (43, 13, 22)
    assert summary["entry_counts"] == {
        "globally_soluble_but_not_aa_bb_admissible": 29,
        "refuted": 10,
        "already_closed": 4,
    }
    assert summary["cover_counts"] == {
        "globally_soluble_but_not_aa_bb_admissible": 15,
        "refuted": 5,
        "already_closed": 2,
    }
    assert summary["opposite_side_squareclass_failure_entry_count"] == 29
    assert summary["not_ready_cover_family_count"] == 15
    assert summary["missing_explicit_d_vector_count"] == 1
    old_routes = set(
        _legacy("closure_quotient_rank_zero_aa_bb_wl526_post_wl525_route_choice_audit.json")[
            "route_families"
        ]
    )
    assert set(project_a2(a2, "wl526")["route_choices"]) == old_routes
    assert not any(projection["no_claims"].values())


def test_every_wl500_wl527_has_one_boundary_destination() -> None:
    spec = load_boundary_spec(DATA / "a2-boundary-spec.v1.json")
    assert sorted(spec["work_logs"], key=lambda value: int(value[2:])) == [
        f"wl{number}" for number in range(500, 528)
    ]
    assert spec["work_logs"]["wl523"] == "A2-LEMMA"
    assert spec["work_logs"]["wl527"] == "A2-SCOPE"


def test_a1_materialization_is_byte_identical_to_checked_in_projection(
    tmp_path: Path,
) -> None:
    for name in ("a0-ledger", "a0-witnesses", "a0-taxonomy", "a0-inventory"):
        shutil.copyfile(DATA / CANONICAL_FILES[name], tmp_path / CANONICAL_FILES[name])
    materialize_a1_certificates(RESULTS, tmp_path)
    assert (tmp_path / "a1-certificates.v1.json").read_bytes() == (
        DATA / "a1-certificates.v1.json"
    ).read_bytes()


def test_legacy_claim_boundaries_remain_false_at_every_checkpoint() -> None:
    forbidden = {
        "broad_rank_or_selmer_diagnostics_run",
        "complete_selmer_upper_bound_proved",
        "dim_sel2_eq_2_claimed",
        "rank_zero_claimed",
        "sha2_trivial_claimed",
        "uniform_m_tail_full_rank_claimed",
        "new_local_row_proved_here",
        "final_obstruction_candidate_selected_here",
    }
    for number in range(500, 528):
        matches = sorted(RESULTS.glob(f"{RESULT_PREFIX}_wl{number}_*.json"))
        assert matches, f"missing legacy parity payload for wl{number}"
        payload = json.loads(matches[0].read_text(encoding="utf-8"))
        for key in forbidden.intersection(payload):
            assert payload[key] is False, f"wl{number}.{key}"
        assert payload.get("family_exclusion_proved_count", 0) == 0


def _payload(number: int) -> dict[str, object]:
    matches = sorted(RESULTS.glob(f"{RESULT_PREFIX}_wl{number}_*.json"))
    assert len(matches) == 1
    return json.loads(matches[0].read_text(encoding="utf-8"))


def test_every_cover_stage_preserves_candidates_statuses_d_vectors_and_points() -> None:
    spec = load_boundary_spec(DATA / "a2-boundary-spec.v1.json")
    a0 = load_a0(DATA)
    points = {
        f"a0:{row['candidate_id']}": (row["point_on_cover"], row["point_on_E_L"])
        for row in a0.witnesses
    }
    points.update(
        {
            f"a1:{row['certificate_id']}": (row["point_on_cover"], row["point_on_E_L"])
            for row in load_certificates(DATA / "a1-certificates.v1.json")
            if row["status"] == "globally_soluble"
        }
    )
    row_keys = {
        500: "routed_active_u5_supports",
        505: "routed_active_shell7_supports",
        506: "resolved_deferred_entries",
        511: "routed_active_shell9_supports",
        512: "classified_deferred_entries",
        514: "classified_u7_entries",
        517: "routed_active_shell10_supports",
        519: "classified_shell10_u5_entries",
    }
    for number, row_key in row_keys.items():
        old = _payload(number)
        old_rows = old[row_key]
        if number == 514:
            old_rows = [
                dict(
                    row,
                    ambient_c_d_global_solubility=old[
                        "shared_cover_resolution_certificate"
                    ],
                )
                for row in old_rows
            ]
        new_rows = spec["stages"][f"wl{number}"]["candidate_rows"]
        assert [row["candidate_id"] for row in new_rows] == [
            row["candidate_id"] for row in old_rows
        ]
        for new, old_row in zip(new_rows, old_rows, strict=True):
            ambient = old_row["ambient_c_d_global_solubility"]
            assert new["d_vector"] == old_row["complete_c_d_cover"]["d_vector"]
            assert new["ambient_status"] == ambient["status"]
            assert new["certificate_type"] == ambient["certificate_type"]
            if ambient["status"] == "globally_soluble":
                point_on_cover, point_on_curve = points[new["point_ref"]]
                assert point_on_cover == ambient["point_on_cover"]
                assert point_on_curve == ambient["induced_point_on_E_L"]


def test_project_a1_reconstructs_every_cover_stage_from_tracked_evidence() -> None:
    a0 = load_a0(DATA)
    a1 = build_a1(a0, load_certificates(DATA / "a1-certificates.v1.json"))
    spec = load_boundary_spec(DATA / "a2-boundary-spec.v1.json")
    for work_log in ("wl500", "wl505", "wl506", "wl511", "wl512", "wl514", "wl517", "wl519"):
        actual = {row["candidate_id"]: row for row in project_a1(a1, work_log)["candidate_rows"]}
        expected = {
            row["candidate_id"]: {key: value for key, value in row.items() if key != "sample"}
            for row in spec["stages"][work_log]["candidate_rows"]
        }
        assert actual == expected


def test_every_boundary_stage_preserves_route_gate_and_state_transition() -> None:
    spec = load_boundary_spec(DATA / "a2-boundary-spec.v1.json")
    for number in (501, 503, 507, 509, 513, 515, 520, 524, 526):
        old = _payload(number)
        new = spec["stages"][f"wl{number}"]
        assert new["selected_next_gate"] == old["selected_next_gate"]
        expected_summaries = {
            key: value for key, value in old.items() if key.endswith("route_state_summary")
        }
        assert new.get("route_state_summaries", {}) == expected_summaries
    assert spec["stages"]["wl526"]["route_choices"] == sorted(
        _payload(526)["route_families"]
    )


def test_taxonomy_lemma_uniform_attempt_and_scope_stages_match_legacy() -> None:
    spec = load_boundary_spec(DATA / "a2-boundary-spec.v1.json")
    for number in (518, 521):
        old = _payload(number)
        new = spec["stages"][f"wl{number}"]
        assert new["ledger_summary"] == old["ledger_summary"]
        assert [row["candidate_id"] for row in new["ledger_rows"]] == [
            row["candidate_id"] for row in old["final_candidate_ledgers"]
        ]
    wl522, old522 = spec["stages"]["wl522"], _payload(522)
    assert wl522["taxonomy_summary"] == old522["taxonomy_summary"]
    assert wl522["selected_next_gate"] == old522["selected_next_gate"]
    wl523, old523 = spec["stages"]["wl523"], _payload(523)
    assert wl523["proof_decision"] == old523["proof_decision"]
    assert wl523["wl522_taxonomy_application"] == old523["wl522_taxonomy_application"]
    wl525, old525 = spec["stages"]["wl525"], _payload(525)
    for key in (
        "attempt_decision", "finite_input_snapshot", "precise_failure_point",
        "proof_obligation_audit", "uniform_lemma_target",
    ):
        assert wl525[key] == old525[key]
    wl527, old527 = spec["stages"]["wl527"], _payload(527)
    assert wl527["scope_summary"] == old527["scope_summary"]
    assert wl527["proof_data_readiness_decision"] == old527["proof_data_readiness_decision"]


def test_altered_a2_route_choice_fails_closed(tmp_path: Path) -> None:
    payload = json.loads((DATA / "a2-boundary-spec.v1.json").read_text(encoding="utf-8"))
    payload["route_choices"][0] = "invented_route"
    path = tmp_path / "a2-boundary-spec.v1.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="route choice set mismatch"):
        load_boundary_spec(path)


def test_a2_source_provenance_hashes_bind_all_legacy_payloads() -> None:
    spec = load_boundary_spec(DATA / "a2-boundary-spec.v1.json")
    for source in spec["source_payloads"].values():
        raw = (ROOT / source["path"]).read_bytes()
        assert len(raw) == source["size"]
        assert hashlib.sha256(raw).hexdigest() == source["sha256"]
