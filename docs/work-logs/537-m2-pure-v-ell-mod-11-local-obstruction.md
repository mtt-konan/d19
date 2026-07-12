# M2 Pure v_ell mod-11 Local Obstruction

## Question

Can the exact `wl535` system be excluded on another infinite prime subfamily,
complementing the mod-7 obstruction in `wl536`?

This work proves one additional local obstruction and stops. It does not solve
the remaining congruence classes, produce a counterexample, or enter M3.

## Input And Object Layer

The only mathematical input is the exact `wl535` system

```text
ell - q^2 is a rational square,
ell*q^2 + 4 is a rational square,
ell*q^4 + 4*q^2 - 4*ell > 0,
V^2 = G_ell(q^2),
```

where

```text
G_ell(Q)
  = Q^4 + (16-8*ell)Q^3
    + (32*ell^2-96*ell+72)Q^2
    + (32*ell-64)Q + 16.
```

The touched object layer is only the rational-point obstruction inside this
system for `support=v_ell|L=1|T=ell|d=(ell,1,ell)`.

## Statement

If `ell` is an odd prime satisfying

```text
ell ≡ 1 (mod 4),
ell ≡ 10 (mod 11),
```

then the exact `wl535` system has no rational solution. By the Chinese
remainder theorem these conditions are equivalent to

```text
ell ≡ 21 (mod 44).
```

Since `gcd(21,44)=1`, Dirichlet's theorem shows that this is an infinite prime
subfamily.

## Proof

Assume a solution exists and choose `p,c in Q` with

```text
p^2 = ell-q^2,
c^2 = ell*q^2+4.
```

### 11-adic integrality

Write `p=P/D` and `q=Q/D` with integers `P,Q,D`, `D>0`, and
`gcd(P,Q,D)=1`. Then

```text
P^2 + Q^2 = ell*D^2.
```

Here `11` does not divide `ell`. If `11 | D`, reduction modulo `11` gives
`P^2+Q^2=0`. Since `11 ≡ 3 (mod 4)`, `-1` is a nonsquare modulo `11`, so this
forces `P ≡ Q ≡ 0 (mod 11)`, contradicting primitivity. Hence `11` does not
divide `D`; in particular `p,q` are 11-adically integral. All three rational
squares in the system therefore reduce to square residues modulo `11`.

### Residue elimination

Put `R=q^2 mod 11`. The square residues modulo `11` are

```text
{0,1,3,4,5,9}.
```

For `ell ≡ 10 (mod 11)`, reduction of the quartic gives

```text
G_10(R) ≡ R^4 + 2R^3 + 2R^2 + 3R + 5 (mod 11).
```

Each possible `R` fails at least one necessary square condition:

| `R` | `10-R` | `10R+4` | `G_10(R)` | failure |
|---:|---:|---:|---:|:---|
| 0 | 10 | 4 | 5 | `10-R` |
| 1 | 9 | 3 | 2 | `G_10(R)` |
| 3 | 7 | 1 | 2 | `10-R` |
| 4 | 6 | 0 | 4 | `10-R` |
| 5 | 5 | 10 | 10 | `10R+4` |
| 9 | 1 | 6 | 7 | `10R+4` |

Thus no residue for `q^2` survives, a contradiction.

The strict positivity predicate was not needed; excluding solutions of the
three square equations already excludes the full exact system.

## Boundary

Proved here:

- the direct 11-adic obstruction `ell ≡ 10 (mod 11)`;
- equivalently, exclusion of the infinite prime class `ell ≡ 21 (mod 44)`.

Not proved here:

- the full `wl535` proposition;
- disjointness from the `wl536` class or a partition of all remaining primes;
- a complete Selmer upper bound, rank-zero theorem, `Sha[2]=0`, or family
  exclusion beyond this exact M2 support family;
- anything in M3.

## Next Gate

The exact `wl535` proposition remains open outside the union of the mod-7 and
mod-11 excluded classes. The next step must again be a rigorous local/descent
obstruction, a strict fully lifted counterexample, or a genuinely smaller
arithmetic lemma. This work enters none of them.
