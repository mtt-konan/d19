from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from collections import OrderedDict
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[3]
DATA = ROOT / "data" / "theory" / "aa_bb" / "wl500"
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb import d4_factor_twist as module
from scripts.theory.aa_bb.a1_certificates import build_a1, load_certificates
from scripts.theory.aa_bb.a2_evidence import build_a2, load_boundary_spec
from scripts.theory.aa_bb.c3_pure_v_ell import build_c3
from scripts.theory.aa_bb.consolidation_inputs import load_a0


@pytest.fixture(scope="module")
def canonical_inputs():
    a0 = load_a0(DATA)
    a1 = build_a1(a0, load_certificates(DATA / "a1-certificates.v1.json"))
    a2 = build_a2(a0, a1, load_boundary_spec(DATA / "a2-boundary-spec.v1.json"))
    return a0, a2, build_c3()


@pytest.fixture(scope="module")
def kernel_payloads():
    pure = module.pure_d0.build_wl587_pure_u7_d0_relative_2_descent()
    mixed = module.mixed_d0.build_wl589_mixed_d0_relative_2_descent()
    return {
        "wl587": pure,
        "wl589": mixed,
        "wl590": module.p5_kernel.build_wl590_from_d0(pure, mixed),
        "wl591": module.p7_kernel.build_wl591_from_mixed_d0(mixed),
        "wl592": module.p17_kernel.build_wl592_from_mixed_d0(mixed),
    }


def _injected_kernels(payloads, calls: list[str]):
    def wrapper(name: str):
        def invoke(*_args):
            calls.append(name)
            return copy.deepcopy(payloads[name])

        return invoke

    return {name: wrapper(name) for name in module.KERNEL_ORDER}


