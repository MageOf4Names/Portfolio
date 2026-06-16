import re
from textnode import *
from htmlnode import *


def extract_image(text: str):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_link(text: str):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def extract_title(md: str):
    header = md.split("\n")[0]
    if header[:2] == "# ":
        return header[2:]
    else:
        raise Exception("No header found in document.")


def strip_whitespace(text: str) -> str:
    return text.strip("\n").strip("\t").strip(" ")


def parse_nodes(old_nodes: list[TextNode], delimiter: str, type: TextType) -> list[TextNode]:
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.PLAIN:
            new_nodes.append(n)
            continue
        new_strings = n.text.split(delimiter)

        # Check if there are an even number of delimiters
        if len(new_strings) % 2 != 1:
            raise Exception("Invalid markdown syntax: Uneven delimiters")
        # Track if a node is enveloped by delimeters by its parity
        if n.text[:len(delimiter)] == delimiter:
            count = 1
        else:
            count = 0
        for s in new_strings:
            # Skip over empty strings
            if s == "":
                continue
            # If the string is outside delimeters, make it plain text
            elif count % 2 == 0:
                new_nodes.append(TextNode(s, TextType.PLAIN))
            # Otherwise, add a new node with the proper type
            else:
                new_nodes.append(TextNode(s, type))
            count += 1
    
    return new_nodes

def split_url_nodes(old_nodes: list[TextNode], type: TextType):
    match type:
        case TextType.EMBED:
            parser = r"!\[(.*?)\]\((.*?)\)"
        case TextType.LINK:
            parser = r"\[(.*?)\]\((.*?)\)"
        case _:
            raise Exception("Exception: Unsupported Text Type. Must be EMBED or LINK")

    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.PLAIN:
            new_nodes.append(n)
            continue
        # Save the original text of the node to use for later
        text = n.text
        # Find all the text, alt text, and urls in the string
        links = re.findall(parser, n.text)
        
        # No links found, add the node as is and skip the iteration
        if len(links) == 0:
            new_nodes.append(n)
            continue

        for l in links:
            # Split the string or fragment by the proper format
            if type == TextType.EMBED:
                splits = text.split(f"![{l[0]}]({l[1]})", 1)
            else:
                splits = text.split(f"[{l[0]}]({l[1]})", 1)
            # Check if there was text before the link
            if splits[0] != '':
                new_nodes.append(TextNode(splits[0], TextType.PLAIN))
            # Then add the linked node
            new_nodes.append(TextNode(l[0], type, l[1]))
            # Assign the text variable to the rest of the string
            text = splits[1]
        # Check for text after the last link
        if splits[1] != '':
            new_nodes.append(TextNode(splits[1], TextType.PLAIN))
    
    return new_nodes


def parse_text(text: str) -> list[TextNode]:
    # Define a parsing order (dict makes it expandable)
    parse_order = {
        TextType.BOLD: "**",
        TextType.ITALIC: "_",
        TextType.CODE: "`",
    }
    # Do the same for link types
    link_order = [TextType.EMBED, TextType.LINK]
    nodes = [TextNode(text, TextType.PLAIN)]

    # Loop through delimeter types and restructure the list
    for k,v in parse_order.items():
        nodes = parse_nodes(nodes, v, k)
    
    # Loop through the embed types and restructure
    for type in link_order:
        nodes = split_url_nodes(nodes, type)
    
    return nodes


def markdown_to_blocks(text: str) -> list[str]:
    raw_blocks = text.split("\n\n")
    finished_blocks = []
    for b in raw_blocks:
        if b != "":
            finished_blocks.append(strip_whitespace(b))

    return finished_blocks


def assign_block_type(block: str) -> BlockType:
    # Check for a heading
    heading = re.search(r"\A#{1,6} ", block)
    if heading:
        return BlockType(heading.span()[1] - 1)
    # Next, check for a code block
    if block[0:4] == "```\n" and block[-3:] == "```":
        return BlockType.CODE
    # Split the string by newlines to check for lists or quotes
    lines = block.split("\n")
    quote = True
    order = True
    unorder = True
    for line in lines:
        # Skip over blank lines. These will be processed out
        if line == '':
            continue
        if line[0] != ">":
            quote = False
        if re.findall(r"[0-9]+.", line) == []:
            order = False
        if line[:2] != "- ":
            unorder = False
    # Return the proper type according to the findings per line
    if quote:
        return BlockType.QUOTE
    if order:
        return BlockType.ORDERED
    if unorder:
        return BlockType.UNORDERED
    return BlockType.PARAGRAPH


def block_to_html(text: str, type: BlockType) -> list[str]:
    elements = []
    match type:
        case BlockType.HEADING1:
            elements = [text[2:]]
        case BlockType.HEADING2:
            elements = [text[3:]]
        case BlockType.HEADING3:
            elements = [text[4:]]
        case BlockType.HEADING4:
            elements = [text[5:]]
        case BlockType.HEADING5:
            elements = [text[6:]]
        case BlockType.HEADING6:
            elements = [text[7:]]
        case BlockType.CODE:
            if text[-4] == "\n":
                text = text[4:-3]
            else:
                text = text[4:-2]
            return [LeafNode(None, text)]
        case BlockType.QUOTE | BlockType.UNORDERED | BlockType.ORDERED:
            lines = text.split("\n")
            for l in lines:
                if type == BlockType.QUOTE:
                    elements.append(re.sub(r">\s?", "", l, count=1))
                elif type == BlockType.ORDERED:
                    elements.append(re.sub(r"[0-9]+. ", "", l, count=1))
                else:
                    elements.append(l[2:])
        case BlockType.PARAGRAPH:
            elements = text.split("\n")
            for i in range(len(elements) - 1):
                elements[i] += " "
        case _:
            raise Exception(f"Unhandled block type: {type}")
    
    children = []
    for e in elements:
        items = parse_text(e)
        item_html = [text_node_to_html_node(i) for i in items]
        # Make a special wrapper for lists 
        if type in [BlockType.UNORDERED, BlockType.ORDERED]:
            children.append(ParentNode(type_to_tag[TextType.LIST_ITEM], item_html))
        elif type == BlockType.QUOTE:
            if e != elements[-1]:
                if len(item_html) > 0:
                    item_html[-1].value += "\n"
                else:
                    item_html.append(LeafNode(None, "\n"))
            children += item_html
        else:
            children += item_html

    return children


def markdown_to_html(text: str) -> HTMLNode:
    blocks = markdown_to_blocks(text)
    # Establish a root for the document
    root = ParentNode(type_to_tag[BlockType.DIV], [])
    for block in blocks:
        type = assign_block_type(block)
        # Establish a root for the block
        block_root = ParentNode(type_to_tag[type], None)
        if type == BlockType.CODE:
            pre_block = ParentNode(type_to_tag[BlockType.PRE], [block_root])
            root.children.append(pre_block)
        else:
            root.children.append(block_root)
        # Remove the delimeters from the block and break by line if necessary
        block_root.children = block_to_html(block, type)
        
    # Return the root node
    return root
