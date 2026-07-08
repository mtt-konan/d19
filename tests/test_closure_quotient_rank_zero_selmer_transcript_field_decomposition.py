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
    "scripts.theory."
    "audit_closure_quotient_rank_zero_selmer_transcript_field_decomposition"
)


def _decomposition_module() -> ModuleType:
    assert importlib.util.find_spec(MODULE_NAME) is not None
    return importlib.import_module(MODULE_NAME)


def _transcript_intake() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "package_count": 4,
        "open_package_count": 4,
        "transcript_package_ready_count": 0,
        "missing_transcript_package_count": 4,
        "strict_promotion_ready_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "candidate_not_proof": True,
    }


def _transcript_bridge() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "package_count": 4,
        "kernel_schema_count": 2,
        "shared_local_squareclass_template_count": 2,
        "package_specific_transcript_count": 4,
        "transcript_package_ready_count": 0,
        "strict_promotion_ready_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
    }


def _isogeny_setup_templates() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "package_count": 4,
        "kernel_schema_count": 2,
        "setup_template_count": 2,
        "shared_isogeny_setup_template_count": 2,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
    }


def _family_conclusion_templates() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "family_conclusion_template_count": 2,
        "kernel_bound_package_count": 4,
        "open_family_conclusion_count": 2,
        "rank_zero_conclusion_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
    }


def test_transcript_field_decomposition_identifies_next_blocker() -> None:
    decomposition = _decomposition_module()

    audit = decomposition.audit_rank_zero_selmer_transcript_field_decomposition(
        transcript_intake=_transcript_intake(),
        transcript_bridge=_transcript_bridge(),
        isogeny_setup_templates=_isogeny_setup_templates(),
        family_conclusion_templates=_family_conclusion_templates(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["required_transcript_field_count"] == 6
    assert audit["kernel_shared_field_count"] == 2
    assert audit["kernel_shared_template_count"] == 2
    assert audit["family_aggregated_field_count"] == 1
    assert audit["family_conclusion_template_count"] == 2
    assert audit["package_specific_field_count"] == 3
    assert audit["package_specific_open_field_obligation_count"] == 12
    assert audit["primary_remaining_proof_field"] == "selmer_bound_argument"
    assert audit["transcript_package_ready_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["field_decomposition"] == {
        "kernel_shared_fields": [
            "local_squareclass_conditions",
            "isogeny_setup",
        ],
        "family_aggregated_fields": ["rank_zero_conclusion"],
        "package_specific_fields": [
            "statement",
            "selmer_bound_argument",
            "review_notes",
        ],
    }


def test_transcript_field_decomposition_rejects_promoted_family_conclusion() -> None:
    decomposition = _decomposition_module()
    family_conclusions = _family_conclusion_templates()
    family_conclusions["rank_zero_conclusion_proved_count"] = 1

    audit = decomposition.audit_rank_zero_selmer_transcript_field_decomposition(
        transcript_intake=_transcript_intake(),
        transcript_bridge=_transcript_bridge(),
        isogeny_setup_templates=_isogeny_setup_templates(),
        family_conclusion_templates=family_conclusions,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["rank_zero_conclusion_claim_count_nonzero"]


def test_transcript_field_decomposition_cli_writes_audit(tmp_path: Path) -> None:
    paths = {
        "intake": tmp_path / "intake.json",
        "bridge": tmp_path / "bridge.json",
        "isogeny": tmp_path / "isogeny.json",
        "family": tmp_path / "family.json",
    }
    paths["intake"].write_text(json.dumps(_transcript_intake()), encoding="utf-8")
    paths["bridge"].write_text(json.dumps(_transcript_bridge()), encoding="utf-8")
    paths["isogeny"].write_text(
        json.dumps(_isogeny_setup_templates()), encoding="utf-8"
    )
    paths["family"].write_text(
        json.dumps(_family_conclusion_templates()), encoding="utf-8"
    )
    out = tmp_path / "field_decomposition.json"

    result = subprocess.run(
        [
            sys.executable,
            (
                "scripts/theory/"
                "audit_closure_quotient_rank_zero_selmer_transcript_field_decomposition.py"
            ),
            "--transcript-intake",
            str(paths["intake"]),
            "--transcript-bridge",
            str(paths["bridge"]),
            "--isogeny-setup-templates",
            str(paths["isogeny"]),
            "--family-conclusion-templates",
            str(paths["family"]),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "primary_remaining_proof_field=selmer_bound_argument" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["package_specific_open_field_obligation_count"] == 12


def test_write_json_writes_sorted_transcript_field_decomposition(tmp_path: Path) -> None:
    decomposition = _decomposition_module()
    out = tmp_path / "field_decomposition.json"

    decomposition.write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
