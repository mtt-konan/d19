# M2 Pure v_ell Finite Gaussian S-Squareclass Descent

## Question

Can the last homogeneous `G_ell` square remaining after `wl546` be reduced to
finitely many Gaussian squareclasses?

## Gaussian Norm Form Of The G Square

For primitive integers `Q,D`, define

```text
P = -Q^4+(8ell-12)Q^2D^2+4D^4,
R =  Q^4+4Q^2D^2-4D^4.
```

The homogeneous `G` condition is

```text
W^2=(P^2+R^2)/2.
```

The integers `P,R` have the same parity, so

```text
delta=(P+iR)/(1+i)
```

lies in `Z[i]` and satisfies

```text
Norm(delta)=W^2.
```

## Common-Factor Support

Let a Gaussian prime over an odd rational prime `p` divide both `delta` and
its conjugate. It then divides

```text
delta+conjugate(delta)=P+R,
delta-conjugate(delta)=i*(R-P).
```

Hence `p|P` and `p|R`. The identity

```text
P+R=8Q^2D^2*(ell-1)
```

shows that `p` divides `Q`, `D`, or `ell-1`.

The first two cases are impossible. If `p|Q`, primitivity gives `p∤D`, but
`R ≡ -4D^4 (mod p)`. If `p|D`, then `p∤Q` and `R ≡ Q^4 (mod p)`.
Therefore

```text
p | ell-1.
```

Since `Q,D` are units modulo `p`, put `t=Q^2/D^2`. Reducing `P` at
`ell=1` gives

```text
t^2+4t-4=0 (mod p).
```

Its discriminant is `32`, so a necessary condition is

```text
(2/p)=1.
```

This applies whether `p` is inert or split in `Z[i]`. The prime above `2` is
kept separately.

## Finite S-Squareclass Proposition

Define the finite Gaussian support

```text
S_ell = {1+i}
        union {Gaussian primes over odd p : p|ell-1 and (2/p)=1}.
```

Outside `S_ell`, a Gaussian prime cannot divide both `delta` and its
conjugate. Since their product is the square ideal `(W)^2`, its exponent in
`delta` is even. Unique factorization therefore gives

```text
delta = eta*d*gamma^2,
```

where

- `eta` is one of the two Gaussian unit classes modulo squares;
- `d` is squarefree and supported on `S_ell`;
- `gamma in Z[i]`.

Thus the final `G` square is a finite union of explicit Gaussian element
equations. Candidate-dependent common odd primes satisfy the sharper root
condition `t^2+4t-4=0`; the fixed set `S_ell` is a safe finite superset, not a
claim that every listed prime actually occurs.

## Remaining Exact System

On either `wl546` Gaussian orientation, one must now solve finitely many
equations

```text
(P+iR)/(1+i)=eta*d*gamma^2,
```

with `d` in the finite `S_ell` squareclass set, together with the two
double-descent compatibility equations and

```text
ell*Q^4+4Q^2D^2-4ellD^4>0.
```

This is a Gaussian norm descent for the explicit `G` condition. It is not an
elliptic-curve Selmer group, not a complete Selmer upper bound, not a solved
orientation, not a family exclusion, and not M3.
