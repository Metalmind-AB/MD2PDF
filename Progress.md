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

### Verification
- All 9 CSS templates validated: `page-break-inside: auto` on table, `thead` header group, `tr` avoid break
- `BaseConverter` orientation parameter tests pass (None, portrait, landscape)
- CLI `--help` shows `--orientation` option correctly
- WeasyPrint GTK libraries not available in terminal session; full PDF generation test deferred
