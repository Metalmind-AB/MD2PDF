Utilities Module
================

The utils module provides helper functions and utilities used throughout MD2PDF.

File Utilities
--------------

.. autofunction:: md2pdf.utils.file_utils.ensure_directory_exists

.. autofunction:: md2pdf.utils.file_utils.get_file_extension

.. autofunction:: md2pdf.utils.file_utils.change_extension

.. autofunction:: md2pdf.utils.file_utils.get_relative_path

.. autofunction:: md2pdf.utils.file_utils.is_markdown_file

.. autofunction:: md2pdf.utils.file_utils.find_markdown_files

   **Example Usage**:

   .. code-block:: python

      from md2pdf.utils.file_utils import find_markdown_files, ensure_directory_exists

      # Find all markdown files
      md_files = find_markdown_files('docs/', recursive=True)
      
      # Ensure output directory exists
      ensure_directory_exists('output/pdfs/')

String Utilities
---------------

.. autofunction:: md2pdf.utils.string_utils.slugify

.. autofunction:: md2pdf.utils.string_utils.truncate_string

.. autofunction:: md2pdf.utils.string_utils.sanitize_filename

.. autofunction:: md2pdf.utils.string_utils.extract_title_from_markdown

.. autofunction:: md2pdf.utils.string_utils.count_words

   **Example Usage**:

   .. code-block:: python

      from md2pdf.utils.string_utils import slugify, extract_title_from_markdown

      # Create URL-friendly slug
      slug = slugify("My Document Title!")  # returns "my-document-title"
      
      # Extract title from markdown content
      title = extract_title_from_markdown("# My Title\n\nContent here")

Date and Time Utilities
-----------------------

.. autofunction:: md2pdf.utils.datetime_utils.format_timestamp

.. autofunction:: md2pdf.utils.datetime_utils.get_current_timestamp

.. autofunction:: md2pdf.utils.datetime_utils.parse_date_string

   **Example Usage**:

   .. code-block:: python

      from md2pdf.utils.datetime_utils import format_timestamp

      # Format current time for filename
      timestamp = format_timestamp(format='%Y%m%d_%H%M%S')
      filename = f"document_{timestamp}.pdf"

Color Utilities
--------------

.. autofunction:: md2pdf.utils.color_utils.hex_to_rgb

.. autofunction:: md2pdf.utils.color_utils.rgb_to_hex

.. autofunction:: md2pdf.utils.color_utils.lighten_color

.. autofunction:: md2pdf.utils.color_utils.darken_color

.. autofunction:: md2pdf.utils.color_utils.get_contrast_ratio

.. autofunction:: md2pdf.utils.color_utils.is_light_color

   **Example Usage**:

   .. code-block:: python

      from md2pdf.utils.color_utils import hex_to_rgb, lighten_color

      # Convert hex to RGB
      r, g, b = hex_to_rgb("#3366cc")
      
      # Create lighter version of color
      light_color = lighten_color("#3366cc", 0.2)  # 20% lighter

CSS Utilities
------------

.. autofunction:: md2pdf.utils.css_utils.parse_css_variables

.. autofunction:: md2pdf.utils.css_utils.extract_color_variables

.. autofunction:: md2pdf.utils.css_utils.minify_css

.. autofunction:: md2pdf.utils.css_utils.validate_css

.. autofunction:: md2pdf.utils.css_utils.merge_css_rules

   **Example Usage**:

   .. code-block:: python

      from md2pdf.utils.css_utils import parse_css_variables, minify_css

      # Parse CSS variables from stylesheet
      variables = parse_css_variables(css_content)
      
      # Minify CSS for production
      minified = minify_css(css_content)

HTML Utilities
-------------

.. autofunction:: md2pdf.utils.html_utils.clean_html

.. autofunction:: md2pdf.utils.html_utils.extract_text_from_html

.. autofunction:: md2pdf.utils.html_utils.add_css_to_html

.. autofunction:: md2pdf.utils.html_utils.process_images

.. autofunction:: md2pdf.utils.html_utils.add_table_of_contents

   **Example Usage**:

   .. code-block:: python

      from md2pdf.utils.html_utils import clean_html, add_table_of_contents

      # Clean up HTML content
      clean_content = clean_html(html_content)
      
      # Add table of contents
      html_with_toc = add_table_of_contents(html_content)

Markdown Utilities
-----------------

.. autofunction:: md2pdf.utils.markdown_utils.extract_frontmatter

.. autofunction:: md2pdf.utils.markdown_utils.remove_frontmatter

.. autofunction:: md2pdf.utils.markdown_utils.get_heading_structure

.. autofunction:: md2pdf.utils.markdown_utils.estimate_reading_time

