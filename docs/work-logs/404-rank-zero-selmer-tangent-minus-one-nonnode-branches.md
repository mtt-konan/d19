# Rank-Zero Selmer Tangent-Minus-One Non-Node Branches

## Question

What squareclass consequence holds away from the node for the tangent
squareclass `-1` standard families?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_minus_one_nonnode_branches.py \
  --tangent-minus-one-normal-forms results/closure_quotient_rank_zero_selmer_tangent_minus_one_normal_forms.json \
  --out results/closure_quotient_rank_zero_selmer_tangent_minus_one_nonnode_branches.json \
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

普通话说：`nu` 是固定的 nonsquare unit。在非节点分支上，两个标准族给出：

```text
Y^2 = nu*X*(X-1)^2,     X-1 != 0  =>  nu*X = (Y/(X-1))^2
Y^2 = nu*X^2*(1-X),     X != 0    =>  nu*(1-X) = (Y/X)^2
```

所以第一个模型的非节点分支上 `X` 的平方类是 `nu`，第二个模型的非节点分支上
`1-X` 的平方类是 `nu`。这只是 branch-level 结论，还没有处理节点中心，也没有
证明 local image。

## Boundary

This proves only non-node branch squareclass consequences while retaining the
nonsquare unit parameter `nu`. It does not prove any local image theorem, local
condition, Selmer rank bound, or lambda-family exclusion.
