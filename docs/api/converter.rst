Converter Module
===============

The converter module contains the main conversion functionality for MD2PDF.

MD2PDFConverter Class
--------------------

.. autoclass:: md2pdf.core.converter.MD2PDFConverter
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

.. autoclass:: md2pdf.core.converter.BaseConverter
   :members:
   :undoc-members:
   :show-inheritance:

Conversion Options
-----------------

.. autoclass:: md2pdf.core.converter.ConversionOptions
   :members:
   :undoc-members:
   :show-inheritance:

Page Options
-----------

.. autoclass:: md2pdf.core.converter.PageOptions
   :members:
   :undoc-members:
   :show-inheritance:

   **Example Usage**:

   .. code-block:: python

      from md2pdf import MD2PDFConverter, PageOptions

      page_opts = PageOptions(
          size='A4',
          margin='2cm',
          orientation='portrait'
      )

      converter = MD2PDFConverter(page_options=page_opts)
      converter.convert('document.md', 'output.pdf')

Metadata Extraction
------------------

.. autoclass:: md2pdf.core.metadata.DocumentMetadata
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: md2pdf.core.metadata.extract_metadata

   **Example Usage**:

   .. code-block:: python

      from md2pdf.core.metadata import extract_metadata

      metadata = extract_metadata('document.md')
      print(f"Title: {metadata.title}")
      print(f"Author: {metadata.author}")
      print(f"Word count: {metadata.word_count}")

Exception Classes
----------------

.. autoexception:: md2pdf.exceptions.ConversionError
   :members:

.. autoexception:: md2pdf.exceptions.InvalidInputError
   :members:

.. autoexception:: md2pdf.exceptions.OutputError
   :members:

Utility Functions
----------------

.. autofunction:: md2pdf.core.converter.validate_input_file

.. autofunction:: md2pdf.core.converter.generate_output_path

.. autofunction:: md2pdf.core.converter.cleanup_temp_files