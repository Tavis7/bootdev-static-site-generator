from textnode import TextType, TextNode, split_nodes_delimiter
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
print("Hello world")

def main():
    text_node_1 = TextNode("Hello `code` world", TextType.PLAIN_TEXT)
    split = split_nodes_delimiter([text_node_1], "`", TextType.CODE_TEXT)
    print(split)

if __name__ == "__main__":
    main()

