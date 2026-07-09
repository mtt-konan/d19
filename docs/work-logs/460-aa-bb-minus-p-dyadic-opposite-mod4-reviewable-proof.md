# AA+BB Minus-P Dyadic Opposite-Mod-4 Reviewable Proof

## Question

Can one narrow dyadic branch of

```text
rank-zero-selmer-AA-BB-kernel-minus-p
```

be written as a reviewable proof, rather than left as a finite residue sanity
check?

This note proves the odd-odd opposite-mod-4 branch for the subgroup-relevant
dyadic target:

```text
x_minus_p(Q_2) ∩ {1, -1, 2, -2}.
```

## Result

Yes. If `A` and `B` are odd and opposite modulo `4`, then `T=A+B` is divisible
by `4`. For either one-sided package, with `L=A` or `L=B`, the dyadic local
image of the `kernel_minus_p` coordinate satisfies:

```text
x_minus_p(Q_2) ∩ {1, -1, 2, -2} = {1}.
```

Therefore the same equality holds after imposing the `AA+BB` common-source
intersection.

普通话说：这不是完整 dyadic theorem。它只把之前 `odd-odd` bucket 里已经看起来
安全的一半，也就是 `A != B mod 4` 的分支，写成可逐行检查的证明。真正还活着的
困难分支仍然是 `odd-odd / same-mod-4`。

## Setup

The one-sided `kernel_minus_p` target model is

```text
E_L: y^2 = x^3 + (32*L^2 - 8*T^2)*x^2 + 16*(T^2 + 4*L^2)^2*x,
T = A+B.
```

Let

```text
Q_L(x) = x^2 + (32*L^2 - 8*T^2)*x + 16*(T^2 + 4*L^2)^2.
```

The tracked descent coordinate is the squareclass of `x`.

Assume throughout this proof that:

```text
L is odd,
T = 4*s with s in Z.
```

This is exactly what happens on both sides of `AA+BB` when `A` and `B` are
odd and opposite modulo `4`.

We use the standard `Q_2` squareclass labels:

```text
1, -1, 2, -2, 5, -5, 10, -10.
```

Here the relevant rational 2-primary subgroup is only:

```text
{1, -1, 2, -2}.
```

## Lemma 1: The Non-Middle Valuations Force Class 1

Let `m = v_2(x)`. If `m != 4`, then any local point whose `x`-class lies in
`{1, -1, 2, -2}` has `x`-class `1`.

## Proof Of Lemma 1

Write

```text
a2 = 32*L^2 - 8*T^2,
a4 = 16*(T^2 + 4*L^2)^2.
```

Since `L` is odd and `T=4*s`, we have:

```text
v_2(a2) = 5,
v_2(a4) = 8.
```

If `m < 4`, then

```text
Q_L(x) = x^2 * (1 + a2/x + a4/x^2).
```

For `m <= 2`, the parenthesized unit is congruent to `1 mod 8`, hence is a
square in `Q_2`. Thus `x*Q_L(x)` has the same squareclass as `x`, so the
existence of `y` forces `x` to be a square.

For `m = 3`, the parenthesized factor is still a unit, so

```text
v_2(x*Q_L(x)) = 3*m = 9,
```

which is odd. Hence no local point exists in this valuation.

If `m > 4`, then

```text
Q_L(x) = a4 * (1 + a2*x/a4 + x^2/a4).
```

For `m >= 6`, the parenthesized unit is congruent to `1 mod 8`, hence is a
square; since `a4` is already a square, the existence of `y` again forces
`x` to be a square.

For `m = 5`, the parenthesized factor is a unit and

```text
v_2(x*Q_L(x)) = m + 8 = 13,
```

which is odd. Hence no local point exists in this valuation.

So outside `m=4`, the only relevant subgroup class that can occur is `1`.

## Lemma 2: The Middle Valuation Has No Relevant Nontrivial Class

Let `m=4`, so `x=16*u` with `u` odd. If `x` lies in the relevant subgroup
`{1, -1, 2, -2}`, then any local point has `x`-class `1`.

## Proof Of Lemma 2

Since `m=4`, the class of `x` is a unit class. Inside the relevant subgroup,
the only unit classes are:

```text
1, -1.
```

So it remains to rule out the class `-1`, i.e. `u == 7 mod 8`.

Put

```text
d = L^2 + 4*s^2,
c = 2*L^2 - 8*s^2.
```

Then

```text
T^2 + 4*L^2 = 4*d,
a2 = 16*c,
a4 = 256*d^2.
```

For `x=16*u`,

```text
Q_L(16*u) = 256 * H,
H = u^2 + c*u + d^2.
```

A direct completion gives

```text
H = (u + L^2 - 4*s^2)^2 + (4*L*s)^2.
```

Now use the elementary `Q_2` fact that a nonzero sum of two rational squares
has squareclass in

```text
{1, 2, 5, 10}.
```

Indeed, after removing the smaller square factor, unequal valuations give a
unit congruent to either `1` or `5 mod 8`; equal valuations reduce to the sum
of two odd squares, which has squareclass `2` or `10`.

Thus `H` never has squareclass `-1`. But

```text
x*Q_L(x) = 2^12 * u * H.
```

If `u` had class `-1`, then `u*H` could be a square only if `H` also had class
`-1`. This is impossible. Therefore the relevant class `-1` cannot occur at
`m=4`.

The only relevant subgroup class left at `m=4` is `1`.

## Theorem

For `A` and `B` odd with `A != B mod 4`, the `AA+BB / kernel_minus_p` dyadic
opposite-mod-4 branch satisfies

```text
x_minus_p(Q_2) ∩ {1, -1, 2, -2} = {1}.
```

## Proof

If `A` and `B` are odd and opposite modulo `4`, then `T=A+B` is divisible by
`4`.

On the `AA` side, `L=A` is odd and Lemma 1 plus Lemma 2 show that the relevant
subgroup intersection is only `{1}`.

On the `BB` side, `L=B` is odd and the same proof applies.

The `AA+BB` common-source condition takes the intersection of the two
one-sided conditions. Since each side already has relevant subgroup
intersection `{1}`, the common-source branch also has intersection `{1}`.

## Conclusion

The dyadic opposite-mod-4 branch of
`rank-zero-selmer-AA-BB-kernel-minus-p` is now a reviewable proof segment:

```text
odd-odd, A != B mod 4:
  x_minus_p(Q_2) ∩ {1, -1, 2, -2} = {1}.
```

This turns the finite observation from `wl446` into an actual local proof for
that half of the odd-odd bucket. The remaining dyadic obstruction is still the
same-mod-4 branch, where the finite sanity checks still see class `2`.

## Boundary

This note does not prove:

- the same-mod-4 dyadic branch,
- the full `Q_2*/Q_2*2` local image,
- a Selmer lift from common-source points to Selmer classes,
- a global Selmer dimension bound,
- rank zero,
- any family-level lambda exclusion.

It records one review-ready dyadic branch only.
