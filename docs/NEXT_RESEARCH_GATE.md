# Next Research Gate

This page is the short handoff for the next agent. It names the current gate,
the closed route state, and the moves that must not be reopened accidentally.

## Current Gate

If `wl592` is present, the completed handoff is:

```text
wl592_mixed_p17_factor_twist_local_image_complete
```

Do not re-enter `wl535`. `wl587`, `wl589`, `wl590`, and `wl591` remain frozen
inputs.
The exact `p=5` normalized factor-twist images remain

```text
I_{5,u} = empty set
I_{5,m} = {[5]}
```

The place is family-specific: all pure named representatives are deleted and
the mixed survivors are `5, 3045, 66045, 91205`. This closes the selected gate;
preserve the exact pole, boundary, factor-zero, and AA+BB lift evidence in
`docs/work-logs/590-p5-factor-twist-local-image-comparison.md`.

`wl591` then resolves the selected mixed `p=7` obligation exactly:

```text
I_{7,m} = {[1]}
```

The four mixed representatives map as `5 -> [u]`, `3045 -> [7]`,
`66045 -> [7u]`, and `91205 -> [1]`; hence the first three are deleted and
`91205` survives. The proof includes all affine/infinity strata, poles,
factor-zero and zero-value branches, the fixed-cover coordinate `R`, and the
exact AA+BB lift.

`wl592` then resolves the selected mixed `p=17` obligation exactly:

```text
I_{17,m} = {[u]}
[91205] = [17u] not in I_{17,m}
```

The complete proof covers integral affine disks, every negative-valuation and
infinity disk, D/A denominator poles, factor-zero and R=0 branches, zero-value
branches, the fixed-cover coordinate `R`, and the exact AA+BB lift. Controller
review found no blocking mathematical issue. Cumulatively, `wl590`-`wl592`
leave no real/`Q_2`-filtered factor-twist candidate for either frozen
representative. This is only a fixed-representative local-solubility
conclusion; it is not a family exclusion, Selmer/rank theorem, or D2 result.
No later gate is selected.

## Historical wl535 Chain

`wl535` takes the exact `wl534` one-parameter square-predicate obstruction and
removes the last dependence on the chosen sum-of-two-squares chart
`a^2+b^2=ell` and the affine parameter `u`. Keep

```text
D(u) = 1 + u^2
N(u) = b*(1-u^2) + 2*a*u
P(u) = a*(1-u^2) - 2*b*u
```

and define

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

Therefore the only remaining exact obstruction is:

```text
For every odd prime ell congruent to 1 mod 4, there is no rational pair (q,V)
such that

ell - q^2 is a rational square,
ell*q^2 + 4 is a rational square,
ell*q^4 + 4*q^2 - 4*ell > 0,
V^2 = G_ell(q^2).
```

This is still an exact missing proposition, not a uniform exclusion theorem
and not a counterexample. Stop at this direct `q`-root-coordinate
square/quartic obstruction. Do not enter M3.

`wl536` records one strict local consequence without changing that gate:
inside the exact `wl535` rational system, the residue class

```text
ell ≡ 5 (mod 7)
```

is impossible. The proof uses only the `wl535` equations. Because

```text
7 ≡ 3 (mod 4),
```

any rational solution of

```text
p^2 + q^2 = ell
```

with `7 ∤ ell` is automatically `7`-adically integral in `p` and `q`, so
`q^2`, `ell-q^2`, `ell*q^2+4`, and `G_ell(q^2)` reduce to square classes mod
`7`. For `ell ≡ 5 (mod 7)`, the only possible residues

```text
q^2 mod 7 ∈ {0,1,2,4}
```

all fail one of those square tests. So the open part of `wl535` now lies only
in the complementary odd-prime classes. This is still not a full proof of the
remaining `wl535` proposition, not a counterexample, and not M3.

`wl537` records a second strict local consequence. The same denominator
argument at `11 ≡ 3 (mod 4)` makes `p,q` 11-adically integral whenever
`11 ∤ ell`. For `ell ≡ 10 (mod 11)`, every square residue
`q^2 mod 11 ∈ {0,1,3,4,5,9}` fails one of the reductions of `ell-q^2`,
`ell*q^2+4`, and `G_ell(q^2)`. With `ell ≡ 1 (mod 4)`, this excludes the
infinite prime class `ell ≡ 21 (mod 44)`. The open part of `wl535` is now
outside the union of the `wl536` and `wl537` classes. This remains a partial
M2 result, not a full `wl535` proof and not M3.

`wl538` adds the analogous direct obstruction at `19`. For
`ell ≡ 15 (mod 19)`, all ten square residues for `q^2 mod 19` fail one of the
same three necessary square tests. Under `ell ≡ 1 (mod 4)`, this excludes the
infinite prime class `ell ≡ 53 (mod 76)`. The full proposition remains open
outside the union of the three recorded local classes.

`wl539` closes the direct single-prime good-reduction residue-table method.
It adds `(p,e)=(23,5)`, hence the infinite prime class
`ell ≡ 5 (mod 92)`, and proves the complete auxiliary-pair list is

```text
(7,5), (11,10), (19,15), (23,5).
```

A quadratic-character lower bound guarantees a nonzero residue survivor for
all relevant `p >= 1907`; exact enumeration below that bound proves the list.
Therefore another table of the same type is forbidden as route progress. The
next gate must use bad-reduction/valuation information, genuinely coupled
local conditions, descent, or a strict rational counterexample. The full
`wl535` proposition remains open and M3 is not entered.

`wl540` enters only the parameter-prime valuation gate. It proves
`v_ell(q)=0`; the square roots of `ell-q^2` and `ell*q^2+4` are units as well.
Writing `Q=q^2`, the final square condition is either a nonzero square modulo
`ell`, or `Q` lies at positive even distance from a unique simple Hensel root
of `G_ell`. The root identity

```text
Q*(Q/4+2-i/2)^2=2
```

shows that the root branch requires `ell ≡ 1 (mod 8)`. Thus
`ell ≡ 5 (mod 8)` has only the nonzero unit branch. The next gate must analyze
that unit branch and, separately, the even-distance branch for
`ell ≡ 1 (mod 8)`. No full exclusion or M3 step is proved.

`wl541` proves that the unit branch is always populated locally. The curve

```text
y^2 = x^8+16*x^6+72*x^4-64*x^2+16
```

is a smooth genus-three curve over every odd parameter prime. Hasse-Weil plus
seven explicit small-prime witnesses produces `x*y != 0` for every
`ell ≡ 1 (mod 4)`, and the point simultaneously Hensel-lifts the three square
equations with the same unit `q=x`. Therefore the parameter prime alone never
locally excludes the algebraic wl535 system. The next gate must genuinely
couple places, use descent/global information, or combine arithmetic with the
real positivity predicate. No rational point or M3 result follows.

`wl542` couples the first two square equations through a primitive global
denominator. Writing `a=A/D`, `q=Q/D`, it proves `D` is odd and coprime to
`ell`, and every `r|D` satisfies

```text
r ≡ 1 (mod 4), (ell/r)=(r/ell)=1.
```

Thus every denominator prime splits completely in `Q(i,sqrt(ell))` and
`D mod ell` is a nonzero square. The exact local converse also holds: at any
such negative-valuation place, the first two equations and `G_ell(q^2)` are
automatically local squares, since their remaining factors are odd-prime
principal units. So denominator-place analysis alone is also exhausted. The
next gate must derive a global relation among the split support, numerator,
and positivity, or use descent/counterexample evidence. M3 remains closed.

`wl543` performs the selected global descent in `K=Q(sqrt(ell))`. With

```text
alpha=(C+Q*sqrt(ell))/2,
```

