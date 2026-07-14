from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[3]
SCRIPT = ROOT / "scripts/theory/aa_bb/global_invariant_candidate_audit.py"
sys.path.insert(0, str(ROOT))


def _module():
    assert SCRIPT.is_file()
    return importlib.import_module("scripts.theory.aa_bb.global_invariant_candidate_audit")


def test_candidate_audit_certifies_the_three_exact_algebraic_boundaries() -> None:
    payload = _module().build_global_invariant_candidate_audit()

    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["outcome"] == "global_invariant_candidate_space_exhausted"
    assert payload["verification"]["violations"] == []
    assert all(payload["verification"]["checks"].values())


def test_involution_and_six_closure_directions_are_not_a_positive_domain_map() -> None:
    candidate = _module().build_global_invariant_candidate_audit()["candidates"]["involution"]

    assert all(candidate["checks"].values())
    assert candidate["degree_removed"] == 0
    assert len(candidate["closure_directions"]) == 6
    assert "q>=s" in candidate["positive_domain"]
    assert "q=s maps to q=r" in candidate["boundary_action"]


def test_integer_factorization_has_exact_split_identity_and_gcd_support() -> None:
    candidate = _module().build_global_invariant_candidate_audit()["candidates"]["factorization"]

    assert all(candidate["checks"].values())
    assert candidate["degree_removed"] == 0
    assert "(q^2-Delta-2*U*q)" in candidate["split_factorization"]
    assert "s-r=2*Bbar" in candidate["gcd_support"]["bounds"]
    assert "2*r" in candidate["gcd_support"]["bounds"]
    assert "Gaussian norm" in candidate["ring_boundary"]


def test_reciprocity_retains_odd_units_dyadic_units_and_infinity() -> None:
    candidate = _module().build_global_invariant_candidate_audit()["candidates"]["reciprocity"]

    assert all(candidate["checks"].values())
    assert "product_v" in candidate["global_formula"]
    assert "(u/p)^beta" in candidate["odd_local_formula"]
    assert "omega" in candidate["dyadic_local_formula"]
    assert "not a function" in candidate["why_bits_do_not_close"]


def test_strict_cli_materializes_the_candidate_audit(tmp_path: Path) -> None:
    out = tmp_path / "global-invariant-candidate-audit.json"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    assert result.stdout.splitlines() == [
        "status=ok",
        "task=wl596-global-invariant-candidate-audit",
        "ready=True",
        "outcome=global_invariant_candidate_space_exhausted",
        "violations=[]",
    ]
    saved = json.loads(out.read_text(encoding="utf-8"))
    assert saved["proof_boundary"]["HRL_should_pause"] is True
    assert saved["retained_boundaries"]["all_six_closure_directions"] is True
