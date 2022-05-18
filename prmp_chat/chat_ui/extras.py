from typing import Any

from .mimi_camera import Camera
from .base import *


def TOP_WINDOW(self: QWidget):
    top = self
    while top.parent():
        top = top.parent()
    return top


def SET_MARGINS(layout: QBoxLayout, m=2):
    layout.setContentsMargins(m, m, m, m)


def FONT_FORMAT(size=0, weight="") -> str:
    font = "font-family: TImes New Roman; "
    if size:
        font += f"font-size: {size}px; "
    if weight:
        font += f"font-weight: {weight}; "

    return font


def GET_DEFAULT_ICON(chat_object):
    if isinstance(chat_object, User):
        return "user"

    elif isinstance(chat_object, Contact):
        return "contact"

    elif isinstance(chat_object, Group):
        return "group"

    elif isinstance(chat_object, Channel):
        return "channel"


class Thread(QThread):
    def __init__(self, parent, function):
        super().__init__(parent)
        self.function = function

    def run(self):
        self.function()


class STYLE:

    LIGHT = "white"
    LIGHT_SHADE = "#f2e9e2"

    DARK = "#d85461"
    DARK_SHADE = "#d48f93"


def GET_STYLE():
    file = QFile(":qss/normal.qss")
    HOME_STYLE = file.readAll()
    # print(type(HOME_STYLE))
    return HOME_STYLE % (
        STYLE.LIGHT_SHADE,
        STYLE.DARK_SHADE,  # QWidget
        STYLE.DARK_SHADE,
        STYLE.LIGHT,  # QPushButton
        STYLE.LIGHT,  # ImageButton
        STYLE.LIGHT_SHADE,  # ChatRoomButton
        STYLE.LIGHT_SHADE,
        STYLE.DARK,  # QPushButton::hover
        STYLE.DARK_SHADE,
        STYLE.LIGHT,  # MenuButton
        STYLE.LIGHT_SHADE,  # MenuButton::hover
        STYLE.DARK,
        STYLE.LIGHT,  # QPushButton::pressed
        STYLE.DARK,  # QTabWidget::pane
        STYLE.LIGHT_SHADE,
        STYLE.DARK,
        STYLE.DARK,  # QTabBar::tab
        STYLE.DARK_SHADE,
        STYLE.LIGHT_SHADE,  # QTabBar::tab:hover
        STYLE.DARK,
        STYLE.LIGHT_SHADE,
        STYLE.LIGHT_SHADE,  # QTabBar::tab:selected
        STYLE.DARK_SHADE,
        STYLE.LIGHT,  # QLineEdit, QTetEdit
    )


def SETUP_FRAME(
    mother_layout: QLayout = None,
    orient="v",
    margins=[],
    obj=None,
    re_obj=0,
    space=0,
    klass=QFrame,
    **kwargs,
):
    margins = margins or [0, 0, 0, 0]

    if orient == "v":
        Layout = QVBoxLayout
    elif orient == "h":
        Layout = QHBoxLayout
    elif orient == "g":
        Layout = QGridLayout

    frame = None
    if obj:
        frame = obj
    elif klass:
        frame = klass(**kwargs)

    frame_layout = None
    if orient:
        frame_layout = Layout(frame)
        frame_layout.setSpacing(space)
        frame_layout.setContentsMargins(*margins)

    if mother_layout:
        if frame:
            mother_layout.addWidget(frame)
        else:
            mother_layout.addLayout(frame_layout)
    if re_obj:
        return (frame, frame_layout)
    else:
        return frame_layout or frame


def CREATE_TAB(tab, icon, name, klass=QFrame, kwargs={}):
    frame = klass(tab, **kwargs)
    tab.addTab(frame, GET_ICON(None, icon), name)
    return frame


def MASK_IMAGE(image: QImage, size=128) -> QImage:
    image = image.convertToFormat(QImage.Format_ARGB32)

    imgsize = min(image.width(), image.height())
    rect = QRect(
        (image.width() - imgsize) / 2, (image.height() - imgsize) / 2, imgsize, imgsize
    )
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

    return _image


