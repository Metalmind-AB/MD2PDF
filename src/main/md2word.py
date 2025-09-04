#!/usr/bin/env python3
"""
MD2Word - Beautiful Markdown to Word Converter
A comprehensive tool that converts Markdown files to professionally formatted Word documents
with custom styling and responsive layout.
"""

import argparse
import sys
from pathlib import Path
from processors.workflow_processor import WorkflowProcessor
from converters.word_converter import WordConverter
from utils.style_loader import style_loader

def main():
    """Main function to handle command line arguments and run conversion."""
    parser = argparse.ArgumentParser(
        description="Convert Markdown files to beautifully formatted Word documents with multiple style templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python md2word.py document.md
  python md2word.py input.md -o output.docx
  python md2word.py document.md --style whitepaper
  python md2word.py *.md --style story
  python md2word.py --list-styles
  python md2word.py --style modern --theme elegant  # Process all files in input/
        """
    )
    
    parser.add_argument(
        'input',
        nargs='?',
        help='Input markdown file(s) or glob pattern (optional: if not provided, processes all files in input/ folder)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output Word file (optional, defaults to input filename with .docx extension)'
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
    
    # Initialize workflow processor
    workflow = WorkflowProcessor()
    workflow.ensure_folders_exist()
    
    # Parse header argument
    include_header = args.header == 'yes'
    
    # Check if input is provided
    if not args.input:
        # Default workflow: process all files in input folder
        print("🚀 Starting default workflow...")
        print("Processing all markdown files in input/ folder")
        
        def word_converter_factory(input_file, output_file, style, theme, include_header):
            return WordConverter(input_file, output_file, style, theme, include_header)
        
        success_count = workflow.process_files(args.style, args.theme, include_header, word_converter_factory)
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
        
        converter = WordConverter(str(input_file), args.output, args.style, args.theme, include_header)
        if converter.convert():
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"Conversion complete: {success_count}/{total_count} files processed successfully")
    print(f"{'='*60}")
    
    if success_count == 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
