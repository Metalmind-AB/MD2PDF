#!/usr/bin/env python3
"""Generate reflowable HTML for Kindle/EPUB conversion."""

import sys

sys.path.insert(0, "src")

from md2pdf.core.processors.markdown_processor import MarkdownProcessor


def create_reflowable_html(input_file: str, output_file: str):
    """Convert markdown to reflowable HTML with Kindle-friendly styling."""

    # Read markdown content
    with open(input_file, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Process markdown to HTML
    processor = MarkdownProcessor()
    html_content = processor.process_markdown(markdown_content)

    # Create reflowable-friendly CSS
    reflowable_css = """
    <style>
        /* Reflowable eBook styles based on amazon_book */
        body {
            font-family: Georgia, 'Times New Roman', serif;
            line-height: 1.6;
            color: #000000;
            margin: 0;
            padding: 0;
        }

        /* Headings */
        h1 {
            font-size: 2em;
            font-weight: 300;
            text-align: center;
            margin: 1.5em 0 1em 0;
            page-break-before: always;
            page-break-after: avoid;
        }

        h2 {
            font-size: 1.5em;
            font-weight: 400;
            margin: 1.5em 0 0.8em 0;
            text-align: center;
            page-break-after: avoid;
        }

        h3 {
            font-size: 1.3em;
            font-weight: 600;
            margin: 1.2em 0 0.6em 0;
            page-break-after: avoid;
        }

        h4, h5, h6 {
            font-size: 1.1em;
            font-weight: 600;
            font-style: italic;
            margin: 1em 0 0.5em 0;
            page-break-after: avoid;
        }

        /* Paragraphs */
        p {
            margin: 0 0 0.8em 0;
            text-align: left;
            text-indent: 0;
        }

        /* No indent for centered text */
        p[style*="text-align: center"] {
            text-indent: 0;
        }

        /* Links */
        a {
            color: #000000;
            text-decoration: underline;
        }

        /* Lists */
        ul, ol {
            margin: 0.8em 0;
            padding-left: 1.5em;
        }

        li {
            margin: 0.4em 0;
        }

        /* Blockquotes */
        blockquote {
            margin: 1em 1.5em;
            padding-left: 1em;
            border-left: 2px solid #4a4a4a;
            font-style: italic;
            color: #4a4a4a;
        }

        /* Code - simplified for reflowable */
        pre {
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            background: #f5f5f5;
            padding: 0.5em;
            margin: 0.8em 0;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        code {
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
            background: #f5f5f5;
            padding: 0.1em 0.3em;
        }

        /* Tables - simplified */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1em 0;
            font-size: 0.9em;
        }

        th {
            font-weight: 600;
            text-align: left;
            padding: 0.5em;
            border-bottom: 1px solid #000000;
            background: #f5f5f5;
        }

        td {
            padding: 0.4em 0.5em;
            border-bottom: 1px solid #d0d0d0;
        }

        /* Images */
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 1em auto;
        }

        /* Page breaks */
        .page-break {
            page-break-before: always;
        }

        /* Remove decorative elements for reflowable */
        h1::before, h1::after,
        h2::after,
        hr::after {
            display: none;
        }

        hr {
            border: none;
            border-top: 1px solid #d0d0d0;
            margin: 1.5em 0;
        }
    </style>
    """

    # Create complete HTML document
    html_document = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Velocity Framework</title>
    {reflowable_css}
</head>
<body>
    {html_content}
</body>
</html>"""

    # Write output
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_document)

    print(f"✅ Reflowable HTML created: {output_file}")
    print("\nNext steps for Kindle/EPUB:")
    print("1. For Kindle: Use Kindle Previewer or Calibre to convert HTML to MOBI/AZW3")
    print("2. For EPUB: Use Calibre or Pandoc to convert HTML to EPUB")
    print("3. The styling will adapt to different screen sizes and user preferences")


if __name__ == "__main__":
    create_reflowable_html(
        "data/input/The_Velocity_Framework.md", "The_Velocity_Framework_reflowable.html"
    )
