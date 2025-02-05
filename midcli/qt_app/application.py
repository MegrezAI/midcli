import os
import sys
from PyQt5.QtWidgets import QApplication
from .main_window import MainWindow

def launch_application():

    os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = "9222"
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-logging --log-level=0 --no-sandbox"
    os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()