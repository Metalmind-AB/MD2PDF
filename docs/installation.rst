Installation Guide
==================

System Requirements
------------------

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 512MB RAM (minimum), 1GB+ recommended for large documents

System Dependencies
------------------

MD2PDF requires some system libraries for PDF generation. Install these before installing MD2PDF:

macOS
~~~~~

Using Homebrew:

.. code-block:: bash

   brew install cairo pango gdk-pixbuf libffi

Ubuntu/Debian
~~~~~~~~~~~~~

.. code-block:: bash

   sudo apt-get update
   sudo apt-get install build-essential python3-dev python3-pip \
     python3-setuptools python3-wheel python3-cffi libcairo2 \
     libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 \
     libffi-dev shared-mime-info

CentOS/RHEL/Fedora
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # CentOS/RHEL
   sudo yum install gcc python3-devel python3-pip \
     cairo-devel pango-devel gdk-pixbuf2-devel libffi-devel

   # Fedora
   sudo dnf install gcc python3-devel python3-pip \
     cairo-devel pango-devel gdk-pixbuf2-devel libffi-devel

Windows
~~~~~~~

Most dependencies are handled automatically on Windows. You may need:

- **Visual Studio Build Tools** (for some packages)
- **Microsoft C++ Build Tools** (automatically installed with Visual Studio)

Installing MD2PDF
-----------------

From PyPI (Recommended)
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install md2pdf

This will install MD2PDF and all required Python dependencies.

From Source
~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/mps-metalmind/md2pdf.git
   cd md2pdf
   pip install .

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~

For contributing or development:

.. code-block:: bash

   git clone https://github.com/mps-metalmind/md2pdf.git
   cd md2pdf
   pip install -e ".[dev,docs,test]"

This installs MD2PDF in "editable" mode with all development dependencies.

Virtual Environment Setup
-------------------------

It's recommended to use a virtual environment:

.. code-block:: bash

   python -m venv md2pdf-env

   # On Windows
   md2pdf-env\Scripts\activate

   # On macOS/Linux
   source md2pdf-env/bin/activate

   pip install md2pdf

Verifying Installation
---------------------

Test your installation:

.. code-block:: bash

   md2pdf --version
   md2pdf --list-styles
   md2pdf --list-themes

Create a test markdown file and convert it:

.. code-block:: bash

   echo "# Test Document\n\nThis is a **test**." > test.md
   md2pdf test.md

The command should generate ``test.pdf`` in the current directory.

Troubleshooting
--------------

WeasyPrint Installation Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you encounter WeasyPrint-related errors:

1. **Check system dependencies**: Ensure Cairo, Pango, and related libraries are installed
2. **Update pip**: ``pip install --upgrade pip``
3. **Try with --no-cache-dir**: ``pip install --no-cache-dir md2pdf``

Font Issues
~~~~~~~~~~

If fonts don't render correctly:

1. **System fonts**: MD2PDF uses system fonts when Google Fonts aren't available
2. **Internet connection**: Some styles require Google Fonts (internet connection needed)
3. **Font installation**: Install missing fonts on your system

Permission Errors
~~~~~~~~~~~~~~~~

On Unix systems, you might need to install in user space:

.. code-block:: bash

   pip install --user md2pdf

Memory Issues
~~~~~~~~~~~~

For large documents or batch processing:

1. **Increase system memory** if possible
2. **Process files individually** instead of batch processing
3. **Use simpler styles** that require less memory

Common Error Messages
~~~~~~~~~~~~~~~~~~~~

**"Command 'md2pdf' not found"**
   - The installation didn't complete successfully
   - Try reinstalling: ``pip uninstall md2pdf && pip install md2pdf``
   - Check if your PATH includes pip's binary directory

**"No module named 'md2pdf'"**
   - Installation incomplete or virtual environment not activated
   - Reinstall the package

**"WeasyPrint error"**
   - System dependencies missing
   - Follow the system dependency installation instructions above

Getting Help
-----------

If you continue having installation issues:

1. **Check the GitHub Issues**: https://github.com/mps-metalmind/md2pdf/issues
2. **Create a new issue** with details about your system and error messages
3. **Join discussions**: https://github.com/mps-metalmind/md2pdf/discussions

Include this information when reporting issues:

- Operating system and version
- Python version (``python --version``)
- Installation method used
- Complete error message
- Output of ``pip list | grep -i weasy`` or ``pip list | grep -i md2pdf``
