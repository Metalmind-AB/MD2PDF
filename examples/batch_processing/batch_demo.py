#!/usr/bin/env python3
"""
Batch Processing Demonstration

This script demonstrates MD2PDF's batch processing capabilities
with multiple files, different styles, and comprehensive error handling.
"""

import glob
import sys
import time
from pathlib import Path

# Add the project root to the path so we can import md2pdf
project_root = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(project_root))

from md2pdf import MD2PDFConverter


def create_sample_documents():
    """Create sample markdown documents for batch processing."""
    sample_docs = {
        "technical_guide.md": """# Technical Integration Guide

This document explains how to integrate MD2PDF into your technical workflow.

## Installation

```bash
pip install md2pdf
```

## Basic Usage

```python
from md2pdf import MD2PDFConverter

converter = MD2PDFConverter()
converter.convert('document.md', 'output.pdf')
```

## Advanced Configuration

Use custom styles and themes:

```python
converter = MD2PDFConverter(
    style='technical',
    theme='oceanic'
)
```

## Conclusion

MD2PDF makes technical documentation beautiful and professional.
""",
        "business_report.md": """# Quarterly Business Report

## Executive Summary

This quarter showed significant growth across all business metrics.

## Key Performance Indicators

| Metric | Q3 2023 | Q4 2023 | Growth |
|--------|---------|---------|--------|
| Revenue | $1.2M | $1.8M | +50% |
| Customers | 450 | 680 | +51% |
| Retention | 94% | 96% | +2% |

## Strategic Initiatives

1. **Market Expansion**: Entered 3 new markets
2. **Product Development**: Launched 2 new features
3. **Team Growth**: Hired 15 new employees

## Financial Outlook

> The strong performance this quarter positions us well for continued growth in the coming year.

## Next Steps

- Expand sales team
- Invest in R&D
- Optimize operations
""",
        "user_manual.md": """# User Manual - Getting Started

Welcome to our comprehensive user manual.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Operations](#basic-operations)
3. [Advanced Features](#advanced-features)
4. [Troubleshooting](#troubleshooting)

## Getting Started

### System Requirements

- Operating System: Windows, macOS, or Linux
- Memory: 4GB RAM minimum
- Storage: 100MB available space

### Installation Steps

1. Download the installer
2. Run the installation wizard
3. Accept the license agreement
4. Choose installation directory
5. Complete the installation

## Basic Operations

### Creating Your First Document

To create a new document:

1. Click **File** → **New Document**
2. Choose a template from the gallery
3. Enter your content
4. Save the document

### Formatting Text

Use these keyboard shortcuts:

- **Ctrl+B**: Bold text
- **Ctrl+I**: Italic text
- **Ctrl+U**: Underline text
- **Ctrl+S**: Save document

## Advanced Features

### Custom Styles

Create custom styles for consistent formatting:

```css
.custom-heading {
    color: #2c3e50;
    font-size: 24px;
    font-weight: bold;
}
```

### Automation

Set up automated workflows:

1. Define trigger conditions
2. Configure actions
3. Test the workflow
4. Deploy to production

## Troubleshooting

**Problem**: Application won't start
**Solution**: Check system requirements and reinstall

**Problem**: Documents won't save
**Solution**: Verify file permissions and disk space
""",
        "creative_story.md": """# The Digital Garden

## Chapter 1: The Discovery

Sarah had always been fascinated by the intersection of technology and nature. As a software developer working from her small apartment, she dreamed of creating something that could bridge the digital and natural worlds.

One evening, while debugging a particularly stubborn piece of code, she stumbled upon an idea that would change everything.

## Chapter 2: The Vision

The concept was elegant in its simplicity: a digital garden where code could grow like plants, where algorithms could bloom into beautiful visualizations, and where data could flow like streams through a virtual landscape.

She began sketching her ideas:

- **Seed Functions**: Basic code blocks that could grow
- **Growth Algorithms**: Rules for how code evolves
- **Environmental Variables**: Conditions affecting growth
- **Harvest Cycles**: Points where code produces output

## Chapter 3: The Implementation

Working late into the night, Sarah began prototyping her digital garden. She chose Python for its readability and flexibility:

```python
class DigitalSeed:
    def __init__(self, code, growth_rate=1.0):
        self.code = code
        self.growth_rate = growth_rate
        self.maturity = 0

    def grow(self, environment):
        # Simulate growth based on environmental conditions
        self.maturity += self.growth_rate * environment.fertility
        return self.mature_code()

    def mature_code(self):
        if self.maturity >= 100:
            return self.code.optimize()
        return self.code
```

## Chapter 4: The Garden Blooms

As weeks turned into months, Sarah's digital garden began to take shape. Code snippets grew into full applications, simple algorithms evolved into complex systems, and what started as a personal project began attracting attention from the developer community.

### Key Features Developed

1. **Visual Code Evolution**: Watch your code grow in real-time
2. **Collaborative Gardening**: Multiple developers tending the same garden
3. **Harvest Analytics**: Metrics on code quality and performance
4. **Seasonal Cycles**: Automated refactoring and optimization periods

## Chapter 5: The Community

The digital garden concept resonated with developers worldwide. Soon, Sarah found herself at the center of a growing community of "digital gardeners" who shared her vision of making programming more organic and intuitive.

> "Programming isn't just about writing code," Sarah reflected. "It's about nurturing ideas and watching them grow into something beautiful and useful."

## Epilogue: Seeds of Change

Sarah's digital garden had grown beyond her wildest dreams. What started as a late-night coding session had blossomed into a movement that was changing how people think about software development.

The garden continues to grow, tended by a community of passionate developers who believe that code, like nature, is most beautiful when it's allowed to evolve organically.

---

*The End*

**Author's Note**: This story explores themes of creativity, community, and the organic nature of software development. The digital garden metaphor reminds us that great software grows through nurturing, patience, and collaboration.
""",
        "academic_paper.md": """# The Impact of Automated Document Generation on Technical Communication

## Abstract

This paper examines the role of automated document generation tools in modern technical communication workflows. Through analysis of case studies and user feedback, we demonstrate that tools like MD2PDF significantly improve documentation quality and reduce production time.

**Keywords**: technical communication, automation, document generation, PDF conversion, workflow optimization

## 1. Introduction

Technical documentation has evolved significantly with the advent of markup languages and automated generation tools. The transition from traditional word processors to markdown-based workflows represents a paradigm shift in how technical content is created, maintained, and distributed.

### 1.1 Research Questions

This study addresses the following research questions:

1. How do automated document generation tools impact documentation quality?
2. What are the measurable benefits in terms of time savings and consistency?
3. What challenges do organizations face when adopting these tools?

### 1.2 Methodology

We conducted a mixed-methods study involving:

- **Quantitative Analysis**: Performance metrics from 50 organizations
- **Qualitative Research**: Interviews with 25 technical writers
- **Case Studies**: In-depth analysis of 5 implementation projects

## 2. Literature Review

### 2.1 Traditional Documentation Challenges

Smith et al. (2019) identified key challenges in traditional documentation workflows:

- **Version Control Issues**: Multiple contributors working on shared documents
- **Formatting Inconsistencies**: Manual styling leading to visual discrepancies
- **Time Investment**: Significant overhead in document production
- **Maintenance Burden**: Difficulty keeping documentation current

### 2.2 Markup-Based Solutions

The emergence of lightweight markup languages has addressed many traditional challenges (Johnson, 2020):

```markdown
# Benefits of Markdown
- **Simplicity**: Easy to learn and write
- **Version Control**: Plain text files work with Git
- **Platform Independence**: Works across all systems
- **Automation**: Can be processed programmatically
```

### 2.3 Automated Generation Tools

Recent developments in automated document generation have shown promising results (Davis & Chen, 2021). Tools like MD2PDF represent the latest evolution in this space.

## 3. Case Study Analysis

### 3.1 Technology Company Implementation

**Organization**: Mid-size software company (200 employees)
**Challenge**: Inconsistent API documentation across teams
**Solution**: Implemented automated PDF generation from markdown sources

#### Results

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Doc Production Time | 8 hours | 2 hours | 75% reduction |
| Consistency Score | 6.2/10 | 9.1/10 | 47% improvement |
| User Satisfaction | 7.1/10 | 8.8/10 | 24% improvement |

### 3.2 Academic Institution Implementation

**Organization**: Large university computer science department
**Challenge**: Standardizing research paper formatting
**Solution**: Automated PDF generation with institutional styling

The implementation resulted in:

1. **Standardized Formatting**: All papers follow institutional guidelines
2. **Time Savings**: Faculty report 60% reduction in formatting time
3. **Focus on Content**: More time available for research and writing

## 4. Quantitative Analysis

### 4.1 Performance Metrics

Our analysis of 50 organizations revealed significant improvements:

- **Average Time Savings**: 68% reduction in document production time
- **Error Reduction**: 43% fewer formatting-related issues
- **Consistency Improvement**: 52% better visual consistency across documents

### 4.2 Statistical Significance

Using paired t-tests (p < 0.01), we found statistically significant improvements in:

- Document production efficiency (t = 12.34, p < 0.001)
- Visual consistency scores (t = 8.67, p < 0.001)
- User satisfaction ratings (t = 6.23, p < 0.001)

## 5. Implementation Challenges

### 5.1 Technical Barriers

Organizations reported several technical challenges:

1. **Learning Curve**: Staff training on markdown syntax
2. **Tool Integration**: Incorporating new tools into existing workflows
3. **Quality Assurance**: Ensuring automated output meets standards

### 5.2 Organizational Factors

Non-technical challenges included:

- **Resistance to Change**: Some team members preferred traditional tools
- **Initial Investment**: Setup time and training costs
- **Process Adaptation**: Modifying existing documentation workflows

## 6. Best Practices

Based on our research, we recommend the following best practices:

### 6.1 Implementation Strategy

1. **Pilot Programs**: Start with small teams or projects
2. **Training Investment**: Provide comprehensive staff training
3. **Gradual Migration**: Phase transition over several months
4. **Quality Metrics**: Establish measurement criteria

### 6.2 Tool Selection Criteria

When selecting automated generation tools, consider:

- **Output Quality**: Professional appearance and formatting
- **Customization Options**: Ability to match organizational branding
- **Integration Capabilities**: Compatibility with existing systems
- **Community Support**: Active development and user community

## 7. Future Research

This study opens several avenues for future research:

1. **Long-term Impact**: Longitudinal studies of automation adoption
2. **Industry Comparison**: Sector-specific analysis of benefits
3. **Technology Evolution**: Impact of AI on document generation
4. **User Experience**: Detailed usability studies

## 8. Conclusion

Automated document generation tools like MD2PDF represent a significant advancement in technical communication. Our research demonstrates measurable benefits in terms of efficiency, consistency, and user satisfaction.

Key findings include:

- **Significant Time Savings**: Average 68% reduction in production time
- **Improved Consistency**: 52% better visual standardization
- **High User Satisfaction**: 24% improvement in user ratings
- **Manageable Implementation**: Challenges are addressable with proper planning

Organizations considering adoption should focus on gradual implementation, comprehensive training, and clear quality metrics to maximize benefits.

## Acknowledgments

We thank the 50 organizations and 25 technical writers who participated in this study. Special recognition goes to the development teams creating tools that make technical communication more efficient and effective.

## References

Davis, M., & Chen, L. (2021). *Automated Documentation in Agile Development*. Journal of Technical Communication, 45(3), 234-248.

Johnson, R. (2020). *Markup Languages and Modern Documentation*. Technical Writing Quarterly, 38(2), 156-171.

Smith, A., Brown, K., & Wilson, J. (2019). *Challenges in Technical Documentation Management*. Communications Research, 29(4), 445-462.

---

*Corresponding Author*: Dr. Sarah Mitchell, Department of Technical Communication, State University. Email: s.mitchell@university.edu
""",
    }

    return sample_docs


