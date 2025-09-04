Styles and Themes
=================

MD2PDF features a comprehensive style and theme system that allows you to create professional-looking PDFs with consistent branding and typography.

Understanding Styles vs Themes
------------------------------

**Styles** define the overall layout, typography, spacing, and structural elements:

- Font families and sizes
- Page layout and margins  
- Heading hierarchy
- Code block formatting
- Table styling
- List formatting

**Themes** define the color palette and visual aesthetics:

- Text colors
- Background colors
- Code syntax highlighting colors
- Border and accent colors
- Link colors

Available Styles
---------------

MD2PDF includes several built-in styles optimized for different document types:

Technical
~~~~~~~~

**Best for**: API documentation, technical guides, developer documentation

**Features**:
- Clean, readable typography with Inter font family
- Excellent code block formatting with JetBrains Mono
- Structured heading hierarchy
- Optimized for technical content

.. code-block:: bash

   md2pdf document.md --style technical

Modern
~~~~~~

**Best for**: Premium documentation, presentations, contemporary designs

**Features**:
- Sophisticated typography with Source Serif Pro
- Elegant spacing and layout
- Professional appearance
- Contemporary design aesthetic

.. code-block:: bash

   md2pdf document.md --style modern

Whitepaper
~~~~~~~~~

**Best for**: Research papers, business documents, academic writing

**Features**:
- Academic-style typography
- Authoritative appearance
- Formal document structure
- Citation-friendly formatting

.. code-block:: bash

   md2pdf document.md --style whitepaper

Story
~~~~~

**Best for**: Creative writing, narratives, literary documents

**Features**:
- Literary typography with serif fonts
- Readable paragraph formatting
- First-line paragraph indentation
- Book-like appearance

.. code-block:: bash

   md2pdf document.md --style story

Academic
~~~~~~~~

**Best for**: Research papers, theses, scholarly documents

**Features**:
- Formal scholarly formatting
- Citation-friendly design
- Traditional academic typography
- Structured document hierarchy

.. code-block:: bash

   md2pdf document.md --style academic

Consultancy
~~~~~~~~~~

**Best for**: Business reports, consulting documents, corporate materials

**Features**:
- Professional business styling
- Corporate-friendly typography
- Executive summary formatting
- Clean, authoritative design

.. code-block:: bash

   md2pdf document.md --style consultancy

Futuristic
~~~~~~~~~~

**Best for**: Tech presentations, modern interfaces, innovative designs

**Features**:
- Modern, cutting-edge typography
- Unique visual elements
- Tech-forward styling
- Contemporary aesthetics

.. code-block:: bash

   md2pdf document.md --style futuristic

Available Themes
---------------

Default
~~~~~~

**Type**: Light theme

Clean and professional appearance with standard colors. Perfect for business documents and general use.

.. code-block:: bash

   md2pdf document.md --theme default

Minimal
~~~~~~

**Type**: Light theme

Sophisticated, elegant, and timeless design with subtle colors and clean aesthetics.

.. code-block:: bash

   md2pdf document.md --theme minimal

Sophisticated
~~~~~~~~~~~~

**Type**: Light theme

Refined light design with subtle accents and premium color palette.

.. code-block:: bash

   md2pdf document.md --theme sophisticated

Elegant
~~~~~~

**Type**: Dark theme

Sophisticated dark design with high contrast and premium feel.

.. code-block:: bash

   md2pdf document.md --theme elegant

Dark
~~~~

**Type**: Light theme with dark containers

Light background with dark containers for code and special elements.

.. code-block:: bash

   md2pdf document.md --theme dark

Midnight
~~~~~~~~

**Type**: Light theme with high-contrast dark containers

Similar to Dark theme but with higher contrast for better readability.

.. code-block:: bash

   md2pdf document.md --theme midnight

Oceanic
~~~~~~

**Type**: Light theme

Cool, calming blue tones inspired by ocean colors. Perfect for technical documentation.

.. code-block:: bash

   md2pdf document.md --theme oceanic

Forest
~~~~~~

**Type**: Light theme

Natural, earthy green palette inspired by forest colors. Great for environmental or nature-related content.

.. code-block:: bash

   md2pdf document.md --theme forest

Sepia
~~~~~

**Type**: Light theme

Warm, vintage book-like colors with a classic, timeless feel.

.. code-block:: bash

   md2pdf document.md --theme sepia

Agile
~~~~

**Type**: Light theme

Modern, dynamic theme optimized for agile development and project management documentation.

.. code-block:: bash

   md2pdf document.md --theme agile

Style and Theme Combinations
---------------------------

Not all styles work well with all themes. Here are recommended combinations:

Business and Professional
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Executive documents
   md2pdf report.md --style consultancy --theme sophisticated
   
   # Technical documentation
   md2pdf api-docs.md --style technical --theme oceanic
   
   # Business proposals
   md2pdf proposal.md --style whitepaper --theme minimal

Academic and Research
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Research papers
   md2pdf paper.md --style academic --theme default
   
   # Thesis documents
   md2pdf thesis.md --style whitepaper --theme sophisticated
   
   # Literature reviews
   md2pdf review.md --style story --theme sepia

Creative and Design
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Creative portfolios
   md2pdf portfolio.md --style modern --theme elegant
   
   # Design documentation
   md2pdf design-system.md --style futuristic --theme midnight
   
   # Storytelling
   md2pdf story.md --style story --theme sepia

