import sys
import os
import json
from app.data.database.database import Database
from app.data.serialization.versions import CURRENT_SERIALIZATION_VERSION

def serialize_project_database(project_path, provided_game_nid=None, provided_title=None):
    """
    Properly serializes the database for a project.
    This ensures all database tables and references are correctly set up.
    
    Args:
        project_path: Full path to the project directory
        provided_game_nid: Optional game_nid to explicitly set
        provided_title: Optional title to explicitly set
    """
    try:
        print(f"Serializing database for project at: {project_path}")
        
        # First, read the current values from constants.json directly
        constants_file_path = os.path.join(project_path, 'game_data', 'constants.json')
        custom_game_nid = provided_game_nid
        custom_title = provided_title
        
        # If the NID and title weren't provided as arguments, try to read them from constants.json
        if not custom_game_nid or not custom_title:
            try:
                with open(constants_file_path, 'r') as f:
                    constants_data = json.load(f)
                    for constant in constants_data:
                        if constant['nid'] == 'game_nid' and not custom_game_nid:
                            custom_game_nid = constant['value']
                        elif constant['nid'] == 'title' and not custom_title:
                            custom_title = constant['value']
                
                print(f"Found in constants.json: game_nid={custom_game_nid}, title={custom_title}")
            except Exception as e:
                print(f"Error reading constants.json: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"Using provided values: game_nid={custom_game_nid}, title={custom_title}")
        
        # Load the database for the project
        new_project_db = Database()
        new_project_db.load(project_path, CURRENT_SERIALIZATION_VERSION)
        
        # Check what values the database loaded
        current_game_nid = new_project_db.constants.get('game_nid').value
        current_title = new_project_db.constants.get('title').value
        print(f"Database initially loaded with: game_nid={current_game_nid}, title={current_title}")
        
        # Set the correct values from constants.json or from provided arguments into the database
        if custom_game_nid and custom_game_nid != current_game_nid:
            print(f"Updating game_nid in database from {current_game_nid} to {custom_game_nid}")
            new_project_db.constants.get('game_nid').set_value(custom_game_nid)
        
        if custom_title and custom_title != current_title:
            print(f"Updating title in database from {current_title} to {custom_title}")
            new_project_db.constants.get('title').set_value(custom_title)
        
        # Serialize the database back to the project directory
        # This ensures all tables and references are properly set up
        print(f"Serializing database to: {project_path}")
        new_project_db.serialize(project_path)
        
        print(f"Database serialization completed successfully")
        return True
    except Exception as e:
        print(f"Error serializing database: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python serialize_project_db.py <project_full_path> [game_nid] [title]")
        sys.exit(1)
    
    project_path = sys.argv[1]
    game_nid = sys.argv[2] if len(sys.argv) > 2 else None
    title = sys.argv[3] if len(sys.argv) > 3 else None
    
    success = serialize_project_database(project_path, game_nid, title)
    
    if success:
        print("Project database serialization successful")
        sys.exit(0)
    else:
        print("Project database serialization failed")
        sys.exit(1)

if __name__ == '__main__':
    main() 