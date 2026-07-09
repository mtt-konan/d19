# PDF Cache

This directory is for local literature PDF and extracted-text caches. The cache
is intentionally not tracked, except for this README and `.gitignore`.

## Naming

```text
{first-author-last-name-lowercase}-{year}-{short-keywords}.pdf
{first-author-last-name-lowercase}-{year}-{short-keywords}.txt
```

Examples:

- `peschmann-2026-quartic-reductions.pdf`
- `knaf-selder-spindler-2019-algorithm.pdf`
- `ono-1996-eulers-concordant-forms.pdf`

## Text Extraction

Use:

```bash
uv run --group literature python scripts/utility/extract_pdf_text.py docs/literature/pdfs/*.pdf
```

The extractor writes `.txt` files next to the PDFs. Those text files are also a
local cache by default; keep durable reading notes in `docs/literature/notes/`
and bibliographic metadata in `docs/literature/references.bib`.

## Git Policy

Do not track PDFs or extracted `.txt` caches here. Reasons:

1. PDFs are binary and often copyright-sensitive.
2. Extracted text can be regenerated from local PDFs.
3. Durable review material belongs in notes, not a cache directory.
4. Metadata and source URLs belong in `../references.bib` or the relevant note.

For exact sources and recommended downloads, read `../references.bib` and
`../notes/*.md`.
