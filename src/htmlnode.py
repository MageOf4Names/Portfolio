class HTMLNode():
    def __init__(self, tag: str | None = None, val: str | None = None,
                 children = None,
                 props: dict[str, str] | None = None):
        self.tag = tag
        self.value = val
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        props = ""

        # If props is empty or doesn't exist, return an empty string
        if not self.props or self.props == {}:
            return props
        
        # Iterate through all properties of props and add it to the return string
        for k, v in self.props.items():
            props += f'{k}="{v}" '
        # Return the final string minus the last trailing space
        return props[:-1]
    
    def __repr__(self):
        return f"HTMLNODE:\nTag:\t{self.tag}\nValue\t{self.value}\nChildren\t{self.children}\nProps:\t{self.props_to_html})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, val: str | None, props = None, children: None = None):
        super().__init__(tag, val, props=props)

    def to_html(self):
        # Leaf nodes cannot have no value, raise error
        if self.value == None:
            return ValueError()
        # No tag gets returned as plain text
        if self.tag == None:
            return self.value
        # Pretty print if there are tags
        if self.props and self.props != {}:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        # No whitespace for no tags
        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"HTMLNODE:\nTag:\t{self.tag}\nValue\t{self.value}\nProps:\t{self.props_to_html()})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError()
        childText = ""
        for c in self.children:
            childText += c.to_html()

        # Pretty print if there are tags
        if self.props and self.props != {}:
            return f"<{self.tag} {self.props_to_html()}>{childText}</{self.tag}>"
        # No whitespace for no tags
        return f"<{self.tag}>{childText}</{self.tag}>"
