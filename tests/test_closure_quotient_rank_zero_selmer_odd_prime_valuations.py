from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_selmer_odd_prime_valuations import (
    BOUNDARY,
    KERNEL_VALUATION_SHAPES,
    audit_rank_zero_selmer_odd_prime_valuations,
    write_json,
)


def _odd_prime_cases() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "package_count": 2,
        "coprime_support_entry_count": 2,
        "odd_prime_case_count": 6,
        "two_adic_case_count": 2,
        "case_checklist_not_proof": True,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "case_entries": [
            {
                "package_id": "rank-zero-selmer-AA-kernel-minus-p",
                "kernel": "kernel_minus_p",
                "case_label": "odd-prime-divides-L",
                "prime_condition": "ell odd and ell | L",
                "required_transcript_section": "local_squareclass_conditions",
                "case_status": "open",
                "local_condition_proved": False,
            },
            {
                "package_id": "rank-zero-selmer-AA-kernel-minus-p",
                "kernel": "kernel_minus_p",
                "case_label": "odd-prime-divides-T",
                "prime_condition": "ell odd and ell | T",
                "required_transcript_section": "local_squareclass_conditions",
                "case_status": "open",
                "local_condition_proved": False,
            },
            {
                "package_id": "rank-zero-selmer-AA-kernel-minus-p",
                "kernel": "kernel_minus_p",
                "case_label": "odd-prime-divides-T2-plus-4L2",
                "prime_condition": "ell odd and ell | T^2 + 4*L^2",
                "required_transcript_section": "local_squareclass_conditions",
                "case_status": "open",
                "local_condition_proved": False,
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
                "kernel": "kernel_pos_2sqrt_q",
                "case_label": "odd-prime-divides-L",
                "prime_condition": "ell odd and ell | L",
                "required_transcript_section": "local_squareclass_conditions",
                "case_status": "open",
                "local_condition_proved": False,
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
                "kernel": "kernel_pos_2sqrt_q",
                "case_label": "odd-prime-divides-T",
                "prime_condition": "ell odd and ell | T",
                "required_transcript_section": "local_squareclass_conditions",
                "case_status": "open",
                "local_condition_proved": False,
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
                "kernel": "kernel_pos_2sqrt_q",
                "case_label": "odd-prime-divides-T2-plus-4L2",
                "prime_condition": "ell odd and ell | T^2 + 4*L^2",
                "required_transcript_section": "local_squareclass_conditions",
                "case_status": "open",
                "local_condition_proved": False,
            },
            {
                "package_id": "rank-zero-selmer-CC-kernel-neg-2sqrt-q",
                "kernel": "kernel_neg_2sqrt_q",
                "case_label": "odd-prime-divides-T2-plus-4L2",
                "prime_condition": "ell odd and ell | T^2 + 4*L^2",
                "required_transcript_section": "local_squareclass_conditions",
                "case_status": "open",
                "local_condition_proved": False,
            },
        ],
    }


def test_rank_zero_selmer_odd_prime_valuations_export_shape_candidates() -> None:
    audit = audit_rank_zero_selmer_odd_prime_valuations(
        odd_prime_cases=_odd_prime_cases(),
    )

    assert audit["status"] == "ok"
    assert audit["package_count"] == 2
    assert audit["odd_prime_valuation_case_count"] == 7
    assert audit["valuation_shapes_not_conditions"] is True
    assert audit["local_condition_proved_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["boundary"] == BOUNDARY
    assert set(audit["kernel_valuation_shapes"]) == set(KERNEL_VALUATION_SHAPES)
    assert audit["valuation_entries"][0] == {
        "package_id": "rank-zero-selmer-AA-kernel-minus-p",
        "kernel": "kernel_minus_p",
        "case_label": "odd-prime-divides-L",
        "prime_condition": "ell odd and ell | L",
        "target_a2": "32*L^2 - 8*T^2",
        "target_a4": "16*(T^2 + 4*L^2)^2",
        "quadratic_discriminant": "-1024*L^2*T^2",
        "a2_valuation_shape": "v_ell(a2)=0; a2 == -8*T^2 mod ell",
        "a4_valuation_shape": "v_ell(a4)=0",
        "quadratic_discriminant_valuation_shape": "v_ell(discriminant)=2*v_ell(L)",
        "unit_reason": (
            "ell is odd, ell | L, and coprime support gives ell not dividing "
            "T or T^2 + 4*L^2"
        ),
        "valuation_shape_status": "candidate",
        "local_condition_proved": False,
    }
    assert audit["valuation_entries"][4]["a4_valuation_shape"] == (
        "v_ell(a4)=4*v_ell(T)"
    )
    assert audit["valuation_entries"][5]["quadratic_discriminant_valuation_shape"] == (
        "v_ell(discriminant)=v_ell(T^2 + 4*L^2)"
    )
    assert audit["valuation_entries"][6]["a2_valuation_shape"] == (
        "v_ell(a2)=0; a2 == -32*L^2 mod ell"
    )


def test_rank_zero_selmer_odd_prime_valuations_reports_unready_inputs() -> None:
    odd_prime_cases = _odd_prime_cases()
    odd_prime_cases["ready"] = False
    odd_prime_cases["status"] = "issues"

    audit = audit_rank_zero_selmer_odd_prime_valuations(
        odd_prime_cases=odd_prime_cases,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["odd_prime_cases_not_ready"]


def test_rank_zero_selmer_odd_prime_valuations_cli_writes_audit(
    tmp_path: Path,
) -> None:
    odd_prime_cases = tmp_path / "odd_prime_cases.json"
    out = tmp_path / "odd_prime_valuations.json"
    odd_prime_cases.write_text(json.dumps(_odd_prime_cases()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_valuations.py",
            "--odd-prime-cases",
            str(odd_prime_cases),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "odd_prime_valuation_case_count=7" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["valuation_shapes_not_conditions"] is True


def test_write_json_writes_sorted_rank_zero_selmer_odd_prime_valuations(
    tmp_path: Path,
) -> None:
    out = tmp_path / "odd_prime_valuations.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
