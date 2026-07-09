# AA+BB Same-Mod-4 Cross-Kernel Compatibility

## Question

After `wl461` showed that class `2` is locally admissible for
`x_minus_p` on the same-mod-4 branch, can the branch still be ruled out at the
common-source level by using the other two kernel coordinates?

## Result

Yes, at the level of genuine common-source rational points. On the branch

```text
A, B odd,
A == B mod 4,
T = A+B = 2*s with s odd,
```

the one-sided dyadic local conditions force:

```text
x_pos_2sqrt_q ∈ {1}
x_neg_2sqrt_q ∈ {1, -1}
```

inside the rational 2-primary subgroup `{1,-1,2,-2}`. Therefore a
common-source point cannot have

```text
x_minus_p = 2,
```

because the common-source product relation

```text
x_minus_p * x_pos_2sqrt_q * x_neg_2sqrt_q = 1
```

would require `x_pos_2sqrt_q * x_neg_2sqrt_q = 2`, impossible from
`{1} * {1,-1}`.

普通话说：`wl461` 说 `x_minus_p=2` 单独看是局部可行的；本条说明它和另外两个
kernel 放回同一个 source point 以后不相容。这仍然不是 Selmer lift theorem，但它把
same-mod-4 分支的正确攻击点固定为“把 common-source compatibility lift 到 Selmer
层”。

## Setup

The two remaining one-sided target models are:

```text
kernel_pos_2sqrt_q:
  y^2 = x^3 - 8*(T^2 + 8*L^2)*x^2 + 16*T^4*x

kernel_neg_2sqrt_q:
  y^2 = x^3 + 16*(T^2 + 2*L^2)*x^2 + 256*L^4*x
```

Assume:

```text
L odd,
T = 2*s with s odd.
```

This applies to both `L=A` and `L=B` when `A` and `B` are odd and equal
modulo `4`.

We only track the rational 2-primary subgroup:

```text
{1, -1, 2, -2}.
```

## Lemma 1: The Positive Kernel Has Only Class 1

For `kernel_pos_2sqrt_q`, the relevant subgroup image is contained in `{1}`.

## Proof Of Lemma 1

Write the quadratic factor as

```text
Q_+(x) = x^2 - 8*(T^2 + 8*L^2)*x + 16*T^4.
```

With `T=2*s`, this becomes

```text
Q_+(x) = x^2 - 32*(s^2 + 2*L^2)*x + 256*s^4.
```

Let `m=v_2(x)`.

If `m <= 2`, then

```text
Q_+(x) = x^2 * (1 - 32*(s^2+2L^2)/x + 256*s^4/x^2),
```

and the parenthesized factor is `1 mod 8`, hence a square in `Q_2`. Thus
`x*Q_+(x)` has the same squareclass as `x`, so a point can exist only when
`x` is a square.

If `m=3`, the quadratic factor still has valuation `2m`, so

```text
v_2(x*Q_+(x)) = 3m = 9,
```

which is odd. No point exists.

If `m=5`, then `Q_+(x)` has valuation `8`, so

```text
v_2(x*Q_+(x)) = 13,
```

again impossible.

If `m >= 6`, then

```text
Q_+(x) = 256*s^4 *
  (1 - 32*(s^2+2L^2)*x/(256*s^4) + x^2/(256*s^4)),
```

and the parenthesized factor is `1 mod 8`, hence a square. Since `256*s^4` is
a square, a point again forces `x` to be a square.

It remains to check `m=4`. Write `x=16*u` with `u` odd. Then

```text
Q_+(16*u) = 256*H_+,
H_+ = u^2 - 2*(s^2+2L^2)*u + s^4.
```

The only nontrivial unit class in `{1,-1,2,-2}` is `-1`, which means
`u == 7 mod 8`. A direct reduction modulo `16`, using odd squares
`1 or 9 mod 16`, gives

```text
H_+ == 8 mod 16.
```

So

```text
v_2(x*Q_+(x)) = 4 + 8 + 3 = 15,
```

which is odd. Hence class `-1` cannot occur either.

Therefore the positive kernel contributes only the class `1` inside
`{1,-1,2,-2}`.

## Lemma 2: The Negative Kernel Has Only Unit Classes

For `kernel_neg_2sqrt_q`, the relevant subgroup image is contained in
`{1,-1}`.

## Proof Of Lemma 2

Write

```text
Q_-(x) = x^2 + 16*(T^2 + 2*L^2)*x + 256*L^4.
```

With `T=2*s`, this is

```text
Q_-(x) = x^2 + 32*(2*s^2+L^2)*x + 256*L^4.
```

Again let `m=v_2(x)`.

The same valuation ranges as above show:

- if `m <= 2`, the factor `Q_-(x)/x^2` is `1 mod 8`, so a point forces
  `x` to be a square;
- if `m=3` or `m=5`, the valuation of `x*Q_-(x)` is odd, so no point exists;
- if `m >= 6`, the factor `Q_-(x)/(256*L^4)` is `1 mod 8`, so a point again
  forces `x` to be a square.

Thus no ramified class `2` or `-2` can occur. At `m=4`, the squareclass is a
unit class, so the relevant subgroup image is contained in `{1,-1}`.

## Theorem

For genuine common-source points in the `AA+BB` same-mod-4 branch, the local
class

```text
x_minus_p = 2
```

is impossible.

## Proof

For a common-source point, the three kernel coordinates satisfy the squareclass
product relation:

```text
x_minus_p * x_pos_2sqrt_q * x_neg_2sqrt_q = 1.
```

On the same-mod-4 branch, Lemma 1 applies to both the `L=A` and `L=B` positive
kernel conditions, so

```text
x_pos_2sqrt_q = 1.
```

Lemma 2 applies to both negative-kernel conditions, so

```text
x_neg_2sqrt_q ∈ {1,-1}.
```

If `x_minus_p=2`, the product relation would force

```text
x_pos_2sqrt_q * x_neg_2sqrt_q = 2.
```

But the left side lies in `{1,-1}`. Contradiction.

Therefore class `2` in `x_minus_p` is incompatible with being a genuine
common-source point on the same-mod-4 branch.

## Boundary

This proves a common-source compatibility obstruction, not a Selmer theorem.
It does not prove that every Selmer class lifts to a common-source point, and
therefore does not prove a Selmer rank bound, rank zero, or a lambda-family
exclusion. It identifies the exact next lift target: transport this
cross-kernel compatibility to the Selmer layer.
