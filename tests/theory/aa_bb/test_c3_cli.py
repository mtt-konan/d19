from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

import scripts.theory.aa_bb.c3_pure_v_ell as module
from scripts.theory.aa_bb.c3_pure_v_ell import (
    C3_ALLOWLISTS,
    C3_PROOF_ALLOWLISTS,
    C3_STAGES,
    C3Evidence,
    build_c3,
    project_stage,
    semantic_projection,
)
from tests.theory.aa_bb.projection_digests import assert_projection_digest


@pytest.fixture(scope="module")
def evidence() -> C3Evidence:
    return build_c3()


def _canonical_wl568() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "work_log": "wl568",
        "violations": [],
        "proof_status": {
            "allocation_route_independent_obstruction_refuted_here": True,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        },
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "advance_to_m3": False,
        "rational_wl535_point_produced_here": False,
        "stop_after_current_task": True,
    }


def test_composition_has_exact_stage_order_and_allowlists(evidence: C3Evidence) -> None:
    assert tuple(f"wl{number}" for number in range(569, 586)) == C3_STAGES
    assert tuple(evidence.stages) == C3_STAGES
    assert tuple(C3_ALLOWLISTS) == C3_STAGES
    assert tuple(C3_PROOF_ALLOWLISTS) == C3_STAGES
    assert len(C3_STAGES) == 17


def test_full_stage_semantic_projections_have_frozen_digests(evidence: C3Evidence) -> None:
    for work_log in C3_STAGES:
        assert_projection_digest(
            "c3", work_log, semantic_projection(project_stage(evidence, work_log), work_log)
        )


def test_all_composed_stages_keep_no_claim_boundaries(evidence: C3Evidence) -> None:
    for work_log, stage in evidence.stages.items():
        assert set(stage) == C3_ALLOWLISTS[work_log] | {"ready", "violations"}
        assert set(semantic_projection(stage, work_log)) == C3_ALLOWLISTS[work_log]
        assert stage["work_log"] == work_log
        assert stage["status"] == "ok"
        assert stage["ready"] is True
        assert stage["violations"] == []
        assert stage["complete_selmer_upper_bound_proved"] is False
        assert stage["rank_zero_claimed"] is False
        assert stage["sha2_trivial_claimed"] is False
        assert stage["advance_to_m3"] is False
        assert stage["stop_after_current_task"] is True
        assert stage["rational_wl535_point_produced_here"] is False
        assert set(stage["proof_status"]) == C3_PROOF_ALLOWLISTS[work_log]
        assert stage["proof_status"]["uniform_full_wl535_obstruction_proved_here"] is False
        assert stage["proof_status"]["advance_to_m3"] is False


def test_composition_calls_c2_and_each_slice_once(monkeypatch) -> None:
    calls = {"c2": 0, "real": 0, "magnitude": 0, "quotient": 0}
    c2_stage = _canonical_wl568()
    real_wl574 = {"work_log": "wl574"}
    magnitude_wl580 = {"work_log": "wl580"}
    seen: dict[str, object] = {}

    def counted_c2() -> SimpleNamespace:
        calls["c2"] += 1
        return SimpleNamespace(stages={"wl568": c2_stage})

    def counted_real(wl568) -> dict[str, dict[str, object]]:
        calls["real"] += 1
        seen["wl568"] = wl568
        return {work_log: {"work_log": work_log} for work_log in C3_STAGES[:6]} | {
            "wl574": real_wl574
        }

    def counted_magnitude(wl574) -> dict[str, dict[str, object]]:
        calls["magnitude"] += 1
        seen["wl574"] = wl574
        return {work_log: {"work_log": work_log} for work_log in C3_STAGES[6:12]} | {
            "wl580": magnitude_wl580
        }

    def counted_quotient(wl580) -> dict[str, dict[str, object]]:
        calls["quotient"] += 1
        seen["wl580"] = wl580
        return {work_log: {"work_log": work_log} for work_log in C3_STAGES[12:]}

    monkeypatch.setattr(module, "build_c2", counted_c2)
    monkeypatch.setattr(module, "build_c3_real_branch", counted_real)
    monkeypatch.setattr(module, "build_c3_magnitude_descent", counted_magnitude)
    monkeypatch.setattr(module, "build_c3_quotient_limits", counted_quotient)

    result = module.build_c3()

    assert calls == {"c2": 1, "real": 1, "magnitude": 1, "quotient": 1}
    assert seen == {"wl568": c2_stage, "wl574": real_wl574, "wl580": magnitude_wl580}
    assert tuple(result.stages) == C3_STAGES


