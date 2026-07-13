# Open Directions

This document keeps only directions that are still worth considering. Detailed
history belongs in the worklogs, not here.

## P0: Post-p17 Relative 2-Descent Review After wl592

Completed handoff:

```text
wl592_mixed_p17_factor_twist_local_image_complete
```

`wl587` and `wl589` supply independent complete D0 relative-descent schemas
for pure `u_7` and mixed `u_3+v_5+w_17`. The selected p=5 gate is now closed
exactly:

```text
I_{5,u} = empty set
I_{5,m} = {[5]}
```

It handles all normalized source strata, poles, projective boundaries,
factor-zero branches, and exact AA+BB lifts. Every pure named representative
is deleted; the mixed survivors are `5, 3045, 66045, 91205`. No prime other
than `5` was processed.

`wl591` resolves the selected mixed `p=7` normalized factor-twist image:

```text
I_{7,m} = {[1]}
```

The complete local proof retains affine and infinity strata, `D/A` denominator
branches, factor-zero and zero-value branches, the fixed-cover coordinate `R`,
and the exact AA+BB lift. It deletes `5, 3045, 66045` and leaves `91205`.

`wl592` closes the selected mixed `p=17` normalized factor-twist image:

```text
I_{17,m} = {[u]},
[91205] = [17u] not in I_{17,m}.
```

Its certificate covers all integral, negative-valuation/infinity, denominator,
factor-zero, R=0, zero-value, fixed-cover, positivity, and AA+BB lift
branches. Controller review found no blocking mathematical issue. The selected
`p=5,7,17` chain now exhausts the factor-twist candidate ledgers for both
frozen representatives. This does not promote the result to a family
exclusion, Selmer/rank theorem, or D2 statement. No later gate is selected.

The exact `wl535` obstruction remains a frozen input:

The remaining exact obstruction is:

```text
ell - q^2 square,
ell*q^2 + 4 square,
ell*q^4 + 4*q^2 - 4*ell > 0,
V^2 = G_ell(q^2).
```

This is still not a proof, not a counterexample, and not M3.

Three direct local subfamilies are now closed: `wl536` excludes
`ell ≡ 5 (mod 28)`, `wl537` excludes `ell ≡ 21 (mod 44)`, and `wl538`
excludes `ell ≡ 53 (mod 76)`. The P0 question remains the exact system outside
their union.

`wl539` adds `ell ≡ 5 (mod 92)` and classifies the method: no other auxiliary
prime `p ≡ 3 (mod 4)` gives a direct complete residue elimination. P0 must now
use bad reduction, coupled local information, descent, or a counterexample;
another isolated residue table is closed as a direction.

`wl540` supplies the first parameter-prime valuation split. P0 now separates
the nonzero unit squareclass branch from an even-distance Hensel-root branch,
the latter existing only when `ell ≡ 1 (mod 8)`.

`wl541` proves that the unit branch is always locally populated, closing the
parameter prime as a standalone obstruction. The remaining live directions
must genuinely couple places, use global descent, combine arithmetic with
positivity, or find a strict counterexample.

`wl542` supplies the first coupled global support restriction: denominator
primes split completely in `Q(i,sqrt(ell))`. Since the same work proves local
compatibility at every allowed denominator place, the live question is now a
global relation among that support, the numerator, and real positivity.

`wl543` supplies that first global descent: the real-quadratic norm element is
a unit times a square, with at most two totally positive unit classes. The
next live direction is to combine those explicit classes with the Gaussian
equation, `G_ell`, and positivity.

`wl544` now gives those explicit branches. The trivial unit branch is the
first live target; the second branch exists only when the negative Pell unit
class does not collapse.

`wl545` reduces the trivial class further to one parity pattern for each
`ell mod 8`. Odd/global arithmetic or positivity must now be coupled to one of
those patterns; another standalone 2-adic check is closed.

`wl546` removes the Gaussian square from the trivial unit class and leaves two
explicit double-descent orientations. The live target is now the homogeneous
`G_ell` square together with positivity on one orientation.

