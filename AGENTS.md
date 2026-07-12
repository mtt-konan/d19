# Agent Guide

This repository is a research notebook plus executable audit tools for the
rational-distance-to-square problem. Optimize for object clarity, not for
making the story sound more complete than it is.

## Start Here

Read these files before changing research direction:

1. `docs/PROJECT_STATUS.md`
2. `docs/NEXT_RESEARCH_GATE.md`
3. `docs/OPEN_DIRECTIONS.md`
4. `docs/CLOSURE_QUOTIENT_MAINLINE.md`
5. `docs/work-logs/README.md`

For script names and entry points, read `scripts/README.md`. For terminology,
read `docs/GLOSSARY.md`.

## Current Research Gate

The current handoff is:

```text
wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction_stop
```

`wl535` removes the final
dependence on the chosen `a^2+b^2=ell` chart from `wl534` and rewrites the
remaining M2 question directly in the rational `q`-root coordinate:

```text
wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction_stop
```

Keep

```text
D(u) = 1 + u^2
N(u) = b*(1-u^2) + 2*a*u
P(u) = a*(1-u^2) - 2*b*u
```

and define the direct rational circle coordinates

```text
q(u) = N(u) / D(u)
p(u) = P(u) / D(u).
```

Then `q(u)^2 + p(u)^2 = ell`, so `ell-q(u)^2` is automatically a rational
square. Also

```text
S(u) = D(u)^2*(ell*q(u)^2 + 4)
R(u) = D(u)^4*(ell*q(u)^4 + 4*q(u)^2 - 4*ell)
T(u) = D(u)^8*G_ell(q(u)^2),
```

where

```text
G_ell(Q)
  = Q^4 + (16-8*ell)Q^3 + (32*ell^2-96*ell+72)Q^2 + (32*ell-64)Q + 16.
```

Conversely, if `q` is rational and `ell-q^2` is a rational square, choose a
rational `p` with `p^2=ell-q^2`. Then

```text
u = (q-b)/(p+a) when p+a != 0,
u = (a-p)/(q+b) when q+b != 0.
```

The two visible zero-denominator branches are removable:

```text
(-a,b)  ->  u = (a-(-a))/(b+b) = a/b,
(a,-b)  ->  u = ((-b)-b)/(a+a) = -b/a.
```

The only missed point is the antipode `(-a,-b)`. Switching the sign of `p`
gives the visible point `(a,-b)` with the same `q=-b`, and every current
condition depends only on `q^2`.

Therefore the exact `wl534` obstruction is equivalent to:

```text
For every odd prime ell congruent to 1 mod 4, there is no rational pair (q,V)
such that

ell - q^2 is a rational square,
ell*q^2 + 4 is a rational square,
ell*q^4 + 4*q^2 - 4*ell > 0,
V^2 = G_ell(q^2).
```

`wl535` is still not an exclusion theorem and not a counterexample. Only a
fresh narrow task may prove or refute this exact `q`-root-coordinate
square/quartic proposition; do not enter M3 from this checkpoint.

`wl536`-`wl538` prove three partial local consequences inside this exact
system. They exclude respectively the infinite prime classes
`ell ≡ 5 (mod 28)`, `ell ≡ 21 (mod 44)`, and `ell ≡ 53 (mod 76)`. Their union
is still not the full `wl535` proposition, and none enters M3.

`wl539` classifies this direct single-prime good-reduction residue method.
It adds the final class `ell ≡ 5 (mod 92)` from auxiliary prime `23` and
proves, by a Weil-bound cutoff plus exhaustive finite certificate, that no
other prime `p ≡ 3 (mod 4)` eliminates a parameter residue by the same four
square-residue table. Do not continue accumulating tables of this form.

`wl540` starts the bad-reduction route at the parameter prime. It proves that
`q` and the two auxiliary square roots are `ell`-adic units. The last square
condition splits into a nonzero unit-reduction branch and an even-distance
simple Hensel-root branch; the latter is impossible for `ell ≡ 5 (mod 8)`.
This is still not the full `wl535` theorem and does not enter M3.

`wl541` proves the parameter-prime algebraic square system is locally soluble
for every `ell ≡ 1 (mod 4)`. A genus-three Hasse-Weil argument supplies a
nonzero unit point for `ell >= 61`, and seven explicit small-prime witnesses
complete the proof. Thus the parameter prime alone is exhausted as a local
obstruction; it must be coupled to another place or to global/real data.

