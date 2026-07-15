#!/usr/bin/env python3
"""Submit a Magma source file to the free University of Sydney calculator."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path

CALCULATOR_ENDPOINT = "http://magma.maths.usyd.edu.au/xml/calculator.xml"
CALCULATOR_PAGE = "http://magma.maths.usyd.edu.au/calc/"
MAX_INPUT_BYTES = 50_000


@dataclass(frozen=True)
class CalculatorResult:
    status: str
    version: str | None
    max_time: int | None
    max_input: int | None
    seed: int | None
    elapsed_seconds: float | None
    memory: str | None
    warnings: list[str]
    lines: list[str]


def validate_source(source: str) -> int:
    size = len(source.encode("utf-8"))
    if size > MAX_INPUT_BYTES:
        raise ValueError(f"Magma input is {size} bytes; calculator limit is {MAX_INPUT_BYTES}")
    return size


def calculator_url(source: str) -> str:
    validate_source(source)
    return f"{CALCULATOR_PAGE}?{urllib.parse.urlencode({'input': source})}"


def parse_calculator_xml(payload: bytes) -> CalculatorResult:
    root = ET.fromstring(payload)
    if root.tag != "calculator":
        raise ValueError(f"unexpected calculator response root: {root.tag}")

    headers = root.find("headers")

    def header(name: str) -> str | None:
        node = headers.find(name) if headers is not None else None
        return node.text if node is not None else None

    warnings = [node.text or "" for node in (() if headers is None else headers.findall("warning"))]
    alert = header("alert")
    if alert:
        warnings.insert(0, alert)
    lines_node = root.find("results")
    lines = [node.text or "" for node in (() if lines_node is None else lines_node.findall("line"))]
    error_markers = ("Runtime error", "User error", "Internal error")
    has_magma_error = any(marker in line for marker in error_markers for line in lines)
    status = "magma_error" if warnings or has_magma_error else "ok"

    return CalculatorResult(
        status=status,
        version=header("version"),
        max_time=int(value) if (value := header("max_time")) else None,
        max_input=int(value) if (value := header("max_input")) else None,
        seed=int(value) if (value := header("seed")) else None,
        elapsed_seconds=float(value) if (value := header("time")) else None,
        memory=header("memory"),
        warnings=warnings,
        lines=lines,
    )


def submit_source(
    source: str,
    *,
    timeout: float = 75.0,
    proxy: str | None = None,
) -> CalculatorResult:
    validate_source(source)
    body = urllib.parse.urlencode({"input": source}).encode("ascii")
    request = urllib.request.Request(
        CALCULATOR_ENDPOINT,
        data=body,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "d19-magma-calculator/1",
        },
        method="POST",
    )
    proxy_config = {"http": proxy, "https": proxy} if proxy else {}
    opener = urllib.request.build_opener(urllib.request.ProxyHandler(proxy_config))
    with opener.open(request, timeout=timeout) as response:
        return parse_calculator_xml(response.read())


def _print_result(result: CalculatorResult) -> None:
    print(f"status={result.status}")
    print(f"version={result.version or 'unknown'}")
    if result.elapsed_seconds is not None:
        print(f"elapsed_seconds={result.elapsed_seconds}")
    if result.memory is not None:
        print(f"memory={result.memory}")
    for warning in result.warnings:
        print(f"warning={warning}", file=sys.stderr)
    if result.lines:
        print("--- magma output ---")
        print("\n".join(result.lines))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Magma .m source file")
    parser.add_argument("--timeout", type=float, default=75.0)
    parser.add_argument(
        "--proxy",
        help="optional HTTP proxy; environment proxy variables are ignored by default",
    )
    parser.add_argument("--json-out", type=Path)
    parser.add_argument(
        "--print-url",
        action="store_true",
        help="print a browser URL instead of submitting the source",
    )
    args = parser.parse_args()

    try:
        source = args.source.read_text(encoding="utf-8")
        size = validate_source(source)
        print(f"input_bytes={size}")
        if args.print_url:
            print(calculator_url(source))
            return 0
        result = submit_source(source, timeout=args.timeout, proxy=args.proxy)
    except (OSError, ValueError, ET.ParseError, urllib.error.URLError) as exc:
        print(f"status=transport_error\nerror={exc}", file=sys.stderr)
        return 3

    _print_result(result)
    if args.json_out is not None:
        args.json_out.write_text(
            json.dumps(asdict(result), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return 0 if result.status == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
