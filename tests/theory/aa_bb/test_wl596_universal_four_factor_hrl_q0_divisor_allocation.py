from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[3]
SCRIPT = ROOT / "scripts/theory/aa_bb/wl596_universal_four_factor_hrl_q0_divisor_allocation.py"
sys.path.insert(0, str(ROOT))


def _module():
    assert SCRIPT.is_file()
    return importlib.import_module(
        "scripts.theory.aa_bb.wl596_universal_four_factor_hrl_q0_divisor_allocation"
    )


def test_source_converse_and_balanced_parity_certificate() -> None:
    payload = _module().build_hrl_q0_divisor_allocation()

    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["accepted_outcome"] == "precise_smaller_arithmetic_blocker"
    assert payload["verification"]["violations"] == []
    assert all(payload["verification"]["checks"].values())
    balanced = payload["balanced_parity_certificate"]
    assert balanced["odd_failures"] == []
    assert balanced["dyadic_failures"] == []


def test_corrected_dyadic_and_unbalanced_boundaries() -> None:
    payload = _module().build_hrl_q0_divisor_allocation()
    parity = payload["parity_consequences"]

    assert set(parity["dyadic_middle"]["residues"].values()) == {3, 7}
    assert parity["dyadic_middle"]["middle_branch_has_no_Q2_source_point"] is True
    assert "Odd-p valuation data does not determine" in parity["odd_beta_not_gamma"]
    witness = parity["odd_unbalanced_local_witness"]
    assert witness["v7_rho_squared"] == 2
    assert witness["source_square_at_z"] == "1/4"
    assert witness["source_square_at_rho_over_z"] == "1/4"
    assert witness["allocation_parities"] == [0, 1]
    assert witness["scope"].startswith("Q_7 local")
    assert "exact dyadic unit" in parity["dyadic_unbalanced"]
    assert parity["midpoint"].startswith("q1=q2")


def test_reduced_proposition_retains_the_exact_converse_and_boundaries() -> None:
    payload = _module().build_hrl_q0_divisor_allocation()
    reduced = payload["reduced_exact_proposition"]

    assert reduced["positive_source_image"].startswith("q_i>=s")
    assert "nonnegative integer square" in reduced["source_square"]
    assert set(reduced["closure_union"]) == {
        "U1+U2=s",
        "U1+U2=r",
        "U1-U2=s",
        "U2-U1=s",
        "U1-U2=r",
        "U2-U1=r",
    }
    assert "primitive common scale" in reduced["converse"]
    assert "midpoint" in payload["boundary_audit"]["finite"]
    assert "infinity" in payload["boundary_audit"]["projective"]
    assert len(payload["removed_freedoms"]) == 5
    assert payload["proof_boundary"]["finite_parameter_uniform_support_proved"] is False


def test_strict_cli_materializes_q0_certificate(tmp_path: Path) -> None:
    out = tmp_path / "hrl-q0-divisor-allocation.json"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    assert result.stdout.splitlines() == [
        "status=ok",
        "task=universal-four-factor-hrl-q0-divisor-allocation",
        "ready=True",
        "accepted_outcome=precise_smaller_arithmetic_blocker",
        "violations=[]",
    ]
    saved = json.loads(out.read_text(encoding="utf-8"))
    assert saved["accepted_outcome"] == "precise_smaller_arithmetic_blocker"
    assert "global invariant" in saved["missing_input"]