def setup_sample_files(sample_dir):
    """Create sample files for batch processing demonstration."""
    print("Setting up sample documents...")

    sample_dir = Path(sample_dir)
    sample_dir.mkdir(exist_ok=True)

    sample_docs = create_sample_documents()
    created_files = []

    for filename, content in sample_docs.items():
        file_path = sample_dir / filename
        file_path.write_text(content)
        created_files.append(file_path)
        print(f"  ✓ Created: {filename}")

    return created_files


def demonstrate_single_style_batch(sample_files, style, theme, output_dir):
    """Demonstrate batch processing with a single style and theme."""
    print(
        f"\n--- Batch Processing with {style.title()} Style & {theme.title()} Theme ---"
    )

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    converter = MD2PDFConverter(style=style, theme=theme, verbose=True)

    successful = 0
    failed = 0

    for file_path in sample_files:
        try:
            # Generate output filename
            output_filename = f"{file_path.stem}_{style}_{theme}.pdf"
            output_path = output_dir / output_filename

            print(f"Converting: {file_path.name}")
            start_time = time.time()

            converter.convert(str(file_path), str(output_path))

            end_time = time.time()
            conversion_time = end_time - start_time

            # Check output file
            if output_path.exists():
                size_kb = output_path.stat().st_size / 1024
                print(
                    f"  ✅ Success: {output_filename} ({size_kb:.1f} KB, {conversion_time:.1f}s)"
                )
                successful += 1
            else:
                print(f"  ❌ Failed: Output file not created")
                failed += 1

        except Exception as e:
            print(f"  ❌ Error: {e}")
            failed += 1

    print(f"\nBatch Summary: {successful} successful, {failed} failed")
    return successful, failed


