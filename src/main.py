from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode
print("Hello world")

def main():
    node = TextNode("This is some anchor text", TextType.LINK_TEXT, "https://www.boot.dev")

    print(node)

    node2 = HTMLNode(props={"href":"https://boot.dev/", "target":"_blank"})
    print(node2)
    print(f"|{node2.props_to_html()}|")

    node3 = LeafNode("p", "this is a paragraph")
    print(node3)
    print(node3.to_html())

    node4 = LeafNode("a", "Click me!", {"href": "https//boot.dev/"})
    print(node4)
    print(node4.to_html())

if __name__ == "__main__":
    main()

