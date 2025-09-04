# Copyright (c) 2025 MPS Metalmind AB
# Licensed under the MIT License (see LICENSE file)

"""
Integration tests for MD2PDF end-to-end workflows.
"""

import time
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner

from md2pdf.cli import cli
from md2pdf.core.converters.pdf_converter import PDFConverter
from md2pdf.core.converters.word_converter import WordConverter


class TestEndToEndWorkflows:
    """Test complete end-to-end conversion workflows."""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_complete_pdf_workflow(self, temp_dir):
        """Test complete workflow from markdown to PDF."""
        # Create test markdown file
        md_file = temp_dir / "workflow_test.md"
        md_content = """# Workflow Test Document

## Introduction
This is a complete workflow test.

### Features
- Lists
- Code blocks
- Tables

```python
def test():
    return "workflow"
```

| Col1 | Col2 |
|------|------|
| A    | B    |
"""
        md_file.write_text(md_content)

        # Convert to PDF
        output_file = temp_dir / "workflow_test.pdf"
        converter = PDFConverter(
            input_file=str(md_file),
            output_file=str(output_file),
            style="technical",
            theme="default",
        )

        # Mock WeasyPrint to avoid actual PDF generation in tests
        with patch("md2pdf.core.converters.pdf_converter.HTML") as mock_html:
            mock_html_instance = Mock()
            mock_html.return_value = mock_html_instance
            mock_html_instance.write_pdf.return_value = None

            result = converter.convert()

            assert result is True
            mock_html_instance.write_pdf.assert_called_once()

    @pytest.mark.integration
    @pytest.mark.slow
    def test_complete_word_workflow(self, temp_dir):
        """Test complete workflow from markdown to Word."""
        # Create test markdown file
        md_file = temp_dir / "word_workflow_test.md"
        md_content = """# Word Workflow Test

## Section 1
Content for section 1.

## Section 2
Content for section 2 with **bold** and *italic*.
"""
        md_file.write_text(md_content)

        # Convert to Word
        output_file = temp_dir / "word_workflow_test.docx"
        converter = WordConverter(
            input_file=str(md_file), output_file=str(output_file), style="academic"
        )

        # Mock python-docx to avoid actual Word generation
        with patch("md2pdf.core.converters.word_converter.Document") as mock_doc:
            mock_doc_instance = Mock()
            mock_doc.return_value = mock_doc_instance

            result = converter.convert()

            assert result is True
            mock_doc_instance.save.assert_called_once()

    @pytest.mark.integration
    def test_batch_processing_workflow(self, temp_dir):
        """Test batch processing of multiple files."""
        # Create multiple markdown files
        files = []
        for i in range(5):
            md_file = temp_dir / f"batch_test_{i}.md"
            md_file.write_text(f"# Document {i}\n\nContent for document {i}.")
            files.append(md_file)

        # Process all files
        results = []
        for md_file in files:
            output_file = temp_dir / f"{md_file.stem}.pdf"
            converter = PDFConverter(
                input_file=str(md_file), output_file=str(output_file)
            )

            with patch("md2pdf.core.converters.pdf_converter.HTML"):
                result = converter.convert()
                results.append(result)

        assert all(results), "All batch conversions should succeed"
        assert len(results) == 5

    @pytest.mark.integration
    def test_cli_workflow(self, temp_dir):
        """Test complete CLI workflow."""
        runner = CliRunner()

        # Create test file
        md_file = temp_dir / "cli_workflow.md"
        md_file.write_text("# CLI Test\n\nTesting CLI workflow.")

        with patch("md2pdf.cli.PDFConverter") as mock_converter:
            mock_instance = Mock()
            mock_converter.return_value = mock_instance
            mock_instance.convert.return_value = True
            mock_instance.output_file = temp_dir / "cli_workflow.pdf"

            # Test CLI command
            result = runner.invoke(
                cli,
                ["convert", str(md_file), "--style", "technical", "--theme", "dark"],
            )

            assert result.exit_code == 0
            assert mock_converter.called

    @pytest.mark.integration
    @pytest.mark.slow
    def test_style_switching_workflow(self, temp_dir):
        """Test workflow with different styles."""
        md_file = temp_dir / "style_test.md"
        md_file.write_text(
            """# Style Test Document

## Testing Different Styles

This document will be converted with different styles.
"""
        )

        styles = ["technical", "academic", "creative", "simple", "professional"]

        for style in styles:
            output_file = temp_dir / f"style_{style}.pdf"
            converter = PDFConverter(
                input_file=str(md_file),
                output_file=str(output_file),
                style=style,
                theme="default",
            )

            with patch("md2pdf.core.converters.pdf_converter.HTML"):
                result = converter.convert()
                assert result is True, f"Conversion with style '{style}' failed"

    @pytest.mark.integration
    @pytest.mark.slow
    def test_theme_switching_workflow(self, temp_dir):
        """Test workflow with different themes."""
        md_file = temp_dir / "theme_test.md"
        md_file.write_text(
            """# Theme Test Document

## Testing Different Themes

This document will be converted with different color themes.
"""
        )

        themes = ["default", "dark", "ocean", "forest", "lavender"]

        for theme in themes:
            output_file = temp_dir / f"theme_{theme}.pdf"
            converter = PDFConverter(
                input_file=str(md_file),
                output_file=str(output_file),
                style="technical",
                theme=theme,
            )

            with patch("md2pdf.core.converters.pdf_converter.HTML"):
                result = converter.convert()
                assert result is True, f"Conversion with theme '{theme}' failed"

    @pytest.mark.integration
    def test_complex_document_workflow(self, temp_dir):
        """Test workflow with complex document from fixtures."""
        # Use the complex fixture file
        fixture_file = Path("tests/fixtures/complex.md")
        if fixture_file.exists():
            output_file = temp_dir / "complex_output.pdf"
            converter = PDFConverter(
                input_file=str(fixture_file),
                output_file=str(output_file),
                style="academic",
                theme="default",
            )

            # Process markdown to HTML
            html = converter.process_markdown()

            # Verify complex features are handled
            assert "<table" in html or "table" in html.lower()
            assert "<code" in html or "code" in html.lower()
            assert len(html) > 1000  # Should be substantial

    @pytest.mark.integration
    @pytest.mark.slow
    def test_performance_workflow(self, temp_dir):
        """Test performance with large document."""
        # Create large document
        large_content = "# Large Document\n\n"
        for i in range(500):
            large_content += f"## Section {i}\n\n"
            large_content += f"This is content for section {i}. " * 10
            large_content += "\n\n"

        md_file = temp_dir / "large_perf_test.md"
        md_file.write_text(large_content)

        output_file = temp_dir / "large_perf_test.pdf"
        converter = PDFConverter(input_file=str(md_file), output_file=str(output_file))

        start_time = time.time()
        html = converter.process_markdown()
        processing_time = time.time() - start_time

        assert html is not None
        assert len(html) > 10000
        assert (
            processing_time < 10.0
        ), f"Processing took {processing_time}s, should be < 10s"

    @pytest.mark.integration
    def test_error_recovery_workflow(self, temp_dir):
        """Test error recovery in conversion workflow."""
        # Create markdown with potential issues
        problematic_md = """# Test Document

## Unclosed code block
```python
def test():
    # Missing closing backticks

## Broken table
| Col1 | Col2 |
| Missing closing

## Invalid link
[Broken link](

## Still should process
This content should still be processed.
"""

        md_file = temp_dir / "problematic.md"
        md_file.write_text(problematic_md)

        converter = PDFConverter(
            input_file=str(md_file), output_file=str(temp_dir / "problematic.pdf")
        )

        # Should handle errors gracefully
        html = converter.process_markdown()
        assert html is not None
        assert "This content should still be processed" in html

    @pytest.mark.integration
    def test_unicode_workflow(self, temp_dir):
        """Test workflow with Unicode and special characters."""
        unicode_content = """# Unicode Test 🌍

## International Content

Chinese: 你好世界
Japanese: こんにちは世界
Arabic: مرحبا بالعالم
Russian: Привет мир
Greek: Γεια σου κόσμος

## Math Symbols

α + β = γ
∫ f(x) dx = F(x) + C
∑(i=1 to n) = n(n+1)/2

## Emoji

🚀 🎨 💻 📚 ✨
"""

        md_file = temp_dir / "unicode_test.md"
        md_file.write_text(unicode_content, encoding="utf-8")

        converter = PDFConverter(
            input_file=str(md_file), output_file=str(temp_dir / "unicode_test.pdf")
        )

        html = converter.process_markdown()

        # Check Unicode preservation
        assert "你好世界" in html
        assert "こんにちは" in html
        assert "مرحبا" in html or "&#" in html  # Arabic might be encoded

    @pytest.mark.integration
    def test_format_switching_workflow(self, temp_dir):
        """Test switching between PDF and Word formats."""
        md_file = temp_dir / "format_test.md"
        md_file.write_text(
            """# Format Test

Testing conversion to different formats.
"""
        )

        # Convert to PDF
        pdf_converter = PDFConverter(
            input_file=str(md_file), output_file=str(temp_dir / "format_test.pdf")
        )

        with patch("md2pdf.core.converters.pdf_converter.HTML"):
            pdf_result = pdf_converter.convert()
            assert pdf_result is True

        # Convert to Word
        word_converter = WordConverter(
            input_file=str(md_file), output_file=str(temp_dir / "format_test.docx")
        )

        with patch("md2pdf.core.converters.word_converter.Document"):
            word_result = word_converter.convert()
            assert word_result is True

    @pytest.mark.integration
    @pytest.mark.slow
    def test_concurrent_conversions(self, temp_dir):
        """Test multiple concurrent conversions."""
        import concurrent.futures

        # Create test files
        files = []
        for i in range(10):
            md_file = temp_dir / f"concurrent_{i}.md"
            md_file.write_text(f"# Document {i}\n\nConcurrent test {i}.")
            files.append(md_file)

        def convert_file(md_file):
            output_file = temp_dir / f"{md_file.stem}.pdf"
            converter = PDFConverter(
                input_file=str(md_file), output_file=str(output_file)
            )
            with patch("md2pdf.core.converters.pdf_converter.HTML"):
                return converter.convert()

        # Run conversions concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(convert_file, files))

        assert all(results), "All concurrent conversions should succeed"
        assert len(results) == 10
