# Rank-Zero Frontier Recheck: 567,3757 BB

Date: 2026-07-07

## Question

Can the next rank-zero residual frontier target `(567,3757) BB` be turned into a
strict rank-zero proof by a finite Sage rank recheck?

This target accounts for two residual covers in the `rank-zero-needs-rank-proof`
bucket. In plain terms: if the elliptic rank bounds closed to `[0,0]`, the
existing torsion-preimage audit could be rerun under a strict rank-zero
hypothesis. Without that closed rank proof, the covers stay on the open
frontier.

## Command

```bash
DOT_SAGE=/private/tmp/d19-dot-sage \
UV_CACHE_DIR=/private/tmp/d19-uv-cache \
uv run python scripts/theory/sage_recheck_mixed_closure_residuals.py \
  --summary results/mixed_closure_rank_summary.json \
  --target 567,3757,BB \
  --second-limit 13 \
  --second-limit 20 \
  --timeout 120 \
  --out results/sage_rankzero_frontier_recheck_567_3757_BB_s13_20_t120.jsonl
```

The recheck was then folded into the rank-zero frontier queue together with the
earlier `(1625,5643) AA` recheck:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/summarize_mixed_closure_rank_zero_frontier.py \
  --open-frontier-audit results/mixed_closure_residual_open_frontier_audit.json \
  --diagnostics results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl \
  --sage-recheck results/sage_rankzero_frontier_recheck_s13_20_t120.jsonl \
  --sage-recheck results/sage_rankzero_frontier_recheck_567_3757_BB_s13_20_t120.jsonl \
  --out results/mixed_closure_rank_zero_frontier_queue.json \
  --strict
```

## Result

The Sage run timed out after the 120-second per-curve budget:

```text
(567,3757) BB status = timeout
final_rank_bounds = missing
status_counts = {'timeout': 1}
```

The rank-zero frontier queue now records:

```text
rank_zero_frontier_cover_count = 16
rank_zero_frontier_target_count = 8
closed_rank_zero_target_count = 0
target_status_counts = {'not-retried': 6, 'sage-timeout': 2}
```

For `(567,3757) BB`, the stored status is:

```text
rank_proof_queue_status = sage-timeout
sage_recheck_status = timeout
sage_recheck_final_rank_bounds = None
next_step = retry rank proof with stronger descent tooling or external CAS
```

## Boundary

This is not a rank-zero proof and not a no-point certificate. It only records
that one finite Sage attempt did not close the rank bounds. The strict result
remains unchanged: only already certified rank-zero `AA/BB` torsion pullback
rows are paper-ready.
