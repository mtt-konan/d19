# wl595 Universal Closure-Product G4 Route Death

## Scope

This checkpoint encodes the accepted G4 decision

```text
precise_g4_universal_closure_product_route_death
```

It imports the accepted `wl594` G0 certificate and records the exact G1-G3
algebra. The conclusion is scoped to the universal closure-product
Kummer/single-split-prime/denominator-place mechanism. It is not a global
AA+BB theorem, a family exclusion, a Selmer or rank theorem, or a claim that
all future relative 2-descent is impossible.

The executable certificate is:

```text
scripts/theory/aa_bb/wl595_universal_closure_product_g4_route_death.py
```

## G0 Input

`wl594` is imported and must be ready with
`accepted_outcome=exact_parameterized_input_ready`. Its exact centered family
is

```text
N=(T+t)/2, M=(T-t)/2,
Q_L(t)=((T+t)^2+4*L^2)((T-t)^2+4*L^2)
      =t^4+(8*L^2-2*T^2)t^2+(T^2+4*L^2)^2,
W^2=Q_A(t)*Q_B(t).
```

The two target branches are retained separately. For `T=A+B`,

```text
Q_A=t^4+2*(A-B)*(3*A+B)*t^2+(5*A^2+2*A*B+B^2)^2
Q_B=t^4-2*(A-B)*(A+3*B)*t^2+(A^2+2*A*B+5*B^2)^2.
```

For `T=|A-B|`, with `A>B>0`,

```text
Q_A=t^4+2*(A+B)*(3*A-B)*t^2+(5*A^2-2*A*B+B^2)^2
Q_B=t^4+2*(A+B)*(3*B-A)*t^2+(A^2-2*A*B+5*B^2)^2.
```

After common scale and `A<->B`, the genuine parameter is `lambda=A/B`.
The plus ray has `T/B=lambda+1`; the minus ray has `T/B=lambda-1` after
`A>B`. The smooth positive domain is `A>0,B>0,T>0,A!=B`.

The degree-eight product cover has genus `3`. With `x=t^2`,

```text
w^2=f_A(x)*f_B(x),
f_L(x)=x^2+(8*L^2-2*T^2)*x+(T^2+4*L^2)^2,
```

is a genus-one quartic. The simultaneous cover

```text
z_A^2=Q_A(t), z_B^2=Q_B(t)
```

has genus `5`.

The complete GEN-CLOSURE quantifier is retained:

```text
For every exact AA+BB candidate with A,B,N1,N2>0,
{N1+N2,abs(N1-N2)} intersects {A+B,abs(A-B)}.
```

Thus all four relations remain in scope:

```text
N1+N2=A+B,
N1+N2=abs(A-B),
abs(N1-N2)=A+B,
abs(N1-N2)=abs(A-B).
```

For either positive sum target, `|t|<T`. For either signed difference target,
both orientations are retained: `N1-N2=c` gives `t=N1+N2>T`, and
`N2-N1=c` gives the swapped representative with the same strict signed
interval. The midpoint `t=0`, endpoints `t=+/-T`, factor-zero roots
`t=-T+/-2*i*L` and `t=T+/-2*i*L`, infinity, and the separate `x=0` cubic
chart boundary are all retained. The converse hierarchy remains strict:

```text
x=t^2 is a nonzero positive rational square in the correct interval;
Q_A(t), Q_B(t) are individual rational squares;
the four original AA/BB factors lift individually.
```

## G1 Natural Class

Set

```text
S=A^2+B^2,
Delta=A^2-B^2,
f_A=x^2+(8*A^2-2*T^2)*x+(T^2+4*A^2)^2,
f_B=x^2+(8*B^2-2*T^2)*x+(T^2+4*B^2)^2.
```

Direct subtraction gives

```text
f_A-f_B=8*Delta*(x+T^2+2*S),
x0=-(T^2+2*S).
```

The general resultant is

```text
Res_x(f_A,f_B)
 =2^8*Delta^2*(T^2+(A-B)^2)*(T^2+(A+B)^2).
```

Specializing to the two closure targets gives

```text
T=A+B:   Res=2^10*Delta^2*S*(A+B)^2,
T=A-B:   Res=2^10*Delta^2*S*(A-B)^2.
```

At the common difference center,

```text
f_A(x0)=4*(T^2+(A-B)^2)*(T^2+(A+B)^2).
```

On either closure branch this is exactly

```text
f_A(x0)=16*S*T^2.
```

After the individual `f_A,f_B` lifts, write `f_A=a^2` and `f_B=b^2`.
Then the natural class is exactly

```text
delta=[f_A]=[f_B]=1.
```

This is an automatic identity on the restricted individual image, not a
nontrivial Kummer obstruction. Removing this redundant product class does
not remove a parameter, a degree of freedom, or the individual/four-factor
lift.

## G2 Four-Factor Split-Prime Audit

Use the four cleared factors

```text
Phi_A_plus  =(T+t)^2+4*A^2,
Phi_A_minus =(T-t)^2+4*A^2,
Phi_B_plus  =(T+t)^2+4*B^2,
Phi_B_minus =(T-t)^2+4*B^2.
```

Their six exact differences are

```text
Phi_A_plus-Phi_A_minus  =4*T*t,
Phi_A_plus-Phi_B_plus   =4*Delta,
Phi_A_plus-Phi_B_minus  =4*(Delta+T*t),
Phi_A_minus-Phi_B_plus  =4*(Delta-T*t),
Phi_A_minus-Phi_B_minus =4*Delta,
Phi_B_plus-Phi_B_minus  =4*T*t.
```