`wl547` makes the last square finite-class data. The live target is one
Gaussian orientation, one supported `S_ell` class, and the positivity
inequality; these classes are not theorem-level Selmer objects.

`wl548` removes `1+i` from the squarefree support. The live class must now be
an odd class over `p|ell-1` with `(2/p)=1`, still coupled to one `wl546`
orientation and positivity.

`wl549` sharpens this to primes where `t^2+4t-4` has a square root and proves
that every `p ≡ 7 (mod 8)` survives. The live target is no longer another
root-residue table; it is the odd valuation/class equation coupled to an
orientation or positivity.

`wl550` proves the same-prime orientation coupling is also automatic by
quadratic-etale Hilbert 90. The live target must now be global class
compatibility, a genuinely coupled multi-place argument, or positivity.

`wl551` globally pairs conjugate split-prime classes and replaces the
Gaussian-squarefree factor by rational `r|rad(ell-1)`. The live target is the
real/imaginary coordinate equation for `delta=eta*r*gamma^2`, coupled to one
orientation or positivity.

`wl552` forces `eta=i` by dyadic coordinate parity. The live target is now the
single-unit coordinate system for rational squarefree `r`, coupled to one
orientation or positivity.

`wl553` transfers positivity to a binary cone and exhausts it as a standalone
condition. The live target is now one complete simultaneous
orientation/class-coordinate/cone system.

`wl554` removes the remaining divisor-class choice by identifying
`r=sqf_odd(gcd(ell-1,R))`. The live target is one simultaneous system with
this canonical class substituted.

`wl555` removes branch-dependent signs using the standard norm element
`F+iE=r(a+ib)^2`. The live target is this unit-free equation and its uniform
cone coupled to one complete orientation.

`wl556` eliminates one complete orientation in each branch. The live target
is either the surviving `R_pi` simultaneous system for `ell ≡ 5 (mod 8)` or
the surviving `B_pi` system for `ell ≡ 1 (mod 8)`.

`wl557` exhausts the remaining orientation-specific dyadic valuation strata.
The live target must use odd/global compatibility with the standard square and
cone, not another 2-adic refinement.

`wl558` enters odd/global compatibility: each split unit prime dividing
`ell-1` imposes `Legendre(F/r,p)=1`. The live target is the combined character
system plus positive even-common-valuation places.

`wl559` handles those even-common places with explicit leading characters.
`wl560` adds odd-common valuation and unifies every split place. The live
target is now the assembled character system across all split prime divisors
of `ell-1`, not another isolated local case.

`wl561` assembles the matrix and cancels split-split pairs by reciprocity. The
live target is to control the remaining leading characters from the selected
orientation/source equations or find a wrong-sign parameter subfamily.

`wl562` closes the residue-level version of that target: both leading bits are
locally compatible with either orientation modulo `13`. The live target must
now use global integer compatibility, positivity, or a globally forced-sign
subfamily.

`wl563` supplies the first global integer reduction: complementary squarefree
parts `alpha*beta=kappa`, the scale equation `gMN=h|QD|`, and a quartic
difference. The live target is one such split system with the selected
orientation and cone.

`wl564` removes the binary choice at `2` whenever it occurs. The live target
is the remaining odd divisor allocation inside the quartic split systems.

`wl565` resolves all inert odd allocation. The live target is now only split
odd factors, requiring quartic residues, orientation, or the scale equation.

`wl566` supplies the quartic residue rule and shows it is not uniformly
decisive. The live target is the coupled split-prime quartic-sign system with
the scale/orientation equation.

`wl567` packages the split allocation as an affine `F_2` system. The live
target is its coupling to the global scale, orientation, quartic equality, and
strict cone.

`wl568` proves that coupling is redundant: scale and cone restate the original
coordinate and positivity equations, while the affine rows are identities for
an actual factorization. Do not continue allocation-matrix refinements. The
live trivial-unit target is the selected orientation/norm-square intersection;
the nontrivial real-unit class remains separate.

