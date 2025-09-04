#!/usr/bin/env python3
"""
Base Converter - Common functionality for document converters
Provides shared functionality for PDF and Word converters.
"""

from pathlib import Path
from typing import Optional
from pygments.formatters import HtmlFormatter
from utils.style_loader import style_loader
from processors.markdown_processor import MarkdownProcessor
from processors.header_processor import HeaderProcessor

class BaseConverter:
    """Base class for document converters with shared functionality."""
    
    def __init__(self, input_file: str, output_file: Optional[str] = None, 
                 style: str = 'technical', theme: str = 'default', 
                 include_header: bool = False):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file) if output_file else self._generate_output_path()
        self.style_name = style
        self.theme_name = theme
        self.include_header = include_header
        self.css_styles = style_loader.combine_style_and_theme(style, theme)
        
        # Initialize processors
        self.markdown_processor = MarkdownProcessor()
        self.header_processor = HeaderProcessor()
        
        # Include Pygments CSS so class-based highlighting renders consistently across themes
        try:
            self.pygments_css = HtmlFormatter(style='default').get_style_defs('.codehilite')
        except Exception:
            self.pygments_css = ''
    
    def _generate_output_path(self) -> Path:
        """Generate output path based on input file."""
        return self.input_file.with_suffix('.pdf')  # Default to PDF, override in subclasses
    
    def _read_markdown_content(self) -> str:
        """Read the markdown file content."""
        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file '{self.input_file}' not found.")
        
        print(f"Reading markdown file: {self.input_file}")
        with open(self.input_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _process_markdown(self, content: str) -> str:
        """Process markdown content to HTML."""
        print("Converting markdown to HTML...")
        return self.markdown_processor.process_markdown(content)
    
    def _create_html_document(self, html_content: str) -> str:
        """Create a complete HTML document with proper structure."""
        header_html, header_css = self.header_processor.create_header_html(self.include_header)
        
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
            <div class="content{' has-header' if self.include_header else ''}">
                {html_content}
            </div>
        </body>
        </html>
        """
    
    def convert(self) -> bool:
        """Convert Markdown file to output format. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement convert() method")
