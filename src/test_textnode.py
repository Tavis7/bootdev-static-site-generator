import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node1, node2)

        node1 = TextNode("This is text node 1", TextType.BOLD_TEXT)
        node2 = TextNode("This is text node 2", TextType.BOLD_TEXT)
        self.assertNotEqual(node1, node2)

        node1 = TextNode("This is a text node", TextType.PLAIN_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node1, node2)

        node1 = TextNode("This is a text node", TextType.ITALIC_TEXT, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT, "https://boot.dev")
        self.assertEqual(node1, node2)

        node1 = TextNode("This is a text node", TextType.ITALIC_TEXT, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT, )
        self.assertNotEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()
