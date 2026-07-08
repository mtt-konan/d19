# Rank-Zero Selmer Tangent-Minus-One Node Values

## Question

What reduction-level value can be safely recorded at the nodes of the tangent
squareclass `-1` standard families?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_minus_one_node_values.py \
  --tangent-minus-one-normal-forms results/closure_quotient_rank_zero_selmer_tangent_minus_one_normal_forms.json \
  --out results/closure_quotient_rank_zero_selmer_tangent_minus_one_node_values.json \
  --strict
```

## Output

```text
status=ok
input_normal_form_count=2
node_value_count=2
node_reduction_value_proved_count=2
node_local_lift_analysis_proved_count=0
local_image_schema_proved_count=0
```

## Interpretation

普通话说：`-1` 的两个标准模型虽然在非节点分支上带着 nonsquare unit `nu`，
但节点中心本身还是落在 tracked coordinate 等于 `1` 的位置：

```text
Y^2 = nu*X*(X-1)^2,     node (X,Y)=(1,0), tracked X = 1
Y^2 = nu*X^2*(1-X),     node (X,Y)=(0,0), tracked 1-X = 1
```

所以节点中心给出的平方类是 trivial。和上一层合起来看，`-1` 情况现在有一个
清楚的 reduction-level 图像：非节点分支给 `nu`，节点中心给 trivial。

## Boundary

This proves only reduction-level node values. It does not prove formal lift
analysis, any local image theorem, local condition, Selmer rank bound, or
lambda-family exclusion.
