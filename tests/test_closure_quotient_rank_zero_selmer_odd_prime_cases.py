from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_selmer_odd_prime_cases import (
    BOUNDARY,
    ODD_PRIME_CASES,
    audit_rank_zero_selmer_odd_prime_cases,
    write_json,
)


def _coprime_supports() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "package_count": 2,
        "support_entry_count": 2,
        "coprime_support_entry_count": 2,
        "support_candidates_not_conditions": True,
        "two_adic_exception": True,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "odd_prime_partition": [
            "odd primes dividing L",
            "odd primes dividing T",
            "odd primes dividing T^2 + 4*L^2",
        ],
        "entries": [
            {
                "package_id": "rank-zero-selmer-AA-kernel-minus-p",
                "kernel": "kernel_minus_p",
                "odd_prime_partition_applies": True,
                "two_adic_check_required": True,
                "local_condition_proved": False,
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
                "kernel": "kernel_pos_2sqrt_q",
                "odd_prime_partition_applies": True,
                "two_adic_check_required": True,
                "local_condition_proved": False,
            },
        ],
    }


def test_rank_zero_selmer_odd_prime_cases_exports_open_case_checklist() -> None:
    audit = audit_rank_zero_selmer_odd_prime_cases(
        coprime_supports=_coprime_supports(),
    )

    assert audit["status"] == "ok"
    assert audit["package_count"] == 2
    assert audit["odd_prime_case_count"] == 6
    assert audit["two_adic_case_count"] == 2
    assert audit["local_condition_proved_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["case_checklist_not_proof"] is True
    assert audit["odd_prime_cases"] == ODD_PRIME_CASES
    assert audit["boundary"] == BOUNDARY
    assert audit["case_entries"][0] == {
        "package_id": "rank-zero-selmer-AA-kernel-minus-p",
        "kernel": "kernel_minus_p",
        "case_label": "odd-prime-divides-L",
        "prime_condition": "ell odd and ell | L",
        "required_transcript_section": "local_squareclass_conditions",
        "case_status": "open",
        "local_condition_proved": False,
    }
    assert audit["two_adic_entries"][0] == {
        "package_id": "rank-zero-selmer-AA-kernel-minus-p",
        "kernel": "kernel_minus_p",
        "case_label": "prime-2-adic",
        "prime_condition": "ell = 2",
        "required_transcript_section": "local_squareclass_conditions",
        "case_status": "open",
        "local_condition_proved": False,
    }


def test_rank_zero_selmer_odd_prime_cases_reports_unready_inputs() -> None:
    coprime_supports = _coprime_supports()
    coprime_supports["ready"] = False
    coprime_supports["status"] = "issues"

    audit = audit_rank_zero_selmer_odd_prime_cases(
        coprime_supports=coprime_supports,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["coprime_supports_not_ready"]


def test_rank_zero_selmer_odd_prime_cases_cli_writes_audit(tmp_path: Path) -> None:
    coprime_supports = tmp_path / "coprime_supports.json"
    out = tmp_path / "odd_prime_cases.json"
    coprime_supports.write_text(json.dumps(_coprime_supports()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_cases.py",
            "--coprime-supports",
            str(coprime_supports),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "odd_prime_case_count=6" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["two_adic_case_count"] == 2


def test_write_json_writes_sorted_rank_zero_selmer_odd_prime_cases(
    tmp_path: Path,
) -> None:
    out = tmp_path / "odd_prime_cases.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
