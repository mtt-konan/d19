# Universal Four-Factor Relative Picard Census

## Accepted Outcome

```text
accepted_outcome=low_support_candidate_space_zero
```

This is a scoped zero certificate for the explicitly defined
base-pullback collision/boundary Kummer candidate space below. It is not a
census of `Pic(C)`, `Pic^0(C)[2]`, a Prym, a Brauer group, or all relative
2-descent classes. It does not authorize wl596 and does not prove a family
obstruction, Selmer/rank statement, or global nonexistence theorem.

## Phase 0: Object And Literature

For each closure branch use a separate generic parameter field

```text
K_plus  = Q(A,B), T=A+B,
K_minus = Q(A,B), T=A-B with A>B>0 on the real chamber.
```

The physical minus branch is the positive representative `T=|A-B|`; the
ordered chart above supplies it with `A>B`. Work on the smooth open where

```text
A*B*T*(A^2-B^2) != 0
```

and all six factor resultants are nonzero. On the stated positive chambers
this is exactly the nondegenerate domain retained by wl594.

Put

```text
P_A+ = (T+t)^2 + 4*A^2       P_A- = (T-t)^2 + 4*A^2
P_B+ = (T+t)^2 + 4*B^2       P_B- = (T-t)^2 + 4*B^2.
```

The full individual cover used here is the normalization `C -> P^1_t` of

```text
r_A+^2=P_A+, r_A-^2=P_A-,
r_B+^2=P_B+, r_B-^2=P_B-.
```

This is deliberately the degree-16 four-radical cover, not the degree-4
wl594 cover `z_A^2=P_A+*P_A-`, `z_B^2=P_B+*P_B-`. The latter is its quotient
under the two within-leg radical products. The four original lifts are
retained on `C`.

The later AA/BB image is not enlarged or silently replaced: it retains
`x=t^2` as a positive rational square, the sum intervals `0<|t|<T`, the
signed-difference intervals `|t|>T` with both orientations, the individual
four factor lifts, primitive/gcd conditions, and the p=2 place. The divisor
calculation below is performed before imposing these arithmetic and real
conditions, so neither boundary chart is discarded. No p=2 local-solubility
claim is made here.

Over `K` the four radicands are independent modulo squares: each has a
geometrically disjoint simple zero orbit. Thus `C` is connected of degree 16
over the generic `t`-line. There are eight geometric branch values, one for
each root of the four quadratics, and the cover is unramified at infinity.
Riemann-Hurwitz gives

```text
2*g(C)-2 = 16*(-2) + 8*8 = 32,
g(C)=17.
```

The object actually computed is the image of the following relative Kummer
subspace in `H^1(C,mu_2)`:

```text
{ h in K(t)^* : div_C(h) is even } / (K^* * K(t)^{*2}),
```

with the known four factor-radical classes and the wl595 automatic product
class quotiented out. This is a base-pullback Kummer subspace; it is not the
full relative Picard or Prym group.

The literature audit found reusable descent language but no ready-made
non-factor class on this four-radical cover. Peschmann's note records a
Kummer character and partial 2-descent obstruction, while explicitly retaining
a residual descent class and an unresolved gap. KSS supplies homogeneous
spaces for the elliptic concordant-form curve, and Ono/Halbeisen-Hungerbuhler
describe the related elliptic curve and special points. Those analogies do
not retain the four independent factor lifts: KSS concerns finding points on
the elliptic curve, Ono concerns general concordant solutions, and
Halbeisen-Hungerbuhler's rank equivalence concerns a different special-point
condition. The notes' Brauer-Manin references are future methods, not a
constructed class for `C`.

## Phase 1: Exact Divisor Audit

Let

```text
Delta=A^2-B^2,
l_plus  = Delta + T*t,
l_minus = Delta - T*t,
kappa   = l_plus/l_minus.
```

The six factor differences include

```text
P_A+ - P_A- = 4*T*t,
P_A+ - P_B+ = 4*Delta,
P_A+ - P_B- = 4*l_plus,
P_A- - P_B+ = 4*l_minus,
P_A- - P_B- = 4*Delta,
P_B+ - P_B- = 4*T*t.
```

The cross-collision values are

```text
P_A+ = P_B- at t=-Delta/T,
P_A- = P_B+ at t= Delta/T,
```

and the common value at either point is

```text
((T^2+(A-B)^2)*(T^2+(A+B)^2))/T^2.
```

On both closure branches this equals `4*(A^2+B^2)`, so neither collision
point is a factor-zero point. The nonzero resultant formulas in wl595 also
show that the eight factor-zero values are pairwise disjoint on the smooth
parameter open.

On the base projective line,

```text
div(l_plus)  = [-Delta/T] - [infinity],
div(l_minus) = [ Delta/T] - [infinity],
div(kappa)   = [-Delta/T] - [Delta/T].
```

Let `F_a` be the sum of the 16 geometric points of `C` above an unramified
base value `t=a`, and let `F_inf` be the sum of the 16 points above infinity.
The collision values, midpoint, and endpoints are all unramified because

```text
P_i(-Delta/T) and P_i(Delta/T) are nonzero,
P_i(0)=T^2+4*L^2 != 0,
P_L-(T)=P_L+(-T)=4*L^2 != 0.
```

Therefore the exact pullback is

```text
div_C(kappa) = F_{-Delta/T} - F_{Delta/T}.
```

