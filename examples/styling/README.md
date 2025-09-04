# Styling Examples

This directory demonstrates MD2PDF's powerful styling capabilities, including built-in styles, themes, and custom styling options.

## Files in This Directory

- `style_showcase.py` - Demonstrates all built-in styles
- `theme_showcase.py` - Shows all color themes  
- `combination_demo.py` - Tests style + theme combinations
- `custom_styling.py` - Custom CSS and styling examples
- `comparison_generator.py` - Generate side-by-side style comparisons
- `sample_content.md` - Sample document for styling demonstrations

## Built-in Styles

MD2PDF includes 7 professional styles:

### Technical
- **Purpose**: Technical documentation, API guides, developer docs
- **Features**: Clean typography, excellent code formatting
- **Font**: Inter + JetBrains Mono
- **Best with themes**: Default, Dark, Oceanic, Midnight

### Modern  
- **Purpose**: Premium documentation, presentations
- **Features**: Sophisticated layout, contemporary design
- **Font**: Source Serif Pro + JetBrains Mono
- **Best with themes**: Elegant, Sophisticated, Minimal

### Whitepaper
- **Purpose**: Business documents, research papers, academic writing
- **Features**: Authoritative appearance, formal structure
- **Font**: Georgia + Consolas
- **Best with themes**: Default, Sophisticated, Minimal

### Story
- **Purpose**: Creative writing, narratives, literature
- **Features**: Book-like appearance, paragraph indentation
- **Font**: Crimson Text + Fira Code
- **Best with themes**: Sepia, Default, Forest

### Academic
- **Purpose**: Scholarly documents, theses, research papers
- **Features**: Formal academic formatting, citation-friendly
- **Font**: Times New Roman + Courier New
- **Best with themes**: Default, Sophisticated, Minimal

### Consultancy
- **Purpose**: Business reports, consulting documents
- **Features**: Professional corporate styling
- **Font**: Roboto + Roboto Mono
- **Best with themes**: Sophisticated, Elegant, Default

### Futuristic
- **Purpose**: Tech presentations, modern interfaces
- **Features**: Cutting-edge typography, unique elements
- **Font**: Orbitron + Fira Code  
- **Best with themes**: Midnight, Elegant, Dark

## Color Themes

MD2PDF provides 10 sophisticated color themes:

### Light Themes
- **Default**: Clean, professional standard colors
- **Minimal**: Elegant, sophisticated, timeless design
- **Sophisticated**: Refined with subtle accent colors
- **Oceanic**: Cool, calming blue tones
- **Forest**: Natural, earthy green palette  
- **Sepia**: Warm, vintage book-like colors
- **Agile**: Modern, dynamic for development docs

### Dark Themes
- **Elegant**: Sophisticated dark design with high contrast
- **Dark**: Light background with dark containers
- **Midnight**: High-contrast dark containers

## Running Style Examples

### View All Styles
```bash
python style_showcase.py
```
This generates PDFs using the same content with all available styles.

### View All Themes
```bash
python theme_showcase.py
```
This shows how each theme affects the appearance of documents.

### Test Combinations
```bash
python combination_demo.py
```
Generates PDFs for recommended style + theme combinations.

### Custom Styling
```bash
python custom_styling.py
```
Demonstrates how to add custom CSS and create custom styles.

## Style Selection Guide

### By Document Type

**Technical Documentation**
- Primary: `technical` + `oceanic`
- Alternative: `technical` + `dark`

**Business Reports**  
- Primary: `consultancy` + `sophisticated`
- Alternative: `whitepaper` + `minimal`

**Academic Papers**
- Primary: `academic` + `default`
- Alternative: `whitepaper` + `sophisticated`

**Creative Writing**
- Primary: `story` + `sepia`
- Alternative: `story` + `forest`

**Modern Documentation**
- Primary: `modern` + `elegant`
- Alternative: `modern` + `sophisticated`

**Presentations**
- Primary: `futuristic` + `midnight`
- Alternative: `modern` + `elegant`

### By Audience

**Executives/Management**
- `consultancy` + `sophisticated`
- `whitepaper` + `minimal`

**Developers/Technical**
- `technical` + `oceanic`
- `technical` + `dark`

**Academics/Researchers**  
- `academic` + `default`
- `whitepaper` + `sophisticated`

**General Public**
- `modern` + `default`
- `story` + `sepia`

## Customization Examples

### Adding Custom CSS

```python
from md2pdf import MD2PDFConverter

# Add custom CSS to any conversion
custom_css = """
/* Custom heading colors */
h1 { color: #2c3e50; border-bottom: 3px solid #3498db; }
h2 { color: #34495e; }

/* Custom code block styling */
.codehilite { 
    border-left: 4px solid #3498db;
    background: #f8f9fa;
}

/* Custom table styling */
table { 
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border-radius: 8px;
}
"""

converter = MD2PDFConverter()
converter.add_custom_css(custom_css)
converter.convert('document.md', 'custom_styled.pdf')
```

### Creating Theme Variants

```python
# Create a custom theme based on existing one
oceanic_variant_css = """
/* Oceanic Blue Variant - Darker blues */
:root {
    --theme-primary: #1e3a8a;      /* Darker blue */
    --theme-secondary: #1d4ed8;     /* Medium blue */
    --theme-accent: #3b82f6;        /* Light blue */
    --theme-text: #1f2937;          /* Dark gray */
    --theme-background: #ffffff;     /* White */
    --theme-surface: #f0f9ff;       /* Very light blue */
}
"""
```

## Performance Considerations

### Style Performance

**Fastest (Simple CSS)**
1. Technical
2. Academic  
3. Whitepaper

**Medium (Moderate CSS)**
4. Story
5. Consultancy
6. Modern

**Slowest (Complex CSS)**
7. Futuristic

### Theme Performance

**Fastest**: Default, Minimal, Dark
**Medium**: Sophisticated, Oceanic, Forest, Sepia
**Slowest**: Elegant, Midnight, Agile

## Best Practices

### Style Selection
1. **Match content type** to style purpose
2. **Consider target audience** preferences
3. **Test readability** with actual content
4. **Check print quality** if PDFs will be printed

### Theme Selection  
1. **Ensure sufficient contrast** for accessibility
2. **Consider brand colors** when choosing themes
3. **Test on different devices** and screen sizes
4. **Verify print appearance** for physical documents

### Custom Styling
1. **Use CSS variables** for consistent theming
2. **Test across different content types**
3. **Maintain print compatibility**
4. **Keep CSS simple** for better performance

## Troubleshooting

### Common Styling Issues

**Fonts not loading**
- Check internet connection for Google Fonts
- Verify font names are spelled correctly
- Consider using system font fallbacks

**Colors not appearing correctly**
- Ensure color values are valid CSS
- Check contrast ratios for accessibility
- Test in both light and dark environments

**Layout problems**
- Verify CSS syntax is correct
- Check for conflicting styles
- Test with simpler content first

**Performance issues**
- Use simpler styles for large documents
- Minimize custom CSS complexity
- Consider caching for batch processing

## Getting Help

For styling-related questions:

1. Check the [Styles and Themes Documentation](../../docs/styles_themes.rst)
2. Review built-in CSS files in `src/md2pdf/styles/`  
3. Open an issue for style bugs or requests
4. Share custom styles in GitHub Discussions

## Contributing Styles

To contribute new styles or themes:

1. Follow the [Contributing Guidelines](../../docs/contributing.rst)
2. Create CSS files following existing patterns
3. Test with various content types
4. Document style purpose and best use cases
5. Submit a pull request with examples