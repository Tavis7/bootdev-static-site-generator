from enum import Enum

class TextType(Enum):
    PLAIN_TEXT  = "plain"
    BOLD_TEXT   = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT   = "code"
    LINK_TEXT   = "link"
    IMAGE_TEXT  = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        if text_type == TextType.LINK_TEXT or text_type == TextType.IMAGE_TEXT:
            if url == None:
                raise Exception(f"{self.text_type.value} nodes require a URL")

    def __eq__(self, other):
        return (self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url)
    
    def __repr__(self):
        return f'TextNode("{self.text}", {self.text_type.value}, "{self.url}")'

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        inside = True
        for part in node.text.split(delimiter):
            inside = not inside
            new_nodes.append(TextNode(part,
                                      node.text_type if not inside else text_type))
        if inside:
            raise Exception(f"Missing matching '{delimiter}' for {node.text}")
    return new_nodes
