# Copyright (c) 2025 MPS Metalmind AB
# Licensed under the MIT License (see LICENSE file)

"""
Tests for MD2PDF converter core functionality.
"""

from unittest.mock import Mock, patch

import pytest

from md2pdf.core.converters.base_converter import BaseConverter

try:
    from md2pdf.core.converters.pdf_converter import PDFConverter

    WEASYPRINT_AVAILABLE = True
except ImportError:
    PDFConverter = None
    WEASYPRINT_AVAILABLE = False
from md2pdf.core.converters.word_converter import WordConverter


class TestBaseConverter:
    """Test the base converter functionality."""

    @pytest.mark.unit
    def test_base_converter_initialization(self, sample_markdown_file):
        """Test base converter can be initialized with valid input."""
        converter = BaseConverter(
            input_file=str(sample_markdown_file),
            output_file=None,
            style="technical",
            theme="default",
        )

        assert converter.input_file == sample_markdown_file
        assert converter.style_name == "technical"
        assert converter.theme_name == "default"
        assert converter.output_file == sample_markdown_file.with_suffix(".pdf")

    @pytest.mark.unit
    def test_base_converter_with_output_file(self, sample_markdown_file, temp_dir):
        """Test base converter with specified output file."""
        output_path = temp_dir / "output.pdf"
        converter = BaseConverter(
            input_file=str(sample_markdown_file),
            output_file=str(output_path),
            style="academic",
            theme="oceanic",
        )

        assert converter.input_file == sample_markdown_file
        assert converter.output_file == output_path
        assert converter.style == "academic"
        assert converter.theme == "oceanic"

    @pytest.mark.unit
    def test_base_converter_invalid_input(self):
        """Test base converter with non-existent input file."""
        with pytest.raises(FileNotFoundError):
            BaseConverter(input_file="/nonexistent/file.md", output_file=None)

    @pytest.mark.unit
    def test_base_converter_abstract_convert(self, sample_markdown_file):
        """Test that base converter convert method is abstract."""
        converter = BaseConverter(input_file=str(sample_markdown_file))

        with pytest.raises(NotImplementedError):
            converter.convert()

    @pytest.mark.unit
    def test_process_markdown(self, sample_markdown_file):
        """Test markdown processing in base converter."""
        converter = BaseConverter(input_file=str(sample_markdown_file))

        html = converter.process_markdown()

        assert html is not None
        assert "<h1>" in html or "<h1 " in html  # Check for H1 tag
        assert "<p>" in html  # Check for paragraph tags
        assert len(html) > 100  # Ensure substantial HTML output


@pytest.mark.skipif(not WEASYPRINT_AVAILABLE, reason="WeasyPrint not available")
class TestPDFConverter:
    """Test the PDF converter functionality."""

    @pytest.mark.unit
    def test_pdf_converter_initialization(self, sample_markdown_file):
        """Test PDF converter initialization."""
        converter = PDFConverter(
            input_file=str(sample_markdown_file), style="technical", theme="default"
        )

        assert isinstance(converter, PDFConverter)
        assert isinstance(converter, BaseConverter)
        assert converter.style_name == "technical"
        assert converter.theme_name == "default"

    @pytest.mark.unit
    def test_pdf_output_path_generation(self, sample_markdown_file):
        """Test automatic PDF output path generation."""
        converter = PDFConverter(input_file=str(sample_markdown_file))

        output_path = converter._generate_output_path()

        assert output_path.suffix == ".pdf"
        assert output_path.stem == sample_markdown_file.stem

    @pytest.mark.unit
    def test_pdf_output_with_custom_path(self, sample_markdown_file, temp_dir):
        """Test PDF converter with custom output path."""
        custom_output = temp_dir / "custom_name.pdf"
        converter = PDFConverter(
            input_file=str(sample_markdown_file), output_file=str(custom_output)
        )

        assert converter.output_file == custom_output
        assert converter.output_file.suffix == ".pdf"

    @pytest.mark.integration
    @patch("md2pdf.core.converters.pdf_converter.HTML")
    def test_pdf_conversion_success(self, mock_html, sample_markdown_file, temp_dir):
        """Test successful PDF conversion (mocked)."""
        # Setup mocks
        mock_html_instance = Mock()
        mock_html.return_value = mock_html_instance
        mock_html_instance.write_pdf.return_value = None

        output_file = temp_dir / "test.pdf"
        converter = PDFConverter(
            input_file=str(sample_markdown_file), output_file=str(output_file)
        )

        result = converter.convert()

        assert result is True
        mock_html_instance.write_pdf.assert_called_once()

    @pytest.mark.integration
    def test_pdf_conversion_real(self, sample_markdown_file, temp_dir):
        """Test real PDF conversion if WeasyPrint is available."""
        output_file = temp_dir / "test_real.pdf"
        converter = PDFConverter(
            input_file=str(sample_markdown_file),
            output_file=str(output_file),
            style="technical",
            theme="default",
        )

        try:
            result = converter.convert()
            if result:
                assert output_file.exists()
                assert output_file.stat().st_size > 0
        except ImportError:
            pytest.skip("WeasyPrint not available for real conversion test")

    @pytest.mark.unit
    def test_pdf_converter_with_options(self, sample_markdown_file, temp_dir):
        """Test PDF converter with various options."""
        output_file = temp_dir / "options_test.pdf"
        converter = PDFConverter(
            input_file=str(sample_markdown_file),
            output_file=str(output_file),
            style="academic",
            theme="oceanic",
        )

        assert converter.style == "academic"
        assert converter.theme == "oceanic"
        assert converter.output_file == output_file

    @pytest.mark.unit
    @patch("md2pdf.core.converters.pdf_converter.HTML")
    def test_pdf_conversion_failure(self, mock_html, sample_markdown_file, temp_dir):
        """Test PDF conversion failure handling."""
        # Setup mock to raise exception
        mock_html.side_effect = Exception("Conversion failed")

        output_file = temp_dir / "test_fail.pdf"
        converter = PDFConverter(
            input_file=str(sample_markdown_file), output_file=str(output_file)
        )

        result = converter.convert()

        assert result is False


