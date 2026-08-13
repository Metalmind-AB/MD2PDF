"""MD2PDF - Markdown to PDF Converter.

Copyright (c) 2025 MPS Metalmind AB
Licensed under the MIT License (see LICENSE file)

Margin Guard - Keeps content inside the printable area of the page.

Print media has no viewport to scroll, so an element whose *minimum* width is
larger than the page area is simply laid out past the ``@page`` margin box and
bleeds off the paper.  The two mechanisms here work together:

* :data:`MARGIN_SAFETY_CSS` is always applied.  It lowers the minimum width of
  the usual offenders (long identifiers, URLs, code lines, oversized images) so
  the layout engine is able to fit them.  It only takes effect when content
  would not fit, so documents that already fit are unchanged.
* :func:`find_overflowing_tables` measures the rendered document and
  :func:`build_table_fit_css` relaxes only the tables that overflow, in
  escalating tiers.  Table cells are left out of the always-on rules because
  breaking inside a cell changes how the column widths are distributed: this
  way a table that already fits keeps its no-wrap headers and its layout.
"""

from typing import Dict, Iterable, List, Optional

# Attribute used to address an individual table from generated CSS.
TABLE_ID_ATTR = "data-md2pdf-table"

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

# Sub-pixel differences are rounding, not overflow.
_OVERFLOW_TOLERANCE_PX = 0.5


def tag_tables(html: str) -> str:
    """Give every ``<table>`` in ``html`` a stable, addressable index.

    The index lets :func:`build_table_fit_css` target one specific table
    without disturbing classes the document already carries.
    """
    parts = html.split("<table")
    if len(parts) == 1:
        return html
    tagged = [parts[0]]
    for index, part in enumerate(parts[1:]):
        # Only a real tag: "<table>" or "<table ...". Anything else is text.
        if part[:1] in (">", " ", "\t", "\n", "\r", "/"):
            tagged.append(f' {TABLE_ID_ATTR}="{index}"{part}')
        else:
            tagged.append(part)
    return "<table".join(tagged)


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


def _sort_key(table_id: str):
    """Sort numeric table ids numerically, anything else lexically."""
    return (0, int(table_id), "") if str(table_id).isdigit() else (1, 0, str(table_id))


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
