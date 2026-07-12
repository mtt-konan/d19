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
            "audit_closure_quotient_rank_zero_aa_bb_wl538_m2_pure_v_ell_mod_19_local_obstruction"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl538_m2_pure_v_ell_mod_19_local_obstruction()


def test_wl538_eliminates_all_mod_19_square_residues() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["work_log"] == "wl538"
    local = audit["local_obstruction"]["mod_19_case_table"]
    assert local["square_residues_mod_19"] == [0, 1, 4, 5, 6, 7, 9, 11, 16, 17]
    assert local["surviving_q_square_residues_mod_19"] == []
    assert local["obstruction_proved"] is True
    values = {
        case["q_square_mod_19"]: (
            case["ell_minus_q_square_mod_19"],
            case["ell_q_square_plus_4_mod_19"],
            case["G_ell_q_square_mod_19"],
        )
        for case in local["q_square_residue_cases"]
    }
    assert values == {
        0: (15, 4, 16), 1: (14, 0, 5), 4: (11, 7, 14),
        5: (10, 3, 13), 6: (9, 18, 4), 7: (8, 14, 8),
        9: (6, 6, 12), 11: (4, 17, 8), 16: (18, 16, 14), 17: (17, 12, 9),
    }


def test_wl538_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["proof_status"] == {
        "wl535_residue_class_ell_eq_15_mod_19_excluded_here": True,
        "local_prime_19_integrality_obstruction_proved_here": True,
        "equivalent_prime_class_ell_eq_53_mod_76": True,
        "uniform_full_wl535_obstruction_proved_here": False,
        "strict_counterexample_found_here": False,
        "advance_to_m3": False,
    }
    assert audit["local_obstruction"]["removed_prime_class_mod_76"] == 53
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["advance_to_m3"] is False


def test_wl538_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl537_ready", lambda _: False)
    audit = module.build_wl538_m2_pure_v_ell_mod_19_local_obstruction()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl538_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl538.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl538_m2_pure_v_ell_mod_19_local_obstruction.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "local_prime_19_integrality_obstruction_proved_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
