from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_selmer_odd_prime_lemma_queue import (
    BOUNDARY,
    audit_rank_zero_selmer_odd_prime_lemma_queue,
    write_json,
)


def _odd_prime_valuations() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "package_count": 3,
        "odd_prime_case_count": 3,
        "odd_prime_valuation_case_count": 3,
        "valuation_shapes_not_conditions": True,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "valuation_entries": [
            {
                "package_id": "rank-zero-selmer-AA-kernel-minus-p",
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
                "valuation_shape_status": "candidate",
                "local_condition_proved": False,
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-minus-p",
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
                "valuation_shape_status": "candidate",
                "local_condition_proved": False,
            },
            {
                "package_id": "rank-zero-selmer-AA-kernel-pos-2sqrt-q",
                "kernel": "kernel_pos_2sqrt_q",
                "case_label": "odd-prime-divides-T",
                "prime_condition": "ell odd and ell | T",
                "target_a2": "-8*(T^2 + 8*L^2)",
                "target_a4": "16*T^4",
                "quadratic_discriminant": "1024*L^2*(T^2 + 4*L^2)",
                "a2_valuation_shape": "v_ell(a2)=0; a2 == -64*L^2 mod ell",
                "a4_valuation_shape": "v_ell(a4)=4*v_ell(T)",
                "quadratic_discriminant_valuation_shape": "v_ell(discriminant)=0",
                "unit_reason": (
                    "ell is odd, ell | T, and coprime support gives ell not "
                    "dividing L or T^2 + 4*L^2"
                ),
                "valuation_shape_status": "candidate",
                "local_condition_proved": False,
            },
        ],
    }


def test_rank_zero_selmer_odd_prime_lemma_queue_groups_uniform_shapes() -> None:
    audit = audit_rank_zero_selmer_odd_prime_lemma_queue(
        odd_prime_valuations=_odd_prime_valuations(),
    )

    assert audit["status"] == "ok"
    assert audit["input_valuation_case_count"] == 3
    assert audit["lemma_obligation_count"] == 2
    assert audit["lemma_queue_not_proof"] is True
    assert audit["local_lemma_proved_count"] == 0
    assert audit["local_condition_proved_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["boundary"] == BOUNDARY
    assert audit["lemma_obligations"][0] == {
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
            "ell is odd, ell | L, and coprime support gives ell not dividing "
            "T or T^2 + 4*L^2"
        ),
        "covered_valuation_case_count": 2,
        "package_ids": [
            "rank-zero-selmer-AA-kernel-minus-p",
            "rank-zero-selmer-BB-kernel-minus-p",
        ],
        "uniform_over_packages": True,
        "required_transcript_section": "local_squareclass_conditions",
        "next_review_task": (
            "prove this valuation shape gives the required local squareclass "
            "condition for arbitrary primitive A:B"
        ),
        "proof_status": "open",
        "local_lemma_proved": False,
        "local_condition_proved": False,
    }


def test_rank_zero_selmer_odd_prime_lemma_queue_reports_unready_inputs() -> None:
    odd_prime_valuations = _odd_prime_valuations()
    odd_prime_valuations["ready"] = False
    odd_prime_valuations["status"] = "issues"

    audit = audit_rank_zero_selmer_odd_prime_lemma_queue(
        odd_prime_valuations=odd_prime_valuations,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["odd_prime_valuations_not_ready"]


def test_rank_zero_selmer_odd_prime_lemma_queue_cli_writes_audit(
    tmp_path: Path,
) -> None:
    odd_prime_valuations = tmp_path / "odd_prime_valuations.json"
    out = tmp_path / "odd_prime_lemma_queue.json"
    odd_prime_valuations.write_text(
        json.dumps(_odd_prime_valuations()),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_lemma_queue.py",
            "--odd-prime-valuations",
            str(odd_prime_valuations),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "lemma_obligation_count=2" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["lemma_queue_not_proof"] is True


def test_write_json_writes_sorted_rank_zero_selmer_odd_prime_lemma_queue(
    tmp_path: Path,
) -> None:
    out = tmp_path / "odd_prime_lemma_queue.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
