import os
from copy_static import copy_directory_recursive
from generate_page import generate_pages_recursive


def main():
    # Get the project root directory (parent of src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Define paths
    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")
    content_dir = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")
    
    print("Starting static site generation...")
    print(f"Project root: {project_root}")
    print()
    
    # Copy static files to public directory
    copy_directory_recursive(static_dir, public_dir)
    print()
    
    # Generate all pages recursively from content directory
    generate_pages_recursive(content_dir, template_path, public_dir)
    
    print("\nStatic site generation completed!")


if __name__ == "__main__":
    main()
