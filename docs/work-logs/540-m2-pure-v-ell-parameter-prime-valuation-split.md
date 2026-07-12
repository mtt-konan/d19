# M2 Pure v_ell Parameter-Prime Valuation Split

## Question

After `wl539` exhausts direct good-reduction residue tables, what exact
bad-reduction information is forced at the parameter prime `ell` itself?

## Statement

Assume the exact `wl535` system and choose `a,c in Q` with

```text
a^2 = ell-q^2,
c^2 = ell*q^2+4.
```

Then `q,a,c` are all `ell`-adic units. Put `Q=q^2` and

```text
g(Q)=G_ell(Q) mod ell
    = Q^4+16Q^3+72Q^2-64Q+16.
```

The last square equation has exactly two local branches:

1. `g(Q mod ell)` is a nonzero square and `V` is an `ell`-adic unit.
2. `Q mod ell` is a simple root of `g`; if `alpha` is its unique Hensel lift
   satisfying `G_ell(alpha)=0`, then

   ```text
   v_ell(Q-alpha) = v_ell(G_ell(Q)) = 2k > 0.
   ```

The second branch can occur only when `ell ≡ 1 (mod 8)`. Hence every exact
solution with `ell ≡ 5 (mod 8)` lies in the first, nonzero-reduction branch.

## Unit Proof

Let `m=v_ell(q)`. If `m<0`, then

```text
v_ell(ell*q^2)=1+2m<0
```

is odd and differs from `v_ell(4)=0`. Thus
`v_ell(ell*q^2+4)=1+2m` is odd, impossible for `c^2`.

If `m>0`, then `v_ell(q^2)>=2`, so

```text
v_ell(ell-q^2)=1,
```

impossible for `a^2`. Therefore `m=0`. The terms of `ell-q^2` then have
different valuations `1` and `0`, so `a` is a unit. Likewise the terms of
`ell*q^2+4` have valuations `1` and `0`, so `c` is a unit and
`c ≡ +/-2 (mod ell)`.

## Simple Roots And Hensel Distance

The reduced quartic has

```text
disc(g)=2^29.
```

It is therefore squarefree modulo every odd `ell`. If `g(Q mod ell)` is
nonzero, the square equation makes it a nonzero square and makes `V` a unit.

If `g(Q mod ell)=0`, Hensel's lemma gives a unique root `alpha` of the full
polynomial `G_ell` in that residue class. Its derivative is a unit, so the
local factorization gives

```text
v_ell(G_ell(Q))=v_ell(Q-alpha).
```

Since the left side is `v_ell(V^2)`, it must be positive and even. Conversely,
an even positive distance gives an even valuation; the remaining unit
squareclass is still part of the exact local square condition and is not
silently claimed automatic here.

## Why The Root Branch Forces ell = 1 mod 8

Choose `i mod ell` with `i^2=-1`. The reduced quartic factors as

```text
g(Q)
 = (Q^2+(8-4i)Q-4)(Q^2+(8+4i)Q-4).
```

For a root of the first factor, the exact quotient-ring identity is

```text
Q*(Q/4 + 2 - i/2)^2 = 2.
```

The conjugate identity holds for the other factor. The parenthesized factor
cannot vanish because the right side is nonzero. Hence every root satisfies

```text
chi(Q)=chi(2).
```

But the exact system has `Q=q^2`, a nonzero square modulo `ell`. Thus a root
branch forces `2` to be a square modulo `ell`. Under the standing condition
`ell ≡ 1 (mod 4)`, this is equivalent to `ell ≡ 1 (mod 8)`.

## Boundary And Next Gate

This is a genuine valuation reduction: it removes all negative, positive, and
zero-reduction `q` branches, and removes the entire Hensel-root branch for
`ell ≡ 5 (mod 8)`. It does not exclude the remaining unit branch, prove the
full `wl535` proposition, produce a counterexample, establish a Selmer/rank/
`Sha` theorem, or enter M3.

The next exact problem is now split by `ell mod 8`: analyze the nonzero unit
squareclass branch for all `ell`, and, only for `ell ≡ 1 (mod 8)`, the
even-distance Hensel-root branch.
