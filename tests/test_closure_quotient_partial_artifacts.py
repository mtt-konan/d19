from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_partial_artifacts import (
    DEFAULT_REQUIRED_ARTIFACTS,
    Artifact,
    audit_artifacts,
    parse_required_artifact,
    write_json,
)


def test_audit_artifacts_marks_ready_when_required_files_exist(tmp_path: Path) -> None:
    required = [
        Artifact("script", "scripts/theory/example.py"),
        Artifact("test", "tests/test_example.py"),
        Artifact("result", "results/example.json"),
        Artifact("worklog", "docs/work-logs/999-example.md"),
    ]
    for artifact in required:
        path = tmp_path / artifact.path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("ok\n", encoding="utf-8")

    audit = audit_artifacts(root=tmp_path, required=required)

    assert audit == {
        "ready": True,
        "required_file_count": 4,
        "category_counts": {
            "result": 1,
            "script": 1,
            "test": 1,
            "worklog": 1,
        },
        "missing_files": [],
        "required_files": [
            {"category": "script", "path": "scripts/theory/example.py"},
            {"category": "test", "path": "tests/test_example.py"},
            {"category": "result", "path": "results/example.json"},
            {"category": "worklog", "path": "docs/work-logs/999-example.md"},
        ],
        "boundary": (
            "This checks artifact presence for the closure-quotient partial-result "
            "package. It does not check mathematical truth."
        ),
    }


def test_audit_artifacts_reports_missing_files(tmp_path: Path) -> None:
    required = [
        Artifact("script", "scripts/theory/present.py"),
        Artifact("result", "results/missing.json"),
    ]
    present = tmp_path / "scripts/theory/present.py"
    present.parent.mkdir(parents=True, exist_ok=True)
    present.write_text("ok\n", encoding="utf-8")

    audit = audit_artifacts(root=tmp_path, required=required)

    assert audit["ready"] is False
    assert audit["missing_files"] == [
        {"category": "result", "path": "results/missing.json"}
    ]


