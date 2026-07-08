# Rank-Zero Selmer Tangent-One Non-Node Branches

## Question

Can the tangent-one standard models cover more than the unit branches without
turning this into a full local-image theorem?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_one_nonnode_branches.py \
  --tangent-one-normal-forms results/closure_quotient_rank_zero_selmer_odd_prime_tangent_one_normal_forms.json \
  --out results/closure_quotient_rank_zero_selmer_tangent_one_nonnode_branches.json \
  --strict
```

## Output

```text
status=ok
input_normal_form_count=2
nonnode_branch_count=2
nonnode_squareclass_consequence_proved_count=2
local_image_schema_proved_count=0
```

## Interpretation

普通话说：上一层只说了 `X` 和 `X-1` 都是单位时可以相除。其实这里不需要
它们是单位，只需要除数不是零：

```text
Y^2 = X*(X - 1)^2,   X - 1 != 0  =>  X = (Y/(X - 1))^2
Y^2 = X^2*(1 - X),   X != 0      =>  1 - X = (Y/X)^2
```

所以两个 tangent-one 标准模型的非节点分支都已经有平方类结论。还没处理的是
节点本身：第一个模型的 `X=1` 分支、第二个模型的 `X=0` 分支，以及 tangent
squareclass 为 `-1` 的两个 schema。

## Boundary

This proves only the non-node branch squareclass consequences on the two
tangent-one standard models. It does not prove any local image theorem, local
condition, Selmer rank bound, or lambda-family exclusion.
