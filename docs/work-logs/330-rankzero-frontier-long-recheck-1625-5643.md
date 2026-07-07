# Rank-Zero Frontier Long Recheck: 1625,5643 AA

Date: 2026-07-07

## Question

Does simply extending the Sage/eclib time budget close the top rank-zero
frontier target `(1625,5643) AA`?

This is the highest-priority `rank-zero-needs-rank-proof` target. A previous
finite run with `second_limit=13,20` and a 120-second budget timed out. This
worklog repeats the target with a larger second-descent setting and a 600-second
budget.

## Command

```bash
DOT_SAGE=/private/tmp/d19-dot-sage \
UV_CACHE_DIR=/private/tmp/d19-uv-cache \
uv run python scripts/theory/sage_recheck_mixed_closure_residuals.py \
  --summary results/mixed_closure_rank_summary.json \
  --target 1625,5643,AA \
  --second-limit 20 \
  --second-limit 40 \
  --timeout 600 \
  --out results/sage_rankzero_frontier_recheck_1625_5643_AA_s20_40_t600.jsonl
```

The long recheck was folded into the rank-zero frontier queue after the shorter
rank-zero rechecks:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/summarize_mixed_closure_rank_zero_frontier.py \
  --open-frontier-audit results/mixed_closure_residual_open_frontier_audit.json \
  --diagnostics results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl \
  --sage-recheck results/sage_rankzero_frontier_recheck_s13_20_t120.jsonl \
  --sage-recheck results/sage_rankzero_frontier_recheck_567_3757_BB_s13_20_t120.jsonl \
  --sage-recheck results/sage_rankzero_frontier_recheck_5075_17901_AA_s13_20_t120.jsonl \
  --sage-recheck results/sage_rankzero_frontier_recheck_1625_5643_AA_s20_40_t600.jsonl \
  --out results/mixed_closure_rank_zero_frontier_queue.json \
  --strict
```

## Result

The longer Sage run also timed out:

```text
(1625,5643) AA status = timeout
timeout_seconds = 600
elapsed_seconds = 600.004439
final_rank_bounds = missing
status_counts = {'timeout': 1}
```

The rank-zero queue still records no closed rank-zero target:

```text
rank_zero_frontier_cover_count = 16
rank_zero_frontier_target_count = 8
closed_rank_zero_target_count = 0
target_status_counts = {'not-retried': 5, 'sage-timeout': 3}
```

For `(1625,5643) AA`, the stored queue row now records the long timeout:

```text
rank_proof_queue_status = sage-timeout
sage_recheck_timeout_seconds = 600
sage_recheck_elapsed_seconds = 600.004439
sage_recheck_final_rank_bounds = None
next_step = retry rank proof with stronger descent tooling or external CAS
```

## Boundary

This is evidence about tool budget, not a mathematical proof. The 600-second
timeout does not prove the rank is positive, does not prove the rank is zero,
and does not certify any residual cover as pointless. It only shows that this
target did not close under a larger default Sage/eclib descent attempt. The
next useful step is stronger descent tooling or a cover-level proof, not
relabeling this timeout as a theorem.
