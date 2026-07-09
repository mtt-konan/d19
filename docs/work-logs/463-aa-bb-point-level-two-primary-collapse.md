# AA+BB Point-Level Two-Primary Collapse

## Question

After `wl460` through `wl462`, what exactly remains of the `AA+BB`
two-primary obstruction?

## Result

For genuine common-source rational points, the nontrivial two-primary patterns
are gone. The only possible rational 2-primary triple is:

```text
(x_minus_p, x_pos_2sqrt_q, x_neg_2sqrt_q) = (1, 1, 1).
```

This does **not** prove the Selmer theorem. The correct next formulation is no
longer "make rational points lift to Selmer classes." In complete 2-descent,
Selmer membership is already local common-source membership at every place.
The next theorem is therefore an upper-bound problem:

```text
build a pseudo-Selmer container S~ in the complete 2-descent coordinates,
then check whether its F2 dimension is forced down to 2.
```

普通话说：局部点层面的分支已经不应该继续拆了。真正剩下的是 complete 2-descent 的
上界账本，不是更多 `A:B` 样本，也不是把 rational point 硬说成 Selmer class。

## Setup

Work inside the relevant rational 2-primary subgroup:

```text
G = {1, -1, 2, -2}.
```

For a genuine common-source point, the three target coordinates satisfy:

```text
x_minus_p * x_pos_2sqrt_q * x_neg_2sqrt_q = 1
```

as squareclasses.

The odd-prime work has already removed odd valuation support from
`x_minus_p` and `x_neg_2sqrt_q`; `x_pos_2sqrt_q` has no independent
common-source odd valuation after the product relation. Thus the remaining
point-level question is only about `G`.

## Dyadic Inputs

The dyadic branch results now needed are:

```text
opposite-mod-4 branch:
  x_minus_p ∈ {1}                         (wl460)

same-mod-4 branch:
  x_minus_p = 2 is locally possible       (wl461)
  but incompatible with the other kernels (wl462)
```

The other two kernel bounds used in the compatibility check are:

```text
x_pos_2sqrt_q ∈ {1, 2}
x_neg_2sqrt_q ∈ {1, -1}
```

inside `G` on the odd-odd dyadic branch. In the same-mod-4 subbranch, `wl462`
sharpens the first line to `x_pos_2sqrt_q ∈ {1}`.

## Theorem

For a genuine `AA+BB` common-source rational point, the only possible
2-primary squareclass triple in `G^3` is:

```text
(1, 1, 1).
```

## Proof

Split the odd-odd branch by congruence modulo `4`.

### Opposite Modulo 4

By `wl460`,

```text
x_minus_p = 1.
```

The product relation becomes:

```text
x_pos_2sqrt_q * x_neg_2sqrt_q = 1.
```

But the dyadic bounds give:

```text
x_pos_2sqrt_q ∈ {1, 2}
x_neg_2sqrt_q ∈ {1, -1}.
```

The only pair from these two sets whose product is `1` is:

```text
x_pos_2sqrt_q = 1,
x_neg_2sqrt_q = 1.
```

So the opposite-mod-4 branch gives only `(1,1,1)`.

### Same Modulo 4

By `wl462`, the locally admissible same-mod-4 class

```text
x_minus_p = 2
```

is incompatible with the product relation and the other two kernel images.
Therefore `x_minus_p` cannot be `2` for a genuine common-source point.

The remaining local option in `G` is:

```text
x_minus_p = 1.
```

Again the product relation gives:

```text
x_pos_2sqrt_q * x_neg_2sqrt_q = 1.
```

On this branch, `wl462` gives:

```text
x_pos_2sqrt_q ∈ {1},
x_neg_2sqrt_q ∈ {1, -1}.
```

Thus `x_neg_2sqrt_q` must also be `1`.

So the same-mod-4 branch also gives only `(1,1,1)`.

## Conclusion

At the common-source rational-point level:

```text
AA+BB two-primary nontrivial patterns = none.
```

The remaining gap is not another point-level local enumeration. In the
complete 2-descent framing, the product relation and local common-source
condition are part of Selmer membership. The next cheaper audit is:

```text
Sel_2(E) subset S~,
dim_F2 S~ <= 2 + omega_{1 mod 4}(T) + epsilon_sign.
```

Only if this pseudo-container collapses to dimension `2` can it become a
rank-zero Selmer theorem candidate. Otherwise the route has to attack the
remaining `ell | T`, `ell == 1 mod 4` tail, the sign bit, or a genuine
`Sha[2]` obstruction.

Follow-ups `wl464` and `wl465` recast this as a complete 2-descent and
pseudo-Selmer upper-bound audit. The full `C_d` local matrix should not be
built until the cheaper `S~` dimension audit says it is actually needed.

## Boundary

This note does not prove:

- a Selmer rank upper bound,
- rank zero,
- any lambda-family exclusion.

It packages the point-level two-primary collapse and identifies the exact
remaining theorem target.
