''' app/init.py '''
import sys
from PyQt6.QtWidgets import QApplication
from .ui.main_window import MainWindow
from .utils.config import AppConfig
# from .ui.widgets.copilot_worker import Gui


def run() -> int:
    """
    Initializes the application and runs it.

    Returns:
        int: The exit status code.
    """
    app: QApplication = QApplication(sys.argv)
    AppConfig.initialize()

    window: MainWindow = MainWindow()
    window.show()

    # Handling of exit functions upon application exit
    def onExit():
        window.abort_countdown()  # Stops the worker and thread
    app.aboutToQuit.connect(onExit)

    return sys.exit(app.exec())

