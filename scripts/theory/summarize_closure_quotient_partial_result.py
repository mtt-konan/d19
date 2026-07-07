#!/usr/bin/env python3
"""Summarize the closure-quotient partial-result gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _int_value(payload: dict[str, Any], key: str) -> int:
    return int(payload.get(key, 0))


def _blocking_issues(
    *,
    claim_audit: dict[str, Any],
    language_audit: dict[str, Any],
    priority_summary: dict[str, Any],
    priority_handoff_audit: dict[str, Any],
    residual_local_witnesses: dict[str, Any],
    selmer_gap_ledger: dict[str, Any],
    residual_cover_map_verify: dict[str, Any],
    rank0_torsion_preimage_audit: dict[str, Any],
    bsd_conditional_no_point_audit: dict[str, Any],
    residual_open_frontier_audit: dict[str, Any],
    rank_zero_frontier_queue: dict[str, Any],
    non_rankzero_frontier_queue: dict[str, Any],
    artifact_audit: dict[str, Any],
) -> list[str]:
    issues: list[str] = []
    if claim_audit.get("mismatches"):
        issues.append("claim-audit-mismatches")
    if language_audit.get("violations"):
        issues.append("language-audit-violations")
    if not priority_summary.get("top_targets"):
        issues.append("missing-priority-top-target")
    if priority_handoff_audit.get("ready") is not True:
        issues.append("priority-handoff-audit-issues")
    if (
        residual_local_witnesses.get("status") != "ok"
        or residual_local_witnesses.get("sage", {}).get("all_bad_primes_witnessed")
        is not True
        or int(residual_local_witnesses.get("unresolved_bad_prime_total", 0)) != 0
    ):
        issues.append("residual-local-witness-issues")
    if (
        _int_value(selmer_gap_ledger, "candidate_cover_total")
        != _int_value(priority_summary, "candidate_cover_total")
        or _int_value(selmer_gap_ledger, "missing_diagnostic_rows") != 0
        or selmer_gap_ledger.get("all_rows_candidate_not_proof") is not True
    ):
        issues.append("residual-selmer-gap-ledger-issues")
    if (
        residual_cover_map_verify.get("all_verified") is not True
        or _int_value(residual_cover_map_verify, "target_cover_count")
        != _int_value(priority_summary, "candidate_cover_total")
        or _int_value(residual_cover_map_verify, "failed_cover_count") != 0
    ):
        issues.append("residual-cover-map-verify-issues")
    if (
        rank0_torsion_preimage_audit.get("status") != "ok"
        or rank0_torsion_preimage_audit.get("all_no_torsion_preimages") is not True
        or _int_value(rank0_torsion_preimage_audit, "target_cover_count")
        != _int_value(selmer_gap_ledger, "rank0_sha2_gap2_cover_total")
        or _int_value(rank0_torsion_preimage_audit, "failed_cover_count") != 0
    ):
        issues.append("rank0-torsion-preimage-audit-issues")
    if (
        bsd_conditional_no_point_audit.get("status") != "ok"
        or bsd_conditional_no_point_audit.get("candidate_not_proof") is not True
        or _int_value(bsd_conditional_no_point_audit, "strict_no_point_cover_count")
        != 0
        or _int_value(bsd_conditional_no_point_audit, "rank0_sha2_gap2_cover_count")
        != _int_value(selmer_gap_ledger, "rank0_sha2_gap2_cover_total")
    ):
        issues.append("bsd-conditional-no-point-audit-issues")
    if (
        residual_open_frontier_audit.get("status") != "ok"
        or _int_value(residual_open_frontier_audit, "candidate_cover_total")
        != _int_value(priority_summary, "candidate_cover_total")
        or _int_value(residual_open_frontier_audit, "conditional_no_point_cover_count")
        != _int_value(
            bsd_conditional_no_point_audit,
            "bsd_conditional_no_point_cover_count",
        )
        or _int_value(residual_open_frontier_audit, "strict_no_point_cover_count")
        != 0
    ):
        issues.append("residual-open-frontier-audit-issues")
    if (
        rank_zero_frontier_queue.get("status") != "ok"
        or _int_value(rank_zero_frontier_queue, "rank_zero_frontier_cover_count")
        != int(
            residual_open_frontier_audit.get("open_frontier_type_counts", {}).get(
                "rank-zero-needs-rank-proof", 0
            )
        )
        or _int_value(rank_zero_frontier_queue, "closed_rank_zero_target_count") != 0
    ):
        issues.append("rank-zero-frontier-queue-issues")
    non_rankzero_expected = sum(
        int(residual_open_frontier_audit.get("open_frontier_type_counts", {}).get(key, 0))
        for key in (
            "rank1-needs-visible-generator-or-descent",
            "even-rank-gap4-needs-deeper-descent",
        )
    )
    if (
        non_rankzero_frontier_queue.get("status") != "ok"
        or _int_value(
            non_rankzero_frontier_queue, "non_rankzero_frontier_cover_count"
        )
        != non_rankzero_expected
    ):
        issues.append("non-rankzero-frontier-queue-issues")
    if artifact_audit.get("ready") is not True:
        issues.append("artifact-audit-missing-files")
    return issues


def summarize_partial_result(
    *,
    claim_audit: dict[str, Any],
    language_audit: dict[str, Any],
    priority_summary: dict[str, Any],
    priority_handoff_audit: dict[str, Any],
    residual_local_witnesses: dict[str, Any],
    selmer_gap_ledger: dict[str, Any],
    residual_cover_map_verify: dict[str, Any],
    rank0_torsion_preimage_audit: dict[str, Any],
    bsd_conditional_no_point_audit: dict[str, Any],
    residual_open_frontier_audit: dict[str, Any],
    rank_zero_frontier_queue: dict[str, Any],
    non_rankzero_frontier_queue: dict[str, Any],
    artifact_audit: dict[str, Any],
) -> dict[str, Any]:
    claim_values = claim_audit.get("claim_values", {})
    top_targets = priority_summary.get("top_targets", [])
    top_target = top_targets[0] if top_targets else None
    issues = _blocking_issues(
        claim_audit=claim_audit,
        language_audit=language_audit,
        priority_summary=priority_summary,
        priority_handoff_audit=priority_handoff_audit,
        residual_local_witnesses=residual_local_witnesses,
        selmer_gap_ledger=selmer_gap_ledger,
        residual_cover_map_verify=residual_cover_map_verify,
        rank0_torsion_preimage_audit=rank0_torsion_preimage_audit,
        bsd_conditional_no_point_audit=bsd_conditional_no_point_audit,
        residual_open_frontier_audit=residual_open_frontier_audit,
        rank_zero_frontier_queue=rank_zero_frontier_queue,
        non_rankzero_frontier_queue=non_rankzero_frontier_queue,
        artifact_audit=artifact_audit,
    )
    non_rankzero_expected = sum(
        int(residual_open_frontier_audit.get("open_frontier_type_counts", {}).get(key, 0))
        for key in (
            "rank1-needs-visible-generator-or-descent",
            "even-rank-gap4-needs-deeper-descent",
        )
    )

    return {
        "ready_for_partial_result": not issues,
        "blocking_issues": issues,
        "strict_certificate": {
            "rank0_torsion_certificates": _int_value(
                claim_values, "rank0_torsion_certificates"
            ),
            "strict_excluded_pair_count": _int_value(
                claim_values, "strict_excluded_pair_count"
            ),
        },
        "residual_status": {
            "candidate_cover_total": _int_value(
                claim_values, "residual_evidence_candidate_cover_total"
            ),
            "top_target": top_target,
            "bsd_analytic_rank0_rows": _int_value(
                claim_values, "bsd_analytic_rank0_rows"
            ),
            "proof_status": "candidate-not-proof",
        },
        "language_status": {
            "files": _int_value(language_audit, "files"),
            "violations": len(language_audit.get("violations", [])),
        },
        "priority_handoff_status": {
            "ready": priority_handoff_audit.get("ready") is True,
            "groups_checked": _int_value(priority_handoff_audit, "groups_checked"),
            "target_cover_count": _int_value(
                priority_handoff_audit, "target_cover_count"
            ),
            "map_verified_groups": int(
                priority_handoff_audit.get("map_verify_status_counts", {}).get("ok", 0)
            ),
            "local_witnessed_groups": int(
                priority_handoff_audit.get("local_witness_status_counts", {}).get(
                    "ok", 0
                )
            ),
            "violations": len(priority_handoff_audit.get("violations", [])),
        },
        "residual_local_witness_status": {
            "ready": residual_local_witnesses.get("status") == "ok"
            and residual_local_witnesses.get("sage", {}).get("all_bad_primes_witnessed")
            is True
            and _int_value(residual_local_witnesses, "unresolved_bad_prime_total")
            == 0,
            "candidate_cover_total": _int_value(
                residual_local_witnesses, "candidate_cover_total"
            ),
            "bad_prime_check_total": _int_value(
                residual_local_witnesses, "bad_prime_check_total"
            ),
            "unresolved_bad_prime_total": _int_value(
                residual_local_witnesses, "unresolved_bad_prime_total"
            ),
        },
        "residual_selmer_gap_status": {
            "ready": _int_value(selmer_gap_ledger, "candidate_cover_total")
            == _int_value(priority_summary, "candidate_cover_total")
            and _int_value(selmer_gap_ledger, "missing_diagnostic_rows") == 0
            and selmer_gap_ledger.get("all_rows_candidate_not_proof") is True,
            "candidate_cover_total": _int_value(
                selmer_gap_ledger, "candidate_cover_total"
            ),
            "rows_with_ok_diagnostics": _int_value(
                selmer_gap_ledger, "rows_with_ok_diagnostics"
            ),
            "missing_diagnostic_rows": _int_value(
                selmer_gap_ledger, "missing_diagnostic_rows"
            ),
            "rank0_sha2_gap2_cover_total": _int_value(
                selmer_gap_ledger, "rank0_sha2_gap2_cover_total"
            ),
            "gap_type_counts": dict(
                sorted(selmer_gap_ledger.get("gap_type_counts", {}).items())
            ),
        },
        "residual_cover_map_status": {
            "ready": residual_cover_map_verify.get("all_verified") is True
            and _int_value(residual_cover_map_verify, "target_cover_count")
            == _int_value(priority_summary, "candidate_cover_total")
            and _int_value(residual_cover_map_verify, "failed_cover_count") == 0,
            "target_cover_count": _int_value(
                residual_cover_map_verify, "target_cover_count"
            ),
            "verified_cover_count": _int_value(
                residual_cover_map_verify, "verified_cover_count"
            ),
            "failed_cover_count": _int_value(
                residual_cover_map_verify, "failed_cover_count"
            ),
        },
        "rank0_torsion_preimage_status": {
            "ready": rank0_torsion_preimage_audit.get("status") == "ok"
            and rank0_torsion_preimage_audit.get("all_no_torsion_preimages") is True
            and _int_value(rank0_torsion_preimage_audit, "target_cover_count")
            == _int_value(selmer_gap_ledger, "rank0_sha2_gap2_cover_total")
            and _int_value(rank0_torsion_preimage_audit, "failed_cover_count") == 0,
            "target_cover_count": _int_value(
                rank0_torsion_preimage_audit, "target_cover_count"
            ),
            "no_torsion_preimage_count": _int_value(
                rank0_torsion_preimage_audit, "no_torsion_preimage_count"
            ),
            "failed_cover_count": _int_value(
                rank0_torsion_preimage_audit, "failed_cover_count"
            ),
            "conditional_on_rank_zero": True,
        },
        "bsd_conditional_no_point_status": {
            "ready": bsd_conditional_no_point_audit.get("status") == "ok"
            and bsd_conditional_no_point_audit.get("candidate_not_proof") is True
            and _int_value(
                bsd_conditional_no_point_audit, "strict_no_point_cover_count"
            )
            == 0
            and _int_value(
                bsd_conditional_no_point_audit, "rank0_sha2_gap2_cover_count"
            )
            == _int_value(selmer_gap_ledger, "rank0_sha2_gap2_cover_total"),
            "bsd_conditional_no_point_cover_count": _int_value(
                bsd_conditional_no_point_audit,
                "bsd_conditional_no_point_cover_count",
            ),
            "rank0_sha2_gap2_cover_count": _int_value(
                bsd_conditional_no_point_audit, "rank0_sha2_gap2_cover_count"
            ),
            "strict_no_point_cover_count": _int_value(
                bsd_conditional_no_point_audit, "strict_no_point_cover_count"
            ),
            "candidate_not_proof": bsd_conditional_no_point_audit.get(
                "candidate_not_proof"
            )
            is True,
            "proof_status": "conditional-not-proof",
        },
        "residual_open_frontier_status": {
            "ready": residual_open_frontier_audit.get("status") == "ok"
            and _int_value(residual_open_frontier_audit, "candidate_cover_total")
            == _int_value(priority_summary, "candidate_cover_total")
            and _int_value(
                residual_open_frontier_audit, "conditional_no_point_cover_count"
            )
            == _int_value(
                bsd_conditional_no_point_audit,
                "bsd_conditional_no_point_cover_count",
            )
            and _int_value(
                residual_open_frontier_audit, "strict_no_point_cover_count"
            )
            == 0,
            "candidate_cover_total": _int_value(
                residual_open_frontier_audit, "candidate_cover_total"
            ),
            "conditional_no_point_cover_count": _int_value(
                residual_open_frontier_audit, "conditional_no_point_cover_count"
            ),
            "strict_no_point_cover_count": _int_value(
                residual_open_frontier_audit, "strict_no_point_cover_count"
            ),
            "open_frontier_cover_count": _int_value(
                residual_open_frontier_audit, "open_frontier_cover_count"
            ),
            "open_frontier_type_counts": dict(
                sorted(
                    residual_open_frontier_audit.get(
                        "open_frontier_type_counts", {}
                    ).items()
                )
            ),
            "proof_status": "open-frontier-not-proof",
        },
        "rank_zero_frontier_status": {
            "ready": rank_zero_frontier_queue.get("status") == "ok"
            and _int_value(rank_zero_frontier_queue, "rank_zero_frontier_cover_count")
            == int(
                residual_open_frontier_audit.get("open_frontier_type_counts", {}).get(
                    "rank-zero-needs-rank-proof", 0
                )
            )
            and _int_value(rank_zero_frontier_queue, "closed_rank_zero_target_count")
            == 0,
            "rank_zero_frontier_cover_count": _int_value(
                rank_zero_frontier_queue, "rank_zero_frontier_cover_count"
            ),
            "rank_zero_frontier_target_count": _int_value(
                rank_zero_frontier_queue, "rank_zero_frontier_target_count"
            ),
            "closed_rank_zero_target_count": _int_value(
                rank_zero_frontier_queue, "closed_rank_zero_target_count"
            ),
            "target_status_counts": dict(
                sorted(rank_zero_frontier_queue.get("target_status_counts", {}).items())
            ),
            "proof_status": "rank-proof-frontier-not-proof",
        },
        "non_rankzero_frontier_status": {
            "ready": non_rankzero_frontier_queue.get("status") == "ok"
            and _int_value(
                non_rankzero_frontier_queue, "non_rankzero_frontier_cover_count"
            )
            == non_rankzero_expected,
            "non_rankzero_frontier_cover_count": _int_value(
                non_rankzero_frontier_queue, "non_rankzero_frontier_cover_count"
            ),
            "non_rankzero_frontier_target_count": _int_value(
                non_rankzero_frontier_queue, "non_rankzero_frontier_target_count"
            ),
            "target_type_counts": dict(
                sorted(
                    non_rankzero_frontier_queue.get("target_type_counts", {}).items()
                )
            ),
            "proof_status": "non-rankzero-frontier-not-proof",
        },
        "artifact_status": {
            "ready": artifact_audit.get("ready") is True,
            "required_file_count": _int_value(artifact_audit, "required_file_count"),
            "missing_file_count": len(artifact_audit.get("missing_files", [])),
        },
        "boundary": (
            "Ready here means the stored partial-result evidence is internally "
            "consistent and wording boundaries are clean. It does not mean the "
            "residual 2-covers have been strictly proven pointless."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claim-audit", type=Path, required=True)
    parser.add_argument("--language-audit", type=Path, required=True)
    parser.add_argument("--priority-summary", type=Path, required=True)
    parser.add_argument("--priority-handoff-audit", type=Path, required=True)
    parser.add_argument("--residual-local-witnesses", type=Path, required=True)
    parser.add_argument("--selmer-gap-ledger", type=Path, required=True)
    parser.add_argument("--residual-cover-map-verify", type=Path, required=True)
    parser.add_argument("--rank0-torsion-preimage-audit", type=Path, required=True)
    parser.add_argument("--bsd-conditional-no-point-audit", type=Path, required=True)
    parser.add_argument("--residual-open-frontier-audit", type=Path, required=True)
    parser.add_argument("--rank-zero-frontier-queue", type=Path, required=True)
    parser.add_argument("--non-rankzero-frontier-queue", type=Path, required=True)
    parser.add_argument("--artifact-audit", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = summarize_partial_result(
        claim_audit=load_json(args.claim_audit),
        language_audit=load_json(args.language_audit),
        priority_summary=load_json(args.priority_summary),
        priority_handoff_audit=load_json(args.priority_handoff_audit),
        residual_local_witnesses=load_json(args.residual_local_witnesses),
        selmer_gap_ledger=load_json(args.selmer_gap_ledger),
        residual_cover_map_verify=load_json(args.residual_cover_map_verify),
        rank0_torsion_preimage_audit=load_json(args.rank0_torsion_preimage_audit),
        bsd_conditional_no_point_audit=load_json(
            args.bsd_conditional_no_point_audit
        ),
        residual_open_frontier_audit=load_json(args.residual_open_frontier_audit),
        rank_zero_frontier_queue=load_json(args.rank_zero_frontier_queue),
        non_rankzero_frontier_queue=load_json(args.non_rankzero_frontier_queue),
        artifact_audit=load_json(args.artifact_audit),
    )
    write_json(args.out, summary)
    print(f"wrote closure quotient partial-result summary to {args.out}")
    print(f"ready_for_partial_result={summary['ready_for_partial_result']}")
    print(f"blocking_issues={summary['blocking_issues']}")
    if args.strict and not summary["ready_for_partial_result"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
