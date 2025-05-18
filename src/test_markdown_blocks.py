import unittest
from markdown_blocks import *


class TestMarkdownToHTML(unittest.TestCase):
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

    def test_markdown_to_blocks_newlines(self):
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



        
    def test_markdown_to_blocks_with_header(self):
            md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "# This is a heading",
                    "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                    "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
                ],
            )


class TestMarkdownBlocks(unittest.TestCase):
    def test_block_to_heading1(self):
         block = "# Heading 1"
         self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
         )
    def test_block_to_heading2(self):
         block = "## Heading 2"
         self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
         )
    def test_block_to_heading3(self):
         block = "### Heading 3"
         self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
         )
    def test_block_to_heading4(self):
         block = "#### Heading 4"
         self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
         )
    def test_block_to_heading5(self):
         block = "##### Heading 5"
         self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
         )
    def test_block_to_heading6(self):
         block = "###### Heading 6"
         self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
         )
    def test_block_to_code(self):
         block = "```This is a code block```"
         self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE
         )
    def test_block_to_code_multiline(self):
         block = "```This is a code block\nIt has multiple lines\nbut still is valid```"
         self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE
         )
    def test_block_to_code_multiline_wrong(self):
         block = "```This is a code block\nIt has multiple lines```\nbut still is no longer valid"
         self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
         )
    def test_block_to_quote(self):
         block = ">This is a quote block"
         self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
         )
    def test_block_to_quote_multiline(self):
         block = """>This is a quote block
>It has multiple lines
>but still is valid"""
         self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
         )
    def test_block_to_quote_multiline_wrong(self):
         block = """>This is a quote block
>It has multiple lines
but still is no longer valid"""
         self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
         )

    def test_block_to_unordered(self):
         block = "- This is a unordered list block"
         self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDEREDLIST
         )
    def test_block_to_unordered_multiline(self):
         block = """- This is a unordered list block
- It has multiple lines
- but still is valid"""
         self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDEREDLIST
         )
    def test_block_to_unordered_multiline_wrong(self):
         block = """- This is a unordered list block
- It has multiple lines
but still is no longer valid"""
         self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
         )    


    def test_block_to_ordered(self):
         block = "1. This is a ordered list block"
         self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDEREDLIST
         )
    def test_block_to_ordered_multiline(self):
         block = """1. This is a ordered list block
2. It has multiple lines
3. but still is valid"""
         self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDEREDLIST
         )
    def test_block_to_ordered_multiline_wrong(self):
         block = """1. This is a ordered list block
2. It has multiple lines
3.but still is no longer valid"""
         self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
         )     

    def test_block_to_ordered_multiline_wrong2(self):
         block = """1. This is a ordered list block
2. It has multiple lines
but still is no longer valid"""
         self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
         )   

    def test_block_to_ordered_multiline_wron3(self):
         block = """1. This is a ordered list block
2. It has multiple lines
2. but still is no longer valid"""
         self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
         )   

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDEREDLIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDEREDLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownBlocksToHTML(unittest.TestCase):
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
      
   def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

   def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

   def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

   def test_code(self):
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


if __name__ == "__main__":
    unittest.main()
