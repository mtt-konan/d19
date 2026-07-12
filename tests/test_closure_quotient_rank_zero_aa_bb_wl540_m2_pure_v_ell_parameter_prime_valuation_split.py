from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


def _module():
    try:
        return importlib.import_module(
            "scripts.theory."
            "audit_closure_quotient_rank_zero_aa_bb_wl540_m2_pure_v_ell_parameter_prime_valuation_split"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl540_m2_pure_v_ell_parameter_prime_valuation_split()


def test_wl540_symbolic_certificate() -> None:
    audit = _audit()
    symbolic = audit["symbolic_certificate"]
    assert symbolic == {
        "reduction_identity_verified": True,
        "reduced_discriminant": "536870912",
        "reduced_discriminant_equals_2_pow_29": True,
        "gaussian_factorization_verified": True,
        "root_squareclass_identity_verified": True,
        "root_squareclass_identity": "Q*(Q/4+2-i/2)^2=2",
    }


def test_wl540_records_exact_valuation_split() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["work_log"] == "wl540"
    assert audit["valuation_lemma"]["forced_values"] == [
        "v_ell(q)=0",
        "v_ell(a)=0 for a^2=ell-q^2",
        "v_ell(c)=0 for c^2=ell*q^2+4",
        "c is congruent to plus or minus 2 mod ell",
    ]
    assert audit["G_local_split"]["root_branch_only_if_ell_mod_8"] == 1
    assert (
        audit["G_local_split"]["unit_squareclass_after_even_root_distance_still_required"]
        is True
    )


def test_wl540_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["proof_status"] == {
        "q_a_c_are_parameter_prime_units_here": True,
        "G_square_condition_split_by_simple_hensel_roots_here": True,
        "root_reduction_branch_requires_ell_eq_1_mod_8_here": True,
        "ell_eq_5_mod_8_reduced_to_nonzero_unit_branch_here": True,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["advance_to_m3"] is False


def test_wl540_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl539_ready", lambda _: False)
    audit = module.build_wl540_m2_pure_v_ell_parameter_prime_valuation_split()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl540_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl540.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl540_m2_pure_v_ell_parameter_prime_valuation_split.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "root_reduction_branch_requires_ell_eq_1_mod_8_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
