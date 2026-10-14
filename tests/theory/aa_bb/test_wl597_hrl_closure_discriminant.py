from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[3]
SCRIPT = ROOT / "scripts/theory/aa_bb/wl597_hrl_closure_discriminant.py"
sys.path.insert(0, str(ROOT))


def _module():
    assert SCRIPT.is_file()
    return importlib.import_module(
        "scripts.theory.aa_bb.wl597_hrl_closure_discriminant"
    )


def test_symmetric_quadratic_and_discriminant_factorization() -> None:
    payload = _module().build_certificate()

    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["accepted_outcome"] == "precise_smaller_arithmetic_proposition"
    assert payload["verification"]["violations"] == []
    assert all(payload["verification"]["checks"].values())
    assert "F0(z)*FT(z)" in payload["discriminant"]["necessary_square"]


def test_gate_retains_source_and_root_conditions() -> None:
    payload = _module().build_certificate()
    retained = payload["retained_conditions"]

    assert any("source values" in item for item in retained)
    assert any("E^2-4*z^2" in item for item in retained)
    assert any("sign inequality" in item for item in retained)
    assert payload["proof_boundary"]["uniform_exclusion"] is False


def test_dyadic_branch_reduction_is_scoped() -> None:
    payload = _module().build_certificate()
    reduction = payload["dyadic_branch_reduction"]

    assert "all six" in reduction["opposite_parity"]["closure"]
    assert reduction["both_odd"]["surviving_branch"] == "the physical T branch with 4 dividing T"
    assert "odd squareclass" in reduction["scope"]


def test_strict_cli() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--strict"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    assert result.stdout.splitlines() == [
        "status=ok",
        "task=universal-four-factor-hrl-closure-discriminant",
        "ready=True",
        "accepted_outcome=precise_smaller_arithmetic_proposition",
        "violations=[]",
    ]
