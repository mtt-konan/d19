"""Thin compatibility entrypoint for the split search CLI."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rational_distance.cli.search import (
    _resolve_parametric_limits,
    _run_chain,
    _run_chain_fast,
    _run_concordant,
    _run_ec,
    _run_parametric,
    build_parser,
    main,
)
from rational_distance.cli.search.output import (
    _NearMissTopK,
    _print_chain_fast_profile,
)

__all__ = [
    "_NearMissTopK",
    "_print_chain_fast_profile",
    "_resolve_parametric_limits",
    "_run_chain",
    "_run_chain_fast",
    "_run_concordant",
    "_run_ec",
    "_run_parametric",
    "build_parser",
    "main",
]


if __name__ == "__main__":
    main()
