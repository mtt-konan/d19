from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_family_obligations import (
    BOUNDARY,
    audit_rank_zero_family_obligations,
    write_json,
)


def _convergence_priorities() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "priority_order": ["rank_zero", "root_number", "two_cover"],
        "family_exclusion_proved_count": 0,
        "routes": [
            {
                "route": "rank_zero",
                "missing_theorem": "rank-zero primitive lambda family theorem",
                "family_exclusion_proved": False,
            }
        ],
    }


def _rank_zero_seeds() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "seed_group_count": 2,
        "candidate_class_count": 3,
        "family_exclusion_proved_count": 0,
        "groups": [
            {
                "pattern": "AA",
                "candidate_class_count": 2,
                "model_count": 2,
                "model_counts_by_curve": {"AA": 2},
                "family_exclusion_proved": False,
            },
            {
                "pattern": "BB",
                "candidate_class_count": 1,
                "model_count": 1,
                "model_counts_by_curve": {"BB": 1},
                "family_exclusion_proved": False,
            },
        ],
    }


def _primitive_models() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "model_count": 3,
        "family_exclusion_proved_count": 0,
    }


def _identity_audit() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "coefficient_identity_verified_count": 3,
        "coefficient_identity_violation_count": 0,
    }


def _invariants() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "primitive_model_count": 3,
        "missing_primitive_model_count": 0,
        "all_matched_models_rank_zero": True,
        "all_matched_models_root_number_one": True,
        "all_matched_models_torsion_order_four": True,
        "family_exclusion_proved_count": 0,
    }


def _forced_torsion() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "primitive_model_count": 3,
        "forced_full_two_torsion_count": 3,
        "forced_two_torsion_violation_count": 0,
        "observed_extra_torsion_model_count": 0,
        "family_exclusion_proved_count": 0,
    }


def _audit() -> dict[str, object]:
    return audit_rank_zero_family_obligations(
        convergence_priorities=_convergence_priorities(),
        rank_zero_seeds=_rank_zero_seeds(),
        primitive_models=_primitive_models(),
        identity_audit=_identity_audit(),
        invariants=_invariants(),
        forced_torsion=_forced_torsion(),
    )


def test_rank_zero_family_obligations_keep_theorem_gap_open() -> None:
    audit = _audit()

    assert audit["status"] == "ok"
    assert audit["rank_zero_family_proof_complete"] is False
    assert audit["rank_zero_family_obligation_count"] == 2
    assert audit["open_obligation_count"] == 2
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["next_main_action"] == (
        "Prove a uniform rank-zero theorem for the AA, AA+BB, and BB "
        "primitive lambda seed groups."
    )
    assert audit["groups"][0] == {
        "priority": 1,
        "pattern": "AA",
        "candidate_class_count": 2,
        "model_count": 2,
        "model_counts_by_curve": {"AA": 2},
        "already_checked_inputs": [
            "coefficient identities",
            "observed rank-zero invariant rows",
            "forced full rational 2-torsion",
        ],
        "missing_theorem": "uniform rank-zero proof over the primitive lambda family",
        "acceptable_closure_routes": [
            "uniform 2-isogeny or Selmer descent rank upper bound for the seed family",
            "or an external reviewable rank-zero theorem certificate for the seed family",
        ],
        "unacceptable_progress": (
            "More individual scaled (A,B) rank rows are diagnostics only; they "
            "are not rank-zero family proof progress."
        ),
        "family_exclusion_proved": False,
    }
    assert audit["boundary"] == BOUNDARY


def test_rank_zero_family_obligations_report_support_violations() -> None:
    invariants = _invariants()
    invariants["all_matched_models_rank_zero"] = False
    seeds = _rank_zero_seeds()
    seeds["groups"] = [{**seeds["groups"][0], "family_exclusion_proved": True}]

    audit = audit_rank_zero_family_obligations(
        convergence_priorities=_convergence_priorities(),
        rank_zero_seeds=seeds,
        primitive_models=_primitive_models(),
        identity_audit=_identity_audit(),
        invariants=invariants,
        forced_torsion=_forced_torsion(),
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "rank_zero_seed_groups_present",
        "primitive_support_complete",
        "group_boundaries_retained",
    ]


def test_rank_zero_family_obligations_cli_writes_audit(tmp_path: Path) -> None:
    convergence = tmp_path / "convergence.json"
    seeds = tmp_path / "seeds.json"
    primitive = tmp_path / "primitive.json"
    identity = tmp_path / "identity.json"
    invariants = tmp_path / "invariants.json"
    forced = tmp_path / "forced.json"
    out = tmp_path / "obligations.json"
    convergence.write_text(json.dumps(_convergence_priorities()), encoding="utf-8")
    seeds.write_text(json.dumps(_rank_zero_seeds()), encoding="utf-8")
    primitive.write_text(json.dumps(_primitive_models()), encoding="utf-8")
    identity.write_text(json.dumps(_identity_audit()), encoding="utf-8")
    invariants.write_text(json.dumps(_invariants()), encoding="utf-8")
    forced.write_text(json.dumps(_forced_torsion()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_family_obligations.py",
            "--convergence-priorities",
            str(convergence),
            "--rank-zero-seeds",
            str(seeds),
            "--primitive-models",
            str(primitive),
            "--identity-audit",
            str(identity),
            "--invariants",
            str(invariants),
            "--forced-torsion",
            str(forced),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "rank_zero_family_obligation_count=2" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "rank_zero_family_proof_complete"
    ] is False


def test_write_json_writes_sorted_rank_zero_family_obligations(tmp_path: Path) -> None:
    out = tmp_path / "obligations.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
