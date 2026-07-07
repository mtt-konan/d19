#!/usr/bin/env python3
"""Audit artifact presence for the closure-quotient partial-result package."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This checks artifact presence for the closure-quotient partial-result "
    "package. It does not check mathematical truth."
)


@dataclass(frozen=True)
class Artifact:
    category: str
    path: str


DEFAULT_REQUIRED_ARTIFACTS: tuple[Artifact, ...] = (
    Artifact("script", "scripts/theory/rank_mixed_closure_curves.py"),
    Artifact("script", "scripts/theory/audit_mixed_closure_rank0_certificates.py"),
    Artifact("script", "scripts/theory/audit_mixed_closure_even_model_identities.py"),
    Artifact("script", "scripts/theory/summarize_mixed_closure_residual_covers.py"),
    Artifact("script", "scripts/theory/audit_mixed_closure_residual_evidence.py"),
    Artifact("script", "scripts/theory/pari_ell2cover_mixed_residuals.py"),
    Artifact("script", "scripts/theory/pari_bsd_mixed_closure_residuals.py"),
    Artifact("script", "scripts/theory/sage_diagnose_mixed_closure_residuals.py"),
    Artifact("script", "scripts/theory/prioritize_mixed_closure_residual_covers.py"),
    Artifact("script", "scripts/theory/export_mixed_closure_residual_handoff.py"),
    Artifact("script", "scripts/theory/sage_probe_mixed_closure_handoff.py"),
    Artifact("script", "scripts/theory/sage_verify_mixed_closure_handoff_maps.py"),
    Artifact("script", "scripts/theory/sage_verify_mixed_closure_residual_cover_maps.py"),
    Artifact("script", "scripts/theory/sage_audit_mixed_closure_rank0_torsion_preimages.py"),
    Artifact("script", "scripts/theory/audit_mixed_closure_bsd_conditional_no_points.py"),
    Artifact("script", "scripts/theory/audit_mixed_closure_residual_open_frontier.py"),
    Artifact("script", "scripts/theory/summarize_mixed_closure_rank_zero_frontier.py"),
    Artifact("script", "scripts/theory/summarize_mixed_closure_non_rankzero_frontier.py"),
    Artifact("script", "scripts/theory/audit_mixed_closure_residual_frontier_strategy.py"),
    Artifact("script", "scripts/theory/audit_mixed_closure_frontier_handoffs.py"),
    Artifact("script", "scripts/theory/summarize_mixed_closure_frontier_strictification.py"),
    Artifact("script", "scripts/theory/audit_mixed_closure_frontier_strictification_attempts.py"),
    Artifact("script", "scripts/theory/sage_probe_mixed_closure_rank_methods.py"),
    Artifact("script", "scripts/theory/batch_sage_probe_mixed_closure_rank_methods.py"),
    Artifact("script", "scripts/theory/audit_mixed_closure_frontier_next_actions.py"),
    Artifact("script", "scripts/theory/audit_mixed_closure_frontier_escalation_queue.py"),
    Artifact("script", "scripts/theory/probe_mwrank_mixed_closure_rank.py"),
    Artifact("script", "scripts/theory/audit_sage_cover_tool_capabilities.py"),
    Artifact("script", "scripts/theory/audit_external_cover_descent_route.py"),
    Artifact("script", "scripts/theory/audit_external_cover_certificate_intake.py"),
    Artifact(
        "script",
        "scripts/theory/audit_external_cover_certificate_frontier_intake.py",
    ),
    Artifact("script", "scripts/theory/export_external_cover_descent_packages.py"),
    Artifact("script", "scripts/theory/sage_probe_mixed_closure_local_witnesses.py"),
    Artifact("script", "scripts/theory/summarize_mixed_closure_residual_selmer_gaps.py"),
    Artifact("script", "scripts/theory/audit_mixed_closure_residual_language.py"),
    Artifact("script", "scripts/theory/audit_mixed_closure_priority_handoffs.py"),
    Artifact("script", "scripts/theory/audit_closure_quotient_paper_claims.py"),
    Artifact("script", "scripts/theory/audit_closure_quotient_paper_structure.py"),
    Artifact("script", "scripts/theory/audit_closure_quotient_partial_dependencies.py"),
    Artifact("script", "scripts/theory/summarize_closure_quotient_ray_ledger.py"),
    Artifact("script", "scripts/theory/summarize_closure_quotient_lambda_frontier.py"),
    Artifact("script", "scripts/theory/audit_closure_quotient_ray_scale_invariance.py"),
    Artifact(
        "script",
        "scripts/theory/summarize_closure_quotient_rank_zero_family_candidates.py",
    ),
    Artifact(
        "script",
        "scripts/theory/summarize_closure_quotient_rank_zero_primitive_models.py",
    ),
    Artifact(
        "script",
        "scripts/theory/summarize_closure_quotient_rank_zero_proof_seeds.py",
    ),
    Artifact(
        "script",
        "scripts/theory/summarize_closure_quotient_rank_zero_certifying_invariants.py",
    ),
    Artifact(
        "script",
        "scripts/theory/audit_closure_quotient_rank_zero_forced_torsion.py",
    ),
    Artifact(
        "script",
        "scripts/theory/audit_closure_quotient_rank_zero_seed_identities.py",
    ),
    Artifact(
        "script",
        "scripts/theory/audit_closure_quotient_rank_zero_family_obligations.py",
    ),
    Artifact(
        "script",
        "scripts/theory/audit_closure_quotient_rank_zero_symbolic_descent_inputs.py",
    ),
    Artifact(
        "script",
        "scripts/theory/audit_closure_quotient_rank_zero_isogeny_templates.py",
    ),
    Artifact(
        "script",
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_obligations.py",
    ),
    Artifact(
        "script",
        "scripts/theory/export_closure_quotient_rank_zero_selmer_package_index.py",
    ),
    Artifact(
        "script",
        "scripts/theory/materialize_closure_quotient_rank_zero_selmer_packages.py",
    ),
    Artifact(
        "script",
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_transcript_intake.py",
    ),
    Artifact(
        "script",
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_local_supports.py",
    ),
    Artifact(
        "script",
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_coprime_supports.py",
    ),
    Artifact(
        "script",
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_cases.py",
    ),
    Artifact(
        "script",
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_valuations.py",
    ),
    Artifact(
        "script",
        "scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_lemma_queue.py",
    ),
    Artifact(
        "script",
        "scripts/theory/summarize_closure_quotient_root_number_lambda_triage.py",
    ),
    Artifact(
        "script",
        "scripts/theory/summarize_closure_quotient_root_number_proof_seeds.py",
    ),
    Artifact(
        "script",
        "scripts/theory/summarize_closure_quotient_two_cover_lambda_frontier.py",
    ),
    Artifact(
        "script",
        "scripts/theory/summarize_closure_quotient_two_cover_proof_seeds.py",
    ),
    Artifact("script", "scripts/theory/audit_closure_quotient_lambda_route_partition.py"),
    Artifact("script", "scripts/theory/audit_closure_quotient_lambda_mainline.py"),
    Artifact("script", "scripts/theory/audit_closure_quotient_lambda_proof_seed_coverage.py"),
    Artifact(
        "script",
        "scripts/theory/audit_closure_quotient_lambda_convergence_priorities.py",
    ),
    Artifact("script", "scripts/theory/summarize_closure_quotient_partial_result.py"),
    Artifact("script", "scripts/theory/audit_closure_quotient_partial_artifacts.py"),
    Artifact("test", "tests/test_mixed_closure_rank_cli.py"),
    Artifact("test", "tests/test_mixed_closure_rank0_certificate_audit.py"),
    Artifact("test", "tests/test_mixed_closure_even_model_identity_audit.py"),
    Artifact("test", "tests/test_mixed_closure_residual_cover_summary.py"),
    Artifact("test", "tests/test_mixed_closure_residual_evidence_audit.py"),
    Artifact("test", "tests/test_pari_ell2cover_mixed_residuals.py"),
    Artifact("test", "tests/test_pari_bsd_mixed_closure_residuals.py"),
    Artifact("test", "tests/test_sage_diagnose_mixed_closure_residuals.py"),
    Artifact("test", "tests/test_prioritize_mixed_closure_residual_covers.py"),
    Artifact("test", "tests/test_mixed_closure_residual_handoff.py"),
    Artifact("test", "tests/test_sage_probe_mixed_closure_handoff.py"),
    Artifact("test", "tests/test_sage_verify_mixed_closure_handoff_maps.py"),
    Artifact("test", "tests/test_sage_verify_mixed_closure_residual_cover_maps.py"),
    Artifact("test", "tests/test_sage_audit_mixed_closure_rank0_torsion_preimages.py"),
    Artifact("test", "tests/test_mixed_closure_bsd_conditional_no_point_audit.py"),
    Artifact("test", "tests/test_mixed_closure_residual_open_frontier_audit.py"),
    Artifact("test", "tests/test_mixed_closure_rank_zero_frontier_queue.py"),
    Artifact("test", "tests/test_mixed_closure_non_rankzero_frontier_queue.py"),
    Artifact("test", "tests/test_mixed_closure_residual_frontier_strategy.py"),
    Artifact("test", "tests/test_mixed_closure_frontier_handoff_audit.py"),
    Artifact("test", "tests/test_mixed_closure_frontier_strictification_queue.py"),
    Artifact("test", "tests/test_mixed_closure_frontier_strictification_attempts.py"),
    Artifact("test", "tests/test_sage_probe_mixed_closure_rank_methods.py"),
    Artifact("test", "tests/test_batch_sage_probe_mixed_closure_rank_methods.py"),
    Artifact("test", "tests/test_mixed_closure_frontier_next_action_audit.py"),
    Artifact("test", "tests/test_mixed_closure_frontier_escalation_queue.py"),
    Artifact("test", "tests/test_probe_mwrank_mixed_closure_rank.py"),
    Artifact("test", "tests/test_audit_sage_cover_tool_capabilities.py"),
    Artifact("test", "tests/test_audit_external_cover_descent_route.py"),
    Artifact("test", "tests/test_audit_external_cover_certificate_intake.py"),
    Artifact(
        "test",
        "tests/test_audit_external_cover_certificate_frontier_intake.py",
    ),
    Artifact("test", "tests/test_export_external_cover_descent_packages.py"),
    Artifact("test", "tests/test_sage_probe_mixed_closure_local_witnesses.py"),
    Artifact("test", "tests/test_mixed_closure_residual_selmer_gap_ledger.py"),
    Artifact("test", "tests/test_mixed_closure_residual_language_audit.py"),
    Artifact("test", "tests/test_mixed_closure_priority_handoff_audit.py"),
    Artifact("test", "tests/test_closure_quotient_paper_claim_audit.py"),
    Artifact("test", "tests/test_closure_quotient_paper_structure_audit.py"),
    Artifact("test", "tests/test_closure_quotient_partial_dependency_audit.py"),
    Artifact("test", "tests/test_closure_quotient_ray_ledger.py"),
    Artifact("test", "tests/test_closure_quotient_lambda_frontier.py"),
    Artifact("test", "tests/test_closure_quotient_ray_scale_invariance.py"),
    Artifact("test", "tests/test_closure_quotient_rank_zero_family_candidates.py"),
    Artifact("test", "tests/test_closure_quotient_rank_zero_primitive_models.py"),
    Artifact("test", "tests/test_closure_quotient_rank_zero_proof_seeds.py"),
    Artifact(
        "test",
        "tests/test_closure_quotient_rank_zero_certifying_invariants.py",
    ),
    Artifact("test", "tests/test_closure_quotient_rank_zero_forced_torsion.py"),
    Artifact("test", "tests/test_closure_quotient_rank_zero_seed_identities.py"),
    Artifact("test", "tests/test_closure_quotient_rank_zero_family_obligations.py"),
    Artifact("test", "tests/test_closure_quotient_rank_zero_symbolic_descent_inputs.py"),
    Artifact("test", "tests/test_closure_quotient_rank_zero_isogeny_templates.py"),
    Artifact("test", "tests/test_closure_quotient_rank_zero_selmer_obligations.py"),
    Artifact("test", "tests/test_closure_quotient_rank_zero_selmer_package_index.py"),
    Artifact(
        "test",
        "tests/test_closure_quotient_rank_zero_selmer_package_materialization.py",
    ),
    Artifact(
        "test",
        "tests/test_closure_quotient_rank_zero_selmer_transcript_intake.py",
    ),
    Artifact(
        "test",
        "tests/test_closure_quotient_rank_zero_selmer_local_supports.py",
    ),
    Artifact(
        "test",
        "tests/test_closure_quotient_rank_zero_selmer_coprime_supports.py",
    ),
    Artifact(
        "test",
        "tests/test_closure_quotient_rank_zero_selmer_odd_prime_cases.py",
    ),
    Artifact(
        "test",
        "tests/test_closure_quotient_rank_zero_selmer_odd_prime_valuations.py",
    ),
    Artifact(
        "test",
        "tests/test_closure_quotient_rank_zero_selmer_odd_prime_lemma_queue.py",
    ),
    Artifact("test", "tests/test_closure_quotient_root_number_lambda_triage.py"),
    Artifact("test", "tests/test_closure_quotient_root_number_proof_seeds.py"),
    Artifact("test", "tests/test_closure_quotient_two_cover_lambda_frontier.py"),
    Artifact("test", "tests/test_closure_quotient_two_cover_proof_seeds.py"),
    Artifact("test", "tests/test_closure_quotient_lambda_route_partition.py"),
    Artifact("test", "tests/test_closure_quotient_lambda_mainline_gate.py"),
    Artifact("test", "tests/test_closure_quotient_lambda_proof_seed_coverage.py"),
    Artifact("test", "tests/test_closure_quotient_lambda_convergence_priorities.py"),
    Artifact("test", "tests/test_summarize_closure_quotient_partial_result.py"),
    Artifact("test", "tests/test_closure_quotient_partial_artifacts.py"),
    Artifact("doc", "docs/CLOSURE_QUOTIENT_MAINLINE.md"),
    Artifact("doc", "docs/paper/CLOSURE_QUOTIENT_PARTIAL_RESULT.md"),
    Artifact("worklog", "docs/work-logs/294-tmp-mixed-closure-answer.md"),
    Artifact("worklog", "docs/work-logs/295-sage-mixed-closure-residual-rank-recheck.md"),
    Artifact("worklog", "docs/work-logs/296-mixed-closure-residual-cover-summary.md"),
    Artifact("worklog", "docs/work-logs/297-mixed-closure-cover-map-handoff.md"),
    Artifact("worklog", "docs/work-logs/298-mixed-closure-rank0-certificate-audit.md"),
    Artifact("worklog", "docs/work-logs/299-mixed-closure-pari-bsd-diagnostics.md"),
    Artifact("worklog", "docs/work-logs/300-closure-quotient-paper-claim-audit.md"),
    Artifact("worklog", "docs/work-logs/301-mixed-closure-residual-handoff.md"),
    Artifact("worklog", "docs/work-logs/302-mixed-closure-even-model-identity-audit.md"),
    Artifact("worklog", "docs/work-logs/303-mixed-closure-rank0-classification-detail-audit.md"),
    Artifact("worklog", "docs/work-logs/304-mixed-closure-residual-evidence-audit.md"),
    Artifact("worklog", "docs/work-logs/305-sage-residual-handoff-probe.md"),
    Artifact("worklog", "docs/work-logs/306-mixed-residual-cover-priority-queue.md"),
    Artifact("worklog", "docs/work-logs/307-priority-handoff-export-and-second-sage-probe.md"),
    Artifact("worklog", "docs/work-logs/308-priority-queue-paper-claim-gate.md"),
    Artifact("worklog", "docs/work-logs/309-residual-language-overclaim-audit.md"),
    Artifact("worklog", "docs/work-logs/310-language-audit-paper-claim-gate.md"),
    Artifact("worklog", "docs/work-logs/311-closure-quotient-partial-result-summary.md"),
    Artifact("worklog", "docs/work-logs/312-closure-quotient-partial-artifact-audit.md"),
    Artifact("worklog", "docs/work-logs/313-priority-handoff-probe-audit.md"),
    Artifact("worklog", "docs/work-logs/314-sage-cover-map-identity-verification.md"),
    Artifact("worklog", "docs/work-logs/315-sage-local-witness-probe.md"),
    Artifact("worklog", "docs/work-logs/316-all-residual-local-witnesses.md"),
    Artifact("worklog", "docs/work-logs/317-residual-local-witness-paper-claim-gate.md"),
    Artifact("worklog", "docs/work-logs/318-residual-selmer-gap-ledger.md"),
    Artifact("worklog", "docs/work-logs/319-all-residual-cover-map-verification.md"),
    Artifact("worklog", "docs/work-logs/320-residual-selmer-gap-frontier-split.md"),
    Artifact("worklog", "docs/work-logs/321-rank0-torsion-preimage-audit.md"),
    Artifact("worklog", "docs/work-logs/322-bsd-conditional-no-point-audit.md"),
    Artifact("worklog", "docs/work-logs/323-residual-open-frontier-audit.md"),
    Artifact("worklog", "docs/work-logs/324-rank-zero-frontier-queue.md"),
    Artifact("worklog", "docs/work-logs/325-non-rankzero-frontier-queue.md"),
    Artifact("worklog", "docs/work-logs/326-rank1-frontier-recheck.md"),
    Artifact("worklog", "docs/work-logs/327-even-gap4-frontier-recheck.md"),
    Artifact("worklog", "docs/work-logs/328-rankzero-frontier-recheck-567-3757.md"),
    Artifact("worklog", "docs/work-logs/329-rankzero-frontier-recheck-5075-17901.md"),
    Artifact("worklog", "docs/work-logs/330-rankzero-frontier-long-recheck-1625-5643.md"),
    Artifact("worklog", "docs/work-logs/331-rankzero-frontier-recheck-8075-8613.md"),
    Artifact("worklog", "docs/work-logs/332-rankzero-frontier-recheck-391-9009.md"),
    Artifact("worklog", "docs/work-logs/333-rankzero-frontier-recheck-209-21735.md"),
    Artifact("worklog", "docs/work-logs/334-rankzero-frontier-recheck-5083-12825.md"),
    Artifact("worklog", "docs/work-logs/335-rankzero-frontier-recheck-5301-38675.md"),
    Artifact("worklog", "docs/work-logs/336-residual-frontier-strategy-audit.md"),
    Artifact("worklog", "docs/work-logs/337-frontier-target-handoff-1625-5643.md"),
    Artifact("worklog", "docs/work-logs/338-all-rankzero-frontier-handoffs.md"),
    Artifact("worklog", "docs/work-logs/339-non-rankzero-frontier-handoffs.md"),
    Artifact("worklog", "docs/work-logs/340-frontier-handoff-audit.md"),
    Artifact("worklog", "docs/work-logs/341-frontier-strictification-queue.md"),
    Artifact("worklog", "docs/work-logs/342-frontier-strictification-attempt.md"),
    Artifact("worklog", "docs/work-logs/343-frontier-rank-method-probe.md"),
    Artifact("worklog", "docs/work-logs/344-frontier-batch-rank-method-probe.md"),
    Artifact("worklog", "docs/work-logs/345-frontier-next-action-audit.md"),
    Artifact("worklog", "docs/work-logs/346-rankzero-frontier-long-recheck-567-3757.md"),
    Artifact("worklog", "docs/work-logs/347-rankzero-frontier-long-recheck-5075-17901.md"),
    Artifact("worklog", "docs/work-logs/348-rankzero-frontier-long-recheck-8075-8613.md"),
    Artifact("worklog", "docs/work-logs/349-rankzero-frontier-long-recheck-391-9009.md"),
    Artifact("worklog", "docs/work-logs/350-rankzero-frontier-long-recheck-209-21735.md"),
    Artifact("worklog", "docs/work-logs/351-rankzero-frontier-long-recheck-5083-12825.md"),
    Artifact("worklog", "docs/work-logs/352-rankzero-frontier-long-recheck-5301-38675.md"),
    Artifact("worklog", "docs/work-logs/353-frontier-escalation-queue.md"),
    Artifact("worklog", "docs/work-logs/354-mwrank-frontier-rank-probe.md"),
    Artifact("worklog", "docs/work-logs/355-sage-cover-tool-capability-audit.md"),
    Artifact("worklog", "docs/work-logs/356-external-cover-descent-route-audit.md"),
    Artifact("worklog", "docs/work-logs/357-external-cover-certificate-intake.md"),
    Artifact(
        "worklog",
        "docs/work-logs/358-frontier-external-certificate-intake.md",
    ),
    Artifact(
        "worklog",
        "docs/work-logs/359-summary-gate-external-certificate-intake.md",
    ),
    Artifact("worklog", "docs/work-logs/360-paper-structure-audit.md"),
    Artifact("worklog", "docs/work-logs/361-partial-result-dependency-audit.md"),
    Artifact("worklog", "docs/work-logs/362-external-cover-descent-packages.md"),
    Artifact("worklog", "docs/work-logs/363-closure-quotient-ray-ledger.md"),
    Artifact("worklog", "docs/work-logs/364-closure-quotient-lambda-frontier.md"),
    Artifact("worklog", "docs/work-logs/365-closure-quotient-ray-scale-invariance.md"),
    Artifact("worklog", "docs/work-logs/366-rank-zero-family-candidates.md"),
    Artifact("worklog", "docs/work-logs/367-rank-zero-primitive-models.md"),
    Artifact("worklog", "docs/work-logs/368-root-number-lambda-triage.md"),
    Artifact("worklog", "docs/work-logs/369-two-cover-lambda-frontier.md"),
    Artifact("worklog", "docs/work-logs/370-lambda-route-partition-audit.md"),
    Artifact("worklog", "docs/work-logs/371-lambda-mainline-audit.md"),
    Artifact("worklog", "docs/work-logs/372-rank-zero-proof-seeds.md"),
    Artifact("worklog", "docs/work-logs/373-rank-zero-seed-identities.md"),
    Artifact("worklog", "docs/work-logs/374-rank-zero-certifying-invariants.md"),
    Artifact("worklog", "docs/work-logs/375-rank-zero-forced-torsion.md"),
    Artifact("worklog", "docs/work-logs/376-root-number-proof-seeds.md"),
    Artifact("worklog", "docs/work-logs/377-two-cover-proof-seeds.md"),
    Artifact("worklog", "docs/work-logs/378-lambda-proof-seed-coverage.md"),
    Artifact("worklog", "docs/work-logs/379-lambda-mainline-proof-seed-gate.md"),
    Artifact("worklog", "docs/work-logs/380-lambda-convergence-priorities.md"),
    Artifact("worklog", "docs/work-logs/381-rank-zero-family-obligations.md"),
    Artifact("worklog", "docs/work-logs/382-rank-zero-symbolic-descent-inputs.md"),
    Artifact("worklog", "docs/work-logs/383-rank-zero-isogeny-templates.md"),
    Artifact("worklog", "docs/work-logs/384-rank-zero-selmer-obligations.md"),
    Artifact("worklog", "docs/work-logs/385-rank-zero-selmer-package-index.md"),
    Artifact("worklog", "docs/work-logs/386-rank-zero-selmer-package-materialization.md"),
    Artifact("worklog", "docs/work-logs/387-rank-zero-selmer-transcript-intake.md"),
    Artifact("worklog", "docs/work-logs/388-lambda-mainline-transcript-intake-gate.md"),
    Artifact("worklog", "docs/work-logs/389-rank-zero-selmer-local-supports.md"),
    Artifact("worklog", "docs/work-logs/390-rank-zero-selmer-coprime-supports.md"),
    Artifact("worklog", "docs/work-logs/391-rank-zero-selmer-odd-prime-cases.md"),
    Artifact(
        "worklog",
        "docs/work-logs/392-rank-zero-selmer-odd-prime-valuations.md",
    ),
    Artifact(
        "worklog",
        "docs/work-logs/393-rank-zero-selmer-odd-prime-lemma-queue.md",
    ),
    Artifact("result", "results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl"),
    Artifact("result", "results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl"),
    Artifact("result", "results/mixed_closure_rank_summary.json"),
    Artifact("result", "results/mixed_closure_rank0_certificate_audit.json"),
    Artifact("result", "results/mixed_closure_even_model_identity_audit.json"),
    Artifact("result", "results/mixed_closure_aabb_residual_cover_summary.json"),
    Artifact("result", "results/mixed_closure_aabb_residual_evidence_audit.json"),
    Artifact("result", "results/mixed_closure_aabb_residual_cover_priorities.json"),
    Artifact("result", "results/mixed_closure_priority_handoff_audit_top4.json"),
    Artifact("result", "results/mixed_closure_aabb_residual_local_witnesses.json"),
    Artifact("result", "results/mixed_closure_residual_selmer_gap_ledger.json"),
    Artifact("result", "results/mixed_closure_residual_cover_map_verify.json"),
    Artifact("result", "results/mixed_closure_rank0_sha2_torsion_preimage_audit.json"),
    Artifact("result", "results/mixed_closure_bsd_conditional_no_point_audit.json"),
    Artifact("result", "results/mixed_closure_residual_open_frontier_audit.json"),
    Artifact("result", "results/sage_rankzero_frontier_recheck_s13_20_t120.jsonl"),
    Artifact(
        "result",
        "results/sage_rankzero_frontier_recheck_1625_5643_AA_s20_40_t600.jsonl",
    ),
    Artifact(
        "result",
        "results/sage_rankzero_frontier_recheck_567_3757_BB_s13_20_t120.jsonl",
    ),
    Artifact(
        "result",
        "results/sage_rankzero_frontier_recheck_5075_17901_AA_s13_20_t120.jsonl",
    ),
    Artifact(
        "result",
        "results/sage_rankzero_frontier_recheck_8075_8613_AA_s13_20_t120.jsonl",
    ),
    Artifact(
        "result",
        "results/sage_rankzero_frontier_recheck_391_9009_BB_s13_20_t120.jsonl",
    ),
    Artifact(
        "result",
        "results/sage_rankzero_frontier_recheck_209_21735_BB_s13_20_t120.jsonl",
    ),
    Artifact(
        "result",
        "results/sage_rankzero_frontier_recheck_5083_12825_BB_s13_20_t120.jsonl",
    ),
    Artifact(
        "result",
        "results/sage_rankzero_frontier_recheck_5301_38675_BB_s13_20_t120.jsonl",
    ),
    Artifact(
        "result",
        "results/sage_rank1_frontier_recheck_209_5355_BB_s13_20_t120.jsonl",
    ),
    Artifact(
        "result",
        "results/sage_even_gap4_frontier_recheck_1449_12155_BB_s13_20_t120.jsonl",
    ),
    Artifact("result", "results/mixed_closure_rank_zero_frontier_queue.json"),
    Artifact("result", "results/mixed_closure_non_rankzero_frontier_queue.json"),
    Artifact("result", "results/mixed_closure_residual_frontier_strategy_audit.json"),
    Artifact("result", "results/mixed_closure_frontier_handoff_audit.json"),
    Artifact("result", "results/mixed_closure_frontier_strictification_queue.json"),
    Artifact("result", "results/mixed_closure_frontier_strictification_attempt_audit.json"),
    Artifact("result", "results/mixed_closure_frontier_escalation_queue.json"),
    Artifact(
        "result",
        "results/priority_005_1625_5643_AA_covers_4_3_twodescent20_probe.json",
    ),
    Artifact(
        "result",
        "results/priority_005_1625_5643_AA_rank_methods_t90_twodescent20.json",
    ),
    Artifact(
        "result",
        "results/mixed_closure_rank_zero_frontier_batch_rank_methods_t45.json",
    ),
    Artifact("result", "results/mixed_closure_frontier_next_action_audit.json"),
    Artifact(
        "result",
        "results/priority_006_567_3757_BB_rank_methods_t600_twodescent40.json",
    ),
    Artifact(
        "result",
        "results/priority_009_5075_17901_AA_rank_methods_t600_twodescent40.json",
    ),
    Artifact(
        "result",
        "results/priority_012_8075_8613_AA_rank_methods_t600_twodescent40.json",
    ),
    Artifact(
        "result",
        "results/priority_013_391_9009_BB_rank_methods_t600_twodescent40.json",
    ),
    Artifact(
        "result",
        "results/priority_017_209_21735_BB_rank_methods_t600_twodescent40.json",
    ),
    Artifact(
        "result",
        "results/priority_024_5083_12825_BB_rank_methods_t600_twodescent40.json",
    ),
    Artifact(
        "result",
        "results/priority_025_5301_38675_BB_rank_methods_t600_twodescent40.json",
    ),
    Artifact("result", "results/priority_005_1625_5643_AA_mwrank_rank_probe.json"),
    Artifact("result", "results/priority_006_567_3757_BB_mwrank_rank_probe.json"),
    Artifact("result", "results/priority_009_5075_17901_AA_mwrank_rank_probe.json"),
    Artifact("result", "results/priority_012_8075_8613_AA_mwrank_rank_probe.json"),
    Artifact("result", "results/priority_013_391_9009_BB_mwrank_rank_probe.json"),
    Artifact("result", "results/priority_017_209_21735_BB_mwrank_rank_probe.json"),
    Artifact("result", "results/priority_024_5083_12825_BB_mwrank_rank_probe.json"),
    Artifact("result", "results/priority_025_5301_38675_BB_mwrank_rank_probe.json"),
    Artifact(
        "result",
        "results/priority_005_1625_5643_AA_mwrank_b20_x30_t60_probe.json",
    ),
    Artifact(
        "result",
        "results/priority_005_1625_5643_AA_cover_tool_capabilities.json",
    ),
    Artifact(
        "result",
        "results/priority_005_1625_5643_AA_external_cover_descent_route.json",
    ),
    Artifact(
        "result",
        "results/priority_005_1625_5643_AA_external_cover_certificate_intake.json",
    ),
    Artifact(
        "result",
        "results/priority_005_1625_5643_AA_external_cover_certificate_template.json",
    ),
    Artifact(
        "result",
        "results/mixed_closure_external_cover_certificate_frontier_intake.json",
    ),
    Artifact(
        "result",
        "results/mixed_closure_external_cover_certificate_template_index.json",
    ),
    Artifact(
        "result",
        "results/mixed_closure_external_cover_descent_package_index.json",
    ),
    Artifact("result", "results/mixed_closure_residual_language_audit.json"),
    Artifact("result", "results/closure_quotient_paper_claim_audit.json"),
    Artifact("result", "results/closure_quotient_paper_structure_audit.json"),
    Artifact("result", "results/closure_quotient_partial_artifact_audit.json"),
    Artifact("result", "results/closure_quotient_partial_dependency_audit.json"),
    Artifact("result", "results/closure_quotient_ray_ledger.json"),
    Artifact("result", "results/closure_quotient_lambda_frontier.json"),
    Artifact("result", "results/closure_quotient_ray_scale_invariance_audit.json"),
    Artifact("result", "results/closure_quotient_rank_zero_family_candidates.json"),
    Artifact("result", "results/closure_quotient_rank_zero_primitive_models.json"),
    Artifact("result", "results/closure_quotient_rank_zero_proof_seeds.json"),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_certifying_invariants.json",
    ),
    Artifact("result", "results/closure_quotient_rank_zero_forced_torsion_audit.json"),
    Artifact("result", "results/closure_quotient_rank_zero_seed_identity_audit.json"),
    Artifact("result", "results/closure_quotient_rank_zero_family_obligations.json"),
    Artifact("result", "results/closure_quotient_rank_zero_symbolic_descent_inputs.json"),
    Artifact("result", "results/closure_quotient_rank_zero_isogeny_templates.json"),
    Artifact("result", "results/closure_quotient_rank_zero_selmer_obligations.json"),
    Artifact("result", "results/closure_quotient_rank_zero_selmer_package_index.json"),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_package_materialization.json",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_transcript_intake.json",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_transcript_template_index.json",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_local_supports.json",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_coprime_supports.json",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_odd_prime_cases.json",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_odd_prime_valuations.json",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_odd_prime_lemma_queue.json",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_packages/rank-zero-selmer-AA-kernel-minus-p.json",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_packages/rank-zero-selmer-AA-kernel-minus-p.md",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_packages/rank-zero-selmer-AA-kernel-neg-2sqrt-q.json",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_packages/rank-zero-selmer-AA-kernel-neg-2sqrt-q.md",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_packages/rank-zero-selmer-AA-kernel-pos-2sqrt-q.json",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_packages/rank-zero-selmer-AA-kernel-pos-2sqrt-q.md",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_packages/rank-zero-selmer-AA-BB-kernel-minus-p.json",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_packages/rank-zero-selmer-AA-BB-kernel-minus-p.md",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_packages/rank-zero-selmer-AA-BB-kernel-neg-2sqrt-q.json",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_packages/rank-zero-selmer-AA-BB-kernel-neg-2sqrt-q.md",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_packages/rank-zero-selmer-AA-BB-kernel-pos-2sqrt-q.json",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_packages/rank-zero-selmer-AA-BB-kernel-pos-2sqrt-q.md",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_packages/rank-zero-selmer-BB-kernel-minus-p.json",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_packages/rank-zero-selmer-BB-kernel-minus-p.md",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_packages/rank-zero-selmer-BB-kernel-neg-2sqrt-q.json",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_packages/rank-zero-selmer-BB-kernel-neg-2sqrt-q.md",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_packages/rank-zero-selmer-BB-kernel-pos-2sqrt-q.json",
    ),
    Artifact(
        "result",
        "results/closure_quotient_rank_zero_selmer_packages/rank-zero-selmer-BB-kernel-pos-2sqrt-q.md",
    ),
    Artifact("result", "results/closure_quotient_root_number_lambda_triage.json"),
    Artifact("result", "results/closure_quotient_root_number_proof_seeds.json"),
    Artifact("result", "results/closure_quotient_two_cover_lambda_frontier.json"),
    Artifact("result", "results/closure_quotient_two_cover_proof_seeds.json"),
    Artifact("result", "results/closure_quotient_lambda_route_partition_audit.json"),
    Artifact("result", "results/closure_quotient_lambda_mainline_audit.json"),
    Artifact("result", "results/closure_quotient_lambda_proof_seed_coverage_audit.json"),
    Artifact("result", "results/closure_quotient_lambda_convergence_priorities.json"),
    Artifact("result", "results/closure_quotient_partial_result_summary.json"),
    Artifact("result", "results/pari_ell2cover_mixed_aabb_h100000.jsonl"),
    Artifact("result", "results/pari_bsd_mixed_aabb_t10.jsonl"),
    Artifact("result", "results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl"),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_001_115_297_AA_covers_3_4.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_001_115_297_AA_covers_3_4.sage",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_001_115_297_AA_covers_3_4.magma",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_001_115_297_AA_covers_3_4_sage_probe.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_001_115_297_AA_covers_3_4_map_verify.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_001_115_297_AA_covers_3_4_local_witnesses.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.sage",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.magma",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3_sage_probe.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3_map_verify.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3_local_witnesses.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_006_567_3757_BB_covers_4_3.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_006_567_3757_BB_covers_4_3.sage",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_006_567_3757_BB_covers_4_3.magma",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_006_567_3757_BB_covers_4_3_sage_probe.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_006_567_3757_BB_covers_4_3_map_verify.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_006_567_3757_BB_covers_4_3_local_witnesses.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_009_5075_17901_AA_covers_4_3.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_009_5075_17901_AA_covers_4_3.sage",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_009_5075_17901_AA_covers_4_3.magma",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_009_5075_17901_AA_covers_4_3_sage_probe.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_009_5075_17901_AA_covers_4_3_map_verify.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_009_5075_17901_AA_covers_4_3_local_witnesses.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_012_8075_8613_AA_covers_4_3.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_012_8075_8613_AA_covers_4_3.sage",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_012_8075_8613_AA_covers_4_3.magma",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_012_8075_8613_AA_covers_4_3_sage_probe.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_012_8075_8613_AA_covers_4_3_map_verify.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_012_8075_8613_AA_covers_4_3_local_witnesses.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_013_391_9009_BB_covers_4_3.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_013_391_9009_BB_covers_4_3.sage",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_013_391_9009_BB_covers_4_3.magma",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_013_391_9009_BB_covers_4_3_sage_probe.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_013_391_9009_BB_covers_4_3_map_verify.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_013_391_9009_BB_covers_4_3_local_witnesses.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_017_209_21735_BB_covers_3_4.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_017_209_21735_BB_covers_3_4.sage",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_017_209_21735_BB_covers_3_4.magma",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_017_209_21735_BB_covers_3_4_sage_probe.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_017_209_21735_BB_covers_3_4_map_verify.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_017_209_21735_BB_covers_3_4_local_witnesses.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_024_5083_12825_BB_covers_3_4.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_024_5083_12825_BB_covers_3_4.sage",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_024_5083_12825_BB_covers_3_4.magma",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_024_5083_12825_BB_covers_3_4_sage_probe.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_024_5083_12825_BB_covers_3_4_map_verify.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_024_5083_12825_BB_covers_3_4_local_witnesses.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_025_5301_38675_BB_covers_4_3.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_025_5301_38675_BB_covers_4_3.sage",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_025_5301_38675_BB_covers_4_3.magma",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_025_5301_38675_BB_covers_4_3_sage_probe.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_025_5301_38675_BB_covers_4_3_map_verify.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_025_5301_38675_BB_covers_4_3_local_witnesses.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_008_209_5355_BB_covers_5_4_3.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_008_209_5355_BB_covers_5_4_3.sage",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_008_209_5355_BB_covers_5_4_3.magma",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_008_209_5355_BB_covers_5_4_3_sage_probe.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_008_209_5355_BB_covers_5_4_3_map_verify.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_008_209_5355_BB_covers_5_4_3_local_witnesses.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_011_1449_12155_BB_covers_5_6_3_4.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_011_1449_12155_BB_covers_5_6_3_4.sage",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_011_1449_12155_BB_covers_5_6_3_4.magma",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_011_1449_12155_BB_covers_5_6_3_4_sage_probe.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_011_1449_12155_BB_covers_5_6_3_4_map_verify.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_011_1449_12155_BB_covers_5_6_3_4_local_witnesses.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_003_575_4641_AA_covers_4_3.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_003_575_4641_AA_covers_4_3.sage",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_003_575_4641_AA_covers_4_3.magma",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_003_575_4641_AA_covers_4_3_sage_probe.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_003_575_4641_AA_covers_4_3_map_verify.json",
    ),
    Artifact(
        "handoff",
        "results/mixed_closure_residual_handoffs/priority_003_575_4641_AA_covers_4_3_local_witnesses.json",
    ),
)


def parse_required_artifact(raw: str) -> Artifact:
    category, separator, path = raw.partition(":")
    if not separator or not category or not path:
        raise argparse.ArgumentTypeError(
            "--require entries must use CATEGORY:relative/path"
        )
    parsed_path = Path(path)
    if parsed_path.is_absolute() or ".." in parsed_path.parts:
        raise argparse.ArgumentTypeError("--require paths must stay under --root")
    return Artifact(category=category, path=path)


def _artifact_dict(artifact: Artifact) -> dict[str, str]:
    return {"category": artifact.category, "path": artifact.path}


def audit_artifacts(*, root: Path, required: list[Artifact]) -> dict[str, Any]:
    missing = [
        _artifact_dict(artifact)
        for artifact in required
        if not (root / artifact.path).is_file()
    ]
    category_counts = dict(sorted(Counter(a.category for a in required).items()))
    return {
        "ready": not missing,
        "required_file_count": len(required),
        "category_counts": category_counts,
        "missing_files": missing,
        "required_files": [_artifact_dict(artifact) for artifact in required],
        "boundary": BOUNDARY,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--require",
        action="append",
        type=parse_required_artifact,
        default=[],
        help=(
            "Required artifact as CATEGORY:relative/path. When omitted, the "
            "built-in closure-quotient partial-result manifest is used."
        ),
    )
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    required = args.require or list(DEFAULT_REQUIRED_ARTIFACTS)
    audit = audit_artifacts(root=args.root, required=required)
    write_json(args.out, audit)
    print(f"wrote closure quotient partial-result artifact audit to {args.out}")
    print(f"ready={audit['ready']}")
    print(f"required_file_count={audit['required_file_count']}")
    print(f"missing_files={audit['missing_files']}")
    if args.strict and not audit["ready"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
