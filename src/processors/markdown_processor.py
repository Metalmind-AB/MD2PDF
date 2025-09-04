#!/usr/bin/env python3
"""
Markdown Processor - Core markdown processing functionality
Handles markdown conversion, syntax highlighting, and emoji replacement.
"""

import markdown
import re
import base64
from pathlib import Path
from typing import Optional
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter

class MarkdownProcessor:
    """Core markdown processing functionality."""
    
    def __init__(self):
        self.extensions = [
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list',
            'markdown.extensions.footnotes',
            'markdown.extensions.smarty',
            'markdown.extensions.nl2br'
        ]
        
        self.extension_configs = {
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
    
    def process_markdown(self, content: str) -> str:
        """Convert Markdown content to HTML with extensions."""
        md = markdown.Markdown(extensions=self.extensions, extension_configs=self.extension_configs)
        html = md.convert(content)
        
        # Apply custom syntax highlighting
        html = self._highlight_code_blocks(html)
        
        # Replace emojis with Twemoji images
        html = self._replace_emojis_with_images(html)
        
        return html
    
    def _highlight_code_blocks(self, html_content: str) -> str:
        """Apply syntax highlighting to code blocks in HTML content."""
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
        """Replace emoji grapheme clusters with Twemoji SVG images for robust rendering."""
        from html import escape
        import emoji

        def to_twemoji_codepoints(grapheme: str) -> str:
            """Return hyphen-joined lowercase hex codepoints for a grapheme cluster."""
            return '-'.join(f"{ord(ch):x}" for ch in grapheme)

        def normalize_candidates(codepoints: str) -> list:
            """Generate plausible Twemoji filename variants for a codepoint string."""
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