`wl542` gives the first coupled global denominator restriction. In a primitive
common denominator `D`, every prime divisor splits completely in
`Q(i,sqrt(ell))`; `D` is odd, coprime to `ell`, and a nonzero square modulo
`ell`. Conversely all three square equations are automatically locally
compatible at negative valuation over such split primes. The next gate must
use a global relation among this restricted support, the numerator, and/or
real positivity rather than another standalone place.

`wl543` promotes that support theorem to a real-quadratic square-ideal
descent. For `alpha=(C+Q*sqrt(ell))/2`, it proves
`(alpha)=a^2`; prime-discriminant genus theory kills the ordinary ideal-class
ambiguity, so `alpha=epsilon*beta^2`. Only at most two totally positive unit
squareclasses remain, and only one when the negative Pell equation is
soluble. Keep this norm-torus descent separate from theorem-level Selmer.

`wl544` expands those one or two unit classes into an exact integer system.
For quadratic forms `F,H,N` in `(u,v)`, the remaining conditions are
`Z^2=ell*N^2-F^2`, one homogeneous `G` square, and the exact homogenized
positivity inequality, with reconstruction `q=F/N`. This finite branch system
is the current gate; it is still not a family exclusion or M3 result.

`wl545` splits the trivial unit branch 2-adically. For `ell ≡ 5 (mod 8)`,
`q` is a 2-adic unit and `u,v` are odd. For `ell ≡ 1 (mod 8)`,
`v_2(q)>=3` and `u=2m,v=2n` with opposite-parity halves. The `G` condition
is automatic at `2` in both branches, so no further standalone 2-adic table
is a valid next step.

`wl546` couples that real-quadratic branch to Gaussian UFD. The Gaussian
square is replaced exactly by two quadratic-form orientations with
`x^2+y^2=D` and `Q` equal to one of two explicit forms. Only the homogeneous
`G` square and positivity remain on this trivial-unit double descent. Do not
mistake the finite orientations for a solved branch.

`wl547` applies a second Gaussian norm descent to the remaining `G` square.
All common odd factors are confined to primes `p|ell-1` with `(2/p)=1`; after
including `1+i`, the last square is a finite union
`delta=eta*d*gamma^2` over squarefree `S_ell` classes. This is not a
theorem-level Selmer object and the finite classes are not yet solved.

`wl548` computes the dyadic valuation in those classes exactly. It is `0` for
`ell ≡ 5 (mod 8)` and `4` for `ell ≡ 1 (mod 8)`, so `1+i` never occurs in
the squarefree factor `d`. Only the selected odd primes over `ell-1` remain;
they are still not solved and positivity has not yet been used.

`wl549` sharpens the odd support using the forced square `t=Q^2/D^2`. At a
common prime, `t^2+4t-4=0` makes `1-t=t^2/4` and `t+4=4/t`, so the source
square residues are automatic once the root `t` is square. Every
`p ≡ 7 (mod 8)` has exactly one such root; the common-prime residue test is
therefore exhausted there. The class equation, a fixed orientation, or
positivity must be used next.

`wl550` couples that surviving root to each `wl546` orientation over the same
common prime. Quadratic-etale Hilbert 90 shows both orientations realize every
`q` with `1-q^2` square, so they are automatically locally compatible with a
`wl549` square root. Same-prime orientation analysis is exhausted; the next
step must be genuinely global, multi-place, or use real positivity.

`wl551` uses the global norm equation. Since `Norm(delta)=W^2`, the
Gaussian-squarefree factor `d` has square norm. Conjugate primes over every
split `p` must therefore occur together, while an inert Gaussian prime is the
rational element `p`. Up to a unit, `d` is a rational squarefree divisor `r`
of `rad(ell-1)`. The next gate is the resulting rational-class coordinate
equation with one orientation, not independent Gaussian-prime enumeration.

`wl552` uses the dyadic coordinate parities in that global equation. After
removing the exact `(1+i)` power, `delta` has even real and odd imaginary
part, while an odd rational multiple of a Gaussian square has odd real and
even imaginary part. Hence the sole surviving unit class is `eta=i` in both
mod-8 branches. The next gate has one rational class and one unit class.

