# Batch Processing Examples

This directory demonstrates MD2PDF's powerful batch processing capabilities for handling multiple files efficiently.

## Files in This Directory

- `batch_demo.py` - Complete batch processing demonstration
- `directory_processor.py` - Process entire directories of markdown files
- `pattern_matching.py` - Use glob patterns to select specific files
- `parallel_processing.py` - Process multiple files in parallel
- `workflow_automation.py` - Automated workflow examples
- `progress_tracking.py` - Monitor batch processing progress
- `sample_docs/` - Sample markdown files for batch processing

## Batch Processing Features

MD2PDF provides several ways to process multiple files:

### Command Line Batch Processing

```bash
# Process all .md files in current directory
md2pdf *.md --style technical --theme dark

# Process files in specific directory
md2pdf docs/*.md --output-dir pdfs/ --style modern

# Recursive processing (shell expansion)
md2pdf **/*.md --style whitepaper --theme sophisticated
```

### Python API Batch Processing

```python
from md2pdf import MD2PDFConverter

# Simple batch processing
converter = MD2PDFConverter(style='technical', theme='oceanic')
converter.convert_batch('docs/*.md', output_dir='pdfs/')

# Advanced batch processing with options
results = converter.convert_batch(
    pattern='**/*.md',
    output_dir='output/',
    recursive=True,
    parallel=True,
    max_workers=4
)
```

## Use Cases

### 1. Documentation Websites
Convert entire documentation sites to PDF format:

```bash
md2pdf docs/**/*.md --style technical --output-dir dist/pdfs/
```

### 2. Report Generation  
Generate multiple reports with consistent styling:

```bash
md2pdf reports/*.md --style consultancy --theme sophisticated
```

### 3. Academic Papers
Process research papers and theses:

```bash
md2pdf papers/*.md --style academic --theme default
```

### 4. Creative Writing
Convert stories and creative content:

```bash
md2pdf stories/*.md --style story --theme sepia
```

## Running Batch Examples

### Complete Demonstration
```bash
python batch_demo.py
```
This runs a comprehensive batch processing demonstration with multiple files and configurations.

### Directory Processing
```bash
python directory_processor.py
```
Shows how to process entire directory trees of markdown files.

### Pattern Matching
```bash
python pattern_matching.py  
```
Demonstrates advanced file selection using glob patterns.

### Parallel Processing
```bash
python parallel_processing.py
```
Shows how to process multiple files simultaneously for better performance.

### Workflow Automation
```bash
python workflow_automation.py
```
Example of automated batch processing workflows.

## Performance Considerations

### File Selection Strategies

**Small Projects (< 50 files)**
- Process all files together
- Use simple glob patterns
- Single-threaded processing is sufficient

**Medium Projects (50-500 files)**  
- Group by file type or directory
- Use parallel processing
- Monitor memory usage

**Large Projects (500+ files)**
- Process in batches
- Use multiple workers
- Implement progress tracking
- Consider streaming processing

### Memory Management

```python
# For large batch jobs, process in chunks
from md2pdf import MD2PDFConverter
import glob

files = glob.glob('large_docs/**/*.md', recursive=True)
converter = MD2PDFConverter()

# Process in chunks of 10
chunk_size = 10
for i in range(0, len(files), chunk_size):
    chunk = files[i:i + chunk_size]
    for file in chunk:
        converter.convert(file)
    print(f"Processed {min(i + chunk_size, len(files))}/{len(files)} files")
```

## Error Handling

### Robust Batch Processing

```python
from md2pdf import MD2PDFConverter, ConversionError
import glob
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def batch_convert_with_error_handling(pattern, **kwargs):
    \"\"\"Convert multiple files with comprehensive error handling.\"\"\"
    converter = MD2PDFConverter(**kwargs)
    files = glob.glob(pattern)
    
    successful = []
    failed = []
    
    for file_path in files:
        try:
            output_path = converter.convert(file_path)
            successful.append((file_path, output_path))
            logger.info(f"✅ Converted: {file_path}")
            
        except ConversionError as e:
            failed.append((file_path, str(e)))
            logger.error(f"❌ Conversion failed for {file_path}: {e}")
            
        except Exception as e:
            failed.append((file_path, f"Unexpected error: {e}"))
            logger.error(f"❌ Unexpected error for {file_path}: {e}")
    
    return {
        'successful': successful,
        'failed': failed,
        'total': len(files),
        'success_rate': len(successful) / len(files) if files else 0
    }
```

## Configuration Files

