Usage Guide
===========

Command Line Interface
----------------------

The ``md2pdf`` command provides a simple interface for converting Markdown files to PDF.

Basic Syntax
~~~~~~~~~~~~

.. code-block:: bash

   md2pdf [INPUT] [OPTIONS]

**Arguments:**

- ``INPUT``: Input markdown file or glob pattern (optional for batch processing)

**Common Options:**

- ``-o, --output PATH``: Output PDF file or directory
- ``-s, --style STYLE``: Style template (default: technical)
- ``-t, --theme THEME``: Color theme (default: default)
- ``--output-dir PATH``: Output directory for batch processing
- ``--verbose``: Enable verbose output
- ``--help``: Show help message

Single File Conversion
~~~~~~~~~~~~~~~~~~~~~~

Convert a single Markdown file:

.. code-block:: bash

   # Basic conversion
   md2pdf document.md

   # Specify output file
   md2pdf document.md -o custom-name.pdf

   # With custom styling
   md2pdf document.md --style modern --theme elegant

   # All options combined
   md2pdf document.md -o styled-doc.pdf -s whitepaper -t sophisticated --verbose

Batch Processing
~~~~~~~~~~~~~~~

Process multiple files at once:

.. code-block:: bash

   # Convert all .md files in current directory
   md2pdf *.md

   # Process files in specific directory
   md2pdf docs/*.md --output-dir pdfs/

   # Recursive processing (using shell globbing)
   md2pdf **/*.md -s technical -t dark

Listing Available Options
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # List all available styles
   md2pdf --list-styles

   # List all available themes
   md2pdf --list-themes

   # Show all style + theme combinations
   md2pdf --list-combinations

Python API
----------

For programmatic usage, import and use the MD2PDF classes directly.

Basic Usage
~~~~~~~~~~

.. code-block:: python

   from md2pdf import MD2PDFConverter

   # Simple conversion
   converter = MD2PDFConverter()
   converter.convert('document.md', 'output.pdf')

Advanced Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from md2pdf import MD2PDFConverter

   # Configure converter with custom options
   converter = MD2PDFConverter(
       style='modern',
       theme='elegant',
       output_dir='pdfs/',
       verbose=True
   )

   # Convert single file
   converter.convert('document.md')  # Uses auto-generated output name

   # Convert with custom output
   converter.convert('document.md', 'custom-output.pdf')

Batch Processing with Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from md2pdf import MD2PDFConverter
   import glob

   converter = MD2PDFConverter(style='technical', theme='dark')

   # Process multiple files
   markdown_files = glob.glob('docs/*.md')
   for md_file in markdown_files:
       try:
           converter.convert(md_file)
           print(f"Converted: {md_file}")
       except Exception as e:
           print(f"Error converting {md_file}: {e}")

   # Or use built-in batch processing
   converter.convert_batch('docs/*.md', output_dir='pdfs/')

Style and Theme Management
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from md2pdf import StyleManager

   style_manager = StyleManager()

   # Get available styles
   styles = style_manager.list_styles()
   for style in styles:
       print(f"{style.name}: {style.description}")

   # Get available themes
   themes = style_manager.list_themes()
   for theme in themes:
       print(f"{theme.name}: {theme.description}")

   # Check if combination is valid
   is_valid = style_manager.is_valid_combination('modern', 'elegant')
   print(f"Modern + Elegant combination is valid: {is_valid}")

Error Handling
~~~~~~~~~~~~~

.. code-block:: python

   from md2pdf import MD2PDFConverter, ConversionError

   converter = MD2PDFConverter()

   try:
       converter.convert('document.md', 'output.pdf')
   except ConversionError as e:
       print(f"Conversion failed: {e}")
   except FileNotFoundError as e:
       print(f"File not found: {e}")
   except Exception as e:
       print(f"Unexpected error: {e}")

Configuration Files
------------------

MD2PDF supports configuration files for consistent styling across projects.

YAML Configuration
~~~~~~~~~~~~~~~~~

Create a ``.md2pdf.yml`` file in your project directory:

