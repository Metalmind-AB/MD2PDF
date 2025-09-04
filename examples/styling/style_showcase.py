#!/usr/bin/env python3
"""
Style Showcase Example

This script demonstrates all available MD2PDF styles by generating
PDFs with the same content using different style templates.
"""

import sys
from pathlib import Path

# Add the project root to the path so we can import md2pdf
project_root = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(project_root))

from md2pdf import MD2PDFConverter, StyleManager


def create_sample_content():
    """Create comprehensive sample content for style demonstration."""
    return """# Style Showcase Document

This document demonstrates the **{style}** style template with various Markdown elements to show how different content types are rendered.

## Typography Hierarchy

This section shows how different heading levels appear in the **{style}** style.

### Level 3 Heading
Content under level 3 heading with *italic emphasis* and **bold text**.

#### Level 4 Heading
Content under level 4 heading with `inline code` formatting.

##### Level 5 Heading
Content under level 5 heading with [a link](https://github.com/mps-metalmind/md2pdf).

###### Level 6 Heading
The deepest heading level in the hierarchy.

## Text Formatting

This paragraph demonstrates various text formatting options available in Markdown:

- **Bold text** for emphasis
- *Italic text* for subtle emphasis
- `Inline code` for technical terms
- ~~Strikethrough text~~ for corrections
- Normal text for body content

You can combine formatting: **_bold and italic_**, `**bold code**`, and *`italic code`*.

## Code Blocks

Here's how the **{style}** style renders code blocks with syntax highlighting:

### Python Example

```python
from md2pdf import MD2PDFConverter

def convert_document(input_file, output_file, style='{style}'):
    \"\"\"Convert markdown to PDF with specified style.\"\"\"
    converter = MD2PDFConverter(style=style, theme='default')
    try:
        converter.convert(input_file, output_file)
        print(f"✅ Converted {{input_file}} using {{style}} style")
        return True
    except Exception as e:
        print(f"❌ Error: {{e}}")
        return False

# Example usage
success = convert_document('README.md', 'output.pdf', '{style}')
```

### JavaScript Example

```javascript
// MD2PDF JavaScript integration example
const md2pdf = require('md2pdf');

async function convertMarkdown(inputPath, outputPath) {{
    const options = {{
        style: '{style}',
        theme: 'default',
        verbose: true
    }};

    try {{
        await md2pdf.convert(inputPath, outputPath, options);
        console.log(`✅ PDF generated successfully with {{options.style}} style`);
    }} catch (error) {{
        console.error(`❌ Conversion failed: ${{error.message}}`);
    }}
}}

convertMarkdown('document.md', 'output.pdf');
```

### Shell Script Example

```bash
#!/bin/bash
# Batch convert markdown files using {style} style

INPUT_DIR="markdown_files"
OUTPUT_DIR="pdf_output"
STYLE="{style}"

echo "Converting markdown files with $STYLE style..."

for file in "$INPUT_DIR"/*.md; do
    if [[ -f "$file" ]]; then
        filename=$(basename "$file" .md)
        echo "Processing: $filename"
        md2pdf "$file" --style "$STYLE" --output "$OUTPUT_DIR/$filename.pdf"
    fi
done

echo "Conversion complete!"
```

## Lists and Structure

The **{style}** style handles different list types elegantly:

### Unordered Lists

- First level item
- Another first level item with **bold text**
  - Second level nested item
  - Another second level item with *italic text*
    - Third level deeply nested item
    - Another third level item with `code`
- Back to first level with [a link](https://md2pdf.readthedocs.io)

### Ordered Lists

1. First numbered item with detailed explanation
2. Second numbered item with multiple paragraphs

   This is a continuation of the second item with additional details
   that span multiple lines and demonstrate proper formatting.

3. Third numbered item with nested elements:
   - Nested bullet point
   - Another nested point with **emphasis**

4. Fourth numbered item with code example:
   ```python
   print("This is nested code in a list")
   ```

### Mixed Lists

1. Numbered item with bullet subitems:
   - Bullet subitem A
   - Bullet subitem B with `inline code`

2. Another numbered item with more bullets:
   - Complex bullet with **bold** and *italic* text
   - Bullet with [external link](https://github.com)

## Tables

The **{style}** style provides beautiful table formatting:

| Feature | Status | Description | Example |
|---------|--------|-------------|---------|
| **Syntax Highlighting** | ✅ Complete | Full Pygments integration | `python`, `javascript`, `bash` |
| **Table Support** | ✅ Complete | Beautiful table rendering | This table |
| **Typography** | ✅ Complete | Professional font selection | All text |
| **Themes** | ✅ Complete | Multiple color schemes | 10 themes available |
| **CLI Interface** | ✅ Complete | Command-line tool | `md2pdf document.md` |

### Complex Table

| Style | Font Family | Best For | Themes | Rating |
|-------|-------------|----------|--------|--------|
| Technical | Inter + JetBrains Mono | API docs, guides | Default, Dark, Oceanic | ⭐⭐⭐⭐⭐ |
| Modern | Source Serif + JetBrains | Premium docs | Elegant, Sophisticated | ⭐⭐⭐⭐⭐ |
| Whitepaper | Georgia + Consolas | Business docs | Default, Minimal | ⭐⭐⭐⭐ |
| Story | Crimson Text + Fira Code | Creative writing | Sepia, Forest | ⭐⭐⭐⭐ |

## Blockquotes

The **{style}** style renders blockquotes with distinctive formatting:

> This is a blockquote demonstrating how the **{style}** style handles quoted content. Blockquotes are perfect for highlighting important information, testimonials, or citations.

> **Multi-paragraph blockquote:**
>
> This blockquote spans multiple paragraphs to show how the **{style}** style maintains consistent formatting across longer quoted sections.
>
> The second paragraph continues the quote with proper spacing and typography that matches the overall document aesthetic.

### Nested Blockquotes

> This is a parent blockquote that contains nested content:
>
> > This is a nested blockquote within the parent quote, showing how the **{style}** style handles quote hierarchies.
>
> Back to the parent quote level with additional content.

## Images and Media

The **{style}** style handles images responsively:

![Placeholder Image](https://via.placeholder.com/600x300/3366cc/ffffff?text={style}+Style+Demo)

*Caption: Example image showing how the **{style}** style renders images with proper spacing and alignment.*

## Horizontal Rules

The **{style}** style provides elegant horizontal rules for section separation:

---

Content after a horizontal rule continues with proper spacing.

## Special Elements

### Definition Lists

Term 1
: Definition for term 1 with detailed explanation

Term 2
: Definition for term 2 with **bold text**

Complex Term
: Definition with multiple paragraphs

  This definition continues with additional information
  and demonstrates proper formatting.

### Footnotes

This text has a footnote reference[^1] that demonstrates footnote formatting in the **{style}** style.

Here's another footnote[^2] with more complex content.

[^1]: This is the first footnote with simple text.

[^2]: This is the second footnote with **formatting** and `code`.

## Performance Metrics

The **{style}** style is optimized for:

- **Rendering Speed**: Fast CSS processing
- **File Size**: Optimized asset loading
- **Print Quality**: High-resolution output
- **Accessibility**: Proper contrast ratios
- **Compatibility**: Cross-platform support

## Conclusion

The **{style}** style provides professional, readable formatting for all types of Markdown content. From simple text to complex code examples and structured data tables, this style maintains consistent typography and visual hierarchy throughout your documents.

---

*This showcase document was generated using MD2PDF's **{style}** style template.*
"""