### Project-Level Configuration

Create `.md2pdf.yml` in your project root:

```yaml
# MD2PDF Batch Configuration
default_style: technical
default_theme: oceanic
output_dir: dist/pdfs/
parallel: true
max_workers: 4

# File-specific overrides
overrides:
  "README.md":
    style: modern
    theme: elegant
    output: "README_special.pdf"
  
  "docs/api/*.md":
    style: technical
    theme: dark
  
  "guides/*.md":
    style: whitepaper
    theme: sophisticated
```

### Batch Processing Script

```python
# batch_config.py
import yaml
from pathlib import Path
from md2pdf import MD2PDFConverter

def load_batch_config(config_path='.md2pdf.yml'):
    \"\"\"Load batch processing configuration.\"\"\"
    config_file = Path(config_path)
    if not config_file.exists():
        return {}
    
    with open(config_file) as f:
        return yaml.safe_load(f)

def run_batch_with_config():
    \"\"\"Run batch processing using configuration file.\"\"\"
    config = load_batch_config()
    
    # Default settings
    converter = MD2PDFConverter(
        style=config.get('default_style', 'technical'),
        theme=config.get('default_theme', 'default')
    )
    
    # Process with overrides
    overrides = config.get('overrides', {})
    for pattern, settings in overrides.items():
        print(f"Processing {pattern} with custom settings...")
        custom_converter = MD2PDFConverter(**settings)
        custom_converter.convert_batch(pattern)
```

## Integration Examples

### Makefile Integration

```makefile
# Makefile for document generation
.PHONY: docs pdfs clean

# Generate all PDFs
pdfs:
	md2pdf docs/*.md --style technical --theme oceanic --output-dir dist/pdfs/
	md2pdf guides/*.md --style whitepaper --theme sophisticated --output-dir dist/guides/
	md2pdf README.md --style modern --theme elegant --output dist/README.pdf

# Clean generated files
clean:
	rm -rf dist/pdfs/*.pdf dist/guides/*.pdf dist/README.pdf

# Watch for changes and regenerate
watch:
	while inotifywait -e modify docs/ guides/ README.md; do make pdfs; done
```

### CI/CD Pipeline

```yaml
# .github/workflows/docs.yml
name: Generate Documentation PDFs

on:
  push:
    paths:
      - 'docs/**/*.md'
      - 'guides/**/*.md'
      - 'README.md'

jobs:
  generate-pdfs:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
          
      - name: Install system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev
          
      - name: Install MD2PDF
        run: pip install md2pdf
        
      - name: Generate PDFs
        run: |
          md2pdf docs/**/*.md --style technical --output-dir dist/docs/
          md2pdf guides/*.md --style whitepaper --output-dir dist/guides/
          md2pdf README.md --style modern --output dist/README.pdf
          
      - name: Upload PDFs
        uses: actions/upload-artifact@v2
        with:
          name: documentation-pdfs
          path: dist/
```

## Best Practices

### Organization

1. **Group similar files**: Process files of the same type together
2. **Use consistent naming**: Follow predictable output naming patterns
3. **Separate by purpose**: Different styles for different document types
4. **Version control**: Track batch processing scripts and configurations

### Performance

1. **Use parallel processing** for large batches
2. **Monitor memory usage** with large files
3. **Process incrementally** for very large projects
4. **Cache results** to avoid reprocessing unchanged files

### Error Management

1. **Log all operations** for debugging
2. **Handle errors gracefully** without stopping entire batch
3. **Provide progress feedback** for long-running operations
4. **Validate inputs** before processing

### Quality Control

1. **Test with sample files** before full batch
2. **Verify output quality** with spot checks
3. **Validate file sizes** and content
4. **Check error logs** regularly

## Troubleshooting

### Common Issues

**Memory errors with large batches**
- Process files in smaller chunks
- Increase available memory
- Use parallel processing to distribute load

**Slow processing**
- Enable parallel processing
- Use simpler styles for large batches
- Process files incrementally

**Inconsistent output**
- Verify configuration files
- Check file permissions
- Validate input file formats

**File not found errors**
- Use absolute paths
- Verify glob patterns
- Check directory permissions

### Debugging

Enable verbose logging for batch processing:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

converter = MD2PDFConverter(verbose=True)
converter.convert_batch('docs/*.md')
```

## Getting Help

For batch processing questions:

1. Check the [Usage Documentation](../../docs/usage.rst)
2. Review example scripts in this directory
3. Open an issue for batch processing bugs
4. Join discussions for workflow questions