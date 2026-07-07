# Lambda Mainline Proof Seed Gate

## Question

Does the top-level lambda mainline gate now require proof-seed coverage, not just
route partition coverage?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_lambda_mainline.py \
  --ray-ledger results/closure_quotient_ray_ledger.json \
  --lambda-frontier results/closure_quotient_lambda_frontier.json \
  --route-partition results/closure_quotient_lambda_route_partition_audit.json \
  --two-cover-frontier results/closure_quotient_two_cover_lambda_frontier.json \
  --proof-seed-coverage results/closure_quotient_lambda_proof_seed_coverage_audit.json \
  --out results/closure_quotient_lambda_mainline_audit.json \
  --strict
```

## Output

```text
status=ok
lambda_class_count=356
covered_class_count=356
```

Checks now include:

```text
proof_seed_coverage_complete=True
```

## Interpretation

普通话说：以前 mainline gate 确认 356 个比例类分到了三条路线里。现在它进一步要求：
三条路线必须都有 proof-seed ledger 覆盖。

这把 wl378 的独立检查提升为主线总门槛。以后如果有人只更新 route partition，却没有更新
rank-zero / root-number / two-cover 的 seed ledger，mainline gate 会失败。

这一步仍然不证明任何比例类整族排除。它只是把“不能靠单点搜索数量推进”的工作方式固定进总 gate。

## Boundary

This audits that the closure quotient work is organized as a lambda-level
structural proof mainline. It does not prove any lambda-family exclusion.
