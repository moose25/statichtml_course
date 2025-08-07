import unittest

from markdown_blocks import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
# This is an h1

## This is an h2

### This is an h3 with **bold** text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is an h1</h1><h2>This is an h2</h2><h3>This is an h3 with <b>bold</b> text</h3></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> with multiple lines
> and **bold** text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines and <b>bold</b> text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- First item with **bold**
- Second item with _italic_
- Third item with `code`
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item with <b>bold</b></li><li>Second item with <i>italic</i></li><li>Third item with <code>code</code></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First numbered item
2. Second numbered item with **bold**
3. Third numbered item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First numbered item</li><li>Second numbered item with <b>bold</b></li><li>Third numbered item</li></ol></div>",
        )

    def test_mixed_content(self):
        md = """
# Main Heading

This is a paragraph with **bold** and _italic_ text.

## Subheading

Here's a list:

- Item one
- Item two

And here's some code:

```
def hello():
    print("Hello, world!")
```

> This is a quote block
> with multiple lines

1. Ordered item one
2. Ordered item two
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>"
            "<h1>Main Heading</h1>"
            "<p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p>"
            "<h2>Subheading</h2>"
            "<p>Here's a list:</p>"
            "<ul><li>Item one</li><li>Item two</li></ul>"
            "<p>And here's some code:</p>"
            "<pre><code>def hello():\n    print(\"Hello, world!\")\n</code></pre>"
            "<blockquote>This is a quote block with multiple lines</blockquote>"
            "<ol><li>Ordered item one</li><li>Ordered item two</li></ol>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_paragraph_with_line_breaks(self):
        md = """
This is a paragraph
with line breaks
in the same block
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph with line breaks in the same block</p></div>",
        )

    def test_empty_markdown(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_only_whitespace(self):
        md = "   \n\n   \n\n   "
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_complex_inline_formatting(self):
        md = """
This paragraph has **bold text** and _italic text_ and `code text` and even [links](https://example.com) and ![images](https://example.com/image.png).
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This paragraph has <b>bold text</b> and <i>italic text</i> and <code>code text</code> and even <a href="https://example.com">links</a> and <img src="https://example.com/image.png" alt="images"></img>.</p></div>',
        )


if __name__ == "__main__":
    unittest.main()
