# M2 Pure v_ell Parameter-Prime Local Solubility

## Question

Can the parameter-prime branches isolated in `wl540` ever give a complete
local obstruction to the exact `wl535` algebraic square conditions?

## Statement

For every odd prime `ell ≡ 1 (mod 4)`, the three square equations

```text
a^2 = ell-q^2,
c^2 = ell*q^2+4,
V^2 = G_ell(q^2)
```

have a simultaneous solution over `Q_ell` with `q,a,c,V` all units. Thus the
parameter prime by itself never locally excludes a member of this family.

This is a local-solubility statement for the algebraic square equations. It
does not address the real positivity inequality and does not produce a
rational point.

## Finite-Field Curve

Keep the reduced quartic from `wl540`:

```text
g(Q)=Q^4+16Q^3+72Q^2-64Q+16.
```

Consider the smooth projective model of

```text
C_ell: y^2=g(x^2).
```

The degree-eight polynomial `g(x^2)` is squarefree for odd `ell`: `g` has
discriminant `2^29`, `g(0)=16`, and differentiating the composition introduces
no repeated root. Hence `C_ell` is a genus-three hyperelliptic curve. Its two
points at infinity are rational because the leading coefficient is `1`.

The Hasse-Weil bound gives

```text
#C_ell(F_ell) >= ell+1-6*sqrt(ell).
```

A point usable for the unit branch must have `x != 0` and `y != 0`. There are
at most:

```text
2 points at infinity,
2 affine points with x=0,
8 affine points with y=0.
```

So more than twelve points guarantees a usable point. For every
`ell >= 61`,

```text
ell+1-6*sqrt(ell) > 12.
```

## Small-Prime Certificate

The primes `ell ≡ 1 (mod 4)` below `61` have the following explicit points.
The last two columns are `Q=x^2` and `y^2=g(Q)` modulo `ell`.

| `ell` | `x` | `y` | `Q` | `g(Q)` |
|---:|---:|---:|---:|---:|
| 5 | 1 | 4 | 1 | 1 |
| 13 | 4 | 7 | 3 | 10 |
| 17 | 2 | 13 | 4 | 16 |
| 29 | 3 | 23 | 9 | 7 |
| 37 | 1 | 35 | 1 | 4 |
| 41 | 3 | 39 | 9 | 4 |
| 53 | 4 | 34 | 16 | 43 |

Every displayed `x,y` is nonzero.

## Simultaneous Hensel Lift

Choose a usable finite-field point and keep an `ell`-adic unit lift of `q=x`.
Because `ell ≡ 1 (mod 4)`, choose `i mod ell` with `i^2=-1`. Modulo `ell`, the
three equations have the nonzero roots

```text
a = i*x,
c = 2,
V = y.
```

Their derivatives with respect to `a,c,V` are `2a,2c,2V`, all units. Hensel's
lemma therefore lifts the three roots independently and simultaneously for
the same fixed `q`. This gives the claimed unit solution over `Q_ell`.

## Exact Failure Proposition

The parameter-prime local route is exhausted as a standalone obstruction:
neither the nonzero unit branch nor the conditional Hensel-root branch can
make the algebraic `wl535` system locally empty, because the unit branch is
always populated.

Further progress must couple the parameter-prime information to another
place, use a global descent, exploit the real positivity condition together
with arithmetic data, or produce a strict rational counterexample. This work
does not prove the full `wl535` proposition, a complete Selmer upper bound,
rank zero, `Sha[2]=0`, or anything in M3.
