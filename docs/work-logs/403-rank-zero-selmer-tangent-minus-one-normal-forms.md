# Rank-Zero Selmer Tangent-Minus-One Normal Forms

## Question

Can the tangent-squareclass `-1` local-image schemas be normalized without
pretending the nonsquare tangent is a square?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_minus_one_normal_forms.py \
  --odd-prime-local-image-schemas results/closure_quotient_rank_zero_selmer_odd_prime_local_image_schemas.json \
  --out results/closure_quotient_rank_zero_selmer_tangent_minus_one_normal_forms.json \
  --strict
```

## Output

```text
status=ok
input_schema_count=4
tangent_minus_one_schema_count=2
normal_form_proved_count=2
local_image_schema_proved_count=0
```

## Interpretation

普通话说：tangent squareclass 为 `-1` 时，不能像 tangent-one 那样把所有单位都
开平方吸收掉。正确做法是固定一个 nonsquare unit `nu`，只吸收 square-unit 部分：

```text
y^2 = x*(x-r)^2,    r = nu*u^2   ->  Y^2 = nu*X*(X-1)^2
y^2 = x^2*(x-s),   -s = nu*u^2   ->  Y^2 = nu*X^2*(1-X)
```

这把两个 `-1` schema 也收成了标准族，但 `nu` 必须留下。下一步要研究的是带
这个 nonsquare 参数的 local squareclass image，而不是把它当作 tangent-one 情况。

## Boundary

This proves only square-unit normalization while retaining a nonsquare unit
parameter `nu`. It does not prove any local image theorem, local condition,
Selmer rank bound, or lambda-family exclusion.