def test_invalid_c2_predecessor_fails_closed() -> None:
    invalid = _canonical_wl568()
    invalid["proof_status"] = dict(invalid["proof_status"])
    invalid["proof_status"]["allocation_route_independent_obstruction_refuted_here"] = False
    failed = build_c3(SimpleNamespace(stages={"wl568": invalid}))
    assert tuple(failed.stages) == C3_STAGES
    assert failed["wl569"]["status"] == "issues"
    assert failed["wl569"]["violations"] == ["wl568_input_not_ready"]
    assert failed["wl569"]["proof_status"] == {}
    assert all(stage["status"] == "issues" for stage in failed.stages.values())
    assert not module._strict_ready(failed)


def test_projection_rejects_unknown_missing_mislabeled_and_mutated_stages(
    evidence: C3Evidence,
) -> None:
    with pytest.raises(KeyError):
        project_stage(evidence, "wl568")
    missing = dict(evidence.stages)
    del missing["wl585"]
    with pytest.raises(KeyError):
        project_stage(missing, "wl585")
    mislabeled = {"wl569": dict(evidence["wl569"])}
    mislabeled["wl569"]["work_log"] = "wl570"
    with pytest.raises(ValueError):
        project_stage(mislabeled, "wl569")

    unknown = dict(evidence["wl569"])
    unknown["unexpected"] = True
    with pytest.raises(ValueError):
        semantic_projection(unknown, "wl569")
    missing_field = dict(evidence["wl570"])
    del missing_field["system_certificate"]
    with pytest.raises(ValueError):
        semantic_projection(missing_field, "wl570")
    bad_checkpoint = dict(evidence["wl571"])
    bad_checkpoint["input_checkpoint"] = {"work_log": "wl569", "ready": True}
    with pytest.raises(ValueError):
        semantic_projection(bad_checkpoint, "wl571")
    bad_proof = dict(evidence["wl585"])
    bad_proof["proof_status"] = dict(bad_proof["proof_status"])
    bad_proof["proof_status"]["restricted_combined_elliptic_image_solved_here"] = True
    with pytest.raises(ValueError):
        semantic_projection(bad_proof, "wl585")
    bad_top_level = dict(evidence["wl584"])
    bad_top_level["rank_zero_claimed"] = True
    with pytest.raises(ValueError):
        semantic_projection(bad_top_level, "wl584")


def test_cli_writes_one_strict_deterministic_17_stage_payload(tmp_path: Path) -> None:
    out = tmp_path / "c3.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.theory.aa_bb.c3_pure_v_ell",
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.stdout == "stage_count=17\nstatus=ok\n"
    payload_text = out.read_text(encoding="utf-8")
    payload = json.loads(payload_text)
    assert payload["schema_version"] == 1
    assert tuple(payload["stages"]) == C3_STAGES
    assert all(stage["status"] == "ok" for stage in payload["stages"].values())
    assert payload_text == json.dumps(payload, indent=2, sort_keys=True) + "\n"


def test_orchestrator_has_no_forbidden_runtime_dependency() -> None:
    source = (ROOT / "scripts/theory/aa_bb/c3_pure_v_ell.py").read_text(encoding="utf-8")
    for forbidden in (
        "audit_closure_",
        "results/",
        "importlib",
        ".glob(",
        ".rglob(",
        "subprocess",
        "wl586",
        "c1_",
        "consolidated",
    ):
        assert forbidden not in source
