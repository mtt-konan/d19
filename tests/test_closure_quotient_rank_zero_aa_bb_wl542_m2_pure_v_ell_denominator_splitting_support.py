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
            "audit_closure_quotient_rank_zero_aa_bb_wl542_m2_pure_v_ell_denominator_splitting_support"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl542_m2_pure_v_ell_denominator_splitting_support()


def test_wl542_symbolic_local_factorizations() -> None:
    audit = _audit()
    symbolic = audit["local_converse"]["symbolic_factorization"]
    assert symbolic == {
        "G_leading_term_factorization_verified": True,
        "first_square_factorization_verified": True,
        "second_square_factorization_verified": True,
        "smallest_principal_unit_valuation_for_v_r_q_minus_k": "2*k",
    }


def test_wl542_records_exact_denominator_support() -> None:
    audit = _audit()
    support = audit["denominator_support"]
    assert support == {
        "primitive_equations": [
            "A^2+Q^2=ell*D^2",
            "C^2=ell*Q^2+4*D^2",
        ],
        "D_is_odd": True,
        "gcd_D_ell": 1,
        "prime_conditions": [
            "r is congruent to 1 mod 4",
            "Legendre(ell/r)=1",
            "Legendre(r/ell)=1",
        ],
        "splitting_field": "Q(i,sqrt(ell))",
        "D_mod_ell_is_nonzero_square": True,
    }


def test_wl542_preserves_exact_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"] == {
        "global_denominator_is_odd_and_coprime_to_ell_here": True,
        "every_denominator_prime_splits_completely_here": True,
        "D_mod_ell_is_nonzero_square_here": True,
        "allowed_denominator_places_add_no_G_local_obstruction_here": True,
        "rational_wl535_point_produced_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    assert audit["local_converse"]["all_three_square_conditions_locally_compatible"] is True
    assert audit["complete_selmer_upper_bound_proved"] is False


def test_wl542_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl541_ready", lambda _: False)
    audit = module.build_wl542_m2_pure_v_ell_denominator_splitting_support()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl542_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl542.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl542_m2_pure_v_ell_denominator_splitting_support.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "every_denominator_prime_splits_completely_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
