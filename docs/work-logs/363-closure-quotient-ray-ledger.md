# Closure Quotient Ray Ledger

## Question

Can the existing closure quotient work be reorganized by primitive ratio
`A:B`, with `c_- = |A-B|`, instead of reporting progress as more individual
`(A,B)` certificates?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_ray_ledger.py \
  --rank-jsonl results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --rank-jsonl results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --rank-summary results/mixed_closure_rank_summary.json \
  --residual-cover-summary results/mixed_closure_aabb_residual_cover_summary.json \
  --out results/closure_quotient_ray_ledger.json \
  --strict
```

## Output

```text
status=ok
pair_count=384
primitive_ray_count=356
c_ratio_class_count=356
strict_c_ratio_class_count=200
```

Additional ledger counts:

```text
c_minus_zero_pair_count=0
strict_pair_count=220
strict_ray_count=200
residual_candidate_pair_count=8
pair_status_counts={
  'observed-not-closed-by-local-tool': 156,
  'residual-candidate-not-proof': 8,
  'strict-local-tool-excludes-observed-pair': 220
}
```

## Interpretation

普通话说：这一轮没有继续增加单个 `(A,B)` 证书，而是把已有结果压到比例层。
对每个 pair 记录：

- 本原比例 `A:B`；
- `c_+ = A+B`；
- `c_- = |A-B|`；
- `c_+/c_-`；
- 当前这个观测 pair 是 strict local tool 覆盖、residual candidate，还是仍开放。

`c_+/c_-` 识别的是无向比例类 `{A:B, B:A}`。它适合作为 ray ledger 的键，
但不能单独区分 `lambda=A/B` 和 `1/lambda`，也不是整族排除定理。

当前 356 个观测本原 ray 中，200 个 ray 的观测 pair 已被 strict local tool 覆盖；
另有 8 个 ray 仍是 residual candidate。12 个 residual cover row 中有 4 个 pair
已经被 strict local tool 覆盖，所以 pair 状态按 strict 优先后只剩 8 个 residual
candidate pair。

## Boundary

This ledger reorganizes existing evidence. It does not add a no-point
certificate and does not prove a lambda-family theorem.