class TestWordConverter:
    """Test the Word converter functionality."""

    @pytest.mark.unit
    def test_word_converter_initialization(self, sample_markdown_file):
        """Test Word converter initialization."""
        converter = WordConverter(
            input_file=str(sample_markdown_file), style="technical"
        )

        assert isinstance(converter, WordConverter)
        assert isinstance(converter, BaseConverter)
        assert converter.style == "technical"

    @pytest.mark.unit
    def test_word_output_path_generation(self, sample_markdown_file):
        """Test automatic Word output path generation."""
        converter = WordConverter(input_file=str(sample_markdown_file))

        output_path = converter._generate_output_path()

        assert output_path.suffix == ".docx"
        assert output_path.stem == sample_markdown_file.stem

    @pytest.mark.integration
    @patch("md2pdf.core.converters.word_converter.BeautifulSoup")
    @patch("md2pdf.core.converters.word_converter.Document")
    def test_word_conversion_success(
        self, mock_document, mock_soup, sample_markdown_file, temp_dir
    ):
        """Test successful Word conversion (mocked)."""
        # Setup mocks
        mock_doc_instance = Mock()
        mock_document.return_value = mock_doc_instance
        mock_doc_instance.save.return_value = None

        # Setup BeautifulSoup mock
        from unittest.mock import MagicMock

        mock_soup_instance = MagicMock()
        mock_soup.return_value = mock_soup_instance
        # When soup is called as a function soup(["script", "style"]), return empty list
        mock_soup_instance.return_value = (
            []
        )  # This makes the mock callable and return []
        # Mock find_all for element processing
        mock_soup_instance.find_all.return_value = []

        output_file = temp_dir / "test.docx"
        converter = WordConverter(
            input_file=str(sample_markdown_file), output_file=str(output_file)
        )

        result = converter.convert()

        assert result is True
        mock_doc_instance.save.assert_called_once()

    @pytest.mark.integration
    def test_word_conversion_real(self, sample_markdown_file, temp_dir):
        """Test real Word conversion if python-docx is available."""
        output_file = temp_dir / "test_real.docx"
        converter = WordConverter(
            input_file=str(sample_markdown_file),
            output_file=str(output_file),
            style="technical",
        )

        try:
            result = converter.convert()
            if result:
                assert output_file.exists()
                assert output_file.stat().st_size > 0
        except ImportError:
            pytest.skip("python-docx not available for real conversion test")

    @pytest.mark.unit
    @patch("md2pdf.core.converters.word_converter.Document")
    def test_word_conversion_failure(
        self, mock_document, sample_markdown_file, temp_dir
    ):
        """Test Word conversion failure handling."""
        # Setup mock to raise exception
        mock_document.side_effect = Exception("Conversion failed")

        output_file = temp_dir / "test_fail.docx"
        converter = WordConverter(
            input_file=str(sample_markdown_file), output_file=str(output_file)
        )

        result = converter.convert()

        assert result is False


