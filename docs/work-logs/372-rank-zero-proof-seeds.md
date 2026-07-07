# Rank-Zero Proof Seeds

## Question

For the 200 rank-zero family candidates, can we group the primitive AA/BB
models into a small number of proof-seed patterns?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_rank_zero_proof_seeds.py \
  --primitive-models results/closure_quotient_rank_zero_primitive_models.json \
  --out results/closure_quotient_rank_zero_proof_seeds.json \
  --strict
```

## Output

```text
status=ok
seed_group_count=3
candidate_class_count=200
model_count=243
family_exclusion_proved_count=0
```

Groups:

```text
AA: candidate_class_count=82, model_count=82, p_sign_counts={'negative': 82}
AA+BB: candidate_class_count=43, model_count=86, p_sign_counts={'negative': 43, 'positive': 43}
BB: candidate_class_count=75, model_count=75, p_sign_counts={'positive': 75}
```

## Interpretation

普通话说：这一步把 200 个 rank-zero 候选比例类压成 3 个后续证明入口。

- `AA` 组只看到 AA 机制，且对应 `p` 全为负。
- `BB` 组只看到 BB 机制，且对应 `p` 全为正。
- `AA+BB` 组两边都有，AA 的 `p` 为负，BB 的 `p` 为正。

这说明下一步不该继续按单个 `(A,B)` 增加证书数量，而应该尝试证明这些模式背后的本原
`lambda=A/B` 族结构。这个 ledger 只是把证明入口整理清楚。

## Boundary

This groups rank-zero primitive model seeds for future lambda-family proof work.
It does not prove any family exclusion theorem.
