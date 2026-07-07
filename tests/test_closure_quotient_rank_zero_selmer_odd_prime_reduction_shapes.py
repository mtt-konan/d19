from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_selmer_odd_prime_reduction_shapes import (
    BOUNDARY,
    audit_rank_zero_selmer_odd_prime_reduction_shapes,
    write_json,
)


def _lemma_queue() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "package_count": 3,
        "input_valuation_case_count": 6,
        "lemma_obligation_count": 2,
        "lemma_queue_not_proof": True,
        "local_lemma_proved_count": 0,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "lemma_obligations": [
            {
                "lemma_id": "odd-prime-lemma-kernel-minus-p-divides-L",
                "kernel": "kernel_minus_p",
                "case_label": "odd-prime-divides-L",
                "prime_condition": "ell odd and ell | L",
                "target_a2": "32*L^2 - 8*T^2",
                "target_a4": "16*(T^2 + 4*L^2)^2",
                "quadratic_discriminant": "-1024*L^2*T^2",
                "a2_valuation_shape": "v_ell(a2)=0; a2 == -8*T^2 mod ell",
                "a4_valuation_shape": "v_ell(a4)=0",
                "quadratic_discriminant_valuation_shape": (
                    "v_ell(discriminant)=2*v_ell(L)"
                ),
                "unit_reason": (
                    "ell is odd, ell | L, and coprime support gives ell not "
                    "dividing T or T^2 + 4*L^2"
                ),
                "covered_valuation_case_count": 3,
                "package_ids": [
                    "rank-zero-selmer-AA-kernel-minus-p",
                    "rank-zero-selmer-AA-BB-kernel-minus-p",
                    "rank-zero-selmer-BB-kernel-minus-p",
                ],
                "uniform_over_packages": True,
                "proof_status": "open",
                "local_lemma_proved": False,
                "local_condition_proved": False,
            },
            {
                "lemma_id": "odd-prime-lemma-kernel-pos-2sqrt-q-divides-T",
                "kernel": "kernel_pos_2sqrt_q",
                "case_label": "odd-prime-divides-T",
                "prime_condition": "ell odd and ell | T",
                "target_a2": "-8*(T^2 + 8*L^2)",
                "target_a4": "16*T^4",
                "quadratic_discriminant": "1024*L^2*(T^2 + 4*L^2)",
                "a2_valuation_shape": "v_ell(a2)=0; a2 == -64*L^2 mod ell",
                "a4_valuation_shape": "v_ell(a4)=4*v_ell(T)",
                "quadratic_discriminant_valuation_shape": (
                    "v_ell(discriminant)=0"
                ),
                "unit_reason": (
                    "ell is odd, ell | T, and coprime support gives ell not "
                    "dividing L or T^2 + 4*L^2"
                ),
                "covered_valuation_case_count": 3,
                "package_ids": ["rank-zero-selmer-AA-kernel-pos-2sqrt-q"],
                "uniform_over_packages": True,
                "proof_status": "open",
                "local_lemma_proved": False,
                "local_condition_proved": False,
            },
        ],
    }


def test_rank_zero_selmer_odd_prime_reduction_shapes_prove_nodal_forms() -> None:
    audit = audit_rank_zero_selmer_odd_prime_reduction_shapes(
        odd_prime_lemma_queue=_lemma_queue(),
    )

    assert audit["status"] == "ok"
    assert audit["input_lemma_obligation_count"] == 2
    assert audit["reduction_shape_count"] == 2
    assert audit["reduction_shape_proved_count"] == 2
    assert audit["reduction_shapes_not_local_conditions"] is True
    assert audit["local_condition_proved_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["boundary"] == BOUNDARY
    assert audit["reduction_entries"][0] == {
        "lemma_id": "odd-prime-lemma-kernel-minus-p-divides-L",
        "kernel": "kernel_minus_p",
        "case_label": "odd-prime-divides-L",
        "prime_condition": "ell odd and ell | L",
        "mod_relation": "L == 0 mod ell",
        "reduced_a2": "-8*T^2",
        "reduced_a4": "16*T^4",
        "reduced_cubic_factorization": "x*(x - 4*T^2)^2",
        "double_root": "4*T^2",
        "simple_root": "0",
        "double_root_unit": True,
        "simple_root_unit": False,
        "nodal_reduction_shape": "split-nodal-cubic-with-nonzero-double-root",
        "reduction_shape_proved": True,
        "local_condition_proved": False,
        "next_local_gap": (
            "derive the required isogeny-Selmer local squareclass image from "
            "this nodal reduction shape"
        ),
    }
    assert audit["reduction_entries"][1]["reduced_cubic_factorization"] == (
        "x^2*(x - 64*L^2)"
    )
    assert audit["reduction_entries"][1]["double_root"] == "0"
    assert audit["reduction_entries"][1]["simple_root_unit"] is True


def test_rank_zero_selmer_odd_prime_reduction_shapes_reports_unready_inputs() -> None:
    lemma_queue = _lemma_queue()
    lemma_queue["ready"] = False
    lemma_queue["status"] = "issues"

    audit = audit_rank_zero_selmer_odd_prime_reduction_shapes(
        odd_prime_lemma_queue=lemma_queue,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["odd_prime_lemma_queue_not_ready"]


def test_rank_zero_selmer_odd_prime_reduction_shapes_cli_writes_audit(
    tmp_path: Path,
) -> None:
    lemma_queue = tmp_path / "odd_prime_lemma_queue.json"
    out = tmp_path / "odd_prime_reduction_shapes.json"
    lemma_queue.write_text(json.dumps(_lemma_queue()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_reduction_shapes.py",
            "--odd-prime-lemma-queue",
            str(lemma_queue),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "reduction_shape_proved_count=2" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["reduction_shapes_not_local_conditions"] is True


def test_write_json_writes_sorted_rank_zero_selmer_odd_prime_reduction_shapes(
    tmp_path: Path,
) -> None:
    out = tmp_path / "odd_prime_reduction_shapes.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
