from __future__ import annotations

import importlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

MODULE_NAME = (
    "scripts.theory.audit_closure_quotient_rank_zero_selmer_kernel_local_schemas"
)


def _schemas_module() -> ModuleType:
    assert importlib.util.find_spec(MODULE_NAME) is not None
    return importlib.import_module(MODULE_NAME)


def _local_supports() -> dict[str, object]:
    support_rows: list[dict[str, object]] = []
    templates = {
        "kernel_minus_p": {
            "target_a2": "32*L^2 - 8*T^2",
            "target_a4": "16*(T^2 + 4*L^2)^2",
            "a4_square_root": "4*(T^2 + 4*L^2)",
            "quadratic_discriminant": "-1024*L^2*T^2",
            "quadratic_discriminant_squareclass": "-1",
        },
        "kernel_neg_2sqrt_q": {
            "target_a2": "16*(T^2 + 2*L^2)",
            "target_a4": "256*L^4",
            "a4_square_root": "16*L^2",
            "quadratic_discriminant": "256*T^2*(T^2 + 4*L^2)",
            "quadratic_discriminant_squareclass": "T^2 + 4*L^2",
        },
        "kernel_pos_2sqrt_q": {
            "target_a2": "-8*(T^2 + 8*L^2)",
            "target_a4": "16*T^4",
            "a4_square_root": "4*T^2",
            "quadratic_discriminant": "1024*L^2*(T^2 + 4*L^2)",
            "quadratic_discriminant_squareclass": "T^2 + 4*L^2",
        },
    }
    for family_pattern in ["AA", "BB"]:
        for kernel, template in templates.items():
            support_rows.append(
                {
                    "package_id": f"rank-zero-selmer-{family_pattern}-{kernel}",
                    "family_pattern": family_pattern,
                    "kernel": kernel,
                    "status": "open",
                    "candidate_bad_factors": ["2", "L", "T", "T^2 + 4*L^2"],
                    "support_candidates_not_conditions": True,
                    "local_condition_proved": False,
                    "selmer_rank_upper_bound_proved": False,
                    "family_exclusion_proved": False,
                    **template,
                }
            )
    return {
        "status": "ok",
        "ready": True,
        "package_count": 6,
        "support_entry_count": 6,
        "kernel_count": 3,
        "support_factor_template": ["2", "L", "T", "T^2 + 4*L^2"],
        "support_candidates_not_conditions": True,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "support_entries": support_rows,
        "violations": [],
    }


def test_kernel_local_schemas_collapse_supports_by_kernel() -> None:
    schemas = _schemas_module()

    audit = schemas.audit_rank_zero_selmer_kernel_local_schemas(
        local_supports=_local_supports()
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["package_count"] == 6
    assert audit["support_entry_count"] == 6
    assert audit["family_pattern_count"] == 2
    assert audit["kernel_schema_count"] == 3
    assert audit["shared_kernel_schema_count"] == 3
    assert audit["local_condition_proved_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["violations"] == []

    by_kernel = {row["kernel"]: row for row in audit["kernel_schemas"]}
    assert by_kernel["kernel_minus_p"] == {
        "schema_id": "rank-zero-selmer-local-support-kernel-minus-p",
        "kernel": "kernel_minus_p",
        "family_patterns": ["AA", "BB"],
        "package_ids": [
            "rank-zero-selmer-AA-kernel_minus_p",
            "rank-zero-selmer-BB-kernel_minus_p",
        ],
        "package_count": 2,
        "target_a2": "32*L^2 - 8*T^2",
        "target_a4": "16*(T^2 + 4*L^2)^2",
        "a4_square_root": "4*(T^2 + 4*L^2)",
        "quadratic_discriminant": "-1024*L^2*T^2",
        "quadratic_discriminant_squareclass": "-1",
        "candidate_bad_factors": ["2", "L", "T", "T^2 + 4*L^2"],
        "support_candidates_not_conditions": True,
        "local_condition_proved": False,
        "selmer_rank_upper_bound_proved": False,
        "family_exclusion_proved": False,
    }


def test_kernel_local_schemas_reject_inconsistent_kernel_signature() -> None:
    schemas = _schemas_module()
    local_supports = _local_supports()
    local_supports["support_entries"][1]["quadratic_discriminant_squareclass"] = "-1"

    audit = schemas.audit_rank_zero_selmer_kernel_local_schemas(
        local_supports=local_supports
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "kernel_signature_mismatch=kernel_neg_2sqrt_q",
    ]


def test_kernel_local_schemas_cli_writes_audit(tmp_path: Path) -> None:
    local_supports = tmp_path / "local_supports.json"
    out = tmp_path / "kernel_local_schemas.json"
    local_supports.write_text(json.dumps(_local_supports()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            (
                "scripts/theory/"
                "audit_closure_quotient_rank_zero_selmer_kernel_local_schemas.py"
            ),
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

    assert "kernel_schema_count=3" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["shared_kernel_schema_count"] == 3


def test_write_json_writes_sorted_kernel_local_schemas(tmp_path: Path) -> None:
    schemas = _schemas_module()
    out = tmp_path / "kernel_local_schemas.json"

    schemas.write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
