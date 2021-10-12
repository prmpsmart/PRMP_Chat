
import os
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from base64 import b64decode

from . import resources


class STYLE:

    LIGHT = 'white'
    LIGHT_SHADE = '#f2e9e2'

    DARK = '#d85461'
    DARK_SHADE = '#d48f93'



HOME_STYLE = open(os.path.join(os.path.dirname(__file__), "resources/qss/normal.qss")).read()


def GET_STYLE(): return HOME_STYLE % (
        STYLE.LIGHT_SHADE, STYLE.DARK_SHADE, # QWidget
        STYLE.DARK_SHADE, STYLE.LIGHT, # QPushButton
        STYLE.LIGHT, # IconButton
        STYLE.LIGHT_SHADE, # ChatRoomButton
        STYLE.LIGHT_SHADE, STYLE.DARK, # QPushButton::hover
        STYLE.DARK_SHADE, STYLE.LIGHT,# MenuButton
        STYLE.LIGHT_SHADE, # MenuButton::hover
        STYLE.DARK, STYLE.LIGHT, # QPushButton::pressed
        STYLE.DARK, # QTabWidget::pane
        STYLE.LIGHT_SHADE, STYLE.DARK, STYLE.DARK, # QTabBar::tab
        STYLE.DARK_SHADE, STYLE.LIGHT_SHADE, # QTabBar::tab:hover

        STYLE.DARK, STYLE.LIGHT_SHADE, STYLE.LIGHT_SHADE, # QTabBar::tab:selected
        STYLE.DARK_SHADE, STYLE.LIGHT, # QLineEdit, QTetEdit
    )


def SETUP_FRAME(mother_layout: QLayout=None, orient='v', margins=[], obj=None, re_obj=0, space=0, klass=QFrame, **kwargs):
    margins = margins or [0, 0, 0, 0]
    
    if orient == 'v': Layout = QVBoxLayout
    elif orient == 'h': Layout = QHBoxLayout
    elif orient == 'g': Layout = QGridLayout

    frame = None
    if obj: frame = obj
    elif klass: frame = klass(**kwargs)
    
    frame_layout = None
    if orient:
        frame_layout = Layout(frame)
        frame_layout.setSpacing(space)
        frame_layout.setContentsMargins(*margins)

    if mother_layout:
        if frame: mother_layout.addWidget(frame)
        else: mother_layout.addLayout(frame_layout)
    if re_obj: return (frame, frame_layout)
    else: return frame_layout or frame


def CREATE_TAB(tab, icon, name, klass=QFrame, kwargs={}):
    frame = klass(tab, **kwargs)
    tab.addTab(frame, QIcon(f':{icon}'), name)
    return frame


def MASK_IMAGE(image, size=128, pix=0):
    if isinstance(image, bytes):
        _image = QImage()
        _image.loadFromData(image)
        image = _image
    elif isinstance(image, str): image = QImage(image)

    image = image.convertToFormat(QImage.Format_ARGB32)

    imgsize = min(image.width(), image.height())
    rect = QRect((image.width()-imgsize)/2, (image.height()-imgsize)/2, imgsize, imgsize)
    image = image.copy(rect)

    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)

    brush = QBrush(image)

    painter = QPainter(out_img)
    painter.setBrush(brush)
    painter.setPen(Qt.NoPen)
    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.drawEllipse(0, 0, imgsize, imgsize)
    painter.end()

    _image = out_img.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    _image.setDevicePixelRatio(QWindow().devicePixelRatio())

    if pix: return QPixmap(_image)
    return _image


def GET_ICON(icon, default='', size=128):
    if isinstance(icon, bytes):
        icon = b64decode(icon)
        icon = MASK_IMAGE(icon, size=size, pix=1)

    elif icon and isinstance(icon, str): icon = f':{icon}'

    elif not icon: icon = default
    icon = QIcon(icon)
    return icon


# Buttons
class ImageButton(QPushButton):
    def __init__(self, parent=None, icon=None, size=0, offset=5):
        QPushButton.__init__(self, parent)
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self._style = 'text-align: center'
        self.default_style = lambda: self.setStyleSheet(self._style)
        self.default_style()

        self.offset = offset

        self.set_icon(icon)

        if size:
            self.setMinimumSize(size, size)
            self.setMaximumSize(size, size)
    
    def set_icon(self, icon):
        self._icon = icon
        icon = GET_ICON(icon, default=':chat_list/user.svg')
        self.setIcon(icon)
    
    def mouseReleaseEvent(self, event): self.default_style()

    def resizeEvent(self, event):
        s = self.size().toTuple()
        s = QSize(s[0]-self.offset, s[1]-self.offset)
        self.setIconSize(s)
        # self.


class Icon2Button(QPushButton):

    def __init__(self, icon, text, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon(f':{icon}'))
        self.setText(text)


class MenuButton(Icon2Button):
    def _hide(self): self.setText('')
    def _show(self): self.setText(self.tip)

    def __init__(self, ref=None, icon='', tip='', user=0, window=0, action=None, parent=None, show=0):
        super().__init__(icon, tip, parent=parent)
        
        self.setToolTip(tip)
        self.tip = tip
        self.ref = ref
        self.user = user
        self._win = window
        self._window = None
        self.clicked.connect(action or self.action)
        if show: self._show()
        else: self._hide()
    
    def action(self):
        if self._win:
            if not self._window: self._window = self._win(parent=self, user=self.user)

            pos = self.ref.pos()
            
            geo = self.geometry()

            self._window.move(pos.x()+geo.width()+10, pos.y()+geo.y())
            self._window.show()


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

