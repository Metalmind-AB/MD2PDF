# Basic Usage Examples

This directory demonstrates the fundamental features of MD2PDF with simple, easy-to-understand examples.

## Files in This Directory

- `simple_conversion.py` - Basic file conversion
- `cli_examples.py` - Command-line interface examples
- `output_customization.py` - Custom output file naming
- `error_handling.py` - Basic error handling patterns
- `run_examples.py` - Script to run all basic examples

## Example 1: Simple Conversion

The most basic usage of MD2PDF:

```python
from md2pdf import MD2PDFConverter

# Create converter instance
converter = MD2PDFConverter()

# Convert markdown to PDF
converter.convert('input.md', 'output.pdf')
```

## Example 2: Command Line Usage

Using MD2PDF from the command line:

```bash
# Basic conversion
md2pdf document.md

# Specify output file
md2pdf document.md --output custom_name.pdf

# Use different style and theme
md2pdf document.md --style modern --theme elegant
```

## Example 3: With Configuration

Using MD2PDF with custom configuration:

```python
from md2pdf import MD2PDFConverter

# Configure converter
converter = MD2PDFConverter(
    style='technical',
    theme='oceanic',
    verbose=True
)

# Convert with configuration
converter.convert('../sample_documents/getting_started.md')
```

## Running the Examples

Execute the example runner:

```bash
python run_examples.py
```

Or run individual examples:

```bash
python simple_conversion.py
python cli_examples.py
python output_customization.py
```

## Expected Output

After running these examples, you should see:

- PDF files generated in the current directory
- Console output showing conversion progress
- Different styling applied based on the chosen style/theme combinations

## Common Use Cases

These basic examples cover:

1. **Single file conversion**: Converting one markdown file to PDF
2. **Output customization**: Specifying custom output file names and locations
3. **Style application**: Using different built-in styles and themes
4. **Error handling**: Dealing with common conversion errors
5. **CLI usage**: Using MD2PDF from the command line

## Next Steps

After mastering these basic examples, explore:

- [API Examples](../api_examples/) for more advanced Python usage
- [Styling Examples](../styling/) for custom styling and themes
- [Batch Processing](../batch_processing/) for handling multiple files
- [Advanced Examples](../advanced/) for complex configurations
