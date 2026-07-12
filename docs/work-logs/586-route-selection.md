# Cross-Family Truth Audit And Pure-v_ell Route Death

## Question

After the consolidated `wl530`-`wl585` audit, should work re-enter the exact
`wl535` pure-`v_ell` proposition, or does the evidence require a cross-family
route switch?

This checkpoint accepts only a route-death certificate or an invariant that
survives comparison across cover families. It does not count another model,
quotient, character refinement, fixed-`ell` table, or finite no-point search
as progress.

## Truth Audit

The current facts are:

1. `wl585` gives the full fixed-`ell` degree-16 genus-17 cover. Its elliptic
   quotient is lower genus, but the restricted image must restore `X` square,
   positivity, and the three individual square lifts. It is not a smaller
   arithmetic proposition.
2. The proposed quadratic parameter character is automatic after
   `Fh+i*Eh=r*(a+i*b)^2`, because `W+Fh` is `2*r*a^2` or `-2*r*b^2` and every
   prime in canonical `r` divides `ell-1`.
3. The quartic refinement was reviewed read-only. Its normalized value is

   ```text
   ell congruent to 1 mod 8: +1,
   ell congruent to 5 mod 8 and r congruent to 1 mod 8: +1,
   ell congruent to 5 mod 8 and r congruent to 7 mod 8: -1.
   ```

   Thus it depends only on the existing dyadic branch and canonical `r`.
   Under the controlling stop rule it must not become `wl588`; no `wl588`
   checkpoint is created.

This kills only characters derived from the same Gaussian factors. It is not
a theorem that all future global invariants are impossible.

## Three Representative Families

The comparison uses three `wl522` globally soluble but not AA+BB-admissible
cover families, each with both AA and BB point-level failures:

| role | cover family | why representative |
|---|---|---|
| pure `v` | `support=v_5|L=1|T=5|d=(5,1,5)` | only family with a post-`wl527` explicit prototype and exact lift chain |
| pure `u` | `support=u_7|L=7|T=9|d=(7,7,1)` | changes the support orientation while retaining a pure support |
| mixed | `support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85)` | contains all three support types and has no trivial `d` coordinate |

`wl527` has only `L,T,d` labels for all three. Later work supplies a model and
maps only for the pure-`v` representative. The `wl505` complete-`d` equations
nevertheless suffice to recover the generic centered-even function and test
its squareclass on the pure-`u` and mixed fixed covers; no new model checkpoint
is needed.

## Generic Cross-Family Certificate

On either AA source cover, use the same function

```text
t=Y/(2*(X+p)),
N=(A+B+t)/2,
M=A+B-N,
P_op=(N^2+B^2)(M^2+B^2).
```

At the exact smooth nonexceptional `wl505` points:

```text
pure u_7:
  t=69/4, N=105/8, M=-33/8,
  P_op=15172945/4096, not a rational square;

mixed u_3+v_5+w_17:
  t=17, N=27/2, M=-7/2,
  P_op=226625/16, not a rational square.
```

Over the `u_minus_p` line, the other two coordinates adjoin square roots of
two quadratic polynomials with simple, disjoint zero sets. Hence each cover is
a geometrically integral biquadratic cover. The two affine equations have
Jacobian rank two at both displayed points, and the denominator of `t` is
nonzero. If `P_op` were a square in either function field, its square root
would be a unit in the smooth local ring and would specialize to a rational
square. The displayed nonsquare values therefore prove that the same `P_op`
definition is a nontrivial function-field squareclass on both covers.

This is a generic invariant, not a uniform rational-point obstruction. A
nonsquare function can take square values at rational points. Classifying
those values is exactly the rational-point problem on the new double cover
`R^2=P_op`; the specialization certificate removes no parameter or square
lift.

## Invariant Feasibility

| tool | pure `v` | pure `u` | mixed | verdict |
|---|---|---|---|---|
| Gaussian parameter characters | automatic | no input | no input | route dead |
| restricted elliptic image | restores all lifts | no input | no input | current quotient route dead |
| opposite-side divisor parity | nonsquare prototype exists | generic nonsquare proved | generic nonsquare proved | transfers generically, not pointwise |
| point-level common-source nonsquare | observed | observed | observed | finite signal, not a uniform invariant |

There is consequently no evidence-based reason to re-enter `wl535`. The
divisor-parity squareclass does survive on two structurally different covers,
but only generically. Turning it into an exclusion would require a separate
square-specialization analysis for each fixed cover, recreating the same lift
problem rather than yielding a parameterized uniform mechanism.

## Route-Death Certificate

The following routes are frozen:

```text
pure-v_ell equivalent models and quotients,
pure-v_ell parameter characters determined by r,a,b,g,alpha,beta,
representative-only generic divisor parity as a uniform exclusion,
unrestricted fixed-ell rank/torsion calculations.
```

This is the accepted result of `wl586`: a route-death certificate, not a proof
of `wl535` and not a counterexample.

## Selected Cross-Family Gate

No next route is entered from the current inputs:

```text
none_without_parameterized_family_level_input
```

A future reopening would require a parameterized family-level input that
relates at least two cover families and controls square specializations
uniformly. Two more fixed double covers, their ranks, or their rational-point
tables would not meet that gate.

## Boundary

No new support is computed, shell 11 is not executed, no new ambient
solubility is tested, M3 is not entered, and no Selmer, rank-zero, Sha, family
exclusion, or uniform AA+BB theorem is claimed.