`wl553` transfers the quartic positivity exactly to the binary form
`C_ell(m,n)=ell(m^2-n^2)-2(ell-1)mn`. Its sign is positive in the
`ell ≡ 5 (mod 8)` normalization and negative in the `ell ≡ 1 (mod 8)`
normalization. Uniform parity/valuation-compatible cone points show positivity
alone is exhausted; the simultaneous orientation and both class-coordinate
equations must now be used.

`wl554` proves that the rational class `r` is not an independent divisor
choice. Odd common valuations of the two coordinates of a Gaussian square are
even, so
`r=sqf_odd(gcd(E,F))=sqf_odd(gcd(ell-1,R))`. The simultaneous system may now
substitute this candidate-canonical class directly.

`wl555` rotates back to the standard norm element
`Z=F+iE=r(a+ib)^2`. This removes the branch-dependent normalized signs:
positivity is uniformly
`ell(a^2-b^2)+2(ell-1)ab>0`, with `ab>0`. The next gate must combine this
unit-free equation and canonical `r` with one complete `wl546` orientation.

`wl556` performs that first coupling. With `a_0` odd, `b_0` even and
`x,y` opposite parity, `B_pi` is even and `R_pi` is odd. Hence
`ell ≡ 5 (mod 8)` retains only `R_pi`, while `ell ≡ 1 (mod 8)` retains only
`B_pi` (with `v_2(B_pi)>=3`). One complete orientation is eliminated in each
branch.

`wl557` stratifies the surviving orientations. The `R_pi` branch adds no new
2-adic condition. For the `B_pi` branch, with
`c=v_2(b_0)` and `k=v_2(xy)`, the two summand valuations are `c` and `k+1`;
`v_2(B_pi)>=3` holds exactly for `(c=2,k=1)` or `(c>=3,k>=2)`, and must match
`2+v_2(mu*nu)`. Standalone dyadic analysis is now exhausted.

`wl558` enters the first odd distinct-place gate. At an odd unit prime
`p|ell-1`, `Z=r(a+ib)^2` is automatic when `p ≡ 3 (mod 4)`, but for split
`p ≡ 1 (mod 4)` it forces `Legendre(F/r,p)=1`. Since canonical `r` records
the other common primes, this is a global character coupling rather than a
standalone residue table.

`wl559` handles the remaining positive even common valuations. After dividing
the common square `p^d`, inert places are automatic from the square norm;
split places impose one leading-component character, with explicit cases
`e<k`, `k<e`, and `e=k`. Together `wl558`-`wl559` partition every odd place
over `ell-1` not contained in `r`.

`wl560` supplies the missing odd-common leading character and unifies all
cases. With `d=min(v_p(ell-1),v_p(R))`, `epsilon=d mod 2`, and
`r_p=r/p^epsilon`, every split prime obeys
`Legendre((F_d+jE_d)/r_p,p)=1`; inert primes are automatic. The next gate is
now genuinely the assembled global character system.

`wl561` assembles that system over `F_2`. Rows are split primes `p|ell-1`,
columns are all odd `q|ell-1`, and the canonical valuation-parity vector
determines `r`. Reciprocity cancels split-split pairs in the product over
split primes contained in `r`, leaving only inert cross terms and the
candidate-dependent leading characters. The matrix alone gives no uniform
contradiction.

`wl562` proves the leading row bit is not determined by local source squares
and the selected orientation. Modulo `13`, the same unit stratum admits
source-compatible `t=0` with square `f(t)` and `t=10` with nonsquare `f(t)`;
both `B_pi` and `R_pi` realize both residues locally. Another residue-level
orientation table therefore cannot close `wl561`.

`wl563` returns to global integers. From `2rab=4(ell-1)Q^2D^2`, it writes
`2(ell-1)/r=kappa*h^2` and forces the coprime parts of `a,b` to be
`alpha*M^2,beta*N^2` with `alpha*beta=kappa`. The exact scale equation is
`gMN=h|QD|`, and the real coordinate becomes a quartic difference. The next
gate must attack these complementary divisor-split systems.

`wl564` assigns the factor `2` inside that complementary split whenever
`2|kappa`. For `ell ≡ 5 (mod 8)`, `r ≡ 1` puts `2` in `beta` and
`r ≡ 7` puts it in `alpha`. For `ell ≡ 1 (mod 8)`, the allocation is reversed
when `v_2(ell-1)` is even; when it is odd, `kappa` is odd. Only odd divisor
allocation remains.

