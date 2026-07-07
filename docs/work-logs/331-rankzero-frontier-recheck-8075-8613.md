# Rank-Zero Frontier Recheck: 8075,8613 AA

Date: 2026-07-07

## Question

Can the next rank-zero residual frontier target `(8075,8613) AA` be turned into
a strict rank-zero proof by a finite Sage rank recheck?

This target accounts for two residual covers in the `rank-zero-needs-rank-proof`
bucket. If the elliptic rank bounds closed to `[0,0]`, downstream strict
torsion-preimage auditing would be required. If Sage times out, the target
stays on the proof-work frontier.

## Command

```bash
DOT_SAGE=/private/tmp/d19-dot-sage \
UV_CACHE_DIR=/private/tmp/d19-uv-cache \
uv run python scripts/theory/sage_recheck_mixed_closure_residuals.py \
  --summary results/mixed_closure_rank_summary.json \
  --target 8075,8613,AA \
  --second-limit 13 \
  --second-limit 20 \
  --timeout 120 \
  --out results/sage_rankzero_frontier_recheck_8075_8613_AA_s13_20_t120.jsonl
```

The recheck was then folded into the rank-zero frontier queue:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/summarize_mixed_closure_rank_zero_frontier.py \
  --open-frontier-audit results/mixed_closure_residual_open_frontier_audit.json \
  --diagnostics results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl \
  --sage-recheck results/sage_rankzero_frontier_recheck_s13_20_t120.jsonl \
  --sage-recheck results/sage_rankzero_frontier_recheck_1625_5643_AA_s20_40_t600.jsonl \
  --sage-recheck results/sage_rankzero_frontier_recheck_567_3757_BB_s13_20_t120.jsonl \
  --sage-recheck results/sage_rankzero_frontier_recheck_5075_17901_AA_s13_20_t120.jsonl \
  --sage-recheck results/sage_rankzero_frontier_recheck_8075_8613_AA_s13_20_t120.jsonl \
  --out results/mixed_closure_rank_zero_frontier_queue.json \
  --strict
```

## Result

The Sage run timed out after the 120-second per-curve budget:

```text
(8075,8613) AA status = timeout
timeout_seconds = 120
elapsed_seconds = 120.003778
final_rank_bounds = missing
status_counts = {'timeout': 1}
```

The stdout tail shows the first global descent had lower bound `1` and upper
bound `2` before entering second descent, but the run timed out before producing
a final rank-bound update. That is useful diagnostic information, not a proof.

The rank-zero frontier queue now records:

```text
rank_zero_frontier_cover_count = 16
rank_zero_frontier_target_count = 8
closed_rank_zero_target_count = 0
target_status_counts = {'not-retried': 4, 'sage-timeout': 4}
```

For `(8075,8613) AA`, the stored status is:

```text
rank_proof_queue_status = sage-timeout
sage_recheck_status = timeout
sage_recheck_timeout_seconds = 120
sage_recheck_final_rank_bounds = None
next_step = retry rank proof with stronger descent tooling or external CAS
```

## Boundary

This is not a rank-zero proof and not a no-point certificate. The timeout does
not prove rank zero or positive rank. The strict partial result remains
unchanged: only already certified rank-zero `AA/BB` torsion pullback rows are
paper-ready.
