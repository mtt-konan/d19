# Advanced Theory Directions

This file now records fallback directions if the rank-zero Selmer route fails.

## Current Advanced Mainline

The advanced route currently being attempted is not Heegner or Chabauty. It is:

```text
2-isogeny / Selmer analysis of closure quotient families
```

See:

- [CLOSURE_QUOTIENT_MAINLINE.md](../CLOSURE_QUOTIENT_MAINLINE.md)
- [386-rank-zero-selmer-package-consolidated.md](../work-logs/386-rank-zero-selmer-package-consolidated.md)
- [394-rank-zero-odd-prime-reduction-consolidated.md](../work-logs/394-rank-zero-odd-prime-reduction-consolidated.md)

## Fallbacks

If the family Selmer bound does not close, the serious fallback directions are:

- Mordell-Weil sieve on explicit residual covers;
- Cassels-Tate pairing for Sha[2] candidates;
- Magma/Sage no-point certificates;
- Chabauty or quadratic Chabauty on carefully chosen high-genus models;
- Brauer-Manin obstruction with outside expertise.

These are heavier and less automatic than the current family proof attempt.

## Closed As Mainline

The following are no longer recommended as main proof engines:

- Heegner height as a global decider;
- L-function rank computation as a filter;
- second descent only to decide rank;
- pure mod-`p^2` universal obstruction;
- K3 surface speculation without a concrete model.

They may still be useful as local tools or paper background.

## Practical Rule

Use an advanced direction only when it can produce one of:

- a no-point certificate for a specific residual cover;
- a theorem covering infinitely many `lambda`;
- a falsifiable obstruction stronger than current local filters.
