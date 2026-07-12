# M2 Pure v_ell Real-Quadratic Square-Ideal Descent

## Question

Can the denominator support theorem `wl542` be promoted to a genuine global
descent rather than another list of local conditions?

## Setup

Keep the primitive equations

```text
A^2+Q^2 = ell*D^2,
C^2 = ell*Q^2+4*D^2,
```

with `D>0`, `D` odd, `gcd(D,ell)=1`, and choose the sign `C>0`. Put

```text
K = Q(sqrt(ell)),
alpha = (C+Q*sqrt(ell))/2.
```

Because `ell ≡ 1 (mod 4)`, the ring of integers is
`O_K=Z[(1+sqrt(ell))/2]`. Reducing the second equation modulo `4` shows
`C` and `Q` have the same parity, so `alpha` is integral.

## Square-Ideal Proposition

The element `alpha` is totally positive and satisfies

```text
Norm_K/Q(alpha)=D^2.
```

Moreover, there is an integral ideal `a` of `O_K` such that

```text
(alpha)=a^2.
```

### Proof

Since

```text
C^2-ell*Q^2=4D^2>0
```

and `C>0`, one has `C>|Q|*sqrt(ell)`. Thus both real embeddings of `alpha`
are positive, proving total positivity and the norm identity.

The ideals `(alpha)` and `(conjugate(alpha))` are coprime. Indeed, a common
prime ideal would divide both `C` and `Q*sqrt(ell)`. Its rational prime cannot
be `2`, because the norm `D^2` is odd, and cannot be `ell`, because
`gcd(D,ell)=1`. At any remaining prime dividing `D`, `wl542` proves that `Q`
is a unit, while `sqrt(ell)` is also a unit, a contradiction.

Now

```text
(alpha)*(conjugate(alpha))=(D)^2.
```

Two coprime integral ideals whose product is a square ideal are individually
square ideals. This gives `(alpha)=a^2`.

## Eliminate The Ideal-Class Ambiguity

The discriminant of `K` is the single prime `ell`. Gauss genus theory for the
ordinary ideal class group gives

```text
Cl(K)[2]=0.
```

Since `[a]^2=1`, the ideal `a` is principal. Therefore there exist
`beta in O_K` and a unit `epsilon in O_K^x` such that

```text
alpha = epsilon*beta^2.
```

Because `alpha` and `beta^2` are totally positive, `epsilon` is a totally
positive unit.

This use of the ordinary class group is essential. The narrow class group can
retain an extra sign class when the negative Pell equation is insoluble; that
sign issue is exactly the unit ambiguity below, not an unproved ideal-class
obstruction.

## Exact Unit-Square Ambiguity

Modulo unit squares, the totally positive unit `epsilon` has:

- one possible class if `K` has a unit of norm `-1`;
- two possible classes if every unit has norm `+1`.

Indeed, if a fundamental unit has norm `-1`, every totally positive unit is an
even power and hence a square. If the fundamental unit has norm `+1`, its
powers are totally positive and parity of the exponent leaves exactly two
classes modulo squares.

Existence of a norm-`-1` unit is equivalent to solvability of

```text
x^2-ell*y^2=-4
```

with the parity required for an algebraic integer `(x+y*sqrt(ell))/2`.

## Exact Reduced Obstruction

Every rational `wl535` candidate therefore supplies the exact descent datum

```text
(C+Q*sqrt(ell))/2 = epsilon*beta^2,
```

where the ideal class obstruction has disappeared and `epsilon` ranges over
at most two explicit totally positive unit squareclasses. For primes with a
norm-`-1` unit, even that ambiguity disappears.

This is a genuine global reduction, not a rational point or a family
exclusion. The remaining task is to combine the resulting one- or two-class
element equations with `A^2+Q^2=ell D^2`, the `G_ell` square, and positivity.
No theorem-level Selmer, rank, `Sha`, or M3 claim is made.
