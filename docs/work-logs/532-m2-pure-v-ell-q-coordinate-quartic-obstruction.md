# M2 Pure v_ell Q-Coordinate Quartic Obstruction

## Question

Starting from the exact `wl531` `X`-fiber-product square-lift proposition for

```text
support=v_ell|L=1|T=ell|d=(ell,1,ell)
```

with `ell` an odd prime, can that remaining proposition be shrunk further
without changing the mathematical content? Accepted outcomes were:

- a rigorous proof of the remaining proposition;
- a strict counterexample;
- or one genuinely smaller exact arithmetic obstruction.

This work reaches only the third outcome. It does not prove the remaining
quartic obstruction, does not produce a counterexample, and does not enter M3.

## Input

Immediate checked input:

```text
wl531  exact X-fiber-product square-lift proposition
```

The touched object layer is still only:

```text
pure-v_ell M2 exact missing proposition
-> exact coordinate shrink
-> smaller arithmetic obstruction
```

not theorem-level Selmer, not a new support family, not shell 11, and not the
old package-`x` / `S~` bridge.

## Exact Q-Coordinate Shrink

`wl531` left the exact proposition:

```text
z^2 = X^2 + (8 - 2*ell^2)*X + (ell^2 + 4)^2
U^2 = X^2 + (6*ell^2 - 16*ell + 8)*X + (5*ell^2 - 8*ell + 4)^2
```

with

```text
0 < X < ell^2
X a rational square
A_ell(X,z) = 2*(X - ell^2 + 4 + z)/ell a rational square
B_ell(X,z) = 2*(X - ell^2 - 4 + z) a rational square.
```

On that locus `wl531` already proved:

```text
B_ell(X,z) = ell*A_ell(X,z) - 16
4*A_ell(X,z)*X = B_ell(X,z)*(A_ell(X,z) + 4*ell)
A_ell(X,z) != 0.
```

Define the new coordinate

```text
Q = 16 / A_ell(X,z).
```

Since `A_ell(X,z)` is a nonzero rational square, `Q` is also a rational
square.

The first `wl531` lift relation immediately becomes

```text
ell - Q = B_ell(X,z) / A_ell(X,z),
```

so `ell-Q` is another rational square.

Using the exact `wl531` factorization

```text
4*A_ell(X,z)*X = B_ell(X,z)*(A_ell(X,z) + 4*ell),
```

and substituting `A_ell(X,z)=16/Q` and `B_ell(X,z)=16*(ell-Q)/Q`, one gets the
exact source-side formula

```text
X(Q) = ((ell - Q)*(ell*Q + 4)) / Q.
```

The zero branch is absent: `ell-Q=B_ell/A_ell`, and `ell-Q=0` would give
`B_ell=0`, which `wl531` converts to `X=0`, contrary to `X>0`. Therefore
`Q` and `ell-Q` are nonzero rational squares. Dividing the square identity for
`X(Q)` by these nonzero square factors proves that `ell*Q+4` is also a rational
square.

Finally write

```text
V = U*Q/ell.
```

Substituting `X(Q)` into the opposite quadratic gives the exact quartic:

```text
V^2 = G_ell(Q)
```

with

```text
G_ell(Q) =
  Q^4 + (16 - 8*ell)Q^3 + (32*ell^2 - 96*ell + 72)Q^2 + (32*ell - 64)Q + 16
```

and also the completed-square form

```text
G_ell(Q) = (Q^2 + (8 - 4*ell)Q - 4)^2 + 16*(ell - 1)^2*Q^2.
```

So every `wl531` point yields an exact `Q`-coordinate point with:

```text
Q a rational square
ell - Q a rational square
ell*Q + 4 a rational square
0 < X(Q) < ell^2
V^2 = G_ell(Q).
```

## Immediate Prime-Class Exclusion

The first two square conditions already force a prime-class restriction.

If

```text
Q = q^2
ell - Q = p^2
```

with `p,q in Q`, then

```text
ell = p^2 + q^2.
```

Clearing denominators gives a primitive integer relation

```text
u^2 + w^2 = ell*v^2.
```

For an odd prime `ell ≡ 3 (mod 4)`, reduce this relation modulo `ell`. If
`w` were nonzero modulo `ell`, then `(u/w)^2=-1`; Euler's criterion says this
is impossible because `-1` is not a square modulo such an `ell`. Thus `ell`
divides both `u` and `w`. Substitution into the integer relation then forces
`ell` to divide `v`, contradicting primitivity. Therefore, for this pure
`v_ell` M2 point-existence proposition:

