"""Search CLI split into parser, runners, and output helpers."""

from __future__ import annotations

from .parser import build_parser
from .runners import (
    RUNNERS,
    _resolve_parametric_limits,
    _run_chain,
    _run_chain_fast,
    _run_concordant,
    _run_ec,
    _run_parametric,
)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    RUNNERS[args.method](args)


__all__ = [
    "RUNNERS",
    "_resolve_parametric_limits",
    "_run_chain",
    "_run_chain_fast",
    "_run_concordant",
    "_run_ec",
    "_run_parametric",
    "build_parser",
    "main",
]
