# Lambda Proof Seed Coverage

## Question

Do all lambda route classes now have proof-seed ledgers, rather than being
tracked as growing single `(A,B)` certificate counts?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_lambda_proof_seed_coverage.py \
  --route-partition results/closure_quotient_lambda_route_partition_audit.json \
  --rank-zero-seeds results/closure_quotient_rank_zero_proof_seeds.json \
  --root-number-seeds results/closure_quotient_root_number_proof_seeds.json \
  --two-cover-seeds results/closure_quotient_two_cover_proof_seeds.json \
  --out results/closure_quotient_lambda_proof_seed_coverage_audit.json \
  --strict
```

## Output

```text
status=ok
lambda_class_count=356
seed_ledger_class_count=356
violations=[]
```

Route counts:

```text
rank_zero: 200 classes, 3 seed groups
root_number: 148 classes, 21 seed groups
two_cover: 8 classes, 7 seed groups
```

## Interpretation

普通话说：这一步确认 closure quotient 的 `lambda` 主线已经从“继续堆 `(A,B)` 证书”
切成三条结构路线：

- 200 个 rank-zero family-generalization 类；
- 148 个 root-number/rank-structure routing 类；
- 8 个 two-cover / Selmer strict-certificate 类。

三条路线的 seed ledger 正好覆盖 356 个本原比例类，没有漏类、没有重复路线，也没有任何类被误标成
已经整族排除。

这不是最终数学证明。它只是确认后续工作入口已经从单点搜索数量，转为 `lambda=A/B` 层面的
结构证明问题。

## Boundary

This checks that lambda route classes are covered by proof-seed ledgers. It does
not prove any lambda-family exclusion theorem.
