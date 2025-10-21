from textnode import TextType, TextNode, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from markdown import markdown_to_blocks
print("Hello world")

def main():
    text_node_1 = TextNode("Hello `code` world", TextType.PLAIN_TEXT)
    split = split_nodes_delimiter([text_node_1], "`", TextType.CODE_TEXT)
    print(split)

    images,_ = extract_markdown_images(
        "".join(["![image](example.com/img.png), ",
                 "and another: ![second image](example.com/img2.png)"]))
    print("images: ",images)

    node = TextNode("".join([
        "This is an image: ![alt text](example.com/image.png).",
    ]), TextType.PLAIN_TEXT)
    new_nodes = split_nodes_images([node])

if __name__ == "__main__":
    main()

