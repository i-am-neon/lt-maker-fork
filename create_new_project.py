import sys
import os
import traceback

from app.editor.file_manager.project_initializer import ProjectInitializer
from PyQt5.QtCore import QDir


def normalize_path(path):
    """Normalize path for cross-platform compatibility."""
    # Remove any double quotes that might have been passed
    path = path.replace('"', '')
    # Convert backslashes to forward slashes first for consistency
    path = path.replace('\\', '/')
    # Then convert to OS-specific path format
    return os.path.normpath(path)


def initialize_new_project_files(nid, title, lt_project_base_path, new_project_relative_path):
    print(f"lt_project_base_path: {lt_project_base_path}")
    
    try:
        # Normalize paths for cross-platform compatibility
        lt_project_base_path = normalize_path(lt_project_base_path)
        new_project_relative_path = normalize_path(new_project_relative_path)
        
        # Debug the paths we're using - with better formatting
        full_path = os.path.join(lt_project_base_path, new_project_relative_path)
        print(f"Full project path: {full_path}")
        print(f"Current working directory: {os.getcwd()}")
        
        # Ensure the parent directory exists (create if needed)
        parent_dir = os.path.dirname(full_path)
        if not os.path.exists(parent_dir):
            print(f"Creating parent directory: {parent_dir}")
            os.makedirs(parent_dir, exist_ok=True)
        
        # Initialize the project
        initializer = ProjectInitializer()
        try:
            initializer.initialize_new_project_files_with_default_project_path(nid, title, lt_project_base_path, new_project_relative_path)
            print(f"Project successfully initialized at: {full_path}")
            return full_path
        except Exception as e:
            print(f"Error in ProjectInitializer: {e}")
            print(f"Error type: {type(e).__name__}")
            traceback.print_exc()
            return None
    except Exception as outer_e:
        print(f"Outer error in initialize_new_project_files: {outer_e}")
        print(f"Error type: {type(outer_e).__name__}")
        traceback.print_exc()
        return None

def main():
    if len(sys.argv) != 5:
        print("Usage: python initialize_new_project.py <nid> <title> <lt_project_base_path> <new_project_relative_path>")
        sys.exit(1)
    
    nid = sys.argv[1]
    title = sys.argv[2]
    lt_project_base_path = sys.argv[3]
    new_project_relative_path = sys.argv[4]
    
    print(f"Creating new project with:")
    print(f"  NID: {nid}")
    print(f"  Title: {title}")
    print(f"  Base Path: {lt_project_base_path}")
    print(f"  Relative Path: {new_project_relative_path}")
    
    new_project_path = initialize_new_project_files(nid, title, lt_project_base_path, new_project_relative_path)
    if new_project_path:
        print(f"Project initialized at {new_project_path}")
    else:
        print("Initialization failed")
        sys.exit(1)

if __name__ == '__main__':
    main()