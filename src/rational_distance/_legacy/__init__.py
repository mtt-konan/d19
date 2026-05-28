"""Deprecated implementations from the chain-fast / EC / parametric era (wl053).

Code in this package is **not** the place to add new functionality. Each
module here exists only to keep historical functionality alive. Canonical
homes for new code:

- ``rational_distance._legacy.concordant_ec``      → ``rational_distance.concordant.*``
- ``rational_distance._legacy.pair_generator``     → ``rational_distance.concordant.pairs``
- ``rational_distance._legacy.search_chain_fast``  → ``rational_distance.chain_fast``
- ``rational_distance._legacy.search_ec``          → ``rational_distance.ec_search``

History note: the top-level ``rational_distance/<name>.py`` stubs that used
to forward into this package were removed in wl084-followup refactor; all
call sites now import from ``rational_distance._legacy.<name>`` directly.
"""
