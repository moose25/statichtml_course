from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not a TEXT type, just add it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Split the text by the delimiter
        parts = old_node.text.split(delimiter)
        
        # If there's an odd number of parts, the delimiters are unmatched
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown, formatted section not closed")
        
        # Process the parts
        for i, part in enumerate(parts):
            if part == "":
                continue
            
            # Even indices are regular text, odd indices are formatted text
            if i % 2 == 0:
                # Regular text
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Formatted text
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not a TEXT type, just add it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Extract all images from the text
        images = extract_markdown_images(old_node.text)
        
        # If no images found, add the node as-is
        if not images:
            new_nodes.append(old_node)
            continue
        
        # Process the text, splitting around images
        current_text = old_node.text
        
        for alt_text, url in images:
            # Find the full markdown syntax for this image
            image_markdown = f"![{alt_text}]({url})"
            
            # Split the current text around this image
            parts = current_text.split(image_markdown, 1)
            
            # Add the text before the image (if any)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            # Continue with the rest of the text
            current_text = parts[1] if len(parts) > 1 else ""
        
        # Add any remaining text after all images
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not a TEXT type, just add it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Extract all links from the text
        links = extract_markdown_links(old_node.text)
        
        # If no links found, add the node as-is
        if not links:
            new_nodes.append(old_node)
            continue
        
        # Process the text, splitting around links
        current_text = old_node.text
        
        for anchor_text, url in links:
            # Find the full markdown syntax for this link
            link_markdown = f"[{anchor_text}]({url})"
            
            # Split the current text around this link
            parts = current_text.split(link_markdown, 1)
            
            # Add the text before the link (if any)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            # Add the link node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            
            # Continue with the rest of the text
            current_text = parts[1] if len(parts) > 1 else ""
        
        # Add any remaining text after all links
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes


def text_to_textnodes(text):
    """
    Convert raw markdown text to a list of TextNode objects.
    
    This function applies all markdown parsing in sequence:
    1. Start with a single TEXT node
    2. Split bold (**text**)
    3. Split italic (*text*)  
    4. Split code (`text`)
    5. Split images (![alt](url))
    6. Split links ([text](url))
    """
    # Start with a single TEXT node containing all the text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Apply all the splitting functions in sequence
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes
