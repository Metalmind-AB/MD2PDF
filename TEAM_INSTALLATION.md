# MD2PDF - Team Installation Guide

## 🔒 Private Package Access

MD2PDF is distributed privately via GitHub releases for MPS Metalmind AB team members only.

## 📦 Quick Installation

### Method 1: Latest Release (Recommended)
```bash
pip install https://github.com/mps-metalmind/md2pdf/releases/latest/download/md2pdf-1.0.0-py3-none-any.whl
```

### Method 2: Specific Version
```bash
pip install https://github.com/mps-metalmind/md2pdf/releases/download/v1.0.0/md2pdf-1.0.0-py3-none-any.whl
```

### Method 3: Direct from Repository
```bash
pip install git+https://github.com/mps-metalmind/md2pdf.git
```

## ⚡ Verify Installation

```bash
md2pdf --version
md2pdf --help
```

## 🚀 Quick Test

```bash
# Create a test file
echo "# Test Document

This is a **test** of MD2PDF.

- Feature 1
- Feature 2

\`\`\`python
print('Hello, World!')
\`\`\`" > test.md

# Convert to PDF
md2pdf convert -o test.pdf test.md
```

## 🛠️ System Requirements

**macOS:**
```bash
brew install cairo pango gdk-pixbuf libffi
```

**Ubuntu/Debian:**
```bash
sudo apt-get install libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev libffi-dev
```

**Windows:**
```bash
# WeasyPrint will handle dependencies automatically
```

## 🔄 Updating

To update to a new release, simply reinstall:
```bash
pip uninstall md2pdf
pip install https://github.com/mps-metalmind/md2pdf/releases/latest/download/md2pdf-1.0.0-py3-none-any.whl
```

## ❓ Support

For technical support or issues:
1. Check the [GitHub Issues](https://github.com/mps-metalmind/md2pdf/issues)
2. Contact the development team
3. See the full [README](README.md) for detailed usage

## 🔐 Access Requirements

Team members need:
- Access to the private GitHub repository
- Python 3.8+ installed
- System dependencies for PDF generation (see above)
