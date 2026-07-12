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
            "audit_closure_quotient_rank_zero_aa_bb_wl548_m2_pure_v_ell_dyadic_gaussian_squareclass_elimination"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl548_m2_pure_v_ell_dyadic_gaussian_squareclass_elimination()


def _v_one_plus_i(real: int, imag: int) -> int:
    valuation = 0
    while (real - imag) % 2 == 0:
        real, imag = (real + imag) // 2, (imag - real) // 2
        valuation += 1
    return valuation


def test_wl548_exact_dyadic_valuations() -> None:
    valuation = _audit()["valuation_certificate"]
    assert valuation["ell_eq_5_mod_8"]["v_1_plus_i_delta"] == 0
    assert valuation["ell_eq_1_mod_8"]["v_1_plus_i_delta"] == 4
    assert valuation["ell_eq_1_mod_8"]["P_over_4_and_R_over_4_are_odd"] is True
    assert valuation["both_delta_valuations_are_even"] is True


def test_wl548_unit_branch_congruences_force_exact_valuation() -> None:
    for ell in range(5, 64, 8):
        for q in range(1, 16, 2):
            for d in range(1, 16, 2):
                p = -(q**4) + (8 * ell - 12) * q**2 * d**2 + 4 * d**4
                r = q**4 + 4 * q**2 * d**2 - 4 * d**4
                assert (p % 8, r % 8) == (7, 1)
                assert _v_one_plus_i(p, r) == 1


def test_wl548_high_valuation_branch_congruences_force_exact_valuation() -> None:
    for ell in range(1, 64, 8):
        for q in range(8, 33, 8):
            for d in range(1, 16, 2):
                p = -(q**4) + (8 * ell - 12) * q**2 * d**2 + 4 * d**4
                r = q**4 + 4 * q**2 * d**2 - 4 * d**4
                assert ((p // 4) % 4, (r // 4) % 4) == (1, 3)
                assert _v_one_plus_i(p, r) == 5


def test_wl548_refines_support_to_odd_primes() -> None:
    support = _audit()["refined_support"]
    assert support == {
        "contains_one_plus_i": False,
        "odd_rational_primes": "p|ell-1 with Legendre(2/p)=1",
        "candidate_root_condition": "(Q^2/D^2)^2+4*(Q^2/D^2)-4=0 mod p",
    }


def test_wl548_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"] == {
        "dyadic_delta_valuation_computed_exactly_here": True,
        "one_plus_i_squareclass_eliminated_here": True,
        "finite_support_reduced_to_odd_primes_here": True,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    assert audit["rational_wl535_point_produced_here"] is False


def test_wl548_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl547_ready", lambda _: False)
    audit = module.build_wl548_m2_pure_v_ell_dyadic_gaussian_squareclass_elimination()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl548_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl548.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl548_m2_pure_v_ell_dyadic_gaussian_squareclass_elimination.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "one_plus_i_squareclass_eliminated_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
