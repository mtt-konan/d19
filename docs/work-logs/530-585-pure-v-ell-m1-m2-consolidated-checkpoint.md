# wl530-wl585 Pure v_ell M1/M2 Consolidated Checkpoint

## Review Verdict

This checkpoint consolidates the 56 steps `wl530` through `wl585` after an
adversarial algebra and route review.

No correctness defect was found in the checked symbolic identities,
forward/converse maps, denominator exclusions, exceptional branches, or genus
counts. The main conclusion is negative but precise:

```text
the elliptic-quotient subroute is exhausted.
```

`wl585` does not reduce the active arithmetic problem. Its unrestricted
elliptic curve forgets the individual square lifts; imposing the stated
restricted image conditions reconstructs the full fixed-`ell` genus-17
problem. Therefore another equivalent model, quotient, rank table, or fixed
prime computation is not accepted as progress.

M2 remains open. There is no uniform exclusion theorem, strict counterexample,
or complete Selmer upper bound here.

## Stable Input And Exact Target

The M1 symbolic family is

```text
support=v_ell|L=1|T=ell|d=(ell,1,ell),
ell an odd prime.
```

After the exact `wl531`-`wl535` forward/converse reductions, the unresolved
M2 proposition is:

```text
For every odd prime ell congruent to 1 mod 4, there is no rational (q,C)
such that

ell-q^2 is a rational square,
ell*q^2+4 is a rational square,
ell*q^4+4*q^2-4*ell>0,
C^2=G_ell(q^2),
```

where

```text
G_ell(X)
 =X^4+(16-8*ell)X^3
  +(32*ell^2-96*ell+72)X^2
  +(32*ell-64)X+16.
```

This statement remains the authoritative proof obligation.

## Independent Algebra Checks

The consolidated executable audit recomputes, rather than merely trusts, the
following cross-stage identities:

```text
G_ell(X)
 =(X^2+(8-4*ell)X-4)^2+16*(ell-1)^2*X^2,

ell=L(X,tau)
 iff E*tau^2-2*F*tau-E=0,

disc_tau=4*(F^2+E^2)=4*G_ell(X),

ell-X
 =-(X*tau+2X-2)*(2X*tau-X-2tau)/(2X*delta),

ell*X+4
 =(X+2tau+4)*(X*tau+4tau-2)/(2delta),

tau>rho_ell iff ell*X^2+4X-4ell>0 iff X>sigma_ell,

G_ell(-4/X)=16*G_ell(X)/X^4.
```

It also recomputes the combined quotient

```text
W^2=X*(ell-X)*(ell*X+4)*G_ell(X),
S=X-4/X,
Z=W/X^2,

Z^2=(ell^2-ell*S-4)
    *(S^2+(16-8*ell)S+32*ell^2-96*ell+80).
```

The quartic and cubic discriminants, source-branch evaluations, and exact
`ell=5` recovery remain nonzero/correct in the stated scope.

## Equivalence And Exception Audit

The reviewed chain has the following status.

| Steps | Status | Converse / exception boundary |
|---|---|---|
| `wl530` | M1 symbolic derivation | Exact `ell=5` recovery; no rational-point theorem |
| `wl531`-`wl535` | Exact equivalences | `X=0`, zero lift factors, circle-chart denominators, antipode, and sign branches handled |
| `wl536`-`wl541` | Strict local consequences and method exhaustion | Partial residue classes only; parameter prime is locally soluble |
| `wl542`-`wl568` | Global descent data and exhausted allocation route | No uniform contradiction; finite classes and affine systems are not proof |
| `wl569`-`wl572` | Exact norm-ratio and cover geometry | `F<0`; selected root unique; `delta=0` excluded; `tau=1/2` excluded by integrality |
| `wl573`-`wl580` | Descent reconstruction | Primitive denominators and squareclasses reconstruct the `wl570` system; no smaller condition remains |
| `wl581`-`wl582` | `Q(i)` quotient and audit | Rational-locus condition reconstructs the genus-2 point; quadratic lift is automatic |
| `wl583`-`wl584` | Source torsor and prime coupling | Unrestricted torsor/source-elliptic solubility forgets the final norm lift |
| `wl585` | Genus-17 cover and rational elliptic quotient | Forward only; restricted lift compatibility restores the full problem |

No old worklog is promoted beyond its stated quantifiers.

## Fixed-Parameter Geometry

For fixed prime `ell`, the four independent squareclasses are

```text
X,
ell-X,
ell*X+4,
G_ell(X).
```

Their smooth projective normalization has degree `16`, eight inertia-two
branch points, and genus `17`. The selected real-root condition adds no new
constraint beyond positivity.

The `wl585` combined elliptic quotient is a necessary image only. To recover a
candidate one must still impose:

```text
S^2+16 square,
the positive quadratic lift X is itself a rational square,
ell-X square,
ell*X+4 square,
G_ell(X) square,
sigma_ell<X<ell,
ell prime congruent to 1 mod 4.
```

These conditions restore the original four squareclasses and the positivity
domain. Hence the quotient has not removed a free parameter or square lift.

## Arithmetic Tool Assessment

No existing tool currently available in this repository gives a uniform
attack on the restricted `wl585` image while preserving all quantifiers.

- Ordinary elliptic rank/torsion computes unrestricted points and forgets the
  four lift conditions.
- Fixed-`ell` 2-descent, covering collections, Chabauty, elliptic Chabauty,
  and Mordell-Weil sieves require curve-specific rank/generator input and do
  not quantify over all primes `ell`.
- Relative or family Chabauty would require a proved uniform rank bound and
  control of sections; neither exists here.
- A Brauer-Manin, Hilbert-symbol, or reciprocity attack would need a new
  uniform invariant surviving the locally soluble and allocation-exhaustion
  results `wl539`-`wl580`; none has been produced.

Therefore the rational elliptic-quotient route is marked:

```text
exhausted_without_uniform_arithmetic_obstruction
```

## Accepted Future Progress

No `wl586+` continuation is authorized merely for another equivalent model or
quotient. A future mathematical checkpoint must provide exactly one of:

1. a direct proof of the `wl535` proposition;
2. a strict rational counterexample satisfying every condition;
3. a genuinely smaller arithmetic proposition, with an explicit accounting
   of which parameter, degree of freedom, or square lift has been removed and
   a proof that the reduction is strict.

If none is available, keep this checkpoint active and do not manufacture a
new numbered worklog.

## Verification

The consolidated audit is:

```text
scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl530_wl585_consolidated_checkpoint.py
tests/test_closure_quotient_rank_zero_aa_bb_wl530_wl585_consolidated_checkpoint.py
```

It fails closed unless both endpoint checkpoints are ready, all independent
symbolic checks pass, and the final status remains M2-open / M3-closed.

## Claim Boundary

This checkpoint does not prove `wl535`, a uniform pure-`v_ell` exclusion,
`dim Sel_2=2`, rank zero, `Sha[2]=0`, a complete Selmer upper bound, or a
Harborth theorem. It does not enter M3 and does not authorize shell 11.
