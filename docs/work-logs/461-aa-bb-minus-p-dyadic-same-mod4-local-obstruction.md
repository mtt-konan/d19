# AA+BB Minus-P Dyadic Same-Mod-4 Local Obstruction

## Question

Can the remaining `odd-odd / same-mod-4` branch of

```text
rank-zero-selmer-AA-BB-kernel-minus-p
```

be closed by the same subgroup-singleton dyadic theorem used in the
opposite-mod-4 branch?

## Result

No. The singleton statement is false on this branch. If `A` and `B` are odd
and equal modulo `4`, then `T=A+B=2*s` with `s` odd. For every odd `L`, the
one-sided `kernel_minus_p` local model has a `Q_2` point whose tracked
`x`-class is `2`.

Therefore, on the `AA+BB` same-mod-4 branch, the class `2` survives both the
`L=A` and `L=B` one-sided dyadic local conditions. The next proof cannot be a
one-kernel local singleton theorem for `x_minus_p`; it must use cross-kernel
or Selmer-level compatibility.

普通话说：这一步不是“又加一个 case”。它把错误路线剪掉了：same-mod-4 这半边不能靠
`x_minus_p(Q_2) ∩ {1,-1,2,-2} = {1}` 解决，因为 class `2` 确实有局部点。

## Setup

The one-sided `kernel_minus_p` target model is

```text
E_L: y^2 = x^3 + (32*L^2 - 8*T^2)*x^2 + 16*(T^2 + 4*L^2)^2*x.
```

Write

```text
Q_L(x) = x^2 + (32*L^2 - 8*T^2)*x + 16*(T^2 + 4*L^2)^2.
```

Assume

```text
L odd,
T = 2*s with s odd.
```

This covers both one-sided packages when `A` and `B` are odd and equal modulo
`4`, since then `T=A+B` has exact 2-adic valuation `1`, and both `L=A` and
`L=B` are odd.

## Lemma

For every odd `L` and odd `s`, the point with

```text
x = -224
```

has square RHS on `E_L` with `T=2*s`. Moreover, the `Q_2` squareclass of
`x=-224` is `2`.

## Proof

Put

```text
x = 32*u,
u = -7.
```

Then `v_2(x)=5`, and the odd unit part of `x` is `u == 1 mod 8`. Hence the
`Q_2` squareclass of `x` is `2`.

Now substitute `T=2*s` into the quadratic factor:

```text
32*L^2 - 8*T^2 = 32*(L^2 - s^2),
16*(T^2 + 4*L^2)^2 = 256*(s^2 + L^2)^2.
```

Therefore

```text
Q_L(32*u) = 256 * H,
H = 4*u^2 + 4*u*(L^2 - s^2) + (s^2 + L^2)^2.
```

For `u=-7`, this is

```text
H = 196 - 28*(L^2 - s^2) + (s^2 + L^2)^2.
```

Because odd squares are `1 mod 8`, a direct reduction modulo `128` gives

```text
H == 8 or 72 mod 128.
```

In either case:

```text
v_2(H) = 3,
H / 8 == 1 mod 8.
```

Thus

```text
x * Q_L(x) = 32*u * 256*H = 2^13 * u * H.
```

The valuation is

```text
13 + v_2(H) = 16,
```

which is even. Its odd unit part is the product of

```text
u == 1 mod 8
and
H/8 == 1 mod 8,
```

so the odd unit part is also `1 mod 8`. Hence `x*Q_L(x)` is a square in
`Q_2`. Therefore `x=-224` gives a `Q_2` point on the local model, and its
tracked squareclass is `2`.

## Theorem

On the `AA+BB / kernel_minus_p` same-mod-4 branch, class `2` is locally
admissible for `x_minus_p` on both one-sided dyadic models.

## Proof

If `A` and `B` are odd and equal modulo `4`, then

```text
T = A+B = 2*s
```

with `s` odd.

On the `AA` side, take `L=A`, which is odd. The lemma gives a `Q_2` point with
`x`-class `2`.

On the `BB` side, take `L=B`, which is also odd. The same lemma gives a
`Q_2` point with `x`-class `2`.

Therefore class `2` survives the two one-sided dyadic local conditions that
define the `AA+BB` same-mod-4 branch.

## Conclusion

The same-mod-4 branch cannot be closed by proving

```text
x_minus_p(Q_2) ∩ {1,-1,2,-2} = {1}.
```

The local image already contains class `2`. The remaining branch must be
attacked by a different theorem: either a cross-kernel compatibility relation,
a Selmer-level lift constraint, or another global condition. More finite
sampling of this same local image is not progress.

## Boundary

This note does not prove:

- a dyadic exclusion for the same-mod-4 branch,
- a cross-kernel compatibility theorem,
- a Selmer lift,
- a global Selmer dimension bound,
- rank zero,
- any family-level lambda exclusion.

It proves only that the naive one-kernel singleton target is false on the
same-mod-4 branch.
