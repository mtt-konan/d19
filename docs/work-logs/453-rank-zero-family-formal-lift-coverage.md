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
reviewable_formal_lift_package_count=9
```

The family rows are:

```text
AA     -> 3/3 packages have reviewable formal-lift segments
AA+BB  -> 3/3 packages have reviewable formal-lift segments
BB     -> 3/3 packages have reviewable formal-lift segments
```

## Result

The `AA`, `AA+BB`, and `BB` families have completed the odd-prime
`formal_lift_compatibility` segment across all three Selmer packages.

In ordinary language: this is not a rank-zero proof. It only says which
odd-prime proof segments are now written clearly enough to review:

```text
AA: complete at this segment layer
BB: complete at this segment layer
AA+BB: complete at this segment layer
```

So none of the three rank-zero families should keep revisiting odd-prime
formal lift as the next main task. Their next blockers are:

- dyadic local condition,
- global Selmer dimension bound,
- rank-zero conclusion.

For `AA+BB`, the completed narrow layer is:

```text
kernel_neg_2sqrt_q    no odd-prime valuation support
kernel_minus_p        no odd-prime valuation support
kernel_pos_2sqrt_q    support only from ell | T, ell == 1 mod 4
```

This last line is deliberately weaker than "no odd support"; it records the
remaining odd-prime tail that the dyadic/global work must still handle.

## Boundary

This still does not prove:

- any dyadic local condition,
- any Selmer rank bound,
- rank zero,
- or any `lambda` family exclusion.
