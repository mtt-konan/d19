# Historical Script Archive

This directory keeps only the small archived code that still has an active
test/import path.

## Kept

```text
compare_parametric.py
analyze_chain_db.py
analyze_ec_db.py
```

These remain because tests still cover their old command surfaces.

## Removed

Older dual-EC, ell2cover, finite-descent implementation, SHA2 worker,
generator-lattice, and stale `proof_status.db` one-off scripts were removed
from the active tree. They were historical run tools, not current research
entry points. Recover exact text with git history if needed.

Current entry points live in `scripts/README.md`.
