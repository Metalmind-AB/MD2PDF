#!/usr/bin/env python3
"""
Simple Conversion Example

This example demonstrates the most basic usage of MD2PDF:
converting a single markdown file to PDF with default settings.
"""

import sys
from pathlib import Path

# Add the project root to the path so we can import md2pdf
project_root = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(project_root))

from md2pdf import MD2PDFConverter  # noqa: E402


def main():
    """Demonstrate simple markdown to PDF conversion."""
    print("MD2PDF - Simple Conversion Example")
    print("=" * 40)

    # Create converter with default settings
    converter = MD2PDFConverter()

    # Define paths
    input_file = Path("../sample_documents/getting_started.md")
    output_file = Path("simple_output.pdf")

    try:
        # Check if input file exists
        if not input_file.exists():
            print(f"⚠️  Input file not found: {input_file}")
            print("Creating a sample input file...")

            # Create a simple sample file
            sample_content = """# Getting Started with MD2PDF

This is a **simple example** document to demonstrate MD2PDF conversion.

## Features

MD2PDF supports:

- **Bold** and *italic* text formatting
- `Inline code` and code blocks
- Lists and numbered items
- Tables and images
- And much more!

## Code Example

```python
from md2pdf import MD2PDFConverter

converter = MD2PDFConverter()
converter.convert('input.md', 'output.pdf')
```

## Conclusion

Converting markdown to beautiful PDFs has never been easier!
"""
            input_file.parent.mkdir(parents=True, exist_ok=True)
            input_file.write_text(sample_content)
            print(f"✓ Created sample file: {input_file}")

        print(f"\n📄 Converting: {input_file}")
        print(f"📁 Output: {output_file}")

        # Perform the conversion
        converter.convert(str(input_file), str(output_file))

        print("✅ Conversion successful!")
        print(f"📄 PDF created: {output_file}")

        # Check output file size
        if output_file.exists():
            size_kb = output_file.stat().st_size / 1024
            print(f"📊 File size: {size_kb:.1f} KB")

    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
