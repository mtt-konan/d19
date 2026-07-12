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
            "audit_closure_quotient_rank_zero_aa_bb_wl547_m2_pure_v_ell_finite_gaussian_s_squareclass_descent"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl547_m2_pure_v_ell_finite_gaussian_s_squareclass_descent()


def test_wl547_symbolic_support_certificate() -> None:
    symbolic = _audit()["symbolic_certificate"]
    assert symbolic["P_plus_R_identity_verified"] is True
    assert symbolic["ell_eq_1_root_polynomial_verified"] is True
    assert symbolic["root_polynomial"] == "t^2+4*t-4"
    assert symbolic["root_discriminant"] == 32


def test_wl547_records_finite_support() -> None:
    support = _audit()["finite_support"]
    assert support == {
        "dyadic_prime": "1+i",
        "odd_rational_primes": "p|ell-1 with Legendre(2/p)=1",
        "candidate_root_condition": "(Q^2/D^2)^2+4*(Q^2/D^2)-4=0 mod p",
        "outside_support_Gaussian_valuations_are_even": True,
    }


def test_wl547_preserves_object_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"] == {
        "G_square_rewritten_as_Gaussian_norm_square_here": True,
        "common_odd_prime_support_bounded_by_ell_minus_1_here": True,
        "common_odd_primes_require_Legendre_2_eq_1_here": True,
        "G_square_reduced_to_finite_S_squareclasses_here": True,
        "theorem_level_Selmer_object_claimed_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    assert audit["squareclass_equation"]["d_supported_on_finite_S_ell"] is True
    assert audit["complete_selmer_upper_bound_proved"] is False


def test_wl547_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl546_ready", lambda _: False)
    audit = module.build_wl547_m2_pure_v_ell_finite_gaussian_s_squareclass_descent()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl547_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl547.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl547_m2_pure_v_ell_finite_gaussian_s_squareclass_descent.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "G_square_reduced_to_finite_S_squareclasses_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
