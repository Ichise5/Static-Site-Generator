import unittest

from htmlnode import *


class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        # Test single property
        html_node1 = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(html_node1.props_to_html(), ' href="https://www.google.com"')

        # Test multiple properties
        html_node2 = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        self.assertEqual(html_node2.props_to_html(), ' href="https://google.com" target="_blank"')
        
        # Test with None props
        html_node3 = HTMLNode()
        self.assertEqual(html_node3.props_to_html(), '')


    def test_repr(self):
        # Test representation of node
        html_node = HTMLNode(tag="p", value="Hello", props={"class": "greeting"})
        expected = 'This is current tag: p\nThis is current value: Hello\nThis is current children: None\nThis is current props: {\'class\': \'greeting\'}'
        self.assertEqual(repr(html_node), expected)

    def test_LeafNode(self):
        # Test empty node
        leaf_node1 = LeafNode(None, None, None)
        with self.assertRaises(ValueError):
            leaf_node1.to_html()

        # Test node without value with tag
        leaf_node2 = LeafNode("p", None, None)
        with self.assertRaises(ValueError):
            leaf_node2.to_html()

        # Test values with or without tags
        leaf_node3 = LeafNode("p", "paragraph", None)
        self.assertEqual(leaf_node3.to_html(), "<p>paragraph</p>")

        leaf_node4 = LeafNode("a", "This is a link to Google", {"href":"https://google.com"})
        self.assertEqual(leaf_node4.to_html(), '<a href="https://google.com">This is a link to Google</a>')
        
        leaf_node5 = LeafNode(None, "This is plain text")
        self.assertEqual(leaf_node5.to_html(), "This is plain text")

    def test_to_html_props(self):
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

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )
    def test_parent_node(self):

        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            )
        self.assertEqual(node.to_html(),'<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

        node2 = ParentNode(
            "p",
            [node,
             node]
        )
        self.assertEqual(node2.to_html(),'<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>')

        # Not correctly specified nodes
        node3 = ParentNode(
            None,
            None
        )
        with self.assertRaises(ValueError):
            node3.to_html()

        node4 = ParentNode(
            None,
            [node2]
        )
        with self.assertRaises(ValueError):
            node4.to_html()

        node5 = ParentNode(
            "p",
            None
        )
        with self.assertRaises(ValueError):
            node5.to_html()



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

    def test_to_html_many_children(self):
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

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
if __name__ == "__main__":
    unittest.main()