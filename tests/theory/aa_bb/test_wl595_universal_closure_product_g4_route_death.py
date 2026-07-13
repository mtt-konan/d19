from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[3]
SCRIPT = ROOT / "scripts/theory/aa_bb/wl595_universal_closure_product_g4_route_death.py"
sys.path.insert(0, str(ROOT))


def _module():
    assert SCRIPT.is_file()
    return importlib.import_module(
        "scripts.theory.aa_bb.wl595_universal_closure_product_g4_route_death"
    )


def test_wl595_accepts_the_scoped_route_death_certificate() -> None:
    payload = _module().build_wl595_universal_closure_product_g4_route_death()

    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["work_log"] == "wl595"
    assert payload["accepted_outcome"] == "route_death_certificate"
    assert payload["verification"]["violations"] == []
    assert all(payload["verification"]["checks"].values())
    assert payload["proof_boundary"] == {
        "scoped_objective_complete": True,
        "long_term_object_complete": True,
        "long_term_object_scope": (
            "the universal closure-product Kummer/split-prime objective only"
        ),
        "global_problem_complete": False,
        "all_future_relative_2_descent_impossible": False,
        "Harborth": False,
        "family_exclusion": False,
        "Selmer": False,
        "rank": False,
        "D2": False,
        "D5": False,
        "M3": False,
        "global_point": False,
        "new_parameterized_global_certificate_supplied": False,
    }


def test_wl595_retains_g0_and_exact_g1_algebra() -> None:
    payload = _module().build_wl595_universal_closure_product_g4_route_death()

    g0 = payload["G0"]
    assert g0["accepted_outcome"] == "exact_parameterized_input_ready"
    assert all(g0["checks"].values())
    assert g0["details"]["genus_and_quotient"]["product_cover"].startswith(
        "genus 3"
    )
    assert g0["details"]["genus_and_quotient"]["simultaneous_cover"].startswith(
        "z_A^2=Q_A, z_B^2=Q_B has genus 5"
    )

    g1 = payload["G1"]
    assert all(g1["checks"].values())
    assert g1["identities"]["f_A_minus_f_B"] == (
        "8*Delta*(x+T^2+2*S)"
    )
    assert g1["identities"]["general_resultant"].startswith("256")
    assert g1["identities"]["plus_resultant"] == (
        "2^10*Delta^2*S*(A+B)^2"
    )
    assert g1["identities"]["minus_resultant"] == (
        "2^10*Delta^2*S*(A-B)^2"
    )
    assert g1["identities"]["closure_branch_f_A_x0"] == "16*S*T^2"
    assert g1["natural_class"]["conclusion"] == (
        "[f_A]=[f_B]=1, hence delta=1"
    )


def test_wl595_checks_g2_collision_and_negative_valuation_branches() -> None:
    payload = _module().build_wl595_universal_closure_product_g4_route_death()
    g2 = payload["G2"]

    assert all(g2["checks"].values())
    assert len(g2["differences"]) == 6
    assert len(g2["pairwise_resultants"]) == 6
    assert g2["cross_collision"]["closure_branch_common_value"] == "4*S"
    assert "t^-2*Phi_(L,+/-)" in g2["negative_valuation"]["identity"]
    assert g2["checks"]["p5_integral_branch_excluded"] is True
    assert g2["checks"]["p5_negative_branch_survives"] is True
    assert g2["checks"]["global_point_not_claimed"] is True


def test_wl595_checks_primitive_denominators_and_g4_scope() -> None:
    payload = _module().build_wl595_universal_closure_product_g4_route_death()
    g3 = payload["G3"]
    g4 = payload["G4"]

    assert all(g3["checks"].values())
    assert g3["primitive_coordinate"]["parameterization"] == (
        "t=C/den with gcd(C,den)=1"
    )
    assert "gcd(F_i,F_j) divides Res_t(Phi_i,Phi_j)" in g3[
        "pairwise_gcd_bounds"
    ]["statement"]
    assert "1+q*Z_q" in g3["denominator_local_proof"]["odd_q"]
    assert "1+8*Z_2" in g3["denominator_local_proof"]["q=2"]
    assert all(g4["checks"].values())
    assert g4["accepted_outcome"] == (
        "precise_g4_universal_closure_product_route_death"
    )
    assert "full individual four-factor cover" in g4["reopening_input"]
    assert "both T branches" in g4["reopening_input"]


def test_wl595_strict_cli_output(tmp_path: Path) -> None:
    out = tmp_path / "wl595.json"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    assert result.stdout.splitlines() == [
        "status=ok",
        "work_log=wl595",
        "ready=True",
        "accepted_outcome=route_death_certificate",
        "scoped_objective_complete=True",
        "long_term_object_complete=True",
        "global_problem_complete=False",
        "violations=[]",
    ]
    saved = json.loads(out.read_text(encoding="utf-8"))
    assert saved["work_log"] == "wl595"
    assert saved["proof_boundary"]["family_exclusion"] is False
