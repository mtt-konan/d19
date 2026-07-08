# Rank-Zero Selmer Tangent-One Reduction Partition

## Question

After the non-node, punctured-node, and node-value audits, what reduction-level
squareclass candidates remain for the two tangent-one standard models?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_one_reduction_partition.py \
  --nonnode-branches results/closure_quotient_rank_zero_selmer_tangent_one_nonnode_branches.json \
  --node-values results/closure_quotient_rank_zero_selmer_tangent_one_node_values.json \
  --punctured-nodes results/closure_quotient_rank_zero_selmer_tangent_one_punctured_nodes.json \
  --out results/closure_quotient_rank_zero_selmer_tangent_one_reduction_partition.json \
  --strict
```

## Output

```text
status=ok
reduction_partition_count=2
reduction_partition_exhausted_count=2
formal_lift_compatibility_proved_count=0
local_image_schema_proved_count=0
```

## Interpretation

普通话说：在 reduction 层，两个 tangent-one 标准模型已经可以整理成很小的候选集合：

```text
Y^2 = X*(X - 1)^2      tracked X      candidates {trivial}
Y^2 = X^2*(1 - X)      tracked 1 - X  candidates {trivial}
```

这把前面几层的分支信息汇总成了 ledger：非节点、穿孔节点邻域、节点中心都已经
在 reduction 层登记。还没证明的是这些 reduction 层候选如何通过原曲线的
formal lifts 变成真正的 local image。

Note: this corrects the earlier sign convention for the zero-double-root
tangent-one normal form. The coordinate change gives `1-X`, not `X-1`.

## Boundary

This records only reduction-level candidate squareclass sets. It does not prove
formal lift compatibility, any local image theorem, local condition, Selmer
rank bound, or lambda-family exclusion.
