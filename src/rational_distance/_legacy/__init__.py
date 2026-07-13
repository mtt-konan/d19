"""Deprecated implementations from the chain-fast / EC / parametric era (wl053).

Code in this package is **not** the place to add new functionality. Each
module here exists only to keep historical functionality alive. Canonical
homes for the removed re-export modules are:

- concordant analysis: ``rational_distance.concordant``
- pair generation: ``rational_distance.concordant.pairs``
- chain-fast search: ``rational_distance.chain_fast``
- elliptic-curve search: ``rational_distance.ec_search``

The repository's internal callers now use those canonical paths directly.
The remaining modules here are historical database, analysis, and persistence
implementations that still have an explicit provenance or runtime use.
"""
