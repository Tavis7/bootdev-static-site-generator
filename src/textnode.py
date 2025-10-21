from enum import Enum
import re


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
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node) # Don't split non-text nodes
        else:
            for part in node.text.split(delimiter):
                inside = not inside
                new_nodes.append(TextNode(part,
                                          node.text_type if not inside else text_type))
            if inside:
                raise Exception(f"Missing matching '{delimiter}' for {node.text}\n(Nested formatting is not supported)")
    return new_nodes

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            text = node.text
            for image_text,image_alt,image_url in images:
                parts = text.split(image_text, maxsplit=1)
                if len(parts[0]) > 0:
                    new_nodes.append(TextNode(parts[0], TextType.PLAIN_TEXT))
                text = parts[1]
                new_nodes.append(TextNode(image_alt, TextType.IMAGE_TEXT, url=image_url))
            if len(text) > 0:
                new_nodes.append(TextNode(text, TextType.PLAIN_TEXT))
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            text = node.text
            for link_text,link_alt,link_url in links:
                parts = text.split(link_text, maxsplit=1)
                if len(parts[0]) > 0:
                    new_nodes.append(TextNode(parts[0], TextType.PLAIN_TEXT))
                text = parts[1]
                new_nodes.append(TextNode(link_alt, TextType.LINK_TEXT, url=link_url))
            if len(text) > 0:
                new_nodes.append(TextNode(text, TextType.PLAIN_TEXT))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"(!\[([^\[\]]*)]\(([^\(\)]*)\))", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?:^|[^!])(\[([^\[\]]*)]\(([^\(\)]*)\))", text)
    return matches

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    return nodes