Technical and Development
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # API documentation
   md2pdf api.md --style technical --theme dark
   
   # User guides
   md2pdf guide.md --style modern --theme oceanic
   
   # Code documentation
   md2pdf code-docs.md --style technical --theme midnight

Customizing Styles and Themes
-----------------------------

Creating Custom Styles
~~~~~~~~~~~~~~~~~~~~~~

You can create custom styles by adding CSS files to the styles directory:

1. Create a new CSS file in ``src/md2pdf/styles/templates/``
2. Add a descriptive comment at the top:

.. code-block:: css

   /* Custom Business Style - Professional corporate styling */
   
   @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
   
   :root {
       --font-body: 'Inter', sans-serif;
       --font-heading: 'Inter', sans-serif;
       --font-code: 'JetBrains Mono', monospace;
       --font-size-base: 11pt;
       --line-height-base: 1.6;
       /* ... other variables */
   }
   
   /* Your custom styles here */

3. The style will be automatically discovered and available

Creating Custom Themes
~~~~~~~~~~~~~~~~~~~~~~

Create custom themes by adding CSS files to the themes directory:

1. Create a new CSS file in ``src/md2pdf/styles/themes/``
2. Add a descriptive comment:

.. code-block:: css

   /* Corporate Blue Theme - Professional blue color scheme */
   
   :root {
       --theme-primary: #1e40af;
       --theme-secondary: #3b82f6;
       --theme-text: #1f2937;
       --theme-background: #ffffff;
       --theme-surface: #f8fafc;
       --theme-border: #e5e7eb;
       --theme-code-bg: #f1f5f9;
       --theme-code-text: #334155;
       /* ... other theme variables */
   }

3. The theme will be automatically discovered

CSS Variables Reference
~~~~~~~~~~~~~~~~~~~~~~

**Typography Variables**:

- ``--font-body``: Main body font
- ``--font-heading``: Heading font
- ``--font-code``: Monospace font for code
- ``--font-size-base``: Base font size
- ``--line-height-base``: Base line height

**Color Variables**:

- ``--theme-primary``: Primary accent color
- ``--theme-secondary``: Secondary accent color
- ``--theme-text``: Main text color
- ``--theme-background``: Page background
- ``--theme-surface``: Surface/container background
- ``--theme-border``: Border color
- ``--theme-code-bg``: Code block background
- ``--theme-code-text``: Code block text color

**Layout Variables**:

- ``--page-margin``: Page margins
- ``--content-width``: Content width
- ``--heading-spacing``: Heading spacing
- ``--paragraph-spacing``: Paragraph spacing

Advanced Styling
---------------

Print-Specific CSS
~~~~~~~~~~~~~~~~

MD2PDF supports print-specific CSS for fine-tuning PDF output:

.. code-block:: css

   @media print {
       /* Page-specific styles */
       @page {
           size: A4;
           margin: 2cm;
       }
       
       /* Avoid page breaks inside elements */
       h1, h2, h3, h4, h5, h6 {
           page-break-after: avoid;
       }
       
       /* Force page breaks */
       .page-break {
           page-break-before: always;
       }
   }

Code Syntax Highlighting
~~~~~~~~~~~~~~~~~~~~~~~

Each theme includes optimized syntax highlighting:

.. code-block:: css

   /* Custom syntax highlighting */
   .codehilite .k  { color: #0000ff; font-weight: bold; } /* Keyword */
   .codehilite .s  { color: #008000; }                    /* String */
   .codehilite .c  { color: #808080; font-style: italic; } /* Comment */
   .codehilite .n  { color: #000000; }                    /* Name */

Testing Your Custom Styles
~~~~~~~~~~~~~~~~~~~~~~~~~~

Test your custom styles:

.. code-block:: bash

   # Test with a sample document
   md2pdf test.md --style your-custom-style --theme your-custom-theme
   
   # List your custom styles
   md2pdf --list-styles
   
   # List your custom themes
   md2pdf --list-themes

Best Practices
-------------

Style Selection
~~~~~~~~~~~~~~

1. **Match content type**: Use Technical for code docs, Academic for papers
2. **Consider audience**: Modern for executives, Technical for developers
3. **Think about branding**: Choose styles that match your organization
4. **Test readability**: Ensure text is readable in your target format

Theme Selection
~~~~~~~~~~~~~

1. **Consider printing**: Light themes usually print better
2. **Match brand colors**: Choose themes that complement your brand
3. **Think about accessibility**: Ensure sufficient contrast
4. **Test on different devices**: Some themes work better on screen vs print

Performance Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Font loading**: Custom fonts may slow down generation
2. **Complex CSS**: Simpler styles generate faster
3. **Image processing**: Minimize complex image transformations
4. **Memory usage**: Some combinations use more memory

Troubleshooting
--------------

Common Style Issues
~~~~~~~~~~~~~~~~~~

**Fonts not loading**:
- Check internet connection (for Google Fonts)
- Verify font names are correct
- Consider using system fonts as fallback

**Layout problems**:
- Check CSS syntax in custom styles
- Verify all required CSS variables are defined
- Test with simpler styles first

**Color issues**:
- Ensure sufficient contrast between text and background
- Test theme with different content types
- Check color values are valid CSS colors

Getting Help
~~~~~~~~~~~

1. Check existing style files for examples
2. Review the CSS variables reference
3. Test combinations with sample documents
4. Report issues on GitHub with style/theme details