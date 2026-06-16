import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_repr_none(self):
        test = HTMLNode().props_to_html()
        self.assertEqual(test, "")

    def test_repr_empty(self):
        test = HTMLNode(props={}).props_to_html()
        self.assertEqual(test, "")

    def test_repr_true(self):
        test = HTMLNode(props={"href": "http://www.test.io"}).props_to_html()
        self.assertEqual(test, 'href="http://www.test.io"')

    def test_repr_multi(self):
        test = HTMLNode(props={"href": "http://www.test.io", "target": "_blank"}).props_to_html()
        self.assertEqual(test, 'href="http://www.test.io" target="_blank"')


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", {"href": "http://www.test.io"})
        self.assertEqual(
            node.to_html(), '<a href="http://www.test.io">Hello, world!</a>'
        )

    def test_leaf_to_html_empty(self):
        node = LeafNode(None, "This is an empty tag")
        self.assertEqual(
            node.to_html(), 'This is an empty tag'
        )


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("span", "child1")
        child2 = LeafNode("a", "child2", {"href": "http://www.test.io"})
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent_node.to_html(), '<div><span>child1</span><a href="http://www.test.io">child2</a></div>'
        )

    def test_to_html_with_children_props(self):
        child_node = LeafNode("a", "child", {"href": "http://www.test.io"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><a href="http://www.test.io">child</a></div>')

    def test_to_html_with_empty_children(self):
        child_node = LeafNode(None, "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div>child</div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
