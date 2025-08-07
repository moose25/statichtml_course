import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_props_to_html_single_prop(self):
        node = HTMLNode("a", "Click me!", None, {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "A paragraph")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_props(self):
        node = HTMLNode("div", "Content", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            "img",
            None,
            None,
            {"src": "image.jpg", "alt": "Test image", "width": "300"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' src="image.jpg" alt="Test image" width="300"',
        )

    def test_to_html_raises_not_implemented_error(self):
        node = HTMLNode("div", "test")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_repr_with_children(self):
        child_node = HTMLNode("span", "child")
        parent_node = HTMLNode("div", None, [child_node])
        self.assertEqual(
            repr(parent_node),
            "HTMLNode(div, None, children: [HTMLNode(span, child, children: None, None)], None)",
        )


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just raw text")
        self.assertEqual(node.to_html(), "Just raw text")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "This is a heading")
        self.assertEqual(node.to_html(), "<h1>This is a heading</h1>")

    def test_leaf_to_html_img_with_props(self):
        node = LeafNode("img", "", {"src": "image.jpg", "alt": "Test image"})
        self.assertEqual(node.to_html(), '<img src="image.jpg" alt="Test image"></img>')

    def test_leaf_to_html_span_with_multiple_props(self):
        node = LeafNode("span", "Styled text", {"class": "highlight", "id": "main-text"})
        self.assertEqual(node.to_html(), '<span class="highlight" id="main-text">Styled text</span>')

    def test_leaf_to_html_no_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_empty_string_value(self):
        node = LeafNode("br", "")
        self.assertEqual(node.to_html(), "<br></br>")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        self.assertEqual(
            parent_node.to_html(), 
            '<div class="container" id="main"><span>child</span></div>'
        )

    def test_to_html_nested_parents(self):
        leaf1 = LeafNode("b", "Bold")
        leaf2 = LeafNode("i", "Italic")
        parent1 = ParentNode("span", [leaf1])
        parent2 = ParentNode("em", [leaf2])
        root = ParentNode("div", [parent1, parent2])
        self.assertEqual(
            root.to_html(),
            "<div><span><b>Bold</b></span><em><i>Italic</i></em></div>"
        )

    def test_to_html_mixed_children(self):
        leaf = LeafNode("b", "Bold")
        raw_text = LeafNode(None, " and ")
        nested_parent = ParentNode("span", [LeafNode("i", "italic")])
        parent = ParentNode("p", [leaf, raw_text, nested_parent])
        self.assertEqual(
            parent.to_html(),
            "<p><b>Bold</b> and <span><i>italic</i></span></p>"
        )

    def test_to_html_no_tag_raises_error(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "All parent nodes must have a tag")

    def test_to_html_no_children_raises_error(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "Parent node must have children")

    def test_to_html_empty_children_list(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")


if __name__ == "__main__":
    unittest.main()
