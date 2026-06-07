# TuJin PDF

English | [中文](README.md)

![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-a8854a)
![PDF](https://img.shields.io/badge/Output-A4%20PDF-1f1a16)
![HTML](https://img.shields.io/badge/Source-HTML-f4ede1)
![Style](https://img.shields.io/badge/Style-Earthy%20Gold-a8854a)

![TuJin PDF banner](assets/banner.svg)

Turn existing documents into polished A4 magazine-style PDFs with a restrained earthy-gold visual system.

TuJin PDF focuses on one job: **making existing content suitable for delivery, archive, and presentation**. By default, it preserves the original content, numbers, dates, names, conclusions, and business wording. It does not rewrite content unless the user explicitly asks for it.

```text
Read content → Build A4 HTML → Render PDF in browser → Check layout/fidelity → Deliver HTML + PDF
```

![TuJin PDF animated preview](assets/hero.gif)

---

## Use Cases

- Project summaries and delivery archives
- Client confirmation documents
- Reports, proposals, quotations, and review notes
- Content extracted from Markdown, TXT, HTML, DOCX, PDF, or XLSX files
- Text pasted directly into a conversation
- Chinese business documents that need to feel refined without becoming decorative

## Not For

- Heavy rewriting or changing business positions
- Pixel-perfect reconstruction of an existing PDF
- Public publishing, client sending, or external uploading before content confirmation
- Highly similar imitation of a third-party commercial template

---

## Visual System

| Token | Purpose | Value |
|---|---|---|
| Warm paper | Page background | `#f4ede1` |
| Secondary surface | Light blocks | `#efe6d6` |
| Primary text | Headings and body | `#1f1a16` |
| Secondary text | Supporting copy | `#4a3f33` |
| Note text | Footers and notes | `#8a7a68` |
| Gold accent | Lines, numbers, highlights | `#a8854a` |

Layout principles:

- A4 pages, `210mm x 297mm`
- A cover page with source, document type, title, and key metadata
- Section-based body layout with headings, body copy, tables, and information blocks
- Center short table cells; left-align long text cells
- Keep table headers centered
- Use whitespace and rhythm instead of decorative clutter

---

## Installation

Place this directory under a runtime that supports Agent Skills:

```bash
~/.codex/skills/tujinpdf/
```

Or use a runtime that supports GitHub-based skill installation:

```bash
npx skills add https://github.com/judeyang/judeyang-skills/tree/main/tujinpdf
```

---

## Example Prompts

```text
Use TuJin PDF to turn this project summary into a PDF.
Restyle this Markdown document as an earthy gold magazine-style PDF.
Create a client confirmation archive PDF using the TuJin PDF style.
Turn the contents of this Excel file into a TuJin PDF report.
```

---

## Outputs

By default, the skill produces:

- an A4 HTML source file
- a matching PDF file
- an optional preview screenshot for layout review

The HTML source must be kept so later revisions can update the existing layout instead of recreating it from scratch.

The skill does not overwrite old versions by default. Use filenames like:

```text
document_topic_TuJinPDF_v01.html
document_topic_TuJinPDF_v01.pdf
document_topic_TuJinPDF_v01_preview.png
```

---

## Workflow

![Workflow](assets/workflow.svg)

1. **Read source content**: confirm the file path, target reader, and whether this is layout-only.
2. **Extract structure**: identify title, date, sections, tables, lists, and key numbers.
3. **Generate HTML**: use A4 pages, earthy-gold CSS variables, cover, sections, and table styles.
4. **Render PDF**: use a real browser to produce the PDF and preview screenshot.
5. **Quality check**: inspect overflow, overlap, pagination, tables, and source fidelity.
6. **Delivery note**: report generated files, whether content changed, and remaining risks.

---

## Rendering

The skill includes a browser-based rendering script:

```bash
node scripts/render-html-pdf.mjs input.html output.pdf --screenshot preview.png
```

The script prefers an available Puppeteer runtime. If Puppeteer's bundled Chrome is missing, it attempts to use the local Google Chrome installation.

## Validation And Regression

The new regression assets support Darwin or manual review:

- `test-prompts.json`: covers new layout generation, existing-layout repair, and sensitive commercial content.
- `examples/`: contains a minimal sample input and expected output notes.
- `scripts/validate-output.mjs`: checks HTML/PDF/preview files, the A4 page contract, placeholders, and debug artifacts.

```bash
node scripts/validate-output.mjs output.html output.pdf preview.png
```

---

## Quality Gate

![Quality gate](assets/quality-gate.svg)

Before delivery, verify that:

- the PDF opens correctly
- pages are A4
- the cover has no unrelated decoration
- headings, body text, and tables have clear hierarchy
- text does not overflow, overlap, or get clipped
- there are no abnormal blank areas
- short table cells are centered and long text cells are left-aligned
- source content was not silently rewritten
- both the HTML source and PDF are kept
- filenames use matching version numbers

---

## 🔴 Checkpoints

Pause for confirmation before continuing when:

- the user asks to rewrite, remove, hide, or reinterpret important facts, numbers, prices, dates, responsibilities, or client feedback
- the user asks to overwrite an existing HTML/PDF version
- the source contains contracts, quotations, invoices, financial, legal, privacy, account, payment, or customer-sensitive data
- the file must be uploaded to an external online service, publicly published, or sent to a client

---

## Anti-Patterns

- Do not deliver only the PDF without the HTML source
- Do not silently rewrite source content
- Do not hand-build complex PDFs with ReportLab
- Do not nest cards inside cards or add meaningless decoration
- Do not leak FatePaw, fortune-telling, or unrelated business content into ordinary documents
- Do not claim completion before checking the PDF

---

## Structure

```text
tujinpdf/
├── SKILL.md
├── README.md
├── README_EN.md
├── agents/
│   └── openai.yaml
├── examples/
│   ├── expected-output-notes.md
│   └── sample-report.md
├── references/
│   └── fatepaw-style-notes.md
├── templates/
│   └── base-a4.html
├── scripts/
│   ├── render-html-pdf.mjs
│   └── validate-output.mjs
└── test-prompts.json
```

---

## License

MIT License. See [LICENSE](LICENSE).
