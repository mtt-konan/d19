from __future__ import annotations

import importlib
import json
import math
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


def _module():
    try:
        return importlib.import_module(
            "scripts.theory."
            "audit_closure_quotient_rank_zero_aa_bb_wl572_m2_pure_v_ell_exclude_tau_half_by_integrality"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl572_m2_pure_v_ell_exclude_tau_half_by_integrality()


def test_wl572_integral_values_obey_denominator_restriction() -> None:
    for b in range(1, 30):
        for a in range(-60, 61):
            if a == 0 or math.gcd(a, b) != 1:
                continue
            x = Fraction(a * a, b * b)
            ell = x + 5 - 4 / x
            if ell.denominator == 1:
                assert b == 1
                assert a * a in {1, 4}


def test_wl572_surviving_positive_value_is_not_prime() -> None:
    x = Fraction(4)
    ell = x + 5 - 4 / x
    assert ell == 8
    assert 5 - 4 / x == 4
    assert x + 5 == 9


def test_wl572_preserves_claim_boundary() -> None:
    audit = _audit()
    proof = audit["proof_status"]
    assert audit["status"] == "ok"
    assert proof["integral_parameter_forces_q_denominator_one_here"] is True
    assert proof["tau_half_excluded_for_odd_prime_parameter_here"] is True
    assert proof["generic_tau_cover_solved_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl572_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl571_ready", lambda _: False)
    audit = module.build_wl572_m2_pure_v_ell_exclude_tau_half_by_integrality()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl572_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl572.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl572_m2_pure_v_ell_exclude_tau_half_by_integrality.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "tau_half_excluded_for_odd_prime_parameter_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
