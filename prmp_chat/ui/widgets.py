
import os
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from . import resources


class STYLE:

    LIGHT = 'white'
    LIGHT_SHADE = '#f2e9e2'

    DARK = '#d85461'
    DARK_SHADE = '#d48f93'



# open("material-blue.qss").read()
HOME_STYLE = open(os.path.join(os.path.dirname(__file__), "resources/qss/normal.qss")).read() \

def GET_STYLE(): return HOME_STYLE % (
        STYLE.LIGHT_SHADE, STYLE.DARK_SHADE, # QWidget
        STYLE.DARK_SHADE, STYLE.LIGHT, # QPushButton
        STYLE.LIGHT_SHADE, # MenuButton
        STYLE.LIGHT, # IconButton
        STYLE.LIGHT_SHADE, # ChatRoomButton
        STYLE.LIGHT_SHADE, STYLE.DARK, # QPushButton::hover
        STYLE.DARK_SHADE, # MenuButton::hover
        STYLE.DARK, STYLE.LIGHT, # QPushButton::pressed

        STYLE.DARK, # QTabWidget::pane
        STYLE.LIGHT_SHADE, STYLE.DARK, STYLE.DARK, # QTabBar::tab
        STYLE.DARK_SHADE, STYLE.LIGHT_SHADE, # QTabBar::tab:hover

        STYLE.DARK, STYLE.LIGHT_SHADE, STYLE.LIGHT_SHADE, # QTabBar::tab:selected
        )


def SETUP_FRAME(mother_layout=None, orient='v', margins=[], obj=None, re_obj=0, space=0, klass=QFrame, **kwargs):
    margins = margins or [0, 0, 0, 0]
    
    if orient == 'v': Layout = QVBoxLayout
    elif orient == 'h': Layout = QHBoxLayout
    elif orient == 'g': Layout = QGridLayout

    frame = obj if obj else klass(**kwargs)
    
    frame_layout = None
    if orient:
        frame_layout = Layout(frame)
        frame_layout.setSpacing(space)
        frame_layout.setContentsMargins(*margins)

    if mother_layout: mother_layout.addWidget(frame)
    if re_obj: return (frame, frame_layout)
    else: return frame_layout or frame


def CREATE_TAB(tab, icon, name, klass=QFrame, kwargs={}):
    frame = klass(tab, **kwargs)
    tab.addTab(frame, QIcon(f':{icon}'), name)
    return frame


class ScrolledWidget(QScrollArea):
    def __init__(self, parent=None, widget=None, **kwargs):
        QScrollArea.__init__(self, parent)
        self._widget = widget or QWidget()

        self._layout = SETUP_FRAME(obj=self._widget, **kwargs)
        self.set_widget(self._widget)
        
        self.verticalScrollBar().rangeChanged.connect(self.scroll_down)
    
    def set_widget(self, widget):
        self.setWidget(widget)
        self.setWidgetResizable(True)

    def set_bars_off(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def scroll_down(self, minimum, maximum): self.verticalScrollBar().setSliderPosition(maximum)



class ChatWindow(QWidget):
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


class Popups(ChatWindow):
    def __init__(self, **kwargs):
        ChatWindow.__init__(self, flag=Qt.Popup, **kwargs)

