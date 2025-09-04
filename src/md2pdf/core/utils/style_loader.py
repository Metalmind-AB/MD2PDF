"""
MD2PDF - Markdown to PDF Converter
Copyright (c) 2025 MPS Metalmind AB
Licensed under the MIT License (see LICENSE file)
"""

"""
Dynamic Style and Theme Loader
Automatically discovers styles and themes from their respective folders.
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class StyleLoader:
    """Dynamic loader for styles and themes."""

    def __init__(self, styles_dir: str = "styles", themes_dir: str = "themes"):
        # Get the md2pdf package directory (3 levels up from this file)
        package_root = Path(__file__).parent.parent.parent
        self.styles_dir = package_root / styles_dir / "templates"
        self.themes_dir = package_root / themes_dir
        self._styles_cache: Optional[Dict[str, Dict[str, Any]]] = None
        self._themes_cache: Optional[Dict[str, Dict[str, Any]]] = None

    def discover_styles(self) -> Dict[str, Dict[str, Any]]:
        """Discover all available styles from the styles directory."""
        if self._styles_cache is not None:
            return self._styles_cache

        styles: Dict[str, Dict[str, Any]] = {}

        if not self.styles_dir.exists():
            return styles

        for css_file in self.styles_dir.glob("*.css"):
            style_name = css_file.stem
            style_info = self._extract_style_info(css_file)
            styles[style_name] = {
                "name": style_info.get("name", style_name.title()),
                "description": style_info.get(
                    "description", f"{style_name.title()} style"
                ),
                "file": str(css_file),
                "fonts": style_info.get("fonts", {}),
            }

        self._styles_cache = styles
        return styles

    def discover_themes(self) -> Dict[str, Dict[str, Any]]:
        """Discover all available themes from the themes directory."""
        if self._themes_cache is not None:
            return self._themes_cache

        themes: Dict[str, Dict[str, Any]] = {}

        if not self.themes_dir.exists():
            return themes

        for css_file in self.themes_dir.glob("*.css"):
            theme_name = css_file.stem
            theme_info = self._extract_theme_info(css_file)
            themes[theme_name] = {
                "name": theme_info.get("name", theme_name.title()),
                "description": theme_info.get(
                    "description", f"{theme_name.title()} theme"
                ),
                "file": str(css_file),
                "colors": theme_info.get("colors", {}),
            }

        self._themes_cache = themes
        return themes

    def _extract_style_info(self, css_file: Path) -> Dict:
        """Extract style information from CSS file comments."""
        info = {}

        try:
            with open(css_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract name from first comment
            name_match = re.search(r"/\*\s*([^*]+?)\s*\*/", content)
            if name_match:
                info["name"] = name_match.group(1).strip()

            # Extract description from comments
            desc_match = re.search(r"/\*\s*([^*]+?)\s*\*/", content, re.MULTILINE)
            if desc_match:
                info["description"] = desc_match.group(1).strip()

            # Extract font information from CSS variables
            font_vars = re.findall(r"--font-(\w+):\s*([^;]+);", content)
            if font_vars:
                info["fonts"] = dict(font_vars)

        except Exception as e:
            print(f"Warning: Could not extract info from {css_file}: {e}")

        return info

    def _extract_theme_info(self, css_file: Path) -> Dict:
        """Extract theme information from CSS file comments."""
        info = {}

        try:
            with open(css_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract name from first comment
            name_match = re.search(r"/\*\s*([^*]+?)\s*\*/", content)
            if name_match:
                info["name"] = name_match.group(1).strip()

            # Extract description from comments
            desc_match = re.search(r"/\*\s*([^*]+?)\s*\*/", content, re.MULTILINE)
            if desc_match:
                info["description"] = desc_match.group(1).strip()

            # Extract color information from CSS variables
            color_vars = re.findall(r"--theme-(\w+):\s*([^;]+);", content)
            if color_vars:
                info["colors"] = dict(color_vars)

        except Exception as e:
            print(f"Warning: Could not extract info from {css_file}: {e}")

        return info

    def get_style_css(self, style_name: str) -> str:
        """Get the CSS content for a specific style."""
        styles = self.discover_styles()
        if style_name not in styles:
            raise ValueError(
                f"Style '{style_name}' not found. Available: {list(styles.keys())}"
            )

        try:
            with open(styles[style_name]["file"], "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise ValueError(f"Could not read style file: {e}")

    def get_theme_css(self, theme_name: str) -> str:
        """Get the CSS content for a specific theme."""
        themes = self.discover_themes()
        if theme_name not in themes:
            raise ValueError(
                f"Theme '{theme_name}' not found. Available: {list(themes.keys())}"
            )

        try:
            with open(themes[theme_name]["file"], "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise ValueError(f"Could not read theme file: {e}")

    def list_available_styles(self) -> List[str]:
        """List all available style templates."""
        styles = self.discover_styles()
        return sorted(list(styles.keys()))

    def list_available_themes(self) -> List[str]:
        """List all available color themes.""" 
        themes = self.discover_themes()
        return sorted(list(themes.keys()))

    def combine_style_and_theme(self, style_name: str, theme_name: str) -> str:
        """Combine a style with a theme to create the final CSS."""
        style_css = self.get_style_css(style_name)
        theme_css = self.get_theme_css(theme_name)

        # Combine theme variables with style CSS
        return f"{theme_css}\n\n{style_css}"

    def list_styles(self) -> List[Tuple[str, str, str]]:
        """List all available styles with their descriptions."""
        styles = self.discover_styles()
        return [
            (name, info["name"], info["description"]) for name, info in styles.items()
        ]

    def list_themes(self) -> List[Tuple[str, str, str]]:
        """List all available themes with their descriptions."""
        themes = self.discover_themes()
        return [
            (name, info["name"], info["description"]) for name, info in themes.items()
        ]

    def get_available_combinations(self) -> List[Tuple[str, str]]:
        """Get all possible style + theme combinations."""
        styles = self.discover_styles()
        themes = self.discover_themes()

        combinations = []
        for style_name in styles:
            for theme_name in themes:
                combinations.append((style_name, theme_name))

        return combinations

    def validate_combination(self, style_name: str, theme_name: str) -> bool:
        """Validate that a style + theme combination exists."""
        styles = self.discover_styles()
        themes = self.discover_themes()

        return style_name in styles and theme_name in themes


# Global style loader instance
style_loader = StyleLoader()
