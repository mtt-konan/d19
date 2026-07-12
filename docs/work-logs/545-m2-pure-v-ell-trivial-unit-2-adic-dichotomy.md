# M2 Pure v_ell Trivial-Unit 2-adic Dichotomy

## Question

What exact 2-adic branches survive in the explicit trivial-unit descent of
`wl544`, and can the `G_ell` square add a further 2-adic obstruction?

## Primitive Trivial-Unit Setup

For a rational candidate in the trivial unit class, choose the primitive
`wl542` denominator. Then

```text
N=u^2-ell*v^2 = +/-4D,
F=4uv,
q=F/N,
```

with `D` odd. Hence

```text
v_2(N)=2,
u ≡ v (mod 2).
```

## Direct 2-adic Classification Of q

Let `k=v_2(q)`. The odd denominator theorem gives `k>=0`.

If `k=1`, write `q=2q_0` with `q_0` a unit. Then

```text
ell*q^2+4=4*(ell*q_0^2+1).
```

For either `ell ≡ 1` or `5 (mod 8)`, the parenthesized factor has valuation
exactly one. Thus the full valuation is `3`, impossible for a square.

If `k=2`, then

```text
ell*q^2+4=4*(1+4*ell*q_0^2),
```

whose unit factor is `5 (mod 8)` and hence is not a 2-adic square.

If `k=0`, then `q^2 ≡ 1 (mod 8)`. For `ell ≡ 1 (mod 8)`,
`ell*q^2+4 ≡ 5 (mod 8)`, impossible. For `ell ≡ 5 (mod 8)`, both first
square equations pass the necessary unit test.

If `k>=3`, then `ell-q^2 ≡ ell (mod 8)`. This is a square unit only when
`ell ≡ 1 (mod 8)`. In that class the second equation is
`4` times a unit congruent to `1 (mod 8)` and is locally soluble.

Therefore the exact dichotomy is

```text
ell ≡ 5 (mod 8)  =>  v_2(q)=0,
ell ≡ 1 (mod 8)  =>  v_2(q)>=3.
```

## Translate To u,v

Since `u,v` have the same parity, first suppose both are odd. Then

```text
N ≡ 1-ell (mod 8).
```

The condition `v_2(N)=2` is possible only for `ell ≡ 5 (mod 8)`; in this
case `v_2(F)=2`, so `q=F/N` is a unit.

If both are even, write `u=2m`, `v=2n`. Then

```text
N=4*(m^2-ell*n^2).
```

Exact valuation two forces `m,n` to have opposite parity. Consequently

```text
v_2(F)=v_2(16mn)>=5,
v_2(q)>=3.
```

The direct classification above then forces `ell ≡ 1 (mod 8)`. Thus

```text
ell ≡ 5 (mod 8): u,v both odd;
ell ≡ 1 (mod 8): u=2m,v=2n with m,n of opposite parity.
```

## The G Condition Is Automatic At 2

If `q` is a unit, `q^2 ≡ 1 (mod 8)` and direct reduction gives

```text
G_ell(q^2) ≡ 1 (mod 8),
```

so it is a 2-adic square.

If `v_2(q)>=3`, the constant term dominates and

```text
G_ell(q^2)=16*(1+2^7*z)
```

for some `z in Z_2`. After extracting `4^2`, the remaining unit is a square.
Thus `G_ell` creates no further 2-adic obstruction in either allowed branch.

## Exact Boundary

This rigorously separates the trivial unit branch by `ell mod 8` and removes
all other parity patterns. It also exhausts the prime `2` as a standalone
obstruction on that branch. It does not solve either surviving branch, analyze
the second unit class, prove the full `wl535` proposition, or enter M3.
