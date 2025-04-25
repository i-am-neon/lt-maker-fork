import os
import shutil
import traceback
from typing import Tuple

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileDialog

from app.data.database.database import Database
from app.data.serialization.versions import CURRENT_SERIALIZATION_VERSION
from app.editor.new_game_dialog import NewGameDialog


class ProjectInitializer():
    def full_create_new_project(self):
        result = self.get_new_project_info()
        if result:
            nid, title, path = result
            self.initialize_new_project_files(nid, title, path)
            return nid, title, path
        return False

    def get_new_project_info(self) -> Tuple[str, str, str]:
        """Launches a few dialogs that query the user for required project info.

        Returns:
            Tuple[str, str, str]: (ID, Title, ProjectPath)
        """
        id_title_info = NewGameDialog.get()
        if not id_title_info:
            return False
        curr_path = QDir()
        curr_path.cdUp()
        proj_nid, proj_title = id_title_info
        starting_path = curr_path.path() + '/' + proj_title + '.ltproj'
        proj_path, ok = QFileDialog.getSaveFileName(None, "Save Project", starting_path,
                                                    "All Files (*)")
        if not ok:
            return False
        return proj_nid, proj_title, proj_path

    def initialize_new_project_files(self, nid, title, path):
        try:
            default_path = QDir.currentPath() + '/' + 'default.ltproj'
            print(f"Copying from {default_path} to {path}")
            shutil.copytree(default_path, path)
            new_project_db = Database()
            new_project_db.load(path, CURRENT_SERIALIZATION_VERSION)
            new_project_db.constants.get('game_nid').set_value(nid)
            new_project_db.constants.get('title').set_value(title)
            new_project_db.serialize(path)
            print(f"Project successfully initialized at: {path}")
        except Exception as e:
            print(f"Error in initialize_new_project_files: {e}")
            print(f"Error type: {type(e).__name__}")
            traceback.print_exc()
            raise

    def initialize_new_project_files_with_default_project_path(self, nid, title, lt_project_base_path, new_project_relative_path):
        try:
            # Normalize paths for consistency
            lt_project_base_path = os.path.normpath(lt_project_base_path)
            new_project_relative_path = os.path.normpath(new_project_relative_path)
            
            print(f"lt_project_base_path: {lt_project_base_path}")
            print(f"new_project_relative_path: {new_project_relative_path}")
            
            # Use os.path.join for proper path handling
            new_project_directory = os.path.join(lt_project_base_path, new_project_relative_path)
            default_project_path = os.path.join(lt_project_base_path, 'default.ltproj')
            
            print(f"Creating new project at: {new_project_directory}")
            print(f"Copying from default project at: {default_project_path}")
            
            # Ensure the parent directory exists
            parent_dir = os.path.dirname(new_project_directory)
            if not os.path.exists(parent_dir):
                print(f"Creating parent directory: {parent_dir}")
                os.makedirs(parent_dir, exist_ok=True)
            
            # Verify source exists before copying
            if not os.path.exists(default_project_path):
                raise FileNotFoundError(f"Default project not found at: {default_project_path}")
                
            # Copy the default project
            shutil.copytree(default_project_path, new_project_directory)
            print(f"Project directory successfully created at: {new_project_directory}")
            
            # Load and update the database
            new_project_db = Database()
            new_project_db.load(new_project_directory, CURRENT_SERIALIZATION_VERSION)
            new_project_db.constants.get('game_nid').set_value(nid)
            new_project_db.constants.get('title').set_value(title)
            new_project_db.serialize(new_project_directory)
            print(f"Project database successfully updated")
        except Exception as e:
            print(f"Error in initialize_new_project_files_with_default_project_path: {e}")
            print(f"Error type: {type(e).__name__}")
            traceback.print_exc()
            raise