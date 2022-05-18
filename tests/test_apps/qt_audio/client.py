from app import *
from PySide6.QtWidgets import QLineEdit, QFormLayout
import threading


class WaveReceiver(WaveWidget):
    def __init__(self, app: WaveApp, title="Wave Receiver"):
        super().__init__(app=app, title=title, geo=(1000, 50, 1, 1))

        self.connected = False

    def setup(self):
        super().setup()

        vlayout = QVBoxLayout(self)

        formLayout = QFormLayout()
        vlayout.addLayout(formLayout)

        self._server_ip = QLineEdit()
        formLayout.addRow("Server IP", self._server_ip)

        formLayout.addRow("Server Port", self._server_port)

        receive_layout = QGridLayout()
        vlayout.addLayout(receive_layout)

        self._connect = QPushButton()
        receive_layout.addWidget(self._connect, 0, 0)

        self._disconnect = QPushButton()
        self._disconnect.setEnabled(1)
        receive_layout.addWidget(self._disconnect, 0, 1)

        receive_layout.addWidget(self._buffer_size, 1, 0)

        receive_layout.addWidget(self._play_recording, 1, 1)

        self.SET_TEXT(self._server_ip, "localhost")
        self.SET_TEXT(self._connect, "Connect")
        self.SET_TEXT(self._disconnect, "Disconnect")

        self.CONNECT(self._connect, self.start_receiving)
        self.CONNECT(self._disconnect, self.disconnect_)
        self.DISABLE(self._disconnect)

    def get_ip_port(self):
        ip = self.GET_TEXT(self._server_ip)
        port = self.get_port()
        if not port:
            return

        if not ip:
            self.INFO("Invalid IP", "Enter a valid IP Address.")
            return

        return ip, port

    def start_receiving(self):
        self.DISABLE(self._connect)
        self.DISABLE(self._server_ip)
        self.DISABLE(self._server_port)
        self.ENABLE(self._disconnect)
        THREAD(self.connect_)

    def connect_(self):
        if self.connected:
            return

        ip_port = self.get_ip_port()
        if ip_port:
            ip, port = ip_port

            self.connected = True

            while self.connected:
                try:
                    self.sock = EasySocket(ip=ip, port=port)
                    self._start_receiving()
                except Exception as e:
                    print(e)
                    self.notConnected()
                    ...

            self.notConnected()

    def _start_receiving(self):
        chunks = b""
        available = False

        while self.connected:
            chunk = b""
            try:
                chunk = self.sock.recv(4096)
            except Exception as e:
                print(e)

            if not chunk:
                break

            chunks += chunk
            datas = []
            if self.DELIM in chunks:
                datas = chunks.split(self.DELIM)

            if datas:
                if chunks.endswith(self.DELIM):
                    chunks = b""
                else:
                    chunks = datas[-1]
                    datas = datas[:-1]

                for data in datas:
                    if data:
                        self.buffer.setData(data)
                        self.update_buffer_size()

                        if not available:
                            available = True
                            self.ENABLE(self._play_recording)
        self.disconnect_()

    def play_recording(self):
        super().play_recording(1)

    def disconnect_(self):
        self.connected = False
        self.notConnected()

    def notConnected(self):
        self.ENABLE(self._connect)
        self.ENABLE(self._server_ip)
        self.ENABLE(self._server_port)
        self.DISABLE(self._disconnect)

    def closing(self) -> None:
        self.disconnect_()
        return super().closing()


WaveApp(WaveReceiver)
