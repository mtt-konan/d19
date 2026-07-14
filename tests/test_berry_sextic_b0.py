from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/theory/berry_sextic_b0.py"
sys.path.insert(0, str(ROOT))


def _module():
    import scripts.theory.berry_sextic_b0 as b0

    return b0


def test_b0_exact_models_maps_and_reduction_audit_preserves_blocker() -> None:
    payload = _module().build_b0_certificate()

    assert payload["status"] == "blocked"
    assert payload["ready"] is False
    assert payload["outcome"] == "precise_b0_actual_reduction_blocker"
    assert payload["verification"]["violations"] == []
    assert payload["verification"]["blockers"] == ["actual_reduction_at_(1+i)_unresolved"]
    assert all(payload["verification"]["checks"].values())

    models = payload["models"]
    assert models["weighted_projective_space"].startswith("P_K(1,3,1)")
    assert "smooth projective model" in models["ordinary_plane_closure"]
    assert models["hyperelliptic_map"] == "pi_d([T:V:S])=[T:S]"
    assert all(payload["twists"][key]["branch_points"] for key in ("d=1", "d=i"))


def test_b0_retains_all_node_and_boundary_fibers() -> None:
    payload = _module().build_b0_certificate()
    fibers = payload["exceptional_fibers"]
    nodes = fibers["nodes"]

    assert len(nodes) == 7
    assert nodes["A++"]["infinity_fiber"] is True
    assert nodes["A+-"]["finite_parameter_gcd"] == "t"
    assert nodes["B++"]["finite_parameter_gcd"] == "t - 1"
    assert nodes["B-+"]["finite_parameter_gcd"] == "t + 1"
    assert "t**4" in nodes["B+-"]["finite_parameter_gcd"]
    assert nodes["C+-1"]["finite_parameter_gcd"] == "t + 1 + sqrt(2)"
    assert nodes["C--1"]["finite_parameter_gcd"] == "t - sqrt(2) + 1"
    assert "ramified" in fibers["branch_and_factor_zero"]["g6"]
    assert "quartic roots" in fibers["coordinate_zero_fibers"]["X"]
    assert "infinity" in fibers["coordinate_zero_fibers"]["T"]


def test_b0_bad_places_and_trivial_ledger_are_distinguished() -> None:
    payload = _module().build_b0_certificate()
    places = payload["bad_places"]
    ledger = payload["trivial_rational_t_ledger"]

    assert places["curve_displayed_integral_model_support"] == ["(1+i)", "(94*i-169)"]
    assert places["curve_actual_reduction_proved_bad"] == {
        "d=1": ["(94*i-169)"],
        "d=i": ["(94*i-169)"],
    }
    assert places["curve_actual_reduction_unresolved"] == {
        "d=1": ["(1+i)"],
        "d=i": ["(1+i)"],
    }
    assert places["curve_actual_reduction_set_complete"] is False
    assert places["factor_resultant_support"] == ["(1+i)"]
    assert set(places["berry_pullback_support"]) == {
        "(1+i)",
        "(94*i-169)",
        "(-94*i-169)",
    }
    assert len(ledger["d=1"]) == 2
    assert ledger["d=i"] == []
    assert "not a claim" in ledger["scope"]
    assert payload["proof_boundary"]["rank_or_selmer_claimed"] is False


def test_b0_actual_reduction_audit_proves_pi_and_separates_varpi() -> None:
    audit = _module().build_b0_certificate()["actual_reduction_audit"]

    assert audit["criterion_at_pi"]["numerator_residue"] == "15271"
    assert audit["criterion_at_pi"]["valuation"] == "v_pi(j1)=-1"
    assert audit["criterion_at_pi"]["conclusion"].startswith("actual bad")
    assert audit["twist_invariance"]["pi_conclusion"].startswith("both twists")
    assert "unresolved" in audit["twist_invariance"]["varpi_conclusion"]
    assert audit["twist_invariance"]["twist_changes_varpi_answer"] is None
    assert audit["at_varpi"]["displayed_model_status"] == "singular"
    assert audit["at_varpi"]["criterion_status"] == "fixed-center radial audit only; not complete"
    assert audit["at_varpi"]["d=1"] == "unresolved actual reduction"
    assert audit["at_varpi"]["d=i"] == "unresolved actual reduction"
    assert audit["at_varpi"]["normal_form"]["coefficient_valuations_low_to_high"] == [
        11,
        10,
        8,
        9,
        3,
        2,
        0,
    ]
    assert "Bruhat-Tits-tree directions" in audit["blocker"]
    assert audit["resolved"] is False


def test_b0_strict_cli_materializes_certificate(tmp_path: Path) -> None:
    out = tmp_path / "berry-sextic-b0.json"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--out", str(out), "--strict"],
        check=False,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    assert result.returncode == 1
    assert result.stdout.splitlines() == [
        "status=blocked",
        "task=berry-sextic-genus2-b0",
        "ready=False",
        "outcome=precise_b0_actual_reduction_blocker",
        "violations=[]",
        "blockers=['actual_reduction_at_(1+i)_unresolved']",
    ]
    saved = json.loads(out.read_text(encoding="utf-8"))
    assert saved["models"]["genus_argument"].startswith("g6 is squarefree")
    assert saved["actual_reduction_audit"]["resolved"] is False
