# wl343 - Frontier Rank Method Probe

## What changed

Added a Sage probe that runs rank methods in separate subprocesses. This keeps a
timeout in one method from hiding the other method results.

Command run for the first strictification target:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache DOT_SAGE=/private/tmp/d19-dot-sage uv run python scripts/theory/sage_probe_mixed_closure_rank_methods.py \
  --handoff results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json \
  --out results/priority_005_1625_5643_AA_rank_methods_t90_twodescent20.json \
  --sage sage \
  --timeout 90 \
  --method rank_bounds \
  --method rank_proof \
  --method selmer_rank \
  --method pari_ellrank \
  --method two_descent \
  --two-descent-second-limit 20 \
  --dot-sage /private/tmp/d19-dot-sage
```

Output:

```text
status=ok
method_status_counts={'pari_ellrank:ok': 1, 'rank_bounds:ok': 1, 'rank_proof:runtime-error': 1, 'selmer_rank:ok': 1, 'two_descent:timeout': 1}
rank_zero_proof_candidate=False
```

The attempt ledger now includes this probe:

```text
attempt_count=2
attempt_status_counts={'rank-method-timeout-not-proof': 1, 'timeout-not-proof': 1}
strict_certificate_ready_count=0
```

## Boundary

This improves diagnosis only. `rank_bounds`, PARI `ellrank=[0,2,0,[]]`, and
`selmer_rank` completing are not rank-zero certificates. `rank_proof` still does
not prove rank zero, and `two_descent` timed out under this short budget.
