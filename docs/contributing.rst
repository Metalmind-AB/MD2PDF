Contributing to MD2PDF
=====================

We welcome contributions to MD2PDF! This guide will help you get started with contributing code, documentation, styles, themes, and bug reports.

Getting Started
--------------

Development Setup
~~~~~~~~~~~~~~~~

1. **Fork and clone the repository**:

.. code-block:: bash

   git clone https://github.com/yourusername/md2pdf.git
   cd md2pdf

2. **Set up development environment**:

.. code-block:: bash

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install in development mode with all dependencies
   pip install -e ".[dev,docs,test]"

3. **Install pre-commit hooks**:

.. code-block:: bash

   pre-commit install

4. **Verify setup**:

.. code-block:: bash

   pytest
   md2pdf --version

Types of Contributions
---------------------

Code Contributions
~~~~~~~~~~~~~~~~~

We welcome improvements to:

- Core conversion functionality
- CLI interface enhancements
- Performance optimizations
- Bug fixes
- New features

Documentation
~~~~~~~~~~~~

Help improve:

- User guides and tutorials
- API documentation
- Installation instructions
- Example code
- README and project documentation

Styles and Themes
~~~~~~~~~~~~~~~~

Contribute new:

- Style templates for different document types
- Color themes for various use cases
- Improvements to existing styles
- Print optimization

Bug Reports and Feature Requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Report bugs with detailed reproduction steps
- Suggest new features with use cases
- Request improvements to existing functionality

Development Workflow
-------------------

Branch Strategy
~~~~~~~~~~~~~~

- ``main``: Stable release branch
- ``develop``: Development branch for new features
- ``feature/*``: Feature development branches
- ``fix/*``: Bug fix branches
- ``docs/*``: Documentation update branches

Making Changes
~~~~~~~~~~~~~

1. **Create a feature branch**:

.. code-block:: bash

   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description

2. **Make your changes**:

- Write clean, readable code
- Follow existing code style
- Add tests for new functionality
- Update documentation as needed

3. **Test your changes**:

.. code-block:: bash

   # Run full test suite
   pytest

   # Run specific tests
   pytest tests/test_converter.py

   # Test code quality
   pre-commit run --all-files

   # Test documentation
   cd docs && make html

4. **Commit your changes**:

.. code-block:: bash

   git add .
   git commit -m "feat: add new feature description"

   # Use conventional commit format:
   # feat: new features
   # fix: bug fixes
   # docs: documentation changes
   # style: formatting, no code change
   # refactor: code change that neither fixes bug nor adds feature
   # test: adding missing tests
   # chore: updating grunt tasks etc; no production code change

5. **Push and create pull request**:

.. code-block:: bash

   git push origin feature/your-feature-name

Then create a pull request on GitHub.

Code Style and Standards
-----------------------

Python Code Style
~~~~~~~~~~~~~~~~

We follow PEP 8 and use these tools:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

.. code-block:: bash

   # Format code
   black src/ tests/

   # Sort imports
   isort src/ tests/

   # Check linting
   flake8 src/ tests/

   # Type checking
   mypy src/

Type Hints
~~~~~~~~~

Use type hints for all public functions:

.. code-block:: python

   from typing import Optional, Dict, List
   from pathlib import Path

   def convert_file(
       input_path: Path,
       output_path: Optional[Path] = None,
       style: str = "technical",
       theme: str = "default"
   ) -> Dict[str, str]:
       """Convert a markdown file to PDF.

       Args:
           input_path: Path to input markdown file
           output_path: Path for output PDF (optional)
           style: Style template name
           theme: Theme name

       Returns:
           Dictionary with conversion results

       Raises:
           ConversionError: If conversion fails
       """

Documentation Style
~~~~~~~~~~~~~~~~~~

Use Google-style docstrings:

.. code-block:: python

   def example_function(param1: str, param2: int) -> bool:
       """Example function with types documented in the docstring.

       Args:
           param1: The first parameter.
           param2: The second parameter.

       Returns:
           The return value. True for success, False otherwise.

       Raises:
           ValueError: If param1 is empty.
       """

Testing
-------

Test Requirements
~~~~~~~~~~~~~~~~

- Write tests for all new functionality
- Maintain or improve test coverage
- Include both unit and integration tests
- Test edge cases and error conditions

Running Tests
~~~~~~~~~~~~

.. code-block:: bash

   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=md2pdf --cov-report=html

   # Run specific test file
   pytest tests/test_converter.py

   # Run tests matching pattern
   pytest -k "test_conversion"

   # Run tests with verbose output
   pytest -v

Test Structure
~~~~~~~~~~~~~

.. code-block:: python

   import pytest
   from pathlib import Path
   from md2pdf import MD2PDFConverter


   class TestConverter:
       def test_basic_conversion(self, tmp_path):
           """Test basic markdown to PDF conversion."""
           # Setup
           input_file = tmp_path / "test.md"
           input_file.write_text("# Test Document\n\nThis is a test.")

           output_file = tmp_path / "test.pdf"

           # Execute
           converter = MD2PDFConverter()
           converter.convert(str(input_file), str(output_file))

           # Assert
           assert output_file.exists()
           assert output_file.stat().st_size > 0

       def test_invalid_input(self):
           """Test error handling for invalid input."""
           converter = MD2PDFConverter()

           with pytest.raises(FileNotFoundError):
               converter.convert("nonexistent.md", "output.pdf")

Adding Styles and Themes
-----------------------

Creating New Styles
~~~~~~~~~~~~~~~~~~

1. **Create the CSS file**:

.. code-block:: bash

   # Create new style file
   touch src/md2pdf/styles/templates/mystyle.css

2. **Add style metadata**:

.. code-block:: css

   /* My Custom Style - Brief description of the style */

   @import url('https://fonts.googleapis.com/css2?family=YourFont:wght@400;700&display=swap');

   :root {
       --font-body: 'YourFont', sans-serif;
       --font-heading: 'YourFont', sans-serif;
       --font-code: 'JetBrains Mono', monospace;
       /* Add other CSS variables */
   }

