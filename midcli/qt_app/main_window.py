from PyQt5.QtWidgets import QMainWindow, QSizePolicy, QApplication
from PyQt5.QtCore import QUrl
from .web_view import MainWebView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TrueNAS Web Interface')
        
        screen = QApplication.primaryScreen()
        size = screen.size()
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(size)
        
        self.web_view = MainWebView()
        self.web_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.web_view.setMinimumSize(size)
        
        self.setCentralWidget(self.web_view)
        self.showFullScreen()
        
        self.web_view.load(QUrl("http://localhost"))
