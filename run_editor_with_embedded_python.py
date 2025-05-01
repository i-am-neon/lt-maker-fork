import sys
import os
import runpy

# Add the current directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Check which editor module to run based on arguments
if len(sys.argv) > 1:
    # First argument decides which editor module to run
    editor_module = sys.argv[1]
    
    # Remove the script and module name from argv
    if len(sys.argv) > 2:
        # Pass the remaining arguments to the module
        sys.argv = [sys.argv[0]] + sys.argv[2:]
    else:
        # No additional arguments
        sys.argv = [sys.argv[0]]
    
    if editor_module == "run_editor_for_project.py":
        # Run the editor with a specific project
        runpy.run_module('run_editor_for_project', run_name='__main__')
    elif editor_module == "run_editor.py":
        # Run the editor without a specific project
        runpy.run_module('run_editor', run_name='__main__')
    else:
        print(f"Unknown editor module: {editor_module}")
        print("Usage: python run_editor_with_embedded_python.py [run_editor.py|run_editor_for_project.py] [project_name.ltproj]")
        sys.exit(1)
else:
    print("Usage: python run_editor_with_embedded_python.py [run_editor.py|run_editor_for_project.py] [project_name.ltproj]")
    sys.exit(1) 