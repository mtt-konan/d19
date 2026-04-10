"""Placeholder: search for points with rational distances to all 4 vertices.

This script will build on search_3vertex.py by filtering its output and
applying additional algebraic constraints for the fourth vertex.

Usage:
    uv run python scripts/search_4vertex.py [--max-m M] [--max-k-num N] ...

Currently delegates to search_3vertex with --min-rational 4.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scripts.search_3vertex import main as _main3  # noqa: F401

# Override default --min-rational to 4 unless user supplied it
if "--min-rational" not in sys.argv:
    sys.argv += ["--min-rational", "4"]


def main() -> None:
    _main3()


if __name__ == "__main__":
    main()
