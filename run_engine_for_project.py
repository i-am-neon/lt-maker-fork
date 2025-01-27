import json
import argparse
from pathlib import Path
import os, sys

from app.constants import VERSION
from app.data.metadata import Metadata
from app.data.resources.resources import RESOURCES
from app.data.database.database import DB
from app.data.serialization.dataclass_serialization import dataclass_from_dict
from app.engine import engine
from app.engine import config as cf
from app.engine import driver
from app.engine import game_state
from app.engine.codegen import source_generator
from app.data.serialization.versions import CURRENT_SERIALIZATION_VERSION
from app.utilities.system_info import is_editor_engine_built_version

def main(name: str = 'testing_proj'):
    project_path = name if name.endswith('.ltproj') else name + '.ltproj'
    if not os.path.exists(project_path):
        raise ValueError(f"Could not locate LT project {project_path}")
    
    metadata = dataclass_from_dict(Metadata, json.loads(Path(project_path, 'metadata.json').read_text()))
    if metadata.has_fatal_errors:
        raise ValueError("Fatal errors detected in game. If you are the developer, please validate and then save your game data before proceeding. Aborting launch.")
    
    RESOURCES.load(project_path, CURRENT_SERIALIZATION_VERSION)
    DB.load(project_path, CURRENT_SERIALIZATION_VERSION)
    title = DB.constants.value('title')
    driver.start(title)
    game = game_state.start_game()
    driver.run(game)

def test_play(name: str = 'testing_proj'):
    if not os.path.exists(name + '.ltproj'):
        raise ValueError("Could not locate LT project %s" % (name + '.ltproj'))
    metadata = dataclass_from_dict(Metadata, json.loads(Path(name + '.ltproj', 'metadata.json').read_text()))
    if metadata.has_fatal_errors:
        raise ValueError("Fatal errors detected in game. If you are the developer, please validate and then save your game data before proceeding. Aborting launch.")
    RESOURCES.load(name + '.ltproj', CURRENT_SERIALIZATION_VERSION)
    DB.load(name + '.ltproj', CURRENT_SERIALIZATION_VERSION)
    title = DB.constants.value('title')
    driver.start(title, from_editor=True)
    if 'DEBUG' in DB.levels:
        game = game_state.start_level('DEBUG')
    else:
        first_level_nid = DB.levels[0].nid
        game = game_state.start_level(first_level_nid)
    driver.run(game)

def inform_error():
    print("=== === === === === ===")
    print("A bug has been encountered.")
    print("Please copy this error log and send it to rainlash!")
    print('Or send the file "saves/debug.log.1" to rainlash!')
    print("Thank you!")
    print("=== === === === === ===")

def find_and_run_project():
    for name in os.listdir('./'):
        if name.endswith('.ltproj'):
            main(name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Lex Talionis project')
    parser.add_argument('project', nargs='?', help='Project name without .ltproj extension')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    
    args = parser.parse_args()
    
    import logging, traceback
    from app import lt_log
    
    success = lt_log.create_logger()
    if not success:
        engine.terminate()
        
    if not is_editor_engine_built_version():
        source_generator.generate_all()
        
    try:
        if args.project:
            if args.test:
                test_play(args.project)
            else:
                main(args.project)
        else:
            find_and_run_project()
    except Exception as e:
        logging.exception(e)
        inform_error()
        pyver = f'{sys.version_info.major}.{sys.version_info.minor}'
        print(f'*** Lex Talionis Engine Version {VERSION} on Python {pyver} ***')
        print(f'Main Crash {str(e)}')
        traceback.print_exc()
        time.sleep(0.5)
        inform_error()
        engine.terminate(crash=True)
        time.sleep(5 if cf.SETTINGS['debug'] else 20)