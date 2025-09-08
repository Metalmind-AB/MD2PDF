#!/usr/bin/env python3
"""MD2PDF - Watermark Extractor Utility.

Copyright (c) 2025 MPS Metalmind AB
Licensed under the MIT License (see LICENSE file)

Utility to extract and verify watermarks from PDF files.
"""

from pathlib import Path
from typing import Optional

try:
    from pypdf import PdfReader

    PYPDF_AVAILABLE = True
except ImportError:
    PdfReader = None  # type: ignore
    PYPDF_AVAILABLE = False


def extract_watermark(pdf_path: str) -> Optional[str]:
    """Extract watermark from PDF metadata.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        The watermark text if found, None otherwise.
    """
    if not PYPDF_AVAILABLE:
        print("Error: pypdf is not installed.")
        return None

    try:
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            print(f"Error: File '{pdf_path}' not found.")
            return None

        reader = PdfReader(str(pdf_file))

        # Check standard metadata
        if reader.metadata:
            # Check for our custom watermark field
            if "/MD2PDF_Watermark" in reader.metadata:
                return str(reader.metadata["/MD2PDF_Watermark"])

        # Check XMP metadata if available
        if hasattr(reader, "xmp_metadata"):
            xmp = reader.xmp_metadata
            if xmp:
                # Try to extract from XMP
                # Simplified extraction - parse XML properly in production
                xmp_str = str(xmp)
                if "md2pdf:watermark" in xmp_str:
                    import re

                    match = re.search(
                        r"<md2pdf:watermark>(.*?)</md2pdf:watermark>", xmp_str
                    )
                    if match:
                        return match.group(1)

        return None

    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return None


def verify_watermark(pdf_path: str, expected_watermark: str) -> bool:
    """Verify if a PDF contains the expected watermark.

    Args:
        pdf_path: Path to the PDF file.
        expected_watermark: The watermark text to verify.

    Returns:
        True if the watermark matches, False otherwise.
    """
    extracted = extract_watermark(pdf_path)
    return extracted == expected_watermark


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python watermark_extractor.py <pdf_file>")
        sys.exit(1)

    pdf_file = sys.argv[1]
    watermark = extract_watermark(pdf_file)

    if watermark:
        print(f"✅ Watermark found: {watermark}")
    else:
        print("❌ No watermark found in PDF")
