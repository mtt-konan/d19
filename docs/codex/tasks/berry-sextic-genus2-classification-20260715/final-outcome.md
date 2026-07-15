# Berry Sextic Genus-2 Final Outcome

## Outcome

`post_b0_feasibility_audit`

The earlier `precise_genus2_arithmetic_blocker` route judgment is withdrawn;
the remaining C_1 arithmetic is open, but it is not certified as a blocker.

The selected Berry degree-6 pilot is reduced exactly to

```text
C_1: v^2=g6(t),
C_i: i*v^2=g6(t),
t in P^1(Q),
```

with complete projective models, maps and converse to the Berry genus-5
pullback, infinity points, node fibers, factor-zero fibers, degenerate charts,
and the currently certified trivial rational-parameter ledger.

Both curves have good reduction outside

```text
{(1+i), (94*i-169)}.
```

At `(94*i-169)`, both curves have actual bad reduction: the absolute Kohel
Igusa invariant

```text
j1=(23671901*i+580427774)/37397
```

has valuation `-1`. This is intrinsic and is unchanged by the `i`-twist.

## Post-B0 Feasibility Decision

The prior route judgment is withdrawn: a complete stable-model classification at
`(1+i)` is not a prerequisite for B1/B2. The committed fixed-center B0
calculation remains unchanged as a historical B0 input; it is no longer the
reason to stop arithmetic work.

The post-B0 audit in `post-b0-feasibility-audit.md` proves directly that

```text
C_i(K_(1+i)) = empty set,
J_1(K)_tors = 0,
J_i(K)_tors = 0.
```

It also gives the conservative finite support
`{(1+i),(94*i-169),(-94*i-169)}`. The installed Sage toolchain has no exact
genus-2 Jacobian 2-Selmer/local-Kummer route. The public Magma V2.29-8
Calculator exposes `TwoSelmerGroup` for a number-field `JacHyp`, but the exact
selected call exceeds its 60-second limit. No Selmer or rank conclusion is
claimed, and no arithmetic blocker is promoted because the observed failure
is a service timeout, not a dyadic local-image obstruction.

## Certified Boundary

This outcome is not an exclusion of the selected sextic and not a point. It
makes no claim about the other Berry sextics, a degree-6 family, the full D19
problem, Jacobian decomposition, rank, Selmer groups, Chabauty, or a bounded
point search. The trivial Jacobian torsion result above is the one arithmetic
claim made by this post-B0 audit.

Evidence is in `b0-covering-certificate.md`, `post-b0-feasibility-audit.md`,
`scripts/theory/berry_sextic_b0.py`,
`scripts/theory/berry_sextic_b0_reduction.sage`, and
`scripts/theory/berry_sextic_post_b0.py`,
`scripts/theory/berry_sextic_post_b0.sage`,
`scripts/theory/berry_sextic_magma_capabilities.m`,
`scripts/theory/berry_sextic_magma_two_selmer.m`,
`scripts/utility/magma_calculator.py`,
`tests/test_berry_sextic_b0.py`,
`tests/test_berry_sextic_post_b0.py`, and
`tests/test_magma_calculator.py`.