.. code-block:: yaml

   # MD2PDF Configuration
   style: modern
   theme: elegant
   output_dir: pdfs/
   verbose: true

   # File-specific overrides
   overrides:
     "README.md":
       style: whitepaper
       theme: minimal
     "docs/*.md":
       style: technical
       theme: dark

Using Configuration Files
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # MD2PDF automatically detects .md2pdf.yml in current directory
   md2pdf document.md

   # Use specific config file
   md2pdf document.md --config custom-config.yml

Advanced Usage
--------------

Custom CSS Injection
~~~~~~~~~~~~~~~~~~~

Add custom CSS to any conversion:

.. code-block:: python

   from md2pdf import MD2PDFConverter

   custom_css = """
   /* Custom styles */
   body {
       font-family: 'Custom Font', serif;
   }
   .highlight {
       background-color: yellow;
   }
   """

   converter = MD2PDFConverter()
   converter.add_custom_css(custom_css)
   converter.convert('document.md', 'styled-output.pdf')

Metadata Extraction
~~~~~~~~~~~~~~~~~~

Extract document metadata:

.. code-block:: python

   from md2pdf import MD2PDFConverter

   converter = MD2PDFConverter()

   # Get metadata without conversion
   metadata = converter.extract_metadata('document.md')
   print(f"Title: {metadata.get('title', 'Untitled')}")
   print(f"Author: {metadata.get('author', 'Unknown')}")
   print(f"Word count: {metadata.get('word_count', 0)}")

Page Options
~~~~~~~~~~~

Control page layout and formatting:

.. code-block:: python

   from md2pdf import MD2PDFConverter, PageOptions

   page_options = PageOptions(
       size='A4',           # Page size
       margin='2cm',        # Page margins
       orientation='portrait'  # Page orientation
   )

   converter = MD2PDFConverter(page_options=page_options)
   converter.convert('document.md', 'custom-layout.pdf')

Working with Large Documents
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For large documents, use memory-efficient processing:

.. code-block:: python

   from md2pdf import MD2PDFConverter

   # Enable streaming mode for large files
   converter = MD2PDFConverter(
       streaming=True,
       memory_limit='512MB'
   )

   # Process large document
   converter.convert('large-document.md', 'output.pdf')

Integration Examples
-------------------

GitHub Actions
~~~~~~~~~~~~~

Automate PDF generation in GitHub Actions:

.. code-block:: yaml

   name: Generate PDFs
   on: [push, pull_request]

   jobs:
     build-pdfs:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2

         - name: Set up Python
           uses: actions/setup-python@v2
           with:
             python-version: 3.9

         - name: Install system dependencies
           run: |
             sudo apt-get update
             sudo apt-get install -y libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev

         - name: Install MD2PDF
           run: pip install md2pdf

         - name: Generate PDFs
           run: md2pdf docs/*.md --style modern --theme elegant --output-dir dist/

         - name: Upload PDFs
           uses: actions/upload-artifact@v2
           with:
             name: generated-pdfs
             path: dist/*.pdf

Pre-commit Hook
~~~~~~~~~~~~~~

Add PDF generation to pre-commit hooks:

.. code-block:: yaml

   # .pre-commit-config.yaml
   repos:
     - repo: local
       hooks:
         - id: generate-pdf-docs
           name: Generate PDF Documentation
           entry: md2pdf
           args: ['docs/*.md', '--style', 'technical', '--output-dir', 'pdfs/']
           language: system
           files: '\.md$'

Makefile Integration
~~~~~~~~~~~~~~~~~~

Add PDF generation to your Makefile:

.. code-block:: makefile

   # Makefile
   .PHONY: docs pdf clean

   docs: pdf

   pdf:
   	md2pdf docs/*.md --style whitepaper --theme sophisticated --output-dir dist/pdfs/

   clean:
   	rm -rf dist/pdfs/*.pdf

   # Generate specific document types
   technical-docs:
   	md2pdf technical/*.md --style technical --theme dark --output-dir dist/technical/

   user-guides:
   	md2pdf guides/*.md --style modern --theme elegant --output-dir dist/guides/
