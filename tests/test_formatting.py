# Copyright (c) 2025 MPS Metalmind AB
# Licensed under the MIT License (see LICENSE file)

"""
Tests for formatting improvements: front matter parsing, orientation support,
custom CSS injection, and keeping content inside the page margins.
"""

from pathlib import Path

import pytest

from md2pdf.core.converters.base_converter import BaseConverter
from md2pdf.core.utils import margin_guard


class TestFrontMatterExtraction:
    """Test YAML front matter parsing from markdown content."""

    @pytest.mark.unit
    def test_extract_orientation(self, temp_dir):
        md = temp_dir / "test.md"
        md.write_text("---\norientation: landscape\n---\n# Hello\n")
        conv = BaseConverter(input_file=str(md))
        content = conv._read_markdown_content()
        assert conv.orientation == "landscape"
        assert "---" not in content
        assert "# Hello" in content

    @pytest.mark.unit
    def test_extract_portrait(self, temp_dir):
        md = temp_dir / "test.md"
        md.write_text("---\norientation: portrait\n---\n# Hello\n")
        conv = BaseConverter(input_file=str(md))
        conv._read_markdown_content()
        assert conv.orientation == "portrait"

    @pytest.mark.unit
    def test_cli_orientation_overrides_front_matter(self, temp_dir):
        md = temp_dir / "test.md"
        md.write_text("---\norientation: landscape\n---\n# Hello\n")
        conv = BaseConverter(input_file=str(md), orientation="portrait")
        conv._read_markdown_content()
        assert conv.orientation == "portrait"

    @pytest.mark.unit
    def test_no_front_matter(self, temp_dir):
        md = temp_dir / "test.md"
        md.write_text("# Hello\n\nNo front matter here.\n")
        conv = BaseConverter(input_file=str(md))
        content = conv._read_markdown_content()
        assert conv.orientation is None
        assert "# Hello" in content

    @pytest.mark.unit
    def test_invalid_yaml_ignored(self, temp_dir):
        md = temp_dir / "test.md"
        md.write_text("---\n: broken [[\n---\n# Hello\n")
        conv = BaseConverter(input_file=str(md))
        content = conv._read_markdown_content()
        assert conv.orientation is None
        assert "---" in content

    @pytest.mark.unit
    def test_invalid_orientation_value_ignored(self, temp_dir):
        md = temp_dir / "test.md"
        md.write_text("---\norientation: diagonal\n---\n# Hello\n")
        conv = BaseConverter(input_file=str(md))
        conv._read_markdown_content()
        assert conv.orientation is None

    @pytest.mark.unit
    def test_closing_fence_without_trailing_newline(self, temp_dir):
        md = temp_dir / "test.md"
        md.write_text("---\norientation: landscape\n---")
        conv = BaseConverter(input_file=str(md))
        conv._read_markdown_content()
        assert conv.orientation == "landscape"

    @pytest.mark.unit
    def test_custom_css_extraction(self, temp_dir):
        md = temp_dir / "test.md"
        md.write_text("---\ncss: |\n  th:last-child { width: 20%; }\n---\n# Hello\n")
        conv = BaseConverter(input_file=str(md))
        conv._read_markdown_content()
        assert "width: 20%" in conv.custom_css

    @pytest.mark.unit
    def test_custom_css_style_tag_sanitized(self, temp_dir):
        md = temp_dir / "test.md"
        md.write_text(
            "---\ncss: 'body{} </style><script>alert(1)</script>'\n---\n# X\n"
        )
        conv = BaseConverter(input_file=str(md))
        conv._read_markdown_content()
        assert "</style>" not in conv.custom_css


