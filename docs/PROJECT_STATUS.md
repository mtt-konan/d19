# Project Status

This is the current status entry. Old run-by-run records live in the
[worklog index](./work-logs/README.md).

## Current Mainline

The active mainline is:

```text
closure quotient
  -> lambda = A/B ray ledger
  -> AA/BB rank-zero certificates
  -> rank-zero Selmer family proof attempt
```

Entry points:

- [CLOSURE_QUOTIENT_MAINLINE.md](./CLOSURE_QUOTIENT_MAINLINE.md)
- [NEXT_RESEARCH_GATE.md](./NEXT_RESEARCH_GATE.md)
- [OPEN_DIRECTIONS.md](./OPEN_DIRECTIONS.md)
- [GLOSSARY.md](./GLOSSARY.md)
- [worklog index](./work-logs/README.md)

普通话说：现在不是继续数更多 `(A,B)`，而是想证明一整批
`lambda=A/B` ratio family 的 `AA/BB` quotient rank 为 0。

## What Is Proved

Strictly proved or safely usable:

- GEN-CLOSURE 是正确的全平面闭合语言：
  `{N1+N2, |N1-N2|}` 必须和 `{A+B, |A-B|}` 相交。
- 旧 concordant 曲线会漏掉闭合腿 `M=A+B-N` 的信息。
- `AA/BB rank=0 + torsion pullback` 是严格有限证书。
- 已认证的 `AA/BB rank=0` 行只回拉到中点，没有完整闭合点。
- 中点分支由 Yang Ji 定理关闭。
- `AB/BA` 不是 rank-zero 击杀器。

## What Is Not Proved

还没有证明：

- Harborth 全局命题。
- 所有 `lambda` family 的 rank-zero 定理。
- residual two-cover / Sha[2] candidate 没有有理点。
- theorem-level `Sel_2(E_L/Q)` upper bound.

Counts, samples, package totals, and candidate totals are not proof progress by
themselves. They matter only when they shrink a named proof gap or produce a
strict certificate.

## Current Bottleneck

The high-level bottleneck remains the Selmer/rank-zero family proof:

```text
odd-prime local image
dyadic local condition
formal lift compatibility
global Selmer dimension bound
rank-zero conclusion
```

The current narrow handoff is more specific and is recorded in
[NEXT_RESEARCH_GATE.md](./NEXT_RESEARCH_GATE.md):

```text
wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction_stop
```

Within that exact gate, `wl536` excludes the infinite prime class
`ell ≡ 5 (mod 28)`, `wl537` excludes `ell ≡ 21 (mod 44)`, and `wl538`
excludes `ell ≡ 53 (mod 76)`. These are partial M2 local obstructions; the
complementary classes remain open.

`wl539` adds `ell ≡ 5 (mod 92)` and proves that the four auxiliary pairs at
`7,11,19,23` exhaust the direct good-reduction residue-table method. The full
M2 proposition remains open, but that repeated local-table route is closed.

`wl540` begins the bad-reduction analysis at `ell`: `q` is forced to be an
`ell`-adic unit, and the zero-reduction Hensel-root branch of the final square
condition is removed entirely for `ell ≡ 5 (mod 8)`.

`wl541` proves the unit branch exists over `Q_ell` for every allowed parameter
prime. Thus parameter-prime local analysis alone cannot finish M2.

`wl542` constrains every rational candidate denominator to primes splitting
completely in `Q(i,sqrt(ell))`, while proving those allowed places are locally
compatible with all three square equations.

`wl543` removes the remaining ordinary ideal-class ambiguity in the
real-quadratic norm equation and leaves at most two explicit totally positive
unit squareclasses in an element-square descent.

`wl544` expands those classes into one or two explicit integer quartic
branches and retains exact reconstruction of every wl535 condition.

`wl545` splits the trivial unit branch into its two exact mod-8 parity cases
and exhausts the prime `2` as a standalone obstruction there.

`wl546` couples the real and Gaussian descents on that branch, leaving exactly
two quadratic-form orientations with only `G_ell` and positivity unresolved.

`wl547` reduces that `G_ell` square to finitely many Gaussian squareclasses
supported at `1+i` and selected primes over `ell-1`.

`wl548` proves that the `1+i` valuation is always even (`0` or `4` in the two
mod-8 branches), so only the selected odd primes over `ell-1` remain in the
squarefree support. Those odd classes and positivity are still unresolved.

