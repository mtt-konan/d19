from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[3]
SCRIPT = ROOT / "scripts/theory/aa_bb/wl594_universal_closure_product_g0.py"
sys.path.insert(0, str(ROOT))


def _module():
    assert SCRIPT.is_file()
    return importlib.import_module("scripts.theory.aa_bb.wl594_universal_closure_product_g0")


def test_wl594_certifies_the_parameterized_g0_input_without_claiming_an_obstruction() -> None:
    payload = _module().build_wl594_universal_closure_product_g0()

    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["work_log"] == "wl594"
    assert payload["accepted_outcome"] == "exact_parameterized_input_ready"
    assert payload["verification"]["violations"] == []
    assert all(payload["verification"]["checks"].values())
    assert payload["proof_boundary"]["parameterized_geometric_input_supplied"] is True
    assert payload["proof_boundary"]["Kummer_obstruction_proved"] is False
    assert payload["proof_boundary"]["split_prime_obstruction_proved"] is False
    assert payload["proof_boundary"]["long_term_object_complete"] is False
    assert "restricted nonmidpoint image" in payload["missing_result"]

    checks = payload["verification"]["checks"]
    exact_identity_names = (
        "centered_sum_identity",
        "centered_difference_identity",
        "signed_difference_T_identity",
        "signed_difference_t_identity",
        "signed_difference_N_identity",
        "signed_difference_M_identity",
        "swapped_difference_T_identity",
        "swapped_difference_t_identity",
        "swapped_difference_N_identity",
        "swapped_difference_M_identity",
        "scale_W_via_product_equation",
    )
    assert all(checks[name] is True for name in exact_identity_names)
    assert "product_cover_local_obstruction_not_claimed" not in checks
    assert "uniform_Kummer_obstruction_not_proved" not in checks


def test_wl594_records_exact_geometry_lifts_and_gen_closure_boundaries() -> None:
    payload = _module().build_wl594_universal_closure_product_g0()
    details = payload["details"]

    assert details["general_Q_L"].startswith("Q_L(t)=")
    assert details["explicit_formulas"]["T=A+B"]["Q_A"]
    assert details["explicit_formulas"]["T=abs(A-B), A>B>0"]["Q_B"]
    assert details["genus_and_quotient"]["product_cover"].startswith("genus 3")
    assert details["genus_and_quotient"]["simultaneous_cover"].startswith("z_A")
    assert details["forward_and_converse"]["level_b"].startswith("x is")
    assert details["forward_and_converse"]["level_c"].startswith("Q_A")
    assert details["forward_and_converse"]["level_d"].startswith("the four")

    branches = details["gen_closure_quantifiers"]
    assert "For every exact AA+BB candidate" in branches["universal_statement"]
    assert "N1+N2=A+B" in branches["four_relations"]
    assert "abs(N1-N2)=abs(A-B)" in branches["four_relations"]
    assert "N1+N2=c" in branches["sum_branches"]
    assert "t=N1+N2>T" in branches["difference_orientation"]
    assert "N2-N1=c" in branches["difference_swapped_orientation"]
    assert "x=0" in branches["cubic_denominator"]
    assert "(k^4*W)^2" in details["scale_and_parameter"]["scale_product_equation"]
    assert details["novelty_boundary"]["whole_cover_local_solubility"].startswith(
        "automatic"
    )
    assert "No Kummer" in details["novelty_boundary"]["not_proved"]


def test_wl594_strict_cli_output(tmp_path: Path) -> None:
    out = tmp_path / "wl594.json"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    assert result.stdout.splitlines() == [
        "status=ok",
        "work_log=wl594",
        "ready=True",
        "accepted_outcome=exact_parameterized_input_ready",
        "obstruction_proved=False",
        "missing_result=uniform_restricted_image_Kummer_or_split_prime_theorem",
        "violations=[]",
    ]
    saved = json.loads(out.read_text(encoding="utf-8"))
    assert saved["work_log"] == "wl594"
    assert saved["missing_result"].startswith("No uniform Kummer")
