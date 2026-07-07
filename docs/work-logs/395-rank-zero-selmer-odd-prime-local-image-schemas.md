# Rank-Zero Selmer Odd-Prime Local-Image Schemas

## Question

Can the nine proved odd-prime reduction shapes be reduced to a small number of
local-image theorem schemas?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_local_image_schemas.py \
  --odd-prime-reduction-shapes results/closure_quotient_rank_zero_selmer_odd_prime_reduction_shapes.json \
  --out results/closure_quotient_rank_zero_selmer_odd_prime_local_image_schemas.json \
  --strict
```

## Output

```text
status=ok
input_reduction_shape_count=9
local_image_schema_count=2
local_image_schema_proved_count=0
local_condition_proved_count=0
```

## Interpretation

普通话说：9 条奇素数分支现在只剩两种真正要证明的 local-image 模板：

```text
y^2 = x*(x-r)^2, r 是 local unit
y^2 = x^2*(x-s), s 是 local unit
```

也就是说，后续不该逐个 package 或逐个分支乱试。真正要攻的是这两个
2-isogeny local squareclass image 定理。证明这两个模板之后，才有资格回填
9 条 odd-prime local condition。

## Boundary

This groups reduction shapes into theorem schemas only. It does not prove the
local image theorem, any local condition, a Selmer rank bound, or a lambda-family
exclusion.