`wl549` proves that the odd root condition is exactly a root-square condition.
Every `p ≡ 7 (mod 8)` has one surviving square root, while a
`p ≡ 1 (mod 8)` has zero or two. The standalone common-prime residue test is
therefore exhausted; the global class equation or positivity must come next.

`wl550` proves that each `wl546` orientation is locally compatible with every
surviving root-square class at that same prime. Thus orientation coupling does
not repair the local route; only global class compatibility, distinct-place
coupling, or positivity remains on the trivial-unit branch.

`wl551` uses the global norm square to pair conjugate split-prime generators.
Up to a Gaussian unit, every remaining squarefree factor is a rational
squarefree divisor `r|rad(ell-1)`. The live obstruction is now the resulting
rational-class coordinate equation coupled to one orientation or positivity.

`wl552` uses normalized dyadic coordinate parity to force `eta=i` in both
mod-8 branches. There is now one Gaussian unit class and rational squarefree
`r`; the remaining coordinate equations and positivity are unresolved.

`wl553` rewrites positivity as one binary cone inequality in the class-square
coordinates and proves that cone alone has uniform parity-compatible points.
The live obstruction is the full simultaneous orientation/class/cone system.

`wl554` proves `r` is candidate-canonical:
`r=sqf_odd(gcd(ell-1,R))`. Thus the live simultaneous system has no remaining
independent Gaussian unit or rational squareclass choice.

`wl555` packages the result as the uniform standard equation
`F+iE=r(a+ib)^2` and one positivity cone with `ab>0`. The live obstruction is
its simultaneous compatibility with one complete `wl546` orientation.

`wl556` uses parity to select that orientation: `R_pi` is the only candidate
for `ell ≡ 5 (mod 8)`, and `B_pi` is the only candidate for
`ell ≡ 1 (mod 8)`. One simultaneous system remains in each branch.

`wl557` classifies the exact 2-adic strata inside those orientations and shows
they remain populated. Standalone dyadic analysis is exhausted; an odd/global
simultaneous argument is now required.

`wl558` derives the first such condition at split unit primes:
`Legendre(F/r,p)=1`. Because canonical `r` records the other common primes,
the live obstruction is now a genuine distinct-place character system.

`wl559` classifies positive even common valuations. `wl560` then supplies the
odd-common leading character and unifies every odd place over `ell-1`; inert
places are automatic and split places obey one normalized master character.
The live obstruction is the assembled split-prime character system.

`wl561` assembles that system and proves the reciprocity product. Split-split
interactions cancel, but inert cross terms and candidate-dependent leading
characters remain, so the matrix alone does not give a uniform contradiction.

`wl562` proves local orientation/source residues do not determine those
characters: exact mod-13 witnesses realize both row bits in the same stratum.
The remaining route must be genuinely global or use positivity.

`wl563` enters that global gate. The product coordinate forces a finite
complementary split `alpha*beta=kappa`, a scale equation `gMN=h|QD|`, and a
quartic-difference real coordinate coupled to the selected orientation.

`wl564` uniquely assigns the factor `2` to one side whenever `2|kappa`, using
the mod-8 branch and canonical `r`. Only odd divisor allocation remains in the
complementary split.

`wl565` assigns every inert odd factor using the normalized real-coordinate
character. Split odd factors must pass a square-unit test but retain a binary
side choice; these are the only unresolved divisor allocations.

`wl566` refines those split choices by quartic sign. Some factors are uniquely
assigned, while equal predicted signs leave a coupled finite
quartic-character system.

`wl567` linearizes that system over `F_2`, replacing exponential allocation
cases by Gaussian elimination. The surviving affine allocations still have to
satisfy the scale/orientation/real-coordinate/cone equations.

`wl568` performs that coupling and proves its exact failure point. The scale
equation is equivalent to the imaginary-coordinate equality, the cone is the
original positivity identity, and every `wl567` row is automatic when its
right-hand sign is computed from the same actual quartic difference. The
allocation route therefore adds no independent obstruction. On the trivial
real-unit branch the live lemma is now the selected `B_pi`/`R_pi` orientation
intersected directly with `F^2+E^2` square and strict positivity.

