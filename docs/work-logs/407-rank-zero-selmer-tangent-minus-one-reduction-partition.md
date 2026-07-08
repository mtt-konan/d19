# Rank-Zero Selmer Tangent-Minus-One Reduction Partition

## Question

After the non-node, node-value, and punctured-node audits, what reduction-level
squareclass candidates remain for the tangent squareclass `-1` standard
families?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_minus_one_reduction_partition.py \
  --nonnode-branches results/closure_quotient_rank_zero_selmer_tangent_minus_one_nonnode_branches.json \
  --node-values results/closure_quotient_rank_zero_selmer_tangent_minus_one_node_values.json \
  --punctured-nodes results/closure_quotient_rank_zero_selmer_tangent_minus_one_punctured_nodes.json \
  --out results/closure_quotient_rank_zero_selmer_tangent_minus_one_reduction_partition.json \
  --strict
```

## Output

```text
status=ok
reduction_partition_count=2
reduction_partition_exhausted_count=2
punctured_node_neighborhood_excluded_count=2
formal_lift_compatibility_proved_count=0
local_image_schema_proved_count=0
```

## Interpretation

普通话说：`-1` 情况在 reduction 层已经可以整理成一个很小的 ledger：

```text
Y^2 = nu*X*(X - 1)^2      tracked X      candidates {nu, trivial}
Y^2 = nu*X^2*(1 - X)      tracked 1 - X  candidates {nu, trivial}
```

来源也清楚：

```text
nu      comes from the non-node branch
trivial comes from the node center
punctured node neighborhood is excluded by trivial != nu
```

这和 `tangent=1` 的情况不同。`tangent=1` 的候选集合只有 `{trivial}`；`tangent=-1`
在 reduction 层还保留 `{nu, trivial}`。这一步仍然只是局部工具的 reduction-level
收尾，不是完整 local image。

## Boundary

This records only reduction-level candidate squareclass sets and excluded
punctured neighborhoods. It does not prove formal lift compatibility, any local
image theorem, local condition, Selmer rank bound, or lambda-family exclusion.
