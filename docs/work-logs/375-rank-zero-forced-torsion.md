# Rank-Zero Forced Torsion

## Question

In the rank-zero certifying invariant ledger, is `torsion_order=4` a new deep
signal, or is part of it forced by the primitive AA/BB model formula?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_forced_torsion.py \
  --primitive-models results/closure_quotient_rank_zero_primitive_models.json \
  --certifying-invariants results/closure_quotient_rank_zero_certifying_invariants.json \
  --out results/closure_quotient_rank_zero_forced_torsion_audit.json \
  --strict
```

## Output

```text
status=ok
primitive_model_count=243
forced_full_two_torsion_count=243
observed_exact_torsion_order_four_count=243
family_exclusion_proved_count=0
```

## Interpretation

普通话说：`torsion_order=4` 这件事要拆开看。

这些本原 AA/BB 模型都有：

```text
E: V^2 = X^3 + pX^2 - 4qX - 4pq
q = sqrt_q^2
```

所以右边可以写成：

```text
(X+p)(X^2 - 4q)
```

也就是说三个 2-torsion 的 `X` 坐标

```text
X = -p, 2sqrt_q, -2sqrt_q
```

都已经是有理数。这说明“至少有完整 rational 2-torsion”是模型公式强制出来的，不是新
rank-zero 证明线索。

当前数据里额外看到的是：这些模型的 torsion 阶正好都是 `4`，也就是没有额外 torsion。
后续 rank-zero 家族证明真正要解释的是 rank 为什么整族为 0；torsion-4 本身不应该被当成主突破口。

## Boundary

This audits the rational 2-torsion forced by `q` being a square in the
rank-zero primitive models. It does not prove rank zero or a lambda-family
exclusion theorem.
