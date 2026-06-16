import unittest
from parser import *


class TestSplitDelimeter(unittest.TestCase):
    def test_err(self):
        nested = TextNode(
            "This is a broken string with only **one set of delimiters.", TextType.PLAIN
        )
        self.assertRaises(Exception, parse_nodes, [nested], "**", TextType.BOLD)

    def test_bold(self):
        nested = TextNode("This is a plain string with **bolded text** in the middle.", TextType.PLAIN)
        test_base = parse_nodes([nested], '**', TextType.BOLD)
        expected = []
        expected.append(TextNode("This is a plain string with ", TextType.PLAIN))
        expected.append(TextNode("bolded text", TextType.BOLD))
        expected.append(TextNode(" in the middle.", TextType.PLAIN))
        self.assertEqual(test_base, expected)

    def test_italic(self):
        nested = TextNode(
            "This is a plain string with _italic text_ in the middle.", TextType.PLAIN
        )
        test_base = parse_nodes([nested], "_", TextType.ITALIC)
        expected = []
        expected.append(TextNode("This is a plain string with ", TextType.PLAIN))
        expected.append(TextNode("italic text", TextType.ITALIC))
        expected.append(TextNode(" in the middle.", TextType.PLAIN))
        self.assertEqual(test_base, expected)

    def test_code(self):
        nested = TextNode(
            "This is a plain string with `a code block` in the middle.", TextType.PLAIN
        )
        test_base = parse_nodes([nested], "`", TextType.CODE)
        expected = []
        expected.append(TextNode("This is a plain string with ", TextType.PLAIN))
        expected.append(TextNode("a code block", TextType.CODE))
        expected.append(TextNode(" in the middle.", TextType.PLAIN))
        self.assertEqual(test_base, expected)

    def test_no_starting_text(self):
        nested = TextNode(
            "_This sentence starts italicized and_ finishes plain.", TextType.PLAIN
        )
        test_base = parse_nodes([nested], "_", TextType.ITALIC)
        expected = []
        expected.append(TextNode("This sentence starts italicized and", TextType.ITALIC))
        expected.append(TextNode(" finishes plain.", TextType.PLAIN))
        self.assertEqual(test_base, expected)

    def test_no_termination(self):
        nested = TextNode(
            "This is a plain string with `a code block at the end`", TextType.PLAIN
        )
        test_base = parse_nodes([nested], "`", TextType.CODE)
        expected = []
        expected.append(TextNode("This is a plain string with ", TextType.PLAIN))
        expected.append(TextNode("a code block at the end", TextType.CODE))
        self.assertEqual(test_base, expected)

    def test_multiple(self):
        nested = TextNode(
            "This is a **plain text** string with **multiple** sequenced **bold texts** in it.", TextType.PLAIN
        )
        test_base = parse_nodes([nested], "**", TextType.BOLD)
        expected = []
        expected.append(TextNode("This is a ", TextType.PLAIN))
        expected.append(TextNode("plain text", TextType.BOLD))
        expected.append(TextNode(" string with ", TextType.PLAIN))
        expected.append(TextNode("multiple", TextType.BOLD))
        expected.append(TextNode(" sequenced ", TextType.PLAIN))
        expected.append(TextNode("bold texts", TextType.BOLD))
        expected.append(TextNode(" in it.", TextType.PLAIN))
        self.assertEqual(test_base, expected)