def demonstrate_multi_style_batch(sample_files, output_dir):
    """Demonstrate batch processing with different styles for different content types."""
    print(f"\n--- Smart Batch Processing (Content-Aware Styling) ---")

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # Define content-specific styling rules
    styling_rules = {
        "technical_guide.md": {"style": "technical", "theme": "oceanic"},
        "business_report.md": {"style": "consultancy", "theme": "sophisticated"},
        "user_manual.md": {"style": "whitepaper", "theme": "minimal"},
        "creative_story.md": {"style": "story", "theme": "sepia"},
        "academic_paper.md": {"style": "academic", "theme": "default"},
    }

    results = []

    for file_path in sample_files:
        filename = file_path.name

        if filename in styling_rules:
            rules = styling_rules[filename]
            style = rules["style"]
            theme = rules["theme"]

            print(f"\nProcessing: {filename}")
            print(f"  Style: {style.title()}")
            print(f"  Theme: {theme.title()}")

            try:
                converter = MD2PDFConverter(style=style, theme=theme, verbose=False)

                output_filename = f"{file_path.stem}_smart_{style}_{theme}.pdf"
                output_path = output_dir / output_filename

                start_time = time.time()
                converter.convert(str(file_path), str(output_path))
                end_time = time.time()

                if output_path.exists():
                    size_kb = output_path.stat().st_size / 1024
                    conversion_time = end_time - start_time

                    results.append(
                        {
                            "file": filename,
                            "output": output_filename,
                            "style": style,
                            "theme": theme,
                            "size_kb": size_kb,
                            "time_s": conversion_time,
                            "success": True,
                        }
                    )

                    print(
                        f"  ✅ Success: {output_filename} ({size_kb:.1f} KB, {conversion_time:.1f}s)"
                    )
                else:
                    results.append(
                        {"file": filename, "success": False, "error": "No output file"}
                    )
                    print(f"  ❌ Failed: Output file not created")

            except Exception as e:
                results.append({"file": filename, "success": False, "error": str(e)})
                print(f"  ❌ Error: {e}")
        else:
            print(f"Skipping: {filename} (no styling rule defined)")

    # Summary
    successful = sum(1 for r in results if r.get("success", False))
    total = len(results)

    print(f"\nSmart Batch Summary:")
    print(f"  Total files: {total}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {total - successful}")

    if successful > 0:
        avg_size = (
            sum(r.get("size_kb", 0) for r in results if r.get("success")) / successful
        )
        avg_time = (
            sum(r.get("time_s", 0) for r in results if r.get("success")) / successful
        )
        print(f"  Average size: {avg_size:.1f} KB")
        print(f"  Average time: {avg_time:.1f}s")

    return results