class TestOrientationCSS:
    """Test orientation CSS injection in HTML output."""

    @pytest.mark.unit
    def test_landscape_injects_page_and_maxwidth(self, sample_markdown_file):
        conv = BaseConverter(
            input_file=str(sample_markdown_file), orientation="landscape"
        )
        html = conv._create_html_document("<p>test</p>")
        assert "size: A4 landscape" in html
        assert "body { max-width: 100%; }" in html

    @pytest.mark.unit
    def test_portrait_injects_page_without_maxwidth(self, sample_markdown_file):
        conv = BaseConverter(
            input_file=str(sample_markdown_file), orientation="portrait"
        )
        html = conv._create_html_document("<p>test</p>")
        assert "size: A4 portrait" in html
        assert "body { max-width: 100%; }" not in html

    @pytest.mark.unit
    def test_no_orientation_no_override(self, sample_markdown_file):
        conv = BaseConverter(input_file=str(sample_markdown_file))
        html = conv._create_html_document("<p>test</p>")
        # The orientation_css variable should be empty, so no extra @page injected
        # beyond what the style template already defines
        assert "body { max-width: 100%; }" not in html

    @pytest.mark.unit
    def test_preserves_custom_page_size_landscape(self, sample_markdown_file):
        """Landscape with custom dims should swap w/h."""
        conv = BaseConverter(
            input_file=str(sample_markdown_file),
            style="amazon_book",
            orientation="landscape",
        )
        html = conv._create_html_document("<p>test</p>")
        # Custom dims must be swapped for WeasyPrint (landscape keyword is ignored)
        assert "228.6mm 152.4mm" in html
        assert "body { max-width: 100%; }" in html

    @pytest.mark.unit
    def test_preserves_custom_page_size_portrait(self, sample_markdown_file):
        """Portrait with custom dimensions should keep original order."""
        conv = BaseConverter(
            input_file=str(sample_markdown_file),
            style="amazon_book",
            orientation="portrait",
        )
        html = conv._create_html_document("<p>test</p>")
        assert "152.4mm 228.6mm" in html
        assert "body { max-width: 100%; }" not in html

    @pytest.mark.unit
    def test_custom_css_appears_in_html(self, temp_dir):
        md = temp_dir / "test.md"
        md.write_text("---\ncss: |\n  .custom { color: red; }\n---\n# Hello\n")
        conv = BaseConverter(input_file=str(md))
        content = conv._read_markdown_content()
        html = conv._create_html_document(conv._process_markdown(content))
        assert ".custom { color: red; }" in html


class TestPageSizeExtraction:
    """Test _get_page_size helper."""

    @pytest.mark.unit
    def test_extracts_a4(self, sample_markdown_file):
        conv = BaseConverter(input_file=str(sample_markdown_file), style="technical")
        assert conv._get_page_size() == "A4"

    @pytest.mark.unit
    def test_extracts_custom_size(self, sample_markdown_file):
        conv = BaseConverter(input_file=str(sample_markdown_file), style="amazon_book")
        assert conv._get_page_size() == "152.4mm 228.6mm"

    @pytest.mark.unit
    def test_strips_existing_orientation_keyword(self, sample_markdown_file):
        conv = BaseConverter(input_file=str(sample_markdown_file))
        conv.css_styles = "@page { size: A4 portrait; }"
        assert conv._get_page_size() == "A4"

    @pytest.mark.unit
    def test_fallback_when_no_page_rule(self, sample_markdown_file):
        conv = BaseConverter(input_file=str(sample_markdown_file))
        conv.css_styles = "body { color: red; }"
        assert conv._get_page_size() == "A4"


WIDE_TABLE_MARKDOWN = """# Wide

| FEATURE | CUSTOMER URS IMPACT | CUSTOMER TENANT CONFIGURATION CHANGE | \
CUSTOMER-SIDE RE-TEST EVIDENCE REQUIRED | DEVIATION AWARENESS |
|---|---|---|---|---|
| Validation Dossier download | None. New CQD_ADMIN-only capability that does \
not change any pre-existing user-facing behaviour. | None required at all. | \
Configuration evidence that the CQD_ADMIN role assignment is set as intended. | \
Documented at `RR-MM-CQD-2026-013` §5.3. |
"""


class TestTableTagging:
    """Every table gets an index so the fitting pass can address it."""

    @pytest.mark.unit
    def test_tables_are_indexed(self):
        html = "<table><tr><td>a</td></tr></table><p>x</p><table class='k'></table>"
        tagged = margin_guard.add_layout_ids(html)
        assert '<table data-md2pdf-table="0">' in tagged
        assert '<table data-md2pdf-table="1" class=\'k\'>' in tagged

    @pytest.mark.unit
    def test_leaves_other_content_alone(self):
        html = "<p>a &lt;tablet&gt; is not a table</p>"
        assert margin_guard.add_layout_ids(html) == html

    @pytest.mark.unit
    def test_document_without_tables_unchanged(self):
        html = "<h1>Hi</h1><p>No tables here.</p>"
        assert margin_guard.add_layout_ids(html) == html

    @pytest.mark.unit
    def test_rows_are_indexed_independently_of_tables(self):
        html = "<table><tr><td>a</td></tr><tr><td>b</td></tr></table>"
        tagged = margin_guard.add_layout_ids(html)
        assert '<tr data-md2pdf-row="0">' in tagged
        assert '<tr data-md2pdf-row="1">' in tagged
        assert tagged.count("</tr>") == 2

    @pytest.mark.unit
    def test_tagging_applied_in_html_document(self, temp_dir):
        md = temp_dir / "t.md"
        md.write_text("| A | B |\n|---|---|\n| 1 | 2 |\n")
        conv = BaseConverter(input_file=str(md))
        content = conv._read_markdown_content()
        html = conv._create_html_document(conv._process_markdown(content))
        assert 'data-md2pdf-table="0"' in html


