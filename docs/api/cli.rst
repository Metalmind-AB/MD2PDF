Command Line Interface
=====================

The CLI module provides the command-line interface for MD2PDF.

Main CLI Function
----------------

.. autofunction:: md2pdf.cli.main

   The main entry point for the MD2PDF command-line interface.

CLI Commands
-----------

.. autofunction:: md2pdf.cli.convert_command

   Handle the main conversion command.

.. autofunction:: md2pdf.cli.list_styles_command

   List available styles.

.. autofunction:: md2pdf.cli.list_themes_command

   List available themes.

.. autofunction:: md2pdf.cli.list_combinations_command

   List all valid style and theme combinations.

Click Groups and Commands
------------------------

.. autoclass:: md2pdf.cli.MD2PDFGroup
   :members:
   :undoc-members:
   :show-inheritance:

Command Options
--------------

.. autoclass:: md2pdf.cli.ConvertOptions
   :members:
   :undoc-members:
   :show-inheritance:

   **Example Usage**:

   .. code-block:: python

      from md2pdf.cli import ConvertOptions

      options = ConvertOptions(
          input_path='document.md',
          output_path='output.pdf',
          style='modern',
          theme='elegant',
          verbose=True
      )

Utility Functions
----------------

.. autofunction:: md2pdf.cli.setup_logging

   Configure logging for the CLI.

.. autofunction:: md2pdf.cli.validate_paths

   Validate input and output paths.

.. autofunction:: md2pdf.cli.handle_batch_processing

   Handle batch processing of multiple files.

   **Example Usage**:

   .. code-block:: python

      from md2pdf.cli import handle_batch_processing

      results = handle_batch_processing(
          pattern='docs/*.md',
          output_dir='pdfs/',
          style='technical',
          theme='dark'
      )

      for result in results:
          print(f"Converted: {result.input_path} -> {result.output_path}")

Output Formatting
----------------

.. autoclass:: md2pdf.cli.OutputFormatter
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: md2pdf.cli.format_style_list

.. autofunction:: md2pdf.cli.format_theme_list

.. autofunction:: md2pdf.cli.format_conversion_results

Error Handling
--------------

.. autofunction:: md2pdf.cli.handle_conversion_error

.. autofunction:: md2pdf.cli.handle_file_error

.. autofunction:: md2pdf.cli.handle_general_error

Progress Reporting
-----------------

.. autoclass:: md2pdf.cli.ProgressReporter
   :members:
   :undoc-members:
   :show-inheritance:

   **Example Usage**:

   .. code-block:: python

      from md2pdf.cli import ProgressReporter

      reporter = ProgressReporter(verbose=True)
      
      reporter.start_batch(total_files=10)
      
      for i in range(10):
          reporter.update_progress(i + 1)
          # ... conversion work ...
      
      reporter.finish_batch()

Configuration Loading
--------------------

.. autofunction:: md2pdf.cli.load_config_file

.. autofunction:: md2pdf.cli.merge_config_with_args

   **Example Usage**:

   .. code-block:: python

      from md2pdf.cli import load_config_file

      # Load configuration from YAML file
      config = load_config_file('.md2pdf.yml')
      print(f"Default style: {config.get('style', 'technical')}")

Completion Support
-----------------

.. autofunction:: md2pdf.cli.style_completion

   Shell completion for style names.

.. autofunction:: md2pdf.cli.theme_completion

   Shell completion for theme names.

Constants and Defaults
---------------------

.. autodata:: md2pdf.cli.DEFAULT_CONFIG_FILE

   Default configuration file name.

.. autodata:: md2pdf.cli.SUPPORTED_INPUT_EXTENSIONS

   List of supported input file extensions.

.. autodata:: md2pdf.cli.DEFAULT_OUTPUT_EXTENSION

   Default output file extension.