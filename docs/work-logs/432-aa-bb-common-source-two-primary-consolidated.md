# wl432-wl438 — AA+BB common-source and 2-primary reduction consolidated

## Scope

This file replaces `wl432` through `wl438`.

## Result

The `AA+BB` seed group is the current smallest rank-zero theorem target.

Why:

```text
AA      candidate_class_count = 82
AA+BB   candidate_class_count = 43
BB      candidate_class_count = 75
```

The odd-prime work leaves `AA+BB` with less odd support than either one-sided
family. The remaining gap is now best described as:

```text
remaining_gap_kind = Selmer-layer lift of point-level collapse
```

The current compressed target is:

```text
Prove the AA+BB Selmer-layer lift: every relevant Selmer candidate satisfies
the common-source two-primary compatibility whose point-level collapse leaves
only (1,1,1).
```

## Source-Side Relation

All three kernel packages come from the same source curve with roots

```text
-p, 2*sqrt_q, -2*sqrt_q.
```

On the source curve, the three target coordinates satisfy:

```text
x_minus_p * x_pos_2sqrt_q * x_neg_2sqrt_q
  = (X-(-p))*(X-(2*sqrt_q))*(X-(-2*sqrt_q))
  = Y^2.
```

So for an actual common source rational point,

```text
x_minus_p * x_pos_2sqrt_q * x_neg_2sqrt_q
```

is a rational square.

Combined with the `AA+BB` odd-support collapse, this kills the remaining
odd-prime tail for actual rational points. The warning is important: a Selmer
candidate triple need not come from one common source point. The project still
has to lift this compatibility statement to the Selmer layer.

## Two-Primary Pattern Count

For a genuine common-source point in `AA+BB`, the odd valuation part is trivial
in all three kernel coordinates. Therefore each coordinate lies in

```text
<-1, 2> = {1, -1, 2, -2}.
```

The product-square relation leaves:

```text
4 choices for x_minus_p
4 choices for x_pos_2sqrt_q
the third class fixed by the product relation
=> 16 common-source 2-primary triple patterns
```

Those 16 patterns collapse to 5 multiplicative types:

```text
all_trivial                 size 1
minus_one_pair              size 3
two_pair                    size 3
minus_two_pair              size 3
fully_mixed_nontrivial      size 6
```

Plain meaning: after the common-source reduction, the hard part is no longer a
wide odd-prime problem. It is a small 2-primary pattern problem.

Follow-up through `wl460-wl463`: the local/common-source point-level work
collapses those nontrivial 2-primary patterns further. For genuine `AA+BB`
common-source rational points, the only remaining 2-primary triple is:

```text
(x_minus_p, x_pos_2sqrt_q, x_neg_2sqrt_q) = (1, 1, 1).
```

So this file's older "small 2-primary pattern problem" should now be read as
the historical reduction step, not the live target. The live target is the
Selmer-layer lift of this point-level collapse.

## Boundary

This consolidation keeps the `AA+BB` target choice, source-product identity,
and finite 2-primary pattern reduction. It does not prove that every Selmer
candidate comes from a common source point, does not prove a dyadic theorem,
does not prove a Selmer bound, and does not prove rank zero.