the primitive equation gives a totally positive integral element of norm
`D^2`, and coprimality with its conjugate gives `(alpha)=a^2`. Since `K` has
prime discriminant, ordinary genus theory gives `Cl(K)[2]=0`, hence

```text
alpha=epsilon*beta^2.
```

Here `epsilon` is totally positive and has at most two classes modulo unit
squares. If `x^2-ell*y^2=-4` is soluble, a norm-`-1` unit exists and the unit
class is trivial. The next gate must write these one or two element equations
explicitly and combine them with the Gaussian equation, `G_ell`, and
positivity. This is not theorem-level Selmer and does not enter M3.

`wl544` makes the `wl543` descent explicit. For each of at most two unit
representatives `epsilon=(r+s*sqrt(ell))/2`, put

```text
N=u^2-ell*v^2,
F=s*(u^2+ell*v^2)+2*r*u*v,
H=r*(u^2+ell*v^2)+2*ell*s*u*v.
```

Then `H^2-ell*F^2=4N^2`, and the exact remaining system is

```text
N != 0,
Z^2=ell*N^2-F^2,
W^2=J_ell(F,N),
ell*F^4+4*F^2*N^2-4*ell*N^4>0.
```

It reconstructs `q=F/N`, `a=Z/N`, `c=H/N`, and `V=W/N^4`. Thus the
unbounded denominator and ideal-class data are gone; only one or two explicit
integer quartic branches remain. The next gate must attack one branch or prove
that this descent stalls. Do not enter M3.

`wl545` attacks only the trivial unit class at `2`. In primitive normalization
`v_2(N)=2`, and the exact dichotomy is

```text
ell ≡ 5 (mod 8): v_2(q)=0 and u,v are odd;
ell ≡ 1 (mod 8): v_2(q)>=3 and u=2m,v=2n with m,n opposite parity.
```

The valuations `1` and `2` are impossible by the squareclass of
`ell*q^2+4`. In both surviving branches `G_ell(q^2)` is automatically a
2-adic square. Thus prime `2` is exhausted as a standalone obstruction on the
trivial unit branch. The next gate must use an odd/global condition or
positivity on one of these two parity branches. Do not enter M3.

`wl546` removes the Gaussian square variable on the trivial unit branch. Fix
`ell=a_0^2+b_0^2`. Gaussian UFD leaves exactly two essential orientations:

```text
Q=+/-[b_0*(x^2-y^2)+2*a_0*x*y],
Q=+/-[a_0*(x^2-y^2)-2*b_0*x*y],
x^2+y^2=D.
```

Combining `Q=uv` and `D=abs(u^2-ell*v^2)/4` gives two exact double-descent
systems. The Gaussian square is gone; the remaining obstruction is the
homogeneous `G` square plus positivity on these systems. The next gate must
attack one orientation or prove an exact failure point. Do not enter M3.

`wl547` reduces the remaining homogeneous `G` square to finite Gaussian
squareclasses. With

```text
delta=(P+iR)/(1+i), Norm(delta)=W^2,
```

every common odd prime of `delta` and its conjugate lies over

```text
p|ell-1, (2/p)=1,
```

and a candidate must additionally satisfy
`(Q^2/D^2)^2+4(Q^2/D^2)-4=0 mod p`. Therefore

```text
delta=eta*d*gamma^2
```

with squarefree `d` supported on the finite set consisting of `1+i` and those
primes over `ell-1`. The next gate must analyze these finite classes together
with a wl546 orientation and positivity. This is not theorem-level Selmer and
does not enter M3.

`wl548` removes the dyadic generator from that finite set. On the two `wl545`
parity branches it proves respectively

```text
v_(1+i)(delta)=0,
v_(1+i)(delta)=4.
```

Both valuations are even, so the squarefree `d` is supported only at odd
Gaussian primes over `p|ell-1` with `(2/p)=1`, still subject to the `wl547`
root condition. The next gate must analyze an odd class with one `wl546`
orientation and positivity. The nontrivial real-unit class remains separate,
and M3 is not entered.

`wl549` classifies the remaining common-prime root test exactly. At a root
`t=Q^2/D^2` of `t^2+4t-4`, one has

```text
1-t=t^2/4,
t+4=4/t.
```

Thus a square root `t` automatically passes both reduced source-square tests.
For `p ≡ 7 (mod 8)` exactly one of the two roots is square; for
`p ≡ 1 (mod 8)` either zero or both are square. The safe support is refined
to primes for which a square root exists, but the entire `7 mod 8` branch
survives. Another common-prime residue-square test is not a valid next gate.
The next step must use the odd valuation/class equation with one fixed
`wl546` orientation or positivity. M3 remains closed.

`wl550` performs the same-prime coupling to both fixed `wl546` orientations.
In `F_p[i]`, every norm-one element is `z/conjugate(z)`; explicitly use
`z=1+h` unless `h=-1`, when `z=i` works. Therefore each orientation realizes
every `q` satisfying `A^2+q^2=1`. Since `wl549` gives
`1-q^2=t^2/4`, both orientations are locally compatible with every surviving
root-square class. Same-prime orientation tables are now exhausted. The next
gate must use the global integer class equation, couple distinct places, or
use positivity. M3 remains closed.

`wl551` then uses the global equation rather than another local table. From

```text
delta=eta*d*gamma^2,
Norm(delta)=W^2,
```

it follows that `Norm(d)` is a square. At each split rational prime, the two
conjugate Gaussian primes must occur together; an inert Gaussian prime is
already the rational element `p`. Hence, up to a unit,

```text
d=r,
r | rad(ell-1),
```

with `r` rational and squarefree and with the `wl549` support restriction.
The next gate must use the real/imaginary coordinate equation for
`delta=eta*r*gamma^2` together with one fixed orientation or positivity. M3
remains closed.

`wl552` eliminates the remaining Gaussian unit choice. In the
`ell ≡ 5 (mod 8)` branch, `delta` has even real and odd imaginary coordinate,
whereas `r*gamma^2` has odd real and even imaginary coordinate. In the
`ell ≡ 1 (mod 8)` branch the same comparison holds after dividing by the
exact factor `-4=((1+i)^2)^2`. Therefore, uniformly,

```text
eta=i modulo Gaussian unit squares.
```

The next gate is the single `eta=i`, rational-squarefree-`r` coordinate
system coupled to a fixed `wl546` orientation or positivity. M3 remains
closed.

`wl553` transfers the exact positivity polynomial through the class
coordinates. With

```text
C_ell(m,n)=ell*(m^2-n^2)-2*(ell-1)*m*n,
```

positivity is `C_ell>0` for `ell ≡ 5 (mod 8)` and `C_ell<0` for
`ell ≡ 1 (mod 8)`. The uniform cone witnesses `(5,-8)` and
`(1,2^k)` show that parity, dyadic valuation, and positivity alone do not
exclude either branch. The next gate must use the full simultaneous system:
one fixed `wl546` orientation, both `eta=i` coordinate equations, and the
appropriate strict cone. M3 remains closed.

`wl554` removes `r` as an independent finite choice. For every odd prime, the
common valuation of `m^2-n^2` and `2mn` is even. Therefore

```text
r=sqf_odd(gcd(E,F))
 =sqf_odd(gcd(ell-1,R)),
```

where `sqf_odd` keeps primes occurring to odd valuation. The equality uses
the fact that a common odd prime cannot divide `Q` or `D`. The next gate must
attack one simultaneous orientation/class/cone system after substituting this
canonical `r`; no divisor-class enumeration remains. M3 stays closed.

`wl555` replaces the branch-normalized coordinates by the standard norm
element

```text
Z=F+i*E=r*(a+i*b)^2.
```

Thus `F=r(a^2-b^2)`, `E=2rab`, `ab>0`, and positivity is the single uniform
cone

```text
ell*(a^2-b^2)+2*(ell-1)*a*b>0.
```

