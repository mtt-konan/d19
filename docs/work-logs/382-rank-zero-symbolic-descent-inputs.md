# Rank-Zero Symbolic Descent Inputs

## Question

Can the three rank-zero family obligations be reduced one more step, from
observed primitive models to uniform symbolic inputs for a future descent proof?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_symbolic_descent_inputs.py \
  --primitive-models results/closure_quotient_rank_zero_primitive_models.json \
  --out results/closure_quotient_rank_zero_symbolic_descent_inputs.json \
  --strict
```

## Output

```text
status=ok
primitive_model_count=243
symbolic_formula_verified_count=243
selmer_rank_upper_bound_proved_count=0
family_exclusion_proved_count=0
```

## Interpretation

普通话说：`AA` 和 `BB` 的 rank-zero primitive models 共享同一个公式模板。
令 `T=A+B`，令 `L=A` for `AA`、`L=B` for `BB`，则

```text
p = 8L^2 - 2T^2
sqrt_q = T^2 + 4L^2
q = sqrt_q^2
```

对应的 2-torsion root differences 统一为：

```text
(-p) - 2*sqrt_q = -16L^2
(-p) - (-2*sqrt_q) = 4T^2
(2*sqrt_q) - (-2*sqrt_q) = 4(T^2 + 4L^2)
```

这把 243 个模型压成了一个符号 descent 输入模板。它是未来 2-isogeny/Selmer rank upper
bound 的输入，不是 rank-zero 证明本身。

## Boundary

`selmer_rank_upper_bound_proved_count=0` and `family_exclusion_proved_count=0`.
No lambda family is promoted to a proved exclusion here.
