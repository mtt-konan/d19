#!/usr/bin/env python3
"""Historical stub for stale proof-status DB finite-descent layer-2 scans."""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Historical finite-descent layer-2 scan. Defaults referenced "
            "results/proof_status.db, which is stale historical data."
        )
    )
    parser.add_argument("--db", default="results/proof_status.db")
    parser.parse_args()


if __name__ == "__main__":
    main()
