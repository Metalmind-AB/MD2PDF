# MD2PDF Progress

## 2026-03-04 13:08 - Fix Table Page Breaks and Add Orientation Support

**Branch:** `feature/formatting-improvements`

### Changes Made

1. **Fixed table page-break issue across all 9 style templates**
   - Removed `page-break-inside: avoid` from `table` elements (was preventing large tables from splitting across pages, causing a gap after headings)
   - Added `page-break-inside: auto` on tables to allow cross-page breaks
   - Added `thead { display: table-header-group; }` so table headers repeat on each page
   - Added `tr { page-break-inside: avoid; }` to keep individual rows intact
   - Files modified: `technical.css`, `academic.css`, `modern.css`, `story.css`, `whitepaper.css`, `futuristic.css`, `consultancy.css`, `profiler.css`, `amazon_book.css`

2. **Added `--orientation` CLI option for portrait/landscape PDF output**
   - New `--orientation [portrait|landscape]` option on the `convert` command
   - Defaults to `None` (uses whatever the style template defines, which is portrait)
   - Wired through `_process_single_file` into the converter
   - `BaseConverter` accepts `orientation` parameter and injects `@page { size: A4 <orientation>; }` CSS override
   - Files modified: `cli.py`, `base_converter.py`

3. **Fixed landscape tables not using extra page width**
   - When `--orientation landscape` is used, the body `max-width` is now overridden to `100%`
   - All style templates had a `--max-width` (650px-950px) that capped body width below the landscape usable width (~970px)
   - The override is only applied for landscape; portrait remains unaffected
   - File modified: `base_converter.py`

## 2026-03-04 13:22 - No-wrap Headers and YAML Front Matter Support

### Changes Made

4. **Prevent table headers from wrapping**
   - Added `white-space: nowrap` to `th` in all 9 style templates
   - Ensures columns are always at least as wide as their header text (no more "N/A" splitting into "N/" and "A")

5. **YAML front matter support for per-document settings**
   - Markdown files can now include a `---` fenced YAML block at the top
   - Currently supports `orientation: landscape` (or `portrait`)
   - CLI flags override front matter values (front matter serves as default)
   - Invalid YAML or unrecognised values are gracefully ignored
   - Front matter is stripped before markdown processing
   - File modified: `base_converter.py`

### Example usage in markdown file
```yaml
---
orientation: landscape
---
# My Document
...
```

### Verification
- All 9 CSS templates validated: `page-break-inside: auto` on table, `thead` header group, `tr` avoid break
- `BaseConverter` orientation parameter tests pass (None, portrait, landscape)
- Landscape override includes `body { max-width: 100%; }`; portrait and default do not
- CLI `--help` shows `--orientation` option correctly
- Package installed in editable mode (`pip install -e .`) to use local source

## 2026-03-04 13:37 - Code Review Fixes (PR #1)

### Issues Fixed

1. **Orientation override no longer hardcodes A4** — `_get_page_size()` extracts the `size:` value from the style's `@page` rule, preserving custom sizes like `amazon_book`'s `152.4mm 228.6mm`.
2. **`batch` command now passes `--orientation`/`-O`** — the option was previously only on `convert`; now both commands support it.
3. **Custom CSS sanitized** — `</style>` sequences are stripped from front matter CSS to prevent HTML injection.
4. **Front matter regex handles EOF without trailing newline** — closing `---` at end of file now matches correctly.
5. **Duplicate `table` selector in `amazon_book.css` consolidated** — `page-break-inside: auto` merged into the main `table` block.
6. **18 new unit tests added** (`tests/test_formatting.py`) covering front matter parsing, orientation CSS injection, page size extraction, CSS sanitization, and CLI override precedence.
