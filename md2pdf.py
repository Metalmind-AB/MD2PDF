#!/usr/bin/env python3
"""
MD2PDF - Beautiful Markdown to PDF Converter
A comprehensive tool for converting Markdown files to professionally formatted PDFs
with custom styling, syntax highlighting, and responsive layout.
"""

import argparse
import os
import sys
import shutil
from pathlib import Path
from typing import Optional, List, Tuple
import markdown
from weasyprint import HTML
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter
import re
import base64
from datetime import datetime
from style_loader import style_loader

class MD2PDFConverter:
    """Main converter class for transforming Markdown to beautiful PDFs."""
    
    def __init__(self, input_file: str, output_file: Optional[str] = None, style: str = 'technical', theme: str = 'default', include_header: bool = False):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file) if output_file else self._generate_output_path()
        self.style_name = style
        self.theme_name = theme
        self.include_header = include_header
        self.css_styles = style_loader.combine_style_and_theme(style, theme)
        # Include Pygments CSS so class-based highlighting renders consistently across themes
        try:
            self.pygments_css = HtmlFormatter(style='default').get_style_defs('.codehilite')
        except Exception:
            self.pygments_css = ''
        
    def _generate_output_path(self) -> Path:
        """Generate output PDF path based on input file."""
        return self.input_file.with_suffix('.pdf')
    
    def _get_css_styles(self) -> str:
        """Get comprehensive CSS styles for beautiful PDF formatting."""
        # This method is now deprecated in favor of dynamic style loading
        return self.css_styles
    
    def _highlight_code_blocks(self, html_content: str) -> str:
        """Apply syntax highlighting to code blocks in HTML content."""
        # Pattern to match code blocks with language specification
        code_block_pattern = r'<pre><code class="language-(\w+)">(.*?)</code></pre>'
        
        def replace_code_block(match):
            language = match.group(1)
            code = match.group(2)
            
            try:
                lexer = get_lexer_by_name(language, stripall=True)
            except:
                lexer = TextLexer()
            
            formatter = HtmlFormatter(style='default', noclasses=False)
            highlighted_code = highlight(code, lexer, formatter)
            
            # Extract the inner <pre> content and wrap it to ensure backgrounds and spacing apply
            highlighted_content = re.search(r'<pre>(.*?)</pre>', highlighted_code, re.DOTALL)
            inner = highlighted_content.group(1) if highlighted_content else highlighted_code
            return f'<div class="codehilite"><pre>{inner}</pre></div>'
        
        return re.sub(code_block_pattern, replace_code_block, html_content, flags=re.DOTALL)
    
    def _replace_emojis_with_images(self, html_content: str) -> str:
        """Replace emoji grapheme clusters with Twemoji SVG images for robust PDF rendering."""
        from html import escape
        import emoji
        from pathlib import Path

        def to_twemoji_codepoints(grapheme: str) -> str:
            """Return hyphen-joined lowercase hex codepoints for a grapheme cluster.
            Keeps VS16 (FE0F) and ZWJ (200D) so sequences match Twemoji asset names.
            """
            return '-'.join(f"{ord(ch):x}" for ch in grapheme)

        def normalize_candidates(codepoints: str) -> list:
            """Generate plausible Twemoji filename variants for a codepoint string.
            Order is chosen to prefer local base assets where available.
            - original
            - remove FE0F/FE0E tokens cleanly
            - FE0E→FE0F swap
            - append FE0F at end
            - insert FE0F after first codepoint
            - keycaps: ensure FE0F before 20E3
            """
            candidates: list[str] = []
            def add(c: str):
                if c and c not in candidates:
                    candidates.append(c)

            add(codepoints)

            parts = codepoints.split('-') if codepoints else []
            # Remove FE variants by token
            parts_no_fe = [p for p in parts if p not in ('fe0f', 'fe0e')]
            if parts_no_fe:
                add('-'.join(parts_no_fe))

            # FE0E → FE0F swap
            if 'fe0e' in parts:
                swapped = '-'.join(['fe0f' if p == 'fe0e' else p for p in parts])
                add(swapped)

            has_fe0f = 'fe0f' in parts
            if parts and not has_fe0f:
                # append FE0F at end
                add('-'.join(parts + ['fe0f']))
                # insert FE0F after first
                add('-'.join([parts[0], 'fe0f', *parts[1:]]))

            # Keycap: ensure FE0F before 20e3
            if parts and parts[-1] == '20e3' and 'fe0f' not in parts[:-1]:
                add('-'.join([*parts[:-1], 'fe0f', parts[-1]]))

            return candidates

        local_svg_root = Path("assets/twemoji/svg")

        def replacement(grapheme: str, data_dict=None):
            base = to_twemoji_codepoints(grapheme)
            for candidate in normalize_candidates(base):
                local_path = local_svg_root / f"{candidate}.svg"
                if local_path.exists():
                    src = f"assets/twemoji/svg/{candidate}.svg"
                    break
            else:
                # Fallback to CDN with first candidate
                src = f"https://twemoji.maxcdn.com/v/latest/svg/{normalize_candidates(base)[0]}.svg"
            return (
                f'<img class="emoji" draggable="false" alt="{escape(grapheme)}" '
                f'src="{src}" style="width:1em;height:1em;vertical-align:-0.15em;margin:0 0.05em;" />'
            )

        return emoji.replace_emoji(html_content, replace=replacement)
    
    def _process_markdown(self, content: str) -> str:
        """Convert Markdown content to HTML with extensions."""

        
        extensions = [
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list',
            'markdown.extensions.footnotes',
            'markdown.extensions.smarty'
        ]
        
        extension_configs = {
            'codehilite': {
                'css_class': 'codehilite',
                'use_pygments': True,
                'noclasses': False,
                'linenums': False
            },
            'toc': {
                'permalink': True,
                'title': 'Table of Contents'
            }
        }
        
        md = markdown.Markdown(extensions=extensions, extension_configs=extension_configs)
        html = md.convert(content)
        
        # Apply custom syntax highlighting
        html = self._highlight_code_blocks(html)
        
        # Replace emojis with Twemoji images to avoid Apple Color Emoji font issues
        html = self._replace_emojis_with_images(html)
        
        return html
    
    def _process_header_content(self) -> Tuple[Optional[str], Optional[str]]:
        """Process header folder for logo and text content."""
        header_dir = Path('header')
        logo_html = None
        text_html = None
        
        if not header_dir.exists():
            return None, None
        
        # Check for logo image
        logo_extensions = ['.png', '.jpg', '.jpeg', '.svg', '.gif']
        for ext in logo_extensions:
            logo_files = list(header_dir.glob(f'*{ext}'))
            if logo_files:
                logo_file = logo_files[0]  # Use first found logo
                # Convert to base64 for embedding
                with open(logo_file, 'rb') as f:
                    logo_data = f.read()
                    mime_type = {
                        '.png': 'image/png',
                        '.jpg': 'image/jpeg',
                        '.jpeg': 'image/jpeg',
                        '.svg': 'image/svg+xml',
                        '.gif': 'image/gif'
                    }[logo_file.suffix.lower()]
                    logo_base64 = base64.b64encode(logo_data).decode('utf-8')
                    logo_html = f'<img src="data:{mime_type};base64,{logo_base64}" class="header-logo" alt="Logo">'
                break
        
        # Check for text content
        text_files = list(header_dir.glob('*.md'))
        if text_files:
            text_file = text_files[0]  # Use first found markdown file
            with open(text_file, 'r', encoding='utf-8') as f:
                text_content = f.read()
                # Replace #date# placeholder with current date
                today = datetime.now().strftime('%d %b %Y')
                text_content = text_content.replace('#date#', today)
                # Convert markdown to HTML
                text_html = markdown.markdown(text_content)
        
        return logo_html, text_html
    
    def _generate_header_css(self) -> str:
        """Generate CSS for header positioning and styling."""
        return """
        /* Adjust page setup for header - increase top margin */
        @page {
            margin-top: 3.5cm !important;  /* Increase from 2.5cm to make room for header */
        }
        
        /* Header wrapper that becomes a running element */
        .header-wrapper {
            position: running(header);
            width: 100%;
            margin: 0;
            padding: 0;
        }
        
        /* Place the running header in the top margin area */
        @page {
            @top-left-corner {
                content: none;
            }
            @top-left {
                content: element(header);
                width: 100%;
                vertical-align: middle;
                margin: 0;
                padding: 0;
            }
            @top-center {
                content: none;  /* Override any existing top-center content */
            }
            @top-right {
                content: none;
            }
            @top-right-corner {
                content: none;
            }
        }
        
        /* Header container - no margins needed as it's in the margin box */
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            padding: 0;
            margin: 0;
            height: auto;
        }
        
        .header-text {
            flex: 1;
            font-size: 10pt;
            line-height: 1.3;
            text-align: left;
            margin: 0;
            padding: 0;
            padding-right: 15pt;
        }
        
        .header-text p {
            margin: 0 0 2pt 0;
            padding: 0;
            text-indent: 0 !important;
            text-align: left !important;
        }
        
        .header-text h1, .header-text h2, .header-text h3 {
            font-size: 11pt;
            margin: 0 0 2pt 0;
            font-weight: 600;
        }
        
        .header-text strong {
            font-weight: 600;
        }
        
        .header-logo-wrapper {
            flex-shrink: 0;
        }
        
        .header-logo {
            max-height: 35pt;
            width: auto;
            object-fit: contain;
            display: block;
        }
        
        /* Reset body/content margins */
        body {
            margin: 0;
            padding: 0;
        }
        
        .content {
            margin: 0;
            padding: 0;
        }
        """
    
    def _create_html_document(self, html_content: str) -> str:
        """Create a complete HTML document with proper structure."""
        header_html = ""
        header_css = ""
        
        if self.include_header:
            logo_html, text_html = self._process_header_content()
            if logo_html or text_html:
                header_css = self._generate_header_css()
                # Wrap header in a container that respects margins
                header_html = '<div class="header-wrapper"><div class="header-container">'
                if text_html:
                    header_html += f'<div class="header-text">{text_html}</div>'
                if logo_html:
                    header_html += f'<div class="header-logo-wrapper">{logo_html}</div>'
                header_html += '</div></div>'
        
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.input_file.stem}</title>
            <style>
                {self.css_styles}
                {self.pygments_css}
                {header_css}
            </style>
        </head>
        <body>
            {header_html}
            <div class="content">
                {html_content}
            </div>
        </body>
        </html>
        """
    
    def convert(self) -> bool:
        """Convert Markdown file to PDF."""
        try:
            # Read the markdown file
            if not self.input_file.exists():
                print(f"Error: Input file '{self.input_file}' not found.")
                return False
            
            print(f"Reading markdown file: {self.input_file}")
            with open(self.input_file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            # Convert markdown to HTML
            print("Converting markdown to HTML...")
            html_content = self._process_markdown(markdown_content)
            
            # Create complete HTML document
            html_document = self._create_html_document(html_content)
            
            # Convert HTML to PDF directly
            print(f"Generating PDF: {self.output_file}")
            # Set base_url to project root so both font and asset paths resolve correctly
            base_url = str(Path('.').resolve()) + '/'
            html = HTML(string=html_document, base_url=base_url)
            html.write_pdf(str(self.output_file))
            
            print(f"✅ Successfully created PDF: {self.output_file}")
            return True
                
        except Exception as e:
            print(f"❌ Error converting to PDF: {str(e)}")
            return False

def ensure_folders_exist():
    """Ensure input, output, and processed folders exist."""
    folders = ['input', 'output', 'processed']
    for folder in folders:
        Path(folder).mkdir(exist_ok=True)

def get_unique_filename(file_path: Path, target_dir: Path) -> Path:
    """Generate a unique filename to avoid duplicates."""
    base_name = file_path.stem
    extension = file_path.suffix
    counter = 1
    new_path = target_dir / f"{base_name}{extension}"
    
    while new_path.exists():
        new_path = target_dir / f"{base_name}_{counter}{extension}"
        counter += 1
    
    return new_path

def process_input_folder(style: str, theme: str, include_header: bool = False) -> int:
    """Process all markdown files in the input folder."""
    input_folder = Path('input')
    output_folder = Path('output')
    processed_folder = Path('processed')
    
    # Get all markdown files in input folder
    markdown_files = list(input_folder.glob('*.md'))
    
    if not markdown_files:
        print("No markdown files found in input/ folder")
        return 0
    
    print(f"Found {len(markdown_files)} markdown file(s) in input/ folder")
    print(f"Style: {style}")
    print(f"Theme: {theme}")
    if include_header:
        print(f"Header: Enabled")
    print("=" * 60)
    
    success_count = 0
    
    for input_file in markdown_files:
        print(f"\nProcessing: {input_file.name}")
        
        # Generate output filename
        output_filename = f"{input_file.stem}_{style}_{theme}.pdf"
        output_path = output_folder / output_filename
        
        # Handle duplicate output files
        if output_path.exists():
            output_path = get_unique_filename(output_path, output_folder)
        
        # Convert the file
        converter = MD2PDFConverter(str(input_file), str(output_path), style, theme, include_header)
        if converter.convert():
            success_count += 1
            
            # Move original file to processed folder
            processed_path = get_unique_filename(input_file, processed_folder)
            shutil.move(str(input_file), str(processed_path))
            print(f"✅ Converted: {input_file.name} → {output_path.name}")
            print(f"📁 Moved: {input_file.name} → processed/{processed_path.name}")
        else:
            print(f"❌ Failed to convert: {input_file.name}")
    
    print(f"\n{'='*60}")
    print(f"Workflow complete: {success_count}/{len(markdown_files)} files processed successfully")
    print(f"{'='*60}")
    
    return success_count

def main():
    """Main function to handle command line arguments and run conversion."""
    parser = argparse.ArgumentParser(
        description="Convert Markdown files to beautifully formatted PDFs with multiple style templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python md2pdf.py document.md
  python md2pdf.py input.md -o output.pdf
  python md2pdf.py document.md --style whitepaper
  python md2pdf.py *.md --style story
  python md2pdf.py --list-styles
  python md2pdf.py --style modern --theme elegant  # Process all files in input/
        """
    )
    
    parser.add_argument(
        'input',
        nargs='?',
        help='Input markdown file(s) or glob pattern (optional: if not provided, processes all files in input/ folder)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output PDF file (optional, defaults to input filename with .pdf extension)'
    )
    
    parser.add_argument(
        '-s', '--style',
        default='technical',
        help='Style template to use (discovered from styles/ folder)'
    )
    
    parser.add_argument(
        '-t', '--theme',
        default='default',
        help='Color theme to use (discovered from themes/ folder)'
    )
    
    parser.add_argument(
        '--header',
        choices=['yes', 'no'],
        default='no',
        help='Include header with logo and text from header/ folder (default: no)'
    )
    
    parser.add_argument(
        '--list-styles',
        action='store_true',
        help='List all available style templates'
    )
    
    parser.add_argument(
        '--list-themes',
        action='store_true',
        help='List all available color themes'
    )
    
    parser.add_argument(
        '--list-combinations',
        action='store_true',
        help='List all available style + theme combinations'
    )
    
    args = parser.parse_args()
    
    # Handle list options
    if args.list_styles:
        print("🎨 Available Style Templates:")
        print("=" * 60)
        for name, style_name, description in style_loader.list_styles():
            print(f"📝 {name:12} - {style_name}")
            print(f"    {description}")
            print()
        return
    
    if args.list_themes:
        print("🎨 Available Color Themes:")
        print("=" * 60)
        for name, theme_name, description in style_loader.list_themes():
            print(f"🎨 {name:12} - {theme_name}")
            print(f"    {description}")
            print()
        return
    
    if args.list_combinations:
        print("🎨 Available Style + Theme Combinations:")
        print("=" * 60)
        for style_name, theme_name in style_loader.get_available_combinations():
            print(f"📝 {style_name:12} + {theme_name:12}")
        print()
        return
    
    # Ensure folders exist for workflow
    ensure_folders_exist()
    
    # Parse header argument
    include_header = args.header == 'yes'
    
    # Check if input is provided
    if not args.input:
        # Default workflow: process all files in input folder
        print("🚀 Starting default workflow...")
        print("Processing all markdown files in input/ folder")
        success_count = process_input_folder(args.style, args.theme, include_header)
        if success_count == 0:
            sys.exit(1)
        return
    
    # Handle glob patterns
    input_files = list(Path('.').glob(args.input)) if '*' in args.input else [Path(args.input)]
    
    if not input_files:
        print(f"Error: No files found matching '{args.input}'")
        sys.exit(1)
    
    success_count = 0
    total_count = len(input_files)
    
    for input_file in input_files:
        if not input_file.exists():
            print(f"Warning: File '{input_file}' not found, skipping...")
            continue
        
        if input_file.suffix.lower() != '.md':
            print(f"Warning: File '{input_file}' is not a markdown file, skipping...")
            continue
        
        print(f"\n{'='*60}")
        print(f"Processing: {input_file}")
        print(f"Style: {args.style}")
        print(f"Theme: {args.theme}")
        if include_header:
            print(f"Header: Enabled")
        print(f"{'='*60}")
        
        converter = MD2PDFConverter(str(input_file), args.output, args.style, args.theme, include_header)
        if converter.convert():
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"Conversion complete: {success_count}/{total_count} files processed successfully")
    print(f"{'='*60}")
    
    if success_count == 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
