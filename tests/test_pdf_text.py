"""Tests for PDF text extraction helpers."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.literature.pdf_text import extract_pdf_text, write_pdf_text


def _write_minimal_text_pdf(path: Path, text: str = "Hello PDF") -> None:
    """Write a tiny one-page PDF with extractable text."""
    stream = f"BT /F1 24 Tf 72 72 Td ({text}) Tj ET\n".encode("ascii")
    page_object = (
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] "
        + b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n"
    )
    objects = [
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        page_object,
        b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n",
        b"5 0 obj\n<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n"
        + stream
        + b"endstream\nendobj\n",
    ]

    parts = [b"%PDF-1.4\n"]
    offsets = [0]
    cursor = len(parts[0])
    for obj in objects:
        offsets.append(cursor)
        parts.append(obj)
        cursor += len(obj)

    xref_offset = cursor
    xref_lines = [b"xref\n", f"0 {len(objects) + 1}\n".encode("ascii")]
    xref_lines.append(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        xref_lines.append(f"{offset:010d} 00000 n \n".encode("ascii"))
    trailer = (
        b"trailer\n"
        + f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n".encode("ascii")
        + b"startxref\n"
        + str(xref_offset).encode("ascii")
        + b"\n%%EOF\n"
    )
    _ = path.write_bytes(b"".join(parts + xref_lines + [trailer]))


def test_extract_pdf_text_reads_page_text(tmp_path: Path) -> None:
    pdf_path = tmp_path / "sample.pdf"
    _write_minimal_text_pdf(pdf_path, "Hello PDF")

    text = extract_pdf_text(pdf_path)

    assert "Hello PDF" in text


def test_write_pdf_text_uses_txt_suffix_by_default(tmp_path: Path) -> None:
    pdf_path = tmp_path / "paper.pdf"
    _write_minimal_text_pdf(pdf_path, "Paper Text")

    out_path = write_pdf_text(pdf_path)

    assert out_path == tmp_path / "paper.txt"
    assert "Paper Text" in out_path.read_text(encoding="utf-8")
