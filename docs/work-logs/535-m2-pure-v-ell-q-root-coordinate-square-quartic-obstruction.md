# M2 Pure v_ell q-Root Coordinate Square/Quartic Obstruction

## Question

Starting from the exact `wl534` one-parameter square-predicate obstruction for

```text
support=v_ell|L=1|T=ell|d=(ell,1,ell)
```

with `ell` an odd prime congruent to `1 (mod 4)`, can the remaining
proposition be rewritten in a more coordinate-free way without changing the
mathematical content?
Accepted outcomes were:

- a rigorous proof of the remaining proposition;
- a strict counterexample;
- or one coordinate-free exact reformulation of the same arithmetic obstruction.

This work reaches only the third outcome. It does not prove the remaining
obstruction, does not produce a counterexample, and does not enter M3.

## Input

Immediate checked input:

```text
wl534  exact one-parameter square-predicate obstruction
```

The touched object layer is still only:

```text
pure-v_ell M2 exact missing proposition
-> remove the fixed sum-of-two-squares chart from the statement
-> descend from the chart variable u to the direct q-root coordinate
-> replace T(u) square by one explicit q-coordinate quartic equation
-> coordinate-free exact q-root square/quartic reformulation
```

not theorem-level Selmer, not a new support family, not shell 11, and not the
old package-`x` / `S~` bridge.

## Descend To The Direct q-Root Coordinate

Keep the `wl534` setup

```text
D(u) = 1 + u^2
N(u) = b*(1-u^2) + 2*a*u
P(u) = a*(1-u^2) - 2*b*u
```

with fixed integers `a,b` satisfying

```text
a^2 + b^2 = ell.
```

Define the direct circle coordinates

```text
q(u) = N(u) / D(u)
p(u) = P(u) / D(u).
```

Then the standard identity from `wl533` is

```text
q(u)^2 + p(u)^2 = ell.
```

So every rational `u` already gives a rational `q=q(u)` with

```text
ell - q^2 = p(u)^2,
```

which is automatically a rational square.

This removes the need to keep the fixed representation `a^2+b^2=ell` and the
affine chart data `D,N,P` inside the final statement: they are only one chosen
parameterization of the rational circle `p^2+q^2=ell`.

## Translate The Three wl534 Conditions

Set

```text
G_ell(Q)
  = Q^4 + (16-8*ell)Q^3 + (32*ell^2-96*ell+72)Q^2 + (32*ell-64)Q + 16.
```

Then the three `wl534` conditions become direct `q`-coordinate conditions.

First,

```text
S(u) = ell*N(u)^2 + 4*D(u)^2 = D(u)^2*(ell*q(u)^2 + 4),
```

so

```text
S(u) square  <=>  ell*q(u)^2 + 4 square.
```

Second,

```text
R(u) = D(u)^4*(ell*q(u)^4 + 4*q(u)^2 - 4*ell),
```

so

```text
R(u) > 0  <=>  ell*q(u)^4 + 4*q(u)^2 - 4*ell > 0.
```

Third, with

```text
A(u) = -N(u)^4 + (8*ell-12)N(u)^2*D(u)^2 + 4*D(u)^4
B(u) =  N(u)^4 + 4*N(u)^2*D(u)^2 - 4*D(u)^4,
T(u) = (A(u)^2 + B(u)^2)/2,
```

the exact identity is

```text
T(u) = D(u)^8 * G_ell(q(u)^2).
```

Therefore

```text
T(u) square  <=>  G_ell(q(u)^2) square.
```

Equivalently, introducing one explicit curve variable `V`,

```text
T(u) square  <=>  there exists V in Q with V^2 = G_ell(q(u)^2).
```

So the full `wl534` obstruction can be stated directly in the `q`-root
coordinate.

## Converse Reconstruction And Exceptional Branches

Conversely, suppose `q` is rational and

```text
ell - q^2 = p^2
```

for some rational `p`.

Fix any integers `a,b` with `a^2+b^2=ell`. The inverse formulas from `wl533`
remain:

```text
u = (q-b)/(p+a) when p+a != 0,
u = (a-p)/(q+b) when q+b != 0.
```

For an odd prime `ell`, neither `a` nor `b` can vanish, because
`a^2+b^2=ell` would otherwise make `ell` an integer square.

Now split the inverse reconstruction into the only three exceptional cases.

If `p+a=0`, then `p=-a`, hence `q^2=ell-a^2=b^2`. There are two subcases.

- If `q=b`, the point is `(-a,b)`. The first inverse quotient is `0/0`, but
  the second is defined and gives

  ```text
  u = (a-p)/(q+b) = (a-(-a))/(b+b) = a/b.
  ```

  Direct substitution of `u=a/b` into the chart gives

  ```text
  q(a/b)=b,
  p(a/b)=-a.
  ```