The next gate must combine this unit-free standard equation, canonical `r`,
and one complete `wl546` integer orientation. M3 remains closed.

`wl556` couples the dyadic branch to the two `wl546` orientations. Choose
`a_0` odd and `b_0` even. Since `x,y` have opposite parity,

```text
B_pi is even,
R_pi is odd.
```

Therefore `ell ≡ 5 (mod 8)` permits only `Q=+/-R_pi`, while
`ell ≡ 1 (mod 8)` permits only `Q=+/-B_pi`, with the additional condition
`v_2(B_pi)>=3`. The next gate must attack one of these two surviving
branch-specific simultaneous systems; no second orientation remains inside a
fixed branch. M3 remains closed.

`wl557` gives the exact remaining dyadic strata. The `R_pi` branch for
`ell ≡ 5 (mod 8)` is automatically odd and gains no further condition. In the
`B_pi` branch, put `c=v_2(b_0)>=2` and `k=v_2(xy)>=1`. Then

```text
v_2(B_pi)=c       if c<k+1,
v_2(B_pi)=k+1     if c>k+1,
v_2(B_pi)>=c+1    if c=k+1,
```

and `v_2(B_pi)>=3` exactly in the strata `(c=2,k=1)` or
`(c>=3,k>=2)`. This value must equal `2+v_2(mu*nu)` from `u=2mu,v=2nu`.
The strata remain locally populated, so the next gate must use an odd/global
condition or the full standard square/cone; further standalone dyadic work is
closed. M3 remains closed.

`wl558` applies that standard square at odd unit primes. If `p|ell-1` and
`p∤R`, then `Z/r` reduces to the rational unit `F/r`. For
`p ≡ 3 (mod 4)` it is automatically a square in `F_(p^2)`. For split
`p ≡ 1 (mod 4)`, every candidate must satisfy

```text
Legendre(F/r,p)=1.
```

When `p∤QD`, this is `Legendre((t^2+4t-4)/r,p)=1`; when `p|Q` or `p|D`, it
reduces to `Legendre(r,p)=1`. Since `r` depends on the other common primes,
this is a distinct-place condition. The next gate must combine these
characters and handle positive even common valuations. M3 remains closed.

`wl559` handles those positive even valuations. Put
`e=v_p(ell-1)`, `k=v_p(R)`, and `d=min(e,k)>0` even, then divide
`Z=r*Gamma^2` by `p^d`. Inert primes again add no condition. For split primes,
with `j^2=-1`, the normalized leading component must satisfy

```text
Legendre((F_d+j*E_d)/r,p)=1.
```

This becomes `Legendre(L_e*(-1+j)/r,p)=1` for `e<k`,
`Legendre((R/p^k)/r,p)=1` for `k<e`, and
`Legendre(L_e*(lambda-1+j)/r,p)=1` for `e=k`. Together `wl558` and `wl559`
cover every odd `p|ell-1` not in `r`; odd common valuation is exactly `p|r`
but still needs its leading character.

`wl560` supplies that missing case and unifies all valuation parities. Put

```text
d=min(v_p(ell-1),v_p(R)),
epsilon=d mod 2,
r_p=r/p^epsilon.
```

After dividing by `p^d`, every split prime satisfies

```text
Legendre((F_d+j*E_d)/r_p,p)=1,
```

with the same `e<k`, `k<e`, and `e=k` leading forms as above; inert primes
are automatic. Every odd place over `ell-1` is now fully classified. The next
gate is the assembled global character system. M3 remains closed.

`wl561` assembles the split-prime equations as an `F_2` system. With

```text
epsilon_q=min(v_q(ell-1),v_q(R)) mod 2,
n_p=(1-Legendre(C_p,p))/2,
A_pq=(1-Legendre(q,p))/2,
```

the rows are

```text
n_p=sum_(q!=p) A_pq*epsilon_q mod 2.
```

Multiplying the rows for split `p|r` cancels all split-split pairs by
quadratic reciprocity. The remaining product contains only inert factors of
`r` and the candidate-dependent leading characters. Hence the matrix alone
does not uniformly contradict a candidate. The next gate must relate those
leading characters to the surviving orientation/source equations or isolate
a parameter subfamily with the wrong reciprocity sign. M3 remains closed.

`wl562` tests whether the leading row bit can be recovered from the local
source squares and selected orientation. Modulo `13`, both

```text
t=0,  f(t)=9 square,
t=10, f(t)=6 nonsquare
```

have `t`, `1-t`, and `t+4` square and lie in the same unit stratum. Exact
local witnesses show that both the `B_pi` and `R_pi` orientations realize the
corresponding `q=0` and `q=6`. Thus the local orientation data admits both row
bits. The next gate must use global integer compatibility, positivity, or a
parameter subfamily with a globally forced wrong sign; another residue-level
orientation table is closed. M3 remains closed.

`wl563` returns to global integer compatibility. From

```text
2*r*a*b=4*(ell-1)*Q^2*D^2
```

put `2(ell-1)/r=kappa*h^2` with `kappa` squarefree. After removing
`g=gcd(a,b)`, coprimality forces

```text
a=g*alpha*M^2,
b=g*beta*N^2,
alpha*beta=kappa,
g*M*N=h*abs(Q*D).
```

The real coordinate is

```text
F=r*g^2*(alpha^2*M^4-beta^2*N^4),
```

and positivity becomes the corresponding quartic inequality. The next gate
must attack a complementary divisor split `alpha*beta=kappa` together with
the selected orientation, not return to local row tables. M3 remains closed.

`wl564` assigns the dyadic factor in that split. For `ell ≡ 5 (mod 8)`,
`2|kappa` always and

```text
r ≡ 1 (mod 8) => 2|beta,
r ≡ 7 (mod 8) => 2|alpha.
```

For `ell ≡ 1 (mod 8)`, `2|kappa` exactly when `v_2(ell-1)` is even, and the
allocation is reversed. If `v_2(ell-1)` is odd, `kappa` is odd. The next gate
must constrain the remaining odd allocation using the quartic real coordinate
and selected orientation, or certify those finite split systems as the exact
global lemma. M3 remains closed.

`wl565` constrains every odd factor `q|kappa` using the real-coordinate unit

```text
U_q=(F/r)/q^v_q(F/r) mod q.
```

The exact rule is

```text
q|alpha => Legendre(U_q,q)=Legendre(-1,q),
q|beta  => Legendre(U_q,q)=1.
```

Hence every `q ≡ 3 (mod 4)` is uniquely assigned to `alpha` or `beta`. For
`q ≡ 1 (mod 4)`, `U_q` must be a square but the side remains unresolved at
quadratic-character level. Together `wl564`-`wl565` assign the dyadic and all
inert factors; the next gate must constrain split odd allocation by quartic
residues, the selected orientation, or the scale equation. M3 remains closed.

`wl566` applies the quartic sign of

```text
H=alpha^2*M^4-beta^2*N^4
```

at each remaining split `q|kappa`. The exact alternatives are

```text
q|alpha => chi_4,q(H)=(-1)^((q-1)/4)*Legendre(beta,q),
q|beta  => chi_4,q(H)=Legendre(alpha,q).
```

If the predicted signs differ, the observed sign uniquely selects the side;
if they agree, quartic character still leaves the binary choice unresolved.
Thus the remaining allocation is a finite coupled quartic-character system,
not independent choices. The next gate must assemble that system with the
scale/orientation equation or certify it as the exact unresolved global
lemma. M3 remains closed.

`wl567` shows the coupled quartic allocation is affine-linear over `F_2`.
After fixing the dyadic and inert factors, put `x_q=1` when a remaining split
prime `q` lies in `alpha`. With

