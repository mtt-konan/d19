from __future__ import annotations

import importlib
import json
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
            "audit_closure_quotient_rank_zero_aa_bb_wl571_m2_pure_v_ell_source_square_multiquadratic_cover_genus"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl571_m2_pure_v_ell_source_square_multiquadratic_cover_genus()


def test_wl571_product_square_converse_with_X_square() -> None:
    tau = Fraction(2, 3)
    x = Fraction(9, 4)
    delta = tau * tau + 2 * tau - 1
    a = x * (tau + 2) - 2
    b = 2 * tau - x * (2 * tau - 1)
    c = x + 2 * tau + 4
    d = tau * (x + 4) - 2
    u2 = a * b / (2 * x * delta)
    u3 = c * d / (2 * delta)
    product = a * b * c * d
    assert u2 * u3 == product / (4 * x * delta * delta)


def test_wl571_tau_half_simplification() -> None:
    tau = Fraction(1, 2)
    for x in (Fraction(3, 2), Fraction(2), Fraction(9, 4)):
        delta = tau * tau + 2 * tau - 1
        ell = (
            tau * x * x + 2 * x * tau * tau + 8 * x * tau - 2 * x - 4 * tau
        ) / (2 * x * delta)
        p_square = -(
            (x * tau + 2 * x - 2) * (2 * x * tau - x - 2 * tau)
        ) / (2 * x * delta)
        s_square = (
            (x + 2 * tau + 4) * (x * tau + 4 * tau - 2)
        ) / (2 * delta)
        assert ell == x + 5 - 4 / x
        assert p_square == 5 - 4 / x
        assert s_square == x * (x + 5)


def test_wl571_preserves_claim_boundary() -> None:
    audit = _audit()
    proof = audit["proof_status"]
    assert audit["status"] == "ok"
    assert proof["product_quartic_smooth_genus_one_for_all_admissible_tau_here"] is True
    assert proof["full_source_square_cover_genus_five_for_tau_ne_half_here"] is True
    assert proof["tau_half_unique_genus_drop_to_one_here"] is True
    assert proof["exceptional_tau_half_branch_solved_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl571_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl570_ready", lambda _: False)
    audit = module.build_wl571_m2_pure_v_ell_source_square_multiquadratic_cover_genus()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl571_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl571.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl571_m2_pure_v_ell_source_square_multiquadratic_cover_genus.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "tau_half_unique_genus_drop_to_one_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