`wl569` selects the unique positive ordered norm-ratio branch by proving
`F<0`: every candidate has `tau=(C+F)/E` in the exact interval
`rho_ell<tau<1`. The live target is to couple this branch directly to the
selected `R_pi`/`B_pi` orientation.

`wl570` proves the orientation is not needed to state the exact remaining
arithmetic target. The whole `wl535` system is equivalent to a two-variable
`(X,tau)` system with `ell=L(X,tau)`, `X` square, and two explicit factored
source-square predicates in the exact open rectangle. The live target is the
simultaneous factor structure, not another reversible parameterization.

`wl571` proves the product quartic is a smooth elliptic curve for every
admissible `tau` and computes the complete cover genus: five generically and
one only at `tau=1/2`. The narrow next target is the explicit exceptional
genus-one system, or a uniform argument on the generic genus-five cover.

`wl572` excludes `tau=1/2` by an exact denominator argument: the only positive
integral-parameter value gives `ell=8`. The live target is now solely the
generic genus-five cover with `tau!=1/2`.

`wl573` proves the first generic denominator coupling: the square numerator
and denominator of `q` are supported on `4mn` and `mn`, while
`Delta=m^2+2mn-n^2` divides the positive quartic form in `a,b`. The live target
is to combine this support with one factored source-square equation.

`wl574` shows both source-factor products have the same canonical squareclass
`k=sqf(2*Delta)` and produces two complementary splits with explicit gcd
support. The live target is an exact comparison of those two allocations.

`wl575` identifies the comparison as a scaled Gaussian rotation and proves
its coefficient and determinant pairs are primitive away from `2`. The live
target is the induced side transport at odd primes dividing `k`.

`wl576` resolves all regular odd-prime transport and isolates the exact gap:
singular primes dividing `gcd(k,R_1)` or `gcd(k,R_2)`, where a whole factor
pair vanishes and the larger normalized valuation chooses the side.

`wl577` eliminates that apparent gap using `Delta|K`: singular and crossed odd
cases cannot occur. Both allocations agree at every odd prime; the live target
is only the dyadic side when primitive `m,n` have opposite parity.

`wl578` proves the normalized rotation preserves `2`-adic valuation ordering,
so the dyadic side also agrees. Allocation analysis is now exhausted. The live
target is the common-allocation magnitude system.

`wl579` identifies that magnitude system as a smooth genus-one Mobius torsor
with strict ordering `v>u`. The live target is to impose the original
primitive linear-form and gcd constraints on its rational points.

`wl580` shows those primitive coordinates reconstruct uniquely and the
canonical squareclass condition returns exactly the `wl570` source squares.
All descent bookkeeping is exhausted. The live target is now the explicit
rational-point theorem for the self-consistent genus-one/genus-five family.

`wl581` constructs a strict lower-genus forward route: a genus-two character
quotient over `Q` and its reciprocal elliptic quotient over `Q(i)`. The live
question is emptiness of the nonzero affine image satisfying `S in Q`,
`S^2+16` square, the rational-square positive `X` lift, the prime formula, and
the exact interval. Unrestricted elliptic solubility, finite point counts, or
unrelated rank tables do not resolve that locus.

`wl582` proves the `S in Q`, non-two-torsion elliptic locus is actually
equivalent to the genus-two rational locus via `X=-2*Re(Y)/Im(Y)`. The
quadratic lift is automatic, so the elliptic quotient cannot be advanced by
unrestricted ranks or point existence. A next proof must retain square `X`,
one individual source-square condition, or the prime parameter.

`wl583` packages the two individual source squares into a genus-one torsor
over `Q`. The full generic cover is its connected fiber product with
`q^2=X`; square `X` is not automatic because `X` has simple zeros and poles
on the torsor. The next useful result must constrain square-`X` torsor points
with the exact prime formula, not merely compute unrestricted torsor or
product-elliptic points.