Every point in the first fiber has valuation `+1`, and every point in the
second has valuation `-1`. Thus the divisor is not even. The quadratic
extension `y^2=kappa` is a connected ramified double cover of `C`, branched at
the 32 collision preimages. `kappa` is not a valid unramified relative
Kummer/Picard class.

At a factor-zero value, one radicand has one simple zero and the normalized
cover has eight points of ramification index two above that value. The
function `kappa` is a unit at all of them, so it contributes no divisor there.
At infinity, each `P_i` has pole order two, the full cover is unramified, and

```text
kappa = (Delta+T/t)/(Delta-T/t) -> -1.
```

There is no infinity contribution. On the rational denominator chart
`t=C/D0` with `gcd(C,D0)=1`,

```text
kappa=(Delta*D0+T*C)/(Delta*D0-T*C).
```

At a prime dividing `D0`, both displayed factors are units (away from the
already excluded parameter divisors), so denominator charts create no new
horizontal zero or pole. This agrees with the wl595 denominator audit.

The boundary values are also explicit:

```text
kappa(0) = 1,
plus branch:  kappa(T)=-A/B,  kappa(-T)=-B/A,
minus branch: kappa(T)= A/B,   kappa(-T)= B/A.
```

These are parameter-base values, not new geometric divisors.

The branch specializations are

```text
T=A+B:  Delta/T=A-B,
         kappa=(A-B+t)/(A-B-t),
         zero t=B-A, pole t=A-B;

T=A-B:  Delta/T=A+B,
         kappa=(A+B+t)/(A+B-t),
         zero t=-(A+B), pole t=A+B.
```

Thus the zero and pole are inside the positive-sum interval for the plus
branch and in the signed-difference region `|t|>T` for the minus branch.
Both are retained physical chart locations, but both remain unramified for
`C -> P^1_t` and hence give odd pullback valuations.

For `t -> -t`,

```text
kappa(-t)=kappa(t)^(-1).
```

For `A <-> B` with the physical positive `T=|A-B|` convention, `Delta` flips
sign and `kappa` again maps to its inverse. On the signed algebraic chart
`T=A-B`, the swap also sends `T` to `-T`, so the raw expression is fixed;
after reordering back to `A>B` it is the inverse action. The combined
parameter-and-`t` involution fixes the squareclass. These actions exchange
the two odd collision fibers and do not make their multiplicities even.

## Phase 2: Explicit Low-Support Space

The claimed low-support universe is the `K`-rational base-pullback space
whose horizontal support is contained in:

```text
midpoint:       t=0,
endpoints:      t=T, t=-T,
cross-collisions: l_plus=0, l_minus=0,
factor-zero orbits: P_A+, P_A-, P_B+, P_B-,
infinity and parameter-vertical divisors.
```

This is an explicit scoped definition; no claim is made about divisor classes
supported on individual geometric points inside these fibers.

Over `K`, unique factorization on `K[t]` proves that the candidate space is
generated by

```text
t, t-T, t+T,
l_plus, l_minus,
P_A+, P_A-, P_B+, P_B-.
```

Infinity is not an additional generator: the divisor of every rational
function has degree zero, so its coefficient is determined by the finite
factorization. Parameter-vertical factors are in `K^*` and are removed by
the relative quotient. This proves sufficiency for the scoped universe.

For parity, the pullbacks of the generators are

```text
div_C(t-a) = F_a-F_inf                         (a=0,T,-T),
div_C(l_plus)  = F_{-Delta/T}-F_inf,
div_C(l_minus) = F_{ Delta/T}-F_inf,
div_C(P_i) = 2*E_i - 2*F_inf,
```

where `E_i` is the sum of the points above the two geometric roots of
`P_i` (eight points above each root, hence 16 points in `E_i`), and the `P_i`
branch sets are pairwise disjoint from all the linear
boundary and collision fibers. Hence the five non-factor linear generators
have pairwise disjoint finite odd supports. No nonzero F2 combination of
them has an even divisor. The even kernel is exactly the span of the four
factor-radical classes, together with constants; the automatic product class
`[P_A+ P_A- P_B+ P_B-]` is already in that span and is killed again by the
individual lifts.

Quotienting by the four factor classes, the automatic product, parameter-base
squareclasses, and symmetry-equivalent duplicates gives

```text
V_low,unramified = 0.
```

The raw class `[kappa]=[l_plus]+[l_minus]` is nonzero before the parity test
because it has distinct simple zero and pole factors. It is not factor-
dependent or parameter-base trivial; it is rejected solely because its
pullback divisor is odd.

## Phase 3: Boundary And Stop

The surviving class count in the scoped unramified candidate space is zero.
There is no candidate ready for a later descent-design task.

The remaining theorem boundary is precise: a future reopening would have to
compute the Galois-invariant 2-torsion/divisor relations on the genus-17
normalization involving individual point orbits inside the collision and
boundary fibers, or exhibit a function in `K(C)^*` with an even divisor that
is not represented by a base-pullback function above. That is a genuinely
different relative Picard/Prym computation and is not supplied by wl594,
wl595, Peschmann, KSS, Ono, or the Halbeisen-Hungerbuhler analogies.

Stop reason: the explicitly defined low-support base-pullback
collision/boundary candidate universe is rigorously exhausted. Do not start
local-image classification, reciprocity, Selmer/rank work, D2, D5, M3, or
wl596 in this task.
