# M2 Pure v_ell One-Parameter Square-Predicate Obstruction

## Question

Starting from the exact `wl533` one-parameter conic-quartic obstruction for

```text
support=v_ell|L=1|T=ell|d=(ell,1,ell)
```

with `ell` an odd prime congruent to `1 (mod 4)`, can the remaining
proposition be shrunk again without changing the mathematical content?
Accepted outcomes were:

- a rigorous proof of the remaining proposition;
- a strict counterexample;
- or one genuinely smaller exact arithmetic obstruction.

This work reaches only the third outcome. It does not prove the remaining
obstruction, does not produce a counterexample, and does not enter M3.

## Input

Immediate checked input:

```text
wl533  exact one-parameter conic-quartic obstruction
```

The touched object layer is still only:

```text
pure-v_ell M2 exact missing proposition
-> one rational parameter u
-> eliminate automatic zero branches
-> remove auxiliary square-root variables C,Y
-> smaller one-parameter square-predicate obstruction
```

not theorem-level Selmer, not a new support family, not shell 11, and not the
old package-`x` / `S~` bridge.

## Zero Branches Are Automatic

Keep the `wl533` definitions

```text
D(u) = 1 + u^2
N(u) = b*(1-u^2) + 2*a*u
P(u) = a*(1-u^2) - 2*b*u
```

with fixed integers `a,b` satisfying

```text
a^2 + b^2 = ell.
```

The two possible zero branches from `wl533` are actually absent for every
rational `u`.

Indeed `P(u)=0` is the quadratic

```text
a*u^2 + 2*b*u - a = 0
```

and `N(u)=0` is the quadratic

```text
b*u^2 - 2*a*u - b = 0.
```

Both have discriminant

```text
4*(a^2+b^2) = 4*ell.
```

Because `ell` is an odd prime, it is not a rational square, so neither
quadratic has a rational root. Therefore:

```text
For every rational u, P(u) != 0 and N(u) != 0.
```

So the old lower positivity branch

```text
0 < P(u)^2*C^2
```

is automatic as soon as `C^2 = ell*N(u)^2 + 4*D(u)^2` holds, and the hidden
`Q=(N(u)/D(u))^2 != 0` branch is automatic as well.

## Eliminate The Auxiliary Square-Root Variables

Define three `u`-only rational functions:

```text
S(u) = ell*N(u)^2 + 4*D(u)^2
R(u) = ell*N(u)^4 + 4*N(u)^2*D(u)^2 - 4*ell*D(u)^4
T(u) = (A(u)^2 + B(u)^2) / 2
```

where

```text
A(u) = -N(u)^4 + (8*ell-12)N(u)^2*D(u)^2 + 4*D(u)^4
B(u) =  N(u)^4 + 4*N(u)^2*D(u)^2 - 4*D(u)^4.
```

Then the two square-root variables in `wl533` are purely existential:

- `C^2 = S(u)` is equivalent to saying `S(u)` is a rational square.
- `2*Y^2 = A(u)^2 + B(u)^2` is equivalent to saying `T(u)` is a rational
  square.

No sign branch survives in either step. Also

```text
A(u) + B(u) = 8*(ell-1)*N(u)^2*D(u)^2,
```

so `T(u)` is automatically positive because `ell>1`, `D(u)>0`, and `N(u)!=0`
for every rational `u`.

## The Upper Positivity Range Collapses To One Quartic Inequality

`wl533` already has

```text
P(u)^2 + N(u)^2 = ell*D(u)^2.
```

Substitute this together with `C^2 = S(u)` into the upper range condition:

```text
P(u)^2*C^2 < ell^2*N(u)^2*D(u)^2.
```

The left-hand difference simplifies exactly to

```text
ell^2*N(u)^2*D(u)^2 - P(u)^2*S(u) = R(u).
```

So, once `u` is rational, the entire `wl533` strict inequality becomes exactly

```text
R(u) > 0.
```

Equivalently, with `Q(u)=(N(u)/D(u))^2`,

```text
R(u) = D(u)^4 * (ell*Q(u)^2 + 4*Q(u) - 4*ell),
```

so the last surviving range restriction is a single quartic positivity test in
the one parameter `u`.

## Exact Smaller Obstruction

For every odd prime `ell ≡ 1 (mod 4)`, fix integers `a,b` with
`a^2+b^2=ell`. Define `D(u), N(u), A(u), B(u), S(u), R(u), T(u)` as above.

Then the exact `wl533` proposition is equivalent to:

```text
There is no rational u such that

S(u) is a rational square,
R(u) > 0,
T(u) is a rational square.
```

This is strictly smaller than `wl533` because:

- the auxiliary square-root variables `C` and `Y` are gone;
- the lower positivity branch and the hidden `Q != 0` branch are automatic for
  rational `u`;
- only one rational parameter survives, together with two square predicates and
  one quartic inequality.

## Boundary Examples

Two exact examples show the new shrink is real but still not final.

First, at `ell=5`, choose

```text
a=1, b=2, u=0.
```

Then

```text
S(0) = 24
R(0) = 76
T(0) = 5392,
```

so the first failure is already the new square predicate `S(0)` not square.

Second, at `ell=13`, choose

```text
a=2, b=3, u=0.
```

Then

```text
S(0) = 121
R(0) = 1037
T(0) = 288385,
```

so the conic-quartic part and the strict range both hold, but the remaining
failure is exactly the new square predicate `T(0)` not square.

## Certificate

Executable certificate:

```text
scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction.py
tests/test_closure_quotient_rank_zero_aa_bb_wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction.py
```

The audit checks:

- the `wl533` input checkpoint;
- the `P(u)^2 + N(u)^2 = ell*D(u)^2` identity;
- the discriminant `4*ell` for both `P(u)` and `N(u)`;
- the exact collapse of the upper positivity range to `R(u) > 0`;
- the exact elimination of `C` and `Y` in favor of the square predicates
  `S(u)` and `T(u)`;
- the positivity identity `A(u)+B(u)=8*(ell-1)*N(u)^2*D(u)^2`;
- the `ell=5` and `ell=13` boundary examples.

Result artifact:

```text
results/closure_quotient_rank_zero_aa_bb_wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction.json
```

with:

```text
status = ok
ready = true
work_log = wl534
wl533_reduced_to_one_parameter_square_predicate_obstruction_here = true
auxiliary_C_and_Y_variables_eliminated_here = true
lower_positivity_and_zero_branches_automatic_here = true
```
