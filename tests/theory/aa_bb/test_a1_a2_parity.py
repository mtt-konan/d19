from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb.a1_certificates import build_a1, load_certificates, project_a1
from scripts.theory.aa_bb.a2_evidence import build_a2, load_boundary_spec, project_a2
from scripts.theory.aa_bb.consolidation_inputs import (
    load_a0,
)
from tests.theory.aa_bb.projection_digests import assert_projection_digest

DATA = ROOT / "data/theory/aa_bb/wl500"


def test_all_shell_rank_kernel_projections_have_frozen_digests() -> None:
    a0 = load_a0(DATA)
    a1 = build_a1(a0, load_certificates(DATA / "a1-certificates.v1.json"))
    for work_log in ("wl502", "wl504", "wl508", "wl510", "wl516"):
        assert_projection_digest("a1", work_log, project_a1(a1, work_log))


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
    assert set(project_a2(a2, "wl526")["route_choices"]) == set(spec["route_choices"])
    assert not any(projection["no_claims"].values())
    for number in range(500, 528):
        assert_projection_digest("a2", f"wl{number}", project_a2(a2, f"wl{number}"))


def test_every_wl500_wl527_has_one_boundary_destination() -> None:
    spec = load_boundary_spec(DATA / "a2-boundary-spec.v1.json")
    assert sorted(spec["work_logs"], key=lambda value: int(value[2:])) == [
        f"wl{number}" for number in range(500, 528)
    ]
    assert spec["work_logs"]["wl523"] == "A2-LEMMA"
    assert spec["work_logs"]["wl527"] == "A2-SCOPE"


def test_claim_boundaries_remain_false_at_every_checkpoint() -> None:
    a0 = load_a0(DATA)
    a1 = build_a1(a0, load_certificates(DATA / "a1-certificates.v1.json"))
    spec = load_boundary_spec(DATA / "a2-boundary-spec.v1.json")
    a2 = build_a2(a0, a1, spec)
    assert all(
        not any(project_a2(a2, f"wl{number}")["no_claims"].values()) for number in range(500, 528)
    )


def test_every_cover_stage_preserves_candidates_statuses_d_vectors_and_points() -> None:
    spec = load_boundary_spec(DATA / "a2-boundary-spec.v1.json")
    a0 = load_a0(DATA)
    a1 = build_a1(a0, load_certificates(DATA / "a1-certificates.v1.json"))
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
    for number in (500, 505, 506, 511, 512, 514, 517, 519):
        new_rows = spec["stages"][f"wl{number}"]["candidate_rows"]
        assert {row["candidate_id"] for row in new_rows} == {
            row["candidate_id"] for row in project_a1(a1, f"wl{number}")["candidate_rows"]
        }
        assert all(row["point_ref"] in points for row in new_rows if "point_ref" in row)


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
    a0 = load_a0(DATA)
    a1 = build_a1(a0, load_certificates(DATA / "a1-certificates.v1.json"))
    spec = load_boundary_spec(DATA / "a2-boundary-spec.v1.json")
    a2 = build_a2(a0, a1, spec)
    for number in (501, 503, 507, 509, 513, 515, 520, 524, 526):
        new = spec["stages"][f"wl{number}"]
        projection = project_a2(a2, f"wl{number}")
        for key, value in new.items():
            assert projection[key] == value
    assert spec["stages"]["wl526"]["route_choices"] == sorted(spec["route_choices"])


def test_taxonomy_lemma_uniform_attempt_and_scope_stages_match_tracked_spec() -> None:
    a0 = load_a0(DATA)
    a1 = build_a1(a0, load_certificates(DATA / "a1-certificates.v1.json"))
    spec = load_boundary_spec(DATA / "a2-boundary-spec.v1.json")
    a2 = build_a2(a0, a1, spec)
    for number in (518, 521, 522, 523, 525, 527):
        stage = spec["stages"][f"wl{number}"]
        projection = project_a2(a2, f"wl{number}")
        for key, value in stage.items():
            assert projection[key] == value


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
        assert source["path"].startswith("results/")
        assert len(source["sha256"]) == 64
        assert source["size"] > 0