`wl565` uses the quartic real coordinate to assign every odd inert factor of
`kappa`. For `q|kappa`, the normalized unit `U_q` has character `(-1/q)` if
`q|alpha` and `+1` if `q|beta`. Thus `q ≡ 3 (mod 4)` is uniquely assigned;
`q ≡ 1 (mod 4)` must have square `U_q` but retains a binary side choice. Only
split odd allocation remains.

`wl566` refines each remaining split factor with the quartic sign of
`H=alpha^2M^4-beta^2N^4`. If `q|alpha`, the sign is
`(-1)^((q-1)/4)(beta/q)`; if `q|beta`, it is `(alpha/q)`. Different predicted
signs select the side, but equal signs leave a coupled binary choice. The
remaining allocation is a finite quartic-character system.

`wl567` linearizes that system. After fixing already assigned factors, let
`x_q=1` mean a remaining split prime lies in `alpha`. The quartic-sign rows are
an explicit affine `F_2` system with Legendre-symbol off-diagonal entries.
Gaussian elimination replaces exponential allocation search, but its
right-hand vector still comes from the global square coordinates.

`wl568` proves the attempted global coupling adds no independent condition.
The scale equation is exactly the product-coordinate equality after cancelling
the known squareclass; the cone is exactly the original positivity identity;
and the affine rows hold automatically when their quartic signs come from the
same actual factorization. The allocation route is exhausted. The next exact
trivial-unit lemma is the selected `R_pi` or `B_pi` orientation intersected
with `F^2+E^2` square and strict positivity. Do not return to allocation
matrices or enter M3.

`wl569` proves `F<0` on every exact candidate because `0<q^2<ell`. Therefore
the positive ordered norm ratio is uniquely `tau=(C+F)/E`, and the cone gives

```text
rho_ell<tau<1,
rho_ell=(sqrt((ell-1)^2+ell^2)-(ell-1))/ell.
```

The reciprocal branch is closed. The next gate must couple this unique branch
to the selected `R_pi`/`B_pi` orientation; do not re-open the discarded branch
or enter M3.

`wl570` eliminates the quartic square root by the unique rational ratio and
gives the exact whole-`wl535` two-variable system. With
`delta=tau^2+2*tau-1`, every candidate satisfies

```text
ell=(tau*X^2+2*X*tau^2+8*X*tau-2*X-4*tau)/(2*X*delta),
ell-X=-(X*tau+2*X-2)*(2*X*tau-X-2*tau)/(2*X*delta),
ell*X+4=(X+2*tau+4)*(X*tau+4*tau-2)/(2*delta),
```

where `X` and the last two displayed values are rational squares and
`sigma_ell<X<ell`, `rho_ell<tau<1`. The converse reconstructs `q,p,c,V`.
The next gate must attack these simultaneous factored square predicates; do
not merely reintroduce an orientation, unit label, or `V`, and do not enter
M3.

`wl571` writes the four positive linear factors as `a,b,c,d`. The product

```text
Y^2=a*b*c*d
```

is a smooth genus-one curve with full rational `2`-torsion for every
admissible `tau`. Adding the exact squareclasses for `X` and one source square
gives a degree-eight multiquadratic cover: genus five for `tau!=1/2`, and
genus one at the unique drop `tau=1/2`. The exceptional system is

```text
ell=X+5-4/X,
p^2=5-4/X,
r^2=X+5,
X=q^2.
```

The next gate may attack this exceptional curve or the generic genus-five
cover without broad rank diagnostics. Do not claim either is empty or enter
M3.

`wl572` closes the exceptional curve. For reduced `q=a/b`, integrality of

```text
ell=(a^4+5*a^2*b^2-4*b^4)/(a^2*b^2)
```

forces `a^2|4` and `b=1`; positivity leaves `a^2=4`, hence `ell=8`, contrary
to the odd-prime parameter. Therefore `tau=1/2` is impossible. The next gate
must work on the generic genus-five cover with `tau!=1/2`; do not reopen the
exceptional branch or enter M3.

`wl573` writes `X=a^2/b^2`, `tau=m/n` primitively and proves

```text
a^2 divides 4*m*n,
b^2 divides m*n,
Delta=m^2+2*m*n-n^2 divides a^4+4*a^2*b^2-4*b^4,
gcd(Delta,m*n)=1.
```

This is the first global denominator coupling on the generic genus-five
cover. The next gate must combine it with one factored source square; do not
return to standalone local/dyadic tables or enter M3.

