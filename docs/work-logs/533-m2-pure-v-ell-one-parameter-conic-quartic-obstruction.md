# M2 Pure v_ell One-Parameter Conic-Quartic Obstruction

## Question

Starting from the exact `wl532` `Q`-coordinate quartic obstruction for

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
wl532  exact Q-coordinate quartic obstruction
```

The touched object layer is still only:

```text
pure-v_ell M2 exact missing proposition
-> prime-class 1 mod 4 only
-> one-parameter reduction of the Q and ell-Q square constraints
-> smaller conic-quartic obstruction
```

not theorem-level Selmer, not a new support family, not shell 11, and not the
old package-`x` / `S~` bridge.

## Exact One-Parameter Reduction

Because `wl532` already proved that any candidate prime must satisfy
`ell ≡ 1 (mod 4)`, fix integers `a,b` with

```text
a^2 + b^2 = ell.
```

For a rational parameter `u`, define

```text
D(u) = 1 + u^2
N(u) = b*(1-u^2) + 2*a*u
P(u) = a*(1-u^2) - 2*b*u
q(u) = N(u) / D(u)
p(u) = P(u) / D(u).
```

The audit checks symbolically that

```text
q(u)^2 + p(u)^2 = ell.
```

So the two `wl532` square conditions

```text
Q is a rational square
ell - Q is a rational square
```

are absorbed exactly by

```text
Q(u) = q(u)^2 = (N(u) / D(u))^2.
```

For a circle point other than the antipode, the inverse is covered by the two
formulas:

```text
u = (q-b)/(p+a) when p+a != 0,
u = (a-p)/(q+b) when q+b != 0.
```

Indeed, `p(u)+a=2*(a-b*u)/D(u)` and
`q(u)+b=2*(b+a*u)/D(u)`. The first denominator vanishes only at `(-a,b)`,
where the second is `2*b`; the second vanishes only at `(a,-b)`, where the
first is `2*a`. Thus their apparent `0/0` forms are removable by the alternate
formula. The affine parameterization misses only `(-a,-b)`. That point does
not lose any `wl532` state: it has the same `Q=q^2=b^2` as the visible
basepoint `(a,b)` at `u=0`, and every `wl532` condition depends on `Q` and
`V`, not on the sign pair `(p,q)`.

## Remaining ell*Q+4 Square And Positivity

Write `c^2 = ell*Q + 4`. Under `Q=Q(u)`, this clears to one quartic:

```text
C^2 = ell*N(u)^2 + 4*D(u)^2
```

with

```text
c = C / D(u).
```

The right-hand side is strictly positive, so `C` is automatically nonzero.

The `wl532` positivity quantity

```text
X(Q) = ((ell-Q)*(ell*Q+4)) / Q
```

becomes

```text
X(u) = P(u)^2 * C^2 / (N(u)^2 * D(u)^2).
```

Therefore the exact range

```text
0 < X(Q) < ell^2
```

forces `N(u) != 0`, because its right side would otherwise vanish. Thus
`Q=(N(u)/D(u))^2 != 0`, and the range is equivalent to the
denominator-cleared inequality

```text
0 < P(u)^2 * C^2 < ell^2 * N(u)^2 * D(u)^2.
```

So after this step, the only remaining independent square condition from
`wl532` is the single quartic square `C^2 = ell*N(u)^2 + 4*D(u)^2`.

## The Quartic V-Condition Simplifies Further

Set `Q=q^2`. Then the `wl532` quartic polynomial satisfies the exact identity

```text
2*G_ell(q^2)
  = (-q^4 + (8*ell-12)q^2 + 4)^2
    + (q^4 + 4*q^2 - 4)^2.
