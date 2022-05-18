from ..mimi_wave import *
from ..mimi_wave import _WaveApp, _WaveSender, _WaveReceiver, _WaveWidget
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class WaveApp(_WaveApp, QApplication):
    def __init__(self, windowClass: _WaveWidget):
        QApplication.__init__(self)
        _WaveApp.__init__(self, windowClass)

    def start(self):
        self.window.show()
        self.exec()

    def closing(self):
        self.quit()


class WaveWidgetCommon(QWidget):
    klass = None

    def __init__(self):
        QWidget.__init__(self, f=Qt.WindowStaysOnTopHint)

        self.setMinimumWidth(250)
        self.setMinimumWidth(250)

        self.setup()

    def GEOMETRY(self, geo):
        self.setGeometry(*geo)

    def INFO(self, title, text):
        QMessageBox.information(self, title, text)

    def TITLE(self, title):
        self.setWindowTitle(title)

    def CONNECT(self, widget: QWidget, func):
        widget.clicked.connect(func)

    def SET_TEXT(self, widget: QWidget, text):
        widget.setText(text)

    def GET_TEXT(self, widget: QWidget) -> str:
        return widget.text()

    def GET_INT(self, widget: QWidget) -> int:
        return widget.value()

    def DISABLE(self, widget: QWidget):
        widget.setEnabled(0)

    def ENABLE(self, widget: QWidget):
        widget.setEnabled(1)

    def setup(self):
        self._frames_details = QLabel()
        self._play_recording = QPushButton()
        self._server_port = QSpinBox()
        self._server_port.setRange(6000, 9000)
        self._server_port.setToolTip("Server Port")

    def closeEvent(self, event: QCloseEvent) -> None:
        self.klass.closing(self)
        return super().closeEvent(event)
