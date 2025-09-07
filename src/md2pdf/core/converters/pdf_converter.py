#!/usr/bin/env python3
"""MD2PDF - Markdown to PDF Converter.

Copyright (c) 2025 MPS Metalmind AB
Licensed under the MIT License (see LICENSE file)

PDF Converter - Converts Markdown to PDF using WeasyPrint.
Inherits from BaseConverter and provides PDF-specific functionality.
"""

from pathlib import Path

try:
    from weasyprint import HTML

    WEASYPRINT_AVAILABLE = True
except ImportError:
    HTML = None
    WEASYPRINT_AVAILABLE = False

from md2pdf.core.converters.base_converter import BaseConverter


class PDFConverter(BaseConverter):
    """PDF converter using WeasyPrint."""

    def _generate_output_path(self) -> Path:
        """Generate output PDF path based on input file."""
        return self.input_file.with_suffix(".pdf")

    def _ensure_pdf_extension(self, output_path: Path) -> Path:
        """Ensure the output path has .pdf extension."""
        if output_path.suffix.lower() != ".pdf":
            return output_path.with_suffix(".pdf")
        return output_path

    def convert(self) -> bool:
        """Convert Markdown file to PDF."""
        if not WEASYPRINT_AVAILABLE:
            print("Error: WeasyPrint is not installed.")
            print("Please install it to convert to PDF:")
            print("  pip install weasyprint")
            return False

        try:
            # Ensure output path has .pdf extension
            self.output_file: Path = self._ensure_pdf_extension(self.output_file)

            # Read the markdown file
            markdown_content = self._read_markdown_content()

            # Convert markdown to HTML
            html_content = self._process_markdown(markdown_content)

            # Create complete HTML document
            html_document = self._create_html_document(html_content)

            # Convert HTML to PDF with font configuration
            print(f"Generating PDF: {self.output_file}")
            # For future use: Path(self.input_file).parent / "exports"
            base_url = str(Path(".").resolve()) + "/"

            # Create HTML object and write PDF
            html = HTML(string=html_document, base_url=base_url)
            html.write_pdf(str(self.output_file))

            print(f"✅ Successfully created PDF: {self.output_file}")
            return True

        except Exception as e:
            print(f"❌ Error converting to PDF: {str(e)}")
            return False
