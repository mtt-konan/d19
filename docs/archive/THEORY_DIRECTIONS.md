# Theory Directions

This file used to list short and medium-term search-space reductions. Most of
that list is now historical. The current theory layer is smaller and sharper.

## Active Theory Problem

Prove a uniform rank-zero statement for the closure quotient families:

```text
AA / BB / AA+BB quotient family
  -> local image theorem
  -> dyadic local condition
  -> global Selmer dimension bound
  -> rank zero
```

This is the only current theory direction with a plausible path from finite
certificates to a family theorem.

## Strict Tool Already Available

The usable certificate is:

```text
AA/BB quotient rank = 0
  -> enumerate torsion
  -> pull back
  -> only midpoint
  -> Yang Ji excludes midpoint
```

This is strict for the certified rows, but finite unless the rank-zero family
theorem is proved.

## Historical Short-Term Directions

These were useful but are not current mainline theory:

- factor-concordant divisor enumeration;
- Gaussian/mod-`p^2` filters;
- old safe-pair sieves;
- fixed-ratio `sum=A+B` transformations;
- partner/K-hub graph structure.

Their status is summarized in [EXPLORATION_MAP.md](./EXPLORATION_MAP.md) and
the consolidated worklogs.

## Next Checkpoint

The next meaningful theorem checkpoint is not another filter. It is:

```text
global Selmer dimension bound for a rank-zero closure quotient family
```

If that cannot be proved, the project should switch to residual-cover methods
or a different global obstruction.
