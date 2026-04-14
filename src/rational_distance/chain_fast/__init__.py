"""Chain-fast public API."""

from .api import (
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
