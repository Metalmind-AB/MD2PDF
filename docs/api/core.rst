Core Module
===========

The core module contains the fundamental classes and functions that power MD2PDF.

Document Processing
------------------

.. autoclass:: md2pdf.core.processor.MarkdownProcessor
   :members:
   :undoc-members:
   :show-inheritance:

   **Example Usage**:

   .. code-block:: python

      from md2pdf.core.processor import MarkdownProcessor

      processor = MarkdownProcessor()
      html_content = processor.process_markdown('# Title\n\nContent here.')

.. autoclass:: md2pdf.core.processor.HTMLProcessor
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: md2pdf.core.processor.PDFGenerator
   :members:
   :undoc-members:
   :show-inheritance:

Configuration Management
------------------------

.. autoclass:: md2pdf.core.config.Config
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: md2pdf.core.config.ConfigLoader
   :members:
   :undoc-members:
   :show-inheritance:

   **Example Usage**:

   .. code-block:: python

      from md2pdf.core.config import ConfigLoader

      loader = ConfigLoader()
      config = loader.load_from_file('.md2pdf.yml')
      
      # Access configuration values
      style = config.get('style', 'technical')
      theme = config.get('theme', 'default')

File Management
--------------

.. autoclass:: md2pdf.core.filesystem.FileManager
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: md2pdf.core.filesystem.ensure_directory

.. autofunction:: md2pdf.core.filesystem.clean_filename

.. autofunction:: md2pdf.core.filesystem.get_file_hash

   **Example Usage**:

   .. code-block:: python

      from md2pdf.core.filesystem import FileManager, ensure_directory

      # Create file manager
      file_manager = FileManager()
      
      # Ensure output directory exists
      ensure_directory('output/pdfs/')
      
      # Get list of markdown files
      md_files = file_manager.find_files('docs/', '*.md')

Template Engine
--------------

.. autoclass:: md2pdf.core.template.TemplateEngine
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: md2pdf.core.template.Template
   :members:
   :undoc-members:
   :show-inheritance:

   **Example Usage**:

   .. code-block:: python

      from md2pdf.core.template import TemplateEngine

      engine = TemplateEngine()
      
      # Render HTML template with content
      html = engine.render_template(
          'document.html',
          title='My Document',
          content=markdown_html,
          style_css=style_css,
          theme_css=theme_css
      )

Asset Management
---------------

.. autoclass:: md2pdf.core.assets.AssetManager
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: md2pdf.core.assets.resolve_asset_path

.. autofunction:: md2pdf.core.assets.copy_assets

   **Example Usage**:

   .. code-block:: python

      from md2pdf.core.assets import AssetManager

      asset_manager = AssetManager()
      
      # Get path to built-in font
      font_path = asset_manager.get_font_path('inter.woff2')
      
      # Process images in markdown
      processed_html = asset_manager.process_images(html_content)

Logging and Debugging
--------------------

.. autoclass:: md2pdf.core.logging.Logger
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: md2pdf.core.logging.setup_logging

.. autofunction:: md2pdf.core.logging.get_logger

   **Example Usage**:

   .. code-block:: python

      from md2pdf.core.logging import get_logger, setup_logging

      # Setup logging
      setup_logging(level='DEBUG', verbose=True)
      
      # Get logger for module
      logger = get_logger(__name__)
      logger.info('Starting conversion process')

Validation
---------

.. autoclass:: md2pdf.core.validation.Validator
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: md2pdf.core.validation.validate_markdown_file

.. autofunction:: md2pdf.core.validation.validate_output_path

.. autofunction:: md2pdf.core.validation.validate_style_theme_combination

   **Example Usage**:

   .. code-block:: python

      from md2pdf.core.validation import validate_markdown_file

      # Validate input file
      is_valid, errors = validate_markdown_file('document.md')
      if not is_valid:
          for error in errors:
              print(f"Validation error: {error}")

Performance Monitoring
---------------------

.. autoclass:: md2pdf.core.performance.PerformanceMonitor
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: md2pdf.core.performance.profile_function

   **Example Usage**:

   .. code-block:: python

      from md2pdf.core.performance import PerformanceMonitor

      monitor = PerformanceMonitor()
      
      with monitor.measure('conversion'):
          # ... conversion code ...
          pass
      
      # Get performance stats
      stats = monitor.get_stats()
      print(f"Conversion took: {stats['conversion']['duration']:.2f}s")

Cache Management
---------------

.. autoclass:: md2pdf.core.cache.CacheManager
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: md2pdf.core.cache.cache_key_for_file

   **Example Usage**:

   .. code-block:: python

      from md2pdf.core.cache import CacheManager

      cache = CacheManager()
      
      # Check if conversion is cached
      cache_key = cache.get_cache_key('document.md', 'modern', 'elegant')
      if cache.has_cached_result(cache_key):
          pdf_data = cache.get_cached_result(cache_key)
      else:
          # Perform conversion and cache result
          pdf_data = perform_conversion()
          cache.store_result(cache_key, pdf_data)

Plugin System
------------

.. autoclass:: md2pdf.core.plugins.PluginManager
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: md2pdf.core.plugins.Plugin
   :members:
   :undoc-members:
   :show-inheritance:

   **Example Usage**:

   .. code-block:: python

      from md2pdf.core.plugins import PluginManager

      plugin_manager = PluginManager()
      
      # Load plugins from directory
      plugin_manager.load_plugins('plugins/')
      
      # Get available plugins
      plugins = plugin_manager.get_available_plugins()
      for plugin in plugins:
          print(f"Plugin: {plugin.name} - {plugin.description}")

Constants and Enums
------------------

.. autoclass:: md2pdf.core.constants.OutputFormat
   :members:

.. autoclass:: md2pdf.core.constants.PageSize
   :members:

.. autodata:: md2pdf.core.constants.DEFAULT_STYLE

.. autodata:: md2pdf.core.constants.DEFAULT_THEME

.. autodata:: md2pdf.core.constants.SUPPORTED_MARKDOWN_EXTENSIONS

.. autodata:: md2pdf.core.constants.DEFAULT_PAGE_MARGINS