`wl584` proves that after imposing the exact prime formula, the torsor is
pointwise just the fixed-`ell` source genus-one curve. Its square-`X` cover is
also genus one, and the final norm-ratio quadratic has discriminant
`4G_ell(X)`. The next proof must attack that final norm square on the
square-`X` source curve with the selected interval and prime parameter;
unrestricted source-curve ranks or points are exhausted.

`wl585` proves the exact fixed-`ell` full cover has genus seventeen and the
selected `tau` inequality is merely positivity. Its strongest combined
character has genus three and maps to an explicit elliptic curve over `Q`.
The live target is the restricted elliptic image with positive square `X` and
all individual lifts; unrestricted rank or point calculations remain outside
the proof gate.

The `wl530-wl585` consolidated review marks this elliptic-quotient direction
exhausted. `wl586` then performs a truth audit across pure `v`, pure `u`, and
mixed `u+v+w` cover families. The read-only quartic review is determined by
the existing Gaussian factorization, so no `wl588` is created. Parameter
characters and the restricted elliptic quotient remain pure-`v` tools and are
route-dead in their current form. The only surviving feasibility candidate is
common-source function-field divisor parity, which transfers generically to
two representatives but fails to provide a uniform pointwise exclusion.
Another equivalent model, quotient, local table, higher character rewrite,
fixed double cover, or fixed-`ell` rank calculation is not progress.

Input state:

- `wl522` compressed the `wl491`-`wl521` AA+BB admissibility ledgers.
- The taxonomy has no genuinely deferred cover family.
- The taxonomy has no AA+BB-admissible cover family.
- `wl523` tried the named theorem-candidate:

```text
common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families
```

`wl523` records that the point-level obstruction is already provable from
`wl491`: once the centered-even pullback gives rational `N,M`, a non-square
opposite-side common-source product blocks AA+BB admissibility. It also records
that this is not a uniform cover-family theorem.

`wl524` decided the route choice and selected a later attempt at a new uniform
squareclass lemma for those cover families. `wl524` did not enter that proof
attempt. The attempt must not use the 15 cover-family count as proof, and it
must not claim a theorem-level Selmer upper bound unless one is actually
proved.

`wl525` entered the selected attempt and found the precise failure point:

```text
finite_taxonomy_has_no_uniform_squareclass_certificate
```

The finite taxonomy does not provide cover-family function-field models,
rational `N,M` maps, divisor parity data, or a specialization argument for the
opposite-side product. The uniform lemma is therefore not proved from
`wl523` / `wl524`. This does not refute the possible lemma; it refutes only
the finite-taxonomy promotion.

`wl526` made that route choice. It compared exactly four route families and
selected only a later minimal function-field proof-data scoping gate for the
named cover families. The selected gate should inventory cover-family models,
source-side maps, candidate `N,M` function-field elements, the opposite-side
product squareclass/divisor-parity certificate target, and exceptional
specialization / positivity separation. `wl526` did not enter that gate, build
function-field models, prove the uniform lemma, name a theorem-level
complete-Selmer row, abandon the obstruction line, or select a different
candidate.

`wl527` entered only that proof-data scoping gate. It found that the current
data is not ready for a later uniform squareclass proof attempt:

```text
ready_cover_family_count = 0
not_ready_cover_family_count = 15
exact_missing_data_class =
  uniform_function_field_model_maps_and_squareclass_certificate
```

The exact missing data classes are explicit cover-family function-field
models, rational source-side maps on each family, `N,M` as function-field
elements, an opposite-side product squareclass/divisor-parity certificate, and
exceptional specialization / positivity separation. One named row also lacks
an explicit `d` vector in the `wl522` taxonomy label. `wl527` does not build
those objects, prove the uniform lemma, refute the possible mathematical
lemma, or advance to another roadmap step.

`wl528` supplies the first explicitly selected prototype for only:

```text
support=v_5|L=1|T=5|d=(5,1,5)
```

