Converter Module
===============

The converter module contains the main conversion functionality for MD2PDF.

MD2PDFConverter Class
--------------------

.. autoclass:: md2pdf.core.converters.pdf_converter.PDFConverter
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__

   **Basic Usage**:

   .. code-block:: python

      from md2pdf import MD2PDFConverter

      # Simple conversion
      converter = MD2PDFConverter()
      converter.convert('input.md', 'output.pdf')

      # With styling
      converter = MD2PDFConverter(style='modern', theme='elegant')
      converter.convert('input.md', 'styled_output.pdf')

   **Batch Processing**:

   .. code-block:: python

      # Process multiple files
      converter.convert_batch('docs/*.md', output_dir='pdfs/')

Base Converter
--------------

.. autoclass:: md2pdf.core.converters.base_converter.BaseConverter
   :members:
   :undoc-members:
   :show-inheritance:

Word Converter
--------------

.. autoclass:: md2pdf.core.converters.word_converter.WordConverter
   :members:
   :undoc-members:
   :show-inheritance:

   **Example Usage**:

   .. code-block:: python

      from md2pdf.core.converters.word_converter import WordConverter

      converter = WordConverter(
          input_file="document.md",
          output_file="document.docx",
          style="technical"
      )
      converter.convert()
