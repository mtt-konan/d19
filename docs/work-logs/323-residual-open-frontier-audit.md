# Residual Open-Frontier Audit

Date: 2026-07-07

## Question

After the BSD-conditional no-point audit, what exactly remains open among the 27
`AA/BB` residual candidate covers?

This worklog records a machine-readable split of the remaining frontier. It is meant
to make the next strictification step less vague.

## Commands

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/test_mixed_closure_residual_open_frontier_audit.py -q

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/audit_mixed_closure_residual_open_frontier.py \
  tests/test_mixed_closure_residual_open_frontier_audit.py

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/audit_mixed_closure_residual_open_frontier.py \
  --selmer-gap-ledger results/mixed_closure_residual_selmer_gap_ledger.json \
  --bsd-conditional-no-point-audit results/mixed_closure_bsd_conditional_no_point_audit.json \
  --out results/mixed_closure_residual_open_frontier_audit.json \
  --strict
```

## Result

The 27 residual candidate covers now split as follows:

```text
candidate_cover_total = 27
conditional_no_point_cover_count = 4
strict_no_point_cover_count = 0
open_frontier_cover_count = 23
```

Frontier types:

```text
bsd-conditional-no-point = 4
rank-zero-needs-rank-proof = 16
rank1-needs-visible-generator-or-descent = 3
even-rank-gap4-needs-deeper-descent = 4
```

Plainly:

- 4 covers have the strongest current conditional evidence, but still depend on BSD-style rank input.
- 16 covers would become no-point candidates of the same shape if rank zero were strictly proved.
- 3 covers have an odd/rank-one obstruction to separate from the residual Sha[2] class.
- 4 covers have a larger even Selmer gap and need a deeper descent or an independent Sha[2] obstruction.

## Boundary

This audit proves no new no-point statement. It is only a ledger of what is still missing.
It keeps `strict_no_point_cover_count = 0` and marks the frontier as not proof.
