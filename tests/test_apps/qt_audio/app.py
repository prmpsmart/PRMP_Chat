import socket, threading, time
from threading import Thread
from typing import List
from mimi_plarec import QAudio, QBuffer, Player, QTimer
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QSpinBox,
    QWidget,
    QMessageBox,
    QLabel,
    QVBoxLayout,
    QGridLayout,
)


def THREAD(func):
    Thread(target=func).start()


class EasySocket:
    def __init__(self, ip=None, port=None, sock: socket.socket = None, server=False):
        self.ip = ip
        self.port = port
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

        if ip != None and port:
            func = self.bind if server else self.connect
            func(ip, port)

    def connect(self, host, port):
        self.sock.connect((host, port))

    def bind(self, host, port):
        self.sock.bind((host, port))

    def send(self, data):
        return self.sock.send(data)

    def recv(self, read):
        return self.sock.recv(read)

    def accept(self, time=3):
        if time:
            self.sock.settimeout(time)
        return self.sock.accept()

    def listen(self, *args):
        return self.sock.listen(*args)

    def close(self):
        try:
            self.sock.setblocking(False)
            self.sock.shutdown(0)
            self.sock.close()
        except:
            ...

    def __del__(self):
        del self.sock


class WaveApp(QApplication):
    def __init__(self, windowClass: type):
        QApplication.__init__(self)

        self.window: WaveWidget = windowClass(self)
        self.window.show()
        self.exec()

    def closing(self):
        self.quit()


class WaveWidget(QWidget):
    DELIM = b"<<>>"

    def __init__(self, app: WaveApp, title="Wave Widget", geo=()):
        QWidget.__init__(self, f=Qt.WindowStaysOnTopHint)

        self.app = app
        self._title = title
        self._geo = geo
        self.sock: EasySocket = None

        self.player = Player(stateReceiver=self.playing)
        self.buffer: QBuffer = QBuffer()

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
        self._buffer_size = QLabel()
        self._play_recording = QPushButton()
        self._server_port = QSpinBox()
        self._server_port.setRange(6000, 9000)
        self._server_port.setToolTip("Server Port")

        self.TITLE(self._title)
        if self._geo:
            self.GEOMETRY(self._geo)

        self.SET_TEXT(self._buffer_size, "Size")
        self.SET_TEXT(self._play_recording, "Play Recording")
        self.CONNECT(self._play_recording, self.play_recording)
        self.DISABLE(self._play_recording)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.closing()
        return super().closeEvent(event)

    def update_buffer_size(self):
        size = self.buffer.size()
        text = f"{size} B"
        self.SET_TEXT(self._buffer_size, text)

    def playing(self, state: QAudio.State):
        if state == QAudio.State.ActiveState:
            self.SET_TEXT(self._play_recording, "Stop Playing")

        else:
            self.SET_TEXT(self._play_recording, "Play Recording")

    def play_recording(self, extra=True):
        if extra and not self.player.active:
            self.player.play(buffer=self.buffer, block=0)
        else:
            self.player.stop()

    def get_port(self):
        port = self.GET_INT(self._server_port)
        if 6000 <= port <= 9000:
            return port
        else:
            self.INFO("Invalid Port", "The port should be from 6000 and 9000")

    def closing(self) -> None:
        self.player.stop()

        if self.sock:
            self.sock.close()

        self.app.closing()
