# Getting Started with MD2PDF

Welcome to **MD2PDF**, the beautiful Markdown to PDF converter that transforms your documentation into professional-looking PDFs with style and elegance.

## What is MD2PDF?

MD2PDF is a comprehensive Python tool designed to convert Markdown files into impeccably beautiful PDFs. It features:

- 🎨 **Dynamic Style System** with professional templates
- 🌈 **Sophisticated Color Themes** for any occasion
- 📝 **Advanced Markdown Support** with syntax highlighting
- 📄 **Professional Layout** optimized for print and digital
- 🔄 **Batch Processing** for handling multiple files
- 🎯 **Code Block Management** with proper wrapping

## Quick Start

### Installation

Install MD2PDF from PyPI:

```bash
pip install md2pdf
```

### Basic Usage

Convert a markdown file to PDF:

```bash
md2pdf document.md
```

With custom styling:

```bash
md2pdf document.md --style modern --theme elegant
```

### Python API

```python
from md2pdf import MD2PDFConverter

# Simple conversion
converter = MD2PDFConverter()
converter.convert('document.md', 'output.pdf')

# With styling
converter = MD2PDFConverter(style='whitepaper', theme='sophisticated')
converter.convert('document.md', 'styled_output.pdf')
```

## Available Styles

| Style | Description | Best For |
|-------|-------------|----------|
| **Technical** | Clean, professional, code-friendly | API docs, guides |
| **Modern** | Sophisticated, elegant, contemporary | Premium docs |
| **Whitepaper** | Academic, authoritative | Business docs |
| **Story** | Literary, elegant, readable | Creative writing |
| **Academic** | Formal, scholarly | Research papers |

## Color Themes

Choose from 10 beautiful color themes:

- **Default**: Clean and professional
- **Minimal**: Sophisticated, timeless
- **Sophisticated**: Refined with subtle accents
- **Elegant**: Premium dark design
- **Oceanic**: Cool blue tones
- **Forest**: Natural green palette
- **Sepia**: Vintage book-like colors

## Advanced Features

### Code Syntax Highlighting

MD2PDF provides excellent syntax highlighting for code blocks:

```python
def hello_world():
    """A simple greeting function."""
    message = "Hello, World!"
    print(message)
    return message

# Call the function
greeting = hello_world()
```

```javascript
// JavaScript example
const converter = new MD2PDFConverter({
    style: 'modern',
    theme: 'elegant'
});

converter.convert('README.md')
    .then(result => console.log('Success!', result))
    .catch(error => console.error('Error:', error));
```

### Tables

MD2PDF renders beautiful tables with alternating row colors:

| Feature | Status | Notes |
|---------|--------|-------|
| Markdown Processing | ✅ Complete | Full CommonMark support |
| PDF Generation | ✅ Complete | WeasyPrint integration |
| Style System | ✅ Complete | 7 built-in styles |
| Theme System | ✅ Complete | 10 color themes |
| CLI Interface | ✅ Complete | Full command-line support |
| Python API | ✅ Complete | Comprehensive API |

### Lists and Formatting

MD2PDF handles all standard Markdown formatting:

**Ordered Lists:**
1. First item with **bold text**
2. Second item with *italic text*
3. Third item with `inline code`
4. Fourth item with [a link](https://github.com/mps-metalmind/md2pdf)

**Unordered Lists:**
- Bullet point with normal text
- Another point with **emphasis**
- Nested lists are supported:
  - Nested item one
  - Nested item two
  - Even deeper nesting:
    - Deep nested item
    - Another deep item

### Blockquotes

> MD2PDF transforms your markdown into beautiful, professional PDFs with sophisticated styling and layout. Whether you're creating technical documentation, academic papers, or business reports, MD2PDF provides the tools you need to make your content shine.

### Images and Media

MD2PDF supports responsive image handling (when images are available):

![MD2PDF Logo](https://via.placeholder.com/400x200/3366cc/ffffff?text=MD2PDF)

*Images are automatically resized and positioned for optimal PDF layout.*

## Getting Help

Need assistance? Here are your options:

- 📚 **Documentation**: [https://md2pdf.readthedocs.io](https://md2pdf.readthedocs.io)
- 🐛 **Issues**: [GitHub Issues](https://github.com/mps-metalmind/md2pdf/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/mps-metalmind/md2pdf/discussions)
- 📧 **Email**: info@metalmind.se

## What's Next?

Now that you've learned the basics, explore these advanced features:

1. **Batch Processing**: Convert multiple files at once
2. **Custom Styles**: Create your own visual themes
3. **API Integration**: Embed MD2PDF in your applications
4. **Configuration Files**: Set up project-specific defaults
5. **Advanced Layouts**: Master complex document structures

---

**Happy converting!** 🎉

Transform your markdown into beautiful PDFs with MD2PDF.
