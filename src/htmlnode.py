from textnode import TextType, TextNode

def format_string_or_none(string):
    if string == None:
        return "None"
    else:
        return f'"{string}"'

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag      = tag
        self.value    = value
        self.children = children
        self.props    = props

    def to_html(self):
        raise NotImplementedError("Not implemented")

    def props_to_html(self):
        return ("".join(map(lambda key: f' {key}="{self.props[key]}"', self.props))
                if self.props != None else "")

    def __repr__(self):
        return ", ".join([f'HTMLNode(tag={format_string_or_none(self.tag)}',
                          f'value={format_string_or_none(self.value)}',
                          f'children={self.children}',
                          f'props={self.props})'])

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf node with no value")
        else:
            otag,ctag = "",""
            if self.tag != None:
                otag,ctag = f"<{self.tag}{self.props_to_html()}>",f"</{self.tag}>"

            return f'{otag}{self.value}{ctag}'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent node with no tag")
        elif self.children == None:
            raise ValueError("Parent node with no children")
        else:
            children = list(map(lambda child: child.to_html(), self.children))
            return f'<{self.tag}{self.props_to_html()}>{"".join(children)}</{self.tag}>'

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.PLAIN_TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code", text_node.text)
        case TextType.LINK_TEXT:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE_TEXT:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception(f"Unknown text type: {text_node.text_type}")
