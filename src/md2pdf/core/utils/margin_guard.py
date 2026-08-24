"""MD2PDF - Markdown to PDF Converter.

Copyright (c) 2025 MPS Metalmind AB
Licensed under the MIT License (see LICENSE file)

Margin Guard - Keeps content inside the printable area of the page.

Print media has no viewport to scroll, so an element whose *minimum* width is
larger than the page area is simply laid out past the ``@page`` margin box and
bleeds off the paper.  Table rows have a matching problem in the other
direction: ``page-break-inside: avoid`` keeps a row intact, but a row it has to
move onto a new page arrives there without the table's repeated header, and a
row too tall to fit any page costs a blank page as well.  Three mechanisms work
together:

* :data:`MARGIN_SAFETY_CSS` is always applied.  It lowers the minimum width of
  the usual offenders (long identifiers, URLs, code lines, oversized images) so
  the layout engine is able to fit them.  It only takes effect when content
  would not fit, so documents that already fit are unchanged.
* :func:`find_overflowing_tables` measures the rendered document and
  :func:`build_table_fit_css` relaxes only the tables that overflow, in
  escalating tiers.  Table cells are left out of the always-on rules because
  breaking inside a cell changes how the column widths are distributed: this
  way a table that already fits keeps its no-wrap headers and its layout.
* :func:`find_headerless_rows` and :func:`build_row_fit_css` release exactly the
  rows that lost their header from ``page-break-inside: avoid``, so every other
  row still stays intact.
"""

from typing import Any, Dict, Iterable, List, Optional, Set

# Attributes used to address an individual table or row from generated CSS.
TABLE_ID_ATTR = "data-md2pdf-table"
ROW_ID_ATTR = "data-md2pdf-row"

# Applied to every document, after the style/theme CSS.
MARGIN_SAFETY_CSS = """
/* --- md2pdf margin safety ---------------------------------------------
   Nothing may set a minimum width larger than the page area, otherwise it
   is laid out past the @page margin box.  word-break carries the guarantee:
   overflow-wrap only breaks a word that starts a line, which a long
   identifier in running text does not.  Neither takes effect until a word
   genuinely does not fit, so ordinary prose wraps exactly as before. */
body {
    overflow-wrap: anywhere;
    word-break: break-all;
}

/* Table cells opt back out: breaking inside a cell changes how the column
   widths are distributed, so it is applied per table by the fitting pass and
   only to tables measured to overflow. */
th, td {
    overflow-wrap: normal;
    word-break: normal;
}

table {
    max-width: 100%;
}

pre {
    max-width: 100%;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    word-break: break-all;
}

code, kbd, samp {
    overflow-wrap: anywhere;
    word-break: break-all;
}

img, svg {
    max-width: 100%;
    height: auto;
}
"""

# Escalating relaxations for a table that does not fit, gentlest first, so a
# table is never disturbed more than it has to be.  Tier 1 lets the header row
# wrap between words (the usual cause of an oversized table); tier 2 lets long
# words break; tier 3 gives up on proportional columns.
_FIT_TIERS: List[str] = [
    """
{selector} th {{
    white-space: normal;
    overflow: visible;
    text-overflow: clip;
}}
""",
    """
{selector} th, {selector} td {{
    overflow-wrap: anywhere;
    word-break: break-all;
}}
""",
    """
{selector} {{
    table-layout: fixed;
    font-size: 0.85em;
}}
{selector} th, {selector} td {{
    padding: 0.35em 0.45em;
}}
""",
]

MAX_FIT_TIER = len(_FIT_TIERS)

# Releasing one row can push the next one onto a page break, so fitting settles
# over a few passes.  The cap is a backstop against a document that never does.
MAX_FIT_PASSES = 6

# Letting a row break across pages is what brings the header back with it.
_ROW_FIT_CSS = """
{selector} {{
    page-break-inside: auto;
    break-inside: auto;
}}
"""

# Sub-pixel differences are rounding, not overflow.
_OVERFLOW_TOLERANCE_PX = 0.5


def add_layout_ids(html: str) -> str:
    """Give every ``<table>`` and ``<tr>`` in ``html`` a stable, addressable index.

    The indices let the fitting pass target one specific table or row without
    disturbing classes and attributes the document already carries.
    """
    return _tag_elements(_tag_elements(html, "table", TABLE_ID_ATTR), "tr", ROW_ID_ATTR)


def _tag_elements(html: str, tag: str, attr: str) -> str:
    """Number every ``<tag>`` in ``html`` with ``attr="<index>"``."""
    parts = html.split(f"<{tag}")
    if len(parts) == 1:
        return html
    tagged = [parts[0]]
    index = 0
    for part in parts[1:]:
        # Only a real tag: "<tr>" or "<tr ...". Anything else is text.
        if part[:1] in (">", " ", "\t", "\n", "\r", "/"):
            tagged.append(f' {attr}="{index}"{part}')
            index += 1
        else:
            tagged.append(part)
    return f"<{tag}".join(tagged)


def build_table_fit_css(tiers: Dict[int, Iterable[str]]) -> str:
    """Build the CSS that shrinks the tables listed per tier.

    Args:
        tiers: Mapping of tier number (1-based) to the table indices that need
            it.  A tier whose value is ``None`` applies to every table, which is
            the fallback when individual tables cannot be identified.

    Returns:
        CSS text, empty when there is nothing to fit.
    """
    blocks = []
    for tier in sorted(tiers):
        if not 1 <= tier <= MAX_FIT_TIER:
            continue
        table_ids = tiers[tier]
        if table_ids is None:
            selector = "table"
        else:
            ids = sorted(table_ids, key=_sort_key)
            if not ids:
                continue
            selector = ", ".join(f'table[{TABLE_ID_ATTR}="{i}"]' for i in ids)
        blocks.append(_FIT_TIERS[tier - 1].format(selector=selector))
    return "\n".join(blocks)


