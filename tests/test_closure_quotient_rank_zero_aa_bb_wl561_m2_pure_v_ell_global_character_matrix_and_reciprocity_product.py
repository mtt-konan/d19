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
            "audit_closure_quotient_rank_zero_aa_bb_wl561_m2_pure_v_ell_global_character_matrix_and_reciprocity_product"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl561_m2_pure_v_ell_global_character_matrix_and_reciprocity_product()


def _legendre(value: int, prime: int) -> int:
    residue = pow(value % prime, (prime - 1) // 2, prime)
    return -1 if residue == prime - 1 else residue


def test_wl561_split_split_reciprocity_pairs_cancel() -> None:
    split_primes = [5, 13, 17, 29, 37]
    product = 1
    for index, p in enumerate(split_primes):
        for q in split_primes[index + 1 :]:
            assert _legendre(q, p) == _legendre(p, q)
            product *= _legendre(q, p) * _legendre(p, q)
    assert product == 1


def test_wl561_full_product_leaves_only_inert_cross_terms() -> None:
    split = [5, 13, 17]
    inert = [3, 7, 11]
    left_class_product = 1
    for p in split:
        for q in split + inert:
            if q != p:
                left_class_product *= _legendre(q, p)
    inert_cross_product = 1
    for p in split:
        for q in inert:
            inert_cross_product *= _legendre(q, p)
    assert left_class_product == inert_cross_product


def test_wl561_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["split_prime_characters_assembled_as_F2_system_here"] is True
    assert audit["proof_status"]["reciprocity_matrix_uniform_contradiction_proved_here"] is False
    assert audit["theorem_level_selmer_matrix_claimed"] is False
    assert audit["advance_to_m3"] is False


def test_wl561_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl560_ready", lambda _: False)
    audit = module.build_wl561_m2_pure_v_ell_global_character_matrix_and_reciprocity_product()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl561_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl561.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl561_m2_pure_v_ell_global_character_matrix_and_reciprocity_product.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "split_prime_characters_assembled_as_F2_system_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
