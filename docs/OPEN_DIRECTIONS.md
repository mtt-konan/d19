# Open Directions

This document keeps only directions that are still worth considering. Detailed
history belongs in the worklogs, not here.

## P0: Try The Common-Source Square Obstruction Lemma

Current gate:

```text
try_common_source_square_obstruction_lemma_candidate_not_entered_here
```

Input state:

- `wl522` compressed the `wl491`-`wl521` AA+BB admissibility ledgers.
- The taxonomy has no genuinely deferred cover family.
- The taxonomy has no AA+BB-admissible cover family.
- The remaining named theorem-candidate is:

```text
common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families
```

This direction should attempt a reusable proof that the recorded opposite-side
AA/BB common-source products cannot be rational squares in the globally
soluble but not-admissible cover families.

Do not turn this into shell 11, new support computation, new ambient `C_d`
solubility tests, final-candidate selection, or broad Selmer/rank diagnostics.

## P1: Return To Selmer Family Proof Only With A Named Gap

The high-level rank-zero/Selmer route still needs:

```text
odd-prime local image
dyadic local condition
formal lift compatibility
global Selmer dimension bound
rank-zero conclusion
```

Enter this direction only when the next proof obligation is named precisely.
More finite samples, packages, or route counts do not by themselves advance a
theorem-level Selmer upper bound.

## P2: Finite Shell Extension

The previous finite-shell machinery selected a later shell extension at:

```text
max(A,B) = 11
```

This is lower priority than the lemma candidate isolated by `wl522`. Execute
shell 11 only if the user explicitly chooses this route, and keep it classified
as finite `M_tail` diagnostic work rather than Selmer theorem progress.

## Closed Or Paused Directions

- The old package-`x` / `S~` bridge is deprecated as a theorem bridge.
- `M_tail` diagnostics are parameter-dependent; do not claim uniform full rank
  from finite shell counts.
- Ambient `C_d` global points must pass the `wl491` AA+BB common-source
  admissibility filter before entering any admissible-point ledger.
- Globally soluble but not AA+BB-admissible ledgers are diagnostic failures,
  not obstruction candidates.

Older long direction lists are archived under `docs/archive/` and the
consolidated worklogs.