def GET_PIXMAP(data, default, mask=0, mobile=False) -> QPixmap:
    image = None

    ICON_SET = DB.GET_ICON_SET()
    url = f":icons_{ICON_SET}/{default}.{ICON_SET}"

    if data:
        data = B64_DECODE(data) if isinstance(data, str) else data
        image = QImage.fromData(data, "JPEG" if mobile else "PNG")

    if not image:
        image = QImage(url)

    if data and mask:
        image = MASK_IMAGE(image, mask)

    pixmap = QPixmap(image)

    scale = 0
    if default in ["online", "offline"]:
        scale = 25

    if scale:
        pixmap = pixmap.scaled(scale, scale)

    if pixmap.isNull():
        print(url, "isNull=True")

    return pixmap


def GET_ICON(icon, default, mask=0) -> QIcon:
    pixmap = GET_PIXMAP(icon, default, mask=mask)
    return QIcon(pixmap)


def GET_IMAGE_DATA(image: QImage) -> bytes:
    buffer = QBuffer()
    image.save(buffer, "PNG")
    data = buffer.data().data()
    return data


def GET_PIXMAP_DATA(pixmap: QPixmap) -> bytes:
    return GET_IMAGE_DATA(pixmap.toImage())


class IconButton(QPushButton):
    def __init__(self, icon=None, size=None, parent=None, tip=""):
        QPushButton.__init__(self, parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._style = "text-align: center"
        self.default_style = lambda: self.setStyleSheet(self._style)
        self.default_style()

        self.set_icon(icon, tip)

        if isinstance(size, int):
            size = (size, size)

        if size and len(size) == 2:
            self.setMinimumSize(*size)
            self.setMaximumSize(*size)

    def set_icon(self, icon, tip=""):
        tip = tip or icon
        if tip:
            self.setToolTip(tip.title())

        if icon:
            icon = GET_ICON(None, icon)
            self.setIcon(icon)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.default_style()

    def showEvent(self, event):
        w, h = self.size().toTuple()
        self.setIconSize(QSize(w - 5, h - 5))


class ImageButton(IconButton):
    def __init__(self, default, mask=0, **kwargs):
        self.default = default
        self._mask = mask
        self.pixmap: QPixmap = None
        self.scalable = False
        super().__init__(**kwargs)

    def set_icon(self, pixmap: bytes, default=None):
        self.scalable = bool(pixmap)

        if not isinstance(pixmap, (QPixmap, QImage)):
            self._pixmap = pixmap
            if default:
                self.default = default

            if self._pixmap or self.default:
                self.pixmap = GET_PIXMAP(self._pixmap, self.default, mask=self._mask)
        else:
            self.pixmap = QPixmap(pixmap)

        self.scaleIcon()

    def scaleIcon(self) -> QIcon:
        pixmap = self.pixmap
        if self.pixmap:
            if self.scalable:
                pixmap = self.pixmap.scaled(self.size())
            self.setIcon(pixmap)

    def showEvent(self, event: QShowEvent) -> None:
        self.scaleIcon()
        return super().showEvent(event)


class ScrolledWidget(QScrollArea):
    def __init__(self, parent=None, widget=None, autoscroll=1, **kwargs):
        QScrollArea.__init__(self, parent)

        self._widget = widget or QWidget()
        self.set_widget(self._widget)
        self.children_widgets = []
        self.key_children_widgets = {}
        self._layout = SETUP_FRAME(obj=self._widget, **kwargs)

        if autoscroll:
            self.verticalScrollBar().rangeChanged.connect(self.scroll_down)
        self.set_hbar_off()

    def clear(self):
        for child in self.children_widgets:
            child.deleteLater()

        self.children_widgets.clear()
        self.key_children_widgets.clear()

    def get_child(self, key: Any) -> QWidget:
        return self.key_children_widgets.get(key)

    def add_child(self, child: QWidget, key, *args):
        self.children_widgets.append(child)
        self.key_children_widgets[key] = child
        self._layout.addWidget(child, *args)

    def insert_child(self, index: int, child: QWidget, key, *args):
        self.children_widgets.insert(index, child)
        self.key_children_widgets[key] = child
        self._layout.insertWidget(index, child, *args)

    def remove_child(self, key: object):
        if key in self.key_children_widgets:
            child: QWidget = self.key_children_widgets[key]
            del self.key_children_widgets[key]

            if child in self.children_widgets:
                self.children_widgets.remove(child)
                child.deleteLater()

    def set_widget(self, widget):
        self.setWidget(widget)
        self.setWidgetResizable(True)

    def set_hbar_off(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def set_vbar_off(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def set_bars_off(self):
        self.set_hbar_off()
        self.set_vbar_off()

    def set_hbar_on(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def set_vbar_on(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def set_bars_on(self):
        self.set_hbar_on()
        self.set_vbar_on()

    def scroll_down(self, minimum, maximum):
        self.verticalScrollBar().setSliderPosition(maximum)


# Buttons


class CropHood(QLabel):
    def __init__(
        self,
        parent=None,
        offset=0,
        shape="r",
        highlight=Qt.gray,
        border=Qt.red,
        line=Qt.NoPen,
        pattern=Qt.Dense5Pattern,
        maxw=0,
        maxh=0,
    ):
        "shape: s-> square, r-> rectangle, c-> circle"

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

        self.offset = offset
        self.begin_pos = QPoint(0 + offset, 0 + offset)
        self.end_pos = None

    def mousePressEvent(self, event):
        self.begin = event.position()

    def mouseMoveEvent(self, event):
        self.end = event.position().toPoint()

        if self.drawn and self.selected and self.selected.contains(self.end):
            self.move_selected = 1
        else:
            self.move_selected = 0
            if not self.started:
                self.started = 1
        self.update()

    def mouseReleaseEvent(self, ev):
        if self.started:
            self.drawn = 1

    def mouseDoubleClickEvent(self, event):
        self.drawn = False
        self.begin = QPoint()
        self.end = QPoint()
        self.update()
        self.selected = None

    def validate(self):
        x1, y1 = self.begin.toTuple()
        x2, y2 = self.end.toTuple()

        maxh = self.maxh or self.parent().height()
        maxw = self.maxw or self.parent().width()

        if self.started:
            if self.move_selected and self.selected:
                self.selected.moveCenter(self.end)

            else:
                sx1, sy1 = self.begin_pos.toTuple()
                sx2, sy2 = self.end_pos.toTuple()

                if x1 < sx1:
                    x1 = sx1
                if x1 > sx2:
                    x1 = sx2

                if x2 < sx1:
                    x2 = sx1
                if x2 > sx2:
                    x2 = sx2

                if y1 < sy1:
                    y1 = sy1
                if y1 > sy2:
                    y1 = sy2

                if y2 < sy1:
                    y2 = sy1
                if y2 > sy2:
                    y2 = sy2

                if maxw:
                    if abs(x2 - x1) > maxw:
                        if x2 > x1:
                            x2 = x1 + maxw
                        elif x1 > x2:
                            x2 = x1 - maxw

                if maxh:
                    if abs(y2 - y1) > maxh:
                        if y2 > y1:
                            y2 = y1 + maxh
                        elif y1 > y2:
                            y2 = y1 - maxh

        self.begin = QPoint(int(x1), int(y1))
        self.end = QPoint(int(x2), int(y2))

    def paintEvent(self, event):
        if not self.started:
            return

        self.validate()

        qp = QPainter(self)
        qp.setBrush(QBrush(self.highlight, self.pattern))
        qp.setPen(QPen(self.border, 2, self.line))

        self.selected = (
            self.selected if self.move_selected else QRect(self.begin, self.end)
        )

        if self.selected:

            if self.shape != "circle":
                func = qp.drawRect
            else:
                func = qp.drawEllipse
            func(self.selected)

    def resizeEvent(self, event):
        w, h = self.size().toTuple()
        self.end_pos = QPoint(w - (self.offset), h - (self.offset))


class CroppingWidget(QLabel):
    def __init__(self, image=None, parent=None, **kwargs):
        super().__init__(parent)

        self.hood = CropHood(self, **kwargs)
        self.image = self.scaled_image = None
        self.setScaledContents(1)
        self.setImage(image)

    @property
    def drawn(self):
        return self.hood.drawn

    @property
    def selected(self):
        return self.hood.selected

    def setImage(self, image: QImage):
        if image:
            self.image = image
            self.resizeEvent(0)

    def resizeEvent(self, event):
        if self.image:
            self.scaled_image = self.image.scaled(
                self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation
            )

            self.setPixmap(QPixmap(self.scaled_image))

        self.hood.setGeometry(self.rect())

    @property
    def selected_image(self) -> QImage:
        if not self.selected:
            return

        selected: QImage = self.scaled_image.copy(self.selected)

        w, h = self.selected.width(), self.selected.height()

        out_image = QImage(w, h, QImage.Format_ARGB32)
        out_image.fill(Qt.transparent)

        brush = QBrush(selected)

        painter = QPainter(out_image)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)

        if self.hood.shape == "c":
            painter.drawEllipse(0, 0, w, h)
        elif self.hood.shape in ["r", "s"]:
            painter.drawRect(0, 0, w, h)
        painter.end()

        return out_image


class CropImage(QDialog):
    def __init__(
        self,
        image=None,
        output=None,
        parent=None,
        f=Qt.Tool,
        title="Crop Image",
        **kwargs,
    ):
        QDialog.__init__(self, parent, f=f)

        self.setWindowIcon(GET_ICON(None, "image"))
        self.setWindowTitle(title)

        self.error = QMessageBox(self)
        self.error.setWindowTitle("Invalid selection")
        self.error.setText("Select an area to Image!")
        self.error.setInformativeText("You need to select a cropping area.")
        self.error.setStandardButtons(QMessageBox.Cancel)

        self.output = output

        layout = QVBoxLayout(self)
        SET_MARGINS(layout, 5)
        layout.setSpacing(2)

        self.view = CroppingWidget(image=image, **kwargs)
        self.view.setMinimumSize(500, 300)
        layout.addWidget(self.view)

        self.actions_frame = QFrame()
        layout.addWidget(self.actions_frame)

        self.actions_layout = QHBoxLayout(self.actions_frame)

        self._crop = QPushButton("Crop")
        self._crop.clicked.connect(self.crop)
        self._crop.setEnabled(0)
        self.actions_layout.addWidget(self._crop)

        self._save = QPushButton("Save")
        self._save.clicked.connect(self.save)
        self._save.setEnabled(0)
        self.actions_layout.addWidget(self._save)

    @property
    def image(self) -> QImage:
        return self.view.image

    def crop(self):
        if not self.view.drawn:
            self.error.show()
            return

        image = self.view.selected_image
        if image:
            self.save(image)

    def save(self, image: QImage = None):
        if self.output:
            self.output(image or self.image)


class CameraCapture(CropImage):
    def __init__(self, title="Capture Camera", **kwargs):
        super().__init__(title=title, **kwargs)

        self._capture = QPushButton("Capture")
        self._capture.clicked.connect(self.capture)
        self.actions_layout.insertWidget(0, self._capture)

        self.camera = Camera(receiver=self.imageCapture, mirror=1)

    def imageCapture(self, image: QImage):
        image = image.scaled(
            self.view.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        self.view.setImage(image)

    def capture(self):
        if self.camera.isActive():
            self.camera.stop()
            self._capture.setText("Resume")
            self._crop.setEnabled(1)
            self._save.setEnabled(1)
        else:
            self.camera.start()
            self._save.setEnabled(0)
            self._crop.setEnabled(0)
            self._capture.setText("Capture")

    def save(self, *a):
        if not self.camera.isActive():
            super().save(*a)

    def showEvent(self, arg__1: QShowEvent) -> None:
        self.camera.start()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.camera.stop()


class ImageChooser:
    def __init__(self, output, parent: QWidget):
        self.output = output
        self.parent = parent
        self.cam: CameraCapture = None

        self.mb = QMessageBox(
            QMessageBox.Icon.Question,
            "Select Picture",
            "How do you want to select image?",
            parent=self.parent,
        )
        self.mb.addButton("Use Camera", QMessageBox.AcceptRole)
        self.mb.addButton("Pick from Pictures", QMessageBox.RejectRole)
        self.mb.accepted.connect(self.useCamera)
        self.mb.rejected.connect(self.askFile)

    def show(self):
        self.mb.show()

    def useCamera(self):
        self.cam = CameraCapture(output=self.imageReceiver, parent=self.parent)
        self.cam.show()

    def askFile(self):
        if self.mb:
            self.mb.close()

        file = QFileDialog.getOpenFileName(
            self.parent,
            "Choose Image ",
            "",
            "Image files (*.jpg *.png)",
        )[0]

        if file:
            self.imageReceiver(QImage(file))

    def imageReceiver(self, image: QImage):
        if self.cam:
            self.cam.close()

        self.output(image)


class PasswordEdit(QLineEdit):
    def __init__(self, clear=False):
        super().__init__()
        self.shown = True
        self._clear = clear

        self.show_icon = GET_ICON(None, "eye")
        self.hide_icon = GET_ICON(None, "eye-off")

        self.button = QPushButton(self)
        self.button.setCursor(Qt.ArrowCursor)
        self.button.setStyleSheet("border: 0px; padding: 0px;")
        self.button.clicked.connect(self.switch)

        if self._clear:
            self.setClearButtonEnabled(True)

        # self.setEchoMode(QLineEdit.NoEcho)

        self.switch()

    def resizeEvent(self, event):
        buttonSize = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)

        clear = 25 if self._clear else 4

        self.button.move(
            self.rect().right() - frameWidth - clear - buttonSize.width(),
            (self.rect().bottom() - buttonSize.height() + 1) / 2,
        )

        return super().resizeEvent(event)

    def switch(self):
        if self.shown:
            self.button.setIcon(self.hide_icon)
            self.setEchoMode(QLineEdit.Password)
            self.shown = False
        else:
            self.button.setIcon(self.show_icon)
            self.setEchoMode(QLineEdit.Normal)
            self.shown = True


class StopWatch(QObject):
    def __init__(self):
        super().__init__()

        self.runningTime = QElapsedTimer()
        self.reset()

    def reset(self):
        self.time = QTime(0, 0, 0, 0)
        self.running = False

    def pause(self):
        if self.running:
            self.time = self.time.addMSecs(self.elapsed)
            self.running = False
            self.runningTime

    def resume(self):
        self.running = True
        self.runningTime.restart()

    def start(self):
        self.running = True
        self.runningTime.start()

    @property
    def elapsed(self):
        return self.runningTime.elapsed()

    @property
    def timeString(self) -> str:
        time = self.time if not self.running else self.time.addMSecs(self.elapsed)
        time = time.toString("HH:mm:ss:") + str(time.msec())[:2]
        return time


class Window(QWidget):
    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app

        screens = app.screens()

        font = QFont("Times New Roman")
        font.setPixelSize(16)
        self.setStyleSheet(FONT_FORMAT(16))

        self.setWindowIcon(GET_ICON(None, "chat"))

        if User.i():
            if len(screens) > 1:
                self.setScreen(screens[1])

            self.moveToScreen()
        else:
            self.setGeometry(10, 30, 1, 1)
            ...

        # self.moveToScreen()

    def moveToScreen(self):
        self.move(self.screen().availableGeometry().center() - self.rect().center())

    def centerWindow(self):
        screen_geo = self.screen().availableGeometry()
        s_w = screen_geo.width()
        s_h = screen_geo.height()

        w_w = self.width()
        w_h = self.height()

        x = (s_w - w_w) / 2
        y = (s_h - w_h) / 2

        self.setGeometry(x, y, w_w, w_h)

    def showEvent(self, event):
        # self.centerWindow()
        ...


class ServerSettings(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.db = User_DB()

        self.mb = QMessageBox(self)
        self.server_settings = self.db.load_server_settings()

        layout_a = QVBoxLayout(self)

        self.server_ip = QLineEdit(self.server_settings.get("ip") or "")
        self.server_ip.setPlaceholderText("Server IP")
        self.server_ip.setClearButtonEnabled(True)
        layout_a.addWidget(self.server_ip)

        self.server_port = QLineEdit(str(self.server_settings.get("port") or ""))
        self.server_port.setPlaceholderText("Server PORT")
        self.server_port.setClearButtonEnabled(True)

        layout_a.addWidget(self.server_port)

        buttons_layout = QHBoxLayout()

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_server_settings)
        save_button.setStyleSheet("text-align: center;")
        buttons_layout.addWidget(save_button)

        default_button = QPushButton("Default")
        default_button.clicked.connect(self.default_server_settings)
        default_button.setStyleSheet("text-align: center;")
        buttons_layout.addWidget(default_button)

        layout_a.addLayout(buttons_layout)

        for a in [self.server_ip, self.server_port]:
            a.setMinimumHeight(30)

        self.default_server_settings()

    def save_server_settings(self):
        ip = self.server_ip.text()
        port = self.server_port.text()

        if not ip:
            self.mb.setText("Ip Address cannot be empty !")
            self.mb.show()

        try:
            int(port)
        except:
            self.mb.setText("Invalid Port\nMust be a number!")
            self.mb.show()

        DB.SET_SERVER_SETTINGS((ip, port))
        self.db.save_server_settings(ip, port)
        self.mb.setText("Server settings saved!")
        self.mb.show()

    def default_server_settings(self):
        server_settings = DB.GET_SERVER_SETTINGS()
        if server_settings:
            self.server_ip.setText(server_settings[0])
            self.server_port.setText(str(server_settings[1]))
