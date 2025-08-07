import os
import sys
from copy_static import copy_directory_recursive
from generate_page import generate_pages_recursive


def main():
    # Get basepath from command line argument, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    # Get the project root directory (parent of src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Define paths
    static_dir = os.path.join(project_root, "static")
    docs_dir = os.path.join(project_root, "docs")  # Changed from public to docs
    content_dir = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")
    
    print("Starting static site generation...")
    print(f"Project root: {project_root}")
    print(f"Base path: {basepath}")
    print()
    
    # Copy static files to docs directory
    copy_directory_recursive(static_dir, docs_dir)
    print()
    
    # Generate all pages recursively from content directory
    generate_pages_recursive(content_dir, template_path, docs_dir, basepath)
    
    print("\nStatic site generation completed!")


if __name__ == "__main__":
    main()
