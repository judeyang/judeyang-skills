# 土金 PDF Style Notes

This reference is only a visual style guide. It is not a business workflow.

## Purpose

Turn any source document into an A4 PDF with:

- earthy-gold palette;
- magazine-like page rhythm;
- refined Chinese typography;
- clear hierarchy;
- restrained lines and borders;
- thoughtful whitespace.

## Palette

- Paper: `#f4ede1`
- Paper soft: `#efe6d6`
- Ink: `#1f1a16`
- Ink soft: `#4a3f33`
- Taupe: `#8a7a68`
- Brass: `#a8854a`
- Fine line: `rgba(31,26,22,0.10)` or `rgba(31,26,22,0.18)`

## Page Structure

Use fixed A4 pages:

```css
@page { size: A4; margin: 0; }
.page {
  width: 210mm;
  height: 297mm;
  padding: 22mm 26mm 26mm;
  background: var(--paper);
  page-break-after: always;
  overflow: hidden;
}
```

## Cover

Use a clean cover:

- brand/source;
- document type;
- title;
- subtitle if present;
- 2-4 metadata items;
- one key metric only if the source has one;
- small footer line.

Avoid invented diagrams, decorative radar charts, random quotes, and placeholder labels.

## Tables

- Header: centered, taupe, light letter spacing.
- Short cells: centered.
- Long cells: left aligned.
- Use hairline borders only.
- Avoid heavy fills.

## Typography

Use serif Chinese for body and headings. Prefer:

- `Noto Serif SC`
- fallback serif fonts
- `Cormorant Garamond` or `Tenor Sans` only for Latin accents

Do not use oversized hero typography inside compact panels or tables.