class TestMarginSafetyCSS:
    """The always-on rules that keep non-table content inside the margins."""

    @pytest.mark.unit
    def test_safety_css_is_injected(self, sample_markdown_file):
        conv = BaseConverter(input_file=str(sample_markdown_file))
        html = conv._create_html_document("<p>x</p>")
        assert "md2pdf margin safety" in html
        assert "white-space: pre-wrap" in html

    @pytest.mark.unit
    def test_table_cells_opt_out_of_breaking(self, sample_markdown_file):
        """Cells are relaxed per table by the fitter, not globally."""
        conv = BaseConverter(input_file=str(sample_markdown_file))
        html = conv._create_html_document("<p>x</p>")
        assert "th, td {\n    overflow-wrap: normal;" in html

    @pytest.mark.unit
    def test_extra_css_comes_before_custom_css(self, temp_dir):
        md = temp_dir / "t.md"
        md.write_text("---\ncss: '.mine { color: red; }'\n---\n# H\n")
        conv = BaseConverter(input_file=str(md))
        conv._read_markdown_content()
        html = conv._create_html_document("<p>x</p>", extra_css=".fit { color: blue; }")
        assert html.index(".fit { color: blue; }") < html.index(".mine { color: red; }")


class TestTableFitCSS:
    """CSS generated for the tables measured to overflow."""

    @pytest.mark.unit
    def test_targets_only_the_named_tables(self):
        css = margin_guard.build_table_fit_css({1: {"2"}})
        assert 'table[data-md2pdf-table="2"] th' in css
        assert 'table[data-md2pdf-table="0"]' not in css
        assert "white-space: normal" in css

    @pytest.mark.unit
    def test_tiers_escalate_in_order(self):
        css = margin_guard.build_table_fit_css({1: {"0"}, 2: {"0"}, 3: {"0"}})
        assert (
            css.index("white-space: normal")
            < css.index("word-break: break-all")
            < css.index("table-layout: fixed")
        )

    @pytest.mark.unit
    def test_first_tier_only_wraps_headers(self):
        """The gentlest tier must not start breaking words."""
        css = margin_guard.build_table_fit_css({1: {"0"}})
        assert "white-space: normal" in css
        assert "word-break" not in css
        assert "table-layout" not in css

    @pytest.mark.unit
    def test_ids_are_sorted_numerically(self):
        css = margin_guard.build_table_fit_css({1: {"10", "2"}})
        assert css.index('"2"') < css.index('"10"')

    @pytest.mark.unit
    def test_none_falls_back_to_every_table(self):
        css = margin_guard.build_table_fit_css({1: None})
        assert "table th {" in css
        assert "data-md2pdf-table" not in css

    @pytest.mark.unit
    def test_nothing_to_fit_is_empty(self):
        assert margin_guard.build_table_fit_css({}) == ""
        assert margin_guard.build_table_fit_css({1: set()}) == ""


class _FakeElement:
    def __init__(self, element_id=None, attr=None):
        self._element_id = element_id
        self._attr = attr

    def get(self, name):
        return self._element_id if name == self._attr else None


class _FakeBox:
    """Minimal stand-in for a WeasyPrint layout box."""

    def __init__(
        self,
        tag=None,
        x=0.0,
        width=0.0,
        children=(),
        table_id=None,
        row_id=None,
    ):
        self.element_tag = tag
        self.children = children
        self.width = width
        self._x = x
        self.element = None
        if tag == "table":
            self.element = _FakeElement(table_id, margin_guard.TABLE_ID_ATTR)
        elif tag == "tr":
            self.element = _FakeElement(row_id, margin_guard.ROW_ID_ATTR)

    def border_box_x(self):
        return self._x

    def border_width(self):
        return self.width

    def content_box_x(self):
        return self._x


class _FakeDocument:
    def __init__(self, *roots):
        self.pages = [type("Page", (), {"_page_box": root})() for root in roots]


def _page(children, x=50.0, width=500.0):
    """A page area from x to x+width holding the given boxes."""
    return _FakeDocument(_FakeBox(tag="page", x=x, width=width, children=children))


def _pages(*page_children, width=500.0):
    """Several pages, each holding the given boxes."""
    return _FakeDocument(
        *[
            _FakeBox(tag="page", x=50.0, width=width, children=children)
            for children in page_children
        ]
    )


