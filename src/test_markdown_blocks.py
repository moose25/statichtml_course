import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "This is just a single paragraph with no double newlines."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is just a single paragraph with no double newlines."])

    def test_markdown_to_blocks_multiple_newlines(self):
        md = """First block


Second block



Third block"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block", "Third block"])

    def test_markdown_to_blocks_with_whitespace(self):
        md = """   
        
Block with leading whitespace

    Block with trailing whitespace    

        Block with both    
        
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Block with leading whitespace",
                "Block with trailing whitespace",
                "Block with both",
            ],
        )

    def test_markdown_to_blocks_headings_and_paragraphs(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

## This is a subheading

Another paragraph here."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "## This is a subheading",
                "Another paragraph here.",
            ],
        )

    def test_markdown_to_blocks_lists(self):
        md = """- This is the first list item in a list block
- This is a list item
- This is another list item

1. This is an ordered list
2. With numbered items
3. Like this

* Alternative bullet style
* Also works"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
                "1. This is an ordered list\n2. With numbered items\n3. Like this",
                "* Alternative bullet style\n* Also works",
            ],
        )

    def test_markdown_to_blocks_code_blocks(self):
        md = """Here's some code:

```python
def hello():
    print("Hello, world!")
```

And here's more text after the code block."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Here's some code:",
                "```python\ndef hello():\n    print(\"Hello, world!\")\n```",
                "And here's more text after the code block.",
            ],
        )

    def test_markdown_to_blocks_empty_input(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_whitespace_only(self):
        md = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_mixed_content(self):
        md = """# Main Title

This is the introduction paragraph with some **bold text**.

## Features

- Feature one
- Feature two
- Feature three

### Code Example

```javascript
console.log("Hello World");
```

That's all for now!"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Main Title",
                "This is the introduction paragraph with some **bold text**.",
                "## Features",
                "- Feature one\n- Feature two\n- Feature three",
                "### Code Example",
                "```javascript\nconsole.log(\"Hello World\");\n```",
                "That's all for now!",
            ],
        )

    def test_markdown_to_blocks_preserve_single_newlines(self):
        md = """This is line one
This is line two
This is line three

This is a new paragraph
With multiple lines
In the same block"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is line one\nThis is line two\nThis is line three",
                "This is a new paragraph\nWith multiple lines\nIn the same block",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading_h1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_h2(self):
        block = "## This is an h2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_h6(self):
        block = "###### This is an h6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_with_space_required(self):
        # Must have space after #
        block = "#No space after hash"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_too_many_hashes(self):
        # More than 6 # characters should be paragraph
        block = "####### Too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_block(self):
        block = "```python\ndef hello():\n    print('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_block_simple(self):
        block = "```\nsome code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_block_single_line(self):
        block = "```code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_not_code_block_missing_end(self):
        block = "```python\ndef hello():\n    print('Hello')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_not_code_block_missing_start(self):
        block = "def hello():\n    print('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote_single_line(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_quote_multiline(self):
        block = "> This is a quote\n> with multiple lines\n> of text"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_quote_mixed_not_quote(self):
        # All lines must start with >
        block = "> This is a quote\nThis line doesn't start with >\n> Back to quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list_single_item(self):
        block = "- Item one"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_multiple_items(self):
        block = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_missing_space(self):
        # Must have space after -
        block = "-No space after dash\n- Item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list_mixed_not_list(self):
        # All lines must start with "- "
        block = "- Item one\nNot a list item\n- Item three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_single_item(self):
        block = "1. First item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_multiple_items(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_long(self):
        block = "1. First\n2. Second\n3. Third\n4. Fourth\n5. Fifth"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_must_start_with_1(self):
        # Must start with 1
        block = "2. Second item\n3. Third item\n4. Fourth item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_must_increment_by_1(self):
        # Must increment by exactly 1
        block = "1. First item\n3. Third item\n4. Fourth item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_missing_space(self):
        # Must have space after period
        block = "1.No space after period\n2. Second item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_mixed_not_list(self):
        # All lines must match pattern
        block = "1. First item\nNot a list item\n2. Should be second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_simple(self):
        block = "This is just a regular paragraph with some text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_multiline(self):
        block = "This is a paragraph\nwith multiple lines\nof regular text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_with_formatting(self):
        block = "This paragraph has **bold** and *italic* text and `code`."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_numbers_without_list_format(self):
        block = "1 This starts with a number but isn't a list\n2 Same here"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
