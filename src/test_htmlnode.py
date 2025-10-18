import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')

        node = HTMLNode(props={"href": "https://boot.dev/"})
        self.assertEqual(node.props_to_html(),
                         ' href="https://boot.dev/"')

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

        node = LeafNode("b", "this is bold text")
        self.assertEqual(node.to_html(),
                         ''.join(['<b>',
                                  'this is bold text',
                                  '</b>']))
