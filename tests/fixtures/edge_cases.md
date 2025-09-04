# Edge Cases and Parsing Challenges

This document tests various edge cases and potential parsing issues that might break or cause unexpected behavior in markdown-to-PDF conversion.

## Empty and Whitespace Handling

### Multiple Empty Lines



This paragraph follows multiple empty lines.

### Trailing Spaces    

This line has trailing spaces.    
This line also has trailing spaces.    

### Leading Spaces

    This line has leading spaces (not a code block).
  This line has fewer leading spaces.

## Malformed Markdown

### Incomplete Formatting

**This text is bold but not closed properly
*This text is italic but not closed properly
`This is inline code but not closed properly

### Mixed Formatting

**Bold text with *italic inside** and more italic*
***Triple asterisks with incomplete closure**
~~Strikethrough with **bold inside~~ and more bold**

### Broken Links

[Link with no URL]
[Link with empty URL]()
[Link with malformed URL](not-a-real-url
[Missing closing bracket](https://example.com)

![Image with no URL]
![Image with empty URL]()
![Malformed image](broken-image.jpg

## Special Characters in Headers

### Header with `code` inside
### Header with *italic* text
### Header with **bold** text
### Header with "quotes" and 'apostrophes'
### Header with $math$ symbols
### Header with <HTML> tags

## Nested Formatting Edge Cases

### Deep Nesting

> This is a blockquote
> > With nested blockquote
> > > And triple nested
> > > > And quadruple nested
> > > > > This is getting ridiculous

### List Nesting Extremes

1. Level 1
   1. Level 2
      1. Level 3
         1. Level 4
            1. Level 5
               1. Level 6
                  - Mixed with unordered
                    - And more nesting
                      - Even deeper
                        - This is probably too deep

### Code Block Edge Cases

```
Code block with no language specified
```

````
Code block with four backticks
Contains ```three backticks``` inside
````

```python
# Code with markdown inside comments
# **This should not be bold**
# [This should not be a link](https://example.com)
print("But this should be code")
```

## Table Edge Cases

### Table with Empty Cells

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   |          | Cell 3   |
|          | Cell 2   |          |
|          |          |          |

### Table with Malformed Rows

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Too | Few | 
| Too | Many | Cells | Here | Extra |
Completely malformed row without pipes
| Normal | Row | Again |

### Table with Special Characters

| Char | Unicode | HTML Entity | Description |
|------|---------|-------------|-------------|
| & | U+0026 | &amp; | Ampersand |
| < | U+003C | &lt; | Less than |
| > | U+003E | &gt; | Greater than |
| " | U+0022 | &quot; | Quote |
| ' | U+0027 | &#x27; | Apostrophe |

## Link and Image Edge Cases

### Links with Special Characters

[Link with spaces in URL]( https://example.com/path with spaces )
[Link with parentheses](https://example.com/path_(with)_parens)
[Link with square brackets](https://example.com/path[with][brackets])

### Nested Links and Images

[![Image inside link](https://via.placeholder.com/50x50.png)](https://example.com)

### Reference Links Edge Cases

[Reference link without definition][undefined-ref]

[Circular reference 1][circular2]
[Circular reference 2][circular1]

[circular1]: #circular2
[circular2]: #circular1

## HTML Edge Cases

### Unclosed Tags

<div>This div is never closed
<span>This span is also unclosed

<p>This paragraph has proper closing</p>

### Mixed HTML and Markdown

<div>
# This header is inside HTML
**This bold text is inside HTML**
</div>

### Comments

<!-- This is an HTML comment -->
<!-- Multi-line
HTML comment
that spans several lines -->

## Escape Characters

### Backslash Escapes

\*This should not be italic\*
\[This should not be a link\]
\`This should not be code\`
\\This should show a literal backslash

### Special Characters

These need escaping in some contexts: \\ \` \* \_ \{ \} \[ \] \( \) \# \+ \- \. \!

## Zero-Width and Invisible Characters

This line has a zero-width space:​
This line has a zero-width non-joiner:‌
This line has a zero-width joiner:‍

## Unicode Edge Cases

### Emoji Combinations

👨‍👩‍👧‍👦 Family emoji
🏳️‍🌈 Rainbow flag
👨🏽‍💻 Man technologist with skin tone

### Right-to-Left Text

This is English text עברית mixed with Hebrew

### Diacritics and Accents

Café, naïve, résumé, Zürich, São Paulo

## Number and List Edge Cases

### Unusual List Numbers

999999. Very large number
0. Zero start
-1. Negative number (should this work?)

### Mixed List Markers

* Asterisk
+ Plus
- Hyphen
  * Nested asterisk
  + Nested plus
  - Nested hyphen

## Code Fence Edge Cases

### Unusual Languages

```brainfuck
++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
```

```assembly
section .text
    global _start

_start:
    mov eax, 4
    mov ebx, 1
    mov ecx, hello
    mov edx, hello_len
    int 0x80
```

### Code with Extreme Indentation

```python
                                        def deeply_indented():
                                            return "This has extreme indentation"
```

## Pathological Cases

### Very Long Lines

This is a very long line that should test how the PDF converter handles line wrapping and whether it can properly break lines that exceed the page width without breaking words inappropriately or causing overflow issues in the final PDF output which should be handled gracefully by any robust markdown to PDF conversion system.

### Repetitive Patterns

# Header
## Header
### Header
#### Header
##### Header
###### Header

---
***
___

**Bold** *Italic* `Code` ~~Strike~~ **Bold** *Italic* `Code` ~~Strike~~ **Bold** *Italic* `Code` ~~Strike~~

### Empty Elements

[]()
![]()
``
****
____
~~~~~~

### Conflicting Syntax

This *should be italic and **should be bold* but not this**