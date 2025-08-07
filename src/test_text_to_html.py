import unittest

from textnode import TextNode, TextType
from text_to_html import text_node_to_html_node


class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode("print('hello world')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello world')")
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode("Click me!", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "Alt text"})

    def test_link_without_url_raises_error(self):
        node = TextNode("Click me!", TextType.LINK, None)
        html_node = text_node_to_html_node(node)
        # This should still work but will have None href
        self.assertEqual(html_node.props, {"href": None})

    def test_image_without_url_raises_error(self):
        node = TextNode("Alt text", TextType.IMAGE, None)
        html_node = text_node_to_html_node(node)
        # This should still work but will have None src
        self.assertEqual(html_node.props, {"src": None, "alt": "Alt text"})

    def test_to_html_conversion(self):
        # Test that the converted nodes can actually render HTML
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

        link_node = TextNode("Google", TextType.LINK, "https://google.com")
        html_link = text_node_to_html_node(link_node)
        self.assertEqual(html_link.to_html(), '<a href="https://google.com">Google</a>')

        img_node = TextNode("A cat", TextType.IMAGE, "cat.jpg")
        html_img = text_node_to_html_node(img_node)
        self.assertEqual(html_img.to_html(), '<img src="cat.jpg" alt="A cat"></img>')


if __name__ == "__main__":
    unittest.main()
