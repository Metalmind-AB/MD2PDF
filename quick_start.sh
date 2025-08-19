#!/bin/bash

# MD2PDF Quick Start Script
# This script sets up the virtual environment and converts your markdown files

echo "🚀 MD2PDF Quick Start"
echo "====================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Check if markdown files exist
if [ -f "action_documentation.md" ]; then
    echo "📄 Converting action_documentation.md with different style + theme combinations..."
    echo ""
    echo "🎯 Technical + Default theme..."
    python md2pdf.py action_documentation.md
    echo ""
    echo "📚 Story + Sepia theme..."
    python md2pdf.py action_documentation.md --style story --theme sepia -o action_documentation_story_sepia.pdf
    echo ""
    echo "🎨 Technical + Dark theme..."
    python md2pdf.py action_documentation.md --style technical --theme dark -o action_documentation_technical_dark.pdf
    echo ""
    echo "📄 Whitepaper + Oceanic theme..."
    python md2pdf.py action_documentation.md --style whitepaper --theme oceanic -o action_documentation_whitepaper_oceanic.pdf
    echo ""
    echo "✅ Done! Check the generated PDFs:"
    echo "   - action_documentation.pdf (technical + default)"
    echo "   - action_documentation_story_sepia.pdf (story + sepia)"
    echo "   - action_documentation_technical_dark.pdf (technical + dark)"
    echo "   - action_documentation_whitepaper_oceanic.pdf (whitepaper + oceanic)"
else
    echo "📝 No markdown files found. Usage examples:"
    echo "   python md2pdf.py your_file.md"
    echo "   python md2pdf.py your_file.md --style whitepaper --theme oceanic"
    echo "   python md2pdf.py your_file.md --style story --theme sepia"
    echo "   python md2pdf.py your_file.md --style technical --theme dark"
    echo "   python md2pdf.py --list-styles"
    echo "   python md2pdf.py --list-themes"
    echo "   python md2pdf.py --list-combinations"
fi

echo ""
echo "🎉 Setup complete! You can now use:"
echo "   source venv/bin/activate && python md2pdf.py your_file.md --style whitepaper --theme oceanic"