```text
A_qt=(1-Legendre(t,q))/2,
Delta_q=d_q+a_q+b_q+sum_(t!=q) A_qt,
z_q=(1-chi_4,q(H))/2,
```

each row is

```text
Delta_q*x_q+sum_(t!=q) A_qt*x_t=z_q+a_q.
```

Gaussian elimination therefore gives inconsistency, a unique allocation, or
an explicit affine space. The right-hand vector still depends on the global
square coordinates, and every surviving allocation must satisfy the scale,
orientation, real-coordinate, and cone equations. The next gate must couple
the affine space to those integer equations or certify the combined system as
the exact unresolved global lemma. M3 remains closed.

`wl568` completes that coupling audit and proves it cannot supply an
independent obstruction. With the `wl563` notation,

```text
g*M*N=h*abs(Q*D)
```

is equivalent to the imaginary-coordinate equality, and the cone is the
original positivity identity because

```text
ell*Q^4+4*Q^2*D^2-4*ell*D^4=ell*F+(ell-1)*E.
```

Moreover, every `wl567` row holds automatically if `z_q` is computed from the
same actual `H=alpha^2*M^4-beta^2*N^4`. The converse is false: a row solution
does not construct `M,N` or a rational point. Finally, with
`A=alpha*M^2`, `B=beta*N^2`, the real/product equations collapse to

```text
2*F*A*B=E*(A^2-B^2),
C=E*(A^2+B^2)/(2*A*B),
C^2=F^2+E^2.
```

The reverse norm-square implication has two ordered sign branches, and the
actual Gaussian factorization chooses the displayed one. Thus the allocation
route only factors the original norm square; it does not independently
exclude a branch. The
next exact trivial-unit gate is the selected `R_pi`/`B_pi` orientation
intersected directly with `F^2+E^2` square and strict positivity. Keep the
nontrivial real-unit class separate; do not return to allocation refinements
or enter M3.

`wl569` uses `ell-q^2` square and strict positivity to get
`0<q^2<ell`. On that interval,

```text
F/D^4=X^2+(8-4*ell)*X-4<0,
X=q^2.
```

Thus the positive ordered ratio in `wl568` is uniquely

```text
tau=A/B=(C+F)/E,
```

and the reciprocal ordered branch is impossible. The cone is equivalent to

```text
rho_ell<tau<1,
rho_ell=(sqrt((ell-1)^2+ell^2)-(ell-1))/ell,
```

with `sqrt(2)-1<rho_ell<1/2`. The next exact gate must couple this unique
archimedean branch directly to the selected `R_pi`/`B_pi` orientation. The
surviving interval is not proved empty; M3 remains closed.

`wl570` removes the norm-square root with the unique rational `tau`. Put

```text
delta=tau^2+2*tau-1.
```

Then the whole `wl535` system is exactly equivalent to rational `(X,tau)` in
the `wl569` intervals satisfying

```text
ell=(tau*X^2+2*X*tau^2+8*X*tau-2*X-4*tau)/(2*X*delta),

ell-X=-(X*tau+2*X-2)*(2*X*tau-X-2*tau)/(2*X*delta),

ell*X+4=(X+2*tau+4)*(X*tau+4*tau-2)/(2*delta),
```

with `X`, `ell-X`, and `ell*X+4` rational squares. Conversely these data give

```text
q^2=X,
C=4*(ell-1)*X*(1+tau^2)/(2*tau),
C^2=G_ell(X),
```

and reconstruct every exact `wl535` condition. This equivalence is taken
before the real-unit split; it does not merge or eliminate those classes. The
next gate must use the simultaneous factor structure or produce a strict
point. Reintroducing `V`, an orientation, or an allocation is not progress.
M3 remains closed.

`wl571` names the four positive linear factors

```text
a=X*(tau+2)-2,
b=2*tau-X*(2*tau-1),
c=X+2*tau+4,
d=tau*(X+4)-2.
```

Their pairwise projective determinants are nonzero throughout the admissible
interval, so

```text
Y^2=a*b*c*d
```

is a smooth genus-one quartic with four rational branch points. The complete
three-squareclass cover has six inertia-two branch points and genus five for
`tau!=1/2`. At the unique collision with `0` and infinity, `tau=1/2`, it has
four branch points and genus one, with exact equations

```text
ell=X+5-4/X,
p^2=5-4/X,
r^2=X+5,
X=q^2.
```

This is a curve classification, not a rational-point computation. The next
gate may attack the exceptional genus-one branch exactly or derive a uniform
obstruction on the generic genus-five cover. Finite point counts and broad
rank diagnostics remain forbidden; M3 remains closed.

`wl572` excludes the exceptional branch by integrality alone. If
`q=a/b` is reduced, then

```text
ell=(a^4+5*a^2*b^2-4*b^4)/(a^2*b^2).
```

An integral `ell` forces `a^2|4*b^4` and `b^2|a^4`; coprimality gives
`a^2|4` and `b=1`. Positivity excludes `q^2=1`, while `q^2=4` gives
`ell=8`, not an odd prime. Hence

```text
tau!=1/2
```

for every candidate. The next gate is solely the generic genus-five cover.
Do not reopen the exceptional elliptic branch, use finite counts as proof, or
enter M3.

`wl573` enters the generic cover with primitive coordinates

```text
X=a^2/b^2,
tau=m/n,
Delta=m^2+2*m*n-n^2>0.
```

Homogenizing `ell=L(X,tau)` and reducing its numerator modulo `a^2`, `b^2`,
and `Delta` proves

```text
a^2|4*m*n,
b^2|m*n,
gcd(Delta,m*n)=1,
Delta|a^4+4*a^2*b^2-4*b^4.
```

The final quartic is positive by the exact positivity interval. These are
necessary global support constraints, not a solution of the cover. The next
gate must combine them with one factored source-square condition. M3 remains
closed.

`wl574` combines both source-square conditions. Let

```text
2*Delta=k*h^2
```

with `k` positive squarefree, and use the four positive homogeneous factors
`A,B,C,D`. Then the source squares are exactly equivalent to

```text
A*B=k*U^2,
C*D=k*V^2.
```

For `g_1=gcd(A,B)` and `g_2=gcd(C,D)`, determinant identities give

```text
g_1 | 5*a^4-8*a^2*b^2+4*b^4,
g_2 | a^4+8*a^2*b^2+20*b^4.
```

Removing these gcds gives two complementary squarefree allocations of the
same canonical `k`. This is not yet inconsistent. The next gate must compare
the two allocations through exact relations among `A,B,C,D`; treating either
split independently repeats an exhausted route. M3 remains closed.

`wl575` proves the exact scaled Gaussian rotation between the two pairs. Put

```text
P=a^4+4*b^4,
K=a^4+4*a^2*b^2-4*b^4.
```

Then

```text
R1*C=P*A-2*K*B,
R1*D=2*K*A+P*B,
R2*A=P*C+2*K*D,
R2*B=-2*K*C+P*D,
P^2+4*K^2=R1*R2.
```

For primitive `(a,b)`, `gcd(P,K)=gcd(R1,R2)` is exactly `1` for odd `a` and
`4` for even `a`. Therefore at every odd `q|k`, the rotation is invertible
unless `q` divides exactly one of `R1,R2`; the singular case has the rank-one
relation forced by the norm identity. The next gate must classify the induced
side transport in these three cases. No contradiction or M3 step follows yet.

`wl576` completes the first-order classification. Every odd `p|k` divides
`Delta`, is coprime to `a*b*m*n`, and satisfies

```text
(2/p)=1,
p congruent 1 or 7 mod 8.
```

At regular primes:

```text
p|K => same-side transport A->C, B->D,
p|P => crossed transport A->D, B->C.
```

