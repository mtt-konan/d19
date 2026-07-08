# Rank-Zero Selmer Tangent-One Unit Branches

## Question

On the standard tangent-one models

```text
Y^2 = X*(X - 1)^2
Y^2 = X^2*(X - 1)
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
unit_branch_count=2
unit_branch_squareclass_consequence_proved_count=2
local_image_schema_proved_count=0
```

## Interpretation

普通话说：在这两个单位分支里，可以安全相除，得到两个平方类结论：

```text
Y^2 = X*(X - 1)^2
X = (Y/(X - 1))^2

Y^2 = X^2*(X - 1)
X - 1 = (Y/X)^2
```

因此第一个模型的单位分支上 `X` 平方类是平凡的，第二个模型的单位分支上
`X - 1` 平方类是平凡的。这只是分支级结论；它没有覆盖 `X` 非单位、
`X - 1` 非单位，也没有覆盖 tangent squareclass 为 `-1` 的两个 schema。

## Boundary

This proves only the unit-branch squareclass consequences on the two
tangent-one standard models. It does not prove any local image theorem,
local condition, Selmer rank bound, or lambda-family exclusion.