`wl569` uses the exact source-square range to prove `F<0` uniformly. Hence the
positive Gaussian ratio is uniquely

```text
tau=A/B=(C+F)/E
```

and strict positivity forces `rho_ell<tau<1`, where
`rho_ell=(sqrt((ell-1)^2+ell^2)-(ell-1))/ell`. The reciprocal ordered branch
is eliminated. The selected-orientation intersection itself remains open.

`wl570` uses that unique ratio to eliminate the quartic square root entirely.
It solves the norm-ratio equation for `ell` as a rational function
`L(X,tau)` and factors both source-square values in the same two variables.
Forward and converse reconstruction identifies this system exactly with the
whole `wl535` proposition, before the real-unit split. The two-variable square
system remains unsolved.

`wl571` identifies the resulting geometry. The product of the four positive
linear factors is a smooth genus-one quartic with full rational `2`-torsion
for every admissible `tau`. The complete multiquadratic source-square cover
has genus five for `tau!=1/2`, while `tau=1/2` is the unique genus drop and
gives one explicit genus-one exceptional system. Neither curve is solved.

`wl572` closes that exceptional system without a rank computation. Writing
`q=a/b` in lowest terms, integrality of
`ell=q^2+5-4/q^2` forces `b=1` and `a^2|4`. Positivity leaves `q^2=4`, which
gives `ell=8`, not an odd prime. Thus every remaining candidate has
`tau!=1/2` and lies on the generic genus-five cover.

`wl573` begins the generic-cover arithmetic. For primitive
`X=a^2/b^2`, `tau=m/n`, parameter integrality forces

```text
a^2|4mn,
b^2|mn,
m^2+2mn-n^2 | a^4+4a^2b^2-4b^4.
```

The last divisor is coprime to `mn`. This globally couples the two rational
denominators but does not yet contradict either source square.

`wl574` combines both source squares. If `k=sqf(2*Delta)`, their homogeneous
factor products satisfy `AB=kU^2` and `CD=kV^2`. Each pair has a complementary
squarefree split of the same canonical `k`; their common gcds divide two
explicit positive quartics `R_1(a,b)` and `R_2(a,b)`. Comparing the two
allocations remains open.

`wl575` supplies that comparison map: `(C,D)` is a scaled Gaussian rotation of
`(A,B)` with coefficients `P,2K` and scale `R_1`; the inverse has scale
`R_2`, and `P^2+4K^2=R_1R_2`. Primitive `(a,b)` give exact gcds `1` or `4`,
so all odd-prime allocation transport is unambiguous outside one determinant
at a time. A primewise contradiction is not yet proved.

`wl576` classifies that transport. Every odd `p|k` has `(2/p)=1`. At regular
primes, `p|K` preserves the side and `p|P` crosses it. If `p|R_1`, both
`A,B` vanish while exactly one of `C,D` does; `p|R_2` is the inverse case.
Only these singular determinant primes require higher-valuation data.

`wl577` combines this with the earlier global fact `Delta|K`. Every odd
`p|k` therefore lies in `K`, while `P,R_1,R_2` are units. All odd singular
and crossed cases disappear, and the two complementary allocations have
identical odd parts. Only the side of `2`, when `2|k`, remains to compare.

`wl578` resolves that last side. After dividing the rotation by its common
factor `1` or `4`, its matrix has odd diagonal and even off-diagonal entries,
so it preserves the larger `2`-adic valuation. The factor `2` also transports
same-side. Hence the two complementary allocations are fully identical; only
their square magnitudes remain unresolved.

`wl579` reduces those projective magnitudes to one Mobius squareclass equation.
With `lambda=beta/alpha`, `z=lambda*u^2=B/A`, the rotated ratio is
`w=(2K+Pz)/(P-2Kz)=lambda*v^2`. This is a smooth genus-one biquadratic torsor
on the exact positive interval, and it forces `v>u`. Original primitive
linear-form reconstruction remains additional.

`wl580` proves that primitive reconstruction is unique:
`tau=[X+2z(1-X)]/[X(z+2)-2]`, with positive denominator. Imposing the
canonical squareclass `[lambda]=[2(tau^2+2tau-1)]` makes the torsor exactly
equivalent to both source-square predicates. The allocation/magnitude descent
is therefore exhausted; progress now requires a rational-point theorem on the
self-consistent family.

