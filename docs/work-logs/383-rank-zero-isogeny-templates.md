# Rank-Zero Isogeny Templates

## Question

Can the symbolic descent input be converted into concrete 2-isogeny target
templates for the three rational 2-torsion kernels?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_isogeny_templates.py \
  --symbolic-inputs results/closure_quotient_rank_zero_symbolic_descent_inputs.json \
  --out results/closure_quotient_rank_zero_isogeny_templates.json \
  --strict
```

## Output

```text
status=ok
primitive_model_count=243
isogeny_template_verified_count=729
selmer_rank_upper_bound_proved_count=0
family_exclusion_proved_count=0
```

## Interpretation

普通话说：每个 rank-zero primitive model 有 3 个 rational 2-torsion kernel。
这一步把 243 个模型全部转成 3 类 2-isogeny 目标模板，共检查 729 次：

```text
kernel -p:
  y^2 = x^3 + 4p*x^2 + 16*sqrt_q^2*x
  a4 = (4*(T^2 + 4L^2))^2

kernel 2*sqrt_q:
  y^2 = x^3 + (-2p - 12*sqrt_q)*x^2 + (p - 2*sqrt_q)^2*x
  a4 = (4*T^2)^2

kernel -2*sqrt_q:
  y^2 = x^3 + (-2p + 12*sqrt_q)*x^2 + (p + 2*sqrt_q)^2*x
  a4 = (16*L^2)^2
```

这些模板是下一步 uniform 2-isogeny/Selmer rank upper bound 的输入。

## Boundary

`selmer_rank_upper_bound_proved_count=0` and `family_exclusion_proved_count=0`.
This does not compute Selmer groups and does not prove rank zero.
