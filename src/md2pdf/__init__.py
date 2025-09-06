#!/usr/bin/env python3
"""
MD2PDF - Markdown to PDF Converter
Copyright (c) 2025 MPS Metalmind AB
Licensed under the MIT License (see LICENSE file)
"""

__version__ = "1.1.0"
__author__ = "MPS Metalmind AB"
__license__ = "MIT"
__email__ = "info@metalmind.se"

# Lazy imports to avoid loading heavy dependencies for simple operations
__all__ = ["MD2PDFConverter", "main", "__version__", "__author__", "__license__"]


from typing import Any


def __getattr__(name: str) -> Any:
    """Lazy loading of main components."""
    if name == "MD2PDFConverter":
        from .core.md2pdf import MD2PDFConverter

        return MD2PDFConverter
    elif name == "main":
        from .core.main import main

        return main
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
