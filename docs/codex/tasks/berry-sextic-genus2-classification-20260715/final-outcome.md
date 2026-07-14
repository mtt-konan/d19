# Berry Sextic Genus-2 Final Outcome

## Outcome

`precise_genus2_arithmetic_blocker`

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

## Exact Blocker

Actual reduction at `(1+i)` is unresolved for both curves. The displayed
sextic reduces to `(t+1)^6`, while all three displayed absolute Igusa
invariants are integral. The exact fixed-center radial calculations are valid,
but they do not classify the right `PGL2(O)` factor in a general Cartan
decomposition and therefore do not cover every Bruhat-Tits-tree direction or
center.

The smallest remaining theorem is:

```text
Classify every quotient P1 lattice over K_(1+i), including all
Bruhat-Tits-tree directions and centers after the right PGL2(O_(1+i))
factor, with a finite stopping proof; then construct or obstruct the
corresponding smooth proper generalized genus-2 model for C_1 and C_i,
including every infinity chart.
```

Without that theorem, the exact bad-place set is incomplete and B1 local
solubility cannot be certified. Consequently B2 Jacobian rank/Selmer work, B3
rational-`t` enforcement, and B4 point enumeration are not entered.

## Certified Boundary

This outcome is not an exclusion of the selected sextic and not a point. It
makes no claim about the other Berry sextics, a degree-6 family, the full D19
problem, Jacobian decomposition, torsion, rank, Selmer groups, Chabauty, or a
bounded point search.

Evidence is in `b0-covering-certificate.md`,
`scripts/theory/berry_sextic_b0.py`,
`scripts/theory/berry_sextic_b0_reduction.sage`, and
`tests/test_berry_sextic_b0.py`.
