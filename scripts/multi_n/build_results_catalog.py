#!/usr/bin/env python3
"""Build a machine-readable catalog of curated result artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    from rational_distance.results.catalog import write_results_catalog

    output_path = write_results_catalog(ROOT / "results")
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
