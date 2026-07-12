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
            "audit_closure_quotient_rank_zero_aa_bb_wl579_m2_pure_v_ell_common_allocation_mobius_magnitude_curve"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl579_m2_pure_v_ell_common_allocation_mobius_magnitude_curve()


def test_wl579_Mobius_map_is_strictly_above_input() -> None:
    for p, k_form in ((5, 1), (13, 2), (29, 3)):
        for z in (Fraction(1, 10), Fraction(1, 4), Fraction(1, 2)):
            if 2 * k_form * z >= p:
                continue
            w = (2 * k_form + p * z) / (p - 2 * k_form * z)
            assert w > z
            assert w - z == 2 * k_form * (1 + z * z) / (p - 2 * k_form * z)


def test_wl579_projective_ratio_reconstruction() -> None:
    p = Fraction(13)
    k_form = Fraction(2)
    z = Fraction(1, 3)
    r1 = Fraction(5)
    first = Fraction(15)
    second = z * first
    third = (p - 2 * k_form * z) * first / r1
    fourth = (2 * k_form + p * z) * first / r1
    assert r1 * third == p * first - 2 * k_form * second
    assert r1 * fourth == 2 * k_form * first + p * second
    assert fourth / third == (2 * k_form + p * z) / (p - 2 * k_form * z)


def test_wl579_preserves_claim_boundary() -> None:
    audit = _audit()
    proof = audit["proof_status"]
    assert audit["status"] == "ok"
    assert proof["biquadratic_genus_one_curve_proved_here"] is True
    assert proof["strict_normalized_magnitude_ordering_proved_here"] is True
    assert proof["primitive_linear_form_reconstruction_proved_here"] is False
    assert proof["generic_genus_five_cover_solved_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl579_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl578_ready", lambda _: False)
    audit = module.build_wl579_m2_pure_v_ell_common_allocation_mobius_magnitude_curve()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl579_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl579.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl579_m2_pure_v_ell_common_allocation_mobius_magnitude_curve.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "biquadratic_genus_one_curve_proved_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
