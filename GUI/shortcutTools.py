import os
from PyQt5.QtWidgets import QAction

try:
    from GUI.shortCut import create_python_shortcut_onDesktop
except ModuleNotFoundError:
    from shortCut import create_python_shortcut_onDesktop

class shortcutAction(QAction):
    def __init__(self, program_path, **kwargs):
        super().__init__(**kwargs)
        self.program_path = program_path
        self.triggered.connect(self.execute_process)
        
    def execute_process(self):
        create_python_shortcut_onDesktop(script_path=self.program_path)