# Non-Rank-Zero Frontier Queue

Date: 2026-07-07

## Question

After separating the rank-zero frontier, what remains among the residual covers with
non-rank-zero rank bounds?

This worklog groups the `rank1` and `even gap4` residual covers by their shared
elliptic target.

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/summarize_mixed_closure_non_rankzero_frontier.py \
  --open-frontier-audit results/mixed_closure_residual_open_frontier_audit.json \
  --diagnostics results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl \
  --out results/mixed_closure_non_rankzero_frontier_queue.json \
  --strict
```

## Result

The 7 non-rank-zero residual covers collapse to 2 elliptic targets:

```text
non_rankzero_frontier_cover_count = 7
non_rankzero_frontier_target_count = 2
target_type_counts = {
  'even-rank-gap4-needs-deeper-descent': 1,
  'rank1-needs-visible-generator-or-descent': 1
}
```

Targets:

```text
(209,5355) BB:
  covers = 3,4,5
  priorities = 8,10,22
  rank_bounds = [1,3]
  rank_plus_sha2_dimension = 3
  next = find a visible rank-one generator and isolate the residual Sha[2] class

(1449,12155) BB:
  covers = 3,4,5,6
  priorities = 11,15,18,23
  rank_bounds = [0,4]
  rank_plus_sha2_dimension = 4
  next = run deeper descent or produce an independent Sha[2] obstruction
```

## Boundary

This is a proof-work queue, not a no-point certificate. It does not prove that either
target has no rational points, and it does not add any strict closure quotient
exclusion. It only reduces 7 cover rows to 2 concrete next targets.
