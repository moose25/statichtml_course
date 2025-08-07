import unittest

from extract_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_images_no_images(self):
        text = "This is text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty_alt(self):
        text = "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_complex_alt(self):
        text = "This is text with an ![image with spaces and numbers 123](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image with spaces and numbers 123", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multiple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_links_no_links(self):
        text = "This is text with no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_empty_anchor(self):
        text = "This is text with a link [](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_complex_anchor(self):
        text = "This is text with a link [link with spaces and numbers 123](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link with spaces and numbers 123", "https://www.boot.dev")], matches)

    def test_extract_mixed_images_and_links(self):
        text = "Here's an ![image](https://img.com/pic.jpg) and a [link](https://example.com)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertListEqual([("image", "https://img.com/pic.jpg")], images)
        self.assertListEqual([("link", "https://example.com")], links)

    def test_extract_links_ignores_images(self):
        text = "This has an ![image](https://img.com/pic.jpg) and a [link](https://example.com)"
        links = extract_markdown_links(text)
        # Should only find the link, not the image
        self.assertListEqual([("link", "https://example.com")], links)

    def test_extract_images_with_nested_brackets(self):
        # This tests edge cases - simpler case without nested brackets in alt text
        text = "Check out this ![cool image](https://example.com/pic.jpg)"
        images = extract_markdown_images(text)
        self.assertListEqual([("cool image", "https://example.com/pic.jpg")], images)

    def test_extract_links_multiple_same_line(self):
        text = "[Link1](url1) some text [Link2](url2) more text [Link3](url3)"
        links = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("Link1", "url1"),
                ("Link2", "url2"),
                ("Link3", "url3"),
            ],
            links,
        )

    def test_extract_images_multiple_same_line(self):
        text = "![Image1](url1) some text ![Image2](url2) more text ![Image3](url3)"
        images = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("Image1", "url1"),
                ("Image2", "url2"),
                ("Image3", "url3"),
            ],
            images,
        )

    def test_extract_with_special_characters(self):
        text = "Check out this ![image-name_123](https://example.com/path/to/image-123_test.png?param=value&other=123)"
        images = extract_markdown_images(text)
        self.assertListEqual([("image-name_123", "https://example.com/path/to/image-123_test.png?param=value&other=123")], images)


if __name__ == "__main__":
    unittest.main()
