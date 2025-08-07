import unittest

from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_delim_bold_double(self):
        node = TextNode("This is text with a **bolded** word and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
        )

    def test_delim_bold_multiword(self):
        node = TextNode("This is text with a **bolded word** and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_delim_no_delimiter(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is just plain text", TextType.TEXT)])

    def test_delim_only_delimiter(self):
        node = TextNode("**bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("bold", TextType.BOLD)])

    def test_delim_multiple_nodes(self):
        node1 = TextNode("This has **bold** text", TextType.TEXT)
        node2 = TextNode("This is already bold", TextType.BOLD)
        node3 = TextNode("This has more **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
                TextNode("This is already bold", TextType.BOLD),
                TextNode("This has more ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_delim_at_beginning(self):
        node = TextNode("**bold** at the beginning", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" at the beginning", TextType.TEXT),
            ],
        )

    def test_delim_at_end(self):
        node = TextNode("Text ending with **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text ending with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
        )

    def test_delim_consecutive(self):
        node = TextNode("**first****second**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("first", TextType.BOLD),
                TextNode("second", TextType.BOLD),
            ],
        )

    def test_delim_unmatched_raises_error(self):
        node = TextNode("This has **unmatched bold", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(context.exception), "Invalid markdown, formatted section not closed")

    def test_delim_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [])

    def test_delim_multiple_different_types(self):
        # Test that non-TEXT nodes are preserved
        nodes = [
            TextNode("Text with **bold**", TextType.TEXT),
            TextNode("Already italic", TextType.ITALIC),
            TextNode("More **bold** text", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("Already italic", TextType.ITALIC),
                TextNode("More ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_single(self):
        node = TextNode("Check out this ![cool image](https://example.com/pic.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Check out this ", TextType.TEXT),
                TextNode("cool image", TextType.IMAGE, "https://example.com/pic.jpg"),
            ],
            new_nodes,
        )

    def test_split_images_at_beginning(self):
        node = TextNode("![first image](https://example.com/pic.jpg) followed by text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first image", TextType.IMAGE, "https://example.com/pic.jpg"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_at_end(self):
        node = TextNode("Text before ![last image](https://example.com/pic.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("last image", TextType.IMAGE, "https://example.com/pic.jpg"),
            ],
            new_nodes,
        )

    def test_split_images_only_image(self):
        node = TextNode("![only image](https://example.com/pic.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("only image", TextType.IMAGE, "https://example.com/pic.jpg"),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("This is just plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_empty_alt(self):
        node = TextNode("Image with ![](https://example.com/pic.jpg) empty alt", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image with ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://example.com/pic.jpg"),
                TextNode(" empty alt", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("First ![image1](url1) here", TextType.TEXT),
            TextNode("Already an image", TextType.IMAGE, "existing.jpg"),
            TextNode("Second ![image2](url2) there", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "url1"),
                TextNode(" here", TextType.TEXT),
                TextNode("Already an image", TextType.IMAGE, "existing.jpg"),
                TextNode("Second ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "url2"),
                TextNode(" there", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_consecutive(self):
        node = TextNode("![first](url1)![second](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "url1"),
                TextNode("second", TextType.IMAGE, "url2"),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_links_single(self):
        node = TextNode("Check out this [cool link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out this ", TextType.TEXT),
                TextNode("cool link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_links_at_beginning(self):
        node = TextNode("[first link](https://example.com) followed by text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first link", TextType.LINK, "https://example.com"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_at_end(self):
        node = TextNode("Text before [last link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("last link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_links_only_link(self):
        node = TextNode("[only link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("only link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("This is just plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_empty_anchor(self):
        node = TextNode("Link with [](https://example.com) empty anchor", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link with ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://example.com"),
                TextNode(" empty anchor", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode("First [link1](url1) here", TextType.TEXT),
            TextNode("Already a link", TextType.LINK, "existing.com"),
            TextNode("Second [link2](url2) there", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "url1"),
                TextNode(" here", TextType.TEXT),
                TextNode("Already a link", TextType.LINK, "existing.com"),
                TextNode("Second ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url2"),
                TextNode(" there", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_consecutive(self):
        node = TextNode("[first](url1)[second](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "url1"),
                TextNode("second", TextType.LINK, "url2"),
            ],
            new_nodes,
        )

    def test_split_links_ignores_images(self):
        node = TextNode("This has an ![image](img.jpg) and a [link](example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        # Should only split the link, not the image
        self.assertListEqual(
            [
                TextNode("This has an ![image](img.jpg) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "example.com"),
            ],
            new_nodes,
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_bold_only(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_multiple_same_type(self):
        text = "Here is **bold1** and **bold2** text"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("bold1", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold2", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_all_types(self):
        text = "**bold** *italic* `code` ![img](url) [link](url)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url"),
                TextNode(" ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
            ],
            nodes,
        )

    def test_text_to_textnodes_plain_text(self):
        text = "This is just plain text with no formatting"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is just plain text with no formatting", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [],
            nodes,
        )

    def test_text_to_textnodes_nested_formatting_order(self):
        # Test that the order of processing matters
        text = "Text with **bold and *italic* inside**"
        nodes = text_to_textnodes(text)
        # Bold should be processed first, so the italic inside becomes part of the bold text
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bold and *italic* inside", TextType.BOLD),
            ],
            nodes,
        )

    def test_text_to_textnodes_complex_mix(self):
        text = "Start **bold** then *italic* then `code` ![image](img.jpg) [link](url) end"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" then ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" then ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "img.jpg"),
                TextNode(" ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(" end", TextType.TEXT),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
