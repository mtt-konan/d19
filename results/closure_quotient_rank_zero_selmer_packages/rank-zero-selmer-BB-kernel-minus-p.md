# rank-zero-selmer-BB-kernel-minus-p

Status: open

## Scope

- family_pattern = BB
- kernel = kernel_minus_p
- candidate_class_count = 75
- model_count = 75

## Symbolic Model

- T = A+B
- L role = A for AA, B for BB; AA+BB requires both sides to close
- kernel_root = -p
- target_a2 = 32*L^2 - 8*T^2
- target_a4 = 16*(T^2 + 4*L^2)^2

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
  - proof_path = docs/work-logs/456-bb-minus-p-formal-lift-reviewable-proof.md
  - scope = odd-prime only
  - summary = The BB odd-prime formal-lift compatibility segment is written as a line-by-line proof for the minus-p kernel; the dyadic place, the corrected global Selmer bound, and rank zero remain open.

## Boundary

transcript_status = partial

No Selmer rank upper bound is proved by this file. No rank-zero theorem or lambda-family exclusion is claimed here.
