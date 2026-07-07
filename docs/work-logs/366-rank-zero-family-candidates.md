# Rank-Zero Family Candidates

## Question

Which primitive `lambda=A/B` classes should be studied first for an `AA/BB`
rank-zero family mechanism?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_rank_zero_family_candidates.py \
  --ray-ledger results/closure_quotient_ray_ledger.json \
  --out results/closure_quotient_rank_zero_family_candidates.json \
  --strict
```

## Output

```text
status=ok
candidate_class_count=200
strict_observed_pair_count=220
family_exclusion_proved_count=0
certifying_curve_pattern_counts={'AA': 125, 'BB': 118}
```

## Interpretation

普通话说：这一步把 `lambda` frontier 里的 `rank-zero-family-generalization`
路线拆细。现在有 200 个本原比例类值得优先研究 `AA/BB rank-zero` 机制是否能整族化；
这些类对应 220 个已经由局部工具严格覆盖的观测 pair。

`AA` 机制在 125 个候选类中出现，`BB` 机制在 118 个候选类中出现；有些类同时出现
`AA` 和 `BB`。

这一步只是候选清单。它没有证明这些比例类已经整族排除。下一步要做的是从这些候选类里
挑出可公式化的子族，证明 rank-zero / torsion 回拉机制在整个本原 `lambda` 类上成立。

## Boundary

This is a candidate list for family-level proof work. It is not a family
exclusion theorem.
