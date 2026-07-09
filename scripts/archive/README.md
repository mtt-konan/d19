# Historical Script Archive

This directory keeps only the small archived code that still has an active
test/import path.

## Kept

```text
compare_parametric.py
```

CPU/GPU parametric backend comparison helper. It is still imported by
`tests/test_cli.py` as a regression check for the old command surface.

## Removed

Older chain DB, EC DB, SHA2, dual-EC, ell2cover, finite-descent, and generator
lattice one-off scripts were removed from the active tree. They were historical
run tools, not current research entry points. Recover exact text with git
history if needed.

Current entry points live in `scripts/README.md`.
