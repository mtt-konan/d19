#!/usr/bin/env python3
"""Audit residual-cover wording so evidence is not promoted to proof."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

FORBIDDEN_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "bounded-search-proof-overclaim",
        re.compile(
            r"(bounded search|bounded point search|hyperellratpoints)"
            r".{0,80}\b(proves?|certifies?|establishes?)\b"
            r".{0,80}(no rational point|no point|cover has no)",
            re.IGNORECASE,
        ),
    ),
    (
        "bsd-strict-certificate-overclaim",
        re.compile(
            r"\bBSD\b(?!.*\bnot a strict\b)(?!.*\bnot an unconditional\b)"
            r".{0,80}\b(strict|unconditional)\b.{0,80}"
            r"(rank certificate|certificate|proof)",
            re.IGNORECASE,
        ),
    ),
)

REQUIRED_BOUNDARY_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("candidate_not_proof", re.compile(r"candidate-not-proof", re.IGNORECASE)),
    ("sha2_candidate", re.compile(r"Sha\[2\].{0,80}candidate", re.IGNORECASE)),
    (
        "bounded_search_not_proof",
        re.compile(
            r"(bounded (?:point )?search.{0,80}(not a proof|does not prove))"
            r"|((bounded search|bounded rational_points|hyperellratpoints).{0,80}"
            r"(不是|仍只是|!=).{0,80}证明)",
            re.IGNORECASE,
        ),
    ),
    (
        "bsd_not_strict_certificate",
        re.compile(
            r"BSD.{0,100}(not a strict rank certificate|do not replace the strict)"
            r"|BSD.{0,80}不是.{0,20}(严格|无条件).{0,20}证书",
            re.IGNORECASE,
        ),
    ),
)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _violations_for_path(path: Path) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        for kind, pattern in FORBIDDEN_PATTERNS:
            if pattern.search(line):
                violations.append(
                    {
                        "path": str(path),
                        "line": line_number,
                        "kind": kind,
                        "text": line.strip(),
                    }
                )
    return violations


def _required_hits_for_path(path: Path) -> Counter[str]:
    text = path.read_text(encoding="utf-8")
    hits: Counter[str] = Counter()
    for name, pattern in REQUIRED_BOUNDARY_PATTERNS:
        hits[name] += len(pattern.findall(text))
    return hits


def audit_language(paths: list[Path]) -> dict[str, Any]:
    violations: list[dict[str, Any]] = []
    required_hits: Counter[str] = Counter()
    for path in paths:
        violations.extend(_violations_for_path(path))
        required_hits.update(_required_hits_for_path(path))
    return {
        "files": len(paths),
        "violations": violations,
        "required_boundary_hits": {
            name: int(required_hits.get(name, 0))
            for name, _pattern in REQUIRED_BOUNDARY_PATTERNS
        },
        "boundary": (
            "This language audit checks residual-cover wording. It does not "
            "verify the mathematics; it only helps prevent numerical evidence "
            "from being written as a proof."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, action="append", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_language(args.path)
    write_json(args.out, audit)
    violation_count = len(audit["violations"])
    print(f"wrote mixed closure residual language audit to {args.out}")
    print(f"files={audit['files']}")
    print(f"violations={violation_count}")
    print(f"required_boundary_hits={audit['required_boundary_hits']}")
    if args.strict and violation_count:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
