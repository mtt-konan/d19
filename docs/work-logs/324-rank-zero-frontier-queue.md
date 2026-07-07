# Rank-Zero Frontier Queue

Date: 2026-07-07

## Question

The residual open-frontier audit found 16 covers of type `rank-zero-needs-rank-proof`.
Since two covers often share the same elliptic rank computation, group them by
`(A,B,curve)` rank target and record any Sage recheck attempts.

## Commands

Top-priority Sage retry:

```bash
DOT_SAGE=/private/tmp/d19-dot-sage \
UV_CACHE_DIR=/private/tmp/d19-uv-cache \
uv run python scripts/theory/sage_recheck_mixed_closure_residuals.py \
  --summary results/mixed_closure_rank_summary.json \
  --target 1625,5643,AA \
  --second-limit 13 \
  --second-limit 20 \
  --timeout 120 \
  --out results/sage_rankzero_frontier_recheck_s13_20_t120.jsonl
```

Queue summary:

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

The 16 rank-zero-frontier covers collapse to 8 rank proof targets:

```text
rank_zero_frontier_cover_count = 16
rank_zero_frontier_target_count = 8
closed_rank_zero_target_count = 0
target_status_counts = {'not-retried': 6, 'sage-timeout': 2}
```

The first attempted target was `(1625,5643) AA`, covering priorities `5` and `7`
with cover indices `3,4`. The second attempted target was `(567,3757) BB`,
covering priorities `6` and `21` with cover indices `3,4`. Sage did not close
either rank bound within 120 seconds:

```text
status = timeout
second_limits = 13,20
final_rank_bounds = missing
```

The remaining 6 rank targets are queued but not retried yet:

```text
(5075,17901) AA
(8075,8613) AA
(391,9009) BB
(209,21735) BB
(5083,12825) BB
(5301,38675) BB
```

## Boundary

This queue records rank-proof work, not a new theorem. No rank-zero target was
strictly closed here, so no residual cover is promoted into the strict certificate.
The useful output is narrower: the next strictification work now has 8 concrete rank
targets instead of 16 separate cover rows.