`wl574` defines the positive homogeneous factors `A,B,C,D` and proves, for

```text
2*Delta=k*h^2,
```

that

```text
A*B=k*U^2,
C*D=k*V^2.
```

After removing `g_1=gcd(A,B)` and `g_2=gcd(C,D)`, both pairs split into
coprime complementary squarefree factors of the same `k`. Moreover
`g_1|5a^4-8a^2b^2+4b^4` and
`g_2|a^4+8a^2b^2+20b^4`. The next gate must compare the two allocations, not
analyze either independently or enter M3.

`wl575` gives the exact comparison:

```text
R1*C=P*A-2*K*B,
R1*D=2*K*A+P*B,
R2*A=P*C+2*K*D,
R2*B=-2*K*C+P*D,
P^2+4*K^2=R1*R2.
```

For primitive `(a,b)`, both `gcd(P,K)` and `gcd(R1,R2)` are `1` when `a` is
odd and `4` when `a` is even. Thus every odd `q|k` lies in exactly one of the
three determinant cases. The next gate must classify allocation transport
under this rotation, not create a detached allocation table or enter M3.

`wl576` proves every odd `p|k` has `(2/p)=1`. If `p` divides neither
determinant, then `p|K` transports `A->C`, `B->D`, while `p|P` transports
`A->D`, `B->C`. If `p|R1`, both `A,B` vanish and the normalized first side
depends on the larger valuation; if `p|R2`, both `C,D` vanish with the inverse
ambiguity. The next gate must compute higher normalized valuation only at
these singular determinant primes. Do not return to residue-only tables or
enter M3.

`wl577` observes that `wl573` already proves `Delta|K`. Hence every odd
`p|k` divides `K`; the primitive norm identity forces `p` to divide none of
`P,R1,R2`. All odd primes therefore transport same-side, and the odd parts of
the two complementary allocations are identical. The only remaining factor
is `2`, which lies in `k` exactly when `m,n` have opposite parity. The next
gate must compare this single dyadic side, not reopen odd-prime analysis or
enter M3.

`wl578` divides the rotation by the common factor `e=1` or `4`. The normalized
matrix has odd diagonal and even off-diagonal entries, hence preserves which
coordinate has larger `v_2` when the valuations differ. Since `2|k` makes the
valuation sum odd, the dyadic side transports same-side. Therefore

```text
alpha=gamma,
beta=delta_0.
```

No allocation variable remains. The next gate must attack the resulting
square-magnitude equations; all further side-allocation analysis is forbidden,
and M3 remains closed.

`wl579` puts `lambda=beta/alpha`, `z=B/A=lambda*u^2`, and
`w=D/C=lambda*v^2`. The rotation is exactly

```text
w=(2*K+P*z)/(P-2*K*z),
lambda*v^2*(P-2*K*lambda*u^2)=2*K+P*lambda*u^2,
0<u^2<P/(2*K*lambda),
v>u.
```

The smooth projective completion is genus one for every admissible
`P,K,lambda`. This is only the projective magnitude system; it does not
reconstruct primitive `(m,n)` automatically. The next gate must impose those
linear-form/gcd constraints, not compute unrelated ranks or enter M3.

`wl580` proves

```text
tau=[X+2*z*(1-X)]/[X*(z+2)-2],
```

whose denominator is positive for `X>1,z>0`. Thus primitive `(m,n)` has no
extra branch. Requiring

```text
[lambda]=[2*(tau^2+2*tau-1)]
```

makes `z/lambda` and `w/lambda` square exactly equivalent to the two `wl570`
source-square predicates. The allocation/magnitude descent is exhausted. The
next gate must prove a rational-point obstruction on this self-consistent
family or produce a strict point; no further coordinate, gcd, valuation, or
allocation rewrite counts as progress, and M3 remains closed.

`wl581` maps the generic genus-five cover to the genus-two character quotient

```text
Z^2=X*a*b*c*d
```

over `Q`, then to a smooth elliptic quotient over `Q(i)`. `wl582` proves the
exact limitation of that quotient: for `S in Q` and nonzero
`Y=A+i*B`, its equation reconstructs

```text
X=-2*A/B,
Z=A*X,
```

and gives back the genus-two rational point. Consequently `S^2+16` is
automatically square on the relevant locus, and unrestricted elliptic
point/rank data is not a new obstruction. The next gate must attack positive
square `X`, one individual source-square lift, or the prime-parameter
condition. Do not reopen the automatic quadratic lift or enter M3.

