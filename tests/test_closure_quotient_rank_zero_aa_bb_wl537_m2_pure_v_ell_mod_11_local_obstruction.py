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
            "audit_closure_quotient_rank_zero_aa_bb_wl537_m2_pure_v_ell_mod_11_local_obstruction"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl537_m2_pure_v_ell_mod_11_local_obstruction()


def test_wl537_eliminates_every_q_square_residue_mod_11() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["work_log"] == "wl537"
    local = audit["local_obstruction"]["mod_11_case_table"]
    assert local["square_residues_mod_11"] == [0, 1, 3, 4, 5, 9]
    assert local["g_ell_mod_11_specialization"] == (
        "G_ell(Q) ≡ Q^4 + 2*Q^3 + 2*Q^2 + 3*Q + 5 (mod 11)"
    )
    assert local["integrality_lemma"]["minus_one_is_nonsquare_mod_11"] is True
    assert local["surviving_q_square_residues_mod_11"] == []
    assert local["obstruction_proved"] is True
    cases = {entry["q_square_mod_11"]: entry for entry in local["q_square_residue_cases"]}
    values = {
        r: (
            entry["ell_minus_q_square_mod_11"],
            entry["ell_q_square_plus_4_mod_11"],
            entry["G_ell_q_square_mod_11"],
        )
        for r, entry in cases.items()
    }
    assert values == {
        0: (10, 4, 5),
        1: (9, 3, 2),
        3: (7, 1, 2),
        4: (6, 0, 4),
        5: (5, 10, 10),
        9: (1, 6, 7),
    }


def test_wl537_records_exact_claim_boundary() -> None:
    audit = _audit()
    assert audit["proof_status"] == {
        "wl535_residue_class_ell_eq_10_mod_11_excluded_here": True,
        "local_prime_11_integrality_obstruction_proved_here": True,
        "equivalent_prime_class_ell_eq_21_mod_44": True,
        "uniform_full_wl535_obstruction_proved_here": False,
        "strict_counterexample_found_here": False,
        "advance_to_m3": False,
    }
    assert audit["local_obstruction"]["removed_prime_class_mod_44"] == 21
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["advance_to_m3"] is False


def test_wl537_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl536_ready", lambda _: False)
    audit = module.build_wl537_m2_pure_v_ell_mod_11_local_obstruction()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}
    assert "wl536_input_not_ready" in audit["violations"]


def test_wl537_cli_writes_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl537.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl537_m2_pure_v_ell_mod_11_local_obstruction.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "work_log=wl537" in result.stdout
    assert "local_prime_11_integrality_obstruction_proved_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