def test_default_artifact_manifest_includes_priority_handoff_audit() -> None:
    paths = {artifact.path for artifact in DEFAULT_REQUIRED_ARTIFACTS}

    assert "scripts/theory/audit_mixed_closure_priority_handoffs.py" in paths
    assert "scripts/theory/sage_verify_mixed_closure_handoff_maps.py" in paths
    assert "scripts/theory/sage_verify_mixed_closure_residual_cover_maps.py" in paths
    assert "scripts/theory/sage_audit_mixed_closure_rank0_torsion_preimages.py" in paths
    assert "scripts/theory/audit_mixed_closure_bsd_conditional_no_points.py" in paths
    assert "scripts/theory/audit_mixed_closure_residual_open_frontier.py" in paths
    assert "scripts/theory/summarize_mixed_closure_rank_zero_frontier.py" in paths
    assert "scripts/theory/summarize_mixed_closure_non_rankzero_frontier.py" in paths
    assert "scripts/theory/audit_mixed_closure_residual_frontier_strategy.py" in paths
    assert "scripts/theory/audit_mixed_closure_frontier_handoffs.py" in paths
    assert "scripts/theory/summarize_mixed_closure_frontier_strictification.py" in paths
    assert "scripts/theory/audit_mixed_closure_frontier_strictification_attempts.py" in paths
    assert "scripts/theory/sage_probe_mixed_closure_rank_methods.py" in paths
    assert "scripts/theory/batch_sage_probe_mixed_closure_rank_methods.py" in paths
    assert "scripts/theory/audit_mixed_closure_frontier_next_actions.py" in paths
    assert "scripts/theory/audit_mixed_closure_frontier_escalation_queue.py" in paths
    assert "scripts/theory/probe_mwrank_mixed_closure_rank.py" in paths
    assert "scripts/theory/audit_sage_cover_tool_capabilities.py" in paths
    assert "scripts/theory/audit_external_cover_descent_route.py" in paths
    assert "scripts/theory/audit_external_cover_certificate_intake.py" in paths
    assert (
        "scripts/theory/audit_external_cover_certificate_frontier_intake.py"
        in paths
    )
    assert "scripts/theory/export_external_cover_descent_packages.py" in paths
    assert "scripts/theory/audit_closure_quotient_paper_structure.py" in paths
    assert "scripts/theory/audit_closure_quotient_partial_dependencies.py" in paths
    assert "scripts/theory/summarize_closure_quotient_ray_ledger.py" in paths
    assert "scripts/theory/audit_closure_quotient_c_ratio_coverage.py" in paths
    assert "scripts/theory/summarize_closure_quotient_lambda_frontier.py" in paths
    assert "scripts/theory/audit_closure_quotient_ray_scale_invariance.py" in paths
    assert (
        "scripts/theory/summarize_closure_quotient_rank_zero_family_candidates.py"
        in paths
    )
    assert (
        "scripts/theory/summarize_closure_quotient_rank_zero_primitive_models.py"
        in paths
    )
    assert (
        "scripts/theory/summarize_closure_quotient_rank_zero_proof_seeds.py"
        in paths
    )
    assert (
        "scripts/theory/summarize_closure_quotient_rank_zero_certifying_invariants.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_forced_torsion.py" in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_seed_identities.py"
        in paths
    )
    assert (
        "scripts/theory/summarize_closure_quotient_root_number_lambda_triage.py"
        in paths
    )
    assert "scripts/theory/summarize_closure_quotient_root_number_proof_seeds.py" in paths
    assert (
        "scripts/theory/summarize_closure_quotient_two_cover_lambda_frontier.py"
        in paths
    )
    assert "scripts/theory/summarize_closure_quotient_two_cover_proof_seeds.py" in paths
    assert "scripts/theory/audit_closure_quotient_lambda_route_partition.py" in paths
    assert "scripts/theory/audit_closure_quotient_lambda_structural_handoff.py" in paths
    assert "scripts/theory/audit_closure_quotient_lambda_mainline.py" in paths
    assert "scripts/theory/audit_closure_quotient_lambda_proof_seed_coverage.py" in paths
    assert (
        "scripts/theory/audit_closure_quotient_lambda_convergence_priorities.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_family_obligations.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_symbolic_descent_inputs.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_isogeny_templates.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_obligations.py"
        in paths
    )
    assert (
        "scripts/theory/export_closure_quotient_rank_zero_selmer_package_index.py"
        in paths
    )
    assert (
        "scripts/theory/materialize_closure_quotient_rank_zero_selmer_packages.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_transcript_intake.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_local_supports.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_coprime_supports.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_cases.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_valuations.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_lemma_queue.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_reduction_shapes.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_local_image_schemas.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_tangent_one_normal_forms.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_one_unit_branch.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_one_nonnode_branches.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_one_node_values.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_one_punctured_nodes.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_one_reduction_partition.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_minus_one_normal_forms.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_minus_one_nonnode_branches.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_minus_one_node_values.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_minus_one_punctured_nodes.py"
        in paths
    )
    assert (
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_minus_one_reduction_partition.py"
        in paths
    )
    assert "scripts/theory/sage_probe_mixed_closure_local_witnesses.py" in paths
    assert "scripts/theory/summarize_mixed_closure_residual_selmer_gaps.py" in paths
    assert "tests/test_mixed_closure_priority_handoff_audit.py" in paths
    assert "tests/test_sage_verify_mixed_closure_handoff_maps.py" in paths
    assert "tests/test_sage_verify_mixed_closure_residual_cover_maps.py" in paths
    assert "tests/test_sage_audit_mixed_closure_rank0_torsion_preimages.py" in paths
    assert "tests/test_mixed_closure_bsd_conditional_no_point_audit.py" in paths
    assert "tests/test_mixed_closure_residual_open_frontier_audit.py" in paths
    assert "tests/test_mixed_closure_rank_zero_frontier_queue.py" in paths
    assert "tests/test_mixed_closure_non_rankzero_frontier_queue.py" in paths
    assert "tests/test_mixed_closure_residual_frontier_strategy.py" in paths
    assert "tests/test_mixed_closure_frontier_handoff_audit.py" in paths
    assert "tests/test_mixed_closure_frontier_strictification_queue.py" in paths
    assert "tests/test_mixed_closure_frontier_strictification_attempts.py" in paths
    assert "tests/test_sage_probe_mixed_closure_rank_methods.py" in paths
    assert "tests/test_batch_sage_probe_mixed_closure_rank_methods.py" in paths
    assert "tests/test_mixed_closure_frontier_next_action_audit.py" in paths
    assert "tests/test_mixed_closure_frontier_escalation_queue.py" in paths
    assert "tests/test_probe_mwrank_mixed_closure_rank.py" in paths
    assert "tests/test_audit_sage_cover_tool_capabilities.py" in paths
    assert "tests/test_audit_external_cover_descent_route.py" in paths
    assert "tests/test_audit_external_cover_certificate_intake.py" in paths
    assert (
        "tests/test_audit_external_cover_certificate_frontier_intake.py"
        in paths
    )
    assert "tests/test_export_external_cover_descent_packages.py" in paths
    assert "tests/test_closure_quotient_paper_structure_audit.py" in paths
    assert "tests/test_closure_quotient_partial_dependency_audit.py" in paths
    assert "tests/test_closure_quotient_ray_ledger.py" in paths
    assert "tests/test_closure_quotient_c_ratio_coverage.py" in paths
    assert "tests/test_closure_quotient_lambda_frontier.py" in paths
    assert "tests/test_closure_quotient_ray_scale_invariance.py" in paths
    assert "tests/test_closure_quotient_rank_zero_family_candidates.py" in paths
    assert "tests/test_closure_quotient_rank_zero_primitive_models.py" in paths
    assert "tests/test_closure_quotient_rank_zero_proof_seeds.py" in paths
    assert "tests/test_closure_quotient_rank_zero_certifying_invariants.py" in paths
    assert "tests/test_closure_quotient_rank_zero_forced_torsion.py" in paths
    assert "tests/test_closure_quotient_rank_zero_seed_identities.py" in paths
    assert "tests/test_closure_quotient_root_number_lambda_triage.py" in paths
    assert "tests/test_closure_quotient_root_number_proof_seeds.py" in paths
    assert "tests/test_closure_quotient_two_cover_lambda_frontier.py" in paths
    assert "tests/test_closure_quotient_two_cover_proof_seeds.py" in paths
    assert "tests/test_closure_quotient_lambda_route_partition.py" in paths
    assert "tests/test_closure_quotient_lambda_structural_handoff.py" in paths
    assert "tests/test_closure_quotient_lambda_mainline_gate.py" in paths
    assert "tests/test_closure_quotient_lambda_proof_seed_coverage.py" in paths
    assert "tests/test_closure_quotient_lambda_convergence_priorities.py" in paths
    assert "tests/test_closure_quotient_rank_zero_family_obligations.py" in paths
    assert "tests/test_closure_quotient_rank_zero_symbolic_descent_inputs.py" in paths
    assert "tests/test_closure_quotient_rank_zero_isogeny_templates.py" in paths
    assert "tests/test_closure_quotient_rank_zero_selmer_obligations.py" in paths
    assert "tests/test_closure_quotient_rank_zero_selmer_package_index.py" in paths
    assert (
        "tests/test_closure_quotient_rank_zero_selmer_package_materialization.py"
        in paths
    )
    assert (
        "tests/test_closure_quotient_rank_zero_selmer_transcript_intake.py"
        in paths
    )
    assert "tests/test_closure_quotient_rank_zero_selmer_local_supports.py" in paths
    assert "tests/test_closure_quotient_rank_zero_selmer_coprime_supports.py" in paths
    assert "tests/test_closure_quotient_rank_zero_selmer_odd_prime_cases.py" in paths
    assert (
        "tests/test_closure_quotient_rank_zero_selmer_odd_prime_valuations.py"
        in paths
    )
    assert (
        "tests/test_closure_quotient_rank_zero_selmer_odd_prime_lemma_queue.py"
        in paths
    )
    assert (
        "tests/test_closure_quotient_rank_zero_selmer_odd_prime_reduction_shapes.py"
        in paths
    )
    assert (
        "tests/test_closure_quotient_rank_zero_selmer_odd_prime_local_image_schemas.py"
        in paths
    )
    assert (
        "tests/test_closure_quotient_rank_zero_selmer_odd_prime_tangent_one_normal_forms.py"
        in paths
    )
    assert (
        "tests/test_closure_quotient_rank_zero_selmer_tangent_one_unit_branch.py"
        in paths
    )
    assert (
        "tests/test_closure_quotient_rank_zero_selmer_tangent_one_nonnode_branches.py"
        in paths
    )
    assert (
        "tests/test_closure_quotient_rank_zero_selmer_tangent_one_node_values.py"
        in paths
    )
    assert (
        "tests/test_closure_quotient_rank_zero_selmer_tangent_one_punctured_nodes.py"
        in paths
    )
    assert (
        "tests/test_closure_quotient_rank_zero_selmer_tangent_one_reduction_partition.py"
        in paths
    )
    assert (
        "tests/test_closure_quotient_rank_zero_selmer_tangent_minus_one_normal_forms.py"
        in paths
    )
    assert (
        "tests/test_closure_quotient_rank_zero_selmer_tangent_minus_one_nonnode_branches.py"
        in paths
    )
    assert (
        "tests/test_closure_quotient_rank_zero_selmer_tangent_minus_one_node_values.py"
        in paths
    )
    assert (
        "tests/test_closure_quotient_rank_zero_selmer_tangent_minus_one_punctured_nodes.py"
        in paths
    )
    assert (
        "tests/test_closure_quotient_rank_zero_selmer_tangent_minus_one_reduction_partition.py"
        in paths
    )
    assert "tests/test_sage_probe_mixed_closure_local_witnesses.py" in paths
    assert "tests/test_mixed_closure_residual_selmer_gap_ledger.py" in paths
    assert "docs/work-logs/313-priority-handoff-probe-audit.md" in paths
    assert "docs/work-logs/314-sage-cover-map-identity-verification.md" in paths
    assert "docs/work-logs/315-sage-local-witness-probe.md" in paths
    assert "docs/work-logs/316-all-residual-local-witnesses.md" in paths
    assert "docs/work-logs/317-residual-local-witness-paper-claim-gate.md" in paths
    assert "docs/work-logs/318-residual-selmer-gap-ledger.md" in paths
    assert "docs/work-logs/319-all-residual-cover-map-verification.md" in paths
    assert "docs/work-logs/320-residual-selmer-gap-frontier-split.md" in paths
    assert "docs/work-logs/321-rank0-torsion-preimage-audit.md" in paths
    assert "docs/work-logs/322-bsd-conditional-no-point-audit.md" in paths
    assert "docs/work-logs/323-residual-open-frontier-audit.md" in paths
    assert "docs/work-logs/324-rank-zero-frontier-queue.md" in paths
    assert "docs/work-logs/325-non-rankzero-frontier-queue.md" in paths
    assert "docs/work-logs/326-rank1-frontier-recheck.md" in paths
    assert "docs/work-logs/327-even-gap4-frontier-recheck.md" in paths
    assert "docs/work-logs/328-rankzero-frontier-recheck-567-3757.md" in paths
    assert "docs/work-logs/329-rankzero-frontier-recheck-5075-17901.md" in paths
    assert "docs/work-logs/330-rankzero-frontier-long-recheck-1625-5643.md" in paths
    assert "docs/work-logs/331-rankzero-frontier-recheck-8075-8613.md" in paths
    assert "docs/work-logs/332-rankzero-frontier-recheck-391-9009.md" in paths
    assert "docs/work-logs/333-rankzero-frontier-recheck-209-21735.md" in paths
    assert "docs/work-logs/334-rankzero-frontier-recheck-5083-12825.md" in paths
    assert "docs/work-logs/335-rankzero-frontier-recheck-5301-38675.md" in paths
    assert "docs/work-logs/336-residual-frontier-strategy-audit.md" in paths
    assert "docs/work-logs/337-frontier-target-handoff-1625-5643.md" in paths
    assert "docs/work-logs/338-all-rankzero-frontier-handoffs.md" in paths
    assert "docs/work-logs/339-non-rankzero-frontier-handoffs.md" in paths
    assert "docs/work-logs/340-frontier-handoff-audit.md" in paths
    assert "docs/work-logs/341-frontier-strictification-queue.md" in paths
    assert "docs/work-logs/342-frontier-strictification-attempt.md" in paths
    assert "docs/work-logs/343-frontier-rank-method-probe.md" in paths
    assert "docs/work-logs/344-frontier-batch-rank-method-probe.md" in paths
    assert "docs/work-logs/345-frontier-next-action-audit.md" in paths
    assert "docs/work-logs/346-rankzero-frontier-long-recheck-567-3757.md" in paths
    assert "docs/work-logs/347-rankzero-frontier-long-recheck-5075-17901.md" in paths
    assert "docs/work-logs/348-rankzero-frontier-long-recheck-8075-8613.md" in paths
    assert "docs/work-logs/349-rankzero-frontier-long-recheck-391-9009.md" in paths
    assert "docs/work-logs/350-rankzero-frontier-long-recheck-209-21735.md" in paths
    assert "docs/work-logs/351-rankzero-frontier-long-recheck-5083-12825.md" in paths
    assert "docs/work-logs/352-rankzero-frontier-long-recheck-5301-38675.md" in paths
    assert "docs/work-logs/353-frontier-escalation-queue.md" in paths
    assert "docs/work-logs/354-mwrank-frontier-rank-probe.md" in paths
    assert "docs/work-logs/355-sage-cover-tool-capability-audit.md" in paths
    assert "docs/work-logs/356-external-cover-descent-route-audit.md" in paths
    assert "docs/work-logs/357-external-cover-certificate-intake.md" in paths
    assert "docs/work-logs/358-frontier-external-certificate-intake.md" in paths
    assert "docs/work-logs/359-summary-gate-external-certificate-intake.md" in paths
    assert "docs/work-logs/360-paper-structure-audit.md" in paths
    assert "docs/work-logs/361-partial-result-dependency-audit.md" in paths
    assert "docs/work-logs/362-external-cover-descent-packages.md" in paths
    assert "docs/work-logs/363-closure-quotient-ray-ledger.md" in paths
    assert "docs/work-logs/408-closure-quotient-c-ratio-coverage.md" in paths
    assert "docs/work-logs/364-closure-quotient-lambda-frontier.md" in paths
    assert "docs/work-logs/365-closure-quotient-ray-scale-invariance.md" in paths
    assert "docs/work-logs/366-rank-zero-family-candidates.md" in paths
    assert "docs/work-logs/367-rank-zero-primitive-models.md" in paths
    assert "docs/work-logs/368-root-number-lambda-triage.md" in paths
    assert "docs/work-logs/369-two-cover-lambda-frontier.md" in paths
    assert "docs/work-logs/370-lambda-route-partition-audit.md" in paths
    assert "docs/work-logs/371-lambda-mainline-audit.md" in paths
    assert "docs/work-logs/372-rank-zero-proof-seeds.md" in paths
    assert "docs/work-logs/373-rank-zero-seed-identities.md" in paths
    assert "docs/work-logs/374-rank-zero-certifying-invariants.md" in paths
    assert "docs/work-logs/375-rank-zero-forced-torsion.md" in paths
    assert "docs/work-logs/376-root-number-proof-seeds.md" in paths
    assert "docs/work-logs/377-two-cover-proof-seeds.md" in paths
    assert "docs/work-logs/378-lambda-proof-seed-coverage.md" in paths
    assert "docs/work-logs/379-lambda-mainline-proof-seed-gate.md" in paths
    assert "docs/work-logs/380-lambda-convergence-priorities.md" in paths
    assert "docs/work-logs/409-closure-quotient-lambda-structural-handoff.md" in paths
    assert "docs/work-logs/381-rank-zero-family-obligations.md" in paths
    assert "docs/work-logs/382-rank-zero-symbolic-descent-inputs.md" in paths
    assert "docs/work-logs/383-rank-zero-isogeny-templates.md" in paths
    assert "docs/work-logs/384-rank-zero-selmer-obligations.md" in paths
    assert "docs/work-logs/385-rank-zero-selmer-package-index.md" in paths
    assert "docs/work-logs/386-rank-zero-selmer-package-materialization.md" in paths
    assert "docs/work-logs/387-rank-zero-selmer-transcript-intake.md" in paths
    assert "docs/work-logs/388-lambda-mainline-transcript-intake-gate.md" in paths
    assert "docs/work-logs/389-rank-zero-selmer-local-supports.md" in paths
    assert "docs/work-logs/390-rank-zero-selmer-coprime-supports.md" in paths
    assert "docs/work-logs/391-rank-zero-selmer-odd-prime-cases.md" in paths
    assert "docs/work-logs/392-rank-zero-selmer-odd-prime-valuations.md" in paths
    assert "docs/work-logs/393-rank-zero-selmer-odd-prime-lemma-queue.md" in paths
    assert "docs/work-logs/394-rank-zero-selmer-odd-prime-reduction-shapes.md" in paths
    assert "docs/work-logs/395-rank-zero-selmer-odd-prime-local-image-schemas.md" in paths
    assert "docs/work-logs/396-rank-zero-selmer-tangent-squareclass-correction.md" in paths
    assert "docs/work-logs/397-rank-zero-selmer-tangent-one-normal-forms.md" in paths
    assert "docs/work-logs/398-rank-zero-selmer-tangent-one-unit-branch.md" in paths
    assert "docs/work-logs/399-rank-zero-selmer-tangent-one-nonnode-branches.md" in paths
    assert "docs/work-logs/400-rank-zero-selmer-tangent-one-node-values.md" in paths
    assert "docs/work-logs/401-rank-zero-selmer-tangent-one-punctured-nodes.md" in paths
    assert "docs/work-logs/402-rank-zero-selmer-tangent-one-reduction-partition.md" in paths
    assert "docs/work-logs/403-rank-zero-selmer-tangent-minus-one-normal-forms.md" in paths
    assert "docs/work-logs/404-rank-zero-selmer-tangent-minus-one-nonnode-branches.md" in paths
    assert "docs/work-logs/405-rank-zero-selmer-tangent-minus-one-node-values.md" in paths
    assert "docs/work-logs/406-rank-zero-selmer-tangent-minus-one-punctured-nodes.md" in paths
    assert "docs/work-logs/407-rank-zero-selmer-tangent-minus-one-reduction-partition.md" in paths
    assert "results/mixed_closure_priority_handoff_audit_top4.json" in paths
    assert "results/mixed_closure_aabb_residual_local_witnesses.json" in paths
    assert "results/mixed_closure_residual_selmer_gap_ledger.json" in paths
    assert "results/mixed_closure_residual_cover_map_verify.json" in paths
    assert "results/mixed_closure_rank0_sha2_torsion_preimage_audit.json" in paths
    assert "results/mixed_closure_bsd_conditional_no_point_audit.json" in paths
    assert "results/mixed_closure_residual_open_frontier_audit.json" in paths
    assert "results/closure_quotient_paper_structure_audit.json" in paths
    assert "results/closure_quotient_partial_artifact_audit.json" in paths
    assert "results/closure_quotient_partial_dependency_audit.json" in paths
    assert "results/mixed_closure_external_cover_descent_package_index.json" in paths
    assert "results/closure_quotient_ray_ledger.json" in paths
    assert "results/closure_quotient_c_ratio_coverage_audit.json" in paths
    assert "results/closure_quotient_lambda_frontier.json" in paths
    assert "results/closure_quotient_ray_scale_invariance_audit.json" in paths
    assert "results/closure_quotient_rank_zero_family_candidates.json" in paths
    assert "results/closure_quotient_rank_zero_primitive_models.json" in paths
    assert "results/closure_quotient_rank_zero_proof_seeds.json" in paths
    assert "results/closure_quotient_rank_zero_certifying_invariants.json" in paths
    assert "results/closure_quotient_rank_zero_forced_torsion_audit.json" in paths
    assert "results/closure_quotient_rank_zero_seed_identity_audit.json" in paths
    assert "results/closure_quotient_root_number_lambda_triage.json" in paths
    assert "results/closure_quotient_root_number_proof_seeds.json" in paths
    assert "results/closure_quotient_two_cover_lambda_frontier.json" in paths
    assert "results/closure_quotient_two_cover_proof_seeds.json" in paths
    assert "results/closure_quotient_lambda_route_partition_audit.json" in paths
    assert "results/closure_quotient_lambda_structural_handoff_audit.json" in paths
    assert "results/closure_quotient_lambda_mainline_audit.json" in paths
    assert "results/closure_quotient_lambda_proof_seed_coverage_audit.json" in paths
    assert "results/closure_quotient_lambda_convergence_priorities.json" in paths
    assert "results/closure_quotient_rank_zero_family_obligations.json" in paths
    assert "results/closure_quotient_rank_zero_symbolic_descent_inputs.json" in paths
    assert "results/closure_quotient_rank_zero_isogeny_templates.json" in paths
    assert "results/closure_quotient_rank_zero_selmer_obligations.json" in paths
    assert "results/closure_quotient_rank_zero_selmer_package_index.json" in paths
    assert (
        "results/closure_quotient_rank_zero_selmer_package_materialization.json"
        in paths
    )
    assert "results/closure_quotient_rank_zero_selmer_transcript_intake.json" in paths
    assert (
        "results/closure_quotient_rank_zero_selmer_transcript_template_index.json"
        in paths
    )
    assert "results/closure_quotient_rank_zero_selmer_local_supports.json" in paths
    assert "results/closure_quotient_rank_zero_selmer_coprime_supports.json" in paths
    assert "results/closure_quotient_rank_zero_selmer_odd_prime_cases.json" in paths
    assert (
        "results/closure_quotient_rank_zero_selmer_odd_prime_valuations.json"
        in paths
    )
    assert (
        "results/closure_quotient_rank_zero_selmer_odd_prime_lemma_queue.json"
        in paths
    )
    assert (
        "results/closure_quotient_rank_zero_selmer_odd_prime_reduction_shapes.json"
        in paths
    )
    assert (
        "results/closure_quotient_rank_zero_selmer_odd_prime_local_image_schemas.json"
        in paths
    )
    assert (
        "results/closure_quotient_rank_zero_selmer_odd_prime_tangent_one_normal_forms.json"
        in paths
    )
    assert (
        "results/closure_quotient_rank_zero_selmer_tangent_one_unit_branch.json"
        in paths
    )
    assert (
        "results/closure_quotient_rank_zero_selmer_tangent_one_nonnode_branches.json"
        in paths
    )
    assert (
        "results/closure_quotient_rank_zero_selmer_tangent_one_node_values.json"
        in paths
    )
    assert (
        "results/closure_quotient_rank_zero_selmer_tangent_one_punctured_nodes.json"
        in paths
    )
    assert (
        "results/closure_quotient_rank_zero_selmer_tangent_one_reduction_partition.json"
        in paths
    )
    assert (
        "results/closure_quotient_rank_zero_selmer_tangent_minus_one_normal_forms.json"
        in paths
    )
    assert (
        "results/closure_quotient_rank_zero_selmer_tangent_minus_one_nonnode_branches.json"
        in paths
    )
    assert (
        "results/closure_quotient_rank_zero_selmer_tangent_minus_one_node_values.json"
        in paths
    )
    assert (
        "results/closure_quotient_rank_zero_selmer_tangent_minus_one_punctured_nodes.json"
        in paths
    )
    assert (
        "results/closure_quotient_rank_zero_selmer_tangent_minus_one_reduction_partition.json"
        in paths
    )
    for package_id in [
        "rank-zero-selmer-AA-kernel-minus-p",
        "rank-zero-selmer-AA-kernel-neg-2sqrt-q",
        "rank-zero-selmer-AA-kernel-pos-2sqrt-q",
        "rank-zero-selmer-AA-BB-kernel-minus-p",
        "rank-zero-selmer-AA-BB-kernel-neg-2sqrt-q",
        "rank-zero-selmer-AA-BB-kernel-pos-2sqrt-q",
        "rank-zero-selmer-BB-kernel-minus-p",
        "rank-zero-selmer-BB-kernel-neg-2sqrt-q",
        "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
    ]:
        assert (
            f"results/closure_quotient_rank_zero_selmer_packages/{package_id}.json"
            in paths
        )
        assert (
            f"results/closure_quotient_rank_zero_selmer_packages/{package_id}.md"
            in paths
        )
    assert "results/sage_rankzero_frontier_recheck_s13_20_t120.jsonl" in paths
    assert "results/sage_rankzero_frontier_recheck_1625_5643_AA_s20_40_t600.jsonl" in paths
    assert "results/sage_rankzero_frontier_recheck_567_3757_BB_s13_20_t120.jsonl" in paths
    assert "results/sage_rankzero_frontier_recheck_5075_17901_AA_s13_20_t120.jsonl" in paths
    assert "results/sage_rankzero_frontier_recheck_8075_8613_AA_s13_20_t120.jsonl" in paths
    assert "results/sage_rankzero_frontier_recheck_391_9009_BB_s13_20_t120.jsonl" in paths
    assert "results/sage_rankzero_frontier_recheck_209_21735_BB_s13_20_t120.jsonl" in paths
    assert "results/sage_rankzero_frontier_recheck_5083_12825_BB_s13_20_t120.jsonl" in paths
    assert "results/sage_rankzero_frontier_recheck_5301_38675_BB_s13_20_t120.jsonl" in paths
    assert "results/sage_rank1_frontier_recheck_209_5355_BB_s13_20_t120.jsonl" in paths
    assert (
        "results/sage_even_gap4_frontier_recheck_1449_12155_BB_s13_20_t120.jsonl"
        in paths
    )
    assert "results/mixed_closure_rank_zero_frontier_queue.json" in paths
    assert "results/mixed_closure_non_rankzero_frontier_queue.json" in paths
    assert "results/mixed_closure_residual_frontier_strategy_audit.json" in paths
    assert "results/mixed_closure_frontier_handoff_audit.json" in paths
    assert "results/mixed_closure_frontier_strictification_queue.json" in paths
    assert "results/mixed_closure_frontier_strictification_attempt_audit.json" in paths
    assert "results/mixed_closure_frontier_escalation_queue.json" in paths
    assert (
        "results/priority_005_1625_5643_AA_covers_4_3_twodescent20_probe.json"
        in paths
    )
    assert (
        "results/priority_005_1625_5643_AA_rank_methods_t90_twodescent20.json"
        in paths
    )
    assert (
        "results/mixed_closure_rank_zero_frontier_batch_rank_methods_t45.json"
        in paths
    )
    assert "results/mixed_closure_frontier_next_action_audit.json" in paths
    assert (
        "results/priority_006_567_3757_BB_rank_methods_t600_twodescent40.json"
        in paths
    )
    assert (
        "results/priority_009_5075_17901_AA_rank_methods_t600_twodescent40.json"
        in paths
    )
    assert (
        "results/priority_012_8075_8613_AA_rank_methods_t600_twodescent40.json"
        in paths
    )
    assert (
        "results/priority_013_391_9009_BB_rank_methods_t600_twodescent40.json"
        in paths
    )
    assert (
        "results/priority_017_209_21735_BB_rank_methods_t600_twodescent40.json"
        in paths
    )
    assert (
        "results/priority_024_5083_12825_BB_rank_methods_t600_twodescent40.json"
        in paths
    )
    assert (
        "results/priority_025_5301_38675_BB_rank_methods_t600_twodescent40.json"
        in paths
    )
    assert "results/priority_005_1625_5643_AA_mwrank_rank_probe.json" in paths
    assert "results/priority_006_567_3757_BB_mwrank_rank_probe.json" in paths
    assert "results/priority_009_5075_17901_AA_mwrank_rank_probe.json" in paths
    assert "results/priority_012_8075_8613_AA_mwrank_rank_probe.json" in paths
    assert "results/priority_013_391_9009_BB_mwrank_rank_probe.json" in paths
    assert "results/priority_017_209_21735_BB_mwrank_rank_probe.json" in paths
    assert "results/priority_024_5083_12825_BB_mwrank_rank_probe.json" in paths
    assert "results/priority_025_5301_38675_BB_mwrank_rank_probe.json" in paths
    assert (
        "results/priority_005_1625_5643_AA_mwrank_b20_x30_t60_probe.json"
        in paths
    )
    assert "results/priority_005_1625_5643_AA_cover_tool_capabilities.json" in paths
    assert (
        "results/priority_005_1625_5643_AA_external_cover_descent_route.json"
        in paths
    )
    assert (
        "results/priority_005_1625_5643_AA_external_cover_certificate_intake.json"
        in paths
    )
    assert (
        "results/priority_005_1625_5643_AA_external_cover_certificate_template.json"
        in paths
    )
    assert (
        "results/mixed_closure_external_cover_certificate_frontier_intake.json"
        in paths
    )
    assert (
        "results/mixed_closure_external_cover_certificate_template_index.json"
        in paths
    )
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_001_115_297_AA_covers_3_4_sage_probe.json"
    ) in paths
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_001_115_297_AA_covers_3_4_map_verify.json"
    ) in paths
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_001_115_297_AA_covers_3_4_local_witnesses.json"
    ) in paths
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_005_1625_5643_AA_covers_4_3.json"
    ) in paths
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_005_1625_5643_AA_covers_4_3.sage"
    ) in paths
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_005_1625_5643_AA_covers_4_3.magma"
    ) in paths
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_005_1625_5643_AA_covers_4_3_sage_probe.json"
    ) in paths
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_005_1625_5643_AA_covers_4_3_map_verify.json"
    ) in paths
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_005_1625_5643_AA_covers_4_3_local_witnesses.json"
    ) in paths
    for name in [
        "priority_006_567_3757_BB_covers_4_3",
        "priority_009_5075_17901_AA_covers_4_3",
        "priority_012_8075_8613_AA_covers_4_3",
        "priority_013_391_9009_BB_covers_4_3",
        "priority_017_209_21735_BB_covers_3_4",
        "priority_024_5083_12825_BB_covers_3_4",
        "priority_025_5301_38675_BB_covers_4_3",
    ]:
        assert f"results/mixed_closure_residual_handoffs/{name}.json" in paths
        assert f"results/mixed_closure_residual_handoffs/{name}.sage" in paths
        assert f"results/mixed_closure_residual_handoffs/{name}.magma" in paths
        assert (
            f"results/mixed_closure_residual_handoffs/{name}_sage_probe.json"
            in paths
        )
        assert (
            f"results/mixed_closure_residual_handoffs/{name}_map_verify.json"
            in paths
        )
        assert (
            f"results/mixed_closure_residual_handoffs/{name}_local_witnesses.json"
            in paths
        )
    for name in [
        "priority_008_209_5355_BB_covers_5_4_3",
        "priority_011_1449_12155_BB_covers_5_6_3_4",
    ]:
        assert f"results/mixed_closure_residual_handoffs/{name}.json" in paths
        assert f"results/mixed_closure_residual_handoffs/{name}.sage" in paths
        assert f"results/mixed_closure_residual_handoffs/{name}.magma" in paths
        assert (
            f"results/mixed_closure_residual_handoffs/{name}_sage_probe.json"
            in paths
        )
        assert (
            f"results/mixed_closure_residual_handoffs/{name}_map_verify.json"
            in paths
        )
        assert (
            f"results/mixed_closure_residual_handoffs/{name}_local_witnesses.json"
            in paths
        )


def test_parse_required_artifact_requires_category_and_path() -> None:
    assert parse_required_artifact("script:scripts/theory/x.py") == Artifact(
        "script", "scripts/theory/x.py"
    )


def test_artifact_cli_strict_exits_nonzero_when_required_file_is_missing(
    tmp_path: Path,
) -> None:
    out = tmp_path / "audit.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_partial_artifacts.py",
            "--root",
            str(tmp_path),
            "--require",
            "script:scripts/theory/missing.py",
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "ready=False" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["missing_files"] == [
        {"category": "script", "path": "scripts/theory/missing.py"}
    ]


def test_write_json_writes_sorted_artifact_audit(tmp_path: Path) -> None:
    out = tmp_path / "audit.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
