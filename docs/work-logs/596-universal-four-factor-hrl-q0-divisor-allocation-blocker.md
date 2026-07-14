# wl596 Universal Four-Factor HRL Q0 Divisor-Allocation Blocker

## Scope

This checkpoint starts from the exact realized-class formula

```text
[H_RL(P)]=[epsilon_1*epsilon_2*q_1*q_2*Delta_bar^e],
e=1 iff sigma_1!=sigma_2,
```

and resolves Q0 as far as the current exact equations permit. It derives the
complete primewise allocation system, including shared gcds and `p=2`, then
reduces the remaining global problem to a strict divisor-pair proposition.

The executable certificate is:

```text
scripts/theory/aa_bb/wl596_universal_four_factor_hrl_q0_divisor_allocation.py
```

The accepted outcome is:

```text
accepted_outcome=precise_smaller_arithmetic_blocker
```

This is a real Q4 checkpoint, not a progress narrative. It neither proves a
finite parameter-uniform support group nor constructs a realized
infinite-support family.

## Exact Allocation System

After ordering the positive legs, put

```text
s=Abar+Bbar,
r=Abar-Bbar,
Delta_bar=s*r=Abar^2-Bbar^2>0.
```

For a prime `p|Delta_bar`, write

```text
alpha=v_p(Delta_bar), beta=v_p(s), gamma=v_p(r),
x_i=v_p(q_i), y_i=v_p(d_i).
```

The exact source identity `q_i*d_i=Delta_bar` gives

```text
x_i+y_i=alpha,
q_i=p^x_i*Q_i,
d_i=p^(alpha-x_i)*D_i,
Q_i*D_i=Delta_bar/p^alpha.
```

No coprimality is available. In particular,

```text
v_p(gcd(q_i,d_i))=min(x_i,alpha-x_i).
```

The four cross-gcd valuations are the corresponding minima of
`x_1,alpha-x_1,x_2,alpha-x_2`. Thus shared gcds are part of the allocation
data rather than exceptional errors.

## Source-Quartic Valuations

For `c` equal to `s` or `r`, set `kappa=v_p(c)`. Away from equality,

```text
v_p(q_i^2-c^2)=2*min(x_i,kappa).
```

When `x_i=kappa`, the right replacement is the exact cancellation term

```text
2*kappa
 + v_p(q_i/p^kappa-c/p^kappa)
 + v_p(q_i/p^kappa+c/p^kappa).
```

An infinite cancellation is exactly a source-quartic factor zero
`q_i=|c|`, hence `U_i=0`; this is handled as a boundary rather than assigned a
finite valuation. The row `q_i=s` is the positive endpoint, while `q_i=r` is
the sign-flipped source boundary and is removed by the positive-source
condition. Both are distinct from a four-cover radical-zero chart.

For every finite nonzero source point,

```text
2*v_p(U_i)
 = v_p(q_i^2-s^2)+v_p(q_i^2-r^2)
   -2*x_i-v_p(4).
```

If `beta!=gamma`, put `m=min(beta,gamma)` and `M=max(beta,gamma)`. Away from
the equality/cancellation rows, this gives

```text
odd p:
  x_i<m       -> v_p(U_i)=x_i
  m<x_i<M     -> v_p(U_i)=m
  x_i>M       -> v_p(U_i)=alpha-x_i

p=2:
  x_i<m       -> v_2(U_i)=x_i-1
  m<x_i<M     -> v_2(U_i)=m-1
  x_i>M       -> v_2(U_i)=alpha-x_i-1.
```

At `x_i=m` or `M`, the displayed value receives half of the exact even
cancellation valuation. If `beta=gamma=k`, the two outer branches become
`x_i` and `2*k-x_i` for odd `p`, and one less at `p=2`; the center retains the
sum of both cancellation valuations.

## Dyadic Correction

The parity identities

```text
q_i+d_i=2*abar_i,
q_i-d_i=2*bbar_i
```

show that `q_i,d_i` have the same parity. Hence `2|Delta_bar` forces both to
be even, so `alpha>=2` and `1<=x_i<=alpha-1`.

There is a further dyadic restriction that a valuation-only three-segment
table would miss. If

```text
beta<x_i<gamma
```

or the reversed interval, the unit part of

```text
(q_i^2-s^2)*(q_i^2-r^2)/(4*q_i^2)
```

is `3` or `7 mod 8`, never a square unit. Therefore the dyadic middle branch
has no `Q_2` source point. Equality rows retain their exact unit cancellation;
they are not discarded.

## Closure Coupling

All closure choices have the normalized form

```text
epsilon_1*p^u_1*V_1+epsilon_2*p^u_2*V_2=p^tau*W,
```

where the unit signs encode the sum branch and both ordered difference
branches, and

