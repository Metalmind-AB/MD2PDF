MD2PDF Documentation
====================

**MD2PDF** is a comprehensive Python tool that converts Markdown files to impeccably beautiful PDFs with professional styling, syntax highlighting, and responsive layout. It features a dynamic style and theme system with automatic discovery and a powerful workflow for batch processing.

.. image:: https://img.shields.io/pypi/v/md2pdf
   :target: https://pypi.org/project/md2pdf/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/md2pdf
   :target: https://pypi.org/project/md2pdf/
   :alt: Python versions

.. image:: https://img.shields.io/github/license/mps-metalmind/md2pdf
   :target: https://github.com/mps-metalmind/md2pdf/blob/main/LICENSE
   :alt: License

Features
--------

✨ **Dynamic Style System**: Multiple beautiful typography templates with automatic discovery

🌈 **Color Theme Engine**: Sophisticated color themes with CSS custom properties  

📝 **Advanced Markdown Support**: Full syntax highlighting, tables, TOC, footnotes

📄 **Professional Layout**: Optimized for A4 paper with proper margins and page breaks

🔄 **Batch Processing**: Process entire folders with a single command

🎯 **Code Block Management**: Proper wrapping and syntax highlighting

📊 **Table Support**: Beautifully formatted tables with alternating row colors

🔗 **Link Styling**: Elegant link formatting with hover effects

Quick Start
-----------

**Installation**

.. code-block:: bash

   pip install md2pdf

**Basic Usage**

.. code-block:: bash

   # Convert a single file
   md2pdf document.md
   
   # With custom styling
   md2pdf document.md --style modern --theme elegant
   
   # Batch processing
   md2pdf *.md --style technical --theme dark

**Python API**

.. code-block:: python

   from md2pdf import MD2PDFConverter
   
   converter = MD2PDFConverter(style='modern', theme='elegant')
   converter.convert('document.md', 'output.pdf')

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   usage
   styles_themes
   examples

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/modules
   api/converter
   api/styles
   api/cli

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`