`wl581` gives the first direct rational-point quotient after that exhaustion.
The generic genus-five cover maps to `Z^2=Xabcd`, a genus-two character
quotient over `Q`; its reciprocal involution lifts over `Q(i)` and has a
smooth elliptic quotient. Exact candidates land only in a restricted nonzero
affine locus with a rational-square quadratic lift and the original
prime-parameter/interval conditions. That locus is still open, so `wl535` and
M2 remain unresolved.

`wl582` identifies the exact limitation of that quotient. If `Y=A+iB` and
`S in Q`, the elliptic equation itself gives `X=-2A/B` and `Z=AX`, recovering
the genus-two rational point; conversely `wl581` recovers the same elliptic
point. Thus `S^2+16` is automatically square on the relevant locus and
unrestricted elliptic point/rank data is not a smaller obstruction. The live
conditions are square `X`, an individual source-square lift, and the prime
parameter.

`wl583` retains both individual source squares on the genus-one torsor
`U^2=ab/(2delta), V^2=cd/(2delta)`. Its product maps etale of degree two to
the `wl571` product elliptic curve, while adjoining `q^2=X` recovers exactly
the generic genus-five cover. The divisor of `X` on the torsor has simple
zeros and poles, proving square `X` is a genuinely independent condition.
The live problem is the square-`X` and prime-parameter locus on this torsor.

`wl584` couples that torsor back to `ell=L(X,tau)`. Pointwise it becomes the
fixed-`ell` source elliptic `U^2=X(ell-X), V^2=ell X+4`; adjoining square
`X` is an unramified genus-one cover encoding the first two source squares.
The remaining norm-ratio quadratic has discriminant `4G_ell(X)`. Hence only
the simultaneous square-`X`, final norm square, selected real root, and prime
parameter intersection remains live.

`wl585` identifies the exact fixed-parameter geometry: the four squareclasses
define a smooth genus-seventeen cover. The selected `tau` interval is exactly
the original positivity inequality. The combined product of all source and
norm classes gives a genus-three character quotient with a reciprocal
elliptic quotient over `Q`. Candidate images must still have positive square
`X` and every individual squareclass lift, so unrestricted elliptic data does
not close M2.

The consolidated `wl530-wl585` milestone independently rechecks the algebra
and exception handling and finds no correctness defect. It also marks the
elliptic-quotient subroute exhausted: the restricted lift conditions recover
the full genus-seventeen curve, and no available uniform descent/Chabauty/
rank tool preserves all prime-family quantifiers. The proposition at `wl535`
remains open, but the active strategic gate no longer re-enters it; another
equivalent model is not progress.

`wl586` compares the pure-`v_5`, pure-`u_7`, and mixed
`u_3+v_5+w_17` cover families. Its read-only quartic review collapses to the
existing Gaussian data, so no `wl588` is created. It certifies the current
pure-`v_ell` equivalent-model, quotient, and parameter-character routes dead.
The same opposite-side product is generically nonsquare on pure-`u_7` and
mixed `u_3+v_5+w_17`, but square specializations remain a new double-cover
problem. The representative-only divisor-parity route is therefore also dead
as a uniform exclusion mechanism.

`wl522` compressed the `wl491`-`wl521` AA+BB admissibility ledgers into a
support/cover taxonomy. `wl523` then tried the isolated lemma candidate:

```text
common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families
```

The point-level obstruction is already proved by the existing `wl491`
machinery: a certified centered-even pullback with non-square opposite-side
common-source product cannot enter the AA+BB admissible ledger. The stronger
uniform cover-family reading is still unproved and would need a new lemma. It
is not a Selmer upper bound, not a rank-zero theorem, and not a family
exclusion.

`wl524` chose the next narrow route: attempt that new uniform cover-family
squareclass obstruction lemma later, using `wl523` as input. It did not enter
the proof attempt, execute shell 11, compute supports, test new ambient
`C_d` solubility, apply `wl491` to a new point, select a final obstruction
candidate, or claim theorem-level Selmer progress.

`wl525` entered that selected proof attempt at the cover-family statement
layer. The attempted promotion failed from the current inputs: the finite
15 cover-family / 29 entry taxonomy has no cover-family function-field
squareclass certificate, divisor parity data, or specialization argument. This
does not mathematically refute a possible future uniform lemma; it only
refutes promoting the finite taxonomy to that theorem. No next roadmap step is
entered by `wl525`.