class TestExtractions(unittest.TestCase):
    def test_images(self):
        test_case = extract_image("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], test_case)

    def test_images(self):
        test_case = extract_link("This is text with a [link](https://test.org)")
        self.assertListEqual([("link", "https://test.org")], test_case)

    def test_multiple(self):
        test_case = extract_link("This is text with [multiple](https://test.org) [links](https://test.io)")
        self.assertListEqual([("multiple", "https://test.org"), ("links", "https://test.io")], test_case)


class TestURLSplits(unittest.TestCase):
    def test_pretext_image(self):
        nodes = [TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.PLAIN)]
        test_case = split_url_nodes(nodes, TextType.EMBED)
        expected = []
        expected.append(TextNode("This is text with an ", TextType.PLAIN))
        expected.append(TextNode("image", TextType.EMBED, "https://i.imgur.com/zjjcJKZ.png"))
        self.assertListEqual(test_case, expected)

    def test_pretext_link(self):
        nodes = [TextNode("This is text with a [link](https://www.test.io)", TextType.PLAIN)]
        test_case = split_url_nodes(nodes, TextType.LINK)
        expected = []
        expected.append(TextNode("This is text with a ", TextType.PLAIN))
        expected.append(TextNode("link", TextType.LINK, "https://www.test.io"))
        self.assertListEqual(test_case, expected)

    def test_posttext_image(self):
        nodes = [TextNode("![image](https://i.imgur.com/zjjcJKZ.png) followed by text.", TextType.PLAIN)]
        test_case = split_url_nodes(nodes, TextType.EMBED)
        expected = []
        expected.append(TextNode("image", TextType.EMBED, "https://i.imgur.com/zjjcJKZ.png"))
        expected.append(TextNode(" followed by text.", TextType.PLAIN))
        self.assertListEqual(test_case, expected)

    def test_posttext_link(self):
        nodes = [TextNode("[link](https://www.test.io) followed by text.", TextType.PLAIN)]
        test_case = split_url_nodes(nodes, TextType.LINK)
        expected = []
        expected.append(TextNode("link", TextType.LINK, "https://www.test.io"))
        expected.append(TextNode(" followed by text.", TextType.PLAIN))
        self.assertListEqual(test_case, expected)

    def test_mixed_text_image(self):
        nodes = [TextNode("This is an ![image](https://i.imgur.com/zjjcJKZ.png) followed by text.", TextType.PLAIN)]
        test_case = split_url_nodes(nodes, TextType.EMBED)
        expected = []
        expected.append(TextNode("This is an ", TextType.PLAIN))
        expected.append(TextNode("image", TextType.EMBED, "https://i.imgur.com/zjjcJKZ.png"))
        expected.append(TextNode(" followed by text.", TextType.PLAIN))
        self.assertListEqual(test_case, expected)

    def test_mixed_text_link(self):
        nodes = [TextNode("This is a [link](https://www.test.io) followed by text.", TextType.PLAIN)]
        test_case = split_url_nodes(nodes, TextType.LINK)
        expected = []
        expected.append(TextNode("This is a ", TextType.PLAIN))
        expected.append(TextNode("link", TextType.LINK, "https://www.test.io"))
        expected.append(TextNode(" followed by text.", TextType.PLAIN))
        self.assertListEqual(test_case, expected)

    def test_multi_link(self):
        nodes = [TextNode("This is a [link](https://www.test.io) followed by [another link](https://www.another-test.io) followed by text.", TextType.PLAIN)]
        test_case = split_url_nodes(nodes, TextType.LINK)
        expected = []
        expected.append(TextNode("This is a ", TextType.PLAIN))
        expected.append(TextNode("link", TextType.LINK, "https://www.test.io"))
        expected.append(TextNode(" followed by ", TextType.PLAIN))
        expected.append(TextNode("another link", TextType.LINK, "https://www.another-test.io"))
        expected.append(TextNode(" followed by text.", TextType.PLAIN))
        self.assertListEqual(test_case, expected)

    def test_multi_image(self):
        nodes = [TextNode("This is a ![image](https://i.imgur.com/zjjcJKZ.png) followed by ![another image](https://i.imgur.com/3elNhQu.png) followed by text.", TextType.PLAIN)]
        test_case = split_url_nodes(nodes, TextType.EMBED)
        expected = []
        expected.append(TextNode("This is a ", TextType.PLAIN))
        expected.append(TextNode("image", TextType.EMBED, "https://i.imgur.com/zjjcJKZ.png"))
        expected.append(TextNode(" followed by ", TextType.PLAIN))
        expected.append(TextNode("another image", TextType.EMBED, "https://i.imgur.com/3elNhQu.png"))
        expected.append(TextNode(" followed by text.", TextType.PLAIN))
        self.assertListEqual(test_case, expected)

    def test_sequential_link(self):
        nodes = [TextNode("[link](https://www.test.io)[another link](https://www.another-test.io)", TextType.PLAIN)]
        test_case = split_url_nodes(nodes, TextType.LINK)
        expected = []
        expected.append(TextNode("link", TextType.LINK, "https://www.test.io"))
        expected.append(TextNode("another link", TextType.LINK, "https://www.another-test.io"))
        self.assertListEqual(test_case, expected)

    def test_sequential_image(self):
        nodes = [TextNode("![image](https://i.imgur.com/zjjcJKZ.png)![another image](https://i.imgur.com/3elNhQu.png)", TextType.PLAIN)]
        test_case = split_url_nodes(nodes, TextType.EMBED)
        expected = []
        expected.append(TextNode("image", TextType.EMBED, "https://i.imgur.com/zjjcJKZ.png"))
        expected.append(TextNode("another image", TextType.EMBED, "https://i.imgur.com/3elNhQu.png"))
        self.assertListEqual(test_case, expected)


