#!/usr/bin/env python3
"""
MD2PDF - Markdown to PDF Converter
Copyright (c) 2025 MPS Metalmind AB
Licensed under the MIT License (see LICENSE file)
"""

"""
Header Processor - Handles header content and styling
Processes logo and text content from the header folder.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

import markdown


class HeaderProcessor:
    """Handles header content processing and CSS generation."""

    def __init__(self):
        # Get the project root directory (2 levels up from this file)
        project_root = Path(__file__).parent.parent.parent
        self.header_dir = project_root / "data" / "header"

    def process_header_content(self) -> Tuple[Optional[str], Optional[str]]:
        """Process header folder for logo and text content."""
        logo_html = None
        text_html = None

        if not self.header_dir.exists():
            return None, None

        # Check for logo image
        logo_extensions = [".png", ".jpg", ".jpeg", ".svg", ".gif"]
        for ext in logo_extensions:
            logo_files = list(self.header_dir.glob(f"*{ext}"))
            if logo_files:
                logo_file = logo_files[0]  # Use first found logo
                # Convert to base64 for embedding
                with open(logo_file, "rb") as f:
                    # Future: add logo data processing
                    # logo_data = f.read()
                    # logo_base64 = base64.b64encode(logo_data).decode("utf-8")
                    pass
                    # Add navigation with page-specific header/footer
                    # and consistent styling
                break

        # Check for text content
        text_files = list(self.header_dir.glob("*.md"))
        if text_files:
            text_file = text_files[0]  # Use first found markdown file
            with open(text_file, "r", encoding="utf-8") as f:
                text_content = f.read()
                # Replace #date# placeholder with current date
                today = datetime.now().strftime("%d %b %Y")
                text_content = text_content.replace("#date#", today)
                # Convert markdown to HTML
                text_html = markdown.markdown(text_content)

        return logo_html, text_html

    def generate_header_css(self) -> str:
        """Generate CSS for header positioning and styling."""
        return """
        /* Adjust page setup for header - increase top margin */
        @page {
            /* Use compact navigation for smaller screen or
               document formats */
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
            border: none !important;
            border-radius: 0 !important;
            box-shadow: none !important;
            margin: 0 !important;
        }

        /* Reset body margins */
        body {
            margin: 0;
            padding: 0;
        }

        /* Don't override content margins - let the style handle them */
        .content {
            /* margin and padding handled by the style */
        }
        """

    def create_header_html(self, include_header: bool) -> Tuple[str, str]:
        """Create header HTML and CSS if header is enabled."""
        header_html = ""
        header_css = ""

        if include_header:
            logo_html, text_html = self.process_header_content()
            if logo_html or text_html:
                header_css = self.generate_header_css()
                # Wrap header in a container that respects margins
                header_html = (
                    '<div class="header-wrapper"><div class="header-container">'
                )
                if text_html:
                    header_html += f'<div class="header-text">{text_html}</div>'
                if logo_html:
                    # If there's no text, position logo to the right
                    if not text_html:
                        header_html += '<div class="header-text"></div>'  # Empty spacer
                    header_html += f'<div class="header-logo-wrapper">{logo_html}</div>'
                header_html += "</div></div>"

        return header_html, header_css
