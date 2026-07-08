# Rank-Zero Selmer Tangent-One Unit Branch

## Question

On the standard tangent-one model

```text
Y^2 = X*(X - 1)^2
```

what can be proved immediately on the branch where both `X` and `X - 1`
are local units?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_one_unit_branch.py \
  --tangent-one-normal-forms results/closure_quotient_rank_zero_selmer_odd_prime_tangent_one_normal_forms.json \
  --out results/closure_quotient_rank_zero_selmer_tangent_one_unit_branch.json \
  --strict
```

## Output

```text
status=ok
input_normal_form_count=2
unit_branch_count=1
unit_branch_squareclass_consequence_proved_count=1
local_image_schema_proved_count=0
```

## Interpretation

普通话说：在这个分支里，`X - 1` 是单位，所以可以除它：

```text
Y^2 = X*(X - 1)^2
X = (Y/(X - 1))^2
```

因此这个分支上的 `X` 平方类是平凡的。这只是一个分支级结论；它没有覆盖
`X` 非单位、`X - 1` 非单位、另一个 tangent-one 标准模型，也没有覆盖
tangent squareclass 为 `-1` 的两个 schema。

## Boundary

This proves only the unit-branch squareclass consequence on
`Y^2 = X*(X - 1)^2`. It does not prove any local image theorem, local
condition, Selmer rank bound, or lambda-family exclusion.
