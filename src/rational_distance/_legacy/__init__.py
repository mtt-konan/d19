"""Deprecated compatibility re-exports.

Code in this package is **not** the place to add new functionality. Each
module here exists only to keep historical import paths working:

- ``rational_distance.concordant_ec``      → ``rational_distance.concordant.*``
- ``rational_distance.pair_generator``     → ``rational_distance.concordant.pairs``
- ``rational_distance.search_chain_fast``  → ``rational_distance.chain_fast``
- ``rational_distance.search_ec``          → ``rational_distance.ec_search``

The top-level files (e.g. ``rational_distance/concordant_ec.py``) are now
one-line stubs that forward into this package, so they do not clutter the
top-level directory listing with full re-export lists.

When you write new code, import from the canonical packages directly. The
stubs and this ``_legacy`` package can be deleted once every call site has
been migrated.
"""
