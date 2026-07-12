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
            "audit_closure_quotient_rank_zero_aa_bb_wl543_m2_pure_v_ell_real_quadratic_square_ideal_descent"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl543_m2_pure_v_ell_real_quadratic_square_ideal_descent()


def test_wl543_records_square_ideal_descent() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["descent"] == {
        "field": "Q(sqrt(ell))",
        "ring_of_integers": "Z[(1+sqrt(ell))/2]",
        "alpha": "(C+Q*sqrt(ell))/2",
        "norm_alpha": "D^2",
        "alpha_is_totally_positive": True,
        "alpha_and_conjugate_ideals_are_coprime": True,
        "square_ideal_equation": "(alpha)=a^2",
        "ordinary_class_group_2_torsion": "trivial by genus theory",
        "element_equation": "alpha=epsilon*beta^2",
    }


def test_wl543_unit_squareclass_split_is_at_most_binary() -> None:
    split = _audit()["unit_squareclass_split"]
    assert split["norm_minus_one_unit_exists"] == {
        "class_count": 1,
        "epsilon_is_square": True,
    }
    assert split["no_norm_minus_one_unit"] == {
        "class_count": 2,
        "epsilon_classes": ["1", "fundamental totally positive unit"],
    }
    assert split["negative_pell_equivalence"] == "x^2-ell*y^2=-4 is soluble"


def test_wl543_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["proof_status"] == {
        "real_quadratic_alpha_is_totally_positive_integral_here": True,
        "principal_ideal_of_alpha_is_square_ideal_here": True,
        "ordinary_class_group_2_torsion_eliminated_by_genus_theory_here": True,
        "alpha_reduced_to_unit_times_element_square_here": True,
        "remaining_totally_positive_unit_squareclasses_at_most_two": True,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    assert audit["rational_wl535_point_produced_here"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False


def test_wl543_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl542_ready", lambda _: False)
    audit = module.build_wl543_m2_pure_v_ell_real_quadratic_square_ideal_descent()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl543_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl543.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl543_m2_pure_v_ell_real_quadratic_square_ideal_descent.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "alpha_reduced_to_unit_times_element_square_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
