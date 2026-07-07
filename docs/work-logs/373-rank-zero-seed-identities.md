# Rank-Zero Seed Identities

## Question

Do the rank-zero proof-seed `p` signs carry new structure, or are they forced by
the primitive ray ordering?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_seed_identities.py \
  --primitive-models results/closure_quotient_rank_zero_primitive_models.json \
  --out results/closure_quotient_rank_zero_seed_identity_audit.json \
  --strict
```

## Output

```text
status=ok
coefficient_identity_verified_count=243
coefficient_identity_violation_count=0
p_sign_novel_signal_count=0
```

Forced signs:

```text
AA: negative = 125
BB: positive = 118
```

## Interpretation

普通话说：`p` 的正负不是新发现的 rank-zero 线索。

对本原无向比例类，我们按 `0 < a < b` 记录。于是：

```text
AA: p = 8a^2 - 2(a+b)^2 = 2(3a^2 - 2ab - b^2) < 0
BB: p = 8b^2 - 2(a+b)^2 = 2(3b^2 - 2ab - a^2) > 0
```

所以 wl372 里看到的 `AA` 全负、`BB` 全正，只是排序和公式带来的结果。
后续不能把这个符号现象当成证明入口。真正还需要研究的是这些本原模型的 rank-zero
家族结构，或者转向 root-number / 2-cover 的整族障碍。

## Boundary

This audits coefficient identities and forced p-signs for rank-zero proof seeds.
It does not prove rank zero or a family exclusion theorem.