def demonstrate_error_handling(sample_dir, output_dir):
    """Demonstrate robust error handling in batch processing."""
    print(f"\n--- Error Handling Demonstration ---")

    # Create problematic files for testing error handling
    problem_files = {
        "empty_file.md": "",  # Empty file
        "invalid_syntax.md": "# Title\n\n```python\n# Unclosed code block",  # Unclosed code block
        "very_large.md": "# Large Document\n\n"
        + "This is a test paragraph. " * 1000,  # Large file
    }

    sample_dir = Path(sample_dir)
    problem_file_paths = []

    print("Creating problematic test files:")
    for filename, content in problem_files.items():
        file_path = sample_dir / filename
        file_path.write_text(content)
        problem_file_paths.append(file_path)
        print(f"  ✓ Created: {filename}")

    # Batch process with error handling
    converter = MD2PDFConverter(style="technical", theme="default")
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    errors = []
    successful = []

    for file_path in problem_file_paths:
        try:
            output_path = output_dir / f"{file_path.stem}_error_test.pdf"
            print(f"\nProcessing: {file_path.name}")

            converter.convert(str(file_path), str(output_path))

            if output_path.exists():
                size_kb = output_path.stat().st_size / 1024
                successful.append({"file": file_path.name, "size": size_kb})
                print(f"  ✅ Unexpected success: {output_path.name} ({size_kb:.1f} KB)")
            else:
                errors.append({"file": file_path.name, "error": "No output created"})
                print(f"  ❌ Failed: No output file created")

        except Exception as e:
            errors.append({"file": file_path.name, "error": str(e)})
            print(f"  ❌ Expected error: {e}")

    print(f"\nError Handling Summary:")
    print(f"  Test files processed: {len(problem_file_paths)}")
    print(f"  Successful conversions: {len(successful)}")
    print(f"  Errors caught: {len(errors)}")

    # Cleanup problem files
    for file_path in problem_file_paths:
        file_path.unlink()

    return errors, successful


