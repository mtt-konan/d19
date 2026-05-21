# 029-legacy-stub-cleanup

## Summary

Tidied the top-level `src/rational_distance/` directory by moving the four
compatibility re-export files into a new `_legacy/` subpackage, and leaving
9-line forwarding stubs at the top level.

No functionality changed; all 191 tests still pass without touching any
historical import paths.

## Why

The top-level directory had four "compatibility entrypoints" mixed in with
real implementation files:

- `concordant_ec.py` (32 lines, full re-export of `concordant.*`)
- `pair_generator.py` (6 lines, re-exports `concordant.pairs`)
- `search_chain_fast.py` (33 lines, re-exports `chain_fast.*`)
- `search_ec.py` (58 lines, re-exports `ec_search.*`)

They were leftover from a previous restructuring. They have many real
callers — `chain_db.py`, `ec_db.py`, `cli/search/*_runner.py`, and a number
of tests — so they cannot simply be deleted. But they cluttered the listing
when scanning the top level.

## What Changed

Physical layout:

- New subpackage: `src/rational_distance/_legacy/`
  - `__init__.py` — explains the package is deprecated
  - `concordant_ec.py` — moved full re-export here
  - `pair_generator.py` — moved here
  - `search_chain_fast.py` — moved here
  - `search_ec.py` — moved here
- Top-level files shrunk to 9-line stubs of the form:

  ```python
  """Deprecated stub. Real implementation: ``rational_distance.concordant``."""

  from rational_distance._legacy.concordant_ec import *  # noqa: F403
  from rational_distance._legacy.concordant_ec import __all__ as __all__
  ```

Doc updates:

- `docs/IMPLEMENTATION.md` §1 "总原则" — clarifies that the four top-level
  stubs are 9-line forwarders, real lists in `_legacy/`
- `docs/IMPLEMENTATION.md` §4 "兼容层" — splits the description into
  "top-level stubs" vs "real re-export lists", plus a migration path for
  eventually deleting the legacy layer

## Size Comparison

```
Before                                After
------                                -----
concordant_ec.py        801 bytes  →  438 bytes (9 lines)
pair_generator.py       161 bytes  →  403 bytes (9 lines)
search_chain_fast.py    797 bytes  →  436 bytes (9 lines)
search_ec.py           1334 bytes  →  410 bytes (9 lines)
                                     _legacy/  256 bytes (subdir w/ 5 files)
```

(`pair_generator.py` actually grew a bit because the original was 6 lines
with no docstring; the new stub has a 5-line deprecation docstring.)

## Verification

- `uv run pytest`: 191 / 191 passed
- `uv run ruff check src/rational_distance/_legacy/ src/rational_distance/{concordant_ec,pair_generator,search_chain_fast,search_ec}.py`:
  clean after `--fix` of one `RUF100` (unused `noqa`) per file
- No call site was modified — every historical import path
  (`from rational_distance.search_chain_fast import ...`, etc.) still works

## Future Cleanup Path

Whenever the project decides to fully retire the legacy layer:

1. Replace every `from rational_distance.search_chain_fast import X` with
   `from rational_distance.chain_fast import X` (and the three analogous
   substitutions for the other three stubs).
2. Run `uv run pytest` — should still pass.
3. Delete the four top-level stub files and the entire `_legacy/` directory.

Step 1 is the bulk of the work (it touches `chain_db.py`, `ec_db.py`, a few
CLI runners, and several test files). Step 3 is then trivial.

## Takeaway

This is a pure refactor with zero behavioural change. It exists to make the
top-level `src/rational_distance/` listing visually cleaner: the four
forwarding stubs are now obviously small (≈ 400 bytes each) compared to the
real implementation files (1.7–23 KB), which makes the maintenance zoning
documented in `IMPLEMENTATION.md` visually obvious as well.
