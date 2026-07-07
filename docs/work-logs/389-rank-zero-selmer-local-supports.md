# Rank-Zero Selmer Local Supports

## Question

Can the 9 rank-zero Selmer packages be refined from generic transcript tasks
to explicit symbolic local-support candidates?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_local_supports.py \
  --package-index results/closure_quotient_rank_zero_selmer_package_index.json \
  --out results/closure_quotient_rank_zero_selmer_local_supports.json \
  --strict
```

## Output

```text
status=ok
package_count=9
support_entry_count=9
local_condition_proved_count=0
selmer_rank_upper_bound_proved_count=0
family_exclusion_proved_count=0
```

## Symbolic Support

For the isogenous target curve

```text
y^2 = x^3 + a2*x^2 + a4*x
```

the quadratic factor has discriminant `a2^2 - 4a4`. The three kernel templates
give:

```text
kernel_minus_p:
  a2 = 32*L^2 - 8*T^2
  a4 = 16*(T^2 + 4*L^2)^2
  a2^2 - 4a4 = -1024*L^2*T^2
  squareclass = -1

kernel_pos_2sqrt_q:
  a2 = -8*(T^2 + 8*L^2)
  a4 = 16*T^4
  a2^2 - 4a4 = 1024*L^2*(T^2 + 4*L^2)
  squareclass = T^2 + 4*L^2

kernel_neg_2sqrt_q:
  a2 = 16*(T^2 + 2*L^2)
  a4 = 256*L^4
  a2^2 - 4a4 = 256*T^2*(T^2 + 4*L^2)
  squareclass = T^2 + 4*L^2
```

Thus the uniform candidate bad factors for future local checks are:

```text
2, L, T, T^2 + 4*L^2
```

## Interpretation

普通话说：这一步没有证明 local Selmer condition，但它把未来 transcript 里最难含糊的
输入先写清楚了：每个 package 应该围绕同一组符号因子做局部检查。

## Boundary

`support_candidates_not_conditions=True`. No local condition, Selmer rank bound,
rank-zero theorem, or lambda-family exclusion is proved here.
