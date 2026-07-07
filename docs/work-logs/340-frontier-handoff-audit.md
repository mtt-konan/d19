# wl340 - Frontier Handoff Audit

## What changed

Added a content audit for the residual frontier handoff packages:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_mixed_closure_frontier_handoffs.py \
  --rank-zero-queue results/mixed_closure_rank_zero_frontier_queue.json \
  --non-rankzero-queue results/mixed_closure_non_rankzero_frontier_queue.json \
  --priorities results/mixed_closure_aabb_residual_cover_priorities.json \
  --handoff-dir results/mixed_closure_residual_handoffs \
  --out results/mixed_closure_frontier_handoff_audit.json \
  --strict
```

Output:

```text
status=ok
handoff_group_count=10
target_cover_count=23
strict_promotion_count=0
missing_files=[]
violations=[]
```

The audit checks that all 10 frontier handoff groups have JSON/Sage/Magma files,
map verification, bad-prime local witnesses, and bounded Sage probes aligned with
the rank-zero and non-rankzero frontier queues.

## Boundary

This is still a handoff audit, not a proof. The bounded Sage probes have
`rank_proof_status=runtime-error` and zero bounded-search points; that remains
candidate-not-proof evidence. No residual cover is promoted into the strict
theorem by this work.