Their six pairwise resultants in `t` are

```text
Res(Phi_A_plus,Phi_A_minus)
  =16*T^2*(T^2+4*A^2),
Res(Phi_A_plus,Phi_B_plus)=16*Delta^2,
Res(Phi_A_plus,Phi_B_minus)
  =16*(T^2+(A-B)^2)*(T^2+(A+B)^2),
Res(Phi_A_minus,Phi_B_plus)
  =16*(T^2+(A-B)^2)*(T^2+(A+B)^2),
Res(Phi_A_minus,Phi_B_minus)=16*Delta^2,
Res(Phi_B_plus,Phi_B_minus)
  =16*T^2*(T^2+4*B^2).
```

The cross collisions are

```text
Phi_A_plus=Phi_B_minus at t=-Delta/T,
Phi_A_minus=Phi_B_plus at t=Delta/T.
```

Their general common value is

```text
((T^2+(A-B)^2)*(T^2+(A+B)^2))/T^2,
```

which is `4*S` for both `T=A+B` and `T=A-B`.

At every odd `p` in a collision stratum, the negative-valuation branch has

```text
t^-2*Phi_(L,+/-)
 =1 +/- 2*T/t+(T^2+4*L^2)/t^2.
```

If `v_p(t)<0`, the tail lies in `1+p*Z_p`; because `p` is odd, Hensel's
lemma makes each normalized factor a square. Hence the four-factor local
character vector admits the all-square value. At `p=5`, the integral branch
is excluded, but this negative-valuation branch survives. This is local
branch feasibility only; no global point is claimed.

## G3 Primitive Denominator Audit

Write the rational coordinate in lowest terms as

```text
t=C/D0, gcd(C,D0)=1,
F_(L,+/-)=(C +/- T*D0)^2+4*L^2*D0^2.
```

For every `L` and either sign,

```text
F_(L,+/-)=C^2 mod D0,
gcd(F_(L,+/-),D0)=gcd(C^2,D0)=1.
```

The six exact differences are

```text
F_A_plus-F_A_minus  =4*T*C*D0,
F_B_plus-F_B_minus  =4*T*C*D0,
F_A_plus-F_B_plus   =4*Delta*D0^2,
F_A_minus-F_B_minus =4*Delta*D0^2,
F_A_plus-F_B_minus  =4*D0*(Delta*D0+T*C),
F_A_minus-F_B_plus  =4*D0*(Delta*D0-T*C).
```

The same-leg products are exactly

```text
F_A_plus*F_A_minus
 =C^4+(8*A^2-2*T^2)*C^2*D0^2+(T^2+4*A^2)^2*D0^4,
F_B_plus*F_B_minus
 =C^4+(8*B^2-2*T^2)*C^2*D0^2+(T^2+4*B^2)^2*D0^4.
```

The all-four product is exactly

```text
F_A_plus*F_A_minus*F_B_plus*F_B_minus
 =D0^8*Q_A(C/D0)*Q_B(C/D0).
```

Because `D0` is a unit at every common prime of two cleared factors, the
primitive condition gives the pairwise bounds

```text
gcd(F_i,F_j) divides Res_t(Phi_i,Phi_j),
```

with the six explicit resultants listed in G2. No denominator prime is
therefore converted into a new factor-support class.

For an odd `q|D0`, put `r=D0/C`. Then `v_q(r)>0` and

```text
F_(L,+/-)/C^2=1 +/- 2*T*r+(T^2+4*L^2)*r^2 in 1+q*Z_q.
```

Every denominator-place factor is a `Q_q` square. At `q=2`, `C` is odd and
`D0` is even, so

```text
F_(L,+/-)=1 mod 8,
C^2=1 mod 8,
F_(L,+/-)/C^2 in 1+8*Z_2,
```

which is a `Q_2` square. Thus denominator places add no support, parity,
splitting, reciprocity, norm, or character restriction.

## G4 Decision

The available local character bits all admit zero: odd collision primes use
the negative-valuation branch, `p=5` retains that branch, denominator places
are principal-unit squares, and the dyadic denominator branch is also a
square. An integral `p=2` branch is not silently claimed soluble; G0-G3 give
no forced nontrivial bit there, so a uniform integral `p=2` exclusion would be
new input rather than a consequence of this route. G1 makes the natural
global product combination tautological after the individual lifts. Real
intervals are archimedean conditions and cannot create a p-adic character.
Midpoint, endpoints, factor-zero, infinity,
primitive/gcd, individual AA/BB, and full four-factor boundaries remain in
scope; none supplies a missing forced parity relation.

Therefore the exact accepted outcome is

```text
accepted_outcome=route_death_certificate
```

for the universal closure-product Kummer/single-split-prime/denominator
mechanism only. This does not claim a global point, Harborth, family
exclusion, Selmer, rank, D2, D5, or M3 result, and it does not say that all
future relative 2-descent is impossible.

The exact input required to reopen is a new parameter-uniform global
relative 2-descent certificate on the full individual four-factor cover,
with a nontrivial divisor/Kummer class and forced local parity across both
`T` branches, `p=2`, denominator places, all boundary charts, real intervals,
and complete AA/BB lifts.

The certificate sets `scoped_objective_complete=True` and
`long_term_object_complete=True` only for the scoped universal
closure-product Kummer/split-prime objective. It sets
`global_problem_complete=False`, with Harborth, family exclusion, Selmer,
rank, D2, D5, and M3 all false.
