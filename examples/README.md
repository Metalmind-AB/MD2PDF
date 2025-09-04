# MD2PDF Examples

This directory contains practical examples demonstrating various features and use cases of MD2PDF.

## Directory Structure

```
examples/
├── README.md              # This file
├── basic_usage/           # Simple conversion examples
├── api_examples/          # Python API usage examples
├── styling/               # Style and theme demonstrations
├── batch_processing/      # Batch conversion examples
├── advanced/              # Advanced features and configurations
└── sample_documents/      # Sample markdown files for testing
```

## Quick Start Examples

### Command Line Usage

```bash
# Convert a single document
md2pdf sample_documents/getting_started.md

# Convert with custom styling
md2pdf sample_documents/technical_doc.md --style modern --theme elegant

# Batch process multiple files
md2pdf sample_documents/*.md --style technical --theme dark
```

### Python API Usage

```python
from md2pdf import MD2PDFConverter

# Simple conversion
converter = MD2PDFConverter()
converter.convert('sample_documents/getting_started.md', 'output.pdf')

# Advanced usage
converter = MD2PDFConverter(
    style='whitepaper',
    theme='sophisticated',
    verbose=True
)
converter.convert_batch('sample_documents/*.md', output_dir='pdfs/')
```

## Running Examples

Each subdirectory contains its own README with specific instructions. To run all examples:

```bash
# Navigate to examples directory
cd examples/

# Run basic examples
cd basic_usage && python run_examples.py

# Run API examples
cd ../api_examples && python api_demo.py

# Run styling examples
cd ../styling && python style_showcase.py

# Run batch processing examples
cd ../batch_processing && python batch_demo.py
```

## Sample Documents

The `sample_documents/` directory contains various markdown files demonstrating different content types:

- **getting_started.md**: Simple introduction document
- **technical_doc.md**: Technical documentation with code blocks
- **academic_paper.md**: Academic paper with citations and references
- **creative_writing.md**: Story/creative content
- **business_report.md**: Business document with charts and tables
- **api_documentation.md**: API reference documentation
- **user_manual.md**: User guide with screenshots and instructions

## Prerequisites

Before running the examples, ensure you have MD2PDF installed:

```bash
pip install md2pdf
```

Or for development:

```bash
pip install -e ".[dev,docs,test]"
```

## Contributing Examples

To contribute new examples:

1. Create a new subdirectory for your example category
2. Add a README.md explaining the example
3. Include sample input files and expected outputs
4. Add any necessary Python scripts
5. Update this main README.md

See [Contributing Guidelines](../docs/contributing.rst) for more details.

## Support

If you have questions about these examples or need help:

- Check the [Documentation](https://md2pdf.readthedocs.io)
- Open an [Issue](https://github.com/mps-metalmind/md2pdf/issues)
- Start a [Discussion](https://github.com/mps-metalmind/md2pdf/discussions)