```text
Any wl531 point must have ell ≡ 1 (mod 4).
```

So the full `ell ≡ 3 (mod 4)` prime class is closed exactly for this M2
point-existence proposition before the last quartic obstruction is even asked.

## Converse Reconstruction

Conversely, suppose `ell` is an odd prime with `ell ≡ 1 (mod 4)` and suppose
there is a rational point `(Q,V)` with:

```text
Q a rational square
ell - Q a rational square
ell*Q + 4 a rational square
0 < X(Q) < ell^2
V^2 = G_ell(Q).
```

Define

```text
A = 16/Q
B = 16*(ell - Q)/Q
X = ((ell - Q)*(ell*Q + 4))/Q
z = ell^2 - 4 + 8*ell/Q - X
U = ell*V/Q.
```

Then the audit checks symbolically that:

```text
A = 2*(X - ell^2 + 4 + z)/ell
B = 2*(X - ell^2 - 4 + z)
z^2 = X^2 + (8 - 2*ell^2)*X + (ell^2 + 4)^2
U^2 = X^2 + (6*ell^2 - 16*ell + 8)*X + (5*ell^2 - 8*ell + 4)^2.
```

Because `X(Q)>0`, none of `Q`, `ell-Q`, or `ell*Q+4` is zero. The formulas
therefore have legitimate denominators; since all three are rational squares,
the reconstructed `A`, `B`, and `X` are rational squares as well. So this
rebuilds a genuine `wl531` point.

Therefore `wl531` is exactly equivalent to the smaller `Q`-coordinate
obstruction below.

## Exact Smaller Obstruction

For every odd prime `ell ≡ 1 (mod 4)`, there is no rational point `(Q,V)` such
that:

```text
Q is a rational square
ell - Q is a rational square
ell*Q + 4 is a rational square
0 < ((ell - Q)*(ell*Q + 4))/Q < ell^2
V^2 = G_ell(Q).
```

This is strictly smaller than `wl531` because:

- the whole `ell ≡ 3 (mod 4)` prime class is excluded exactly for this pure
  `v_ell` M2 point-existence proposition;
- `z`, `A_ell`, and `B_ell` are no longer free variables;
- only one rational square parameter `Q` remains before the last quartic square
  condition is asked.

## Boundary Examples

Two exact examples show the new reduction is real but still not final.

First, `ell=7` is now excluded immediately:

```text
7 ≡ 3 (mod 4),
```

so the new sum-of-two-rational-squares obstruction already kills the entire
prime without opening the quartic.

Second, the `wl531` source-lift example at `ell=13` becomes exactly:

```text
Q = 9
ell - Q = 4
ell*Q + 4 = 121
X(Q) = 484/9
z(Q) = 1105/9
G_13(9) = 288385.
```

The first four conditions hold, but `288385` is not a rational square, so the
remaining failure is exactly the new quartic square condition.

## Certificate

Executable certificate:

```text
scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction.py
tests/test_closure_quotient_rank_zero_aa_bb_wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction.py
```

The audit checks:

- the `Q=16/A_ell(X,z)` coordinate change;
- the identities `ell-Q = B_ell/A_ell` and `X(Q)=((ell-Q)(ell*Q+4))/Q`;
- the quartic identity `V^2=G_ell(Q)` with `V=UQ/ell`;
- the completed-square form of `G_ell(Q)`;
- the full converse reconstruction back to the `wl531` equations;
- the exact `ell ≡ 3 (mod 4)` exclusion statement as the new first obstruction;
- the `ell=7` and `ell=13` boundary examples.

Result artifact:

```text
results/closure_quotient_rank_zero_aa_bb_wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction.json
```

with:

```text
status = ok
work_log = wl532
object_layer =
  m2_strictly_smaller_q_coordinate_quartic_obstruction_after_wl531
wl531_shrunk_to_strictly_smaller_exact_obstruction_here = true
primes_3_mod_4_excluded_here = true
remaining_case_is_q_coordinate_quartic_here = true
uniform_infinite_subfamily_exclusion_proved_here = false
strict_counterexample_found_here = false
advance_to_m3 = false
stop_after_exact_smaller_obstruction = true
```

## Boundary

This work stops exactly at the `Q`-coordinate quartic obstruction above. It
does not solve the remaining `ell ≡ 1 (mod 4)` case, does not produce a
counterexample, does not claim uniform exclusion, and does not enter M3.
