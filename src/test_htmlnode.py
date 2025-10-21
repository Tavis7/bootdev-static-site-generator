import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node, markdown_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')

    def test_props_to_html_with_one(self):
        node = HTMLNode(props={"href": "https://boot.dev/"})
        self.assertEqual(node.props_to_html(),
                         ' href="https://boot.dev/"')

        node = LeafNode("a", "link",
                        props={"href": "https://boot.dev/"})
        self.assertEqual(node.props_to_html(),
                         ' href="https://boot.dev/"')

    def test_props_to_html_with_two(self):
        node = HTMLNode(props={"href": "https://boot.dev/",
                               "target": "_blank"})
        self.assertEqual(node.props_to_html(),
                         ' href="https://boot.dev/" target="_blank"')

        node = LeafNode("a", "link",
                        props={"href": "https://boot.dev/",
                               "target": "_blank"})
        self.assertEqual(node.props_to_html(),
                         ' href="https://boot.dev/" target="_blank"')

    def test_leaf_to_html(self):
        node = LeafNode("p", "this is a paragraph")
        self.assertEqual(node.to_html(), '<p>this is a paragraph</p>')

        node = LeafNode("b", "this is bold text")
        self.assertEqual(node.to_html(),
                         ''.join(['<b>',
                                  'this is bold text',
                                  '</b>']))

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "this is a link", props={"href": "https://boot.dev/"})
        self.assertEqual(node.to_html(),
                         '<a href="https://boot.dev/">this is a link</a>')

        node = LeafNode("a", "this is another link",
                        props={"href": "https://boot.dev/",
                               "target": "_blank"})
        self.assertEqual(node.to_html(),
                         ''.join(['<a href="https://boot.dev/" target="_blank">',
                                  'this is another link',
                                  '</a>']))

        node = LeafNode("a", "this is another link",
                        props={"href": "https://boot.dev/",
                               "target": "_blank"})
        self.assertEqual(node.to_html(),
                         ''.join(['<a href="https://boot.dev/" target="_blank">',
                                  'this is another link',
                                  '</a>']))

    def test_to_html_with_child(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(),
                         "<div><span>child</span></div>")

    def test_to_html_with_children(self):
        children = [
            LeafNode("span", "child"),
LeafNode("a", "link", {"href":"https://boot.dev/", "target":"_blank"}),
            LeafNode("b", "bold")
]
        parent = ParentNode("div", children)
        self.assertEqual(parent.to_html(),
                         "".join(['<div><span>child</span>',
                                  '<a href="https://boot.dev/" target="_blank">',
                                  'link</a><b>bold</b></div>']))

    def test_to_html_with_grandchild(self):
        grandchild = LeafNode("b", "bold")
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(),
                         "<div><span><b>bold</b></span></div>")

    def test_to_html_with_grandchildren(self):
        grandchildren1 = [
            LeafNode("b", "bold"),
            LeafNode("i", "italic")
        ]
        grandchildren2 = [
            LeafNode("em", "emphasis"),
            LeafNode("span", "text")
        ]
        child1 = ParentNode("span", grandchildren1, {"id":"child1"})
        child2 = ParentNode("span", grandchildren2)
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(parent.to_html(),
                         "".join(['<div>',
                                  '<span id="child1">',
                                  '<b>bold</b><i>italic</i>',
                                  '</span>',
                                  '<span>',
                                  '<em>emphasis</em><span>text</span>',
                                  '</span>',
                                  '</div>']))

    def test_text(self):
        text_node = TextNode("Plain", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "Plain")

    def test_bold(self):
        text_node = TextNode("Bold", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>Bold</b>")

    def test_italic(self):
        text_node = TextNode("Italic", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<i>Italic</i>")

    def test_code(self):
        text_node = TextNode("Code", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<code>Code</code>")

    def test_link(self):
        text_node = TextNode("Link", TextType.LINK_TEXT, "https://boot.dev/")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<a href="https://boot.dev/">Link</a>')

    def test_image(self):
        text_node = TextNode("Image", TextType.IMAGE_TEXT, "example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<img src="example.com/image.png" alt="Image"></img>')

    def test_markdown_to_html_node_basic(self):
        markdown = "\n".join([
            "here's a paragraph",
            "",
            "- unordered list first",
            "- unordered list second",
            "- unordered list third",
            "",
            "> a quote",
            "",
            "1. ordered list first",
            "2. ordered list second",
            "3. ordered list third",
            "",
            "",
            "```python",
            "def say_hello():",
            '    print "hello"',
            "```",
            "",
            "# heading 1",
            "",
            "## heading 2",
            "",
            "another paragraph"
        ])

        node = markdown_to_html_node(markdown)

        self.assertEqual(node.to_html(), "".join([
            "<div>", "<p>",
            "here's a paragraph",
            "</p>",
            "<ul>", "<li>",
            "unordered list first",
            "</li>",
            "<li>",
            "unordered list second",
            "</li>",
            "<li>",
            "unordered list third",
            "</li>", "</ul>",
            "<blockquote>",
            "a quote",
            "</blockquote>",
            "<ol>", "<li>",
            "ordered list first",
            "</li>",
            "<li>",
            "ordered list second",
            "</li>",
            "<li>",
            "ordered list third",
            "</li>", "</ol>",
            "<p>", "<code>",
            "def say_hello():\n",
            '    print "hello"',
            "</code>", "</p>",
            "<h1>",
            "heading 1",
            "</h1>",
            "<h2>",
            "heading 2",
            "</h2>",
            "<p>",
            "another paragraph",
            "</p>", "</div>"
        ]))
