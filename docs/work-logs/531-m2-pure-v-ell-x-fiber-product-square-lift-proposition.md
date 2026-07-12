# M2 Pure v_ell X-Fiber-Product Square-Lift Proposition

## Question

For the infinite pure family

```text
support=v_ell|L=1|T=ell|d=(ell,1,ell)
```

with `ell` an odd prime, can the M2 question be resolved completely after
handling all of the wl530 square-`X`, positivity, and complete-`d` lift
constraints? Accepted outcomes were:

- a rigorous infinite-subfamily exclusion theorem;
- a strict verified counterexample;
- or one exact unresolved arithmetic proposition, with proof that it is the
  first missing lemma.

This work reaches only the third outcome. It does not prove a uniform
exclusion theorem, does not produce a counterexample, and does not enter M3.

## Input

Immediate checked input:

```text
wl530  M1 symbolic derivation for support=v_ell|L=1|T=ell|d=(ell,1,ell)
```

The touched object layer is still:

```text
pure-v_ell complete-d quartic
-> centered-even t-map
-> square-X and positivity reduction
-> exact complete-d lift constraints
```

not theorem-level Selmer, not rank-zero family theorems, and not the old
package-`x` / `S~` bridge.

## Exact X-Fiber-Product Reduction

From `wl530`, any nonexceptional rational point

```text
(r,y) on y^2 = ell*r^4 - 8*(ell^2+8)*r^2 + 16*ell^3
```

with

```text
t = y*(r^2+4*ell)/(4*r*(r^2-4*ell))
```

has

```text
X = t^2
```

and source-side square identity

```text
z^2 = X^2 + (8 - 2*ell^2)*X + (ell^2 + 4)^2.
```

The opposite-side square condition is exactly

```text
U^2 = X^2 + (6*ell^2 - 16*ell + 8)*X + (5*ell^2 - 8*ell + 4)^2.
```

The complete-`d` lift data can then be written using only `X` and `z`:

```text
A_ell(X,z) = 2*(X - ell^2 + 4 + z)/ell
B_ell(X,z) = 2*(X - ell^2 - 4 + z) = ell*A_ell(X,z) - 16.
```

On an actual quartic point these are exactly

```text
A_ell(X,z) = u_minus_p^2
B_ell(X,z) = u_pos_2sqrt_q^2.
```

The audit proves the exact identity

```text
4*A_ell(X,z)*X = B_ell(X,z)*(A_ell(X,z)+4*ell)
```

modulo the source-side quadratic. Therefore once `X` is a rational square and
`A_ell(X,z), B_ell(X,z)` are rational squares, the remaining `u_neg_2sqrt_q^2`
term is forced automatically.

## Converse Reconstruction

Conversely, suppose rational `X,z,U` satisfy the two quadratics, with

```text
0 < X < ell^2
```

and `X` a rational square, and suppose `A_ell(X,z)` and `B_ell(X,z)` are both
rational squares. Choose rational numbers

```text
t, u_minus_p, u_pos_2sqrt_q
```

with

```text
t^2 = X
u_minus_p^2 = A_ell(X,z)
u_pos_2sqrt_q^2 = B_ell(X,z).
```

All divisions below are legitimate. If `B_ell(X,z)=0`, then
`z=ell^2+4-X`; substituting this into the source quadratic gives
`-16*X=0`, contrary to `X>0`. Thus `u_pos_2sqrt_q != 0`. Similarly,
`A_ell(X,z)=0` would give `z=ell^2-4-X` and hence
`B_ell(X,z)=-16`, impossible because `B_ell(X,z)` is a rational square.
Thus `u_minus_p != 0` as well.

Then define

```text
u_neg_2sqrt_q = 2*t*u_minus_p / u_pos_2sqrt_q.
```

The audited identity above gives

```text
u_neg_2sqrt_q^2 = A_ell(X,z) + 4*ell.
```

Now set

```text
r = u_minus_p + u_neg_2sqrt_q
y = 2*r*u_pos_2sqrt_q.
```

The script checks symbolically that:

- `u_neg_2sqrt_q^2 - u_minus_p^2 = 4*ell`;
- `u_minus_p = (r^2 - 4*ell)/(2*r)`;
- `u_neg_2sqrt_q = (r^2 + 4*ell)/(2*r)`;
- `y^2 = ell*r^4 - 8*(ell^2+8)*r^2 + 16*ell^3`;
- the centered-even map first gives
  `u_pos_2sqrt_q*u_neg_2sqrt_q/(2*u_minus_p)`, and the chosen sign in the
  definition of `u_neg_2sqrt_q` makes this exactly the chosen `t`.

