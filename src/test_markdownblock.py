import unittest
from markdownblock import markdown_to_blocks, BlockType, block_to_block_type, extract_title

class TestMarkdownBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        heading_text = "# This is a heading"
        paragraph_text = "".join([
            "This is a paragraph of text. ",
            "It has some **bold** and _italic_ words inside of it."])
        list_text = "\n".join([
            "- This is the first list item in a list block",
            "- This is a list item",
            "- This is another list item"])
        text = "\n".join([
            heading_text,
            "",
            paragraph_text,
            "",
            list_text])
        block_list = markdown_to_blocks(text)
        self.assertEqual(block_list, [heading_text, paragraph_text, list_text])

    def test_markdown_to_blocks_extra_whitespace(self):
        heading_text = "# This is a heading"
        paragraph_text = "".join([
            " This is a paragraph of text. ",
            "It has some **bold** and _italic_ words inside of it.   "])
        list_text = "\n".join([
            "- This is the first list item in a list block",
            "- This is a list item",
            "- This is another list item"])
        text = "\n".join([
            "",
            heading_text,
            "",
            "  ",
            paragraph_text,
            "",
            list_text,
            ""
        ])
        block_list = markdown_to_blocks(text)
        self.assertEqual(block_list,
                         [heading_text.strip(),
                          paragraph_text.strip(),
                          list_text.strip()])

    def test_block_to_block_type_paragraph(self):
        expected_type = BlockType.PARAGRAPH

        text = "this is a paragraph"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "this\nis\nalso\na\nparagraph"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = ""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

    def test_block_to_block_type_heading(self):
        expected_type = BlockType.HEADING

        text = "# this is a heading"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "# this\nis\nnot\na\nheading"
        block_type = block_to_block_type(text)
        self.assertNotEqual(block_type, expected_type)

    def test_block_to_block_type_code(self):
        expected_type = BlockType.CODE

        text = "```\nthis is code\n```"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "```python\n#this is also code\n```"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "```\npython\nthis is not code```"
        block_type = block_to_block_type(text)
        self.assertNotEqual(block_type, expected_type)

        text = "a```\npython\nthis is not code\n```b"
        block_type = block_to_block_type(text)
        self.assertNotEqual(block_type, expected_type)

        text = "```\n```"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "```\n\n```"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "```4\n\n```"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "```abc 4\n\n```"
        block_type = block_to_block_type(text)
        self.assertNotEqual(block_type, expected_type)

        text = "```\n\n``"
        block_type = block_to_block_type(text)
        self.assertNotEqual(block_type, expected_type)


    def test_block_to_block_type_quote(self):
        expected_type = BlockType.QUOTE

        text = "> this is quote"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = ">this is also quote"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = ">"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "> this is quote\n> line two"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = ">this is quote\n> line two\n> line 3"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "> this is not quote\n>line two\nline three\n>line four"
        block_type = block_to_block_type(text)
        self.assertNotEqual(block_type, expected_type)

        text = ">> this is quote\n>line two\n>>>line three\n>line four"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

    def test_block_to_block_type_unordered_list(self):
        expected_type = BlockType.UNORDERED_LIST

        text = "- this is list"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "- this is also list"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "- this is list\n- line two"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "- this is list\n- line two\n- line three\n- line four"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "- this is not list\n- line two\n-line three\n- line four"
        block_type = block_to_block_type(text)
        self.assertNotEqual(block_type, expected_type)

        text = "-not list"
        block_type = block_to_block_type(text)
        self.assertNotEqual(block_type, expected_type)

        text = "- \n- "
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "-\n- "
        block_type = block_to_block_type(text)
        self.assertNotEqual(block_type, expected_type)

    def test_block_to_block_type_ordered_list(self):
        expected_type = BlockType.ORDERED_LIST

        text = "1. this is list"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "22315. this is also list"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "39. this is list\n44. line two"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "39. this is list\n44. line two,\n86. line three\n4. "
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "1.not list"
        block_type = block_to_block_type(text)
        self.assertNotEqual(block_type, expected_type)

        text = "5. \n6. "
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, expected_type)

        text = "5.\n6. "
        block_type = block_to_block_type(text)
        self.assertNotEqual(block_type, expected_type)

    def test_extract_title_alone(self):
        text = "# this is a heading"
        self.assertEqual(extract_title(text), "this is a heading")

    def test_extract_title_with_content(self):
        text = "# this is a heading\n\nand content"
        self.assertEqual(extract_title(text), "this is a heading")

    def test_extract_title_with_padding(self):
        text = "# this is a heading      "
        self.assertEqual(extract_title(text), "this is a heading")
        text = "#       this is a heading"
        self.assertEqual(extract_title(text), "this is a heading")
        text = "# this is a heading\n"
        self.assertEqual(extract_title(text), "this is a heading")
        text = "#      this is a heading      \n"
        self.assertEqual(extract_title(text), "this is a heading")

    def test_extract_title_with_padding_and_content(self):
        text = "# this is a heading    \n\nand content"
        self.assertEqual(extract_title(text), "this is a heading")

        text = "#     this is a heading\n\nand content"
        self.assertEqual(extract_title(text), "this is a heading")

        text = "#      this is a heading    \n\nand content"
        self.assertEqual(extract_title(text), "this is a heading")

if __name__ == "__main__":
    unittest.main()
