# Rank-Zero Family Formal-Lift Coverage

## Question

Across the three primitive rank-zero lambda families

```text
AA, AA+BB, BB,
```

which ones already have reviewable odd-prime `formal_lift_compatibility`
segments on every package?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_family_formal_lift_coverage.py \
  --family-obligations results/closure_quotient_rank_zero_family_obligations.json \
  --package-segments results/closure_quotient_rank_zero_selmer_package_segments.json \
  --out results/closure_quotient_rank_zero_family_formal_lift_coverage.json \
  --strict
```

## Output

```text
status=ok
family_count=3
reviewable_formal_lift_package_count=7
```

The family rows are:

```text
AA     -> 3/3 packages have reviewable formal-lift segments
AA+BB  -> 1/3
BB     -> 3/3 packages have reviewable formal-lift segments
```

## Result

The `AA` and `BB` families have both completed the odd-prime
`formal_lift_compatibility` segment across all three Selmer packages.
`AA+BB` now has its first package-level segment at this field.

In ordinary language: this is not a rank-zero proof. It only says which
odd-prime proof segments are now written clearly enough to review:

```text
AA: complete at this segment layer
BB: complete at this segment layer
AA+BB: started at this segment layer
```

So `AA` and `BB` should not keep revisiting odd-prime formal lift. Their next
blockers are:

- dyadic local condition,
- global Selmer dimension bound,
- rank-zero conclusion.

For `AA+BB`, the immediate state is `1/3`: the `kernel_neg_2sqrt_q` odd-prime
valuation support segment is reviewable, while `kernel_minus_p` and
`kernel_pos_2sqrt_q` remain open at this package layer.

## Boundary

This still does not prove:

- any dyadic local condition,
- any Selmer rank bound,
- rank zero,
- or any `lambda` family exclusion.
