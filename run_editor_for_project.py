import os
import sys
from app.editor.recent_project_dialog import choose_recent_project

from app.editor.editor_locale import init_locale
from app.engine.codegen import source_generator

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QLockFile, QDir, Qt
from PyQt5.QtGui import QIcon

from app.utilities.system_info import is_editor_engine_built_version

def initialize_translations():
    init_locale()

def initialize_icon():
    # Hack to get a Windows icon to show up
    try:
        import ctypes
        myappid = u'rainlash.lextalionis.ltmaker.current'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        print("Maybe not Windows? But that's OK")

def code_gen():
    # compile necessary files
    if not is_editor_engine_built_version():
        source_generator.generate_all()

def initialize_logger():
    from app import lt_log
    success = lt_log.create_logger()
    if not success:
        sys.exit()

if __name__ == '__main__':
    initialize_translations()
    initialize_icon()
    code_gen()
    initialize_logger()

    lockfile = QLockFile(QDir.tempPath() + '/lt-maker.lock')
    if lockfile.tryLock(100):
        # For High DPI displays
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

        ap = QApplication(sys.argv)
        ap.setWindowIcon(QIcon('favicon.ico'))
        from app import dark_theme
        theme = dark_theme.get_theme()
        dark_theme.set(ap, theme)
        
        # Check if a project path was provided as a command line argument
        if len(sys.argv) > 1:
            project_path = sys.argv[1]
            # Normalize path to handle any platform differences
            project_path = project_path.replace('\\', '/')
            # Ensure it ends with .ltproj if not already
            if not project_path.endswith('.ltproj'):
                project_path += '.ltproj'
                
            print(f'Opening project: {project_path}')
            
            # Verify the project exists
            if os.path.exists(project_path) and os.path.isdir(project_path):
                from app.editor.main_editor import MainEditor
                window = MainEditor(project_path)
                window.show()
                ap.exec_()
            else:
                print(f'Error: Project not found at {project_path}')
                sys.exit(1)
        else:
            # No project specified, fall back to normal selection dialog
            selected_path = choose_recent_project(allow_auto_open=True)
            if selected_path:
                from app.editor.main_editor import MainEditor
                window = MainEditor(selected_path)
                window.show()
                ap.exec_()
            else:
                print('Canceling...')
    else:
        print('LT-maker is already running!') 