class TestTextParsing(unittest.TestCase):
    def test_bold(self):
        text = "This string has **bolded text** inside of it."
        test_case = parse_text(text)
        expected = []
        expected.append(TextNode("This string has ", TextType.PLAIN))
        expected.append(TextNode("bolded text", TextType.BOLD))
        expected.append(TextNode(" inside of it.", TextType.PLAIN))
        self.assertListEqual(test_case, expected)

    def test_italic(self):
        text = "This test string has _emphasis._"
        test_case = parse_text(text)
        expected = []
        expected.append(TextNode("This test string has ", TextType.PLAIN))
        expected.append(TextNode("emphasis.", TextType.ITALIC))
        self.assertListEqual(test_case, expected)

    def test_code(self):
        text = "`This test string is entirely within a code block.`"
        test_case = parse_text(text)
        expected = []
        expected.append(TextNode("This test string is entirely within a code block.", TextType.CODE))
        self.assertListEqual(test_case, expected)

    def test_mixed(self):
        text = "This one is **a little wacky** having _so many_ different kinds `of blocks` inside of it."
        test_case = parse_text(text)
        expected = []
        expected.append(TextNode("This one is ", TextType.PLAIN))
        expected.append(TextNode("a little wacky", TextType.BOLD))
        expected.append(TextNode(" having ", TextType.PLAIN))
        expected.append(TextNode("so many", TextType.ITALIC))
        expected.append(TextNode(" different kinds ", TextType.PLAIN))
        expected.append(TextNode("of blocks", TextType.CODE))
        expected.append(TextNode(" inside of it.", TextType.PLAIN))
        self.assertListEqual(test_case, expected)

    def test_mixed_links(self):
        text = "![image](https://i.imgur.com/zjjcJKZ.png)[link](https://www.test.io)"
        test_case = parse_text(text)
        expected = []
        expected.append(TextNode("image", TextType.EMBED, "https://i.imgur.com/zjjcJKZ.png"))
        expected.append(TextNode("link", TextType.LINK, "https://www.test.io"))
        self.assertListEqual(test_case, expected)

    def test_mixed_links_alt_order(self):
        text = "[link](https://www.test.io)![image](https://i.imgur.com/zjjcJKZ.png)"
        test_case = parse_text(text)
        expected = []
        expected.append(TextNode("link", TextType.LINK, "https://www.test.io"))
        expected.append(TextNode("image", TextType.EMBED, "https://i.imgur.com/zjjcJKZ.png"))
        self.assertListEqual(test_case, expected)

    def test_mixed_with_links(self):
        text = "This one is _a little wacky_ having **so many** different kinds `of blocks` inside of it. It's even got [links](https://www.test.io) and ![images](https://i.imgur.com/zjjcJKZ.png)"
        test_case = parse_text(text)
        expected = []
        expected.append(TextNode("This one is ", TextType.PLAIN))
        expected.append(TextNode("a little wacky", TextType.ITALIC))
        expected.append(TextNode(" having ", TextType.PLAIN))
        expected.append(TextNode("so many", TextType.BOLD))
        expected.append(TextNode(" different kinds ", TextType.PLAIN))
        expected.append(TextNode("of blocks", TextType.CODE))
        expected.append(TextNode(" inside of it. It's even got ", TextType.PLAIN))
        expected.append(TextNode("links", TextType.LINK, "https://www.test.io"))
        expected.append(TextNode(" and ", TextType.PLAIN))
        expected.append(TextNode("images", TextType.EMBED, "https://i.imgur.com/zjjcJKZ.png"))
        self.assertListEqual(test_case, expected)


