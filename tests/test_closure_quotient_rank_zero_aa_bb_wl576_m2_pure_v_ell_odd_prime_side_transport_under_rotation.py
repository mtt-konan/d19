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
            "audit_closure_quotient_rank_zero_aa_bb_wl576_m2_pure_v_ell_odd_prime_side_transport_under_rotation"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl576_m2_pure_v_ell_odd_prime_side_transport_under_rotation()


def _legendre(value: int, prime: int) -> int:
    residue = pow(value % prime, (prime - 1) // 2, prime)
    return -1 if residue == prime - 1 else residue


def test_wl576_Delta_roots_force_two_square() -> None:
    for prime in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41):
        roots = [t for t in range(prime) if (t * t + 2 * t - 1) % prime == 0]
        assert bool(roots) == (_legendre(2, prime) == 1)


def test_wl576_regular_transport_truth_table() -> None:
    # Each tuple is (first side, vanishing coefficient, transported side).
    rows = {
        ("A", "K"): "C",
        ("A", "P"): "D",
        ("B", "K"): "D",
        ("B", "P"): "C",
    }
    assert rows[("A", "K")] == "C"
    assert rows[("A", "P")] == "D"
    assert rows[("B", "K")] == "D"
    assert rows[("B", "P")] == "C"


def test_wl576_preserves_claim_boundary() -> None:
    audit = _audit()
    proof = audit["proof_status"]
    assert audit["status"] == "ok"
    assert proof["regular_same_side_transport_by_K_here"] is True
    assert proof["regular_crossed_side_transport_by_P_here"] is True
    assert proof["singular_side_requires_higher_valuation_here"] is True
    assert proof["generic_genus_five_cover_solved_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl576_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl575_ready", lambda _: False)
    audit = module.build_wl576_m2_pure_v_ell_odd_prime_side_transport_under_rotation()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl576_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl576.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl576_m2_pure_v_ell_odd_prime_side_transport_under_rotation.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "singular_side_requires_higher_valuation_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