```

This uses only the `Q=q^2` square substitution; the extra
`ell*Q+4 = c^2` variable disappears completely from the last square condition.

After substituting `q=q(u)=N(u)/D(u)` and clearing denominators by

```text
Y = V * D(u)^4,
```

define

```text
A(u) = -N(u)^4 + (8*ell-12)N(u)^2*D(u)^2 + 4*D(u)^4
B(u) =  N(u)^4 + 4*N(u)^2*D(u)^2 - 4*D(u)^4.
```

Then the exact `wl532` quartic condition

```text
V^2 = G_ell(Q)
```

is equivalent to one denominator-cleared conic-type square identity:

```text
2*Y^2 = A(u)^2 + B(u)^2.
```

So the last square condition no longer depends on the `C`-quartic at all.

## Exact Smaller Obstruction

For every odd prime `ell ≡ 1 (mod 4)`, fix integers `a,b` with
`a^2+b^2=ell`. Define `D(u), N(u), P(u), A(u), B(u)` as above.

Then the exact `wl532` proposition is equivalent to:

```text
There is no rational triple (u,C,Y) such that

C^2 = ell*N(u)^2 + 4*D(u)^2,
0 < P(u)^2*C^2 < ell^2*N(u)^2*D(u)^2,
2*Y^2 = A(u)^2 + B(u)^2.
```

This is strictly smaller than `wl532` because:

- `Q` is no longer a free variable;
- the two square conditions `Q square` and `ell-Q square` have been absorbed
  into one rational parameter `u`;
- the remaining `V`-condition no longer references the `ell*Q+4` square
  variable at all.

## Why This Is The First New Missing Lemma

Everything before this proposition is now exact symbolic bookkeeping:

- `wl532` already supplied the exact `Q`-coordinate proposition.
- This work uses the already-forced prime class `ell ≡ 1 (mod 4)` together
  with a fixed representation `a^2+b^2=ell` to parameterize the circle
  `q^2+p^2=ell`.
- The remaining `ell*Q+4` square condition clears to one explicit quartic.
- The remaining `V`-condition becomes the exact two-square identity
  `2*Y^2 = A(u)^2 + B(u)^2`.

So no earlier ambiguity remains inside the `wl532` object layer. The only
unresolved step is now the simultaneous rational-point claim on this smaller
one-parameter conic-quartic system.

## Boundary Examples

Two exact examples show the new shrink is real but still not final.

First, at `ell=5`, choose

```text
a=1, b=2.
```

Then the basepoint `u=0` gives

```text
Q(0)=4
C^2 = 24,
```

which is not a rational square. So the first remaining failure can already
occur at the cleared `ell*q(u)^2+4` quartic.

Second, at `ell=13`, choose

```text
a=2, b=3.
```

Then `u=0` recovers exactly the old `wl532` boundary value

```text
Q(0)=9
C^2 = 121
C = 11
X(0) = 484/9.
```

The denominator-cleared `V`-condition becomes

```text
A(0)=751
B(0)=113
2*G_13(9) = 751^2 + 113^2 = 576770,
```

while `G_13(9)=288385` is not a rational square. So the remaining failure is
now exactly the new two-square `Y`-condition.

## Certificate

Executable certificate:

```text
scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction.py
tests/test_closure_quotient_rank_zero_aa_bb_wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction.py
```

The audit checks:

- the `ell=a^2+b^2` rational-circle parameterization;
- the inverse formulas and the harmless antipodal omission;
- the cleared quartic `C^2 = ell*N(u)^2 + 4*D(u)^2`;
- the exact positivity formula in the `u`-coordinate;
- the identity
  `2*G_ell(q^2)=(-q^4+(8*ell-12)q^2+4)^2 + (q^4+4*q^2-4)^2`;
- the denominator-cleared form `2*Y^2 = A(u)^2 + B(u)^2`;
- the `ell=5` and `ell=13` boundary examples.

Result artifact:

```text
results/closure_quotient_rank_zero_aa_bb_wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction.json
```

with:

```text
status = ok
ready = true
work_log = wl533
wl532_reduced_to_one_parameter_exact_obstruction_here = true
q_and_ell_minus_q_square_conditions_absorbed_here = true
remaining_ell_q_plus_4_and_v_obstructions_recorded_here = true
uniform_infinite_subfamily_exclusion_proved_here = false
strict_counterexample_found_here = false
advance_to_m3 = false
```

## Boundary

This work stops exactly at the one-parameter conic-quartic obstruction above.
It does not prove the remaining proposition, does not produce a counterexample,
does not classify the remaining rational points, and does not enter M3.
