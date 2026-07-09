# AA+BB D2 Multi-Collision Overlaps

## Question

In the complete `d`-coordinate route for

```text
E_L: Y^2 = (X+p)*(X^2 - 4*q),
```

can an odd prime `ell` divide at least two of

```text
L, T, sqrt_q
```

under the AA+BB primitive normalization? If such overlaps can occur, they
would require a genuine multi-collision local `C_d` row rather than one of the
pure odd rows `wl475`-`wl477`.

## Result

`D2_multi_collision_overlaps` is discharged: odd overlaps are impossible under
the primitive AA+BB inputs.

The only arithmetic identity needed is

```text
sqrt_q = T^2 + 4*L^2.
```

For odd `ell`, the exact gcd lemma is:

```text
ell divides at least two of {L,T,sqrt_q}
if and only if
ell divides gcd(L,T).
```

In that case `ell` divides all three.

Equivalently:

```text
ell | L and ell | T      => ell | sqrt_q
ell | L and ell | sqrt_q => ell | T
ell | T and ell | sqrt_q => ell | L
```

The last implication uses that `ell` is odd, so `4` is a unit modulo `ell`.

The AA+BB primitive normalization supplies the missing input:

```text
A:B primitive, so gcd(A,B)=1
T=A+B
L=A on the AA side, or L=B on the BB side
```

Therefore

```text
gcd(L,T)=1.
```

So no odd prime can divide at least two of `L`, `T`, and `sqrt_q` in the
normalized AA+BB route.

## Complete Local Row

The complete local `C_d` row for odd multi-collision overlaps is vacuous:

```text
complete_local_c_d_row_for_overlaps = vacuous_empty_row
```

No additional allowed squareclass triples are introduced. The prior pure odd
rows cover the odd bad-prime alternatives:

```text
ell | L       handled by wl475
ell | T       handled by wl476
ell | sqrt_q  handled by wl477
```

The dyadic row remains the separate `ell=2` case handled by `wl478`.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_d2_multi_collision_overlaps.json
```

with:

```text
status = ok
d2_multi_status = odd_multi_collision_overlaps_impossible_under_primitive_normalization
multi_collision_overlaps_possible_under_aa_bb_inputs = false
complete_local_c_d_row_for_overlaps = vacuous_empty_row
local_c_d_rows_solved = true
full_c_d_matrix_built = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
```

## Boundary

This work-log stops after discharging the D2 odd multi-collision overlap
obligation. It does not:

- build D4,
- combine local rows into a complete Selmer upper bound,
- prove `dim Sel_2(E)=2`,
- prove rank zero,
- prove `Sha[2]=0`,
- prove any family exclusion theorem.

It also does not advance to the next roadmap step.
