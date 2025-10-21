import unittest
from textnode import TextNode, TextType, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links, text_to_textnodes

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


    def test_split_nodes_delimiter_nested(self):
        node = TextNode("This **sentence** `contains _multiple_ t**ype**s of `text.",
                        TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This **sentence** ", TextType.PLAIN_TEXT),
            TextNode("contains _multiple_ t**ype**s of ", TextType.CODE_TEXT),
            TextNode("text.", TextType.PLAIN_TEXT),
        ])

        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This **sentence** ", TextType.PLAIN_TEXT),
            TextNode("contains _multiple_ t**ype**s of ", TextType.CODE_TEXT),
            TextNode("text.", TextType.PLAIN_TEXT),
        ])

        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This ", TextType.PLAIN_TEXT),
            TextNode("sentence", TextType.BOLD_TEXT),
            TextNode(" ", TextType.PLAIN_TEXT),
            TextNode("contains _multiple_ t**ype**s of ", TextType.CODE_TEXT),
            TextNode("text.", TextType.PLAIN_TEXT),
        ])


    def test_extract_markdown_images(self):
        images = extract_markdown_images(
            "".join(["this is an image: ![image](example.com/img.png), ",
                     "and another: ![second image](example.com/img2.png)..."]))
        self.assertEqual(images, [
            ("![image](example.com/img.png)",
             "image", "example.com/img.png"),
            ("![second image](example.com/img2.png)",
             "second image", "example.com/img2.png")
        ])

        images = extract_markdown_images(
            "".join(["this is a link: [link](example.com/img.png), ",
                     "and another: [second link](example.com/img2.png)"]))
        self.assertEqual(images, [])

        images = extract_markdown_images(
            "".join(["![image](example.com/img.png), ",
                     "![second image](example.com/img2.png)"
                     ]))
        self.assertEqual(images, [
            ("![image](example.com/img.png)",
             "image", "example.com/img.png"),
            ("![second image](example.com/img2.png)",
             "second image", "example.com/img2.png")
        ])

        images = extract_markdown_images(
            "".join(["[link](example.com/img.png), ",
                     "and another: [second link](example.com/img2.png)"]))
        self.assertEqual(images, [])

    def test_extract_markdown_images_brackets(self):
        images = extract_markdown_images("![[]()")
        self.assertEqual(images, [])
        images = extract_markdown_images("![]]()")
        self.assertEqual(images, [])
        images = extract_markdown_images("![](()")
        self.assertEqual(images, [])
        images = extract_markdown_images("![]())")
        self.assertEqual(images, [("![]()", "","")])


    def test_extract_markdown_links(self):
        links = extract_markdown_links(
            "".join(["this is an image: ![image](example.com/img.png), ",
                     "and another: ![second image](example.com/img2.png)..."]))
        self.assertEqual(links, [])

        links = extract_markdown_links(
            "".join(["this is a link: [link](example.com/img.png), ",
                     "and another: [second link](example.com/img2.png)"]))
        self.assertEqual(links, [
            ("[link](example.com/img.png)",
             "link", "example.com/img.png"),
            ("[second link](example.com/img2.png)",
             "second link", "example.com/img2.png")
        ])

        links = extract_markdown_links(
            "".join(["![image](example.com/img.png), ",
                     "![second image](example.com/img2.png)"
                     ]))
        self.assertEqual(links, [])

        links = extract_markdown_links(
            "".join(["[link](example.com/img.png), ",
                     "and another: [second link](example.com/img2.png)"]))
        self.assertEqual(links, [
            ("[link](example.com/img.png)",
             "link", "example.com/img.png"),
            ("[second link](example.com/img2.png)",
             "second link", "example.com/img2.png")
        ])


    def test_extract_markdown_links_brackets(self):
        links = extract_markdown_links("[[]()")
        self.assertEqual(links, [("[]()","","")])
        links = extract_markdown_links("[]]()")
        self.assertEqual(links, [])
        links = extract_markdown_links("[](()")
        self.assertEqual(links, [])
        links = extract_markdown_links("[]())")
        self.assertEqual(links, [("[]()", "","")])

    def test_split_nodes_images_single(self):
        node = TextNode("".join([
            "This is an image: ![alt text](example.com/image.png).",
        ]), TextType.PLAIN_TEXT)
        new_nodes = split_nodes_images([node])
        self.assertEqual(new_nodes, [
            TextNode("This is an image: ", TextType.PLAIN_TEXT),
            TextNode("alt text", TextType.IMAGE_TEXT, url="example.com/image.png"),
            TextNode(".", TextType.PLAIN_TEXT),
        ])

    def test_split_nodes_images_single_formatted(self):
        node = [TextNode("".join([
            "**This is an image: ![alt text](example.com/image.png).**",
        ]), TextType.PLAIN_TEXT)]
        new_nodes = split_nodes_delimiter(node, "**", TextType.BOLD_TEXT)
        new_nodes = split_nodes_images(new_nodes)
        self.assertEqual(new_nodes, [
            TextNode("This is an image: ![alt text](example.com/image.png).",
                     TextType.BOLD_TEXT)
        ])

    def test_split_nodes_links_single(self):
        node = TextNode("".join([
            "This is a link: [link text](example.com/image.png).",
        ]), TextType.PLAIN_TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(new_nodes, [
            TextNode("This is a link: ", TextType.PLAIN_TEXT),
            TextNode("link text", TextType.LINK_TEXT, url="example.com/image.png"),
            TextNode(".", TextType.PLAIN_TEXT),
        ])

    def test_split_nodes_links_single_formatted(self):
        node = [TextNode("".join([
            "**This is a link: [link text](example.com/image.png).**",
        ]), TextType.PLAIN_TEXT)]
        new_nodes = split_nodes_delimiter(node, "**", TextType.BOLD_TEXT)
        new_nodes = split_nodes_links(new_nodes)
        self.assertEqual(new_nodes, [
            TextNode("This is a link: [link text](example.com/image.png).",
                     TextType.BOLD_TEXT)
        ])

    def test_split_nodes_images_multiple(self):
        node = TextNode("".join([
            "This is an image: ![alt text](example.com/image.png), ",
                "and another: ![alt two](example.com/image2.png).",
        ]), TextType.PLAIN_TEXT)
        new_nodes = split_nodes_images([node])
        self.assertEqual(new_nodes, [
            TextNode("This is an image: ", TextType.PLAIN_TEXT),
            TextNode("alt text", TextType.IMAGE_TEXT, url="example.com/image.png"),
            TextNode(", and another: ", TextType.PLAIN_TEXT),
            TextNode("alt two", TextType.IMAGE_TEXT, url="example.com/image2.png"),
            TextNode(".", TextType.PLAIN_TEXT),
        ])

    def test_split_nodes_links_multiple(self):
        node = TextNode("".join([
            "This is a link: [link text](example.com/image.png), ",
            "and another: [link two](example.com/image2.png).",
        ]), TextType.PLAIN_TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(new_nodes, [
            TextNode("This is a link: ", TextType.PLAIN_TEXT),
            TextNode("link text", TextType.LINK_TEXT, url="example.com/image.png"),
            TextNode(", and another: ", TextType.PLAIN_TEXT),
            TextNode("link two", TextType.LINK_TEXT, url="example.com/image2.png"),
            TextNode(".", TextType.PLAIN_TEXT),
        ])

    def test_text_to_textnodes(self):
        text = "".join([
            "This is **text** with an _italic_ word and a `code block` and an ",
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a ",
            "[link](https://boot.dev)"
        ])

        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGE_TEXT,
                     url="https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK_TEXT,
                     url="https://boot.dev"),
        ])

    def test_text_to_textnodes_nested(self):
        text = "".join([
            "This is **text** with an _italic_ word and a `**code_ block` and an ",
            "![**obi _wan_ image**](https://i.imgur.com/fJRm4Vk.jpeg) and a ",
            "[link](https://boot.dev)"
        ])

        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("**code_ block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("**obi _wan_ image**", TextType.IMAGE_TEXT,
                     url="https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK_TEXT,
                     url="https://boot.dev"),
        ])


if __name__ == "__main__":
    unittest.main()
