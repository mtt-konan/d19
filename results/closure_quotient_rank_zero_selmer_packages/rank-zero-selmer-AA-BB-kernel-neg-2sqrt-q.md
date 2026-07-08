# rank-zero-selmer-AA-BB-kernel-neg-2sqrt-q

Status: open

## Scope

- family_pattern = AA+BB
- kernel = kernel_neg_2sqrt_q
- candidate_class_count = 43
- model_count = 86

## Symbolic Model

- T = A+B
- L role = A for AA, B for BB; AA+BB requires both sides to close
- kernel_root = -2*sqrt_q
- target_a2 = 16*(T^2 + 2*L^2)
- target_a4 = 256*L^4

## Required Transcript

- statement
- isogeny_setup
- local_squareclass_conditions
- selmer_bound_argument
- rank_zero_conclusion
- review_notes

## Partial Transcript Segments

- `selmer_bound_argument` / `formal_lift_compatibility`
  - status = reviewable-proof
  - proof_path = docs/work-logs/457-aa-bb-neg-kernel-formal-lift-reviewable-proof.md
  - scope = odd-prime valuation support only
  - summary = The AA+BB odd-prime formal-lift compatibility segment is written as a line-by-line support-collapse proof for the neg kernel; the dyadic place, unit/sign classes, the global Selmer bound, and rank zero remain open.

## Boundary

transcript_status = partial

No Selmer rank upper bound is proved by this file. No rank-zero theorem or lambda-family exclusion is claimed here.