`wl583` retains the two individual source squares on

```text
T_tau: U^2=a*b/(2*delta), V^2=c*d/(2*delta).
```

This is a genus-one torsor over `Q`, and the full generic genus-five cover is
exactly its fiber product with `q^2=X`. The function `X` has simple zeros and
poles on `T_tau`, so square `X` is genuinely independent. The next gate must
constrain positive square-`X` torsor points with the exact prime formula, or
the etale degree-two lift to the product elliptic curve. Unrestricted torsor
or product-curve ranks/points do not count as progress, and M3 remains closed.

`wl584` imposes `ell=L(X,tau)` and obtains the pointwise source curve

```text
U^2=X*(ell-X), V^2=ell*X+4.
```

It is genus one, and adjoining `q^2=X` is an unramified connected genus-one
cover encoding the first two `wl535` squares. The remaining parameter
quadratic has discriminant `4*G_ell(X)`. The next gate must attack this final
norm square on the square-`X` source curve with the selected real root and
prime parameter. Unrestricted source-curve/torsor ranks or points are not
progress, and M3 remains closed.

`wl585` proves the fixed-`ell` four-squareclass curve has genus seventeen and
that the selected `tau` interval is exactly the original positivity condition.
The product of all source and norm classes gives

```text
W^2=X*(ell-X)*(ell*X+4)*G_ell(X),
```

a genus-three curve with an explicit reciprocal elliptic quotient over `Q`.
The next gate must constrain its points whose quadratic lift has positive
square `X` and whose individual squareclasses all lift. Unrestricted elliptic
ranks or points do not count as progress, and M3 remains closed.

The `wl530-wl585` consolidated checkpoint independently verifies the key
algebra, converses, exceptions, and genus counts and marks the elliptic-
quotient subroute exhausted. Do not create `wl586` merely for another
equivalent model or quotient. Only three future outcomes count as progress:

1. a direct proof of `wl535`;
2. a strict counterexample satisfying every `wl535` condition;
3. a genuinely smaller arithmetic proposition, with a proof identifying the
   removed parameter, degree of freedom, or square lift.

If none is available, stop at the consolidated checkpoint. M2 remains open
and M3 remains closed.

`wl534` remains the prior exact reduction checkpoint. It takes the exact
`wl533` proposition and removes the automatic lower-positivity / `Q=0` branch
checks together with the auxiliary square-root variables `C` and `Y`. Fix
integers `a,b` with

```text
a^2 + b^2 = ell.
```

Then define

```text
D(u) = 1 + u^2
N(u) = b*(1-u^2) + 2*a*u
P(u) = a*(1-u^2) - 2*b*u
S(u) = ell*N(u)^2 + 4*D(u)^2
R(u) = ell*N(u)^4 + 4*N(u)^2*D(u)^2 - 4*ell*D(u)^4
```

and

```text
A(u) = -N(u)^4 + (8*ell-12)N(u)^2*D(u)^2 + 4*D(u)^4
B(u) =  N(u)^4 + 4*N(u)^2*D(u)^2 - 4*D(u)^4
T(u) = (A(u)^2 + B(u)^2)/2.
```

`wl534` proves that for rational `u`, both `P(u)` and `N(u)` are automatically
nonzero because their quadratic discriminants are `4*ell`, which is not a
rational square for an odd prime `ell`. Therefore the exact `wl533`
obstruction is equivalent to the following one-parameter statement:

```text
For every odd prime ell congruent to 1 mod 4, fix integers a,b with
a^2+b^2=ell. Then there is no rational u such that

S(u) is a rational square,
R(u) > 0,
T(u) is a rational square.
```

`wl534` is still not an exclusion theorem and not a counterexample. Only a
fresh narrow task may prove or refute this exact one-parameter square-predicate
proposition; do not enter M3 from this checkpoint.

`wl533` remains the prior exact reduction checkpoint. It took the exact
`wl532` proposition and shrank it inside the already-forced odd-prime class
`ell ≡ 1 (mod 4)` by absorbing the `Q square` and `ell-Q square` conditions
into one rational parameter `u`, leaving a triple `(u,C,Y)` with the quartic
`C^2 = ell*N(u)^2 + 4*D(u)^2`, the strict range
`0 < P(u)^2*C^2 < ell^2*N(u)^2*D(u)^2`, and the denominator-cleared square
identity `2*Y^2 = A(u)^2 + B(u)^2`.

