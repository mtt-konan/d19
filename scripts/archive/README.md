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

The stale `proof_status.db` scripts now remain only as tiny `--help` stubs so
old provenance tests continue to document that they used historical data:

```text
batch_ell2cover_hard_cases.py
batch_sha2_scan_v2.py
finite_descent_hard_cases.py
finite_descent_layer2.py
pattern_hunt_hard_cases.py
probe_chain_closure_mod_sieve.py
```

## Removed

Older dual-EC, ell2cover, finite-descent implementation, SHA2 worker, and
generator-lattice one-off scripts were removed from the active tree. They were
historical run tools, not current research entry points. Recover exact text
with git history if needed.

Current entry points live in `scripts/README.md`.