```text
tau=beta for T=A+B=s,
tau=gamma for physical T=|A-B|=r.
```

If `u_1!=u_2`, the lower valuation equals `tau`. If `u_1=u_2`, the exact unit
sum or difference must have valuation `tau-u_1`. At `p=2`, equal odd units
always cancel at least once. Squaring this equation adds no independent
condition.

## Strongest Parity Consequences

At every finite non-boundary point,

```text
v_p(q_1*q_2)=x_1+x_2 mod 2.
```

When `beta=gamma=k`, equal source valuations pair `x` only with `x` or
`2*k-x`. Closure therefore gives

```text
x_1+x_2 in {2*x,2*k,4*k-2*x},
```

so the realized bit is always zero. The midpoint also has `q_1=q_2` and hence
zero bit.

For odd `p` with `beta!=gamma`, the interval between `beta` and `gamma` has
constant source valuation while `x_i` can change parity. Thus valuation data
alone does not determine the bit. Exact closure units decide realizability.
This non-forcing statement has an exact normalized local witness over `Q_7`:

```text
z^2=51,
rho^2=2499/50,
s=1,
r=rho,
F(z)=F(rho/z)=1/4.
```

Taking `U_1=U_2=1/2` gives the sum closure `U_1+U_2=s`. The allocation pairs
`(z,z)` and `(z,rho/z)` have parity bits `0` and `1`, respectively. Hensel
applies because the relevant unit residues are nonzero squares modulo `7`.
This is a `Q_7` valuation/source witness, not a global integral AA/BB family.

For `p=2`, the middle interval is absent. If `alpha=beta+gamma` is even, every
valuation-compatible low/high pairing has even `x_1+x_2`. If `alpha` is odd,
the remaining bit still depends on the exact dyadic square-unit and closure
cancellation equations. No detached dyadic table is authorized.

Across different primes the bits are linked by the same global divisors
`q_1,q_2` and the same closure equation. They are not independent formal
twist coordinates.

## Strict Reduced Proposition

The variables `d_i,abar_i,bbar_i,U_i` can be removed as independent choices.
For primitive integers `Abar>Bbar>0`, define `s,r,Delta_bar` as above and

```text
F(q)=((q^2-s^2)*(q^2-r^2))/(4*q^2).
```

The remaining exact problem is to classify positive divisor pairs
`q_1,q_2|Delta_bar` satisfying, for each `i`,

```text
d_i=Delta_bar/q_i>0,
q_i congruent d_i mod 2,
q_i>=s,
F(q_i) is a nonnegative integer square,
```

and one member of the closure union

```text
U_1+U_2=s,  U_1+U_2=r,
U_1-U_2=s,  U_2-U_1=s,
U_1-U_2=r,  U_2-U_1=r,
```

where `U_i=sqrt(F(q_i))`. Then determine `sqf(q_1*q_2)`.

The converse is exact. Set

```text
abar_i=(q_i+d_i)/2,
bbar_i=(q_i-d_i)/2.
```

The parity and positivity conditions make these positive integers, and direct
algebra gives

```text
abar_i^2=U_i^2+Abar^2,
bbar_i^2=U_i^2+Bbar^2.
```

The closure union reconstructs both physical `T` branches and both ordered
difference directions. Dividing by the recorded primitive common scale
recovers the rational AA/BB point.

This removes two independent `d_i`, four independent source-root variables,
two independent source-square variables, the squareclass contribution of the
common denominator, and arbitrary formal twists.

## Retained Boundaries

The finite divisor classification retains midpoint, endpoints, and collision
fibers `t=+/-Delta/T`. Sum and signed-difference real intervals remain
separate. Factor-zero and infinity charts are projective boundary obligations
and are retained outside the finite divisor-pair parameterization. All four
radical signs remain in the full realized-class formula.

## Q4 Decision

The corrected Q0 system proves neither a fixed parameter-uniform subgroup nor
a valid exact AA/BB family with unbounded support. The missing input is a new
global invariant controlling the closure-compatible divisor pairs across all
prime factors of `Delta_bar`. Primewise valuations, shared gcds, the dyadic
unit restriction, source quartics, and closure valuations do not supply that
invariant.

Therefore the final scoped decision is:

```text
precise_smaller_arithmetic_blocker
```

Reopening requires an argument on the strict divisor-pair proposition above,
not another local-prime table, formal twist family, quotient rewrite, or fixed
sample.

## No-Claim Boundary

This checkpoint proves no finite parameter-uniform `H_RL` obstruction, no
realized infinite-support family, no family exclusion, Selmer/rank/Sha result,
Harborth theorem, D2, D5, or M3 statement. It does not modify `wl587`-`wl595`
or either completed Picard audit.