`wl531` remains the prior exact reduction checkpoint. For the symbolic family
from `wl530`, it proved that the original positivity-domain question is
exactly equivalent to the following single arithmetic proposition: for every
odd prime `ell`, the paired rational quadratics

```text
z^2 = X^2 + (8 - 2*ell^2)*X + (ell^2 + 4)^2
U^2 = X^2 + (6*ell^2 - 16*ell + 8)*X + (5*ell^2 - 8*ell + 4)^2
```

have no point with

```text
0 < X < ell^2, X a rational square,
A_ell(X,z) = 2*(X-ell^2+4+z)/ell a rational square,
B_ell(X,z) = 2*(X-ell^2-4+z) a rational square.
```

The reduction includes the actual complete-`d` lift and all nonexceptional
denominator conditions. It is not an exclusion theorem or a counterexample.

`wl530` is the completed M1 input checkpoint. It derives the symbolic family

```text
support=v_ell|L=1|T=ell|d=(ell,1,ell)
```

for odd primes `ell`, including the complete-`d` equations, a function-field
chart, the `t,N,M` maps, the opposite-side product, and the square-locus
elliptic quotient family. At `ell=5` it recovers exactly the prior prototype

```text
support=v_5|L=1|T=5|d=(5,1,5)
```

from `wl528` and `wl529`.

`wl529` remains the completed one-family square-locus checkpoint. It uses the
`wl528` prototype and touches only:

```text
support=v_5|L=1|T=5|d=(5,1,5)
```

represented by `AA_A1_B4_v_5_m_tail_refresh_candidate` and
`BB_A4_B1_v_5_m_tail_refresh_candidate` in `wl495`.

The `wl522` taxonomy remains the finite input snapshot:

- 43 final candidate-ledger entries.
- 13 support families.
- 22 cover families.
- 5 ambient-globally-not-soluble cover families.
- 15 globally soluble but not AA+BB-admissible cover families.
- 2 processed / duplicate cover families.
- No genuinely deferred cover families.
- No AA+BB-admissible cover families.

The only named theorem-candidate pattern isolated by `wl522` was:

```text
common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families
```

`wl523` proves only the point-level form from existing `wl491` machinery. It
does not prove a uniform cover-family theorem. `wl525` proves only that the
finite taxonomy cannot be promoted to that theorem from the current inputs.
`wl526` then compares four routes and selects only a later gate:

```text
gather_minimal_function_field_squareclass_proof_data_for_named_cover_families
```

`wl527` enters that scoping gate and inventories the minimum function-field
proof data for the named cover families: model inventory, source-side maps,
candidate `N,M` function-field elements, opposite-side product
squareclass/divisor-parity target, and exceptional specialization / positivity
separation. It finds:

```text
ready_cover_family_count = 0
not_ready_cover_family_count = 15
exact_missing_data_class =
  uniform_function_field_model_maps_and_squareclass_certificate
```

No next roadmap step is entered in `wl527`.

`wl528` then supplies the first explicitly selected single-family
function-field prototype. It reconstructs the chart

```text
Q(r,y)/(y^2 - (5*r^4 - 264*r^2 + 2000))
```

derives rational maps to

```text
t = y*(r^2+20)/(4*r*(r^2-20))
N = (5+t)/2
M = (5-t)/2
```

and proves the opposite leg-4 product

```text
(N^2+16)(M^2+16)
```

is nonsquare in this prototype function field by a checked smooth
nonexceptional rational specialization:

```text
r = 10, y = 160, t = 6, N = 11/2, M = -1/2
(N^2+16)(M^2+16) = 12025/16
```

which is not a rational square.

`wl529` analyzes the remaining pointwise square-specialization locus

```text
U^2 = t^4 + 78*t^2 + 7921
```

through the degree-two map `X=t^2, Y=tU` to
`Y^2=X^3+78X^2+7921X`. A rigorous rank-zero and torsion computation on this
elliptic quotient leaves only `t=0`; an executable discriminant certificate
then proves that `t=0` has no rational lift to the `wl528` quartic. Thus the
one-family positivity-domain square-locus question is closed.