class TestOverflowMeasurement:
    """Measuring which tables stick out of the page area."""

    @pytest.mark.unit
    def test_table_inside_the_page_area(self):
        table = _FakeBox(tag="table", x=60, width=400, table_id="0")
        assert margin_guard.find_overflowing_tables(_page([table])) == {}

    @pytest.mark.unit
    def test_table_past_the_right_edge(self):
        table = _FakeBox(tag="table", x=60, width=600, table_id="0")
        overflow = margin_guard.find_overflowing_tables(_page([table]))
        assert overflow == {"0": pytest.approx(110.0)}

    @pytest.mark.unit
    def test_cell_content_sticking_out_counts(self):
        cell = _FakeBox(tag="td", x=500, width=200)
        table = _FakeBox(tag="table", x=60, width=400, children=(cell,), table_id="3")
        overflow = margin_guard.find_overflowing_tables(_page([table]))
        assert overflow == {"3": pytest.approx(150.0)}

    @pytest.mark.unit
    def test_content_outside_tables_is_ignored(self):
        stray = _FakeBox(tag="pre", x=60, width=900)
        assert margin_guard.find_overflowing_tables(_page([stray])) == {}

    @pytest.mark.unit
    def test_untaggable_table_reports_unknown(self):
        table = _FakeBox(tag="table", x=60, width=600)
        assert margin_guard.find_overflowing_tables(_page([table])) is None

    @pytest.mark.unit
    def test_unreadable_layout_tree_reports_unknown(self):
        document = type("Doc", (), {"pages": [object()]})()
        assert margin_guard.find_overflowing_tables(document) is None

    @pytest.mark.unit
    def test_sub_pixel_overflow_is_ignored(self):
        table = _FakeBox(tag="table", x=60, width=490.4, table_id="0")
        assert margin_guard.find_overflowing_tables(_page([table])) == {}


class TestRowFitCSS:
    """CSS generated for rows that cannot be kept on one page."""

    @pytest.mark.unit
    def test_releases_only_the_named_rows(self):
        css = margin_guard.build_row_fit_css({"3"})
        assert 'tr[data-md2pdf-row="3"]' in css
        assert "page-break-inside: auto" in css
        assert 'tr[data-md2pdf-row="0"]' not in css

    @pytest.mark.unit
    def test_ids_are_sorted_numerically(self):
        css = margin_guard.build_row_fit_css({"10", "2"})
        assert css.index('"2"') < css.index('"10"')

    @pytest.mark.unit
    def test_nothing_to_release_is_empty(self):
        assert margin_guard.build_row_fit_css(set()) == ""


def _table(table_id, rows, header=False):
    """A table fragment holding the given row ids, optionally with its header."""
    children = []
    if header:
        children.append(_FakeBox(tag="th"))
    children.extend(_FakeBox(tag="tr", row_id=row_id) for row_id in rows)
    return _FakeBox(tag="table", table_id=table_id, children=tuple(children))


class TestHeaderlessRowMeasurement:
    """Finding rows laid out on a page that lost the repeated table header."""

    @pytest.mark.unit
    def test_page_with_its_header_is_fine(self):
        page = _page([_table("0", ["0", "1"], header=True)])
        assert margin_guard.find_headerless_rows(page) == set()

    @pytest.mark.unit
    def test_continuation_page_without_the_header(self):
        document = _pages(
            [_table("0", ["0"], header=True)],
            [_table("0", ["1", "2"])],
        )
        assert margin_guard.find_headerless_rows(document) == {"1", "2"}

    @pytest.mark.unit
    def test_table_that_never_has_a_header_is_left_alone(self):
        """Nothing to repeat, so nothing to repair."""
        document = _pages([_table("0", ["0"])], [_table("0", ["1"])])
        assert margin_guard.find_headerless_rows(document) == set()

    @pytest.mark.unit
    def test_other_tables_on_the_page_do_not_confuse_it(self):
        document = _pages(
            [_table("0", ["0"], header=True), _table("1", ["5"], header=True)],
            [_table("0", ["1"], header=True), _table("1", ["6"])],
        )
        assert margin_guard.find_headerless_rows(document) == {"6"}

    @pytest.mark.unit
    def test_untagged_row_cannot_be_released(self):
        document = _pages(
            [_table("0", [], header=True)],
            [_FakeBox(tag="table", table_id="0", children=(_FakeBox(tag="tr"),))],
        )
        assert margin_guard.find_headerless_rows(document) == set()

    @pytest.mark.unit
    def test_unreadable_layout_tree_reports_unknown(self):
        document = type("Doc", (), {"pages": [object()]})()
        assert margin_guard.find_headerless_rows(document) is None