def main():
    """Generate style showcase PDFs for all available styles."""
    print("MD2PDF Style Showcase")
    print("=" * 40)

    # Initialize style manager
    style_manager = StyleManager()

    try:
        # Get all available styles
        styles = style_manager.list_styles()
        print(f"Found {len(styles)} available styles")

        # Create output directory
        output_dir = Path("style_showcase_output")
        output_dir.mkdir(exist_ok=True)

        # Generate PDFs for each style
        for i, style in enumerate(styles, 1):
            print(
                f"\n[{i}/{len(styles)}] Generating showcase for '{style.name}' style..."
            )

            # Create content with style name inserted
            content = create_sample_content().format(style=style.name.title())

            # Create temporary markdown file
            temp_md = output_dir / f"temp_{style.name}_showcase.md"
            temp_md.write_text(content)

            # Convert to PDF
            converter = MD2PDFConverter(style=style.name, theme="default")
            output_pdf = output_dir / f"{style.name}_style_showcase.pdf"

            try:
                converter.convert(str(temp_md), str(output_pdf))
                print(f"✅ Generated: {output_pdf}")

                # Clean up temp file
                temp_md.unlink()

            except Exception as e:
                print(f"❌ Failed to generate {style.name} style: {e}")
                # Clean up temp file even on error
                if temp_md.exists():
                    temp_md.unlink()

        print(f"\n🎉 Style showcase complete!")
        print(f"📁 Output directory: {output_dir.absolute()}")
        print(
            f"📄 Generated {len(list(output_dir.glob('*_style_showcase.pdf')))} PDF files"
        )

        # List generated files
        pdf_files = list(output_dir.glob("*_style_showcase.pdf"))
        if pdf_files:
            print("\nGenerated files:")
            for pdf_file in sorted(pdf_files):
                size_kb = pdf_file.stat().st_size / 1024
                print(f"  📄 {pdf_file.name} ({size_kb:.1f} KB)")

    except Exception as e:
        print(f"❌ Error during style showcase generation: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
