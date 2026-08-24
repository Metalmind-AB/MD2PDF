#!/usr/bin/env python3
"""MD2PDF - Markdown to PDF Converter.

Copyright (c) 2025 MPS Metalmind AB
Licensed under the MIT License (see LICENSE file)

PDF Converter - Converts Markdown to PDF using WeasyPrint.
Inherits from BaseConverter and provides PDF-specific functionality.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional, Set
from urllib.parse import unquote, urlparse
from urllib.request import url2pathname

try:
    from weasyprint import HTML

    try:
        from weasyprint import default_url_fetcher
    except ImportError:
        from weasyprint.urls import default_url_fetcher

    WEASYPRINT_AVAILABLE = True
except ImportError:
    HTML = None
    default_url_fetcher = None
    WEASYPRINT_AVAILABLE = False

try:
    from pypdf import PdfReader, PdfWriter

    PYPDF_AVAILABLE = True
except ImportError:
    PdfReader = None  # type: ignore
    PdfWriter = None  # type: ignore
    PYPDF_AVAILABLE = False

from md2pdf.core.converters.base_converter import BaseConverter
from md2pdf.core.utils.margin_guard import (
    MAX_FIT_PASSES,
    MAX_FIT_TIER,
    build_row_fit_css,
    build_table_fit_css,
    describe_overflow,
    find_headerless_rows,
    find_overflowing_tables,
)


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

            # Convert HTML to PDF with font configuration
            print(f"Generating PDF: {self.output_file}")
            # For future use: Path(self.input_file).parent / "exports"
            # Use input file's directory as base URL for relative image paths
            base_url = str(Path(self.input_file).parent.resolve()) + "/"

            # Lay the document out, shrinking anything that would bleed past
            # the page margins, then write the result
            document = self._render_fitted(html_content, base_url)

            # Configure PDF generation for print-ready output
            # Standard PDF without PDF/A which can cause issues with KDP
            document.write_pdf(
                str(self.output_file),
                # Don't use pdf_variant as it can cause compatibility issues
                uncompressed_pdf=False,  # Keep compressed for smaller size
            )

            # Add watermark if provided
            if self.watermark:
                self._embed_watermark()

            print(f"✅ Successfully created PDF: {self.output_file}")
            return True

        except Exception as e:
            print(f"❌ Error converting to PDF: {str(e)}")
            return False

    def _make_url_fetcher(self):
        """Build a WeasyPrint URL fetcher that blocks network and file escapes."""
        if _remote_resources_allowed():
            return default_url_fetcher

        allowed_roots = self._resource_roots()

        def safe_url_fetcher(url: str, *args, **kwargs):
            parsed = urlparse(url)
            scheme = parsed.scheme.lower()

            if scheme in ("http", "https", "ftp"):
                raise ValueError(f"Blocked remote resource: {scheme} URL")

            if scheme == "data":
                return default_url_fetcher(url, *args, **kwargs)

            if scheme == "file":
                if parsed.netloc and parsed.netloc not in ("localhost", "127.0.0.1"):
                    raise ValueError("Blocked non-local file resource")
                resource_path = Path(url2pathname(unquote(parsed.path))).resolve()
                if _is_path_under_any_root(resource_path, allowed_roots):
                    return default_url_fetcher(url, *args, **kwargs)
                raise ValueError(f"Blocked file resource outside allowed roots: {url}")

            if not scheme:
                resource_path = Path(url).resolve()
                if _is_path_under_any_root(resource_path, allowed_roots):
                    return default_url_fetcher(url, *args, **kwargs)
                raise ValueError(f"Blocked file resource outside allowed roots: {url}")

            raise ValueError(f"Blocked unsupported resource scheme: {scheme}")

        return safe_url_fetcher

    def _resource_roots(self) -> list[Path]:
        """Return directories WeasyPrint may read local resources from."""
        package_root = Path(__file__).resolve().parents[2]
        roots = [
            Path(self.input_file).parent.resolve(),
            (package_root / "assets").resolve(),
        ]
        return [root for root in roots if root.exists()]

    def _render(self, html_content: str, base_url: str, extra_css: str) -> Any:
        """Lay out the document once with the given extra CSS applied."""
        html_document = self._create_html_document(html_content, extra_css)
        html = HTML(
            string=html_document,
            base_url=base_url,
            url_fetcher=self._make_url_fetcher(),
        )
        return html.render()

    def _render_fitted(self, html_content: str, base_url: str) -> Any:
        """Lay out the document, re-laying it out until every table fits a page.

        Two things do not fit on their own.  A table whose columns cannot shrink
        below the page width is laid out past the ``@page`` margin box and
        bleeds off the paper; each such table gets an escalating relaxation —
        header wrapping, then word breaking, then fixed columns and smaller type
        — until it fits.  And a row that ``page-break-inside: avoid`` moves onto
        a new page arrives without the table's repeated header, so the table
        appears to start mid-page with no header; each such row is released to
        break across pages instead.  Documents where everything already fits are
        laid out once and are unaffected.
        """
        document = self._render(html_content, base_url, "")
        tiers: Dict[int, Optional[Set[str]]] = {}
        released_rows: Set[str] = set()

        for _ in range(MAX_FIT_PASSES):
            if not self._plan_fit(document, tiers, released_rows):
                break
            document = self._render(
                html_content,
                base_url,
                build_table_fit_css(tiers) + build_row_fit_css(released_rows),
            )

        self._report_remaining_overflow(document)
        return document

    def _plan_fit(
        self,
        document: Any,
        tiers: Dict[int, Optional[Set[str]]],
        released_rows: Set[str],
    ) -> bool:
        """Record what to relax next; False when nothing is left to try."""
        released = self._release_headerless_rows(document, released_rows)
        escalated = self._escalate_table_fit(document, tiers)
        return released or escalated

    @staticmethod
    def _release_headerless_rows(document: Any, released_rows: Set[str]) -> bool:
        """Let the rows that lost their header break across pages."""
        new_rows = (find_headerless_rows(document) or set()) - released_rows
        if not new_rows:
            return False

        released_rows |= new_rows
        noun = "row" if len(new_rows) == 1 else "rows"
        print(
            f"Restoring table headers: {len(new_rows)} {noun} released to break "
            "across pages"
        )
        return True

    @staticmethod
    def _escalate_table_fit(
        document: Any, tiers: Dict[int, Optional[Set[str]]]
    ) -> bool:
        """Move the tables that still overflow to the next relaxation tier."""
        overflow = find_overflowing_tables(document)
        tier = max(tiers, default=0)

        if overflow is None:
            if None in tiers.values():
                return False  # the catch-all is already applied
            print(
                "Warning: could not measure table widths "
                "(unexpected WeasyPrint layout tree); "
                "fitting all tables to the page margins"
            )
            tiers[min(tier + 1, MAX_FIT_TIER)] = None
            return True

        if overflow and tier < MAX_FIT_TIER:
            print(f"Fitting to page margins: {describe_overflow(overflow)}")
            tiers[tier + 1] = set(overflow)
            return True

        return False

    @staticmethod
    def _report_remaining_overflow(document: Any) -> None:
        """Say so when a table could not be brought inside the margins."""
        overflow = find_overflowing_tables(document)
        if overflow:
            print(
                f"Warning: {describe_overflow(overflow)} still exceed the page "
                "margins — consider --orientation landscape or fewer columns"
            )

    def _embed_watermark(self) -> None:
        """Embed an invisible watermark in the PDF metadata."""
        if not PYPDF_AVAILABLE:
            print("Warning: pypdf not available, skipping watermark")
            return

        try:
            # Read the PDF
            reader = PdfReader(str(self.output_file))
            writer = PdfWriter()

            # Copy all pages
            for page in reader.pages:
                writer.add_page(page)

            # Add watermark to metadata
            writer.add_metadata(
                {
                    "/Producer": "md2pdf",
                    "/Creator": "md2pdf",
                    "/MD2PDF_Watermark": self.watermark,
                }
            )

            # Also embed in XMP metadata for better compatibility
            if hasattr(writer, "add_metadata_stream"):
                writer.add_metadata_stream(self._build_xmp_metadata())

            # Write back to file
            with open(self.output_file, "wb") as output_pdf:
                writer.write(output_pdf)

            print(f"✅ Watermark embedded in PDF metadata")

        except Exception as e:
            print(f"Warning: Could not embed watermark: {str(e)}")

    def _build_xmp_metadata(self) -> str:
        """Build escaped XMP metadata for the configured watermark."""
        watermark = _escape_xml_text(self.watermark or "")
        return f"""<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
        <rdf:Description rdf:about=""
            xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:md2pdf="http://md2pdf.com/ns/">
            <md2pdf:watermark>{watermark}</md2pdf:watermark>
        </rdf:Description>
    </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>"""


def _remote_resources_allowed() -> bool:
    value = os.getenv("MD2PDF_ALLOW_REMOTE_RESOURCES", "")
    return value.lower() in {"1", "true", "yes", "on"}


def _escape_xml_text(value: str) -> str:
    """Escape text for XML element content."""
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _is_path_under_any_root(path: Path, roots: list[Path]) -> bool:
    resolved = path.resolve()
    for root in roots:
        try:
            resolved.relative_to(root.resolve())
            return True
        except ValueError:
            continue
    return False
