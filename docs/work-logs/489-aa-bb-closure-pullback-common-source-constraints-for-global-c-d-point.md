# AA+BB Closure Pullback Common-Source Constraints For Global C_d Point

## Question

Using `wl488` as input, does the explicit `wl486`/`wl487` global point

```text
X = 152
Y = 1536
d = (3, 3, 1)
```

for `AA, A=3, B=1` satisfy the AA+BB closure / pullback / common-source
constraints, fail them, or force a missing-pullback-data stop?

This is a point-level routing audit only.

## Input From wl488

`wl488` selected the narrow gate:

```text
AA_BB_closure_pullback_common_source_constraints_for_global_C_d_point
```

and did not enter it. The selected point is the `AA_A3_B1_u_3` complete
`d`-coordinate class:

```text
d_minus_p      = 3
d_pos_2sqrt_q  = 3
d_neg_2sqrt_q  = 1
```

with the ambient elliptic curve

```text
E_L: Y^2=(X+p)*(X^2-4*q)
p = 40
q = 2704
sqrt_q = 52
```

## Pullback Check

For the centered even `AA/BB` closure quotient, use the inverse map:

```text
t = Y/(2*(X+p))
z = X/2 - t^2
N = (A+B+t)/2
M = A+B-N
quartic_y = z/4
```

For `(X,Y)=(152,1536)` this gives:

```text
t = 4
z = 60
N = 4
M = 0
quartic_y = 15
```

The map check is exact:

```text
60^2 = 4^4 + 40*4^2 + 2704
15^2 = (4^2+3^2)*(0^2+3^2)
```

So the current repo evidence is enough to pull the point back to the `AA`
closure quotient. `wl489` does not stop at a missing-pullback-data gate.

## Common-Source Constraint Check

The same source variables are:

```text
A = 3
B = 1
N = 4
M = 0
```

The `AA` side closes:

```text
N^2 + A^2 = 25
M^2 + A^2 = 9
(N^2+A^2)*(M^2+A^2) = 225 = 15^2
```

The `BB` side fails:

```text
N^2 + B^2 = 17
M^2 + B^2 = 1
(N^2+B^2)*(M^2+B^2) = 17
```

`17` is not a rational square. Also `M=0`, so the point is not a
nondegenerate positive closure point.

## Verdict

`wl489` proves, only for this explicit point:

```text
status = proved_fails_for_this_explicit_point
proved_satisfies_AA_BB_constraints = false
proved_fails_AA_BB_constraints = true
missing_pullback_data_gate_triggered = false
```

Thus the `u_3` point is a genuine global point on the ambient `AA` curve and
pulls back to the `AA` closure quotient, but it is not an AA+BB common-source
closure point.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl489_closure_pullback_common_source_constraints_for_global_c_d_point.json
```

with:

```text
status = ok
work_log = wl489
input_work_log = wl488
aa_pullback.checks.aa_pullback_proved_for_this_point = true
common_source_constraint_audit.bb_side.product_is_square = false
wl489_verdict.status = proved_fails_for_this_explicit_point
advance_to_wl490 = false
broad_rank_or_selmer_diagnostics_run = false
single_curve_diagnostics_run = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
package_x_s_tilde_bridge_used = false
```

## Boundary

This work-log stops after `wl489`. It does not prove:

- that every ambient `C_d` point fails AA+BB admissibility,
- a new `M_tail` row or full-rank theorem,
- a complete Selmer upper bound,
- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.
