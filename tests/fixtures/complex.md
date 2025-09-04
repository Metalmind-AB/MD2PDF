# Complex Markdown Features Test

This document tests advanced markdown features that require more sophisticated parsing and rendering.

## Code Blocks

### Inline Code with Various Languages

Here's some `Python` code: `print("Hello, World!")`
And some `JavaScript`: `console.log("Hello, World!");`

### Fenced Code Blocks

```python
def fibonacci(n):
    """Generate Fibonacci sequence up to n terms."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])

    return sequence

# Example usage
fib_numbers = fibonacci(10)
print(f"First 10 Fibonacci numbers: {fib_numbers}")
```

```javascript
class Calculator {
    constructor() {
        this.result = 0;
    }

    add(value) {
        this.result += value;
        return this;
    }

    multiply(value) {
        this.result *= value;
        return this;
    }

    getResult() {
        return this.result;
    }
}

// Chaining operations
const calc = new Calculator();
const result = calc.add(5).multiply(3).add(2).getResult();
console.log(`Result: ${result}`); // Output: 17
```

```sql
-- Complex SQL query with joins and subqueries
SELECT
    u.username,
    u.email,
    COUNT(o.id) as order_count,
    SUM(oi.quantity * p.price) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
LEFT JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.id
WHERE u.created_at >= '2023-01-01'
    AND u.status = 'active'
GROUP BY u.id, u.username, u.email
HAVING COUNT(o.id) > 0
ORDER BY total_spent DESC, order_count DESC
LIMIT 50;
```

## Tables

### Simple Table

| Name | Age | City |
|------|-----|------|
| Alice | 30 | New York |
| Bob | 25 | Los Angeles |
| Charlie | 35 | Chicago |

### Complex Table with Alignment

| Feature | Basic Plan | Pro Plan | Enterprise |
|:--------|:----------:|:--------:|-----------:|
| Users | 1-5 | 6-50 | Unlimited |
| Storage | 10GB | 100GB | 1TB |
| Support | Email | Email + Chat | 24/7 Phone |
| Price/month | $9.99 | $29.99 | $99.99 |
| API Calls | 1,000 | 10,000 | Unlimited |
| Custom Integrations | ❌ | ✅ | ✅ |
| Analytics Dashboard | Basic | Advanced | Enterprise |

### Table with Code and Links

| Language | Syntax | Example | Documentation |
|----------|--------|---------|---------------|
| Python | `def function():` | `print("Hello")` | [Python Docs](https://docs.python.org) |
| JavaScript | `function name() {}` | `console.log("Hi")` | [MDN Web Docs](https://developer.mozilla.org) |
| Go | `func name() {}` | `fmt.Println("Hello")` | [Go Docs](https://golang.org/doc/) |

## Mathematical Expressions

### Inline Math

The quadratic formula is $x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$ and Euler's identity is $e^{i\pi} + 1 = 0$.

### Block Math

$$
\begin{align}
\nabla \times \vec{\mathbf{B}} -\, \frac1c\, \frac{\partial\vec{\mathbf{E}}}{\partial t} &= \frac{4\pi}{c}\vec{\mathbf{j}} \\
\nabla \cdot \vec{\mathbf{E}} &= 4 \pi \rho \\
\nabla \times \vec{\mathbf{E}}\, +\, \frac1c\, \frac{\partial\vec{\mathbf{B}}}{\partial t} &= \vec{\mathbf{0}} \\
\nabla \cdot \vec{\mathbf{B}} &= 0
\end{align}
$$

### Statistical Formulas

The normal distribution probability density function:

$$
f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}
$$

## Task Lists

- [x] Completed task
- [x] Another completed task
- [ ] Pending task
- [ ] Another pending task
  - [x] Completed subtask
  - [ ] Pending subtask

## Definition Lists

HTML
: HyperText Markup Language, the standard markup language for creating web pages.

CSS
: Cascading Style Sheets, used for describing the presentation of a document written in HTML.

JavaScript
: A high-level, interpreted programming language that conforms to the ECMAScript specification.

## Footnotes

This text has a footnote[^1]. Here's another sentence with a different footnote[^note].

[^1]: This is the first footnote with some additional information.
[^note]: This is a named footnote that provides extra context.

## Nested Blockquotes with Code

> This is a complex blockquote that contains code:
>
> ```python
> def example():
>     return "This is code inside a blockquote"
> ```
>
> > And this is a nested blockquote inside the original blockquote.
> > It should maintain proper indentation.

## HTML in Markdown

<div align="center">
    <strong>This is HTML content within Markdown</strong>
    <br>
    <em>It should be preserved in the conversion</em>
</div>

<details>
<summary>Click to expand details</summary>

This content is initially hidden and can be toggled. It tests HTML details/summary elements.

```bash
# This is a bash command inside the details
echo "Hidden content revealed!"
```

</details>

## Advanced List Formatting

1. **First major point** with *emphasis*
   - Sub-point with `inline code`
   - Another sub-point
     ```python
     # Code block within list
     print("Nested code block")
     ```
   - Final sub-point

2. **Second major point**

   This paragraph is part of the second list item. It should maintain proper indentation.

   | Column 1 | Column 2 |
   |----------|----------|
   | Data 1   | Data 2   |

   - Nested list within the major point
   - Another nested item

3. **Third major point** ending the list
