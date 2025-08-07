import os

from markdown_blocks import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path, template_path, dest_path, basepath="/"):
    """
    Generate an HTML page from a markdown file using a template.
    
    Args:
        from_path (str): Path to the markdown file
        template_path (str): Path to the HTML template file
        dest_path (str): Path where the generated HTML should be saved
        basepath (str): Base path for URLs (default: "/")
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract the title
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Replace base path URLs
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    
    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write the final HTML to destination
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"Page generated successfully: {dest_path}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """
    Recursively generate HTML pages for all markdown files in a directory.
    
    Args:
        dir_path_content (str): Path to the content directory containing markdown files
        template_path (str): Path to the HTML template file
        dest_dir_path (str): Path to the destination directory where HTML files should be saved
        basepath (str): Base path for URLs (default: "/")
    """
    print(f"Generating pages recursively from {dir_path_content} to {dest_dir_path}")
    
    # Check if content directory exists
    if not os.path.exists(dir_path_content):
        print(f"Content directory does not exist: {dir_path_content}")
        return
    
    # Walk through all files and directories in the content directory
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                # Get the full path to the markdown file
                markdown_path = os.path.join(root, file)
                
                # Calculate the relative path from the content directory
                rel_path = os.path.relpath(markdown_path, dir_path_content)
                
                # Create the destination HTML path
                # Replace .md extension with .html
                html_rel_path = rel_path.replace('.md', '.html')
                dest_path = os.path.join(dest_dir_path, html_rel_path)
                
                # Generate the page
                generate_page(markdown_path, template_path, dest_path, basepath)
    
    print("Recursive page generation completed!")