def main():
    """Run comprehensive batch processing demonstration."""
    print("MD2PDF Batch Processing Demonstration")
    print("=" * 50)

    # Setup
    sample_dir = Path("sample_docs")
    output_dir = Path("batch_output")

    try:
        # Create sample documents
        sample_files = setup_sample_files(sample_dir)

        # Demonstration 1: Single style batch processing
        print("\n" + "=" * 50)
        print("DEMONSTRATION 1: Single Style Batch Processing")
        print("=" * 50)

        demo1_success, demo1_failed = demonstrate_single_style_batch(
            sample_files,
            style="technical",
            theme="oceanic",
            output_dir=output_dir / "single_style",
        )

        # Demonstration 2: Multi-style intelligent batch processing
        print("\n" + "=" * 50)
        print("DEMONSTRATION 2: Intelligent Multi-Style Processing")
        print("=" * 50)

        demo2_results = demonstrate_multi_style_batch(
            sample_files, output_dir=output_dir / "multi_style"
        )

        # Demonstration 3: Error handling
        print("\n" + "=" * 50)
        print("DEMONSTRATION 3: Error Handling")
        print("=" * 50)

        demo3_errors, demo3_success = demonstrate_error_handling(
            sample_dir, output_dir=output_dir / "error_tests"
        )

        # Final summary
        print("\n" + "=" * 50)
        print("FINAL SUMMARY")
        print("=" * 50)

        print(f"📁 Sample documents created: {len(sample_files)}")
        print(
            f"📄 Single-style conversions: {demo1_success} successful, {demo1_failed} failed"
        )
        print(
            f"🎨 Multi-style conversions: {sum(1 for r in demo2_results if r.get('success', False))} successful"
        )
        print(
            f"⚠️  Error handling tests: {len(demo3_errors)} errors caught, {len(demo3_success)} unexpected successes"
        )

        # Show output directory structure
        print(f"\n📂 Output directory: {output_dir.absolute()}")

        if output_dir.exists():
            pdf_files = list(output_dir.glob("**/*.pdf"))
            if pdf_files:
                total_size_kb = sum(f.stat().st_size / 1024 for f in pdf_files)
                print(f"📄 Total PDFs generated: {len(pdf_files)}")
                print(f"📊 Total size: {total_size_kb:.1f} KB")

                print("\nGenerated files:")
                for pdf_file in sorted(pdf_files):
                    relative_path = pdf_file.relative_to(output_dir)
                    size_kb = pdf_file.stat().st_size / 1024
                    print(f"  📄 {relative_path} ({size_kb:.1f} KB)")
            else:
                print("⚠️  No PDF files were generated")

        print(f"\n🎉 Batch processing demonstration complete!")
        print(f"\nNext steps:")
        print(f"  - Review generated PDFs in {output_dir}")
        print(f"  - Try your own batch processing with: md2pdf *.md")
        print(f"  - Explore advanced examples in other directories")

    except Exception as e:
        print(f"❌ Demonstration failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
