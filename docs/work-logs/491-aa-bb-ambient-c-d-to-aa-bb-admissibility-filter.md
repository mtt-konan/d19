# AA+BB Ambient C_d To AA+BB Admissibility Filter

## Question

Using `wl490` as input, what reusable point-level filter must every ambient
global `C_d` point pass before it can enter the AA+BB admissible-point ledger?

This is a narrow filter-contract audit. It defines the reusable gate and applies
it only to the known `u_3` sample as a regression. It does not select another
`M_tail` / kernel candidate.

## Input From wl490

`wl490` removed the explicit `AA, A=3, B=1`, `d=(3,3,1)` point from the current
obstruction and admissible ledgers, kept it only in the diagnostic ledger, and
selected the next narrow gate:

```text
define_reusable_ambient_C_d_to_AA_BB_admissibility_filter
```

with:

```text
entered_here = false
```

## Filter Contract

For an ambient global `C_d` point, the reusable filter requires:

```text
candidate_id
quotient in {AA, BB}
A, B
L matching the source quotient leg
point_on_E_L.X, point_on_E_L.Y
parameters.p, parameters.q
complete_d_squareclass
route_context.ambient_global_C_d_solubility_already_established = true
route_context.old_package_x_S_tilde_bridge_not_used = true
```

The checks run in order:

```text
input_shape_and_scope
centered_even_pullback
AA_common_source_square_product
BB_common_source_square_product
positivity_and_nondegeneracy
```

The centered-even pullback uses:

```text
t = Y/(2*(X+p))
z = X/2 - t^2
N = (A+B+t)/2
M = A+B-N
quartic_y = z/4
```

and certifies both:

```text
z^2 = t^4 + p*t^2 + q
quartic_y^2 = (N^2+L^2)*(M^2+L^2)
```

The common-source square checks then test the same `N,M` on both sides:

```text
AA: (N^2+A^2)*(M^2+A^2)
BB: (N^2+B^2)*(M^2+B^2)
```

The positivity / nondegeneracy gate requires:

```text
A > 0, B > 0, N > 0, M > 0
```

## Output Classes

```text
admissible
  all checks pass

not_admissible
  pullback exists but a square or positivity/nondegeneracy check fails

missing_pullback_data
  input is scoped but the centered-even pullback cannot be certified

invalid_input
  required point-level data or route context is missing
```

Ledger routing is:

```text
admissible           -> admissible_point_ledger
not_admissible       -> globally_soluble_but_not_aa_bb_admissible_ledger
missing_pullback_data -> missing_pullback_data_ledger
invalid_input        -> invalid_or_unscoped_input_ledger
```

Only `admissible` may enter the AA+BB admissible-point ledger.

## u_3 Regression

Applying the filter to the known sample:

```text
candidate_id = AA_A3_B1_u_3_complete_d_candidate
A = 3
B = 1
d = (3, 3, 1)
X = 152
Y = 1536
```

gives the same pullback as `wl489`:

```text
t = 4
z = 60
N = 4
M = 0
quartic_y = 15
```

The `AA` product is square:

```text
(4^2+3^2)*(0^2+3^2) = 225
```

but the `BB` product is not:

```text
(4^2+1^2)*(0^2+1^2) = 17
```

and `M > 0` also fails. Therefore the reusable filter returns:

```text
output_class = not_admissible
can_enter_admissible_point_ledger = false
ledger_route = globally_soluble_but_not_aa_bb_admissible_ledger
blocking_reasons = BB_common_source_product_not_square, M_not_positive
```

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl491_ambient_c_d_to_aa_bb_admissibility_filter.json
```

with:

```text
status = ok
work_log = wl491
input_work_log = wl490
admissibility_filter_defined_here = true
u3_regression.output_class = not_admissible
u3_regression.can_enter_admissible_point_ledger = false
u3_regression.ledger_route =
  globally_soluble_but_not_aa_bb_admissible_ledger
broad_rank_or_selmer_diagnostics_run = false
single_curve_diagnostics_run = false
new_m_tail_or_kernel_candidate_selected_here = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
package_x_s_tilde_bridge_used = false
advance_to_wl492 = false
```

## Boundary

This work-log stops after `wl491`. It does not prove:

- that every ambient `C_d` point fails AA+BB admissibility,
- a new `M_tail` row or full-rank theorem,
- a new `M_tail` / kernel candidate,
- a complete Selmer upper bound,
- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.
