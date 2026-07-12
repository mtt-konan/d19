# M2 Pure v_ell Genus-Seventeen Cover And Combined Source-Norm Elliptic Quotient

## Question

Can the final `wl584` intersection be given one exact fixed-parameter curve,
with the real-root condition simplified and a genuinely lower-genus quotient
that still retains the combined source and norm information?

Yes. The full fixed-`ell` curve is a smooth genus-seventeen multiquadratic
cover. Its combined source-norm character is genus three and has an explicit
elliptic quotient over `Q`. This is a strict forward obstruction, not a
solution of the restricted elliptic image.

## Archimedean Root Is Not Extra

Keep

```text
F=X^2+(8-4*ell)*X-4,
E=4*(ell-1)*X,
C^2=F^2+E^2,
tau=(F+C)/E.
```

On the source interval `0<X<ell`, `wl569` proves `F<0`, while `E>0`.
Taking `C>0` gives

```text
C>|F|,
0<tau<1.
```

Indeed `tau>0` is immediate, and `tau<1` is equivalent after squaring to
`0<-2*E*F`.

The positive root `rho_ell` is characterized by

```text
ell*(tau^2-1)+2*(ell-1)*tau=0.
```

Using `E*tau^2-2*F*tau-E=0`, the left side has the same sign as

```text
ell*F+4*(ell-1)^2*X
 =ell*X^2+4*X-4*ell.
```

All omitted factors are positive. Therefore

```text
tau>rho_ell
iff ell*X^2+4*X-4*ell>0
iff X>sigma_ell.
```

The selected `tau` interval is exactly the original positivity condition; it
is not a fifth independent arithmetic lift.

## Fixed-ell Full Curve

For a fixed odd prime `ell`, the exact four square conditions adjoin the
square roots of

```text
X,
ell-X,
ell*X+4,
G_ell(X).
```

The first three parity supports are

```text
{0,infinity},
{ell,infinity},
{-4/ell,infinity}.
```

The quartic `G_ell` has discriminant

```text
2^26*(ell-2)^2*(ell-1)^4*((ell-1)^2+1),
```

so it has four distinct roots for every `ell>=5`. They avoid the source
branch points because

```text
G_ell(0)=16,
G_ell(ell)=(5*ell^2-8*ell+4)^2,
G_ell(-4/ell)=16*(5*ell^2-8*ell+4)^2/ell^4.
```

The factor `5*ell^2-8*ell+4` never vanishes over `Q` because its
discriminant is `-16`.

The four squareclasses are independent: the four roots of `G_ell` occur in
no source support, and the three source supports are themselves independent.
Hence the smooth projective normalization has degree sixteen over the
`X`-line and eight inertia-two branch points. Riemann-Hurwitz gives

```text
2*g-2=16*(-2)+8*8=32,
g=17.
```

Call this exact fixed-parameter curve `K_ell`. The active theorem is that
`K_ell(Q)` has no point with `sigma_ell<X<ell` for any prime
`ell congruent 1 mod 4`.

## Norm-Bearing Character Quotients

Among the eight characters containing `G_ell`:

```text
G_ell alone                         -> genus 1,
G_ell times one/two source classes -> six genus-2 quotients,
G_ell times all three source classes -> genus 3.
```

The last quotient retains the product of every source squareclass together
with the final norm square:

```text
J_ell:
W^2=X*(ell-X)*(ell*X+4)*G_ell(X).
```

Its eight branch points are exactly the full branch set, so `J_ell` is a
smooth genus-three hyperelliptic curve. Every exact candidate maps to it by

```text
W=q*p*c*C.
```

## Reciprocal Elliptic Quotient

The reciprocal map

```text
T(X)=-4/X
```

satisfies

```text
G_ell(T)=16*G_ell(X)/X^4,

[X*(ell-X)*(ell*X+4)] at T
 =16*[X*(ell-X)*(ell*X+4)]/X^4.
```

Thus it lifts to a rational involution of `J_ell`:

```text
j(X,W)=(-4/X,16*W/X^4).
```

Invariant coordinates are

```text
S=X-4/X,
Z=W/X^2.
```

They satisfy the cubic

```text
E_ell^comb:
Z^2=(ell^2-ell*S-4)
    *(S^2+(16-8*ell)*S+32*ell^2-96*ell+80).
```

The discriminant of the cubic right side is

```text
-64*(ell-1)^2*(5*ell^2-8*ell+4)^4,
```

which is nonzero for `ell>=5`. Hence this is an elliptic curve over `Q`.
Generically `X` satisfies `X^2-S*X-4=0`, so the quotient map has degree two.
The four fixed points over `X=+/-2*i` give the same genus-one quotient by
Riemann-Hurwitz.

## Restricted Candidate Image

Every exact candidate produces a nonzero affine point on `E_ell^comb(Q)`
with

```text
S^2+16=(X+4/X)^2 a rational square,
the positive root X of X^2-S*X-4=0 itself a rational square,
sigma_ell<X<ell,
and individual lifts of ell-X, ell*X+4, and G_ell(X).
```

Conversely, an elliptic point satisfying all these lift conditions
reconstructs the exact `K_ell` point. Unlike `wl582`, the elliptic equation is
defined over `Q` and does not automatically force `S^2+16` to be square.

Therefore this is a genuine lower-genus forward obstruction. Unrestricted
rank, torsion, or point existence on `E_ell^comb` remains insufficient.

## Next Exact Gate

Attack the restricted image on `E_ell^comb`: rational points whose quadratic
lift is a positive square `X` and whose three individual squareclasses lift.
A strict obstruction there proves `wl535`; an unrestricted elliptic
calculation does not.

## Boundary

This proves the exact genus-seventeen curve, removes the redundant real-root
condition, and constructs a combined elliptic quotient. It does not classify
the restricted elliptic image, solve `wl535`, prove family exclusion or a
Selmer upper bound, or enter M3.
