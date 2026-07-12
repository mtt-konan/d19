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
            "audit_closure_quotient_rank_zero_aa_bb_wl545_m2_pure_v_ell_trivial_unit_2_adic_dichotomy"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl545_m2_pure_v_ell_trivial_unit_2_adic_dichotomy()


def test_wl545_residue_certificate() -> None:
    residue = _audit()["residue_certificate"]
    assert residue["unit_square_residues_mod_8"] == [1]
    assert residue["k_eq_1_parenthesized_residues"] == {1: 2, 5: 6}
    assert residue["k_eq_1_total_valuation_is_3"] is True
    assert residue["k_eq_2_unit_residue_mod_8"] == 5
    assert residue["k_eq_2_unit_is_nonsquare"] is True
    assert residue["G_unit_branch_residue_mod_8"] == 1


def test_wl545_records_exact_dichotomy() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["q_valuation_dichotomy"] == {
        "ell_eq_5_mod_8": "v_2(q)=0",
        "ell_eq_1_mod_8": "v_2(q)>=3",
        "excluded_valuations": [1, 2],
    }
    assert audit["descent_variable_parity"] == {
        "ell_eq_5_mod_8": "u and v are both odd",
        "ell_eq_1_mod_8": "u=2m and v=2n with m,n of opposite parity",
        "primitive_normalization": "v_2(N)=2",
    }


def test_wl545_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["proof_status"] == {
        "trivial_unit_2_adic_q_valuation_classified_here": True,
        "ell_eq_5_mod_8_forces_u_v_odd_here": True,
        "ell_eq_1_mod_8_forces_even_halves_opposite_parity_here": True,
        "G_condition_adds_no_2_adic_obstruction_here": True,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    assert audit["rational_wl535_point_produced_here"] is False


def test_wl545_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl544_ready", lambda _: False)
    audit = module.build_wl545_m2_pure_v_ell_trivial_unit_2_adic_dichotomy()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl545_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl545.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl545_m2_pure_v_ell_trivial_unit_2_adic_dichotomy.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "G_condition_adds_no_2_adic_obstruction_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
