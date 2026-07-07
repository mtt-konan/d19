# Rank-Zero Selmer Obligations

## Question

After the 2-isogeny templates are verified, what exactly remains before the
rank-zero route can claim a uniform rank bound?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_obligations.py \
  --family-obligations results/closure_quotient_rank_zero_family_obligations.json \
  --isogeny-templates results/closure_quotient_rank_zero_isogeny_templates.json \
  --out results/closure_quotient_rank_zero_selmer_obligations.json \
  --strict
```

## Output

```text
status=ok
family_obligation_count=3
kernel_count=3
selmer_obligation_count=9
selmer_rank_upper_bound_proved_count=0
family_exclusion_proved_count=0
```

## Interpretation

普通话说：rank-zero 主线现在已经不是 243 个模型，也不是 729 个模板检查。
它被压成 9 个明确的 Selmer 证明义务：

```text
3 个 family pattern: AA, AA+BB, BB
3 个 2-isogeny kernel: kernel_minus_p, kernel_neg_2sqrt_q, kernel_pos_2sqrt_q
```

每个 family pattern 都需要对 3 个 kernel 给出 uniform isogeny-Selmer rank upper bound。

## Boundary

`rank_zero_selmer_obligations_complete=False`,
`selmer_rank_upper_bound_proved_count=0`, and `family_exclusion_proved_count=0`.
This does not compute Selmer groups and does not prove rank zero.
