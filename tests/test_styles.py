# Copyright (c) 2025 MPS Metalmind AB
# Licensed under the MIT License (see LICENSE file)

"""
Tests for MD2PDF style and theme system.
"""


import pytest

from md2pdf.core.utils.style_loader import style_loader


class TestStyleLoader:
    """Test the style loading system."""

    @pytest.mark.unit
    @pytest.mark.style
    def test_style_loader_initialization(self):
        """Test style loader initialization."""
        assert style_loader is not None
        assert hasattr(style_loader, "get_css")
        assert hasattr(style_loader, "list_styles")
        assert hasattr(style_loader, "list_themes")

    @pytest.mark.unit
    @pytest.mark.style
    def test_list_available_styles(self):
        """Test listing available style templates."""
        styles = style_loader.list_available_styles()

        assert isinstance(styles, list)
        assert len(styles) > 0
        # Check for expected default styles
        expected_styles = [
            "technical",
            "academic",
            "story",
            "modern",
            "consultancy",
        ]
        for style in expected_styles:
            assert style in styles, f"Style '{style}' not found"

    @pytest.mark.unit
    @pytest.mark.style
    def test_list_available_themes(self):
        """Test listing available color themes."""
        themes = style_loader.list_available_themes()

        assert isinstance(themes, list)
        assert len(themes) > 0
        # Check for expected default themes
        expected_themes = ["default", "dark", "oceanic", "forest", "sepia"]
        for theme in expected_themes:
            assert theme in themes, f"Theme '{theme}' not found"

    @pytest.mark.unit
    @pytest.mark.style
    def test_get_css_default(self):
        """Test getting CSS with default style and theme."""
        css = style_loader.get_css()

        assert css is not None
        assert len(css) > 100  # Ensure substantial CSS content
        assert "body" in css  # Basic CSS selector
        assert "font-family" in css  # Font definitions

    @pytest.mark.unit
    @pytest.mark.style
    @pytest.mark.parametrize(
        "style", ["technical", "academic", "story", "modern", "consultancy"]
    )
    def test_get_css_different_styles(self, style):
        """Test getting CSS for different style templates."""
        css = style_loader.get_css(style=style, theme="default")

        assert css is not None
        assert len(css) > 100
        assert "body" in css
        # Check for style-specific features
        if style == "technical":
            assert "monospace" in css or "mono" in css.lower()
        elif style == "academic":
            assert "serif" in css.lower()

    @pytest.mark.unit
    @pytest.mark.style
    @pytest.mark.parametrize(
        "theme", ["default", "dark", "oceanic", "forest", "elegant"]
    )
    def test_get_css_different_themes(self, theme):
        """Test getting CSS for different color themes."""
        css = style_loader.get_css(style="technical", theme=theme)

        assert css is not None
        assert len(css) > 100
        # Check for theme-specific colors
        if theme == "dark":
            # Dark themes should have dark backgrounds
            assert "#1" in css or "#2" in css or "#3" in css or "rgb" in css
        elif theme == "oceanic":
            # Ocean theme might have blue colors
            assert "#" in css  # At least has color definitions

    @pytest.mark.unit
    @pytest.mark.style
    def test_get_css_invalid_style(self):
        """Test getting CSS with invalid style name."""
        # Should fall back to default or raise error
        css = style_loader.get_css(style="nonexistent_style", theme="default")

        # Should either return default CSS or be None
        if css is not None:
            assert len(css) > 100  # Got fallback CSS

    @pytest.mark.unit
    @pytest.mark.style
    def test_get_css_invalid_theme(self):
        """Test getting CSS with invalid theme name."""
        # Should fall back to default or raise error
        css = style_loader.get_css(style="technical", theme="nonexistent_theme")

        # Should either return default CSS or be None
        if css is not None:
            assert len(css) > 100  # Got fallback CSS

    @pytest.mark.unit
    @pytest.mark.style
    def test_css_font_imports(self):
        """Test that CSS includes Google Fonts imports."""
        css = style_loader.get_css(style="technical", theme="default")

        # Check for Google Fonts CDN imports
        assert "@import" in css or "fonts.googleapis.com" in css

    @pytest.mark.unit
    @pytest.mark.style
    def test_css_media_queries(self):
        """Test that CSS includes media queries for responsiveness."""
        css = style_loader.get_css(style="professional", theme="default")

        # Check for print media queries
        assert "@media print" in css or "@page" in css

    @pytest.mark.unit
    @pytest.mark.style
    def test_css_page_settings(self):
        """Test that CSS includes page settings for PDF."""
        css = style_loader.get_css(style="academic", theme="default")

        # Check for page-related CSS
        assert "@page" in css or "page-break" in css or "size:" in css

    @pytest.mark.integration
    @pytest.mark.style
    def test_style_css_file_existence(self):
        """Test that actual CSS files exist for each style."""
        styles = style_loader.list_styles()

        for style in styles:
            css = style_loader.get_css(style=style, theme="default")
            assert css is not None, f"No CSS found for style '{style}'"
            assert len(css) > 100, f"CSS for style '{style}' is too short"

    @pytest.mark.integration
    @pytest.mark.style
    def test_theme_css_file_existence(self):
        """Test that actual CSS files exist for each theme."""
        themes = style_loader.list_available_themes()

        for theme in themes:
            css = style_loader.get_css(style="technical", theme=theme)
            assert css is not None, f"No CSS found for theme '{theme}'"
            assert len(css) > 100, f"CSS for theme '{theme}' is too short"

    @pytest.mark.unit
    @pytest.mark.style
    def test_css_syntax_validation(self):
        """Test that generated CSS has valid syntax."""
        css = style_loader.get_css(style="technical", theme="default")

        # Basic CSS syntax checks
        assert css.count("{") == css.count("}"), "Unbalanced braces in CSS"
        assert css.count("/*") == css.count("*/"), "Unbalanced comments in CSS"

        # Check for common CSS patterns
        assert ":" in css, "No property declarations found"
        assert ";" in css, "No statement terminators found"

    @pytest.mark.unit
    @pytest.mark.style
    def test_css_custom_properties(self):
        """Test that CSS includes custom properties for theming."""
        css = style_loader.get_css(style="professional", theme="dark")

        # Check for CSS variables (custom properties)
        if "--" in css:
            assert "var(--" in css, "CSS variables defined but not used"

    @pytest.mark.integration
    @pytest.mark.style
    def test_style_theme_combinations(self):
        """Test all style and theme combinations."""
        styles = style_loader.list_styles()
        themes = style_loader.list_available_themes()

        for style in styles:
            for theme in themes:
                css = style_loader.get_css(style=style, theme=theme)
                assert css is not None, f"Failed for {style}/{theme}"
                assert len(css) > 100, f"CSS too short for {style}/{theme}"

    @pytest.mark.unit
    @pytest.mark.style
    def test_css_code_block_styling(self):
        """Test that CSS includes code block styling."""
        css = style_loader.get_css(style="technical", theme="default")

        # Check for code-related styling
        assert "code" in css or "pre" in css or "highlight" in css
        assert "monospace" in css or "mono" in css.lower()

    @pytest.mark.unit
    @pytest.mark.style
    def test_css_table_styling(self):
        """Test that CSS includes table styling."""
        css = style_loader.get_css(style="academic", theme="default")

        # Check for table-related styling
        assert "table" in css or "td" in css or "th" in css or "tr" in css

    @pytest.mark.unit
    @pytest.mark.style
    def test_css_header_styling(self):
        """Test that CSS includes header styling."""
        css = style_loader.get_css(style="creative", theme="default")

        # Check for header-related styling
        headers = ["h1", "h2", "h3", "h4", "h5", "h6"]
        header_found = any(h in css for h in headers)
        assert header_found, "No header styling found in CSS"

    @pytest.mark.unit
    @pytest.mark.style
    def test_css_list_styling(self):
        """Test that CSS includes list styling."""
        css = style_loader.get_css(style="simple", theme="default")

        # Check for list-related styling
        list_selectors = ["ul", "ol", "li", "list"]
        list_found = any(selector in css for selector in list_selectors)
        assert list_found, "No list styling found in CSS"

    @pytest.mark.unit
    @pytest.mark.style
    def test_css_blockquote_styling(self):
        """Test that CSS includes blockquote styling."""
        css = style_loader.get_css(style="creative", theme="oceanic")

        # Check for blockquote styling
        assert "blockquote" in css or "quote" in css

    @pytest.mark.unit
    @pytest.mark.style
    def test_css_link_styling(self):
        """Test that CSS includes link styling."""
        css = style_loader.get_css(style="professional", theme="default")

        # Check for link styling
        assert "a {" in css or "a:" in css or "link" in css

    @pytest.mark.integration
    @pytest.mark.style
    def test_style_loader_caching(self):
        """Test that style loader caches CSS efficiently."""
        # First call
        css1 = style_loader.get_css(style="technical", theme="default")

        # Second call (should use cache if implemented)
        css2 = style_loader.get_css(style="technical", theme="default")

        assert css1 == css2, "CSS should be consistent between calls"

    @pytest.mark.unit
    @pytest.mark.style
    def test_css_margin_settings(self):
        """Test that CSS includes margin settings."""
        css = style_loader.get_css(style="academic", theme="default")

        # Check for margin-related settings
        assert "margin" in css or "@page" in css

    @pytest.mark.unit
    @pytest.mark.style
    def test_css_font_size_settings(self):
        """Test that CSS includes font size settings."""
        css = style_loader.get_css(style="simple", theme="default")

        # Check for font-size settings
        assert "font-size" in css or "size" in css
        assert "pt" in css or "px" in css or "em" in css or "rem" in css
