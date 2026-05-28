#!/usr/bin/env python3
"""Extract text from one or more PDF files.

Examples:
    uv run python scripts/extract_pdf_text.py docs/literature/pdfs/*.pdf
    uv run python scripts/extract_pdf_text.py paper.pdf --output paper.txt
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import cast

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract text from PDF files using pypdf")
    _ = parser.add_argument("pdfs", nargs="+", type=Path, help="PDF files to extract")
    _ = parser.add_argument(
        "--output",
        type=Path,
        help="Output file. Only valid when extracting a single PDF.",
    )
    return parser.parse_args()


def main() -> int:
    from rational_distance.literature.pdf_text import write_pdf_text

    args = parse_args()
    pdfs = cast(list[Path], args.pdfs)
    output = cast(Path | None, args.output)

    if output is not None and len(pdfs) != 1:
        print("--output can only be used with one PDF", file=sys.stderr)
        return 2

    for pdf_path in pdfs:
        out_path = write_pdf_text(pdf_path, output)
        print(f"wrote {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
