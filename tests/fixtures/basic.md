# Basic Markdown Test

This is a simple markdown document to test basic conversion functionality.

## Introduction

This document contains the most commonly used markdown elements that should be properly converted to PDF format.

### Headings

We have multiple heading levels to test hierarchy:

#### Level 4 Heading
##### Level 5 Heading
###### Level 6 Heading

## Text Formatting

Here we test various text formatting options:

- **Bold text** using double asterisks
- *Italic text* using single asterisks
- ***Bold and italic text*** using triple asterisks
- `Inline code` using backticks
- ~~Strikethrough text~~ using tildes

## Lists

### Unordered Lists

- First item
- Second item
  - Nested item 1
  - Nested item 2
    - Deeply nested item
- Third item

### Ordered Lists

1. First numbered item
2. Second numbered item
   1. Nested numbered item
   2. Another nested item
3. Third numbered item

### Mixed Lists

1. Ordered item
   - Unordered sub-item
   - Another sub-item
2. Another ordered item
   1. Nested ordered
   2. Another nested ordered

## Paragraphs

This is a regular paragraph with some text. It should wrap properly and maintain proper spacing between paragraphs.

This is another paragraph to test spacing. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

## Links

Here are some test links:

- [External link](https://www.example.com)
- [Link with title](https://www.example.com "Example Website")
- Reference style link: [Reference Link][ref1]

[ref1]: https://www.example.com "Reference Link"

## Images

![Alt text for image](https://via.placeholder.com/300x200.png "Test Image")

## Blockquotes

> This is a blockquote. It should be properly indented and formatted differently from regular text.
> 
> This is a continuation of the blockquote with another paragraph.

> Nested blockquote:
> > This is nested inside another blockquote.

## Horizontal Rules

Here's a horizontal rule:

---

And another one:

***

## Line Breaks

This line ends with two spaces  
So this should be on a new line.

This paragraph
has line breaks but
they should not be preserved
unless there are two trailing spaces.