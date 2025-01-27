import sys
import os

from app.editor.file_manager.project_initializer import ProjectInitializer
from PyQt5.QtCore import QDir


def initialize_new_project_files(nid, title, lt_project_base_path, new_project_relative_path):
    initializer = ProjectInitializer()
    initializer.initialize_new_project_files_with_default_project_path(nid, title, lt_project_base_path, new_project_relative_path)
    return os.path.join(lt_project_base_path, new_project_relative_path)

def main():
    if len(sys.argv) != 5:
        print("Usage: python initialize_new_project.py <nid> <title> <lt_project_base_path> <new_project_relative_path>")
        sys.exit(1)
    
    nid = sys.argv[1]
    title = sys.argv[2]
    lt_project_base_path = sys.argv[3]
    new_project_relative_path = sys.argv[4]
    
    new_project_path = initialize_new_project_files(nid, title, lt_project_base_path, new_project_relative_path)
    if new_project_path:
        print(f"Project initialized at {new_project_path}")
    else:
        print("Initialization failed")
        sys.exit(1)

if __name__ == '__main__':
    main()