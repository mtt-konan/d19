from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[3]
SCRIPT = ROOT / "scripts/theory/aa_bb/hrl_exact_evaluation_support.py"
sys.path.insert(0, str(ROOT))


def _module():
    assert SCRIPT.is_file()
    return importlib.import_module("scripts.theory.aa_bb.hrl_exact_evaluation_support")


def test_exact_evaluation_covers_all_radical_sign_patterns() -> None:
    payload = _module().build_hrl_exact_evaluation_support()
    evaluation = payload["certificate"]["evaluation"]

    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["base_commit"] == "8f5a255"
    assert payload["accepted_outcome"] == "precise_evaluation_support_blocker"
    assert len(evaluation["evaluation_cases"]) == 4
    assert len(payload["verification"]["checks"]) >= 20
    assert payload["verification"]["violations"] == []
    assert all(payload["verification"]["checks"].values())
    assert evaluation["squareclass_formula"] == (
        "[H_RL(P)]=[epsilon1*epsilon2*q1*q2*Delta^e], where e=1 iff sigma1 != sigma2"
    )


def test_source_support_reduces_to_delta_divisor_allocation() -> None:
    payload = _module().build_hrl_exact_evaluation_support()
    certificate = payload["certificate"]

    assert certificate["primitive_coordinates"]["q"] == ("q_i=abar_i+bbar_i divides Delta_bar")
    valuation = certificate["valuation_audit"]
    assert "v_p(q1)+v_p(q2)" in valuation["all_primes"]
    assert valuation["odd_p_not_dividing_delta"] == "v_p(H_RL)=0 mod 2"
    assert "If Delta_bar is odd" in valuation["p=2"]
    assert "scale contributes -2*v_p(scale)" in valuation["denominators"]
    assert "closure-compatible divisor-allocation" in payload["missing_input"]
    assert payload["realized_support"]["finite_per_specialization_group"] == (
        "G_Delta=<[-1],[p] for primes p dividing Delta_bar>"
    )
    assert payload["proof_boundary"]["formal_twists_used"] is False
    assert payload["proof_boundary"]["local_prime_tables_run"] is False
    assert all(payload["retained_constraints"].values())


def test_source_quartic_and_branch_boundaries_are_retained() -> None:
    payload = _module().build_hrl_exact_evaluation_support()
    source = payload["certificate"]["source"]
    branches = payload["closure_branches"]
    boundaries = payload["boundary_audit"]

    assert set(source["quartic_reductions"]) == {"source_quartic_1", "source_quartic_2"}
    assert branches["sum_targets"] == ["T=A+B", "T=abs(A-B)"]
    assert "|t|<T" in branches["sum_coordinates"]
    assert "|t|>T" in branches["difference_coordinates"]
    assert branches["positive_square"] == "x=t^2 is positive and nonzero off the midpoint"
    assert boundaries["factor_zero"].startswith("r_i=0 is impossible")
    assert boundaries["infinity"].startswith("not an affine")
    assert "collisions" in boundaries


def test_strict_cli_materializes_the_evaluation_certificate(tmp_path: Path) -> None:
    out = tmp_path / "hrl-exact-evaluation.json"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    assert result.stdout.splitlines() == [
        "status=ok",
        "task=universal-four-factor-hrl-exact-evaluation-support-audit",
        "ready=True",
        "accepted_outcome=precise_evaluation_support_blocker",
        "evaluation_cases=4",
        "violations=[]",
    ]
    saved = json.loads(out.read_text(encoding="utf-8"))
    assert saved["accepted_outcome"] == "precise_evaluation_support_blocker"
    assert saved["certificate"]["valuation_audit"]["odd_p_not_dividing_delta"] == (
        "v_p(H_RL)=0 mod 2"
    )
