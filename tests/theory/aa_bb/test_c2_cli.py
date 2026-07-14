from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb.c2_pure_v_ell import (
    C2_ALLOWLISTS,
    C2_STAGES,
    C2Evidence,
    build_c2,
    project_stage,
    semantic_projection,
)
from tests.theory.aa_bb.projection_digests import assert_projection_digest


@pytest.fixture(scope="module")
def evidence() -> C2Evidence:
    return build_c2()


def test_composition_has_exact_stage_and_allowlist_maps(evidence: C2Evidence) -> None:
    assert tuple(f"wl{number}" for number in range(542, 569)) == C2_STAGES
    assert tuple(evidence.stages) == C2_STAGES
    assert tuple(C2_ALLOWLISTS) == C2_STAGES
    assert len(C2_STAGES) == 27


def test_full_stage_semantic_projections_have_frozen_digests(
    evidence: C2Evidence,
) -> None:
    for work_log in C2_STAGES:
        assert_projection_digest(
            "c2", work_log, semantic_projection(project_stage(evidence, work_log), work_log)
        )


def test_all_composed_stages_keep_no_claim_boundaries(evidence: C2Evidence) -> None:
    for work_log, stage in evidence.stages.items():
        assert stage["work_log"] == work_log
        assert stage["status"] == "ok"
        assert stage["ready"] is True
        assert stage["violations"] == []
        assert stage["complete_selmer_upper_bound_proved"] is False
        assert stage["rank_zero_claimed"] is False
        assert stage["sha2_trivial_claimed"] is False
        assert stage["advance_to_m3"] is False
        assert stage["proof_status"]["uniform_full_wl535_obstruction_proved_here"] is False


def test_composition_calls_each_canonical_builder_once(monkeypatch) -> None:
    import scripts.theory.aa_bb.c2_pure_v_ell as module

    calls = {"c1": 0, "global": 0, "character": 0, "allocation": 0}
    real_c1 = module.build_c1
    real_global = module.build_c2_global_descent
    real_character = module.build_c2_character_system
    real_allocation = module.build_c2_allocation

    def counted_c1(*args, **kwargs):
        calls["c1"] += 1
        return real_c1(*args, **kwargs)

    def counted_global(*args, **kwargs):
        calls["global"] += 1
        return real_global(*args, **kwargs)

    def counted_character(*args, **kwargs):
        calls["character"] += 1
        return real_character(*args, **kwargs)

    def counted_allocation(*args, **kwargs):
        calls["allocation"] += 1
        return real_allocation(*args, **kwargs)

    monkeypatch.setattr(module, "build_c1", counted_c1)
    monkeypatch.setattr(module, "build_c2_global_descent", counted_global)
    monkeypatch.setattr(module, "build_c2_character_system", counted_character)
    monkeypatch.setattr(module, "build_c2_allocation", counted_allocation)
    result = module.build_c2()
    assert tuple(result.stages) == C2_STAGES
    assert calls == {"c1": 1, "global": 1, "character": 1, "allocation": 1}


def test_projection_fails_closed_on_unknown_missing_and_mislabeled_stage(
    evidence: C2Evidence,
) -> None:
    with pytest.raises(KeyError):
        project_stage(evidence, "wl541")
    missing = dict(evidence.stages)
    del missing["wl568"]
    with pytest.raises(KeyError):
        project_stage(missing, "wl568")
    mislabeled = {"wl568": dict(evidence.stages["wl568"])}
    mislabeled["wl568"]["work_log"] = "wl567"
    with pytest.raises(ValueError):
        project_stage(mislabeled, "wl568")


def test_semantic_projection_rejects_unknown_fields_and_no_claim_mutation(
    evidence: C2Evidence,
) -> None:
    malformed = dict(evidence.stages["wl563"])
    malformed["unexpected"] = True
    with pytest.raises(ValueError):
        semantic_projection(malformed, "wl563")
    no_claim = {work_log: dict(stage) for work_log, stage in evidence.stages.items()}
    no_claim["wl568"]["rank_zero_claimed"] = True
    assert not module_strict_ready(C2Evidence(stages=no_claim))
    no_claim_top = {work_log: dict(stage) for work_log, stage in evidence.stages.items()}
    no_claim_top["wl567"]["theorem_level_selmer_matrix_claimed"] = True
    assert not module_strict_ready(C2Evidence(stages=no_claim_top))
    no_claim_proof = {work_log: dict(stage) for work_log, stage in evidence.stages.items()}
    no_claim_proof["wl568"]["proof_status"] = dict(no_claim_proof["wl568"]["proof_status"])
    no_claim_proof["wl568"]["proof_status"][
        "selected_orientation_norm_intersection_solved_here"
    ] = True
    assert not module_strict_ready(C2Evidence(stages=no_claim_proof))


def module_strict_ready(evidence: C2Evidence) -> bool:
    import scripts.theory.aa_bb.c2_pure_v_ell as module

    return module._strict_ready(evidence)


def test_cli_writes_one_deterministic_27_stage_payload(tmp_path: Path) -> None:
    out = tmp_path / "c2.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.theory.aa_bb.c2_pure_v_ell",
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "stage_count=27" in result.stdout
    assert "status=ok" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    assert tuple(payload["stages"]) == C2_STAGES
    assert all(stage["status"] == "ok" for stage in payload["stages"].values())
    assert out.read_text(encoding="utf-8") == json.dumps(payload, indent=2, sort_keys=True) + "\n"


def test_orchestrator_has_no_legacy_or_results_dependency() -> None:
    source = (ROOT / "scripts/theory/aa_bb/c2_pure_v_ell.py").read_text(encoding="utf-8")
    for forbidden in (
        "audit_closure_",
        "results/",
        "importlib",
        ".glob(",
        ".rglob(",
        "wl569",
        "C3",
    ):
        assert forbidden not in source
