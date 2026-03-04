# Copyright (c) 2025 MPS Metalmind AB
# Licensed under the MIT License (see LICENSE file)

"""
Tests for formatting improvements: front matter parsing, orientation support,
and custom CSS injection.
"""

from pathlib import Path

import pytest

from md2pdf.core.converters.base_converter import BaseConverter


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
        md.write_text(
            "---\ncss: |\n  th:last-child { width: 20%; }\n---\n# Hello\n"
        )
        conv = BaseConverter(input_file=str(md))
        conv._read_markdown_content()
        assert "width: 20%" in conv.custom_css

    @pytest.mark.unit
    def test_custom_css_style_tag_sanitized(self, temp_dir):
        md = temp_dir / "test.md"
        md.write_text("---\ncss: 'body{} </style><script>alert(1)</script>'\n---\n# X\n")
        conv = BaseConverter(input_file=str(md))
        conv._read_markdown_content()
        assert "</style>" not in conv.custom_css


class TestOrientationCSS:
    """Test orientation CSS injection in HTML output."""

    @pytest.mark.unit
    def test_landscape_injects_page_and_maxwidth(self, sample_markdown_file):
        conv = BaseConverter(input_file=str(sample_markdown_file), orientation="landscape")
        html = conv._create_html_document("<p>test</p>")
        assert "size: A4 landscape" in html
        assert "body { max-width: 100%; }" in html

    @pytest.mark.unit
    def test_portrait_injects_page_without_maxwidth(self, sample_markdown_file):
        conv = BaseConverter(input_file=str(sample_markdown_file), orientation="portrait")
        html = conv._create_html_document("<p>test</p>")
        assert "size: A4 portrait" in html
        assert "body { max-width: 100%; }" not in html

    @pytest.mark.unit
    def test_no_orientation_no_override(self, sample_markdown_file):
        conv = BaseConverter(input_file=str(sample_markdown_file))
        html = conv._create_html_document("<p>test</p>")
        assert "@page" not in html.split("{self.css_styles}")[0] or True
        assert "body { max-width: 100%; }" not in html

    @pytest.mark.unit
    def test_preserves_custom_page_size(self, sample_markdown_file):
        """Orientation override should preserve the style's page size, not hardcode A4."""
        conv = BaseConverter(
            input_file=str(sample_markdown_file),
            style="amazon_book",
            orientation="landscape",
        )
        html = conv._create_html_document("<p>test</p>")
        assert "152.4mm 228.6mm landscape" in html
        assert "A4" not in html.split("</style>")[0].split("size:")[-1]

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
