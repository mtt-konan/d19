"""PDF text extraction helpers for local literature notes."""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader


def extract_pdf_text(pdf_path: str | Path) -> str:
    """Extract text from every page of a PDF.

    The extractor intentionally keeps page boundaries visible. This makes it easier
    to grep generated text files and to cite page-local context while reading papers.
    """
    path = Path(pdf_path)
    reader = PdfReader(str(path))
    chunks: list[str] = []

    for index, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        chunks.append(f"\n\n--- page {index} ---\n\n{page_text.strip()}")

    return "".join(chunks).strip() + "\n"


def write_pdf_text(pdf_path: str | Path, output_path: str | Path | None = None) -> Path:
    """Extract text from ``pdf_path`` and write it to ``output_path``.

    If ``output_path`` is omitted, ``paper.pdf`` becomes ``paper.txt`` next to the
    source PDF.
    """
    source = Path(pdf_path)
    target = Path(output_path) if output_path is not None else source.with_suffix(".txt")
    target.parent.mkdir(parents=True, exist_ok=True)
    _ = target.write_text(extract_pdf_text(source), encoding="utf-8")
    return target
