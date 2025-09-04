#!/usr/bin/env python3
"""
MD2Word Entry Point
Calls the main md2word script from the src/main directory.
"""

import sys
from pathlib import Path

# Add src to the Python path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

# Import and run the main function
from main.md2word import main

if __name__ == "__main__":
    main()