Finally, `r != 0`: otherwise `u_neg_2sqrt_q=-u_minus_p`, contradicting
`u_neg_2sqrt_q^2-u_minus_p^2=4*ell`. Moreover,
`r^2-4*ell=2*r*u_minus_p != 0`. So this reconstruction gives back a
nonexceptional rational quartic point.

Therefore the original M2 question is exactly equivalent to the following one
arithmetic proposition.

## Exact Missing Proposition

For every odd prime `ell`, the affine `X`-fiber-product curve

```text
z^2 = X^2 + (8 - 2*ell^2)*X + (ell^2 + 4)^2
U^2 = X^2 + (6*ell^2 - 16*ell + 8)*X + (5*ell^2 - 8*ell + 4)^2
```

has no rational point `(X,z,U)` such that:

```text
0 < X < ell^2
X is a rational square
A_ell(X,z) is a rational square
B_ell(X,z) is a rational square.
```

This proposition is exact, not heuristic. Proving it would close M2 for the
pure `v_ell` family. Producing one rational point violating it would give a
strict counterexample.

## Why This Is The First Missing Lemma

Everything before this proposition is now exact symbolic bookkeeping:

- `wl530` already provides the complete-`d` quartic, the centered-even map,
  the opposite-side square formula, and the square-`X` elliptic quotient.
- This work eliminates `r,y` in favor of `X,z,U` and proves the converse
  reconstruction exactly.
- The `X=0` branch is already closed:

  ```text
  z = ±(ell^2+4)
  A_ell(0,z) in {16/ell, -4*ell},
  ```

  and neither value is a rational square for an odd prime `ell`.

So no earlier ambiguity remains. The only unresolved step is the simultaneous
rational-point and square-lift claim on this `X`-fiber-product curve.

Two executable examples show why no smaller statement is enough:

- `ell=7`: the opposite-side quotient has the positivity-compatible square
  point `X=4`, `U=195`, but the source quadratic value is `2465`, not a
  rational square.
- `ell=13`: the quartic point `r=6`, `y=32` gives

  ```text
  t = -22/3
  X = 484/9
  z = 1105/9
  A_13(X,z) = 16/9
  B_13(X,z) = 64/9,
  ```

  so the source-side lift conditions hold in the positivity range, but the
  opposite-side quadratic value is `48737065/81`, not a rational square.

Thus:

```text
quotient-only is insufficient;
source-side-lift-only is insufficient;
the combined X-fiber-product square-lift proposition is the first remaining gap.
```

## Certificate

Executable certificate:

```text
scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl531_m2_pure_v_ell_x_fiber_product_square_lift_proposition.py
tests/test_closure_quotient_rank_zero_aa_bb_wl531_m2_pure_v_ell_x_fiber_product_square_lift_proposition.py
```

The audit checks:

- the source-side quadratic identity from the wl530 chart;
- the exact `A_ell(X,z), B_ell(X,z)` formulas;
- the factorization `4*A_ell*X = B_ell*(A_ell+4*ell)`;
- the converse reconstruction identities back to the wl530 quartic;
- the `X=0` exclusion;
- the `ell=7` and `ell=13` boundary examples.

Result artifact:

```text
results/closure_quotient_rank_zero_aa_bb_wl531_m2_pure_v_ell_x_fiber_product_square_lift_proposition.json
```

with:

```text
status = ok
work_log = wl531
object_layer =
  m2_exact_missing_proposition_after_square_x_and_complete_d_lift_reduction
m2_reduced_to_exact_missing_proposition_here = true
exact_x_fiber_product_square_lift_proposition_identified_here = true
t_zero_excluded_from_the_missing_proposition_here = true
uniform_infinite_subfamily_exclusion_proved_here = false
strict_counterexample_found_here = false
advance_to_m3 = false
stop_after_exact_missing_proposition = true
```

## Boundary

This work stops exactly at the verified missing proposition above. It does not
prove the proposition, does not classify the rational points on the fiber
product, does not reopen another support family, does not execute shell 11,
and does not claim theorem-level Selmer progress.
