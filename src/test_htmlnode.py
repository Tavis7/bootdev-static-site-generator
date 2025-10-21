import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node, markdown_to_html_node
from textnode import TextNode, TextType

def print_line_diff(a, b):
    for i in range(0, len(a)//80 + 1):
        print()
        print(a[i * 80: i * 80 + 80])
        print(b[i * 80: i * 80 + 80])

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
            "> more quote",
            "> even more quote",
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
        
        expected = "".join([
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
            "<blockquote>",
            "more quote ",
            "even more quote",
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
        ])

        self.assertEqual(node.to_html(), expected)

    def test_markdown_to_html_node_paragraphs_with_formatting(self):
        markdown = "\n".join([
            "here's a **paragraph**",
        ])

        node = markdown_to_html_node(markdown)

        self.assertEqual(node.to_html(), "".join([
            "<div>", "<p>",
            "here's a ", "<b>", "paragraph", "</b>",
            "</p>", "</div>"
        ]))

        markdown = "\n".join([
            "here's a **paragraph**",
            "",
            "here's _another_ **paragraph**",
            "",
            "here's one with [some](https://boot.dev/) [links](http://example.com/),",
            "`code`, and a _newline_",
        ])

        node = markdown_to_html_node(markdown)

        self.assertEqual(node.to_html(), "".join([
            "<div>",
            "<p>",
            "here's a ", "<b>", "paragraph", "</b>",
            "</p>",
            "<p>",
            "here's ", "<i>", "another", "</i>", " ", "<b>", "paragraph", "</b>",
            "</p>",
            "<p>",
            "here's one with ",
            '<a href="https://boot.dev/">', "some", "</a>",
            " ",
            '<a href="http://example.com/">', "links", "</a>",
            ",\n",
            "<code>", "code", "</code>", ", and a ", "<i>", "newline", "</i>",
            "</p>",
            "</div>"
        ]))

    def test_markdown_to_html_node_headers_with_formatting(self):
        markdown = "\n".join([
            "# here's a **header**",
        ])

        node = markdown_to_html_node(markdown)

        self.assertEqual(node.to_html(), "".join([
            "<div>", "<h1>",
            "here's a ", "<b>", "header", "</b>",
            "</h1>", "</div>"
        ]))

        markdown = "\n".join([
            "## here's a **header**",
            "",
            "###### here's _another_ **header**",
            "",
            "".join(["#### here's one with [some](https://boot.dev/) ",
                     "[links](http://example.com/), `code`, but no _newline_"])
        ])

        node = markdown_to_html_node(markdown)

        expected = "".join([
            "<div>",
            "<h2>",
            "here's a ", "<b>", "header", "</b>",
            "</h2>",
            "<h6>",
            "here's ", "<i>", "another", "</i>", " ", "<b>", "header", "</b>",
            "</h6>",
            "<h4>",
            "here's one with ",
            '<a href="https://boot.dev/">', "some", "</a>",
            " ",
            '<a href="http://example.com/">', "links", "</a>", ", "
            "<code>", "code", "</code>", ", but no ", "<i>", "newline", "</i>",
            "</h4>",
            "</div>"])

        self.assertEqual(node.to_html(), expected)

    def test_markdown_to_html_node_code_with_formatting(self):
        markdown = "\n".join([
            "```",
            "# here's a **code block**",
            "```"
        ])

        node = markdown_to_html_node(markdown)

        self.assertEqual(node.to_html(), "".join([
            "<div>", "<p>", "<code>",
            "# here's a **code block**",
            "</code>", "</p>", "</div>"
        ]))

    def test_markdown_to_html_node_quote_with_formatting(self):
        markdown = "\n".join([
            "> here's a **quote**",
        ])

        node = markdown_to_html_node(markdown)

        self.assertEqual(node.to_html(), "".join([
            "<div>", "<blockquote>",
            "here's a ", "<b>", "quote", "</b>",
            "</blockquote>", "</div>"
        ]))

        markdown = "\n".join([
            ">here's a **block quote**",
            "",
            "> here's _another_ **block quote**",
            "",
            "".join(["> here's one with [some](https://boot.dev/) \n",
                     ">[links](http://example.com/), `code`, but no _newline_"])
        ])

        node = markdown_to_html_node(markdown)

        expected = "".join([
            "<div>",
            "<blockquote>",
            "here's a ", "<b>", "block quote", "</b>",
            "</blockquote>",
            "<blockquote>",
            "here's ", "<i>", "another", "</i>", " ", "<b>", "block quote", "</b>",
            "</blockquote>",
            "<blockquote>",
            "here's one with ",
            '<a href="https://boot.dev/">', "some", "</a>",
            " ",
            '<a href="http://example.com/">', "links", "</a>", ", "
            "<code>", "code", "</code>", ", but no ", "<i>", "newline", "</i>",
            "</blockquote>",
            "</div>"])

        print_line_diff(node.to_html(), expected)
        self.assertEqual(node.to_html(), expected)

    def test_markdown_to_html_node_unordered_list_with_formatting(self):
        markdown = "\n".join([
            "- here's a **list item**",
        ])

        node = markdown_to_html_node(markdown)

        self.assertEqual(node.to_html(), "".join([
            "<div>", "<ul>", "<li>",
            "here's a ", "<b>", "list item", "</b>",
            "</li>", "</ul>", "</div>"
        ]))

        markdown = "\n".join([
            "- here's a **list item**",
            "",
            "- here's _another_ **list item**",
            "",
            "- here's a list with",
            "- [some](https://boot.dev/)",
            "- [links](http://example.com/)",
            "- ![an image](http://example.com/image.png)",
            "- `code`",
            "- and **some** _formatting_"
        ])

        node = markdown_to_html_node(markdown)

        expected = "".join([
            "<div>",
            "<ul>", "<li>",
            "here's a ", "<b>", "list item", "</b>",
            "</li>", "</ul>",
            "<ul>", "<li>",
            "here's ", "<i>", "another", "</i>", " ", "<b>", "list item", "</b>",
            "</li>", "</ul>",
            "<ul>", "<li>",
            "here's a list with",
            "</li>", "<li>",
            '<a href="https://boot.dev/">', "some", "</a>",
            "</li>", "<li>",
            '<a href="http://example.com/">', "links", "</a>"
            "</li>", "<li>",
            '<img src="http://example.com/image.png" alt="an image">'"</img>"
            "</li>", "<li>",
            "<code>", "code", "</code>",
            "</li>", "<li>",
            "and ",
            "<b>", "some", "</b>", " ",
            "<i>", "formatting", "</i>",
            "</li>", "</ul>",
            "</div>"])

        print_line_diff(node.to_html(), expected)
        self.assertEqual(node.to_html(), expected)

    def test_markdown_to_html_node_ordered_list_with_formatting(self):
        markdown = "\n".join([
            "1. here's a **list item**",
        ])

        node = markdown_to_html_node(markdown)

        self.assertEqual(node.to_html(), "".join([
            "<div>", "<ol>", "<li>",
            "here's a ", "<b>", "list item", "</b>",
            "</li>", "</ol>", "</div>"
        ]))

        markdown = "\n".join([
            "5. here's a **list item**",
            "",
            "5. here's _another_ **list item**",
            "",
            "500. here's a list with",
            "550. [some](https://boot.dev/)",
            "148. [links](http://example.com/)",
            "5. ![an image](http://example.com/image.png)",
            "2. `code`",
            "70. and **some** _formatting_"
        ])

        node = markdown_to_html_node(markdown)

        expected = "".join([
            "<div>",
            "<ol>", "<li>",
            "here's a ", "<b>", "list item", "</b>",
            "</li>", "</ol>",
            "<ol>", "<li>",
            "here's ", "<i>", "another", "</i>", " ", "<b>", "list item", "</b>",
            "</li>", "</ol>",
            "<ol>", "<li>",
            "here's a list with",
            "</li>", "<li>",
            '<a href="https://boot.dev/">', "some", "</a>",
            "</li>", "<li>",
            '<a href="http://example.com/">', "links", "</a>"
            "</li>", "<li>",
            '<img src="http://example.com/image.png" alt="an image">'"</img>"
            "</li>", "<li>",
            "<code>", "code", "</code>",
            "</li>", "<li>",
            "and ",
            "<b>", "some", "</b>", " ",
            "<i>", "formatting", "</i>",
            "</li>", "</ol>",
            "</div>"])

        print_line_diff(node.to_html(), expected)
        self.assertEqual(node.to_html(), expected)