.. autofunction:: md2pdf.utils.markdown_utils.convert_relative_links

   **Example Usage**:

   .. code-block:: python

      from md2pdf.utils.markdown_utils import extract_frontmatter, estimate_reading_time

      # Extract YAML frontmatter
      frontmatter, content = extract_frontmatter(markdown_text)
      
      # Estimate reading time
      minutes = estimate_reading_time(content)
      print(f"Estimated reading time: {minutes} minutes")

Path Utilities
-------------

.. autofunction:: md2pdf.utils.path_utils.resolve_path

.. autofunction:: md2pdf.utils.path_utils.get_project_root

.. autofunction:: md2pdf.utils.path_utils.join_paths

.. autofunction:: md2pdf.utils.path_utils.get_parent_directory

.. autofunction:: md2pdf.utils.path_utils.is_subdirectory

   **Example Usage**:

   .. code-block:: python

      from md2pdf.utils.path_utils import resolve_path, get_project_root

      # Resolve relative path
      full_path = resolve_path('docs/README.md')
      
      # Get project root directory
      root = get_project_root()

Validation Utilities
-------------------

.. autofunction:: md2pdf.utils.validation_utils.is_valid_email

.. autofunction:: md2pdf.utils.validation_utils.is_valid_url

.. autofunction:: md2pdf.utils.validation_utils.is_valid_hex_color

.. autofunction:: md2pdf.utils.validation_utils.validate_file_path

.. autofunction:: md2pdf.utils.validation_utils.validate_directory_path

   **Example Usage**:

   .. code-block:: python

      from md2pdf.utils.validation_utils import is_valid_hex_color, validate_file_path

      # Validate color format
      if is_valid_hex_color("#3366cc"):
          print("Valid color!")
      
      # Validate file path
      is_valid, error = validate_file_path("document.md")

System Utilities
---------------

.. autofunction:: md2pdf.utils.system_utils.get_system_info

.. autofunction:: md2pdf.utils.system_utils.get_available_memory

.. autofunction:: md2pdf.utils.system_utils.get_cpu_count

.. autofunction:: md2pdf.utils.system_utils.is_windows

.. autofunction:: md2pdf.utils.system_utils.is_macos

.. autofunction:: md2pdf.utils.system_utils.is_linux

   **Example Usage**:

   .. code-block:: python

      from md2pdf.utils.system_utils import get_system_info, get_available_memory

      # Get system information
      info = get_system_info()
      print(f"OS: {info['os']}, Python: {info['python_version']}")
      
      # Check available memory
      memory_gb = get_available_memory() / (1024**3)
      print(f"Available memory: {memory_gb:.1f} GB")

Configuration Utilities
-----------------------

.. autofunction:: md2pdf.utils.config_utils.load_yaml_config

.. autofunction:: md2pdf.utils.config_utils.save_yaml_config

.. autofunction:: md2pdf.utils.config_utils.merge_configs

.. autofunction:: md2pdf.utils.config_utils.validate_config

   **Example Usage**:

   .. code-block:: python

      from md2pdf.utils.config_utils import load_yaml_config, merge_configs

      # Load configuration file
      config = load_yaml_config('.md2pdf.yml')
      
      # Merge with default config
      final_config = merge_configs(default_config, user_config)

Template Utilities
------------------

.. autofunction:: md2pdf.utils.template_utils.render_template_string

.. autofunction:: md2pdf.utils.template_utils.get_template_variables

.. autofunction:: md2pdf.utils.template_utils.validate_template

   **Example Usage**:

   .. code-block:: python

      from md2pdf.utils.template_utils import render_template_string

      # Render template with variables
      html = render_template_string(
          template="<h1>{{ title }}</h1>",
          variables={"title": "My Document"}
      )

Error Handling Utilities
------------------------

.. autofunction:: md2pdf.utils.error_utils.format_error_message

.. autofunction:: md2pdf.utils.error_utils.get_error_context

.. autofunction:: md2pdf.utils.error_utils.log_error

   **Example Usage**:

   .. code-block:: python

      from md2pdf.utils.error_utils import format_error_message, log_error

      try:
          # Some operation that might fail
          pass
      except Exception as e:
          formatted_message = format_error_message(e, context="conversion")
          log_error(e, logger)

Constants
--------

.. autodata:: md2pdf.utils.constants.SUPPORTED_IMAGE_FORMATS

.. autodata:: md2pdf.utils.constants.DEFAULT_ENCODING

.. autodata:: md2pdf.utils.constants.MAX_FILE_SIZE

.. autodata:: md2pdf.utils.constants.TEMP_DIRECTORY_PREFIX