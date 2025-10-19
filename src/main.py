from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
print("Hello world")

def main():
    text_node_1 = TextNode("This is some plain text", TextType.PLAIN_TEXT)

    print()
    print(text_node_1)
    print()
    print(text_node_to_html_node(text_node_1))
    print()
    print(text_node_to_html_node(text_node_1).to_html())
    print()

    text_node_2 = TextNode("This is some anchor text", TextType.LINK_TEXT, "https://www.boot.dev")

    print()
    print(text_node_2)
    print()
    print(text_node_to_html_node(text_node_2))
    print()
    print(text_node_to_html_node(text_node_2).to_html())
    print()

    text_node_2 = TextNode("This is some image text", TextType.IMAGE_TEXT, "example.com/image.png")

    print()
    print(text_node_2)
    print()
    print(text_node_to_html_node(text_node_2))
    print()
    print(text_node_to_html_node(text_node_2).to_html())
    print()



    node2 = HTMLNode(props={"href":"https://boot.dev/", "target":"_blank"})
    print(node2)
    print(f"|{node2.props_to_html()}|")

    node3 = LeafNode("p", "this is a paragraph")
    print(node3)
    print(node3.to_html())

    node4 = LeafNode("a", "Click me!", {"href": "https//boot.dev/"})
    print(node4)
    print(node4.to_html())

    node5 = ParentNode("div", [node4, node3])
    print(node5)
    print(node5.to_html())

    print()
    node6 = ParentNode("div", [node5, node5, node3, node5])
    print(node6)
    print()
    print(node6.to_html())

if __name__ == "__main__":
    main()

