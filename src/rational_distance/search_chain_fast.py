"""Compatibility layer for the chain-fast search API.

The implementation now lives in ``rational_distance.chain_fast``:

- ``api.py``      — public entrypoints and stable return types
- ``workflow.py`` — chunking, multiprocessing, merge, and orchestration
- ``kernel.py``   — pure numpy/python scanning logic
"""

from __future__ import annotations

from rational_distance.chain_fast import (
    _HAS_NUMPY,
    _NUMPY_MAX_HYP,
    ChainFastExecution,
    ChainFastProfile,
    build_chain_fast_triples,
    find_chains_fast,
    resolve_backend_choice,
    run_chain_fast,
)

__all__ = [
    "_HAS_NUMPY",
    "_NUMPY_MAX_HYP",
    "ChainFastExecution",
    "ChainFastProfile",
    "build_chain_fast_triples",
    "find_chains_fast",
    "resolve_backend_choice",
    "run_chain_fast",
]