`wl526` is the post-`wl525` route-choice audit. It compares the four explicit
route families: gather minimal function-field squareclass proof data, return
to finite shell / `M_tail` diagnostics, name a theorem-level complete-Selmer
local/Hilbert row obligation, or abandon this obstruction line and select a
different candidate. It selects only the first as the later narrow gate,
because that is the smallest move addressing the missing proof-data failure.
`wl526` does not enter the gate, build function-field models, prove the
uniform lemma, name a Selmer row, select a candidate, execute shell 11, or
claim theorem-level progress.

`wl527` enters only the `wl526` selected proof-data scoping gate. It inventories
the 15 named globally soluble but not AA+BB-admissible cover families and finds
the current data is not ready for a later uniform squareclass proof attempt:
zero cover families are ready. The exact missing class is explicit
cover-family function-field model/map/squareclass-certificate data: models,
rational source-side maps, `N,M` as function-field elements, an opposite-side
product squareclass or divisor-parity certificate, and exceptional
specialization / positivity separation. This is not a proof or refutation of
the possible uniform lemma, and no next roadmap step is entered.

`wl528` is the first explicitly selected single-family prototype after that
scope audit. It handles only `support=v_5|L=1|T=5|d=(5,1,5)`, represented by
`AA_A1_B4` and `BB_A4_B1` in `wl495`. It builds a reviewable function-field
chart, derives rational `N,M` maps, forms the opposite leg-4 product, and
proves that product is nonsquare in the prototype function field by a rational
specialization certificate. It does not prove the uniform cover-family
obstruction: divisor parity / specialization survival over the positivity
domain remains the exact gap.

`wl529` closes that exact one-family specialization gap for the same prototype.
Using

```text
16*(N^2+16)(M^2+16) = (t^2+39)^2 + 6400,
```

it reduces square specializations to the genus-one quartic

```text
U^2 = t^4 + 78*t^2 + 7921
```

and then to the elliptic curve

```text
Y^2 = X^3 + 78*X^2 + 7921*X
```

with `X=t^2`, `Y=tU`. The resulting rational-point certificate proves

```text
E(Q) = {O, (0,0), (89,1424), (89,-1424)},
```

so the square-locus has only `t=0` over `Q`. That value has no rational lift
to the `wl528` quartic, because the induced `r^2` equation has discriminant
`2^10*29`, not a square. Therefore the selected prototype has no rational
point in the required nonexceptional positivity domain `|t|<5` where the
opposite-side product is a rational square.

This closes the one-family square-locus audit and stops. It is not a uniform
cover-family theorem, not a divisor-parity theorem, and not a theorem-level
Selmer/rank result.

`wl530` then completes only the explicitly selected M1 symbolic derivation for

```text
support=v_ell|L=1|T=ell|d=(ell,1,ell)
```

with odd prime `ell`. It derives the complete-`d` family, function-field chart,
centered-even `t,N,M` maps, opposite-leg `ell-1` product, square-locus quartic,
and its degree-two elliptic quotient. The formulas specialize exactly to
`wl528`/`wl529` at `ell=5`. `wl531` then shrinks M2 exactly to one
`X`-fiber-product square-lift proposition, and `wl532` shrinks that again:
every odd prime `ell ≡ 3 (mod 4)` is excluded exactly, and the remaining
`ell ≡ 1 (mod 4)` case is one `Q`-coordinate quartic-square obstruction. No
general rational-point classification or M2 uniform exclusion theorem is
proved.

## Current Stop Rules

Do not execute shell 11, compute new supports, test new ambient `C_d`
solubility, apply `wl491` to a new point, select a final obstruction candidate,
or run broad rank/Selmer diagnostics unless the user explicitly asks for that
route. After `wl527`, do not treat proof-data scoping as a ready proof attempt.
Do not treat the `wl522` finite taxonomy, the `wl524` route choice, the failed
`wl525` promotion attempt, the `wl526` route choice, or the `wl527` scoping
inventory as proof of a uniform cover-family lemma.
No live proof route is entered after the `wl586` route-death certificate. A
future reopening requires parameterized family-level arithmetic controlling
square specializations across cover families. Supporting models, fixed double
covers, and maps do not count by themselves, and M3 remains closed.
