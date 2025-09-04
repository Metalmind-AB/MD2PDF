Changelog
=========

All notable changes to MD2PDF will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[1.0.0] - 2024-09-04
--------------------

Added
~~~~~

- Initial release of MD2PDF
- Core conversion functionality from Markdown to PDF
- Dynamic style system with 7 built-in styles:

  - **Technical**: Clean, professional, code-friendly
  - **Modern**: Sophisticated, elegant, contemporary
  - **Whitepaper**: Academic, authoritative
  - **Story**: Literary, elegant, readable
  - **Academic**: Formal, scholarly, citation-friendly
  - **Consultancy**: Professional business styling
  - **Futuristic**: Modern, cutting-edge typography

- Comprehensive theme system with 10 color themes:

  - **Default**: Clean and professional
  - **Minimal**: Sophisticated, elegant, timeless
  - **Sophisticated**: Refined light design with subtle accents
  - **Elegant**: Sophisticated dark design
  - **Dark**: Light theme with dark containers
  - **Midnight**: High-contrast dark containers
  - **Oceanic**: Cool, calming blue tones
  - **Forest**: Natural, earthy green palette
  - **Sepia**: Warm, vintage book-like colors
  - **Agile**: Modern, dynamic theme for agile development

- Advanced Markdown support:

  - Full syntax highlighting with Pygments
  - Table support with alternating row colors
  - Table of contents generation
  - Footnote support
  - Code block management with proper wrapping
  - Image support with responsive handling
  - Link styling with hover effects
  - List formatting (ordered and unordered)
  - Blockquote styling with left border

- Professional PDF layout:

  - Optimized for A4 paper format
  - Proper margins and page breaks
  - Print-optimized CSS
  - Typography hierarchy
  - Responsive design for different content types

- Command-line interface:

  - Single file conversion
  - Batch processing with glob patterns
  - Style and theme listing commands
  - Verbose output option
  - Configuration file support

- Python API:

  - ``MD2PDFConverter`` class for programmatic usage
  - ``StyleManager`` and ``ThemeManager`` for style/theme management
  - Batch processing capabilities
  - Metadata extraction
  - Error handling with custom exceptions

- Documentation system:

  - Comprehensive Sphinx documentation
  - API reference with examples
  - Installation and usage guides
  - Style and theme reference
  - Contributing guidelines

- Development tools:

  - Pre-commit hooks with code quality checks
  - Black code formatting
  - isort import sorting
  - flake8 linting
  - mypy type checking
  - bandit security analysis
  - pytest test suite with coverage reporting

- Package infrastructure:

  - PyPI-ready package structure
  - GitHub Actions CI/CD pipeline
  - Automated testing on multiple Python versions
  - Code coverage reporting
  - Security scanning

Technical Features
~~~~~~~~~~~~~~~~~

- **CSS Custom Properties**: Dynamic theming with CSS variables
- **Font Management**: Google Fonts integration with system font fallbacks
- **Emoji Support**: Twemoji SVG replacement for robust PDF output
- **Syntax Highlighting**: Embedded Pygments CSS with theme-appropriate contrast
- **Memory Optimization**: Efficient processing for large documents
- **Error Handling**: Comprehensive error reporting and recovery
- **Plugin Architecture**: Extensible plugin system (foundation)
- **Caching System**: Performance optimization for repeated conversions

Performance
~~~~~~~~~~

- Optimized CSS generation and processing
- Efficient HTML to PDF conversion with WeasyPrint
- Memory-conscious handling of large documents
- Fast style and theme discovery
- Cached font loading and asset management

Security
~~~~~~~~

- Input validation and sanitization
- Safe file handling with path traversal protection
- No arbitrary code execution in templates
- Secure handling of external resources
- Comprehensive security scanning with bandit

[Future Releases]
-----------------

Planned
~~~~~~~

- **1.1.0**: Enhanced template system with custom template support
- **1.2.0**: Additional export formats (HTML, EPUB)
- **1.3.0**: Web-based interface and REST API
- **1.4.0**: Plugin marketplace and community templates
- **2.0.0**: Major architecture improvements and breaking changes

Under Consideration
~~~~~~~~~~~~~~~~~~

- Real-time preview functionality
- Collaborative editing features
- Cloud processing capabilities
- Advanced layout options (multi-column, magazine-style)
- Interactive PDF features (forms, annotations)
- Integration with popular documentation platforms

Contributing
-----------

See `Contributing Guidelines <contributing.html>`_ for information on:

- Setting up development environment
- Code style and standards
- Testing requirements
- Documentation standards
- Pull request process

License
-------

This project is licensed under the MIT License - see the `LICENSE <https://github.com/mps-metalmind/md2pdf/blob/main/LICENSE>`_ file for details.

Authors and Acknowledgments
--------------------------

- **MPS Metalmind AB** - Initial development and maintenance
- **Community Contributors** - Bug reports, feature requests, and code contributions

Special thanks to the maintainers of:

- **WeasyPrint** - PDF generation engine
- **Markdown** - Markdown processing
- **Pygments** - Syntax highlighting
- **Click** - Command-line interface framework
