import re


def extract_title(markdown):
    """
    Extract the h1 header from a markdown document.
    
    Args:
        markdown (str): The markdown content
        
    Returns:
        str: The title text without the # symbol and stripped of whitespace
        
    Raises:
        ValueError: If no h1 header is found
    """
    lines = markdown.split('\n')
    
    for line in lines:
        # Check if line starts with exactly one # followed by a space
        if re.match(r'^# ', line):
            # Remove the # and any leading/trailing whitespace
            title = line[2:].strip()
            if title:  # Make sure there's actual content after the #
                return title
    
    # If no h1 header found, raise an exception
    raise ValueError("No h1 header found in markdown")
