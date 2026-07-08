# Rank-Zero Selmer Tangent-Minus-One Punctured Nodes

## Question

What happens near, but not exactly at, the nodes of the tangent squareclass `-1`
standard families?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_minus_one_punctured_nodes.py \
  --nonnode-branches results/closure_quotient_rank_zero_selmer_tangent_minus_one_nonnode_branches.json \
  --node-values results/closure_quotient_rank_zero_selmer_tangent_minus_one_node_values.json \
  --out results/closure_quotient_rank_zero_selmer_tangent_minus_one_punctured_nodes.json \
  --strict
```

## Output

```text
status=ok
input_nonnode_branch_count=2
input_node_value_count=2
punctured_node_neighborhood_excluded_count=2
node_center_lift_analysis_proved_count=0
local_image_schema_proved_count=0
```

## Interpretation

普通话说：在奇素数局部域里，足够靠近 `1` 的单位是平方。所以：

```text
Y^2 = nu*X*(X-1)^2,     X-1 has positive valuation
```

会让 `X` 在节点附近看起来像平方；但非节点分支恒等式要求 `X` 的平方类是
`nu`。`nu` 是非平方，所以矛盾。

同理：

```text
Y^2 = nu*X^2*(1-X),     X has positive valuation
```

会让 `1-X` 在节点附近看起来像平方；但非节点分支恒等式要求 `1-X` 的平方类是
`nu`。因此也矛盾。

所以 `-1` 情况的节点附近没有穿孔分支贡献；剩下要单独处理的是节点中心本身的
formal lift compatibility。

## Boundary

This proves only punctured-neighborhood squareclass obstructions. It does not
prove node-center lift analysis, any local image theorem, local condition,
Selmer rank bound, or lambda-family exclusion.
