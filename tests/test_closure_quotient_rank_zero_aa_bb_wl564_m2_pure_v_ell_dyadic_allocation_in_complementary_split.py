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
            "audit_closure_quotient_rank_zero_aa_bb_wl564_m2_pure_v_ell_dyadic_allocation_in_complementary_split"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl564_m2_pure_v_ell_dyadic_allocation_in_complementary_split()


def test_wl564_mod8_coordinate_side_from_f_over_r() -> None:
    for r_mod_8 in (1, 7):
        inverse = pow(r_mod_8, -1, 8)
        # ell=5 mod 8: F=1 and g is odd.
        difference = inverse % 8
        assert difference == (1 if r_mod_8 == 1 else 7)
        # ell=1 mod 8 after dividing by 4: F/4=7 and g/2 is odd.
        normalized_difference = 7 * inverse % 8
        assert normalized_difference == (7 if r_mod_8 == 1 else 1)


def test_wl564_kappa_parity_matches_v2_ell_minus_one() -> None:
    # r is odd, so only 1+v2(ell-1) controls whether 2 enters kappa.
    for valuation in range(2, 12):
        kappa_is_even = (valuation + 1) % 2 == 1
        assert kappa_is_even == (valuation % 2 == 0)
    assert (2 + 1) % 2 == 1  # ell=5 mod 8 always has 2|kappa.


def test_wl564_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["binary_choice_at_2_removed_when_present_here"] is True
    assert audit["proof_status"]["odd_complementary_divisor_allocation_solved_here"] is False
    assert audit["rational_wl535_point_produced_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl564_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl563_ready", lambda _: False)
    audit = module.build_wl564_m2_pure_v_ell_dyadic_allocation_in_complementary_split()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl564_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl564.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl564_m2_pure_v_ell_dyadic_allocation_in_complementary_split.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "binary_choice_at_2_removed_when_present_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
