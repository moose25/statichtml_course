import unittest

from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        markdown = "# Hello"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello")

    def test_extract_title_with_whitespace(self):
        markdown = "#   Title with spaces   "
        result = extract_title(markdown)
        self.assertEqual(result, "Title with spaces")

    def test_extract_title_multiline(self):
        markdown = """Some intro text

# Main Title

Some content here"""
        result = extract_title(markdown)
        self.assertEqual(result, "Main Title")

    def test_extract_title_with_other_headers(self):
        markdown = """## This is h2

# This is the h1 title

### This is h3"""
        result = extract_title(markdown)
        self.assertEqual(result, "This is the h1 title")

    def test_extract_title_complex(self):
        markdown = """# Tolkien Fan Club

This is some content

## Subheading

More content here"""
        result = extract_title(markdown)
        self.assertEqual(result, "Tolkien Fan Club")

    def test_extract_title_no_space_after_hash(self):
        # This should not be considered an h1 (needs space after #)
        markdown = """#NoSpace

Some content"""
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_no_h1_header(self):
        markdown = """## This is h2

### This is h3

Some content without h1"""
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_empty_h1(self):
        # h1 with just # and space but no content
        markdown = "# "
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_empty_markdown(self):
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_only_higher_level_headers(self):
        markdown = """## Second level

### Third level

#### Fourth level"""
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_multiple_h1_returns_first(self):
        markdown = """# First Title

Some content

# Second Title

More content"""
        result = extract_title(markdown)
        self.assertEqual(result, "First Title")

    def test_extract_title_with_inline_formatting(self):
        markdown = "# This is **bold** and _italic_ title"
        result = extract_title(markdown)
        self.assertEqual(result, "This is **bold** and _italic_ title")


if __name__ == "__main__":
    unittest.main()
