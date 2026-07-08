# wl394-wl407 — rank-zero odd-prime reduction consolidated

## Scope

This file replaces the odd-prime reduction logs `wl394` through `wl407`.

## Result

The odd-prime Selmer work reached reduction-level control, but not a local-image
theorem.

Current status:

```text
shared_odd_prime_local_image_schema_count = 4
reduction_partition_outline_count = 4
formal_lift_compatibility_proved_count = 0
local_image_schema_proved_count = 0
selmer_rank_upper_bound_proved_count = 0
family_exclusion_proved_count = 0
```

Plain meaning: the finite-field algebra has been sorted. The project still has
to lift those statements to the local fields used in the Selmer proof.

## What The Reduction Work Proved

The useful content is:

- The odd-prime cases reduce to 4 local-image schema shapes.
- Tangent squareclass `1` and tangent squareclass `-1` need different normal
  forms.
- For tangent squareclass `1`, the unit and non-node branches give direct
  squareclass control. The node value and punctured-node analysis leave a small
  reduction-level partition.
- For tangent squareclass `-1`, a nonsquare unit `nu` must remain in the normal
  form. Non-node, node, and punctured-node branches again reduce to a small
  partition.

The final reduction-level output is a list of candidate squareclass sets. It is
useful because it tells the next proof exactly what must be lifted.

## Missing Step

The missing step is formal lift compatibility:

```text
reduction-level partition
  -> local-field squareclass condition
  -> local image theorem
  -> Selmer bound
```

Without that lift, this file cannot promote any package to ready.

## Boundary

This consolidation keeps the odd-prime algebraic input and deletes per-branch
bookkeeping. It does not prove formal lift compatibility, any local-image
theorem, a global Selmer dimension bound, rank zero, or any family exclusion.