If `p|R1`, then `p|A` and `p|B` while exactly one of `C,D` vanishes. If
`p|R2`, both `C,D` vanish while exactly one of `A,B` does. The normalized
side in the double-vanishing pair is determined by the larger valuation and
cannot be read modulo `p`. The next gate is this higher-valuation singular
case only; residue-only allocation analysis is exhausted. M3 remains closed.

`wl577` removes all of those singular cases on actual candidates. Since

```text
Delta|K,
```

every odd `p|k` divides `K`. Primitive support gives `p` not dividing `P`, and

```text
P^2+4*K^2=R1*R2
```

then makes both determinants units modulo `p`. Thus every odd prime transports
same-side, and

```text
odd(alpha)=odd(gamma),
odd(beta)=odd(delta_0).
```

No odd crossed or higher-valuation case survives. The factor `2` belongs to
`k` exactly when `m,n` have opposite parity, and it is the sole remaining
allocation comparison. The next gate is this coupled dyadic side only; M3
remains closed.

`wl578` resolves the factor `2`. After dividing `P,K,R1,R2` by their common
factor `e=1` for odd `a` or `e=4` for even `a`, the rotation matrix has odd
diagonal and even off-diagonal entries. Such a matrix preserves the coordinate
with larger `2`-adic valuation. Because `2|k` makes each factor-pair valuation
sum odd, the valuations differ and the side is well defined. Thus `2` also
transports same-side, and

```text
alpha=gamma,
beta=delta_0.
```

The two source squares now use one identical complementary split of `k`.
Allocation analysis is complete. The next gate must attack the coupled square
magnitudes in the exact rotation equations; no new allocation table or M3
step is allowed.

`wl579` eliminates the projective scale from those magnitude equations. Put

```text
lambda=beta/alpha,
z=B/A=lambda*u^2,
w=D/C=lambda*v^2.
```

Then

```text
w=(2*K+P*z)/(P-2*K*z),
lambda*v^2*(P-2*K*lambda*u^2)=2*K+P*lambda*u^2,
0<u^2<P/(2*K*lambda).
```

Moreover

```text
w-z=2*K*(1+z^2)/(P-2*K*z)>0,
v>u.
```

The biquadratic is a smooth genus-one torsor: its four zero/pole branch points
are distinct because `P^2+4*K^2>0`. The projective converse reconstructs the
rotation ratios, but not the original primitive linear forms or gcd
normalizations. The next gate must impose exactly those arithmetic constraints;
unrelated rank diagnostics and M3 remain forbidden.

`wl580` closes the primitive reconstruction question. From
`z=Bbar/Abar`,

```text
tau=[X+2*z*(1-X)]/[X*(z+2)-2],
```

and `X>1,z>0` makes the denominator strictly positive. Hence reduced
`tau=m/n` is unique. With `Delta=m^2+2mn-n^2`, the canonical condition

```text
[lambda]=[k]=[2*Delta]=[2*(tau^2+2*tau-1)]
```

shows that `z/lambda` and `w/lambda` square reconstruct exactly the two
source-square predicates; the converse is supplied by `wl574`-`wl578`.
Therefore the entire allocation/magnitude descent is equivalent to the
`wl570` system once self-consistency is imposed. The exact missing lemma is a
rational-point obstruction for this self-consistent genus-one torsor,
equivalently the generic genus-five cover. No further descent bookkeeping or
M3 step is allowed.

`wl581` starts the permitted direct rational-point route. Multiplying the two
source-square predicates gives the genus-two character quotient

```text
C_tau: Z^2=X*a*b*c*d.
```

Over `Q(i)`, the involution

```text
(X,Z) -> (-4/X, 8*i*Z/X^3)
```

has invariant coordinates

```text
S=X-4/X,
Y=Z*(X-2*i)/X^2,
```

and gives a smooth elliptic quotient. Every exact candidate maps to its
nonzero affine locus with `S in Q`, `S^2+16` a rational square, the positive
quadratic lift `X` itself a rational square, `ell=L(X,tau)` the original odd
prime, and all exact `wl570` intervals. This is only a strict forward
obstruction; infinity and visible two-torsion are always present. The next
gate must analyze this restricted affine image, not unrestricted point
existence, unrelated rank tables, or renewed allocation bookkeeping.

`wl582` proves that even the apparent quadratic-lift restriction is not an
independent obstruction. Write `Y=A+i*B` with `S,A,B in Q`. On every affine
non-two-torsion point, splitting the elliptic equation gives

```text
A^2-B^2=-S*L,
A*B=2*L,
```

and therefore reconstructs

```text
X=-2*A/B,
Z=A*X,
S=X-4/X,
Z^2=X*a*b*c*d.
```

Conversely the `wl581` map returns the same `(X,Z)`. Hence the `S in Q`
nonbranch elliptic locus and the genus-two rational locus are exactly
equivalent, and `S^2+16=(X+4/X)^2` is automatic. The next gate must attack a
condition not absorbed by this equivalence: positive square `X`, one
individual source-square lift, or the prime-parameter condition. Unrestricted
elliptic ranks or points cannot count as progress.

`wl583` isolates the first condition not absorbed by those quotients. Put

```text
T_tau:
U^2=a*b/(2*delta),
V^2=c*d/(2*delta).
```

This is a connected genus-one `(Z/2)^2` cover of the `X`-line. It maps
etale of degree two to the `wl571` product elliptic curve by
`Y=2*delta*U*V`, and every exact candidate maps by `U=q*p,V=s`. Conversely,
a torsor point together with `q^2=X` reconstructs both source squares. Thus
the full generic genus-five cover is exactly

```text
T_tau x_{P^1_X} {q^2=X}.
```

For `tau!=1/2`, `T_tau` is unramified over `X=0,infinity`, so `X` has simple
zeros and poles and is not a square in its function field. The square-`X`
pullback is therefore genuinely connected and independent, unlike the
automatic lift in `wl582`. The next gate must analyze torsor points with
positive square `X` and the exact prime formula, or the etale lift itself;
unrestricted torsor/product-curve ranks or points are insufficient.

`wl584` imposes `ell=L(X,tau)` and proves the pointwise identities

```text
U^2=X*(ell-X),
V^2=ell*X+4,
V^2-U^2=X^2+4.
```

These define a fixed-`ell` genus-one source curve with rational boundary
points at `X=0`. Adjoining `q^2=X` gives an unramified connected genus-one
cover encoding exactly the first two `wl535` squares. The final parameter
equation is

```text
E*tau^2-2*F*tau-E=0,
disc_tau=4*G_ell(X).
```

Thus the active intersection is a square-`X` source point, the final norm
discriminant square with the selected `tau=(F+C)/E`, the exact real interval,
and prime `ell`. Unrestricted source-curve or torsor solubility/rank is
exhausted and cannot count as progress.

`wl585` proves the selected positive norm root adds no extra real condition:
`0<tau<1` is automatic and `tau>rho_ell` is exactly equivalent to
`X>sigma_ell`. For fixed `ell`, adjoining the four squareclasses

```text
X, ell-X, ell*X+4, G_ell(X)
```

gives a smooth degree-sixteen genus-seventeen curve with eight branch points.
The character carrying the product of all four classes is the genus-three
curve

```text
W^2=X*(ell-X)*(ell*X+4)*G_ell(X).
```

Its reciprocal involution has invariant coordinates `S=X-4/X`, `Z=W/X^2`
and the explicit elliptic quotient

```text
Z^2=(ell^2-ell*S-4)
    *(S^2+(16-8*ell)*S+32*ell^2-96*ell+80).
```

The next gate is only the restricted image with positive square `X` and all
individual source/norm lifts. Unrestricted points, torsion, or ranks on this
elliptic curve are insufficient.

