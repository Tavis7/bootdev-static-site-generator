import unittest
from textnode import TextNode, TextType, split_nodes_delimiter

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

    def test_split_nodes_delimiter(self):
        node = TextNode("This text contains nothing", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [node])

        node = TextNode("This text contains `code`", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This text contains ", TextType.PLAIN_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode("", TextType.PLAIN_TEXT)
        ])

    def test_split_nodes_delimiter_multi(self):
        node = TextNode("This **sentence** `contains` _multiple_ t**ype**s `of` text.",
                        TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This ", TextType.PLAIN_TEXT),
            TextNode("sentence", TextType.BOLD_TEXT),
            TextNode(" `contains` _multiple_ t", TextType.PLAIN_TEXT),
            TextNode("ype", TextType.BOLD_TEXT),
            TextNode("s `of` text.", TextType.PLAIN_TEXT)
        ])

        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This ", TextType.PLAIN_TEXT),
            TextNode("sentence", TextType.BOLD_TEXT),
            TextNode(" `contains` ", TextType.PLAIN_TEXT),
            TextNode("multiple", TextType.ITALIC_TEXT),
            TextNode(" t", TextType.PLAIN_TEXT),
            TextNode("ype", TextType.BOLD_TEXT),
            TextNode("s `of` text.", TextType.PLAIN_TEXT)
        ])

        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This ", TextType.PLAIN_TEXT),
            TextNode("sentence", TextType.BOLD_TEXT),
            TextNode(" ", TextType.PLAIN_TEXT),
            TextNode("contains", TextType.CODE_TEXT),
            TextNode(" ", TextType.PLAIN_TEXT),
            TextNode("multiple", TextType.ITALIC_TEXT),
            TextNode(" t", TextType.PLAIN_TEXT),
            TextNode("ype", TextType.BOLD_TEXT),
            TextNode("s ", TextType.PLAIN_TEXT),
            TextNode("of", TextType.CODE_TEXT),
            TextNode(" text.", TextType.PLAIN_TEXT)
        ])



if __name__ == "__main__":
    unittest.main()
