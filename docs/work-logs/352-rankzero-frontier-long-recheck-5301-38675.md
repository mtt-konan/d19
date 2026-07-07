# Rank-Zero Frontier Long Recheck: 5301,38675 BB

## Scope

Run a longer strictification attempt on the eighth rank-zero frontier target
`(5301,38675) BB`, using the same 600-second rank-method budget as the preceding
long rechecks.

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache DOT_SAGE=/private/tmp/d19-dot-sage uv run python scripts/theory/sage_probe_mixed_closure_rank_methods.py \
  --handoff results/mixed_closure_residual_handoffs/priority_025_5301_38675_BB_covers_4_3.json \
  --out results/priority_025_5301_38675_BB_rank_methods_t600_twodescent40.json \
  --sage sage \
  --timeout 600 \
  --method rank_proof \
  --method two_descent \
  --two-descent-second-limit 40 \
  --dot-sage /private/tmp/d19-dot-sage
```

## Output

```text
status=ok
method_status_counts={'rank_proof:runtime-error': 1, 'two_descent:timeout': 1}
rank_zero_proof_candidate=False
```

Details:

```text
rank_proof: runtime-error, rank not provably correct (lower bound: 0)
two_descent: timeout under 600 seconds
```

## Ledger Update

The attempt ledger now includes this long recheck:

```text
attempt_count=17
target_count_with_attempts=8
attempt_status_counts={'rank-method-open-not-proof': 8, 'rank-method-timeout-not-proof': 8, 'timeout-not-proof': 1}
strict_certificate_ready_count=0
```

## Boundary

This is a failed strictification attempt, not a proof. A 600-second
`two_descent(second_limit=40)` budget did not close the rank bounds and did not
prove any residual cover has no rational point.
