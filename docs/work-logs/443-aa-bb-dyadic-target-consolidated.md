# wl439-wl446 — AA+BB dyadic target consolidated

## Scope

This file replaces `wl439` through `wl441` and `wl443` through `wl446`.

## Result

The dyadic route should not try to kill all patterns by a weak one-kernel
exclusion. The combinatorics says any independent per-kernel proof would need
to forbid at least

```text
6 kernel/class atoms
```

while keeping every kernel image nonempty. In minimal witnesses this means
each of the three kernels loses at least two classes.

This makes the next target more specific: work inside the Selmer-relevant
2-primary subgroup

```text
{1, -1, 2, -2}
```

instead of claiming a false full `Q_2*/Q_2*2` singleton image.

## Target Matrix

The 5 pattern types induce these support targets:

```text
all_trivial              each kernel sees {1}
minus_one_pair           each kernel sees {1, -1}
two_pair                 each kernel sees {1, 2}
minus_two_pair           each kernel sees {1, -2}
fully_mixed_nontrivial   each kernel sees {-1, 2, -2}
```

Keeping the trivial Selmer class changes the useful target. The 4
Selmer-relevant support shapes are:

```text
{1}, {1}, {1,-1,2,-2}
{1}, {1,-1}, {1,2,-2}
{1}, {1,2}, {1,-1,-2}
{1}, {1,-2}, {1,-1,2}
```

All four force at least one kernel to have singleton support. The selected
first target is:

```text
rank-zero-selmer-AA-BB-kernel-minus-p
x_minus_p(Q_2) ∩ {1,-1,2,-2} = {1}
```

This is not the same as saying `x_minus_p(Q_2) = {1}`. A finite check already
sees the class `5` in the full `Q_2` squareclass group for the sample `1:2`.

## Current Finite Sanity Checks

The subgroup-relative target survives the finite checks:

```text
sample pairs 1:2, 1:4, 3:5, 5:7:
observed x_minus_p(Q_2) ∩ {1,-1,2,-2} = {1}
```

Modulo `8`, the target is not closed by a coarse parity argument. The only
bucket that still shows the extra relevant class `2` is:

```text
odd-odd
```

Splitting odd-odd further gives:

```text
odd-odd + same mod 4      observed intersection = {1, 2}
odd-odd + opposite mod 4  observed intersection = {1}
```

So the live dyadic branch is:

```text
odd-odd same-mod-4 for x_minus_p.
```

Follow-up: this live branch is not a one-kernel singleton theorem. The
same-mod-4 branch has an explicit local class `2` on both one-sided
`kernel_minus_p` models (`wl461`), so the next obstruction must be
cross-kernel or Selmer-level compatibility rather than more local sampling.

Second follow-up: `wl462` proves the cross-kernel obstruction for genuine
common-source points. On the same-mod-4 branch, the other two kernels force
`x_pos_2sqrt_q` into `{1}` and `x_neg_2sqrt_q` into `{1,-1}` inside the
relevant subgroup, so `x_minus_p=2` violates the product relation. The
remaining gap is the Selmer-layer lift of that compatibility.

## Boundary

This consolidation keeps the dyadic target and finite sanity checks. It does
not prove the subgroup-relative dyadic theorem, any Selmer lift, any Selmer
rank bound, rank zero, or any `lambda` family exclusion.
