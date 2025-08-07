import os
import shutil


def copy_directory_recursive(source_dir, dest_dir):
    """
    Recursively copy all contents from source directory to destination directory.
    
    First deletes all contents of the destination directory to ensure a clean copy,
    then copies all files and subdirectories from source to destination.
    
    Args:
        source_dir (str): Path to the source directory
        dest_dir (str): Path to the destination directory
    """
    # First, clean up the destination directory
    if os.path.exists(dest_dir):
        print(f"Cleaning destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)
    
    # Create the destination directory
    print(f"Creating destination directory: {dest_dir}")
    os.mkdir(dest_dir)
    
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory does not exist: {source_dir}")
        return
    
    # Copy all contents recursively
    _copy_directory_contents(source_dir, dest_dir)
    print(f"Finished copying from {source_dir} to {dest_dir}")


def _copy_directory_contents(source_dir, dest_dir):
    """
    Helper function to recursively copy directory contents.
    
    Args:
        source_dir (str): Path to the source directory
        dest_dir (str): Path to the destination directory
    """
    # List all items in the source directory
    items = os.listdir(source_dir)
    
    for item in items:
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(source_path):
            # If it's a file, copy it
            print(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            # If it's a directory, create it and recursively copy its contents
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            _copy_directory_contents(source_path, dest_path)
