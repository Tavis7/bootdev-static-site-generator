from textnode import TextType, TextNode
from markdownblock import markdown_to_blocks, block_to_block_type, BlockType
import re

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

def markdown_to_html_node(text):
    blocks = markdown_to_blocks(text)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                #todo Parse markdown
                block_nodes.append(LeafNode("p", block))
            case BlockType.HEADING:
                sides = block.split(" ", maxsplit=1)
                level = len(sides[0])
                block_nodes.append(LeafNode(f"h{level}", sides[1]))
            case BlockType.CODE:
                block_text = block.split("\n")
                block_nodes.append(
                    ParentNode("p",
                               [LeafNode("code", "\n".join(block_text[1:-1]))]))
            case BlockType.QUOTE:
                lines = block.split("\n")
                for line in lines:
                    # Assume single level for now
                    # todo: multi-level quotes
                    #sides = re.findall(r"(^>*)([^>].*$)", line)
                    sides = re.findall(r"(^>)(.*$)", line)
                    rest = sides[0][1]
                    rest = rest.strip()
                    # todo Parse markdown
                    block_nodes.append(LeafNode("blockquote", rest))
            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                list_items = []
                for line in lines:
                    line_matches = re.findall(r"^- (.*)$", line)
                    if len(line_matches) != 1:
                        raise Exception(f"wrong number of matches: {len(line_matches)} != 1")
                    line_text = line_matches[0].strip()
                    #todo Parse markdown
                    list_items.append(LeafNode("li", line_text))
                block_nodes.append(ParentNode("ul", list_items))
            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                list_items = []
                for line in lines:
                    line_matches = re.findall(r"^\d*. (.*)$", line)
                    if len(line_matches) != 1:
                        raise Exception(f"wrong number of matches: {len(line_matches)} != 1")
                    line_text = line_matches[0].strip()
                    #todo Parse markdown
                    list_items.append(LeafNode("li", line_text))
                block_nodes.append(ParentNode("ol", list_items))
    result = ParentNode("div", block_nodes)
    return result
