from textnode import TextType, TextNode
from htmlnode import HTMLNode
print("Hello world")

def main():
    node = TextNode("This is some anchor text", TextType.LINK_TEXT, "https://www.boot.dev")

    print(node)

    node2 = HTMLNode(props={"href":"https://boot.dev/", "target":"_blank"})
    print(node2)
    print(f"|{node2.props_to_html()}|")

if __name__ == "__main__":
    main()

