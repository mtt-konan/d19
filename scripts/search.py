"""Compatibility entrypoint for the split search CLI.

Tests still import ``build_parser`` and ``_resolve_parametric_limits`` from
this historical script module, so keep only that small compatibility surface.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rational_distance.cli.search import build_parser, main
from rational_distance.cli.search.parametric_runner import _resolve_parametric_limits

__all__ = ["_resolve_parametric_limits", "build_parser", "main"]


if __name__ == "__main__":
    main()
