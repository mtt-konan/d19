# Even Gap4 Frontier Recheck

Date: 2026-07-07

## Question

Can the remaining even-rank non-rank-zero frontier target `(1449,12155) BB`
be moved forward by a finite Sage rank recheck?

This target accounts for the four `even-rank-sha2-gap4-open` residual covers.
In plain terms: the current descent data leaves a larger 2-primary gap than the
rank-one target. A rank recheck can record whether ordinary descent closes the
elliptic rank bounds, but it still would not by itself prove the residual
2-covers have no rational points.

## Command

```bash
DOT_SAGE=/private/tmp/d19-dot-sage \
UV_CACHE_DIR=/private/tmp/d19-uv-cache \
uv run python scripts/theory/sage_recheck_mixed_closure_residuals.py \
  --summary results/mixed_closure_rank_summary.json \
  --target 1449,12155,BB \
  --second-limit 13 \
  --second-limit 20 \
  --timeout 120 \
  --out results/sage_even_gap4_frontier_recheck_1449_12155_BB_s13_20_t120.jsonl
```

The recheck was then folded into the non-rank-zero frontier queue together with
the earlier rank-one recheck:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/summarize_mixed_closure_non_rankzero_frontier.py \
  --open-frontier-audit results/mixed_closure_residual_open_frontier_audit.json \
  --diagnostics results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl \
  --sage-recheck results/sage_rank1_frontier_recheck_209_5355_BB_s13_20_t120.jsonl \
  --sage-recheck results/sage_even_gap4_frontier_recheck_1449_12155_BB_s13_20_t120.jsonl \
  --out results/mixed_closure_non_rankzero_frontier_queue.json \
  --strict
```

## Result

The Sage run timed out after the 120-second per-curve budget:

```text
(1449,12155) BB status = timeout
final_rank_bounds = missing
status_counts = {'timeout': 1}
```

The non-rank-zero queue now records both elliptic targets as Sage timeouts:

```text
non_rankzero_frontier_cover_count = 7
non_rankzero_frontier_target_count = 2
target_status_counts = {'sage-timeout': 2}
```

For `(1449,12155) BB`, the stored status is:

```text
proof_queue_status = sage-timeout
sage_recheck_status = timeout
sage_recheck_final_rank_bounds = None
next_step = retry with stronger descent tooling or switch to a cover-level proof
```

## Boundary

This is not a no-point proof and not a deeper-descent proof. It is only a record
that one finite Sage attempt did not close the even gap4 target. The strict
partial result remains unchanged: only the rank-zero `AA/BB` torsion pullback
certificates are paper-ready.
