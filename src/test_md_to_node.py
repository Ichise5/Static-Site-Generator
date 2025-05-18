import unittest

from textnode import *
from md_to_node import *


class Test_md_to_node(unittest.TestCase):
    def test_strings_single_bold(self):
        initial_string = "This is text with **bold** statement."
        node = TextNode(initial_string,TextType.TEXT)
        new_nodes=split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = [text_node_to_html_node(node) for node in new_nodes]
        parent_node = ParentNode("p",new_nodes)

        self.assertEqual(
            parent_node.to_html(),
            "<p>This is text with <b>bold</b> statement.</p>",
        )

    def test_strings_double_bold(self):
        initial_string = "This is text with **bold** statement and another **bold** statement."
        node = TextNode(initial_string,TextType.TEXT)
        new_nodes=split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = [text_node_to_html_node(node) for node in new_nodes]
        parent_node = ParentNode("p",new_nodes)

        self.assertEqual(
            parent_node.to_html(),
            "<p>This is text with <b>bold</b> statement and another <b>bold</b> statement.</p>",
        )

        initial_string2 = "**bold** and **bold**"
        node = TextNode(initial_string2,TextType.TEXT)
        new_nodes=split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = [text_node_to_html_node(node) for node in new_nodes]
        parent_node = ParentNode("p",new_nodes)

        self.assertEqual(
            parent_node.to_html(),
            "<p><b>bold</b> and <b>bold</b></p>",
        )

    def test_strings_single_italic(self):
        initial_string = "This is text with *italic* statement."
        node = TextNode(initial_string,TextType.TEXT)
        new_nodes=split_nodes_delimiter([node], "*", TextType.ITALIC)
        new_nodes = [text_node_to_html_node(node) for node in new_nodes]
        parent_node = ParentNode("p",new_nodes)

        self.assertEqual(
            parent_node.to_html(),
            "<p>This is text with <i>italic</i> statement.</p>",
        )

    def test_strings_single_code(self):
        initial_string = "This is text with `code` statement."
        node = TextNode(initial_string,TextType.TEXT)
        new_nodes=split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = [text_node_to_html_node(node) for node in new_nodes]
        parent_node = ParentNode("p",new_nodes)

        self.assertEqual(
            parent_node.to_html(),
            "<p>This is text with <code>code</code> statement.</p>",
        )

    def test_strings_not_valid_md_syntax(self):
        initial_string1 = "This is text with invalid `code statement."
        node1 = TextNode(initial_string1,TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node1], "`", TextType.CODE)

        initial_string2 = "This is text with invalid *italic statement."
        node2 = TextNode(initial_string2,TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node2], "*", TextType.ITALIC)

        initial_string3 = "This is text with invalid **bold statement."
        node3 = TextNode(initial_string3,TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node3], "**", TextType.BOLD)

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

class TestImageAndLinkExtraction(unittest.TestCase):
    def test_no_image(self):
        text = "This is a text."
        result = extract_markdown_images(text)
        self.assertEqual([], result)

    def test_signle_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        result = extract_markdown_images(text)
        self.assertEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif")], result)

    def test_multiple_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        self.assertEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], result)


    def test_no_image(self):
        text = "This is a text."
        result = extract_markdown_images(text)
        self.assertEqual([], result)

    def test_signle_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        result = extract_markdown_links(text)
        self.assertEqual([("to boot dev", "https://www.boot.dev")], result)

    def test_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], result)

class TestImageAndLinkNodeExtraction(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                )
            ]
            
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                )
            ]
            
        )

    def test_split_links_not_images(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" and ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
                
            ]
            
        )
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

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

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

class TestTextToNodes(unittest.TestCase):
    def test_split_images(self):
        
        node_text="This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_nodes(node_text)
        self.assertListEqual(
            new_nodes,
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
            ]

            
        )
