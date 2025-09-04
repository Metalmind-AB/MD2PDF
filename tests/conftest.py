# Copyright (c) 2025 MPS Metalmind AB
# Licensed under the MIT License (see LICENSE file)

"""
PyTest configuration and fixtures for MD2PDF tests.
"""

import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)


@pytest.fixture
def sample_markdown() -> str:
    """Return sample markdown content for testing."""
    return """# Test Document

## Introduction

This is a **test document** for testing the MD2PDF converter.

### Features

- Bullet point 1
- Bullet point 2
- Bullet point 3

1. Numbered item 1
2. Numbered item 2
3. Numbered item 3

### Code Example

```python
def hello_world():
    print("Hello, World!")
```

### Table Example

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |

### Quote

> This is a blockquote.
> It can span multiple lines.

### Links and Images

[Visit GitHub](https://github.com)

---

## Conclusion

This concludes the test document.
"""


@pytest.fixture
def complex_markdown() -> str:
    """Return complex markdown content with various features."""
    return """# Complex Test Document

## Math and Special Characters

Inline math: $E = mc^2$

Block math:
$$
\\int_{0}^{\\infty} e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}
$$

## Nested Lists

1. First level
   - Second level bullet
   - Another bullet
     1. Third level numbered
     2. Another number
   - Back to second level
2. Back to first level

## Task Lists

- [x] Completed task
- [ ] Incomplete task
- [x] Another completed task

## Definition Lists

Term 1
: Definition 1

Term 2
: Definition 2a
: Definition 2b

## Footnotes

Here is a footnote reference[^1].

[^1]: This is the footnote.

## HTML Elements

<details>
<summary>Click to expand</summary>

Hidden content here.

</details>

## Emoji Support

:smile: :heart: :thumbsup:

## Long Code Block

```python
class ComplexClass:
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    def process(self, data: list) -> dict:
        '''Process the data and return results.'''
        result = {}
        for item in data:
            if isinstance(item, str):
                result[item] = len(item)
            elif isinstance(item, int):
                result[str(item)] = item * 2
        return result

    def __repr__(self) -> str:
        return f"ComplexClass(name={self.name}, value={self.value})"
```

## Special Characters & Escaping

Testing special characters: & < > " ' \\ | * _ ` # + - . ! [ ] ( ) { }

## Unicode Support

Chinese: 你好世界
Japanese: こんにちは世界
Arabic: مرحبا بالعالم
Emoji: 🚀 🎉 💻 📚
"""


@pytest.fixture
def minimal_markdown() -> str:
    """Return minimal markdown content."""
    return "# Simple Title\n\nSimple paragraph."


@pytest.fixture
def sample_markdown_file(temp_dir: Path, sample_markdown: str) -> Path:
    """Create a sample markdown file in temp directory."""
    file_path = temp_dir / "sample.md"
    file_path.write_text(sample_markdown)
    return file_path


@pytest.fixture
def multiple_markdown_files(temp_dir: Path) -> list[Path]:
    """Create multiple markdown files for batch processing tests."""
    files = []
    for i in range(3):
        file_path = temp_dir / f"test_{i}.md"
        content = f"# Document {i}\n\nContent for document {i}."
        file_path.write_text(content)
        files.append(file_path)
    return files


@pytest.fixture
def mock_css_content() -> str:
    """Return mock CSS content for style testing."""
    return """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&display=swap');

body {
    font-family: 'Inter', sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333333;
}

h1 {
    font-size: 24pt;
    font-weight: 700;
    color: #000000;
    margin-bottom: 12pt;
}

code {
    font-family: 'JetBrains Mono', monospace;
    background-color: #f5f5f5;
    padding: 2px 4px;
    border-radius: 3px;
}
"""


@pytest.fixture
def invalid_markdown() -> str:
    """Return markdown that might cause parsing issues."""
    return """# Unclosed Code Block

```python
def broken_function():
    # Missing closing backticks

## Another Section

[Broken link](
"""


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment variables before each test."""
    # Store original environment
    original_env = os.environ.copy()

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def mock_converter_config() -> dict:
    """Return mock configuration for converter testing."""
    return {
        "style": "technical",
        "theme": "default",
        "margin": "15mm",
        "page_size": "A4",
        "landscape": False,
        "page_numbers": True,
        "toc": False,
    }


# Markers for test categorization
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "cli: marks tests as CLI tests")
    config.addinivalue_line("markers", "style: marks tests as style-related tests")
