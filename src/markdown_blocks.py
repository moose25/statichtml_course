from enum import Enum
import re

from htmlnode import ParentNode, LeafNode
from textnode import TextNode
from split_nodes import text_to_textnodes
from text_to_html import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    """
    Split a markdown string into blocks based on double newlines.
    
    Args:
        markdown (str): Raw markdown text
        
    Returns:
        list: List of block strings with whitespace stripped and empty blocks removed
    """
    # Split by double newlines to get blocks
    blocks = markdown.split('\n\n')
    
    # Strip whitespace and filter out empty blocks
    cleaned_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:  # Only add non-empty blocks
            cleaned_blocks.append(stripped_block)
    
    return cleaned_blocks


def block_to_block_type(block):
    """
    Determine the type of a markdown block.
    
    Args:
        block (str): A single block of markdown text (already stripped)
        
    Returns:
        BlockType: The type of the block
    """
    lines = block.split('\n')
    
    # Check for heading (1-6 # characters followed by space)
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    
    # Check for code block (starts and ends with ```)
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    
    # Check for quote block (every line starts with >)
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with "- ")
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (every line starts with number. followed by space)
    # Numbers must start at 1 and increment by 1
    if all(re.match(r'^\d+\. ', line) for line in lines):
        # Extract the numbers and check if they start at 1 and increment
        numbers = []
        for line in lines:
            match = re.match(r'^(\d+)\. ', line)
            if match:
                numbers.append(int(match.group(1)))
        
        # Check if numbers start at 1 and increment by 1
        if numbers == list(range(1, len(numbers) + 1)):
            return BlockType.ORDERED_LIST
    
    # Default to paragraph if none of the above match
    return BlockType.PARAGRAPH


def text_to_children(text):
    """
    Convert text with inline markdown to a list of HTMLNode children.
    
    Args:
        text (str): Text that may contain inline markdown formatting
        
    Returns:
        list[HTMLNode]: List of HTMLNode objects representing the inline content
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    """Convert a paragraph block to an HTMLNode."""
    lines = block.split("\n")
    paragraph_text = " ".join(lines)
    children = text_to_children(paragraph_text)
    return ParentNode("p", children)


def heading_to_html_node(block):
    """Convert a heading block to an HTMLNode."""
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    
    if level < 1 or level > 6:
        raise ValueError(f"Invalid heading level: {level}")
    
    text = block[level + 1:]  # Skip the hashes and space
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    """Convert a code block to an HTMLNode."""
    if not (block.startswith("```") and block.endswith("```")):
        raise ValueError("Invalid code block")
    
    text = block[3:-3]  # Remove the ``` from start and end
    if text.startswith("\n"):
        text = text[1:]
    code_node = LeafNode("code", text)
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    """Convert a quote block to an HTMLNode."""
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote line")
        new_lines.append(line.lstrip(">").strip())
    
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    """Convert an unordered list block to an HTMLNode."""
    items = []
    for line in block.split("\n"):
        text = line[2:]  # Remove "- " from start
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ul", items)


def ordered_list_to_html_node(block):
    """Convert an ordered list block to an HTMLNode."""
    items = []
    for line in block.split("\n"):
        text = line.split(". ", 1)[1]  # Remove "1. " etc from start
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ol", items)


def markdown_to_html_node(markdown):
    """
    Convert a full markdown document into a single parent HTMLNode.
    
    Args:
        markdown (str): The markdown text to convert
        
    Returns:
        HTMLNode: A parent HTMLNode containing all the converted markdown blocks
    """
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            node = paragraph_to_html_node(block)
        elif block_type == BlockType.HEADING:
            node = heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            node = code_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            node = quote_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = unordered_list_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = ordered_list_to_html_node(block)
        else:
            raise ValueError(f"Invalid block type: {block_type}")
        
        children.append(node)
    
    return ParentNode("div", children)