# Buttons

class ChatWindow(QWidget):
    def __init__(self, parent=None, flag=Qt.Widget, user=None, app=None):
        QWidget.__init__(self, parent, flag)
        self.user = user
        
        self.app = app
        self.setup_ui()
    
    def setup_ui(self): ...

    def centerWindow(self):
        self.move(QApplication.primaryScreen().availableGeometry().center()-self.rect().center())

    def closeEvent(self, event=0):
        if not self.parent():
            if self.app: self.app.quit()


class CropHood(QLabel):

    def __init__(self, parent=None, offset=0, shape='r', highlight=Qt.gray, border=Qt.red, line=Qt.NoPen, pattern=Qt.Dense5Pattern, maxw=0, maxh=0):
        'shape: s-> square, r-> rectangle, c-> circle'

        super().__init__(parent)

        self.begin = QPoint()
        self.end = QPoint()

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.shape = shape
        self.highlight = highlight
        self.pattern = pattern
        
        self.maxw = maxw
        self.maxh = maxh
        
        self.border = border
        self.line = line
        
        self.selected: QRect = None
        self.drawn = 0
        self.started = 0
        self.move_selected = 0

        self.begin_pos = QPoint(0+offset, 0+offset)
        self.end_pos = None
        self.offset = offset

    def mousePressEvent(self, event):
        self.begin = event.position()

    def mouseMoveEvent(self, event):
        self.end = event.position().toPoint()
        
        if self.drawn and self.selected and self.selected.contains(self.end):
            self.move_selected = 1
        else:
            self.move_selected = 0
            if not self.started: self.started = 1
        self.update()
    
    def mouseReleaseEvent(self, ev):
        if self.started: self.drawn = 1

    def mouseDoubleClickEvent(self, event):
        self.drawn = False
        self.begin = QPoint()
        self.end = QPoint()
        self.update()
        self.selected = None

    def validate(self):
        x1, y1 = self.begin.toTuple()
        x2, y2 = self.end.toTuple()

        if self.started:
            if self.move_selected and self.selected: self.selected.moveCenter(self.end)

            else:
                sx1, sy1 = self.begin_pos.toTuple()
                sx2, sy2 = self.end_pos.toTuple()

                if x1 < sx1: x1 = sx1
                if x1 > sx2: x1 = sx2
                
                if x2 < sx1: x2 = sx1
                if x2 > sx2: x2 = sx2
                
                if y1 < sy1: y1 = sy1
                if y1 > sy2: y1 = sy2
                
                if y2 < sy1: y2 = sy1
                if y2 > sy2: y2 = sy2

                if self.shape == 's':
                    m = min(sx2, sy2)
                    if x2 > m: x2 = m
                    if y2 > m: y2 = m
                
                if self.maxw:
                    if abs(x2 - x1) > self.maxw:
                        if x2 > x1: x2 = x1 + self.maxw
                        elif x1 > x2: x2 = x1 - self.maxw

                if self.maxh:
                    if abs(y2 - y1) > self.maxh:
                        if y2 > y1: y2 = y1 + self.maxh
                        elif y1 > y2: y2 = y1 - self.maxh

        self.begin = QPoint(int(x1), int(y1))
        self.end = QPoint(int(x2), int(y2))

    def paintEvent(self, event):
        if not self.started: return

        self.validate()

        qp = QPainter(self)
        qp.setBrush(QBrush(self.highlight, self.pattern))
        qp.setPen(QPen(self.border, 2, self.line))

        self.selected = self.selected if self.move_selected else QRect(self.begin, self.end)

        if self.shape in ['r', 's']: qp.drawRect(self.selected)
        elif self.shape == 'c': qp.drawEllipse(self.selected)

    def resizeEvent(self, event):
        s = self.size()
        self.end_pos = QPoint(s.width()-(self.offset), s.height()-(self.offset))


class CroppingWidget(QLabel):

    def __init__(self, image=None, parent=None, **kwargs):
        super().__init__(parent)

        self.hood = CropHood(self, **kwargs)
        self.image_name = image
        self.image = self.scaled_image = None
        self.setScaledContents(1)
    
    @property
    def drawn(self): return self.hood.drawn

    @property
    def selected(self): return self.hood.selected

    def resizeEvent(self, event):
        if self.image_name:
            self.image = QImage(self.image_name)
            self.scaled_image = self.image.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

            self.setPixmap(QPixmap(self.scaled_image))
        
        self.hood.setGeometry(self.rect())

    @property
    def selected_image(self):
        selected: QImage = self.scaled_image.copy(self.selected)

        w, h = self.selected.width(), self.selected.height()

        out_image = QImage(w, h, QImage.Format_ARGB32)
        out_image.fill(Qt.transparent)
        
        brush = QBrush(selected)

        painter = QPainter(out_image)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)

        if self.hood.shape == 'c': painter.drawEllipse(0, 0, w, h)
        elif self.hood.shape in ['r', 's']: painter.drawRect(0, 0, w, h)
        painter.end()

        finished_image = QPixmap.fromImage(out_image)

        return finished_image