class TestBlockParser(unittest.TestCase):
    def test_block_splitting(self):
        block_text = """
This is a block of text that needs **breaking up**

There are multiple, _isolated_ blocks of text here
And they're all going to need splitting before we can process them.

- First split by double newline
- Then remove excessive whitespace
"""
        blocks = markdown_to_blocks(block_text)
        self.assertListEqual(
            blocks,
            [
                "This is a block of text that needs **breaking up**",
                "There are multiple, _isolated_ blocks of text here\nAnd they're all going to need splitting before we can process them.",
                "- First split by double newline\n- Then remove excessive whitespace",
            ],
        )

    def test_block_extra_lines(self):
        block_text = """
This is a block of text that needs **breaking up**



There are multiple, _isolated_ blocks of text here
And they're all going to need splitting before we can process them.






- First split by double newline
- Then remove excessive whitespace
"""
        blocks = markdown_to_blocks(block_text)
        self.assertListEqual(
            blocks,
            [
                "This is a block of text that needs **breaking up**",
                "There are multiple, _isolated_ blocks of text here\nAnd they're all going to need splitting before we can process them.",
                "- First split by double newline\n- Then remove excessive whitespace",
            ],
        )

    def test_block_whitespace(self):
        block_text = """
        This is a block of text that needs **breaking up**

There are multiple, _isolated_ blocks of text here
And they're all going to need splitting before we can process them.       

- First split by double newline
- Then remove excessive whitespace          

"""
        blocks = markdown_to_blocks(block_text)
        self.assertListEqual(
            blocks,
            [
                "This is a block of text that needs **breaking up**",
                "There are multiple, _isolated_ blocks of text here\nAnd they're all going to need splitting before we can process them.",
                "- First split by double newline\n- Then remove excessive whitespace",
            ],
        )


class TestBlockTyping(unittest.TestCase):
    def test_heading(self):
        block = "# Heading"
        tests = [
            BlockType.HEADING1,
            BlockType.HEADING2,
            BlockType.HEADING3,
            BlockType.HEADING4,
            BlockType.HEADING5,
            BlockType.HEADING6,
            BlockType.PARAGRAPH,
        ]
        for i in range(6):
            self.assertEqual(tests[i], assign_block_type(block))
            block = "#" + block

    def test_code(self):
        blocks = [
            "```\nGonna write some code here\nand it'll look real good```",
            "```\nGonna write some code here\n and it'll look real good```",
            "```\nGonna write some code here\nand it'll look real good\n```",
            "```\nGonna write some code here and it'll look real good```"
        ]
        for b in blocks:
            self.assertEqual(BlockType.CODE, assign_block_type(b))

    def test_quotes(self):
        block = """
> This is a quote block
>it doesn't always need a space
> But the line does always have to start with '>'"""
        self.assertEqual(BlockType.QUOTE, assign_block_type(block))

    def test_ordered(self):
        block = """
1. This is an ordered list block
1. it does always need a space
1. and the line does always have to start with '.'"""
        self.assertEqual(BlockType.ORDERED, assign_block_type(block))

    def test_unordered(self):
        block = """
- This is an unordered list block
- it does always need a space
- and the line does always have to start with '-'"""
        self.assertEqual(BlockType.UNORDERED, assign_block_type(block))

    def test_mixed_malformed(self):
        block = """
This block is a mix of a bunch of things
> There's a quote
1. and ordered list items
- and unordered list items
>it's a mess"""
        self.assertEqual(BlockType.PARAGRAPH, assign_block_type(block))


class TestParser(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html(md)
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

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
> This is a quote block
>it doesn't _always_ need a space
> But the line does always have to start with '>'
"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote block\nit doesn't <i>always</i> need a space\nBut the line does always have to start with '>'</blockquote></div>",
        )

    def test_orderedblock(self):
        md = """
1. This is an ordered list block
2. it does always need a space
3. and the line does always have to start with '.'
"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an ordered list block</li><li>it does always need a space</li><li>and the line does always have to start with '.'</li></ol></div>",
        )

    def test_unorderedblock(self):
        md = """
- This is an unordered list block
- it does **always** need a space
- and the line does always have to start with '-'
"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is an unordered list block</li><li>it does <b>always</b> need a space</li><li>and the line does always have to start with '-'</li></ul></div>",
        )

    def test_multiblock(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


class TestHeader(unittest.TestCase):
    def test_header(self):
        self.assertEqual(extract_title("# Header"), "Header")

    def test_failed_header(self):
        self.assertRaises(Exception, extract_title, "Header")

    def test_failed_header2(self):
        self.assertRaises(Exception, extract_title, "## Header")