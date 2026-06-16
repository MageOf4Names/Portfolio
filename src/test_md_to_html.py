import unittest
from textnode import *
from htmlnode import *

class TestNodeTranslation(unittest.TestCase):
    def test_plain(self):
        node = TextNode("This is a plain node", TextType.PLAIN)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, None)
        self.assertEqual(html.value, "This is a plain node")
        self.assertEqual(html.to_html(), "This is a plain node")

    def test_bold(self):
        node = TextNode("This is a bolded node", TextType.BOLD)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "b")
        self.assertEqual(html.value, "This is a bolded node")
        self.assertEqual(html.to_html(), "<b>This is a bolded node</b>")

    def test_italic(self):
        node = TextNode("This node is italicized", TextType.ITALIC)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "i")
        self.assertEqual(html.value, "This node is italicized")
        self.assertEqual(html.to_html(), "<i>This node is italicized</i>")

    def test_code(self):
        node = TextNode("This node has code in it", TextType.CODE)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "code")
        self.assertEqual(html.value, "This node has code in it")
        self.assertEqual(html.to_html(), "<code>This node has code in it</code>")

    def test_link(self):
        node = TextNode("This node is a link", TextType.LINK, "http://www.test.io")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "a")
        self.assertEqual(html.value, "This node is a link")
        self.assertEqual(html.props_to_html(), 'href="http://www.test.io"')
        self.assertEqual(html.to_html(), '<a href="http://www.test.io">This node is a link</a>')

    def test_embed(self):
        node = TextNode("This is an image", TextType.EMBED, "./img/testImage")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "img")
        self.assertEqual(html.value, "")
        self.assertEqual(html.props_to_html(), 'src="./img/testImage" alt="This is an image"')
        self.assertEqual(html.to_html(), '<img src="./img/testImage" alt="This is an image"></img>')
