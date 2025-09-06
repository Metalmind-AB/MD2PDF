#!/usr/bin/env python3
"""
Test md2pdf package installation in a clean environment.

This script creates a fresh virtual environment and tests the installation
of the md2pdf package from the built distribution.
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def run_command(cmd, cwd=None, capture=True):
    """Run a command and return output."""
    print(f"  Running: {' '.join(cmd)}")
    if capture:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  Error: {result.stderr}")
        return result
    else:
        return subprocess.run(cmd, cwd=cwd)


def test_installation():
    """Test package installation in a clean environment."""

    # Get the dist directory
    project_dir = Path(__file__).parent.parent
    dist_dir = project_dir / "dist"

    # Find the wheel file
    wheel_files = list(dist_dir.glob("*.whl"))
    if not wheel_files:
        print("❌ No wheel file found in dist/")
        return False

    wheel_file = wheel_files[0]
    print(f"✓ Found wheel file: {wheel_file.name}")
    print(f"  Size: {wheel_file.stat().st_size / (1024*1024):.2f} MB")

    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        print(f"\n📁 Testing in: {temp_path}")

        # Create a virtual environment
        print("\n🔧 Creating virtual environment...")
        venv_path = temp_path / "test_venv"
        result = run_command([sys.executable, "-m", "venv", str(venv_path)])
        if result.returncode != 0:
            print("❌ Failed to create virtual environment")
            return False
        print("✓ Virtual environment created")

        # Determine the pip and python paths
        if sys.platform == "win32":
            pip_path = venv_path / "Scripts" / "pip.exe"
            python_path = venv_path / "Scripts" / "python.exe"
        else:
            pip_path = venv_path / "bin" / "pip"
            python_path = venv_path / "bin" / "python"

        # Upgrade pip
        print("\n📦 Upgrading pip...")
        run_command([str(pip_path), "install", "--upgrade", "pip"])

        # Install the package
        print(f"\n📦 Installing {wheel_file.name}...")
        result = run_command([str(pip_path), "install", str(wheel_file)])
        if result.returncode != 0:
            print("❌ Failed to install package")
            return False
        print("✓ Package installed successfully")

        # Test imports
        print("\n🧪 Testing imports...")
        test_imports = [
            "import md2pdf",
            "from md2pdf import __version__",
            "from md2pdf.core.converter import MD2PDFConverter",
            "from md2pdf.cli import main",
        ]

        for test_import in test_imports:
            result = run_command([str(python_path), "-c", test_import], capture=True)
            if result.returncode != 0:
                print(f"❌ Failed: {test_import}")
                print(f"  Error: {result.stderr}")
                return False
            print(f"✓ {test_import}")

        # Test CLI
        print("\n🖥️  Testing CLI...")

        # Test --version
        result = run_command(
            [str(python_path), "-m", "md2pdf", "--version"], capture=True
        )
        if result.returncode != 0:
            print("❌ Failed to run: md2pdf --version")
            return False
        version = result.stdout.strip()
        print(f"✓ Version: {version}")

        # Test --help
        result = run_command([str(python_path), "-m", "md2pdf", "--help"], capture=True)
        if result.returncode != 0:
            print("❌ Failed to run: md2pdf --help")
            return False
        print("✓ Help command works")

        # Test --list-styles
        result = run_command(
            [str(python_path), "-m", "md2pdf", "--list-styles"], capture=True
        )
        if result.returncode != 0:
            print("❌ Failed to run: md2pdf --list-styles")
            return False
        print("✓ List styles works")

        # Test --list-themes
        result = run_command(
            [str(python_path), "-m", "md2pdf", "--list-themes"], capture=True
        )
        if result.returncode != 0:
            print("❌ Failed to run: md2pdf --list-themes")
            return False
        print("✓ List themes works")

        # Test conversion (create a simple markdown file)
        print("\n📄 Testing conversion...")
        test_md = temp_path / "test.md"
        test_md.write_text(
            """# Test Document

This is a test document for **md2pdf**.

## Features
- Bullet point 1
- Bullet point 2

```python
def hello():
    print("Hello, World!")
```

> This is a blockquote.

| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |
"""
        )

        result = run_command(
            [
                str(python_path),
                "-m",
                "md2pdf",
                str(test_md),
                "-o",
                str(temp_path / "test.pdf"),
                "--style",
                "technical",
                "--theme",
                "github",
            ],
            capture=True,
        )
        if result.returncode != 0:
            print("❌ Failed to convert markdown to PDF")
            print(f"  Error: {result.stderr}")
            return False

        # Check if PDF was created
        pdf_path = temp_path / "test.pdf"
        if not pdf_path.exists():
            print("❌ PDF file was not created")
            return False

        pdf_size = pdf_path.stat().st_size
        print(f"✓ PDF created successfully ({pdf_size:,} bytes)")

        # Test package metadata
        print("\n📊 Package metadata:")
        result = run_command([str(pip_path), "show", "md2pdf"], capture=True)
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                if line.startswith(("Name:", "Version:", "Summary:", "License:")):
                    print(f"  {line}")

        # List installed dependencies
        print("\n📦 Installed dependencies:")
        result = run_command([str(pip_path), "list", "--format", "json"], capture=True)
        if result.returncode == 0:
            packages = json.loads(result.stdout)
            core_deps = [
                "markdown",
                "weasyprint",
                "pygments",
                "beautifulsoup4",
                "click",
                "rich",
            ]
            for pkg in packages:
                if any(dep in pkg["name"].lower() for dep in core_deps):
                    print(f"  - {pkg['name']} {pkg['version']}")

    return True


def test_import_performance():
    """Test import time of the package."""
    print("\n⏱️  Testing import performance...")

    # Test import time
    import_test = """
import time
start = time.perf_counter()
import md2pdf
end = time.perf_counter()
print(f"{(end - start) * 1000:.2f}")
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(import_test)
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, temp_file], capture_output=True, text=True
        )
        if result.returncode == 0:
            import_time = float(result.stdout.strip())
            print(f"  Import time: {import_time:.2f} ms")
            if import_time > 1000:
                print("  ⚠️  Warning: Import time is over 1 second")
            else:
                print("  ✓ Import time is acceptable")
    finally:
        os.unlink(temp_file)


def main():
    """Run all installation tests."""
    print("=" * 60)
    print("MD2PDF Installation Test Suite")
    print("=" * 60)

    # Test installation
    print("\n🚀 Starting installation test...")
    if not test_installation():
        print("\n❌ Installation test failed!")
        return 1

    print("\n✅ Installation test passed!")

    # Test import performance
    test_import_performance()

    print("\n" + "=" * 60)
    print("✨ All tests passed successfully!")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
