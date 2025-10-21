from textnode import TextType, TextNode, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node, markdown_to_html_node
from markdownblock import markdown_to_blocks
print("Hello world")

def main():
    markdown = "\n".join([
        "- unordered list first",
        "- unordered list second",
        "- unordered list third",
        "",
        "1. ordered list first",
        "2. ordered list second",
        "3. ordered list third",
    ])

    nodes = markdown_to_html_node(markdown)
    print(nodes)
    print()
    print(nodes.to_html())

if __name__ == "__main__":
    main()

