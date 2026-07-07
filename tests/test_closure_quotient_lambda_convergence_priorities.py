from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_lambda_convergence_priorities import (
    BOUNDARY,
    audit_lambda_convergence_priorities,
    write_json,
)


def _proof_seed_coverage() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lambda_class_count": 6,
        "seed_ledger_class_count": 6,
        "all_routes_have_seed_ledgers": True,
        "search_count_used_as_progress": False,
        "family_exclusion_proved_count": 0,
    }


def _rank_zero_seeds() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "seed_group_count": 2,
        "candidate_class_count": 3,
        "model_count": 4,
        "family_exclusion_proved_count": 0,
        "groups": [
            {"family_exclusion_proved": False},
            {"family_exclusion_proved": False},
        ],
    }


def _rank_zero_identity_audit() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "coefficient_identity_verified_count": 4,
        "coefficient_identity_violation_count": 0,
    }


def _rank_zero_invariants() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "all_matched_models_rank_zero": True,
        "all_matched_models_root_number_one": True,
        "all_matched_models_torsion_order_four": True,
        "missing_primitive_model_count": 0,
        "family_exclusion_proved_count": 0,
    }


def _rank_zero_forced_torsion() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "forced_two_torsion_violation_count": 0,
        "observed_extra_torsion_model_count": 0,
        "family_exclusion_proved_count": 0,
    }


def _root_number_seeds() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "seed_group_count": 1,
        "target_class_count": 2,
        "target_pair_count": 3,
        "family_exclusion_proved_count": 0,
        "groups": [{"family_exclusion_proved": False}],
    }


def _two_cover_seeds() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "seed_group_count": 1,
        "target_class_count": 1,
        "candidate_cover_total": 2,
        "family_exclusion_proved_count": 0,
        "groups": [
            {
                "candidate_not_proof": True,
                "required_strict_evidence": ["reviewable no-point certificate"],
                "family_exclusion_proved": False,
            }
        ],
    }


def _audit() -> dict[str, object]:
    return audit_lambda_convergence_priorities(
        proof_seed_coverage=_proof_seed_coverage(),
        rank_zero_seeds=_rank_zero_seeds(),
        rank_zero_identity_audit=_rank_zero_identity_audit(),
        rank_zero_invariants=_rank_zero_invariants(),
        rank_zero_forced_torsion=_rank_zero_forced_torsion(),
        root_number_seeds=_root_number_seeds(),
        two_cover_seeds=_two_cover_seeds(),
    )


def test_lambda_convergence_priorities_rank_family_proof_first() -> None:
    audit = _audit()

    assert audit["status"] == "ok"
    assert audit["convergence_complete"] is False
    assert audit["priority_order"] == ["rank_zero", "root_number", "two_cover"]
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["routes"][0] == {
        "route": "rank_zero",
        "priority": 1,
        "class_count": 3,
        "seed_group_count": 2,
        "model_count": 4,
        "supporting_model_count": 4,
        "missing_theorem": "rank-zero primitive lambda family theorem",
        "next_action": (
            "Prove the three rank-zero primitive lambda patterns as family "
            "theorems, using the coefficient identities, matched rank-zero "
            "invariants, and forced full rational 2-torsion as reviewable inputs."
        ),
        "family_exclusion_proved": False,
    }
    assert audit["boundary"] == BOUNDARY


def test_lambda_convergence_priorities_reports_boundary_violations() -> None:
    two_cover = _two_cover_seeds()
    two_cover["groups"] = [{"candidate_not_proof": False}]
    rank_zero_invariants = _rank_zero_invariants()
    rank_zero_invariants["all_matched_models_rank_zero"] = False

    audit = audit_lambda_convergence_priorities(
        proof_seed_coverage=_proof_seed_coverage(),
        rank_zero_seeds=_rank_zero_seeds(),
        rank_zero_identity_audit=_rank_zero_identity_audit(),
        rank_zero_invariants=rank_zero_invariants,
        rank_zero_forced_torsion=_rank_zero_forced_torsion(),
        root_number_seeds=_root_number_seeds(),
        two_cover_seeds=two_cover,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "rank_zero_support_ready",
        "two_cover_requires_strict_evidence",
    ]


def test_lambda_convergence_priorities_cli_writes_audit(tmp_path: Path) -> None:
    proof_seed_coverage = tmp_path / "proof_seed_coverage.json"
    rank_zero_seeds = tmp_path / "rank_zero_seeds.json"
    rank_zero_identity = tmp_path / "rank_zero_identity.json"
    rank_zero_invariants = tmp_path / "rank_zero_invariants.json"
    rank_zero_forced_torsion = tmp_path / "rank_zero_forced_torsion.json"
    root_number_seeds = tmp_path / "root_number_seeds.json"
    two_cover_seeds = tmp_path / "two_cover_seeds.json"
    out = tmp_path / "priorities.json"
    proof_seed_coverage.write_text(json.dumps(_proof_seed_coverage()), encoding="utf-8")
    rank_zero_seeds.write_text(json.dumps(_rank_zero_seeds()), encoding="utf-8")
    rank_zero_identity.write_text(
        json.dumps(_rank_zero_identity_audit()),
        encoding="utf-8",
    )
    rank_zero_invariants.write_text(json.dumps(_rank_zero_invariants()), encoding="utf-8")
    rank_zero_forced_torsion.write_text(
        json.dumps(_rank_zero_forced_torsion()),
        encoding="utf-8",
    )
    root_number_seeds.write_text(json.dumps(_root_number_seeds()), encoding="utf-8")
    two_cover_seeds.write_text(json.dumps(_two_cover_seeds()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_lambda_convergence_priorities.py",
            "--proof-seed-coverage",
            str(proof_seed_coverage),
            "--rank-zero-seeds",
            str(rank_zero_seeds),
            "--rank-zero-identity-audit",
            str(rank_zero_identity),
            "--rank-zero-invariants",
            str(rank_zero_invariants),
            "--rank-zero-forced-torsion",
            str(rank_zero_forced_torsion),
            "--root-number-seeds",
            str(root_number_seeds),
            "--two-cover-seeds",
            str(two_cover_seeds),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "priority_order=['rank_zero', 'root_number', 'two_cover']" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["convergence_complete"] is False


def test_write_json_writes_sorted_lambda_convergence_priorities(tmp_path: Path) -> None:
    out = tmp_path / "priorities.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
