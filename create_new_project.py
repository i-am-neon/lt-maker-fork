import sys
import os

from app.editor.file_manager.project_initializer import ProjectInitializer
from PyQt5.QtCore import QDir


def normalize_path(path):
    """Normalize path for cross-platform compatibility."""
    # Remove any double quotes that might have been passed
    path = path.replace('"', '')
    # Convert to OS-specific path format
    return os.path.normpath(path)


def initialize_new_project_files(nid, title, lt_project_base_path, new_project_relative_path):
    print(f"lt_project_base_path{lt_project_base_path}")
    
    # Normalize paths for cross-platform compatibility
    lt_project_base_path = normalize_path(lt_project_base_path)
    new_project_relative_path = normalize_path(new_project_relative_path)
    
    # Debug the paths we're using
    print(f"HAHAHA {os.path.join(lt_project_base_path, new_project_relative_path)}")
    
    # Initialize the project
    initializer = ProjectInitializer()
    try:
        initializer.initialize_new_project_files_with_default_project_path(nid, title, lt_project_base_path, new_project_relative_path)
        return os.path.join(lt_project_base_path, new_project_relative_path)
    except Exception as e:
        print(f"Error initializing project: {e}")
        import traceback
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