#!/usr/bin/env python3
"""
MD2PDF - Markdown to PDF Converter
Copyright (c) 2025 MPS Metalmind AB
Licensed under the MIT License (see LICENSE file)
"""

"""
Workflow Processor - Handles batch processing workflow
Manages input/output/processed folders and batch file processing.
"""

import shutil
from pathlib import Path
from typing import Callable, List


class WorkflowProcessor:
    """Handles batch processing workflow."""

    def __init__(self) -> None:
        # Get the project root directory (2 levels up from this file)
        project_root = Path(__file__).parent.parent.parent
        self.input_folder = project_root / "data" / "input"
        self.output_folder = project_root / "data" / "output"
        self.processed_folder = project_root / "data" / "processed"

    def ensure_folders_exist(self) -> None:
        """Ensure input, output, and processed folders exist."""
        folders = [self.input_folder, self.output_folder, self.processed_folder]
        for folder in folders:
            folder.mkdir(exist_ok=True)

    def get_unique_filename(self, file_path: Path, target_dir: Path) -> Path:
        """Generate a unique filename to avoid duplicates."""
        base_name = file_path.stem
        extension = file_path.suffix
        counter = 1
        new_path = target_dir / f"{base_name}{extension}"

        while new_path.exists():
            new_path = target_dir / f"{base_name}_{counter}{extension}"
            counter += 1

        return new_path

    def get_markdown_files(self) -> List[Path]:
        """Get all markdown files in input folder."""
        return list(self.input_folder.glob("*.md"))

    def process_files(
        self, style: str, theme: str, include_header: bool, converter_factory: Callable
    ) -> int:
        """Process all markdown files in the input folder."""
        markdown_files = self.get_markdown_files()

        if not markdown_files:
            print("No markdown files found in data/input/ folder")
            return 0

        print(f"Found {len(markdown_files)} markdown file(s) in data/input/ folder")
        print(f"Style: {style}")
        print(f"Theme: {theme}")
        if include_header:
            print(f"Header: Enabled")
        print("=" * 60)

        success_count = 0

        for input_file in markdown_files:
            print(f"\nProcessing: {input_file.name}")

            # Generate output filename with style and theme
            output_filename = f"{input_file.stem}_{style}_{theme}"
            output_path = self.output_folder / output_filename

            # Handle duplicate output files
            if output_path.exists():
                output_path = self.get_unique_filename(output_path, self.output_folder)

            # Convert the file using the provided converter factory
            converter = converter_factory(
                str(input_file), str(output_path), style, theme, include_header
            )
            if converter.convert():
                success_count += 1

                # Move original file to processed folder
                processed_path = self.get_unique_filename(
                    input_file, self.processed_folder
                )
                shutil.move(str(input_file), str(processed_path))
                print(f"✅ Converted: {input_file.name} → {output_path.name}")
                print(f"📁 Moved: {input_file.name} → processed/{processed_path.name}")
            else:
                print(f"❌ Failed to convert: {input_file.name}")

        print(f"\n{'='*60}")
        print(f"✅ Successfully converted {success_count} " f"file(s)")
        print(f"{'='*60}")

        return success_count
