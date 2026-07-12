from __future__ import annotations

import importlib
import json
import subprocess
import sys
from itertools import product
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


def _module():
    try:
        return importlib.import_module(
            "scripts.theory."
            "audit_closure_quotient_rank_zero_aa_bb_wl551_m2_pure_v_ell_global_norm_squareclass_pairing"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl551_m2_pure_v_ell_global_norm_squareclass_pairing()


def test_wl551_norm_square_forces_each_split_pair_to_match() -> None:
    split_primes = [5, 13, 17]
    inert_primes = [3, 7, 11]
    for split_bits in product((0, 1), repeat=2 * len(split_primes)):
        for inert_bits in product((0, 1), repeat=len(inert_primes)):
            norm_exponents = {
                prime: split_bits[2 * index] + split_bits[2 * index + 1]
                for index, prime in enumerate(split_primes)
            }
            norm_exponents.update(
                {prime: 2 * inert_bits[index] for index, prime in enumerate(inert_primes)}
            )
            norm_is_square = all(exponent % 2 == 0 for exponent in norm_exponents.values())
            split_pairs_match = all(
                split_bits[2 * index] == split_bits[2 * index + 1]
                for index in range(len(split_primes))
            )
            assert norm_is_square == split_pairs_match


def test_wl551_reduced_classes_are_rational_squarefree_factors() -> None:
    audit = _audit()
    certificate = audit["norm_certificate"]
    assert certificate["conclusion"] == "Norm(d) is an integer square"
    assert certificate["reduced_factor"] == (
        "d=r up to a unit, with rational squarefree r|rad(ell-1)"
    )
    assert certificate["unit_classes_modulo_squares"] == ["1", "i"]


def test_wl551_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["split_Gaussian_primes_paired_here"] is True
    assert audit["proof_status"]["global_rational_class_equations_solved_here"] is False
    assert audit["rational_wl535_point_produced_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl551_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl550_ready", lambda _: False)
    audit = module.build_wl551_m2_pure_v_ell_global_norm_squareclass_pairing()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl551_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl551.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl551_m2_pure_v_ell_global_norm_squareclass_pairing.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "split_Gaussian_primes_paired_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