It reconstructs the function field

```text
Q(r,y)/(y^2 - (5*r^4 - 264*r^2 + 2000))
```

and proves the opposite-side leg-4 product `(N^2+16)(M^2+16)` is nonsquare in
that function field by the rational specialization `r=10,y=160`, where the
value is `12025/16`. This is a successful single-prototype nonsquare
certificate. It is not yet a uniform cover-family theorem because it lacks a
divisor-parity or specialization-survival argument over every nonexceptional
rational point in the required positivity domain.

`wl529` then closes exactly that one-family specialization gap for the same
prototype. It uses the identity

```text
16*(N^2+16)(M^2+16) = (t^2+39)^2 + 6400
```

to reduce square specializations to the genus-one quartic

```text
U^2 = t^4 + 78*t^2 + 7921.
```

Via the elliptic curve

```text
Y^2 = X^3 + 78*X^2 + 7921*X
```

with `X=t^2`, `Y=tU`, the script proves

```text
E(Q) = {O, (0,0), (89,1424), (89,-1424)}
```

so the square-locus has only `t=0` over `Q`. That `t=0` value has no rational
lift back to the `wl528` quartic because the induced `r^2` equation has
discriminant `2^10*29`, not a square. Therefore the selected prototype has no
rational square specialization in the required nonexceptional positivity domain
`|t|<5`.

This closes the one-family square-locus question. It does not prove a
divisor-parity certificate, a uniform cover-family theorem, or any
theorem-level Selmer statement. No next roadmap step is entered here.

`wl530` completes the later, explicitly selected M1 derivation for the infinite
pure family `v_ell,L=1,T=ell,d=(ell,1,ell)`. It gives exact symbolic cover,
map, opposite-product, square-locus quartic, and elliptic quotient formulas and
recovers `wl528`/`wl529` at `ell=5`.

`wl531` then rewrites M2 exactly as one `X`-fiber-product proposition with
square-`X`, source-side, opposite-side, and complete-`d` lift conditions.
`wl532` shrinks that again: every odd prime `ell ≡ 3 (mod 4)` is excluded
exactly, and the remaining `ell ≡ 1 (mod 4)` case is one `Q`-coordinate
quartic-square obstruction. The current exact remaining proposition is:

```text
For every odd prime ell congruent to 1 mod 4, there is no rational point (Q,V)
with Q a rational square, ell-Q a rational square, ell*Q+4 a rational square,
0 < ((ell-Q)*(ell*Q+4))/Q < ell^2, and
V^2 = Q^4 + (16 - 8*ell)Q^3 + (32*ell^2 - 96*ell + 72)Q^2
    + (32*ell - 64)Q + 16.
```

## P1: Return To Selmer Family Proof Only With A Named Gap

The high-level rank-zero/Selmer route still needs:

```text
odd-prime local image
dyadic local condition
formal lift compatibility
global Selmer dimension bound
rank-zero conclusion
```

Enter this direction only when the next proof obligation is named precisely.
More finite samples, packages, or route counts do not by themselves advance a
theorem-level Selmer upper bound.

## P2: Finite Shell Extension

The previous finite-shell machinery selected a later shell extension at:

```text
max(A,B) = 11
```

This is lower priority than the explicit post-`wl527` missing function-field
proof-data gap. Execute shell 11 only if the user explicitly chooses this
route, and keep it classified as finite `M_tail` diagnostic work rather than
Selmer theorem progress.

## Closed Or Paused Directions

- The old package-`x` / `S~` bridge is deprecated as a theorem bridge.
- `M_tail` diagnostics are parameter-dependent; do not claim uniform full rank
  from finite shell counts.
- Ambient `C_d` global points must pass the `wl491` AA+BB common-source
  admissibility filter before entering any admissible-point ledger.
- Globally soluble but not AA+BB-admissible ledgers are diagnostic failures,
  not obstruction candidates.

Older long direction lists are archived under `docs/archive/` and the
consolidated worklogs.
