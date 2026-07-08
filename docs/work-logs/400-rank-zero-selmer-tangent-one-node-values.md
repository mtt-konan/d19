# Rank-Zero Selmer Tangent-One Node Values

## Question

What can be safely recorded at the two tangent-one nodes before doing formal
neighborhood or local-lift analysis?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_one_node_values.py \
  --tangent-one-normal-forms results/closure_quotient_rank_zero_selmer_odd_prime_tangent_one_normal_forms.json \
  --out results/closure_quotient_rank_zero_selmer_tangent_one_node_values.json \
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

普通话说：两个 tangent-one 标准模型的节点坐标本身可以直接读出来：

```text
Y^2 = X*(X - 1)^2    node (X,Y)=(1,0), so X=1
Y^2 = X^2*(1 - X)    node (X,Y)=(0,0), so 1-X=1
```

这只说明 reduction 层的节点值。真正难的是：原来的光滑曲线里，那些约化到节点
附近的局部点，会在 local squareclass image 里贡献什么。这需要 formal
neighborhood / local-lift 分析，所以这里仍然不关闭 local image。

## Boundary

This proves only reduction-level node coordinates and coordinate values on the
two tangent-one standard models. It does not prove node lift analysis, any
local image theorem, local condition, Selmer rank bound, or lambda-family
exclusion.
