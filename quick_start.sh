#!/bin/bash

# MD2PDF Quick Start Script (standard workflow)
# Sets up the virtual environment and runs the default batch workflow over input/*.md

set -euo pipefail

echo "🚀 MD2PDF Quick Start"
echo "====================="

# Optional args: STYLE THEME (defaults to technical/default)
STYLE=${1:-technical}
THEME=${2:-default}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies if needed
source venv/bin/activate

# Compute requirements fingerprint
REQ_HASH=$(python3 - <<'PY'
import hashlib
with open('requirements.txt','rb') as f:
    print(hashlib.sha256(f.read()).hexdigest())
PY
)

if [ ! -f "venv/.requirements.sha256" ] || [ "$(cat venv/.requirements.sha256)" != "$REQ_HASH" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    echo "$REQ_HASH" > venv/.requirements.sha256
else
    echo "✅ Dependencies up to date."
fi

# Ensure workflow folders exist
mkdir -p data/input data/output data/processed

# Check and offer to download emoji assets if not present
if [ ! -d "assets/twemoji/svg" ] || [ $(find assets/twemoji/svg -name "*.svg" 2>/dev/null | wc -l) -eq 0 ]; then
    echo ""
    echo "📥 Emoji assets not found. Would you like to download them?"
    echo "   (Emojis will fallback to CDN if not downloaded)"
    read -p "Download emoji pack? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python scripts/setup_assets.py
    else
        echo "ℹ️  Skipping emoji download. Using CDN fallback."
    fi
fi

echo ""
echo "📂 Place your .md files in the 'data/input/' folder."
echo "   Running standard workflow with style='${STYLE}' theme='${THEME}'."

# Check for markdown files in data/input/
shopt -s nullglob
md_files=(data/input/*.md)
shopt -u nullglob

if [ ${#md_files[@]} -eq 0 ]; then
    echo "📝 No markdown files found in data/input/. Examples:"
    echo "   cp README.md data/input/"
    echo "   python md2pdf.py --list-styles   # discover styles"
    echo "   python md2pdf.py --list-themes   # discover themes"
    echo ""
    echo "👉 Then re-run: bash quick_start.sh [STYLE] [THEME]"
    exit 0
fi

# Run default workflow (processes all data/input/*.md → data/output/, moves originals to data/processed/)
python md2pdf.py --style "${STYLE}" --theme "${THEME}"

echo ""
echo "✅ Done! PDFs in 'data/output/', originals moved to 'data/processed/'."
echo "   Change style/theme by passing args: bash quick_start.sh modern sophisticated"
echo "   Or render a single file: python md2pdf.py README.md --style story --theme sepia"