`wl530` does not classify rational points on the general elliptic fibers. The
subsequent `wl531`, `wl532`, `wl533`, `wl534`, and `wl535`
reductions do not solve the remaining arithmetic proposition. None of
`wl530`, `wl531`, `wl532`, `wl533`, `wl534`, or `wl535` is a uniform
cover-family theorem or a Selmer/rank/Sha/family-exclusion claim. Do not
enter another support family or skip ahead to M3.

## Do Not Reopen

Unless the user explicitly asks for one of these, do not:

- execute shell 11;
- compute new supports;
- test new ambient `C_d` solubility;
- apply `wl491` to a new point;
- select a final obstruction candidate;
- run broad rank/Selmer diagnostics;
- treat the 15 not-admissible cover families as a theorem;
- claim that `wl523`, `wl525`, `wl526`, `wl527`, `wl528`, `wl529`, `wl530`, `wl531`, `wl532`, `wl533`, `wl534`, or `wl535`
  proves a uniform cover-family obstruction;
- build additional function-field models or prove the uniform lemma unless
  that gate is explicitly entered.
- treat `wl527` proof-data scoping as a ready proof attempt.
- treat `wl528` as more than one checked single-prototype nonsquare
  certificate.
- treat `wl529` as more than one closed one-family positivity-domain
  square-locus audit.
- treat `wl530` as more than the symbolic M1 derivation, or as a rational-point
  classification of the general square-locus elliptic family.
- treat `wl531` as a proof of its exact missing proposition, a uniform
  exclusion theorem, or a counterexample.
- treat `wl532` as a proof of its remaining `Q`-coordinate quartic
  obstruction, a uniform exclusion theorem, or a counterexample.
- treat `wl533` as a proof of its remaining one-parameter conic-quartic
  obstruction, a uniform exclusion theorem, or a counterexample.
- treat `wl534` as a proof of its remaining one-parameter square-predicate
  obstruction, a uniform exclusion theorem, or a counterexample.
- treat `wl535` as a proof of its remaining q-root-coordinate square/quartic
  obstruction, a uniform exclusion theorem, or a counterexample.

The old package-`x` / `S~` bridge is not a theorem-level Selmer object. Do not
route new evidence back into that ledger as if it proved a Selmer upper bound.

## Object Boundaries

Keep these layers separate in every explanation, worklog, and script result:

- `single_curve_full_2_selmer`: diagnostics for one elliptic curve.
- `S~`: old AA+BB common-source pseudo-container; useful history, not a final
  Selmer upper-bound object.
- complete `d`-coordinate `C_d` ledger: current local-solubility framework.
- `M_tail`: parameter-dependent residual `F2` matrix, not uniformly full rank.
- AA+BB admissibility: common-source closure constraints after an ambient
  `C_d` point is found.
- theorem-level `Sel_2(E_L/Q)`: only this can support a rank-zero theorem.

## Hard No-Claim Rules

Do not claim any of the following unless the work proves a complete Selmer
upper bound:

- `rank(E_L)=0` as a family theorem;
- `dim Sel_2(E_L/Q)=2`;
- `Sha(E_L)[2]=0`;
- family exclusion;
- Harborth global theorem.

Counts are not proof progress by themselves. More packages, samples,
candidates, or JSON rows are progress only if they shrink a stated theorem gap
or produce a strict certificate.

## Worklog Pattern

New research steps should usually have all three pieces:

- `docs/work-logs/<number>-<slug>.md`
- `scripts/theory/audit_<slug>.py`
- `tests/test_<slug>.py`

Each worklog should answer:

- What exact question is being audited?
- Which earlier worklog is the input?
- Which object layer is being touched?
- What is proved, what is only sampled, and what remains unproved?
- Which forbidden theorem claims remain false?
- What is the next narrow gate, and whether it is entered here.

Do not edit old worklogs except for clear typo/index maintenance. For route
state after `wl535`, keep the full handoff in `docs/NEXT_RESEARCH_GATE.md`
short and point readers to the relevant worklog.

## Verification

Use `uv` with a temp cache outside the repo:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest <focused tests>
```

For broad hygiene:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest
uv run ruff check .
```

The generated JSON artifacts under `results/` are ignored by default. Do not
force-add them unless the user explicitly asks for a result artifact to become
tracked source material.

## When To Create A Skill

Do not create a reusable skill while the math route is still moving. First keep
the workflow in `AGENTS.md` and `docs/NEXT_RESEARCH_GATE.md`. Extract a skill
only after the same gate pattern has been repeated enough times that the input
objects, forbidden claims, test command, and output schema are stable.
