# Rank-Zero Selmer Tangent-One Normal Forms

## Question

Can the tangent-squareclass-one local-image schemas be normalized to standard
nodal models before computing the local image?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_tangent_one_normal_forms.py \
  --odd-prime-local-image-schemas results/closure_quotient_rank_zero_selmer_odd_prime_local_image_schemas.json \
  --out results/closure_quotient_rank_zero_selmer_odd_prime_tangent_one_normal_forms.json \
  --strict
```

## Output

```text
status=ok
input_schema_count=4
tangent_one_schema_count=2
normal_form_proved_count=2
local_image_schema_proved_count=0
```

## Interpretation

普通话说：在 tangent squareclass 为 `1` 的两个 schema 里，局部单位有平方根，
所以可以做平方单位缩放，把模型化成标准节点形：

```text
y^2 = x*(x-r)^2  ->  Y^2 = X*(X-1)^2
y^2 = x^2*(x-s)  ->  Y^2 = X^2*(1-X)
```

这是真正 local-image 证明前的一段可审阅代数准备。下一步才是计算这两个标准
节点模型的 2-isogeny local squareclass image。

Note: the zero-double-root sign is `1-X`: with `u^2=-s` and
`x=-u^2X, y=u^3Y`, substituting gives `Y^2=X^2(1-X)`.

## Boundary

This proves only the square-unit normal forms for tangent squareclass `1`.
It does not prove any local image theorem, local condition, Selmer rank bound,
or lambda-family exclusion.