- If `q=-b`, the point is the antipode `(-a,-b)`, handled below.

Dually, if `q+b=0`, then `q=-b`, hence `p^2=ell-b^2=a^2`. Again there are two
subcases.

- If `p=a`, the point is `(a,-b)`. The second inverse quotient is `0/0`, but
  the first is defined and gives

  ```text
  u = (q-b)/(p+a) = (-b-b)/(a+a) = -b/a.
  ```

  Direct substitution of `u=-b/a` into the chart gives

  ```text
  q(-b/a)=-b,
  p(-b/a)=a.
  ```

- If `p=-a`, we are again at the antipode `(-a,-b)`.

So the only point not reached directly by one of the two quotients is the
antipode `(-a,-b)`. But that point differs from `(a,-b)` only by the sign of
`p`. Replacing `p` by `-p=a` keeps the same rational `q=-b`, and then the
visible branch above recovers `u=-b/a`. Every `wl535` condition depends only on
`q^2`, namely

```text
ell-q^2,
ell*q^2+4,
ell*q^4+4*q^2-4*ell,
G_ell(q^2),
```

so the sign change in `p` loses no `wl535` state.

Also `D(u)=1+u^2` is never zero over `Q`, and the positivity polynomial

```text
ell*q^4 + 4*q^2 - 4*ell
```

is `-4*ell` at `q=0`, so any positive solution automatically has `q != 0`.
Hence the converse reconstruction has no hidden denominator branch.

Once `u` is recovered, the three displayed identities lift the direct
`q`-coordinate conditions back to the exact `wl534` predicates.

## Exact Coordinate-Free Reformulation

For every odd prime `ell ≡ 1 (mod 4)`, there is no rational pair `(q,V)` such
that

```text
ell - q^2 is a rational square,
ell*q^2 + 4 is a rational square,
ell*q^4 + 4*q^2 - 4*ell > 0,
V^2 = G_ell(q^2).
```

This is exactly equivalent to `wl534`.

It is a coordinate-free exact reformulation of `wl534` because:

- the fixed choice of integers `a,b` with `a^2+b^2=ell` disappears from the
  final proposition;
- the affine circle-chart data `D(u),N(u),P(u),A(u),B(u),S(u),R(u),T(u)` is no
  longer part of the statement;
- the last square predicate is replaced by one explicit `q`-coordinate quartic
  curve equation.

## Boundary Examples

Two exact examples show that the new reformulation is real but still not final.

First, at `ell=5`, choose

```text
q = 1.
```

Then

```text
ell - q^2 = 4,
ell*q^2 + 4 = 9,
ell*q^4 + 4*q^2 - 4*ell = -11,
G_5(q^2) = 481.
```

So both square predicates already hold, but the strict positivity condition
still fails. The new direct `q`-coordinate statement is therefore genuinely
sharper than just keeping the two square predicates.

Second, at `ell=13`, choose

```text
q = 3.
```

Then

```text
ell - q^2 = 4,
ell*q^2 + 4 = 121,
ell*q^4 + 4*q^2 - 4*ell = 1037,
G_13(q^2) = 288385.
```

So the two square predicates and the strict positivity condition all hold, but
the remaining failure is exactly the explicit `q`-coordinate quartic square
condition.

## Certificate

Executable certificate:

```text
scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction.py
tests/test_closure_quotient_rank_zero_aa_bb_wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction.py
```

The audit checks:

- the `wl534` input checkpoint;
- `q(u)^2 + p(u)^2 = ell`;
- `ell - q(u)^2 = p(u)^2`;
- the exact descents
  `S(u)=D(u)^2*(ell*q(u)^2+4)`,
  `R(u)=D(u)^4*(ell*q(u)^4+4*q(u)^2-4*ell)`,
  and `T(u)=D(u)^8*G_ell(q(u)^2)`;
- the two removable inverse-denominator branches `(-a,b)` and `(a,-b)`;
- the antipode/sign branch `(-a,-b) -> (a,-b)`;
- the `ell=5` and `ell=13` boundary examples.

Result artifact:

```text
results/closure_quotient_rank_zero_aa_bb_wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction.json
```

with:

```text
status = ok
ready = true
work_log = wl535
wl534_reduced_to_q_root_coordinate_exact_obstruction_here = true
representation_choice_and_chart_removed_from_statement_here = true
remaining_problem_is_direct_q_root_square_quartic_obstruction = true
```

This work stops exactly at the `q`-root-coordinate obstruction above. It does
not prove the remaining proposition, does not produce a counterexample, does
not claim uniform exclusion, and does not enter M3.