def build_row_fit_css(row_ids: Iterable[str]) -> str:
    """Build the CSS that lets the listed rows break across pages.

    Returns:
        CSS text, empty when there is no row to release.
    """
    ids = sorted(row_ids, key=_sort_key)
    if not ids:
        return ""
    selector = ", ".join(f'tr[{ROW_ID_ATTR}="{i}"]' for i in ids)
    return _ROW_FIT_CSS.format(selector=selector)


def _sort_key(element_id: str):
    """Sort numeric ids numerically, anything else lexically."""
    text = str(element_id)
    return (0, int(text), "") if text.isdigit() else (1, 0, text)


def find_overflowing_tables(document) -> Optional[Dict[str, float]]:
    """Measure which tables extend past the page area of a rendered document.

    Args:
        document: A rendered ``weasyprint.Document``.

    Returns:
        Mapping of table index to its worst overflow in CSS pixels, empty when
        everything fits, or ``None`` when the layout tree could not be
        inspected (WeasyPrint internals changed) and the caller should fall
        back to treating every table as suspect.
    """
    overflow: Dict[str, float] = {}
    unidentified = 0.0

    try:
        for page in document.pages:
            page_box = getattr(page, "_page_box", None)
            if page_box is None:
                return None
            left_limit = page_box.content_box_x()
            right_limit = left_limit + page_box.width

            # Cell content can stick out of a table that is itself in bounds,
            # so everything inside a table is measured, not just the table box.
            for box, table_id in _walk_tables(page_box, None, False):
                box_left = box.border_box_x()
                box_right = box_left + box.border_width()
                worst = max(left_limit - box_left, box_right - right_limit)
                if worst <= _OVERFLOW_TOLERANCE_PX:
                    continue
                if table_id is None:
                    unidentified = max(unidentified, worst)
                else:
                    overflow[table_id] = max(overflow.get(table_id, 0.0), worst)
    except (AttributeError, TypeError):
        return None

    if unidentified and not overflow:
        return None
    return overflow


def find_headerless_rows(document) -> Optional[Set[str]]:
    """Find rows laid out on a page that does not repeat their table's header.

    ``thead { display: table-header-group }`` is supposed to reprint the header
    on every page a table covers, but WeasyPrint drops it whenever
    ``page-break-inside: avoid`` is what moved a row onto the page — either
    because the row did not fit in what was left of the previous page, or
    because it is taller than a whole page and had to be split regardless.  The
    result reads as a table that starts mid-page with no header.  Releasing just
    those rows restores the header.

    Args:
        document: A rendered ``weasyprint.Document``.

    Returns:
        The indices of the rows to release, empty when every page carries its
        header, or ``None`` when the layout tree could not be inspected.
    """
    pages: List[Dict[Optional[str], Dict[str, Any]]] = []
    tables_with_header: Set[Optional[str]] = set()

    try:
        for page in document.pages:
            page_box = getattr(page, "_page_box", None)
            if page_box is None:
                return None

            fragments: Dict[Optional[str], Dict[str, Any]] = {}
            for box, table_id in _walk_tables(page_box, None, False):
                fragment = fragments.setdefault(
                    table_id, {"header": False, "rows": set()}
                )
                tag = getattr(box, "element_tag", None)
                if tag == "th":
                    fragment["header"] = True
                    tables_with_header.add(table_id)
                elif tag == "tr":
                    element = getattr(box, "element", None)
                    row_id = element.get(ROW_ID_ATTR) if element is not None else None
                    if row_id is not None:
                        fragment["rows"].add(row_id)
            pages.append(fragments)
    except (AttributeError, TypeError):
        return None

    orphaned: Set[str] = set()
    for fragments in pages:
        for table_id, fragment in fragments.items():
            # A table that never shows a header has none to repeat.
            if table_id not in tables_with_header:
                continue
            if fragment["rows"] and not fragment["header"]:
                orphaned |= fragment["rows"]
    return orphaned


def _walk_tables(box, table_id: Optional[str], in_table: bool) -> Iterable:
    """Yield ``(box, table_id)`` for every table box and everything inside it.

    Boxes outside any table are skipped: they are kept in bounds by
    :data:`MARGIN_SAFETY_CSS`, not by the per-table fitting.  A ``table_id`` of
    ``None`` means the table carries no index and cannot be targeted.
    """
    if not in_table and getattr(box, "element_tag", None) == "table":
        in_table = True
        element = getattr(box, "element", None)
        table_id = element.get(TABLE_ID_ATTR) if element is not None else None
    if in_table:
        yield box, table_id
    for child in getattr(box, "children", ()) or ():
        yield from _walk_tables(child, table_id, in_table)


def px_to_mm(pixels: float) -> float:
    """Convert CSS pixels (WeasyPrint's layout unit) to millimetres."""
    return pixels / 96.0 * 25.4


def describe_overflow(overflow: Optional[Dict[str, float]]) -> str:
    """Human-readable summary of an overflow measurement, for progress output."""
    if not overflow:
        return "all tables" if overflow is None else "no tables"
    worst = max(overflow.values())
    count = len(overflow)
    noun = "table" if count == 1 else "tables"
    return f"{count} {noun} (worst overflow {px_to_mm(worst):.0f} mm)"
