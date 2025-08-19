#!/usr/bin/env python3
"""
Example usage of the MD2PDF converter with different style + theme combinations
"""

from md2pdf import MD2PDFConverter

def main():
    # Example 1: Convert with technical style + default theme
    print("📄 Converting with technical style + default theme...")
    converter = MD2PDFConverter('action_documentation.md', style='technical', theme='default')
    success = converter.convert()
    
    if success:
        print("✅ Technical + Default conversion successful!")
    else:
        print("❌ Technical + Default conversion failed!")
    
    # Example 2: Convert with story style + sepia theme
    print("\n📄 Converting with story style + sepia theme...")
    converter = MD2PDFConverter('action_documentation.md', output_file='action_documentation_story_sepia.pdf', style='story', theme='sepia')
    success = converter.convert()
    
    if success:
        print("✅ Story + Sepia conversion successful!")
    else:
        print("❌ Story + Sepia conversion failed!")
    
    # Example 3: Convert with technical style + dark theme
    print("\n📄 Converting with technical style + dark theme...")
    converter = MD2PDFConverter('action_documentation.md', output_file='action_documentation_technical_dark.pdf', style='technical', theme='dark')
    success = converter.convert()
    
    if success:
        print("✅ Technical + Dark conversion successful!")
    else:
        print("❌ Technical + Dark conversion failed!")
    
    # Example 4: Convert with whitepaper style + oceanic theme
    print("\n📄 Converting with whitepaper style + oceanic theme...")
    converter = MD2PDFConverter('action_documentation.md', output_file='action_documentation_whitepaper_oceanic.pdf', style='whitepaper', theme='oceanic')
    success = converter.convert()
    
    if success:
        print("✅ Whitepaper + Oceanic conversion successful!")
    else:
        print("❌ Whitepaper + Oceanic conversion failed!")

if __name__ == "__main__":
    main()
