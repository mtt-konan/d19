# AA+BB Route Impact of Global Point

## Question

Using `wl486` as input, what does the exact integral point on the `u_3`
complete `d`-coordinate cover change in the AA+BB route?

This is a route-impact audit only. It does not run broad rank or Selmer
diagnostics.

## Input from wl486

The `wl486` local-solubility gate found that the cover

```text
d = (3, 3, 1)
```

for `AA, A=3, B=1` has the exact integral point

```text
X = 152
u_minus_p = 8
u_pos_2sqrt_q = 4
u_neg_2sqrt_q = 16
```

and induces

```text
(X, Y) = (152, 1536)
```

on

```text
E_L: Y^2=(X+p)*(X^2-4*q)
```

with

```text
p = 40
q = 2704
sqrt_q = 52
```

## Refutation Scope

The global point refutes only this interpretation:

```text
this_specific_u3_as_locally_soluble_globally_pointless_obstruction
```

It proves that this `d=(3,3,1)` cover is not a Sha-style
locally-soluble globally-pointless obstruction candidate.

It does not refute:

- `M_tail_uniform_full_rank_missing` as a general route gap,
- the possibility of other complete `d`-coordinate obstructions,
- the need for a complete Selmer upper bound.

## Point Classification Against the Visible 2-Torsion Baseline

The exact differences from the three roots are

```text
X + p          = 192 = 3*8^2
X - 2*sqrt_q  = 48  = 3*4^2
X + 2*sqrt_q  = 256 = 1*16^2
```

So the point has complete `d`-coordinate squareclass

```text
(3, 3, 1)
```

and satisfies the product relation:

```text
3*3*1 = 3^2
```

For this sample, the visible `E_L[2](Q)` baseline from `wl474`, reduced to
integer squareclass representatives in the same coordinate order, is

```text
O:              (1, 1, 1)
T_minus_p:      (-1, -1, 1)
T_pos_2sqrt_q:  (1, 13, 13)
T_neg_2sqrt_q:  (-1, -13, 13)
```

The point squareclass `(3, 3, 1)` is not one of these baseline representatives.
Also `Y=1536` is nonzero and `X=152` is not one of the roots
`-40, 104, -104`.

Thus `wl487` classifies the point only as

```text
non_torsion_candidate_not_visible_two_torsion_baseline
```

This is not a full Mordell-Weil torsion computation and not a rank computation.

## Route Impact

The `u_3` datum is no longer available as the current global obstruction
candidate:

```text
m_tail_status_after_global_point =
  u3_no_longer_available_as_global_obstruction_candidate

global_obstruction_routing_status =
  current_explicit_C_d_obstruction_route_refuted_by_global_point
```

The ledger impact is:

```text
mark d=(3,3,1) as globally soluble with a non-baseline complete
d-coordinate point candidate; do not count it as an obstruction or as
Selmer upper-bound progress
```

No new local/Hilbert row is found here, and the `M_tail` full-rank rescue path
is not reopened here.

## Next Narrow Gate

The next gate is recorded but not entered:

```text
select_next_complete_d_coordinate_route_after_u3_global_point
```

Allowed next actions at that later gate:

- remove this `u_3` cover from the obstruction-candidate ledger,
- choose the next single complete `d`-coordinate candidate or row gap,
- keep `M_tail` and global-obstruction ledgers separate.

Forbidden at `wl487`:

- broad rank or Selmer diagnostics,
- a complete Selmer upper-bound claim,
- rank-zero or `Sha[2]=0` claims,
- family exclusion claims.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl487_route_impact_of_global_point.json
```

with:

```text
status = ok
work_log = wl487
input_work_log = wl486
refutation_scope.refuted_interpretation =
  this_specific_u3_as_locally_soluble_globally_pointless_obstruction
global_point_classification.classification =
  non_torsion_candidate_not_visible_two_torsion_baseline
route_impact.m_tail_status_after_global_point =
  u3_no_longer_available_as_global_obstruction_candidate
next_narrow_gate.entered_here = false
broad_rank_or_selmer_diagnostics_run = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
```

## Boundary

This work-log stops after the `wl487` route-impact audit. It does not prove:

- full Mordell-Weil torsion classification,
- Mordell-Weil rank,
- a Cassels-Tate or second-descent obstruction,
- an analytic-rank or L-value theorem,
- a complete Selmer upper bound,
- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.