def _semantic_projection_sha256(evidence, work_log: str) -> str:
    projection = module.semantic_projection(module.project_stage(evidence, work_log), work_log)
    canonical_json = json.dumps(
        projection, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return hashlib.sha256(canonical_json).hexdigest()


def test_stage_order_allowlists_and_serialization_are_exact(
    canonical_inputs, kernel_payloads
) -> None:
    a0, a2, c3 = canonical_inputs
    evidence = module.build_d4(a0=a0, a2=a2, c3=c3)

    assert module.D4_STAGES == ("wl586", "wl593")
    assert tuple(evidence.stages) == module.D4_STAGES
    assert set(evidence["wl586"]) == module.WL586_ALLOWLIST | {
        "status",
        "ready",
        "violations",
    }
    assert set(evidence["wl593"]) == module.WL593_ALLOWLIST | {
        "status",
        "ready",
    }
    assert tuple(evidence.kernels) == module.KERNEL_ORDER
    assert set(evidence.kernels) == set(kernel_payloads)

    first = json.dumps(module._serialized(evidence), indent=2, sort_keys=True)
    second = json.dumps(module._serialized(evidence), indent=2, sort_keys=True)
    assert first == second
    serialized = json.loads(first)
    assert serialized["stage_count"] == 2
    assert serialized["status"] == "ok"
    assert serialized["ready"] is True
    assert set(serialized["stages"]) == set(module.D4_STAGES)
    assert "source_cover" not in json.dumps(serialized, sort_keys=True)
    assert set(serialized["stages"]["wl586"]) == module.WL586_ALLOWLIST
    assert serialized["stages"]["wl593"]["verification"] == {
        "checks": evidence["wl593"]["verification"]["checks"]
    }


def test_dependency_aware_adapters_match_zero_argument_builders() -> None:
    pure = module.pure_d0.build_wl587_pure_u7_d0_relative_2_descent()
    mixed = module.mixed_d0.build_wl589_mixed_d0_relative_2_descent()
    assert module.p5_kernel.build_wl590_from_d0(pure, mixed) == (
        module.p5_kernel.build_wl590_p5_factor_twist_local_image_comparison()
    )
    assert module.p7_kernel.build_wl591_from_mixed_d0(mixed) == (
        module.p7_kernel.build_wl591_mixed_p7_factor_twist_local_image()
    )
    assert module.p17_kernel.build_wl592_from_mixed_d0(mixed) == (
        module.p17_kernel.build_wl592_mixed_p17_factor_twist_local_image()
    )


def test_orchestration_calls_each_kernel_once_in_dependency_order(
    canonical_inputs, kernel_payloads
) -> None:
    a0, a2, c3 = canonical_inputs
    calls: list[str] = []
    evidence = module.build_d4(
        a0=a0,
        a2=a2,
        c3=c3,
        kernels=_injected_kernels(kernel_payloads, calls),
    )

    assert calls == list(module.KERNEL_ORDER)
    assert evidence["wl586"]["ready"] is True
    assert evidence["wl593"]["ready"] is True
    assert evidence.dependency_metadata["d0_payloads_rebuilt_by_composition"] is False


def test_wl586_preserves_representatives_witnesses_and_route_boundary(
    canonical_inputs,
) -> None:
    a0, a2, c3 = canonical_inputs
    stage = module.build_d4(a0=a0, a2=a2, c3=c3)["wl586"]

    rows = stage["representative_cover_family_comparison"]
    assert [row["cover_family"] for row in rows] == [
        "support=v_5|L=1|T=5|d=(5,1,5)",
        "support=u_7|L=7|T=9|d=(7,7,1)",
        "support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85)",
    ]
    assert all(row["taxonomy_verified"] for row in rows)
    certificates = stage["cross_family_generic_squareclass_certificates"]
    assert [(row["t_value"], row["N_value"], row["M_value"]) for row in certificates] == [
        ("69/4", "105/8", "-33/8"),
        ("17", "27/2", "-7/2"),
    ]
    assert [row["opposite_product_value"] for row in certificates] == [
        "15172945/4096",
        "226625/16",
    ]
    assert all(
        row["certified"]
        and row["function_field_squareclass"] == "nonsquare"
        and row["value_is_rational_square"] is False
        for row in certificates
    )
    assert stage["route_decision"] == {
        "reenter_wl535_now": False,
        "pure_v_ell_equivalent_model_route": "route_dead",
        "pure_v_ell_parameter_character_route": "route_dead",
        "representative_only_divisor_parity_route": "route_dead_as_uniform_exclusion",
        "wl588_created": False,
        "cross_family_uniform_invariant_proved_here": False,
        "cross_family_generic_invariant_proved_here": True,
        "selected_next_route": "none_without_parameterized_family_level_input",
        "next_route_success_gate": "not_entered",
        "supporting_models_are_not_progress_by_themselves": True,
    }
    assert stage["advance_to_m3"] is False


def test_wl593_preserves_local_images_ledgers_and_global_boundaries(
    canonical_inputs,
) -> None:
    a0, a2, c3 = canonical_inputs
    stage = module.build_d4(a0=a0, a2=a2, c3=c3)["wl593"]

    assert stage["p5_comparison"]["pure_u7_image"] == []
    assert stage["p5_comparison"]["mixed_u3_v5_w17_image"] == ["[5]"]
    assert stage["mixed_instance_chain"] == {
        "p5_survivors": [5, 3045, 66045, 91205],
        "p7_prime": 7,
        "p7_scope": (
            "frozen wl589 mixed cover support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85) at p=7 only"
        ),
        "p7_image": ["[1]"],
        "p7_survivors": [91205],
        "p17_prime": 17,
        "p17_scope": (
            "frozen wl589 mixed cover support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85) at p=17 only"
        ),
        "p17_image": ["[u]"],
        "p17_target": 91205,
        "p17_target_class": "[17u]",
        "p17_target_in_image": False,
        "instance_specific": True,
    }
    assert stage["frozen_boundaries"]["positivity_intervals"] == {
        "pure_u7": "-9<t<9",
        "mixed_u3_v5_w17": "-10<t<10",
    }
    assert stage["frozen_boundaries"]["fixed_cover_equations"] == {
        "pure_u7": "R^2=(N^2+4)*(M^2+4)",
        "mixed_u3_v5_w17": "R^2=(N^2+49)*(M^2+49)",
    }
    assert stage["frozen_boundaries"]["aa_bb_source_products"] == {
        "pure_u7": "(N^2+49)*(M^2+49)=(Z/4)^2",
        "mixed_u3_v5_w17": "(N^2+9)*(M^2+9)=(Z/4)^2",
    }
    assert all(stage["verification"]["checks"].values())
    assert all(value is False for value in stage["proof_boundary"].values())


def test_semantic_projection_matches_frozen_full_parity_digests(canonical_inputs) -> None:
    a0, a2, c3 = canonical_inputs
    evidence = module.build_d4(a0=a0, a2=a2, c3=c3)

    assert _semantic_projection_sha256(evidence, "wl586") == (
        "bc598e278d4d68fdbc3d5b8a5e7bd76d8affbff41dc3db44f4b877100f0d0ae0"
    )
    assert _semantic_projection_sha256(evidence, "wl593") == (
        "4f37688f0e38e3d339dd7771e4486e47b78ac97f858c799cdcef50b2c106da00"
    )


@pytest.mark.parametrize("mutation", ["a0", "a2", "c3"])
def test_canonical_input_mutations_fail_closed(canonical_inputs, mutation: str) -> None:
    a0, a2, c3 = copy.deepcopy(canonical_inputs)
    if mutation == "a0":
        row = next(
            row
            for row in a0.documents["a0-witnesses"]["rows"]
            if row["candidate_id"] == "AA_A7_B2_u_7_m_tail_shell7_candidate"
        )
        row["point_on_E_L"]["Y"] += 1
    elif mutation == "a2":
        row = next(
            row for row in a2.inventory if row["cover_family"] == "support=u_7|L=7|T=9|d=(7,7,1)"
        )
        row["cover_family_model_availability"]["available_data"]["L"] = 999
    else:
        c3.stages["wl585"]["proof_status"]["restricted_combined_elliptic_image_solved_here"] = True

    evidence = module.build_d4(a0=a0, a2=a2, c3=c3)
    assert all(stage["status"] == "issues" for stage in evidence.stages.values())
    assert all(stage["ready"] is False for stage in evidence.stages.values())
    assert all("accepted_outcome" not in stage for stage in evidence.stages.values())


def test_invalid_injected_kernel_and_kernel_shape_fail_closed(
    canonical_inputs, kernel_payloads
) -> None:
    a0, a2, c3 = canonical_inputs
    invalid = copy.deepcopy(kernel_payloads)
    invalid["wl591"]["verification"]["local_checks"]["complete_source_residue_table"] = False
    calls: list[str] = []
    evidence = module.build_d4(
        a0=a0,
        a2=a2,
        c3=c3,
        kernels=_injected_kernels(invalid, calls),
    )
    assert calls == ["wl587", "wl589", "wl590", "wl591"]
    assert all(stage["status"] == "issues" for stage in evidence.stages.values())

    missing = _injected_kernels(kernel_payloads, [])
    del missing["wl592"]
    assert all(
        stage["status"] == "issues"
        for stage in module.build_d4(a0=a0, a2=a2, c3=c3, kernels=missing).stages.values()
    )

    reversed_kernels = OrderedDict(
        (name, _injected_kernels(kernel_payloads, [])[name])
        for name in reversed(module.KERNEL_ORDER)
    )
    assert all(
        stage["status"] == "issues"
        for stage in module.build_d4(a0=a0, a2=a2, c3=c3, kernels=reversed_kernels).stages.values()
    )


def test_project_stage_rejects_unknown_missing_and_mislabeled_stages(
    canonical_inputs,
) -> None:
    a0, a2, c3 = canonical_inputs
    evidence = module.build_d4(a0=a0, a2=a2, c3=c3)
    with pytest.raises(KeyError):
        module.project_stage(evidence, "wl594")
    missing = {"stages": dict(evidence.stages)}
    del missing["stages"]["wl593"]
    with pytest.raises(KeyError):
        module.project_stage(missing, "wl586")
    mislabeled = copy.deepcopy(evidence.stages)
    mislabeled["wl586"]["work_log"] = "wl593"
    with pytest.raises(ValueError):
        module.project_stage(mislabeled, "wl586")
    unknown = copy.deepcopy(evidence["wl586"])
    unknown["unexpected"] = True
    with pytest.raises(ValueError):
        module.semantic_projection(unknown, "wl586")


def test_strict_cli_writes_one_deterministic_two_stage_payload(tmp_path: Path) -> None:
    out = tmp_path / "d4.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.theory.aa_bb.d4_factor_twist",
            "--data-dir",
            str(DATA),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.stdout == "stage_count=2\nstatus=ok\n"
    first = out.read_text(encoding="utf-8")
    payload = json.loads(first)
    assert payload["schema_version"] == 1
    assert tuple(payload["stages"]) == module.D4_STAGES
    assert first == json.dumps(payload, indent=2, sort_keys=True) + "\n"

    bad_out = tmp_path / "bad.json"
    failed = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.theory.aa_bb.d4_factor_twist",
            "--data-dir",
            str(tmp_path / "missing-canonical"),
            "--out",
            str(bad_out),
            "--strict",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert failed.returncode != 0
    assert failed.stdout == "stage_count=2\nstatus=issues\n"
    assert json.loads(bad_out.read_text(encoding="utf-8"))["ready"] is False


def test_runtime_module_has_no_legacy_or_filesystem_fallback_dependency() -> None:
    source = (ROOT / "scripts/theory/aa_bb/d4_factor_twist.py").read_text(encoding="utf-8")
    for forbidden in (
        "results/",
        "audit_closure_",
        "importlib",
        ".glob(",
        ".rglob(",
        "subprocess",
        "wl594",
        "wl595",
    ):
        assert forbidden not in source
    assert "wl587_pure_u7_d0_relative_2_descent" in source
    assert "wl589_mixed_d0_relative_2_descent" in source
    assert "build_wl590_from_d0" in source
    assert "build_wl591_from_mixed_d0" in source
    assert "build_wl592_from_mixed_d0" in source
