import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')

        node = HTMLNode(props={"href": "https://boot.dev/"})
        self.assertEqual(node.props_to_html(),
                         ' href="https://boot.dev/"')

        node = HTMLNode(props={"href": "https://boot.dev/",
                               "target": "_blank"})
        self.assertEqual(node.props_to_html(),
                         ' href="https://boot.dev/" target="_blank"')
