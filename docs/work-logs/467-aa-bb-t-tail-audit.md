# AA+BB T-Tail Audit

## Question

After `wl466` killed the archimedean sign tail, does the remaining

```text
ell | T,
ell == 1 mod 4
```

tail survive in the AA+BB complete 2-descent pseudo-Selmer container `S~`?

## Result

No. The tail is killed inside the cheap `S~` valuation ledger. For each odd
prime

```text
ell | T,
ell == 1 mod 4,
```

the previous AA+BB odd-prime rows leave a possible odd valuation in only one
coordinate:

```text
x_minus_p        valuation parity 0        wl458
x_pos_2sqrt_q    possible tail bit          wl459
x_neg_2sqrt_q    valuation parity 0        wl457
```

But the complete 2-descent product relation gives

```text
x_minus_p * x_pos_2sqrt_q * x_neg_2sqrt_q = 1 in Q*/Q*2,
```

so at every such prime the valuation parities satisfy

```text
0 + tail_bit + 0 = 0 in F2.
```

Hence

```text
tail_bit = 0.
```

The exact `T`-tail dimension in the pseudo-container is therefore

```text
0.
```

No joint `C_d` local-solubility matrix is needed to account for this tail.

## Dimension Ledger

The ledger after `wl466` was

```text
dim_F2 S~ <= 2 + omega_{1 mod 4}(T).
```

The parity argument above removes the last symbolic tail term:

```text
dim_F2 S~ <= 2.
```

Since the torsion baseline already has dimension `2`, this means the cheap
AA+BB pseudo-container has no remaining non-torsion tail in this ledger.

## Why This Is Cheap

This audit uses only:

```text
1. wl457 and wl458: the other two odd-prime supports are killed,
2. wl459: the only possible remaining odd-prime support was the pos coordinate,
3. wl464: the product relation among the three complete-descent coordinates,
4. wl466: epsilon_sign = 0.
```

It does not enumerate local points on a `C_d` cover and does not build the full
complete 2-descent local matrix.

## Result Artifact

The machine-checkable audit is:

```text
results/closure_quotient_rank_zero_aa_bb_t_tail.json
```

with:

```text
t_tail.status = killed
t_tail.tail_dimension = 0
dimension_bound_update.upper_bound = dim_F2 S~ <= 2
route_decision.requires_joint_C_d_local_conditions_for_this_tail = false
```

## Boundary

This note proves only the scoped `T`-tail statement for the AA+BB
pseudo-Selmer container `S~`.

It does not prove:

- `dim Sel_2(E)=2` for a single curve,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.

It also stops after the `T`-tail audit, as requested. Promoting this into a
full rank-zero theorem would require a separately checked theorem-level bridge
from this pseudo-container ledger to the relevant complete Selmer upper bound.
