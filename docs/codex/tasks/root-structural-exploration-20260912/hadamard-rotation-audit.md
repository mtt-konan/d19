# Hadamard / Gaussian-Rotation Audit

Updated: 2026-09-13

## Exact reduction

Use centered coordinates for the unit square.  If the four rational
distances are `a,b,c,d`, paired across the two Hadamard directions, put

```text
R = a^2+b^2 = c^2+d^2
q = a^2-b^2
r = c^2-d^2.
```

The geometry is exactly

```text
q^2+r^2 = 4*(R-1).
```

Since the two pairs have the same norm, there is a rational Gaussian unit
rotation

```text
c+I*d = (C+I*S)*(a+I*b),  C^2+S^2=1,
```

with `C,S` rational.  Set `m=b/a`, `Z=a^2`, and

```text
rho = (C-m*S)^2 - (S+m*C)^2
G = (1-m^2)^2 + rho^2.
```

Then the original equation becomes the quadratic in the scale `Z`:

```text
G*Z^2 - 4*(1+m^2)*Z + 4 = 0.
```

Thus a necessary condition for rational `Z` is the elliptic squareclass

```text
H = (1+m^2)^2 - G = 4*m^2-rho^2 = h^2.
```

The two candidate scales are

```text
Z = 2*(1+m^2 +/- h)/G,
```

and the original rational-distance problem additionally requires `Z` itself
to be a rational square (`a` rational).  This last lift is not optional.

Writing `C=(1-u^2)/(1+u^2)` and `S=2u/(1+u^2)` gives a completely rational
parameterization.  With

```text
k=C^2-S^2,  l=2*C*S,
rho=k*(1-m^2)-2*l*m,
```

the first squareclass factors as

```text
H = (2*m-rho)*(2*m+rho).
```

This is the precise version of the proposed "rotation lock".  It is a
genuine 2-cover condition, but it is not by itself a global obstruction.

## Nontrivial projection witness

Take the non-D4 rational rotation `(C,S)=(3/5,4/5)` (so `u=1/2`) and
`m=-169/505`.  Direct exact arithmetic gives

```text
rho = 2511312/6375625,
H = (3450034/6375625)^2.
```

Both factors `q=1-m^2` and `rho` are nonzero, so this is not an axis or
midpoint degeneration.  Nevertheless the two scale candidates have

```text
Z = 6375625/1819808   or   6375625/5269842,
```

and neither is a rational square.  Equivalently, after clearing the
direction denominator there is an integer equal-norm quadruple

```text
(a,b,c,d) = (2525,-845,2191,1513),
```

with

```text
a^2+b^2 = c^2+d^2 = 7089650,
H_integer = 3450034^2,
```

but the compatible square-side values are `1819808` and `5269842`, neither a
square.  This is a strict audit result: the nontrivial rotation and the first
squareclass lift can coexist, while the rational scale lift fails.

## Structural interpretation

For fixed non-D4 `(C,S)`, the equation `h^2=H(m)` is a genus-one quartic
(the factors are two squarefree quadratics when `C*S*(C^2-S^2) != 0`).
Requiring `Z` to be square is a further double cover of that elliptic curve;
in the generic fixed-rotation model it is a smooth plane-quartic/genus-three
lift, not a finite list of rotations.  The apparent independent freedom is
therefore transferred from the rotation parameter to a second arithmetic
lift.  This is a useful structural explanation, but not yet a proof of
nonexistence.

## Status and next gate

Accepted as a task-local structural result: the proposed first-stage claim
"only D4 rotations pass the squareclass test" is false.  The surviving
question is sharper:

> Can the second, rational-scale double cover be ruled out uniformly, or does
> it have a rational point for some non-D4 rotation?

Any continuation must retain the full square lift and reconstruct all four
distances.  No bounded absence search, product-square identity, or generic
nonsquare claim answers this question.
