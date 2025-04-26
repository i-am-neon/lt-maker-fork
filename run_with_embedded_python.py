import sys
import os
import runpy

# Add the current directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Now run the original script with arguments
if len(sys.argv) > 1:
    # Pass all arguments except the script name
    sys.argv = [sys.argv[0]] + sys.argv[1:]
    runpy.run_module('run_engine_for_project', run_name='__main__')
else:
    print("Usage: python run_with_embedded_python.py [project_name.ltproj]") 