
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

NORMAL_STYLE = '''QWidget {background:rgb(20, 36, 43); color: white}
        QPushButton{
            border: 1px solid;
            border-radius: 4px ;
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 1 rgb(20, 36, 43), stop: 0 rgb(79, 113, 147));
            color: rgb(234, 183, 78)
        }

        QPushButton:pressed {
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 rgb(170, 132, 57), stop: 1 rgb(234, 183, 78));
            color:  rgb(20, 36, 43)
        }'''

BUTTON_ICON = '''QPushButton{
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 rgb(170, 132, 57), stop: 1 rgb(234, 183, 78));
            color:  rgb(20, 36, 43)
        }

        QPushButton:pressed {
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 1 rgb(20, 36, 43), stop: 0 rgb(79, 113, 147));
            color: rgb(234, 183, 78)
        }'''


# NORMAL_STYLE = BUTTON_ICON = ''

class Chat_Ui(QWidget):
    def __init__(self, parent=None, flag=Qt.Widget, client=None, app=None):
        QWidget.__init__(self, parent, flag)
        self.client = client
        
        self.app = app
        if not self.app: self.app = parent.app if parent else None

        self.setup_ui()
    
    def setup_ui(self): ...

    def centerWindow(self):
        size = self.size()
        a, b = size.width(), size.height()
        rect = self.app.screens()[0].availableGeometry()
        geo = QRect(int(rect.width()/2-a/2), int(rect.height()/2-b/2), a, b)
        self.setGeometry(geo)

    def closeEvent(self, event=0):
        if not self.parent():
            if self.app: self.app.quit()


class Popups(Chat_Ui):
    def __init__(self, **kwargs):
        Chat_Ui.__init__(self, flag=Qt.Popup, **kwargs)
