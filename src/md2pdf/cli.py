#!/usr/bin/env python3
"""
MD2PDF - Command Line Interface
Copyright (c) 2025 MPS Metalmind AB
Licensed under the MIT License (see LICENSE file)
"""

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.progress import BarColumn
from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn
from rich.table import Table

from md2pdf import __version__

console = Console()


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version=__version__, prog_name="md2pdf")
def cli(ctx):
    """
    MD2PDF - Beautiful Markdown to PDF Converter

    Convert Markdown files to professionally styled PDFs with various templates and themes.
    """
    if ctx.invoked_subcommand is None:
        # If no subcommand, run the default convert command
        ctx.invoke(convert)


@cli.command()
@click.argument("input_files", nargs=-1, type=click.Path(exists=True))
@click.option(
    "-o", "--output", type=click.Path(), help="Output file path (for single input file)"
)
@click.option(
    "-s",
    "--style",
    default="technical",
    type=click.Choice(
        [
            "technical",
            "academic",
            "story",
            "modern",
            "whitepaper",
            "consultancy",
            "futuristic",
        ],
        case_sensitive=False,
    ),
    help="Style template to use",
)
@click.option(
    "-t",
    "--theme",
    default="default",
    type=click.Choice(
        [
            "default",
            "dark",
            "forest",
            "oceanic",
            "solarized",
            "violet",
            "warm",
            "cool",
            "elegant",
            "sepia",
        ],
        case_sensitive=False,
    ),
    help="Color theme to use",
)
@click.option(
    "--batch/--no-batch", default=False, help="Process multiple files in batch mode"
)
@click.option(
    "--header", type=click.Path(exists=True), help="Optional header template file"
)
@click.option(
    "--format",
    type=click.Choice(["pdf", "word"], case_sensitive=False),
    default="pdf",
    help="Output format (PDF or Word)",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def convert(input_files, output, style, theme, batch, header, format, verbose):
    """Convert Markdown files to PDF or Word documents."""

    # Lazy imports to avoid loading heavy dependencies
    from md2pdf.core.converters.pdf_converter import PDFConverter
    from md2pdf.core.converters.word_converter import WordConverter
    from md2pdf.core.processors.workflow_processor import WorkflowProcessor

    # If no input files specified, process all markdown files in current directory
    if not input_files:
        input_path = Path(".")
        markdown_files = list(input_path.glob("*.md"))
        if not markdown_files:
            console.print(
                "[red]Error:[/red] No markdown files found in current directory"
            )
            sys.exit(1)
        input_files = [str(f) for f in markdown_files]

    # Convert to Path objects
    input_paths = [Path(f) for f in input_files]

    # Check for single file with output option
    if output and len(input_paths) > 1:
        console.print(
            "[yellow]Warning:[/yellow] Output option ignored for multiple input files"
        )
        output = None

    # Initialize workflow processor
    WorkflowProcessor()

    # Select converter based on format
    if format == "pdf":
        ConverterClass = PDFConverter
        default_ext = ".pdf"
    else:
        ConverterClass = WordConverter
        default_ext = ".docx"

    # Process files
    successful = 0
    failed = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(
            f"[cyan]Converting to {format.upper()}...", total=len(input_paths)
        )

        for input_path in input_paths:
            try:
                # Determine output path
                if output and len(input_paths) == 1:
                    output_path = Path(output)
                else:
                    output_path = input_path.with_suffix(default_ext)

                progress.update(
                    task, description=f"[cyan]Converting {input_path.name}..."
                )

                # Initialize converter
                converter = ConverterClass(
                    input_file=str(input_path),
                    output_file=str(output_path),
                    style=style,
                    theme=theme,
                    include_header=bool(header),
                )

                # Convert file
                success = converter.convert()

                if success:
                    successful += 1
                    if verbose:
                        console.print(
                            f"✅ [green]Success:[/green] {input_path.name} → {output_path.name}"
                        )
                else:
                    failed += 1
                    console.print(f"❌ [red]Failed:[/red] {input_path.name}")

            except Exception as e:
                failed += 1
                console.print(
                    f"❌ [red]Error processing {input_path.name}:[/red] {str(e)}"
                )

            progress.advance(task)

    # Print summary
    console.print()
    if successful > 0:
        console.print(f"[green]✅ Successfully converted {successful} file(s)[/green]")
    if failed > 0:
        console.print(f"[red]❌ Failed to convert {failed} file(s)[/red]")

    sys.exit(0 if failed == 0 else 1)


@cli.command("list-styles")
def list_styles():
    """List all available style templates."""
    from md2pdf.core.utils.style_loader import style_loader

    styles = style_loader.list_available_styles()
    themes = style_loader.list_available_themes()

    # Create styles table
    style_table = Table(
        title="Available Styles", show_header=True, header_style="bold magenta"
    )
    style_table.add_column("Style", style="cyan", no_wrap=True)
    style_table.add_column("Description", style="white")

    style_descriptions = {
        "technical": "Clean technical documentation style",
        "academic": "Traditional academic paper style",
        "story": "Elegant storytelling style with serif fonts",
        "modern": "Contemporary design with clean lines",
        "whitepaper": "Professional whitepaper style",
        "consultancy": "Business consulting presentation style",
        "futuristic": "Bold futuristic design",
    }

    for style in styles:
        style_table.add_row(style, style_descriptions.get(style, "Custom style"))

    # Create themes table
    theme_table = Table(
        title="Available Themes", show_header=True, header_style="bold magenta"
    )
    theme_table.add_column("Theme", style="cyan", no_wrap=True)
    theme_table.add_column("Description", style="white")

    theme_descriptions = {
        "default": "Standard light theme",
        "dark": "Dark mode theme",
        "forest": "Natural green tones",
        "oceanic": "Cool blue ocean colors",
        "solarized": "Solarized color scheme",
        "violet": "Purple and violet tones",
        "warm": "Warm orange and red tones",
        "cool": "Cool blue and gray tones",
        "elegant": "Sophisticated grayscale",
        "sepia": "Vintage sepia tones",
    }

    for theme in themes:
        theme_table.add_row(theme, theme_descriptions.get(theme, "Custom theme"))

    console.print(style_table)
    console.print()
    console.print(theme_table)


@cli.command()
@click.argument(
    "input_directory", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.option(
    "-o",
    "--output-directory",
    type=click.Path(file_okay=False, dir_okay=True),
    help="Output directory for converted files",
)
@click.option("-s", "--style", default="technical", help="Style template to use")
@click.option("-t", "--theme", default="default", help="Color theme to use")
@click.option(
    "--format",
    type=click.Choice(["pdf", "word"], case_sensitive=False),
    default="pdf",
    help="Output format",
)
@click.option(
    "--recursive", "-r", is_flag=True, help="Process subdirectories recursively"
)
def batch(input_directory, output_directory, style, theme, format, recursive):
    """Batch convert all Markdown files in a directory."""
    input_path = Path(input_directory)

    # Find markdown files
    if recursive:
        markdown_files = list(input_path.rglob("*.md"))
    else:
        markdown_files = list(input_path.glob("*.md"))

    if not markdown_files:
        console.print(f"[red]Error:[/red] No markdown files found in {input_directory}")
        sys.exit(1)

    console.print(f"[cyan]Found {len(markdown_files)} markdown files[/cyan]")

    # Set output directory
    if output_directory:
        output_path = Path(output_directory)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = input_path

    # Convert files
    ctx = click.get_current_context()
    ctx.invoke(
        convert,
        input_files=[str(f) for f in markdown_files],
        output=None,
        style=style,
        theme=theme,
        batch=True,
        header=None,
        format=format,
        verbose=True,
    )


@cli.command()
def setup():
    """Download optional assets (emojis, extra fonts)."""
    console.print("[cyan]Setting up MD2PDF assets...[/cyan]")

    # Import and run setup script
    try:
        from md2pdf.scripts.setup_assets import main as setup_main

        setup_main()
    except ImportError:
        # Try alternative location
        try:
            import sys

            sys.path.insert(0, str(Path(__file__).parent.parent.parent))
            from scripts.setup_assets import main as setup_main

            setup_main()
        except ImportError:
            console.print(
                "[red]Error:[/red] Setup script not found. Please run scripts/setup_assets.py manually."
            )
            sys.exit(1)


def main():
    """Main entry point for the CLI."""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Conversion cancelled by user[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"[red]Fatal error:[/red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
