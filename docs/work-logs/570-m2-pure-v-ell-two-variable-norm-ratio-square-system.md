# M2 Pure v_ell Two-Variable Norm-Ratio Square System

## Question

Can the unique norm ratio from `wl569` eliminate the final quartic square root
and expose the two source-square conditions as one exact smaller arithmetic
system?

## Norm-Ratio Equation

Put

```text
X=q^2,
F=X^2+(8-4*ell)*X-4,
E=4*(ell-1)*X.
```

For an exact candidate choose `C>0` with `C^2=F^2+E^2` and define

```text
tau=(C+F)/E.
```

By `wl569`, `0<tau<1`. The norm identity is equivalent to

```text
2*tau*F=E*(tau^2-1).
```

Writing

```text
delta=tau^2+2*tau-1,
```

and solving the displayed equation for the parameter gives

```text
ell = L(X,tau)
    = (tau*X^2+2*X*tau^2+8*X*tau-2*X-4*tau)
      /(2*X*delta).
```

The exact cone interval from `wl569` has `tau>rho_ell>sqrt(2)-1`, so
`delta>0`; no denominator is lost.

## Factored Source Squares

Substitution of `L(X,tau)` gives the exact identities

```text
ell-X
 = -(X*tau+2*X-2)*(2*X*tau-X-2*tau)
   /(2*X*delta),

ell*X+4
 = (X+2*tau+4)*(X*tau+4*tau-2)
   /(2*delta).
```

Thus the two source squares become two explicit factored rational-square
predicates in `(X,tau)`. The condition `q in Q` is exactly that `X` itself is
a rational square.

## Exact Positivity Intervals

The positive roots of the original positivity polynomial and the ratio cone
are

```text
sigma_ell=2*(sqrt(ell^2+1)-1)/ell,
rho_ell=(sqrt((ell-1)^2+ell^2)-(ell-1))/ell.
```

Hence every candidate satisfies

```text
sigma_ell<X<ell,
rho_ell<tau<1.
```

In particular `X>1`. Since the first factored square is positive, its first
factor is then positive and its second factor is negative. Therefore

```text
X*(2*tau-1)<2*tau.
```

For `tau>1/2`, this is the additional visible upper bound

```text
X<2*tau/(2*tau-1).
```

## Forward And Converse

Every rational `wl535` candidate produces a unique pair `(X,tau)` satisfying:

- `X` is a positive rational square;
- `ell=L(X,tau)`;
- both displayed factored values are rational squares;
- `sigma_ell<X<ell` and `rho_ell<tau<1`.

Conversely, suppose a rational pair `(X,tau)` satisfies exactly those
conditions for an odd prime `ell congruent 1 mod 4`. Choose rational square
roots

```text
q^2=X,
p^2=ell-X,
c^2=ell*X+4.
```

Define

```text
F=X^2+(8-4*ell)*X-4,
E=4*(ell-1)*X,
C=E*(1+tau^2)/(2*tau).
```

The equation `ell=L(X,tau)` gives

```text
F=E*(tau^2-1)/(2*tau),
```

so direct expansion gives `C^2=F^2+E^2`. Taking `V=+/-C` reconstructs all
four exact `wl535` conditions, including strict positivity from
`X>sigma_ell`. The intervals also exclude `X=0`, `E=0`, `tau=0`, and
`delta=0`, so there are no omitted exceptional branches.

## Relation To The Selected Orientation

The selected `R_pi`/`B_pi` equations are an exact UFD representation of the
first source square inside the trivial real-unit descent. They do not impose
an additional equation on `(X,tau)` beyond that source square and the branch
normalization. The two-variable system instead steps back before the
real-unit split and is exactly equivalent to the whole `wl535` system. It
does not identify the two real-unit classes or claim either one is empty.

## Next Exact Gate

The remaining proposition is now:

```text
For every odd prime ell congruent 1 mod 4, the displayed two-variable
factored square system has no rational point in the exact open rectangle.
```

A next gate must use the simultaneous factor structure or produce a strict
point. Merely reintroducing `V`, an orientation parameter, an allocation
matrix, or a real-unit label is reversible and cannot count as progress.

## Boundary

This is an exact two-variable reduction, not its solution. It does not prove
`wl535`, merge or eliminate real-unit classes, prove family exclusion,
identify a Selmer group, or enter M3.
