import sys 
import os 
print("Python version:", sys.version) 
print("Python paths:", sys.path) 
sys.path.insert(0, r'Z:\Users\silver\Documents\Dev\personal\Infinit\fe-infinity-lt\lt-maker-fork') 
os.environ['PYTHONPATH'] = r'Z:\Users\silver\Documents\Dev\personal\Infinit\fe-infinity-lt\lt-maker-fork' + os.pathsep + os.environ.get('PYTHONPATH', '') 
try: 
    import run_engine_for_project 
    print("Successfully imported run_engine_for_project") 
    run_engine_for_project.main('_the-grand-tourney.ltproj') 
except ImportError as e: 
    print("Failed to import run_engine_for_project:", e) 
    sys.exit(1) 
except Exception as e: 
    print("Error running game:", e) 
    sys.exit(1) 
