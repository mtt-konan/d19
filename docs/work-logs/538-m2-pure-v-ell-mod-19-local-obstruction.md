# M2 Pure v_ell mod-19 Local Obstruction

## Question

Can one prove another direct local obstruction inside the exact `wl535`
system, beyond `wl536` and `wl537`, without replacing it by a birational
coordinate rewrite?

This work proves one additional infinite congruence subfamily and stops.

## Exact Input

For an odd prime `ell ≡ 1 (mod 4)`, the exact `wl535` conditions are

```text
ell-q^2 square,
ell*q^2+4 square,
ell*q^4+4*q^2-4*ell > 0,
V^2 = G_ell(q^2),
```

where

```text
G_ell(Q)
  = Q^4 + (16-8*ell)Q^3
    + (32*ell^2-96*ell+72)Q^2
    + (32*ell-64)Q + 16.
```

## Statement

If additionally

```text
ell ≡ 15 (mod 19),
```

then the system has no rational solution. Together with `ell ≡ 1 (mod 4)`,
the Chinese remainder theorem gives the single class

```text
ell ≡ 53 (mod 76).
```

Because `gcd(53,76)=1`, Dirichlet's theorem makes this an infinite prime
subfamily.

## Proof

Choose `p in Q` with `p^2=ell-q^2`, and write

```text
p=P/D, q=Q/D, gcd(P,Q,D)=1.
```

Then `P^2+Q^2=ell*D^2`. Since `19 ∤ ell` and `-1` is a nonsquare modulo
`19`, a denominator divisible by `19` would force `P ≡ Q ≡ 0 (mod 19)`,
contradicting primitivity. Thus `p,q` are 19-adically integral, and every
rational square in the exact system reduces to a square residue modulo `19`.

Put `R=q^2 mod 19`. The square residues are

```text
{0,1,4,5,6,7,9,11,16,17}.
```

At `ell ≡ 15 (mod 19)`, the quartic reduces to

```text
G_15(R) ≡ R^4 + 10R^3 + 18R^2 + 17R + 16 (mod 19).
```

The complete residue table is:

| `R` | `15-R` | `15R+4` | `G_15(R)` | one failure |
|---:|---:|---:|---:|:---|
| 0 | 15 | 4 | 16 | `15-R` |
| 1 | 14 | 0 | 5 | `15-R` |
| 4 | 11 | 7 | 14 | `G_15(R)` |
| 5 | 10 | 3 | 13 | `15-R` |
| 6 | 9 | 18 | 4 | `15R+4` |
| 7 | 8 | 14 | 8 | `15-R` |
| 9 | 6 | 6 | 12 | `G_15(R)` |
| 11 | 4 | 17 | 8 | `G_15(R)` |
| 16 | 18 | 16 | 14 | `15-R` |
| 17 | 17 | 12 | 9 | `15R+4` |

Every possible `R` fails a necessary square condition. Hence no rational
solution exists. The positivity condition is not needed for this stronger
local contradiction.

## Claim Boundary

This proves only the exact M2 exclusion `ell ≡ 53 (mod 76)` for the current
pure-`v_ell` support family. It does not solve the complementary `wl535`
classes, produce a counterexample, prove a complete Selmer upper bound,
establish rank zero or `Sha[2]=0`, or enter M3.

The attempted Gaussian/Pythagorean parameterization of
`G_ell(q^2)=V^2` is not recorded as progress: with the positivity-forced
nonzero leg it is reversible and merely replaces the same square condition
by a rational slope.
