# Residual Frontier Strategy Audit

Date: 2026-07-07

## Question

After all short Sage frontier retries, what is the next proof route for the
remaining `AA/BB` residual covers?

The point is not to prove new mathematics here. The point is to stop treating
120-second Sage retries as an open queue once every frontier target has already
timed out, and to record the next proof lanes without promoting timeout evidence
into a theorem.

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/audit_mixed_closure_residual_frontier_strategy.py \
  --rank-zero-queue results/mixed_closure_rank_zero_frontier_queue.json \
  --non-rankzero-queue results/mixed_closure_non_rankzero_frontier_queue.json \
  --out results/mixed_closure_residual_frontier_strategy_audit.json \
  --strict
```

## Result

```text
short_sage_retry_status = exhausted-without-proof
short_sage_retry_target_count = 10
short_sage_retry_timeout_target_count = 10
strict_promotion_count = 0
candidate_not_proof = True
```

The 10 targets are the 8 rank-zero frontier rank targets plus the 2 non-rank-zero
frontier targets. All have recorded Sage timeouts under the current local retry
workflow. None returned a strict rank proof or a cover-level no-point certificate.

The next proof lanes are:

```text
external_rank_proof_or_cover_level_descent = 8
rank1_generator_or_sha2_separation = 1
even_gap4_deeper_descent_or_sha2_obstruction = 1
```

The first external rank-proof target remains:

```text
(1625,5643) AA
priorities = [5, 7]
cover_indices = [3, 4]
has_long_sage_timeout = True
max_timeout_seconds = 600
```

## Boundary

This audit is routing information, not a mathematical certificate. It says the
short local Sage retry route has been exhausted without proof. It does not say
that any residual 2-cover has no rational point.

The strict partial result is unchanged: 275 certified rank-zero `AA/BB` torsion
pullback rows, giving 220 strict excluded pairs. The remaining residual covers
still need external rank proof, visible-rank separation, deeper descent, or a
direct cover-level obstruction before they can enter the strict theorem.
