from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(text):
    split = text.split("\n\n")
    blocks = []
    for block in split:
        # todo: handle individual lines
        block_text = block.strip()
        if len(block_text) != 0:
            blocks.append(block_text)
    return blocks

def block_to_block_type(block):
    if re.match(r"^#{1,6} [^\n]*$", block) != None:
        return BlockType.HEADING
    elif re.match(r"^```[a-zA-Z0-9]*\n(?:.*\n)*```$", block) != None:
        return BlockType.CODE
    elif re.match(r"((?:^|\n)>[^\n]*)+$", block) != None:
        return BlockType.QUOTE
    elif re.match(r"((?:^|\n)- [^\n]*)+$", block) != None:
        return BlockType.UNORDERED_LIST
    elif re.match(r"((?:^|\n)\d+\. [^\n]*)+$", block) != None:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def extract_title(markdown):
    matches = re.findall("(^# )([^\n]*)(?:\n\n.*|\n*$)", markdown)
    if len(matches) != 1:
        raise Exception("Title not found")
    title = matches[0][1].strip()
    return title