The `wl530-wl585` consolidated checkpoint now supersedes the individual logs
as the short handoff. An independent symbolic audit found no defect in the key
identities, converses, denominator branches, exceptional cases, or genus
counts. It also finds no uniform arithmetic tool for the restricted `wl585`
image: imposing square `X` and every individual lift reconstructs the full
genus-seventeen problem. Therefore the elliptic-quotient subroute is

```text
exhausted_without_uniform_arithmetic_obstruction.
```

`wl586` performs the required truth audit and compares three structurally
different globally soluble but not AA+BB-admissible cover families:

```text
pure v: support=v_5|L=1|T=5|d=(5,1,5),
pure u: support=u_7|L=7|T=9|d=(7,7,1),
mixed:  support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85).
```

The read-only quartic review collapses to the existing dyadic branch and
canonical `r`, so the controlling stop rule forbids a `wl588` checkpoint.
Only the pure-`v` family has post-`wl527` model/map data; the other two still
have only `L,T,d` labels. Therefore neither the Gaussian parameter character
nor the restricted elliptic quotient is cross-family ready, and both are
route-dead in their current form.

Do not re-enter `wl535` on this evidence. The generic divisor-parity invariant
does transfer to the pure-`u` and mixed representatives, but it does not imply
that all rational specializations are nonsquare. The selected route is now

```text
none_without_parameterized_family_level_input.
```

Analyzing more fixed double covers, ranks, or point tables is not a uniform
mechanism and must not create another numbered checkpoint. M3 remains closed.

If `wl534` is present, the current handoff is:

```text
wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction_stop
```

`wl534` takes the exact `wl533` one-parameter conic-quartic obstruction and
shrinks it again. Fix an odd prime `ell ≡ 1 (mod 4)` and integers `a,b` with

```text
a^2 + b^2 = ell.
```

Define

```text
D(u) = 1 + u^2
N(u) = b*(1-u^2) + 2*a*u
P(u) = a*(1-u^2) - 2*b*u
S(u) = ell*N(u)^2 + 4*D(u)^2
R(u) = ell*N(u)^4 + 4*N(u)^2*D(u)^2 - 4*ell*D(u)^4
A(u) = -N(u)^4 + (8*ell-12)N(u)^2*D(u)^2 + 4*D(u)^4
B(u) =  N(u)^4 + 4*N(u)^2*D(u)^2 - 4*D(u)^4
T(u) = (A(u)^2 + B(u)^2)/2.
```

`wl534` proves that `P(u)=0` and `N(u)=0` are impossible for rational `u`,
because both quadratic equations have discriminant `4*ell`, and an odd prime
`ell` is not a rational square. So the lower `wl533` positivity branch and the
hidden `Q=(N(u)/D(u))^2 != 0` branch are automatic. It also proves:

```text
C^2 = ell*N(u)^2 + 4*D(u)^2
```

is equivalent to `S(u)` being a rational square,

```text
2*Y^2 = A(u)^2 + B(u)^2
```

is equivalent to `T(u)` being a rational square, and

```text
0 < P(u)^2*C^2 < ell^2*N(u)^2*D(u)^2
```

is equivalent to `R(u) > 0`.

Therefore the only remaining exact obstruction is:

```text
For every odd prime ell congruent to 1 mod 4, fix integers a,b with
a^2+b^2=ell. Then there is no rational u such that

S(u) is a rational square,
R(u) > 0,
T(u) is a rational square.
```

This is still an exact missing proposition, not a uniform exclusion theorem
and not a counterexample. Stop at this one-parameter square-predicate
obstruction. Do not enter M3.

If `wl533` is present, the current handoff is:

```text
wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction_stop
```

`wl533` takes the exact `wl532` `Q`-coordinate obstruction and shrinks it
again inside the already-forced odd-prime class `ell ≡ 1 (mod 4)`. Fix
integers `a,b` with

```text
a^2 + b^2 = ell.
```

Then define

```text
D(u) = 1 + u^2
N(u) = b*(1-u^2) + 2*a*u
P(u) = a*(1-u^2) - 2*b*u.
```

The standard rational-circle parameterization gives

```text
Q(u) = (N(u) / D(u))^2
ell - Q(u) = (P(u) / D(u))^2,
```

so the `Q` and `ell-Q` square conditions are absorbed exactly by one rational
parameter `u`. The remaining exact obstruction is:

```text
There is no rational triple (u,C,Y) such that

C^2 = ell*N(u)^2 + 4*D(u)^2,
0 < P(u)^2*C^2 < ell^2*N(u)^2*D(u)^2,
2*Y^2 = A(u)^2 + B(u)^2,
```

where

```text
A(u) = -N(u)^4 + (8*ell-12)N(u)^2*D(u)^2 + 4*D(u)^4
B(u) =  N(u)^4 + 4*N(u)^2*D(u)^2 - 4*D(u)^4.
```

The last identity is the denominator-cleared form of the `wl532` quartic
square condition:

```text
2*G_ell(q^2)
  = (-q^4 + (8*ell-12)q^2 + 4)^2
    + (q^4 + 4*q^2 - 4)^2.
```

This is still an exact missing proposition, not a uniform exclusion theorem
and not a counterexample. Stop at this one-parameter obstruction. Do not enter
M3.

If `wl532` is present, the current handoff is:

```text
wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction_stop
```

`wl532` shrinks the exact `wl531` `X`-fiber-product proposition further. It
defines

```text
Q = 16 / A_ell(X,z)
```

and proves:

```text
Q is a rational square
ell - Q is a rational square
X(Q) = ((ell - Q)*(ell*Q + 4))/Q
ell*Q + 4 is a rational square
V = U*Q/ell satisfies
V^2 = Q^4 + (16 - 8*ell)Q^3 + (32*ell^2 - 96*ell + 72)Q^2
    + (32*ell - 64)Q + 16.
```

Therefore any candidate point already forces `ell` to be a sum of two rational
squares, so every odd prime `ell ≡ 3 (mod 4)` is excluded exactly. The only
remaining exact obstruction is:

```text
For every odd prime ell congruent to 1 mod 4, there is no rational point (Q,V)
with Q a rational square, ell-Q a rational square, ell*Q+4 a rational square,
0 < ((ell-Q)*(ell*Q+4))/Q < ell^2, and the displayed quartic square identity.
```

This is still an exact missing proposition, not a uniform exclusion theorem
and not a counterexample. Stop at this quartic obstruction. Do not enter M3.

If `wl531` is present, the current handoff is:

```text
wl531_m2_pure_v_ell_exact_x_fiber_product_square_lift_proposition_stop
```

`wl531` resolves the current M2 task only to one exact missing arithmetic
proposition for

```text
support=v_ell|L=1|T=ell|d=(ell,1,ell)
```

with `ell` an odd prime. Starting from the `wl530` quartic and centered-even
map, it rewrites the problem using

```text
X = t^2
```

and the exact source/opposite square quadratics

```text
z^2 = X^2 + (8 - 2*ell^2)*X + (ell^2 + 4)^2
U^2 = X^2 + (6*ell^2 - 16*ell + 8)*X + (5*ell^2 - 8*ell + 4)^2
```

together with the complete-`d` lift square forms

```text
A_ell(X,z) = 2*(X - ell^2 + 4 + z)/ell
B_ell(X,z) = 2*(X - ell^2 - 4 + z) = ell*A_ell(X,z) - 16.
```

It proves that the original M2 question is exactly equivalent to:

```text
For every odd prime ell, there is no rational point (X,z,U) on the displayed
X-fiber-product curve with 0 < X < ell^2, X a rational square, and both
A_ell(X,z), B_ell(X,z) rational squares.
```

It also proves that `X=0` cannot satisfy the square-lift conditions, so the
positivity range is exactly `0 < X < ell^2`. This is an exact missing
proposition, not a uniform exclusion theorem and not a counterexample. Stop at
this proposition. Do not enter M3.

If `wl530` is present, the current handoff is:

