# M2 Pure v_ell Archimedean Selection Of The Norm-Ratio Branch

## Question

Can the source-square range and strict positivity select one of the two
ordered norm-ratio branches left explicit in `wl568`?

## Uniform Sign Of F

Write

```text
X=q^2=Q^2/D^2.
```

The first source square gives `ell-X` as a rational square. Equality cannot
hold because the prime `ell` is not a rational square, while `X=0` contradicts
the strict positivity condition. Hence

```text
0<X<ell.
```

For every relevant prime `ell>=5`, put

```text
f_ell(X)=X^2+(8-4*ell)*X-4.
```

On `0<=X<=ell`,

```text
f_ell'(X)=2*X+8-4*ell <= 8-2*ell < 0.
```

Therefore

```text
f_ell(X)<f_ell(0)=-4.
```

Since `F=D^4*f_ell(X)` and `D>0`, every exact candidate satisfies

```text
F<0.
```

## Unique Ordered Ratio Branch

Keep the positive Gaussian coordinates from `wl563`:

```text
A=alpha*M^2>0,
B=beta*N^2>0,
F=r*g^2*(A^2-B^2),
E=2*r*g^2*A*B>0.
```

The sign just proved forces

```text
0<A/B<1.
```

Let `C>0` satisfy `C^2=F^2+E^2`. The signed ratio equation is

```text
E*tau^2-2*F*tau-E=0,
tau=A/B.
```

Its roots are

```text
tau=(F+C)/E>0,
tau=(F-C)/E<0.
```

Thus the actual positive ordered ratio is uniquely

```text
tau=(C+F)/E.
```

The alternative ordered factor in `wl568` corresponds to the reciprocal
ratio `(C-F)/E>1`; it cannot be the candidate ordering because `F<0` forces
`A<B`.

## Exact Cone Interval

The strict cone divided by the positive factor `B^2` is

```text
ell*(tau^2-1)+2*(ell-1)*tau>0.
```

Its unique positive root is

```text
rho_ell=(sqrt((ell-1)^2+ell^2)-(ell-1))/ell.
```

Therefore every candidate on the trivial real-unit branch satisfies the exact
open interval

```text
rho_ell<tau<1.
```

For `ell>=5`, this also gives the uniform but weaker bounds

```text
sqrt(2)-1<rho_ell<1/2,
sqrt(2)-1<tau<1.
```

The lower comparison follows because
`sqrt(1+s^2)-s` is decreasing and `s=(ell-1)/ell<1`; the upper comparison is
equivalent after squaring to `ell>4`.

## Exact Consequence

The two ordered norm-ratio branches from `wl568` are no longer both live.
Every candidate must use

```text
tau=(C+F)/E in (rho_ell,1).
```

The next gate must couple this unique archimedean branch to the selected
`R_pi`/`B_pi` orientation. Rechecking the discarded reciprocal branch,
allocation matrices, standalone local tables, or standalone dyadic strata
cannot produce further progress.

## Boundary

This is a strict branch elimination and interval certificate. It does not
prove the surviving interval empty, solve the selected orientation/norm
intersection, handle the nontrivial real-unit class, prove `wl535`, identify a
Selmer group, or enter M3.
