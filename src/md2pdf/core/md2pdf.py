#!/usr/bin/env python3
"""
MD2PDF - Markdown to PDF Converter
Copyright (c) 2025 MPS Metalmind AB
Licensed under the MIT License (see LICENSE file)
"""

"""
MD2PDF Entry Point
Calls the main md2pdf script from the src/main directory.
"""

import sys
from pathlib import Path

# Add src to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the main function
from md2pdf.core.main.md2pdf import main

if __name__ == "__main__":
    main()