```text
wl530_m1_pure_v_ell_symbolic_derivation_stop
```

`wl530` resolves only M1 for the infinite pure family

```text
support=v_ell|L=1|T=ell|d=(ell,1,ell)
```

with `ell` an odd prime. It derives the exact symbolic complete-`d` equations

```text
X - (2*ell^2 - 8) = ell*u_minus_p^2
X - (2*ell^2 + 8) = u_pos_2sqrt_q^2
X + (2*ell^2 + 8) = ell*u_neg_2sqrt_q^2
```

the function-field chart

```text
Q(ell)(r,y)/(y^2 - (ell*r^4 - 8*(ell^2+8)*r^2 + 16*ell^3))
```

with

```text
t = y*(r^2 + 4*ell)/(4*r*(r^2 - 4*ell))
N = (ell+t)/2
M = (ell-t)/2
```

the opposite-side product

```text
(N^2+(ell-1)^2)(M^2+(ell-1)^2)
```

and the square-specialization elliptic family

```text
Y^2 = X^3 + (6*ell^2 - 16*ell + 8)*X^2 + (5*ell^2 - 8*ell + 4)^2*X
```

via the quartic

```text
U^2 = t^4 + (6*ell^2 - 16*ell + 8)*t^2 + (5*ell^2 - 8*ell + 4)^2
```

and the degree-two map `X=t^2`, `Y=tU`.

`wl530` also verifies exact recovery of the `wl528` and `wl529` formulas at
`ell=5`. It does not classify the rational points of the general elliptic
family, does not enter M2, and does not prove a uniform cover-family
obstruction, a theorem-level Selmer upper bound, rank zero, `Sha[2]=0`, or
family exclusion.

If `wl529` is present, the current handoff is:

```text
wl529_v5_l1_t5_square_locus_complete_stop
```

`wl529` keeps the same user-selected prototype from `wl528`. It still touches
only:

```text
support=v_5|L=1|T=5|d=(5,1,5)
```

represented by `AA_A1_B4_v_5_m_tail_refresh_candidate` and
`BB_A4_B1_v_5_m_tail_refresh_candidate` in `wl495`.

`wl528` already reconstructs the function-field chart

```text
Q(r,y)/(y^2 - (5*r^4 - 264*r^2 + 2000))
```

with

```text
t = y*(r^2+20)/(4*r*(r^2-20))
N = (5+t)/2
M = (5-t)/2
```

and proves the opposite-side product `(N^2+16)(M^2+16)` is nonsquare as a
function-field element.

`wl529` closes the remaining pointwise specialization gap for this one family.
It starts from the exact identity

```text
16*(N^2+16)*(M^2+16) = (t^2+39)^2 + 6400
```

so the square-specialization locus becomes the genus-one quartic

```text
U^2 = t^4 + 78*t^2 + 7921
```

with the smooth intersection-of-quadrics model

```text
V*Z = T^2 + 39*Z^2
U^2 = V^2 + 6400*Z^2
```

and a degree-two map to the elliptic quotient

```text
Y^2 = X^3 + 78*X^2 + 7921*X
```

via `X=t^2`, `Y=tU`. This map is used for rational-point classification; it
is not asserted to be a birational equivalence.

The `wl529` script checks this algebra symbolically, then proves

```text
rank(E(Q)) = 0
E(Q)_tors ~= Z/4Z
E(Q) = {O, (0,0), (89,1424), (89,-1424)}.
```

Any rational square specialization would map to `E(Q)` with `X=t^2` a rational
square. The only square `X`-value among finite rational points is `X=0`, so the
affine square-locus rational points are only

```text
(t,U) = (0,89), (0,-89).
```

`wl529` then checks that `t=0` has no rational lift back to the `wl528`
quartic because writing `x=r^2` gives

```text
5*x^2 - 264*x + 2000 = 0
```

with discriminant `2^10*29`, not a rational square.

Therefore the selected prototype has no rational point in the required
nonexceptional positivity domain `|t|<5` where the opposite-side product is a
rational square. This closes the one-family square-locus question and stops.

Divisor parity remains separate:

```text
Divisor parity can prove generic function-field nonsquareness, but by itself it
cannot rule out every rational specialization landing on a square value.
```

This is still not a uniform cover-family theorem, not a theorem-level Selmer
upper bound, not rank zero, not `Sha[2]=0`, and not family exclusion.

Do not advance to another family from `wl529` without a new explicit user
selection.

If `wl528` is present but `wl529` is not present, the current handoff is:

```text
wl528_v5_l1_t5_function_field_prototype_partial
```

`wl528` is the first user-selected prototype after `wl527`. It proves the
opposite-side product is nonsquare in the prototype function field by a checked
smooth nonexceptional rational specialization, but it does not yet close the
pointwise positivity-domain specialization gap.

If `wl527` is present, the current handoff is:

```text
wl527_completed_function_field_proof_data_scope_not_ready
```

`wl527` uses `wl526` as immediate input and enters only the selected
cover-family function-field proof-data scoping gate. It inventories the 15
`wl522` globally soluble but not AA+BB-admissible cover families and asks
whether the current data is ready for a later uniform squareclass proof
attempt.

The answer is no:

```text
ready_cover_family_count = 0
not_ready_cover_family_count = 15
exact_missing_data_class =
  uniform_function_field_model_maps_and_squareclass_certificate
```

The missing data classes are explicit cover-family function-field models,
rational source-side maps, `N,M` as function-field elements, an opposite-side
product squareclass or divisor-parity certificate, and exceptional
specialization / positivity separation. One row,
`support=u_3|L=3|T=4|d=(?,?,?)`, also lacks an explicit `d` vector in the
`wl522` taxonomy row.

`wl527` does not prove the uniform lemma, refute the possible mathematical
lemma, build a function-field engine, execute shell 11, compute new `M_tail`
supports, test new ambient `C_d` solubility, apply `wl491` to a new point,
name a theorem-level Selmer row, select a final obstruction candidate, or
claim theorem-level progress. No next roadmap step is entered here.

If `wl526` is present but `wl527` is not present, the current handoff is:

```text
gather_minimal_function_field_squareclass_proof_data_for_named_cover_families
```

`wl526` uses `wl525` as immediate input and is only a route-choice audit. It
compares exactly four next-route families:

- gather minimal function-field squareclass proof data for the named cover
  families;
- return to finite shell / `M_tail` diagnostics;
- name a theorem-level complete-Selmer local/Hilbert row obligation;
- abandon this obstruction line and select a different candidate.

The selected later gate is the first route: scope the minimum function-field
proof data needed for the named cover families. That means an inventory of
cover-family models, source-side maps, candidate `N,M` function-field
elements, an opposite-side product squareclass or divisor-parity certificate
target, and exceptional specialization / positivity separation.

This selected gate is not entered in `wl526`. No function-field models are
built, no uniform lemma is proved, no complete-Selmer row obligation is named,
and no candidate is selected or abandoned.

If `wl525` is present but `wl526` is not present, the current handoff is:

```text
wl525_completed_no_next_gate_entered
```

`wl525` entered the `wl524` selected gate:

```text
attempt_uniform_cover_family_squareclass_obstruction_lemma
```

It tried to promote the point-level `wl491` opposite-side squareclass
obstruction to a uniform statement over the `wl522` globally soluble but not
AA+BB-admissible cover families. The attempt failed at the statement/proof
input layer:

```text
finite_taxonomy_has_no_uniform_squareclass_certificate
```

The finite 15 cover-family / 29 entry taxonomy records point-level
non-admissibility checks. It does not contain cover-family function-field
models, rational `N,M` maps, divisor parity data, or a specialization argument
showing that the opposite-side product is non-square for every rational point
on each cover family. Therefore the finite taxonomy cannot be promoted to a
uniform theorem from the current inputs.

