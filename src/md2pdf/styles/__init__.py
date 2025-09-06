#!/usr/bin/env python3
"""MD2PDF - Styles Module.

Copyright (c) 2025 MPS Metalmind AB
Licensed under the MIT License (see LICENSE file).
"""

from pathlib import Path


def get_styles_directory() -> Path:
    """Get the path to the styles templates directory."""
    return Path(__file__).parent / "templates"


def list_available_styles() -> list:
    """List all available style templates."""
    styles_dir = get_styles_directory()
    if not styles_dir.exists():
        return []

    return sorted(
        [f.stem for f in styles_dir.glob("*.css") if not f.stem.startswith("_")]
    )


__all__ = ["get_styles_directory", "list_available_styles"]
