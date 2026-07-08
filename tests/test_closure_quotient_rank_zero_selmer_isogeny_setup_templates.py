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
    "scripts.theory.audit_closure_quotient_rank_zero_selmer_isogeny_setup_templates"
)


def _templates_module() -> ModuleType:
    assert importlib.util.find_spec(MODULE_NAME) is not None
    return importlib.import_module(MODULE_NAME)


def _materialization() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "package_count": 4,
        "open_package_count": 4,
        "packages": [
            {
                "package_id": "rank-zero-selmer-AA-kernel-minus-p",
                "json_path": "unused",
                "package_payload": {
                    "package_id": "rank-zero-selmer-AA-kernel-minus-p",
                    "family_pattern": "AA",
                    "kernel": "kernel_minus_p",
                    "symbolic_model": {
                        "T": "A+B",
                        "L_role": "A for AA, B for BB; AA+BB requires both sides to close",
                        "kernel_root": "-p",
                        "target_a2": "32*L^2 - 8*T^2",
                        "target_a4": "16*(T^2 + 4*L^2)^2",
                    },
                },
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-minus-p",
                "json_path": "unused",
                "package_payload": {
                    "package_id": "rank-zero-selmer-BB-kernel-minus-p",
                    "family_pattern": "BB",
                    "kernel": "kernel_minus_p",
                    "symbolic_model": {
                        "T": "A+B",
                        "L_role": "A for AA, B for BB; AA+BB requires both sides to close",
                        "kernel_root": "-p",
                        "target_a2": "32*L^2 - 8*T^2",
                        "target_a4": "16*(T^2 + 4*L^2)^2",
                    },
                },
            },
            {
                "package_id": "rank-zero-selmer-AA-kernel-pos-2sqrt-q",
                "json_path": "unused",
                "package_payload": {
                    "package_id": "rank-zero-selmer-AA-kernel-pos-2sqrt-q",
                    "family_pattern": "AA",
                    "kernel": "kernel_pos_2sqrt_q",
                    "symbolic_model": {
                        "T": "A+B",
                        "L_role": "A for AA, B for BB; AA+BB requires both sides to close",
                        "kernel_root": "2*sqrt_q",
                        "target_a2": "-8*(T^2 + 8*L^2)",
                        "target_a4": "16*T^4",
                    },
                },
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
                "json_path": "unused",
                "package_payload": {
                    "package_id": "rank-zero-selmer-BB-kernel-pos-2sqrt_q",
                    "family_pattern": "BB",
                    "kernel": "kernel_pos_2sqrt_q",
                    "symbolic_model": {
                        "T": "A+B",
                        "L_role": "A for AA, B for BB; AA+BB requires both sides to close",
                        "kernel_root": "2*sqrt_q",
                        "target_a2": "-8*(T^2 + 8*L^2)",
                        "target_a4": "16*T^4",
                    },
                },
            },
        ],
    }


def _kernel_local_schemas() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "kernel_schema_count": 2,
        "kernel_schemas": [
            {
                "schema_id": "rank-zero-selmer-local-support-kernel-minus-p",
                "kernel": "kernel_minus_p",
                "package_ids": [
                    "rank-zero-selmer-AA-kernel-minus-p",
                    "rank-zero-selmer-BB-kernel-minus-p",
                ],
            },
            {
                "schema_id": "rank-zero-selmer-local-support-kernel-pos-2sqrt-q",
                "kernel": "kernel_pos_2sqrt_q",
                "package_ids": [
                    "rank-zero-selmer-AA-kernel-pos-2sqrt-q",
                    "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
                ],
            },
        ],
    }


def test_isogeny_setup_templates_collapse_by_kernel() -> None:
    templates = _templates_module()

    audit = templates.audit_rank_zero_selmer_isogeny_setup_templates(
        materialization=_materialization(),
        kernel_local_schemas=_kernel_local_schemas(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["package_count"] == 4
    assert audit["kernel_schema_count"] == 2
    assert audit["setup_template_count"] == 2
    assert audit["shared_isogeny_setup_template_count"] == 2
    assert audit["search_count_used_as_progress"] is False
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["violations"] == []
    assert audit["setup_templates"][0] == {
        "kernel": "kernel_minus_p",
        "kernel_schema_id": "rank-zero-selmer-local-support-kernel-minus-p",
        "package_count": 2,
        "package_ids": [
            "rank-zero-selmer-AA-kernel-minus-p",
            "rank-zero-selmer-BB-kernel-minus-p",
        ],
        "symbolic_model": {
            "T": "A+B",
            "L_role": "A for AA, B for BB; AA+BB requires both sides to close",
            "kernel_root": "-p",
            "target_a2": "32*L^2 - 8*T^2",
            "target_a4": "16*(T^2 + 4*L^2)^2",
        },
    }


def test_isogeny_setup_templates_report_kernel_model_mismatch() -> None:
    templates = _templates_module()
    materialization = _materialization()
    materialization["packages"][1]["package_payload"]["symbolic_model"]["target_a2"] = (
        "BROKEN"
    )

    audit = templates.audit_rank_zero_selmer_isogeny_setup_templates(
        materialization=materialization,
        kernel_local_schemas=_kernel_local_schemas(),
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["kernel_symbolic_model_mismatch=kernel_minus_p"]


def test_isogeny_setup_templates_cli_writes_audit(tmp_path: Path) -> None:
    materialization = _materialization()
    packages_dir = tmp_path / "packages"
    packages_dir.mkdir(parents=True, exist_ok=True)
    for package in materialization["packages"]:
        package_id = package["package_id"]
        json_path = packages_dir / f"{package_id}.json"
        json_path.write_text(
            json.dumps(package["package_payload"]), encoding="utf-8"
        )
        package["json_path"] = str(json_path)
    materialization_path = tmp_path / "materialization.json"
    schemas_path = tmp_path / "schemas.json"
    out = tmp_path / "setup_templates.json"
    materialization_path.write_text(json.dumps(materialization), encoding="utf-8")
    schemas_path.write_text(json.dumps(_kernel_local_schemas()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_isogeny_setup_templates.py",
            "--materialization",
            str(materialization_path),
            "--kernel-local-schemas",
            str(schemas_path),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "setup_template_count=2" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["shared_isogeny_setup_template_count"] == 2


def test_write_json_writes_sorted_isogeny_setup_templates(tmp_path: Path) -> None:
    templates = _templates_module()
    out = tmp_path / "setup_templates.json"

    templates.write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
