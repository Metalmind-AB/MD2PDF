# Copyright (c) 2025 MPS Metalmind AB
# Licensed under the MIT License (see LICENSE file)

"""
Tests for MD2PDF command-line interface.
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner

from md2pdf.cli import cli


class TestCLIBasic:
    """Test basic CLI functionality."""

    @pytest.fixture
    def runner(self):
        """Create a Click test runner."""
        return CliRunner()

    @pytest.mark.unit
    @pytest.mark.cli
    def test_cli_version(self, runner):
        """Test CLI version display."""
        result = runner.invoke(cli, ["--version"])

        assert result.exit_code == 0
        assert "md2pdf" in result.output.lower()
        assert "1.0.0" in result.output or "version" in result.output.lower()

    @pytest.mark.unit
    @pytest.mark.cli
    def test_cli_help(self, runner):
        """Test CLI help display."""
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "Usage:" in result.output
        assert "Commands:" in result.output
        assert "convert" in result.output

    @pytest.mark.unit
    @pytest.mark.cli
    def test_cli_no_args(self, runner):
        """Test CLI with no arguments shows help."""
        result = runner.invoke(cli, [])

        # Should show help or usage when no command given
        assert "Usage:" in result.output or "Commands:" in result.output

    @pytest.mark.unit
    @pytest.mark.cli
    def test_convert_help(self, runner):
        """Test convert command help."""
        result = runner.invoke(cli, ["convert", "--help"])

        assert result.exit_code == 0
        assert "--style" in result.output
        assert "--theme" in result.output
        assert "--output" in result.output


class TestCLIConvert:
    """Test the convert command functionality."""

    @pytest.fixture
    def runner(self):
        """Create a Click test runner."""
        return CliRunner()

    @pytest.mark.unit
    @pytest.mark.cli
    @patch("md2pdf.cli.PDFConverter")
    def test_convert_single_file(self, mock_converter, runner, sample_markdown_file):
        """Test converting a single markdown file."""
        # Setup mock
        mock_instance = Mock()
        mock_converter.return_value = mock_instance
        mock_instance.convert.return_value = True
        mock_instance.output_file = Path("output.pdf")

        result = runner.invoke(cli, ["convert", str(sample_markdown_file)])

        assert result.exit_code == 0
        mock_converter.assert_called_once()
        mock_instance.convert.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.cli
    @patch("md2pdf.cli.PDFConverter")
    def test_convert_with_output(
        self, mock_converter, runner, sample_markdown_file, temp_dir
    ):
        """Test converting with specified output file."""
        output_file = temp_dir / "custom_output.pdf"

        # Setup mock
        mock_instance = Mock()
        mock_converter.return_value = mock_instance
        mock_instance.convert.return_value = True
        mock_instance.output_file = output_file

        result = runner.invoke(
            cli, ["convert", str(sample_markdown_file), "--output", str(output_file)]
        )

        assert result.exit_code == 0
        # Check that output path was passed to converter
        call_args = mock_converter.call_args
        assert str(output_file) in str(call_args)

    @pytest.mark.unit
    @pytest.mark.cli
    @patch("md2pdf.cli.PDFConverter")
    def test_convert_with_style(self, mock_converter, runner, sample_markdown_file):
        """Test converting with specified style."""
        # Setup mock
        mock_instance = Mock()
        mock_converter.return_value = mock_instance
        mock_instance.convert.return_value = True
        mock_instance.output_file = Path("output.pdf")

        result = runner.invoke(
            cli, ["convert", str(sample_markdown_file), "--style", "academic"]
        )

        assert result.exit_code == 0
        # Check that style was passed to converter
        call_args = mock_converter.call_args
        assert "academic" in str(call_args)

    @pytest.mark.unit
    @pytest.mark.cli
    @patch("md2pdf.cli.PDFConverter")
    def test_convert_with_theme(self, mock_converter, runner, sample_markdown_file):
        """Test converting with specified theme."""
        # Setup mock
        mock_instance = Mock()
        mock_converter.return_value = mock_instance
        mock_instance.convert.return_value = True
        mock_instance.output_file = Path("output.pdf")

        result = runner.invoke(
            cli, ["convert", str(sample_markdown_file), "--theme", "dark"]
        )

        assert result.exit_code == 0
        # Check that theme was passed to converter
        call_args = mock_converter.call_args
        assert "dark" in str(call_args)

    @pytest.mark.unit
    @pytest.mark.cli
    @patch("md2pdf.cli.WordConverter")
    def test_convert_to_word(self, mock_converter, runner, sample_markdown_file):
        """Test converting to Word format."""
        # Setup mock
        mock_instance = Mock()
        mock_converter.return_value = mock_instance
        mock_instance.convert.return_value = True
        mock_instance.output_file = Path("output.docx")

        result = runner.invoke(
            cli, ["convert", str(sample_markdown_file), "--format", "word"]
        )

        assert result.exit_code == 0
        mock_converter.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.cli
    @patch("md2pdf.cli.PDFConverter")
    def test_convert_multiple_files(
        self, mock_converter, runner, multiple_markdown_files
    ):
        """Test converting multiple files."""
        # Setup mock
        mock_instance = Mock()
        mock_converter.return_value = mock_instance
        mock_instance.convert.return_value = True
        mock_instance.output_file = Path("output.pdf")

        file_args = [str(f) for f in multiple_markdown_files]
        result = runner.invoke(cli, ["convert"] + file_args)

        assert result.exit_code == 0
        # Should be called once per file
        assert mock_converter.call_count == len(multiple_markdown_files)

    @pytest.mark.unit
    @pytest.mark.cli
    def test_convert_nonexistent_file(self, runner):
        """Test converting non-existent file."""
        result = runner.invoke(cli, ["convert", "/nonexistent/file.md"])

        assert result.exit_code != 0

    @pytest.mark.unit
    @pytest.mark.cli
    @patch("md2pdf.cli.PDFConverter")
    def test_convert_failure_handling(
        self, mock_converter, runner, sample_markdown_file
    ):
        """Test handling of conversion failure."""
        # Setup mock to fail
        mock_instance = Mock()
        mock_converter.return_value = mock_instance
        mock_instance.convert.return_value = False
        mock_instance.output_file = Path("output.pdf")

        result = runner.invoke(cli, ["convert", str(sample_markdown_file)])

        # Should handle failure gracefully
        assert "error" in result.output.lower() or "failed" in result.output.lower()

    @pytest.mark.unit
    @pytest.mark.cli
    @patch("md2pdf.cli.PDFConverter")
    def test_convert_verbose_mode(self, mock_converter, runner, sample_markdown_file):
        """Test verbose output mode."""
        # Setup mock
        mock_instance = Mock()
        mock_converter.return_value = mock_instance
        mock_instance.convert.return_value = True
        mock_instance.output_file = Path("output.pdf")

        result = runner.invoke(cli, ["convert", str(sample_markdown_file), "--verbose"])

        assert result.exit_code == 0
        # Verbose mode should show more output
        assert len(result.output) > 0


class TestCLIBatch:
    """Test the batch command functionality."""

    @pytest.fixture
    def runner(self):
        """Create a Click test runner."""
        return CliRunner()

    @pytest.mark.unit
    @pytest.mark.cli
    def test_batch_help(self, runner):
        """Test batch command help."""
        result = runner.invoke(cli, ["batch", "--help"])

        assert result.exit_code == 0
        assert "--recursive" in result.output
        assert "--output-directory" in result.output

    @pytest.mark.unit
    @pytest.mark.cli
    @patch("md2pdf.cli.PDFConverter")
    def test_batch_directory(
        self, mock_converter, runner, temp_dir, multiple_markdown_files
    ):
        """Test batch conversion of directory."""
        # Setup mock
        mock_instance = Mock()
        mock_converter.return_value = mock_instance
        mock_instance.convert.return_value = True
        mock_instance.output_file = Path("output.pdf")

        result = runner.invoke(cli, ["batch", str(temp_dir)])

        assert result.exit_code == 0
        # Should find and convert markdown files
        assert mock_converter.call_count >= len(multiple_markdown_files)

    @pytest.mark.unit
    @pytest.mark.cli
    @patch("md2pdf.cli.PDFConverter")
    def test_batch_recursive(self, mock_converter, runner, temp_dir):
        """Test recursive batch conversion."""
        # Create nested structure
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        (subdir / "nested.md").write_text("# Nested")
        (temp_dir / "top.md").write_text("# Top")

        # Setup mock
        mock_instance = Mock()
        mock_converter.return_value = mock_instance
        mock_instance.convert.return_value = True
        mock_instance.output_file = Path("output.pdf")

        result = runner.invoke(cli, ["batch", str(temp_dir), "--recursive"])

        assert result.exit_code == 0
        # Should find files in subdirectories
        assert mock_converter.call_count >= 2

    @pytest.mark.unit
    @pytest.mark.cli
    @patch("md2pdf.cli.PDFConverter")
    def test_batch_output_directory(
        self, mock_converter, runner, temp_dir, multiple_markdown_files
    ):
        """Test batch conversion with output directory."""
        output_dir = temp_dir / "output"
        output_dir.mkdir()

        # Setup mock
        mock_instance = Mock()
        mock_converter.return_value = mock_instance
        mock_instance.convert.return_value = True
        mock_instance.output_file = output_dir / "output.pdf"

        result = runner.invoke(
            cli, ["batch", str(temp_dir), "--output-directory", str(output_dir)]
        )

        assert result.exit_code == 0


class TestCLIOptions:
    """Test various CLI options and combinations."""

    @pytest.fixture
    def runner(self):
        """Create a Click test runner."""
        return CliRunner()

    @pytest.mark.unit
    @pytest.mark.cli
    @patch("md2pdf.cli.style_loader")
    def test_list_styles(self, mock_style_loader, runner):
        """Test listing available styles."""
        mock_style_loader.list_styles.return_value = [
            "technical",
            "academic",
            "creative",
        ]

        result = runner.invoke(cli, ["list-styles"])

        assert result.exit_code == 0
        assert "technical" in result.output
        assert "academic" in result.output
        assert "creative" in result.output

    @pytest.mark.unit
    @pytest.mark.cli
    @patch("md2pdf.cli.style_loader")
    def test_list_themes(self, mock_style_loader, runner):
        """Test listing available themes."""
        mock_style_loader.list_themes.return_value = ["default", "dark", "ocean"]

        result = runner.invoke(cli, ["list-themes"])

        assert result.exit_code == 0
        assert "default" in result.output
        assert "dark" in result.output
        assert "ocean" in result.output

    @pytest.mark.unit
    @pytest.mark.cli
    @patch("md2pdf.cli.PDFConverter")
    def test_combined_options(
        self, mock_converter, runner, sample_markdown_file, temp_dir
    ):
        """Test multiple options combined."""
        output_file = temp_dir / "custom.pdf"

        # Setup mock
        mock_instance = Mock()
        mock_converter.return_value = mock_instance
        mock_instance.convert.return_value = True
        mock_instance.output_file = output_file

        result = runner.invoke(
            cli,
            [
                "convert",
                str(sample_markdown_file),
                "--output",
                str(output_file),
                "--style",
                "academic",
                "--theme",
                "ocean",
                "--verbose",
            ],
        )

        assert result.exit_code == 0

    @pytest.mark.integration
    @pytest.mark.cli
    def test_cli_integration(self, runner, sample_markdown_file, temp_dir):
        """Test CLI integration with actual conversion."""
        output_file = temp_dir / "integration_test.pdf"

        with patch("md2pdf.cli.PDFConverter") as mock_converter:
            mock_instance = Mock()
            mock_converter.return_value = mock_instance
            mock_instance.convert.return_value = True
            mock_instance.output_file = output_file

            # Test full command with all options
            result = runner.invoke(
                cli,
                [
                    "convert",
                    str(sample_markdown_file),
                    "--output",
                    str(output_file),
                    "--style",
                    "technical",
                    "--theme",
                    "default",
                    "--format",
                    "pdf",
                    "--verbose",
                ],
            )

            assert result.exit_code == 0
            # Verify all options were processed
            assert mock_converter.called
            call_kwargs = mock_converter.call_args[1]
            assert call_kwargs.get("style") == "technical"
            assert call_kwargs.get("theme") == "default"
