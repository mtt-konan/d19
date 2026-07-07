# Frontier Batch Rank-Method Probe

## Scope

Batch-ran cheap Sage rank-method diagnostics over all 8 rank-zero frontier
targets from the strictification queue.

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache DOT_SAGE=/private/tmp/d19-dot-sage uv run python scripts/theory/batch_sage_probe_mixed_closure_rank_methods.py \
  --strictification-queue results/mixed_closure_frontier_strictification_queue.json \
  --handoff-audit results/mixed_closure_frontier_handoff_audit.json \
  --handoff-dir results/mixed_closure_residual_handoffs \
  --out results/mixed_closure_rank_zero_frontier_batch_rank_methods_t45.json \
  --sage sage \
  --timeout 45 \
  --method rank_bounds \
  --method selmer_rank \
  --method pari_ellrank \
  --track rank-zero-rank-proof \
  --limit 8 \
  --dot-sage /private/tmp/d19-dot-sage \
  --strict
```

## Output

```text
status=ok
target_count=8
method_status_counts={'pari_ellrank:ok': 8, 'rank_bounds:ok': 8, 'selmer_rank:ok': 8}
rank_zero_proof_candidate_count=0
```

Per target, the cheap diagnostics agree:

```text
rank_bounds=[0,2]
selmer_rank=4
pari_ellrank=[0,2,0,[]]
```

The 8 targets are:

```text
(1625,5643) AA
(567,3757) BB
(5075,17901) AA
(8075,8613) AA
(391,9009) BB
(209,21735) BB
(5083,12825) BB
(5301,38675) BB
```

## Boundary

This is a diagnostic batch, not a proof. In plain language: every rank-zero
frontier target still looks like an open two-cover/Sha[2] gap. The cheap methods
did not find a target whose rank closed to 0, and PARI `ellrank=[0,2,0,[]]`
is still an open interval, not a rank-zero certificate.

## Ledger Integration

The batch result is also expanded into the strictification attempt ledger:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_mixed_closure_frontier_strictification_attempts.py \
  --strictification-queue results/mixed_closure_frontier_strictification_queue.json \
  --probe sage-twodescent20:results/priority_005_1625_5643_AA_covers_4_3_twodescent20_probe.json \
  --probe sage-rank-methods-t90:results/priority_005_1625_5643_AA_rank_methods_t90_twodescent20.json \
  --batch-probe rankzero-batch-t45:results/mixed_closure_rank_zero_frontier_batch_rank_methods_t45.json \
  --out results/mixed_closure_frontier_strictification_attempt_audit.json \
  --strict
```

Output:

```text
status=ok
attempt_count=10
target_count_with_attempts=8
attempt_status_counts={'rank-method-open-not-proof': 8, 'rank-method-timeout-not-proof': 1, 'timeout-not-proof': 1}
strict_certificate_ready_count=0
```

This makes the ledger say explicitly that all 8 rank-zero frontier targets have
cheap rank-method attempts recorded, and none is a strict certificate.
