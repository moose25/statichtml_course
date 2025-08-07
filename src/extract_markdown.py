import re


def extract_markdown_images(text):
    """
    Extract markdown images from text.
    Returns a list of tuples: (alt_text, url)
    """
    # Pattern for markdown images: ![alt text](url)
    # Use non-greedy matching and handle nested brackets
    pattern = r"!\[([^\]]*)\]\(([^\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    """
    Extract markdown links from text.
    Returns a list of tuples: (anchor_text, url)
    """
    # Pattern for markdown links: [anchor text](url)
    # But not images (which start with !)
    # Use non-greedy matching and handle nested brackets
    pattern = r"(?<!!)\[([^\]]*)\]\(([^\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
