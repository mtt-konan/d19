# wl386-wl393, wl410-wl418 — rank-zero Selmer package consolidated

## Scope

This file replaces the package and queue logs `wl386` through `wl393`, plus
`wl410` through `wl418`.

## Result

The rank-zero route is now an organized proof workload, not a search workload.

Current package status:

```text
family_obligation_count = 3
kernel_count = 3
selmer_obligation_count = 9
package_count = 9
open_package_count = 9
transcript_package_ready_count = 0
strict_promotion_ready_count = 0
selmer_rank_upper_bound_proved_count = 0
family_exclusion_proved_count = 0
```

Plain meaning: there are 9 proof packages. All 9 are still open. The project has
not proved the needed Selmer bound.

## Package Structure

The 3 family obligations are:

```text
AA
AA+BB
BB
```

Each one has 3 kernel obligations:

```text
kernel_minus_p
kernel_pos_2sqrt_q
kernel_neg_2sqrt_q
```

So the proof target is `3 families x 3 kernels = 9 packages`.

The symbolic model is shared enough that the work should not be written 9
separate times. The useful compression is:

```text
kernel_schema_count = 3
shared_kernel_schema_count = 3
setup_template_count = 3
shared_isogeny_setup_template_count = 3
family_conclusion_template_count = 3
```

## Transcript Fields

The transcript has 6 fields:

```text
statement
isogeny_setup
local_squareclass_conditions
selmer_bound_argument
rank_zero_conclusion
review_notes
```

They split like this:

```text
kernel_shared_field_count = 2
family_aggregated_field_count = 1
package_specific_field_count = 3
primary_remaining_proof_field = selmer_bound_argument
```

Plain meaning: `isogeny_setup` and `local_squareclass_conditions` should be
shared by kernel. `rank_zero_conclusion` should be written by family. The hard
part is still `selmer_bound_argument`.

## Local Supports

The candidate bad factors for local Selmer work are:

```text
2
L
T
T^2 + 4L^2
```

The three kernels have these quadratic squareclass shapes:

```text
kernel_minus_p       -> -1
kernel_pos_2sqrt_q   -> T^2 + 4L^2
kernel_neg_2sqrt_q   -> T^2 + 4L^2
```

Odd-prime bookkeeping collapsed to 9 unified tasks, then to 4 local-image schema
targets and 4 formal-lift theorem targets. Those are inputs for proof writing,
not finished proofs.

## Required Bound Argument Sections

Each package still needs 5 sections:

```text
shared_isogeny_setup_reference
odd_prime_local_image_theorems
formal_lift_compatibility
dyadic_local_condition
global_selmer_dimension_bound
```

The count `required_section_count = 45` is just `9 packages x 5 sections`.
Increasing or decreasing this count is bookkeeping. It is not mathematical
progress.

## Boundary

This consolidation keeps the package map and deletes repeated queue logs. It
does not prove any local condition, formal lift, Selmer dimension bound,
rank-zero theorem, or `lambda` family exclusion.
