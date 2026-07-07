from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_selmer_coprime_supports import (
    BOUNDARY,
    audit_rank_zero_selmer_coprime_supports,
    write_json,
)


def _local_supports() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "package_count": 2,
        "support_entry_count": 2,
        "support_candidates_not_conditions": True,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "support_factor_template": ["2", "L", "T", "T^2 + 4*L^2"],
        "support_entries": [
            {
                "package_id": "rank-zero-selmer-AA-kernel-minus-p",
                "kernel": "kernel_minus_p",
                "candidate_bad_factors": ["2", "L", "T", "T^2 + 4*L^2"],
                "local_condition_proved": False,
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
                "kernel": "kernel_pos_2sqrt_q",
                "candidate_bad_factors": ["2", "L", "T", "T^2 + 4*L^2"],
                "local_condition_proved": False,
            },
        ],
    }


def test_rank_zero_selmer_coprime_supports_exports_odd_prime_partition() -> None:
    audit = audit_rank_zero_selmer_coprime_supports(local_supports=_local_supports())

    assert audit == {
        "status": "ok",
        "ready": True,
        "package_count": 2,
        "support_entry_count": 2,
        "coprime_support_entry_count": 2,
        "support_candidates_not_conditions": True,
        "two_adic_exception": True,
        "odd_prime_partition": [
            "odd primes dividing L",
            "odd primes dividing T",
            "odd primes dividing T^2 + 4*L^2",
        ],
        "symbolic_coprimality_facts": [
            {
                "statement": "gcd(L, T) = 1",
                "reason": "gcd(L, T)=gcd(L, A+B)=gcd(A, B) for primitive A:B",
            },
            {
                "statement": "gcd(L, T^2 + 4*L^2) = 1",
                "reason": "any common prime divides L and T^2, hence divides gcd(L,T)",
            },
            {
                "statement": "gcd(T, T^2 + 4*L^2) divides 4",
                "reason": "any common prime divides T and 4*L^2; odd common primes divide gcd(T,L)",
            },
        ],
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
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
        "violations": [],
        "boundary": BOUNDARY,
    }


def test_rank_zero_selmer_coprime_supports_reports_unready_inputs() -> None:
    local_supports = _local_supports()
    local_supports["ready"] = False
    local_supports["status"] = "issues"

    audit = audit_rank_zero_selmer_coprime_supports(local_supports=local_supports)

    assert audit["status"] == "issues"
    assert audit["violations"] == ["local_supports_not_ready"]


def test_rank_zero_selmer_coprime_supports_cli_writes_audit(tmp_path: Path) -> None:
    local_supports = tmp_path / "local_supports.json"
    out = tmp_path / "coprime_supports.json"
    local_supports.write_text(json.dumps(_local_supports()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_coprime_supports.py",
            "--local-supports",
            str(local_supports),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "coprime_support_entry_count=2" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["two_adic_exception"] is True


def test_write_json_writes_sorted_rank_zero_selmer_coprime_supports(
    tmp_path: Path,
) -> None:
    out = tmp_path / "coprime_supports.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
