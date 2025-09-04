#!/usr/bin/env python3
"""
Basic Usage Examples Runner

This script runs all the basic usage examples in sequence,
demonstrating the fundamental features of MD2PDF.
"""

import sys
import subprocess
from pathlib import Path


def run_example(script_name, description):
    """Run a single example script."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Script: {script_name}")
    print('='*60)
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print("✅ Example completed successfully")
        else:
            print(f"❌ Example failed with return code {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Failed to run example: {e}")
        return False


def main():
    """Run all basic usage examples."""
    print("MD2PDF Basic Usage Examples")
    print("=" * 40)
    print("This script demonstrates the fundamental features of MD2PDF")
    print("through a series of basic examples.\n")
    
    examples = [
        ("simple_conversion.py", "Simple Markdown to PDF Conversion"),
        ("output_customization.py", "Custom Output File Naming"),
        ("error_handling.py", "Basic Error Handling"),
        ("cli_examples.py", "Command Line Interface Examples"),
    ]
    
    results = []
    
    for script, description in examples:
        script_path = Path(__file__).parent / script
        
        if not script_path.exists():
            print(f"⚠️  Skipping {script} - file not found")
            results.append(False)
            continue
        
        success = run_example(script, description)
        results.append(success)
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    
    successful = sum(results)
    total = len(results)
    
    for i, (script, description) in enumerate(examples):
        status = "✅ PASSED" if results[i] else "❌ FAILED"
        print(f"{status} - {description}")
    
    print(f"\nTotal: {successful}/{total} examples passed")
    
    if successful == total:
        print("🎉 All basic examples completed successfully!")
        print("\nNext steps:")
        print("- Try the API examples: cd ../api_examples && python api_demo.py")
        print("- Explore styling: cd ../styling && python style_showcase.py")
        print("- Learn batch processing: cd ../batch_processing && python batch_demo.py")
    else:
        print("⚠️  Some examples failed. Check the output above for details.")
    
    return 0 if successful == total else 1


if __name__ == "__main__":
    exit(main())