This does not mathematically refute a possible future uniform lemma. It only
refutes the attempted proof from `wl523` / `wl524` data. No next roadmap step
is entered in `wl525`.

If `wl524` is present but `wl525` is not present, the current handoff is:

```text
attempt_uniform_cover_family_squareclass_obstruction_lemma
```

`wl524` is only a route-choice audit. It uses `wl523` as input, compares the
post-`wl523` options, and selects a later attempt at a new uniform
cover-family squareclass obstruction lemma as the next narrow gate. That gate
is not entered in `wl524`.

The selected later question is whether the opposite-side common-source
product can be proved non-square uniformly on the named globally soluble but
not AA+BB-admissible cover families, without treating finite counts as proof
and without claiming a Selmer upper bound. Returning to finite shell 11
`M_tail` diagnostics is deferred. Proof-level local / Hilbert row work is
deferred until a specific Selmer row obligation is named. Final obstruction
candidate selection is rejected because there is no AA+BB-admissible cover
family, no genuinely deferred cover family, and no active final obstruction
candidate.

If `wl523` is present but `wl524`, `wl525`, `wl526`, and `wl527` are not
present, the current handoff is:

```text
post_wl523_route_choice_not_entered_here
```

`wl523` tried the named common-source square obstruction lemma candidate at the
proof/statement layer. The point-level obstruction is already provable from
the existing `wl491` machinery: after a certified centered-even pullback gives
rational `N,M`, the opposite-side product

```text
AA source: (N^2+B^2)(M^2+B^2)
BB source: (N^2+A^2)(M^2+A^2)
```

being a non-square in `Q*/Q*2` is sufficient to route the point as
`not_admissible`. Sign/positivity failures such as `M_not_positive` are
separate admissibility failures, not squareclass failures.

The stronger cover-family theorem is not proved. The 15 globally soluble but
not AA+BB-admissible cover families from `wl522` are finite taxonomy data; a
uniform claim that every rational point on those cover families fails the
opposite-side squareclass condition would need a new lemma. The next gate, if
chosen, is only a route choice between attempting that new uniform
cover-family squareclass lemma and later returning to the finite-shell route.

If `wl522` is present but `wl523` is not present, the current handoff is:

```text
try_common_source_square_obstruction_lemma_candidate_not_entered_here
```

The next narrow question is whether the recorded opposite-side AA/BB
common-source product-not-square failures can be stated and proved as a
reusable admissibility obstruction lemma:

```text
common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families
```

This lemma candidate has not been proved. No proof-level work was entered in
`wl522`.

## Evidence Snapshot

`wl522` uses `wl521` as the latest state and compresses the `wl491`-`wl521`
ledgers into a stable support/cover taxonomy by classification and failure
mode:

- 43 final candidate-ledger entries.
- 13 support families.
- 22 cover families.
- 5 ambient-globally-not-soluble cover families.
- 15 globally soluble but not AA+BB-admissible cover families.
- 2 processed / duplicate cover families.
- No genuinely deferred cover families.
- No AA+BB-admissible cover families.

The important current classification is:

```text
ambient globally soluble but not AA+BB-admissible
```

For the original `u_3` diagnostic point, the ambient `C_d` point pulls back to
the `AA` quotient with:

```text
N = 4
M = 0
```

but it fails the `BB` common-source closure condition because:

```text
(N^2+B^2)(M^2+B^2) = 17
```

which is not a rational square. This point is therefore neither an obstruction
candidate nor an AA+BB-admissible point.

For the full route history, read:

- `docs/work-logs/archive/522-support-cover-taxonomy-to-lemma-candidate-checkpoint.md`
- `docs/work-logs/523-try-common-source-square-obstruction-lemma-candidate.md`
- `docs/work-logs/524-post-wl523-route-choice-audit.md`
- `docs/work-logs/525-attempt-uniform-cover-family-squareclass-obstruction-lemma.md`
- `docs/work-logs/526-post-wl525-route-choice-audit.md`
- `docs/work-logs/527-function-field-squareclass-proof-data-scope.md`
- `docs/work-logs/528-v5-l1-t5-function-field-prototype.md`
- `docs/work-logs/529-v5-l1-t5-square-locus.md`
- `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl522_support_cover_taxonomy_to_lemma_candidate_checkpoint.py`
- `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl523_try_common_source_square_obstruction_lemma_candidate.py`
- `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl524_post_wl523_route_choice_audit.py`
- `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl525_attempt_uniform_cover_family_squareclass_obstruction_lemma.py`
- `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl526_post_wl525_route_choice_audit.py`
- `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl527_function_field_squareclass_proof_data_scope.py`
- `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl528_v5_l1_t5_function_field_prototype.py`
- `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl529_v5_l1_t5_square_locus.py`
- `tests/test_closure_quotient_rank_zero_aa_bb_wl522_support_cover_taxonomy.py`
- `tests/test_closure_quotient_rank_zero_aa_bb_wl523_common_source_obstruction.py`
- `tests/test_closure_quotient_rank_zero_aa_bb_wl524_post_wl523_route_choice.py`
- `tests/test_closure_quotient_rank_zero_aa_bb_wl525_uniform_cover_family_squareclass_obstruction.py`
- `tests/test_closure_quotient_rank_zero_aa_bb_wl526_post_wl525_route_choice.py`
- `tests/test_closure_quotient_rank_zero_aa_bb_wl527_function_field_squareclass_proof_data.py`
- `tests/test_closure_quotient_rank_zero_aa_bb_wl528_v5_l1_t5_prototype.py`
- `tests/test_closure_quotient_rank_zero_aa_bb_wl529_v5_l1_t5_square_locus.py`
- `docs/work-logs/README.md`

## Do Not Reopen

Unless the user explicitly asks for one of these, do not:

- execute shell 11;
- compute new supports;
- test new ambient `C_d` solubility;
- apply `wl491` to a new point;
- select a final obstruction candidate;
- run broad rank/Selmer diagnostics;
- claim rank zero, a Selmer upper bound, uniform `M_tail` full rank, family
  exclusion, or Harborth global theorem;
- treat the finite count of 15 not-admissible cover families as theorem
  progress.
- treat `wl527` proof-data scoping as a uniform cover-family theorem or as a
  ready proof attempt.
- treat `wl528` as more than one checked single-prototype nonsquare
  certificate.
- treat `wl529` as more than one closed one-family positivity-domain
  square-locus audit.

Do not go back to the old package-`x` / `S~` bridge as if it were a complete
Selmer object. `S~` was a pseudo-container; it is not the theorem-level
`Sel_2(E_L/Q)`.

## Current Route Line

The corrected line is the complete `d`-coordinate route:

```text
complete d-container
  -> local C_d rows
  -> torsion baseline
  -> parameter-dependent M_tail diagnostics
  -> ambient C_d global points
  -> AA+BB common-source admissibility filter (wl491)
  -> support/cover taxonomy (wl522)
  -> point-level common-source square obstruction statement (wl523)
  -> post-wl523 route choice selects uniform cover-family lemma attempt (wl524)
  -> uniform cover-family squareclass obstruction attempt fails from finite taxonomy (wl525)
  -> post-wl525 route choice selects minimal function-field proof-data scoping (wl526)
  -> function-field proof-data scoping finds missing model/map/certificate data (wl527)
  -> one selected v_5 L=1 T=5 function-field nonsquare prototype (wl528)
  -> same prototype square-locus closes in the nonexceptional positivity domain (wl529)
```

`wl529` supplies one closed one-family positivity-domain square-locus audit and
stops. It is not another finite shell computation, not a new point-level
filter run, not a divisor-parity theorem, not the uniform lemma itself, and
not a Selmer-family theorem claim unless a rigorous Selmer upper bound is
actually proved.