3. **Test the style**:

.. code-block:: bash

   md2pdf test.md --style mystyle --theme default

4. **Add tests**:

.. code-block:: python

   def test_custom_style():
       """Test custom style renders correctly."""
       converter = MD2PDFConverter(style='mystyle')
       # Test conversion...

Creating New Themes
~~~~~~~~~~~~~~~~~~

1. **Create theme file**:

.. code-block:: bash

   touch src/md2pdf/styles/themes/mytheme.css

2. **Define theme colors**:

.. code-block:: css

   /* My Custom Theme - Brief description */

   :root {
       --theme-primary: #your-primary-color;
       --theme-secondary: #your-secondary-color;
       --theme-text: #your-text-color;
       --theme-background: #your-bg-color;
       /* Add other theme variables */
   }

3. **Test with multiple styles**:

.. code-block:: bash

   md2pdf test.md --style technical --theme mytheme
   md2pdf test.md --style modern --theme mytheme

Documentation Contributions
--------------------------

Building Documentation
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   cd docs
   make html

   # View documentation
   open _build/html/index.html  # macOS
   xdg-open _build/html/index.html  # Linux

Documentation Structure
~~~~~~~~~~~~~~~~~~~~~~

- ``docs/index.rst``: Main documentation index
- ``docs/installation.rst``: Installation guide
- ``docs/usage.rst``: Usage examples
- ``docs/styles_themes.rst``: Style and theme reference
- ``docs/api/``: API documentation
- ``docs/examples/``: Example code and tutorials

Writing Guidelines
~~~~~~~~~~~~~~~~~

- Use clear, concise language
- Include code examples
- Test all example code
- Link to related sections
- Keep sections focused and organized

Pull Request Process
-------------------

PR Guidelines
~~~~~~~~~~~~

1. **Clear description**: Explain what the PR does and why
2. **Reference issues**: Link to related issues
3. **Test coverage**: Include tests for new features
4. **Documentation**: Update docs for user-facing changes
5. **Changelog**: Add entry to CHANGELOG.md for notable changes

PR Template
~~~~~~~~~~

.. code-block:: markdown

   ## Description
   Brief description of changes made.

   ## Type of Change
   - [ ] Bug fix (non-breaking change which fixes an issue)
   - [ ] New feature (non-breaking change which adds functionality)
   - [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
   - [ ] Documentation update

   ## Testing
   - [ ] Tests pass locally
   - [ ] New tests added for new functionality
   - [ ] Manual testing completed

   ## Documentation
   - [ ] Documentation updated
   - [ ] Examples updated

   ## Checklist
   - [ ] Code follows project style guidelines
   - [ ] Self-review of code completed
   - [ ] Code is properly commented
   - [ ] Changes generate no new warnings

Review Process
~~~~~~~~~~~~~

1. **Automated checks**: All CI checks must pass
2. **Code review**: At least one maintainer review required
3. **Testing**: Verify tests cover new functionality
4. **Documentation**: Check that docs are updated appropriately

Community Guidelines
-------------------

Code of Conduct
~~~~~~~~~~~~~~

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

Getting Help
~~~~~~~~~~~

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: info@metalmind.se for direct contact

Recognition
~~~~~~~~~~

Contributors are recognized in:

- ``AUTHORS`` file
- Release notes for significant contributions
- GitHub contributor statistics

Release Process
--------------

Versioning
~~~~~~~~~

We use Semantic Versioning (SemVer):

- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

Release Workflow
~~~~~~~~~~~~~~~

1. Update version in ``pyproject.toml``
2. Update ``CHANGELOG.md``
3. Create release PR
4. Tag release after merge
5. GitHub Actions handles PyPI publication

Development Roadmap
------------------

Current Priorities
~~~~~~~~~~~~~~~~~

- Performance improvements for large documents
- Additional export formats (HTML, EPUB)
- Enhanced template system
- Better error handling and logging
- Improved CLI experience

Future Goals
~~~~~~~~~~~

- Web-based interface
- Template marketplace
- Advanced layout options
- Plugin system
- Cloud processing capabilities

Thank You
---------

Thank you for contributing to MD2PDF! Your contributions help make document conversion better for everyone.

For questions about contributing, please:

- Open a GitHub issue
- Start a GitHub discussion
- Email the maintainers

We appreciate your time and effort in making MD2PDF better!
