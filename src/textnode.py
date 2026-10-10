from enum import Enum
from htmlnode import *

class TextType(Enum):
    PLAIN       = 1
    BOLD        = 2
    ITALIC      = 3
    CODE        = 4
    LINK        = 5
    EMBED       = 6
    LIST_ITEM   = 7


class BlockType(Enum):
    HEADING1    = 1
    HEADING2    = 2
    HEADING3    = 3
    HEADING4    = 4
    HEADING5    = 5
    HEADING6    = 6
    PARAGRAPH   = 7
    CODE        = 8
    QUOTE       = 9
    UNORDERED   = 10
    ORDERED     = 11
    PRE         = 12
    DIV         = 13

type_to_tag = {
    TextType.PLAIN:     None,
    TextType.BOLD:      "b",
    TextType.ITALIC:    "i",
    TextType.CODE:      "code",
    TextType.LINK:      "a",
    TextType.EMBED:     "img",
    TextType.LIST_ITEM: "li",
    BlockType.HEADING1: "h1",
    BlockType.HEADING2: "h2",
    BlockType.HEADING3: "h3",
    BlockType.HEADING4: "h4",
    BlockType.HEADING5: "h5",
    BlockType.HEADING6: "h6",
    BlockType.PARAGRAPH:"p",
    BlockType.CODE:     "code",
    BlockType.QUOTE:    "blockquote",
    BlockType.UNORDERED:"ul",
    BlockType.ORDERED:  "ol",
    BlockType.PRE:      "pre",
    BlockType.DIV:      "div"
}


class TextNode():
    def __init__(self, text: str, type: TextType, url: str | None = None):
        self.text = text
        self.text_type = type
        self.url = url

    # Overload how the equality operand works on this class
    def __eq__(self, other):
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)

    # Change how the object represents itself as a string
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


class BlockNode(TextNode):
    def __init__(self, text: str | None, type: BlockType, url: str | None = None):
        self.text = text
        self.block_type = type
        self.url = url


def text_node_to_html_node(node: TextNode, constructor = LeafNode) -> HTMLNode:
    match node.text_type:
        case TextType.LINK:
            return constructor("a", node.text, {"href": node.url})
        case TextType.EMBED:
            return constructor("img", "", {"src": node.url, "alt": node.text})
        case _:
            if node.text_type in type_to_tag:
                return constructor(type_to_tag[node.text_type], node.text)
            else:
                raise Exception(f"Unexpected Text Type: {node.text_type.value}")
