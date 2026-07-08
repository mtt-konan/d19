# Rank-Zero Selmer Tangent-One Punctured Nodes

## Question

Do the tangent-one node neighborhoods require a new calculation away from the
node center?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_one_punctured_nodes.py \
  --nonnode-branches results/closure_quotient_rank_zero_selmer_tangent_one_nonnode_branches.json \
  --node-values results/closure_quotient_rank_zero_selmer_tangent_one_node_values.json \
  --out results/closure_quotient_rank_zero_selmer_tangent_one_punctured_nodes.json \
  --strict
```

## Output

```text
status=ok
input_nonnode_branch_count=2
input_node_value_count=2
punctured_node_neighborhood_control_proved_count=2
node_center_lift_analysis_proved_count=0
local_image_schema_proved_count=0
```

## Interpretation

普通话说：节点附近但不等于节点中心的点，仍然可以用上一层的非节点恒等式控制：

```text
Y^2 = X*(X - 1)^2,   X - 1 != 0  =>  X = (Y/(X - 1))^2
Y^2 = X^2*(X - 1),   X != 0      =>  X - 1 = (Y/X)^2
```

所以“穿孔节点邻域”不需要另开一个搜索分支。剩下的真正问题更窄：节点中心
本身的 formal lift / compatibility 怎么处理，以及 tangent squareclass 为 `-1`
的两个 schema 怎么处理。

## Boundary

This proves only that punctured node neighborhoods are controlled by the
non-node branch identities. It does not prove node-center lift analysis, any
local image theorem, local condition, Selmer rank bound, or lambda-family
exclusion.
