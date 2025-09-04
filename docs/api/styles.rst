Styles Module
=============

The styles module handles style and theme management for MD2PDF.

Style Manager
------------

.. autoclass:: md2pdf.core.styles.StyleManager
   :members:
   :undoc-members:
   :show-inheritance:

   **Basic Usage**:

   .. code-block:: python

      from md2pdf import StyleManager

      style_manager = StyleManager()

      # List available styles
      styles = style_manager.list_styles()
      for style in styles:
          print(f"{style.name}: {style.description}")

      # Get style CSS
      css = style_manager.get_style_css('modern')

Theme Manager
------------

.. autoclass:: md2pdf.core.styles.ThemeManager
   :members:
   :undoc-members:
   :show-inheritance:

   **Basic Usage**:

   .. code-block:: python

      from md2pdf import ThemeManager

      theme_manager = ThemeManager()

      # List available themes
      themes = theme_manager.list_themes()
      for theme in themes:
          print(f"{theme.name}: {theme.description}")

Style Information Classes
------------------------

.. autoclass:: md2pdf.core.styles.StyleInfo
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: md2pdf.core.styles.ThemeInfo
   :members:
   :undoc-members:
   :show-inheritance:

Style Loader
-----------

.. autoclass:: md2pdf.core.styles.StyleLoader
   :members:
   :undoc-members:
   :show-inheritance:

   **Advanced Usage**:

   .. code-block:: python

      from md2pdf.core.styles import StyleLoader

      loader = StyleLoader()

      # Load custom style from file
      loader.load_custom_style('/path/to/custom.css')

      # Load custom theme
      loader.load_custom_theme('/path/to/custom_theme.css')

CSS Processor
------------

.. autoclass:: md2pdf.core.styles.CSSProcessor
   :members:
   :undoc-members:
   :show-inheritance:

   **Example Usage**:

   .. code-block:: python

      from md2pdf.core.styles import CSSProcessor

      processor = CSSProcessor()

      # Process and combine CSS
      combined_css = processor.combine_css(
          style_css=style_css,
          theme_css=theme_css,
          custom_css=custom_css
      )

Style Discovery
--------------

.. autofunction:: md2pdf.core.styles.discover_styles

.. autofunction:: md2pdf.core.styles.discover_themes

   **Example Usage**:

   .. code-block:: python

      from md2pdf.core.styles import discover_styles, discover_themes

      # Discover built-in styles
      styles = discover_styles()

      # Discover custom styles in directory
      custom_styles = discover_styles('/path/to/custom/styles/')

      # Discover themes
      themes = discover_themes()

Validation Functions
-------------------

.. autofunction:: md2pdf.core.styles.validate_style

.. autofunction:: md2pdf.core.styles.validate_theme

.. autofunction:: md2pdf.core.styles.validate_combination

   **Example Usage**:

   .. code-block:: python

      from md2pdf.core.styles import validate_combination

      # Check if style and theme work together
      is_valid = validate_combination('modern', 'elegant')
      if not is_valid:
          print("This combination may not work well together")

Exception Classes
----------------

.. autoexception:: md2pdf.exceptions.StyleNotFoundError
   :members:

.. autoexception:: md2pdf.exceptions.ThemeNotFoundError
   :members:

.. autoexception:: md2pdf.exceptions.InvalidStyleError
   :members:

.. autoexception:: md2pdf.exceptions.InvalidThemeError
   :members:

Constants
--------

.. autodata:: md2pdf.core.styles.DEFAULT_STYLE

   Default style name used when no style is specified.

.. autodata:: md2pdf.core.styles.DEFAULT_THEME

   Default theme name used when no theme is specified.

.. autodata:: md2pdf.core.styles.BUILT_IN_STYLES

   List of built-in style names.

.. autodata:: md2pdf.core.styles.BUILT_IN_THEMES

   List of built-in theme names.
