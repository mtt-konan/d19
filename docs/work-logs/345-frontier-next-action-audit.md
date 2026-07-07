# Frontier Next-Action Audit

## Scope

Turn the rank-zero frontier diagnosis into a rerunnable next-action gate. The
goal is not to prove a residual cover has no rational point. The goal is to make
the next route explicit after all 8 rank-zero frontier targets showed the same
cheap rank-method pattern.

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_mixed_closure_frontier_next_actions.py \
  --strictification-queue results/mixed_closure_frontier_strictification_queue.json \
  --attempt-audit results/mixed_closure_frontier_strictification_attempt_audit.json \
  --batch-rank-methods results/mixed_closure_rank_zero_frontier_batch_rank_methods_t45.json \
  --out results/mixed_closure_frontier_next_action_audit.json \
  --strict
```

## Output

```text
status=ok
cheap_rank_method_target_hopping_exhausted=True
recommended_mainline=escalate-beyond-cheap-rank-methods
```

Key fields:

```text
rank_zero_target_count=8
rank_zero_batch_target_count=8
strict_certificate_ready_count=0
violations=[]
```

## Interpretation

In plain language: the cheap rank methods have now done what they can for the
rank-zero frontier. All 8 rank-zero targets were covered, all stayed open, and
none became a strict certificate. The next mainline should therefore stop
expecting easy target-hopping to close the proof, and should escalate to:

- longer or external strict rank proof attempts on selected rank-zero targets;
- or cover-level no-rational-point certificates for every listed residual cover;
- plus the existing rank-one/Sha[2] separation and even-gap4 deeper-descent
  routes for the two non-rankzero frontier targets.

## Boundary

This audit is a routing gate only. It does not prove rank zero and does not prove
that any residual cover has no rational point.