class TestMarginsRespected:
    """End-to-end: a table too wide for the page is fitted onto it."""

    @pytest.mark.integration
    @pytest.mark.parametrize("style", ["technical", "consultancy", "academic"])
    def test_wide_table_is_brought_inside_the_margins(self, temp_dir, style):
        pytest.importorskip("weasyprint")
        from md2pdf.core.converters.pdf_converter import PDFConverter

        md = temp_dir / "wide.md"
        md.write_text(WIDE_TABLE_MARKDOWN, encoding="utf-8")
        conv = PDFConverter(
            input_file=str(md), output_file=str(temp_dir / "wide.pdf"), style=style
        )
        body = conv._read_markdown_content()
        html = conv._process_markdown(body)

        unfitted = conv._render(html, str(temp_dir) + "/", "")
        assert margin_guard.find_overflowing_tables(unfitted), (
            "test fixture is no longer wide enough to overflow the page"
        )

        fitted = conv._render_fitted(html, str(temp_dir) + "/")
        assert margin_guard.find_overflowing_tables(fitted) == {}

    @pytest.mark.integration
    def test_narrow_table_keeps_its_no_wrap_headers(self, temp_dir):
        pytest.importorskip("weasyprint")
        from md2pdf.core.converters.pdf_converter import PDFConverter

        md = temp_dir / "narrow.md"
        md.write_text("| Document | Version | Status |\n|---|---|---|\n"
                      "| Plan | 1.0 | Signed |\n", encoding="utf-8")
        conv = PDFConverter(
            input_file=str(md), output_file=str(temp_dir / "narrow.pdf")
        )
        html = conv._process_markdown(conv._read_markdown_content())
        document = conv._render_fitted(html, str(temp_dir) + "/")

        headers = [
            box
            for box, _ in margin_guard._walk_tables(
                document.pages[0]._page_box, None, False
            )
            if getattr(box, "element_tag", None) == "th"
        ]
        assert headers
        assert all(box.style["white_space"] == "nowrap" for box in headers)


class TestOversizedRowsFitThePage:
    """A row too tall for one page must not cost a blank page or the header."""

    @staticmethod
    def _document(temp_dir, name):
        from md2pdf.core.converters.pdf_converter import PDFConverter

        md = temp_dir / f"{name}.md"
        md.write_text(
            "# Manifest\n\n| ID | DETAIL |\n|---|---|\n| 1 | "
            + ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 200)
            + " |\n| 2 | short |\n",
            encoding="utf-8",
        )
        conv = PDFConverter(
            input_file=str(md), output_file=str(temp_dir / f"{name}.pdf")
        )
        html = conv._process_markdown(conv._read_markdown_content())
        return conv, html

    @staticmethod
    def _header_counts(document):
        """Header cells rendered on each page."""
        counts = []
        for page in document.pages:
            counts.append(
                sum(
                    1
                    for box, _ in margin_guard._walk_tables(
                        page._page_box, None, False
                    )
                    if getattr(box, "element_tag", None) == "th"
                )
            )
        return counts

    @pytest.mark.integration
    def test_the_defect_is_present_without_the_repair(self, temp_dir):
        pytest.importorskip("weasyprint")
        conv, html = self._document(temp_dir, "tall")
        unfitted = conv._render(html, str(temp_dir) + "/", "")
        assert margin_guard.find_headerless_rows(unfitted), (
            "test fixture no longer reproduces the dropped table header"
        )

    @pytest.mark.integration
    def test_header_repeats_on_every_page_of_the_row(self, temp_dir):
        pytest.importorskip("weasyprint")
        conv, html = self._document(temp_dir, "tall")
        document = conv._render_fitted(html, str(temp_dir) + "/")
        counts = self._header_counts(document)
        assert len(counts) > 1, "fixture should span several pages"
        assert all(counts), f"a page lost the repeated table header: {counts}"

    @pytest.mark.integration
    def test_no_blank_page_before_the_row(self, temp_dir):
        pytest.importorskip("weasyprint")
        conv, html = self._document(temp_dir, "tall")
        document = conv._render_fitted(html, str(temp_dir) + "/")
        first_page_cells = [
            box
            for box, _ in margin_guard._walk_tables(
                document.pages[0]._page_box, None, False
            )
            if getattr(box, "element_tag", None) == "td"
        ]
        assert first_page_cells, "the table was pushed off the page it starts on"
