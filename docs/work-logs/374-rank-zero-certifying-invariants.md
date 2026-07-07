# Rank-Zero Certifying Invariants

## Question

After collapsing scaled `(A,B)` rows to primitive `lambda=A/B` models, what
invariants do the rank-zero certifying AA/BB models share?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_rank_zero_certifying_invariants.py \
  --primitive-models results/closure_quotient_rank_zero_primitive_models.json \
  --rank-jsonl results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --rank-jsonl results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --out results/closure_quotient_rank_zero_certifying_invariants.json \
  --strict
```

## Output

```text
status=ok
primitive_model_count=243
matched_primitive_model_count=243
matched_rank_row_count=275
family_exclusion_proved_count=0
```

Invariant counts after primitive collapse:

```text
rank_key_counts={'0/0': 243}
torsion_order_counts={'4': 243}
root_number_counts={'1': 243}
sha2_lower_value_counts={'0': 190, '2': 85}
```

Checks:

```text
all_matched_models_rank_zero=True
all_matched_models_torsion_order_four=True
all_matched_models_root_number_one=True
missing_primitive_model_count=0
```

## Interpretation

普通话说：原来的 275 条 certifying rank 行里有一些只是同一比例类的不同 scale。
折叠到本原 `lambda` 模型后，真正要研究的是 243 个 `class+curve` 模型。

这些模型在当前数据里共同满足：

- rank bounds 都闭合为 `0/0`；
- torsion order 都是 `4`；
- root number 都是 `1`。

这给后续 rank-zero 家族证明一个更干净的目标：不要再按 scale 增加样本，而是解释这些
本原 AA/BB 模型为什么落在 rank-zero、torsion-4、root-number-1 的结构里。

`sha2_lower` 仍然只是 rank 计算输出里的诊断字段；这里没有把它提升为证明。

## Boundary

This summarizes observed rank-zero certifying invariants after collapsing scaled
pairs to primitive lambda models. It does not prove any lambda-family exclusion
theorem.