class TestConverterIntegration:
    """Integration tests for converters."""

    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.skipif(not WEASYPRINT_AVAILABLE, reason="WeasyPrint not available")
    def test_batch_conversion(self, multiple_markdown_files, temp_dir):
        """Test batch conversion of multiple files."""
        results = []

        for md_file in multiple_markdown_files:
            output_file = temp_dir / f"{md_file.stem}_converted.pdf"
            converter = PDFConverter(
                input_file=str(md_file), output_file=str(output_file)
            )

            with patch("md2pdf.core.converters.pdf_converter.HTML"):
                result = converter.convert()
                results.append(result)

        assert all(results), "All conversions should succeed"
        assert len(results) == len(multiple_markdown_files)

    @pytest.mark.integration
    @pytest.mark.skipif(not WEASYPRINT_AVAILABLE, reason="WeasyPrint not available")
    def test_complex_markdown_conversion(self, temp_dir, complex_markdown):
        """Test conversion of complex markdown content."""
        md_file = temp_dir / "complex.md"
        md_file.write_text(complex_markdown)

        output_file = temp_dir / "complex.pdf"
        converter = PDFConverter(input_file=str(md_file), output_file=str(output_file))

        html = converter.process_markdown()

        # Check that complex features are processed
        assert "<h1" in html or "h1>" in html  # Headers
        assert "<ul" in html or "<ol" in html  # Lists
        assert "emoji" in html.lower()  # Emoji support
        assert "footnote" in html.lower()  # Footnotes

    @pytest.mark.integration
    @pytest.mark.skipif(not WEASYPRINT_AVAILABLE, reason="WeasyPrint not available")
    def test_invalid_markdown_handling(self, temp_dir, invalid_markdown):
        """Test handling of invalid/malformed markdown."""
        md_file = temp_dir / "invalid.md"
        md_file.write_text(invalid_markdown)

        converter = PDFConverter(
            input_file=str(md_file), output_file=str(temp_dir / "invalid.pdf")
        )

        # Should not raise exception, should handle gracefully
        html = converter.process_markdown()
        assert html is not None
        assert len(html) > 0

    @pytest.mark.integration
    @pytest.mark.parametrize(
        "style", ["technical", "academic", "story", "modern", "consultancy"]
    )
    @pytest.mark.skipif(not WEASYPRINT_AVAILABLE, reason="WeasyPrint not available")
    def test_different_styles(self, sample_markdown_file, temp_dir, style):
        """Test conversion with different style templates."""
        output_file = temp_dir / f"test_{style}.pdf"
        converter = PDFConverter(
            input_file=str(sample_markdown_file),
            output_file=str(output_file),
            style=style,
        )

        with patch("md2pdf.core.converters.pdf_converter.HTML"):
            result = converter.convert()
            assert result is True

    @pytest.mark.integration
    @pytest.mark.parametrize(
        "theme", ["default", "dark", "oceanic", "forest", "elegant"]
    )
    @pytest.mark.skipif(not WEASYPRINT_AVAILABLE, reason="WeasyPrint not available")
    def test_different_themes(self, sample_markdown_file, temp_dir, theme):
        """Test conversion with different color themes."""
        output_file = temp_dir / f"test_{theme}.pdf"
        converter = PDFConverter(
            input_file=str(sample_markdown_file),
            output_file=str(output_file),
            theme=theme,
        )

        with patch("md2pdf.core.converters.pdf_converter.HTML"):
            result = converter.convert()
            assert result is True

    @pytest.mark.skip(
        reason="Emoji support is now optional - requires separate download"
    )
    @pytest.mark.integration
    @pytest.mark.skipif(not WEASYPRINT_AVAILABLE, reason="WeasyPrint not available")
    def test_unicode_and_emoji_support(self, temp_dir):
        """Test Unicode and emoji support in conversion."""
        content = """# Unicode Test 🚀

        Chinese: 你好世界
        Japanese: こんにちは
        Emoji: 🎉 💻 📚
        Math: α + β = γ
        """

        md_file = temp_dir / "unicode.md"
        md_file.write_text(content)

        converter = PDFConverter(
            input_file=str(md_file), output_file=str(temp_dir / "unicode.pdf")
        )

        html = converter.process_markdown()

        # Check that Unicode is preserved
        assert "你好世界" in html
        assert "こんにちは" in html
        assert "α" in html or "&alpha;" in html

    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.skipif(not WEASYPRINT_AVAILABLE, reason="WeasyPrint not available")
    def test_large_file_performance(self, temp_dir):
        """Test conversion performance with large files."""
        # Create a large markdown file
        large_content = "# Large Document\n\n"
        for i in range(1000):
            large_content += f"## Section {i}\n\n"
            large_content += f"This is paragraph {i} with some content.\n\n"
            large_content += f"- Item {i}-1\n- Item {i}-2\n- Item {i}-3\n\n"

        md_file = temp_dir / "large.md"
        md_file.write_text(large_content)

        converter = PDFConverter(
            input_file=str(md_file), output_file=str(temp_dir / "large.pdf")
        )

        import time

        start = time.time()
        html = converter.process_markdown()
        duration = time.time() - start

        assert html is not None
        assert duration < 5.0, f"Large file processing took too long: {duration}s"
