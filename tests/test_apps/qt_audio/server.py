from app import *
from mimi_plarec import Recorder
from PySide6.QtWidgets import QGroupBox


class WaveSender(WaveWidget):
    def __init__(self, app: WaveApp, title="Wave Sender"):
        super().__init__(app=app, title=title, geo=(50, 50, 1, 1))

        self.serving = False
        self.recorder = Recorder(stateReceiver=self.recording)
        self.clients: List[socket.socket] = []

        self.recording_timer = QTimer()
        self.recording_timer.setInterval(100)
        self.recording_timer.timeout.connect(self.update_buffer_size)

    def setup(self):
        super().setup()

        vlayout = QVBoxLayout(self)

        recording_box = QGroupBox("Recording")
        vlayout.addWidget(recording_box)

        recording_layout = QGridLayout(recording_box)

        self._record = QPushButton()
        recording_layout.addWidget(self._record, 0, 0)

        recording_layout.addWidget(self._buffer_size, 0, 1)

        self._stop_recording = QPushButton()
        self._stop_recording.setEnabled(0)
        recording_layout.addWidget(self._stop_recording, 1, 0)

        recording_layout.addWidget(self._play_recording, 1, 1)

        transfer_box = QGroupBox("Transfer")
        vlayout.addWidget(transfer_box)

        transfer_layout = QGridLayout(transfer_box)

        self._start_server = QPushButton()
        transfer_layout.addWidget(self._start_server, 0, 0)

        transfer_layout.addWidget(self._server_port, 0, 1)

        self._stop_server = QPushButton()
        self._stop_server.setEnabled(0)
        transfer_layout.addWidget(self._stop_server, 1, 0)

        self._send_recorded = QPushButton()
        self._send_recorded.setEnabled(0)
        transfer_layout.addWidget(self._send_recorded, 1, 1)

        self.SET_TEXT(self._record, "Record")
        self.CONNECT(self._record, self.record)

        self.SET_TEXT(self._stop_recording, "Stop Recording")
        self.CONNECT(self._stop_recording, self.stop_recording)
        self.DISABLE(self._stop_recording)

        self.SET_TEXT(self._start_server, "Start Server")
        self.CONNECT(self._start_server, self.start_server)

        self.SET_TEXT(self._stop_server, "Stop Server")
        self.CONNECT(self._stop_server, self.stop_server)
        self.DISABLE(self._stop_server)

        self.SET_TEXT(self._send_recorded, "Send Recorded")
        self.CONNECT(self._send_recorded, self.send_recorded)
        self.DISABLE(self._send_recorded)

    def record(self):
        self.buffer = self.recorder.record(new=True)
        self.DISABLE(self._record)
        self.DISABLE(self._send_recorded)

    def recording(self, state: QAudio.State):
        if state == QAudio.State.ActiveState:
            self.ENABLE(self._stop_recording)
            self.DISABLE(self._play_recording)
            self.DISABLE(self._send_recorded)

            self.recording_timer.start()

        elif state == QAudio.State.StoppedState:
            self.ENABLE(self._record)
            self.ENABLE(self._play_recording)
            self.DISABLE(self._stop_recording)
            self.recording_timer.stop()

            if self.serving and self.clients and self.buffer.data().data():
                self.ENABLE(self._send_recorded)
            else:
                self.DISABLE(self._send_recorded)

    def stop_recording(self):
        self.recorder.stop()

    def play_recording(self):
        super().play_recording(extra=not self.recorder.active)

    def start_server(self):
        port = self.get_port()
        if port:
            if not self.sock:
                self.sock = EasySocket(ip="", port=port, server=True)
                self.sock.listen(10)

            if not self.serving:
                self.serving = True
                THREAD(self.__start_server)

            self.DISABLE(self._start_server)
            self.DISABLE(self._server_port)
            self.ENABLE(self._stop_server)

            self.recording(self.recorder.state)

        else:
            return

    def __start_server(self):
        while self.serving:
            try:
                client, address = self.sock.accept()
                self.clients.append(client)
                self.update_()
            except socket.timeout:
                ...
            except:
                self.stop_server()
        self.update_()

    def stop_server(self):
        self.serving = False
        self.ENABLE(self._start_server)
        self.DISABLE(self._stop_server)
        self.DISABLE(self._send_recorded)
        self.update_()

    def send_recorded(self):
        bytes = self.buffer.data().data()
        if bytes:
            clients = self.clients.copy()
            for client in clients:
                try:
                    client.send(bytes + self.DELIM)
                except Exception as e:
                    self.clients.remove(client)
                    self.update_()

    def update_(self):
        self.recording(self.recorder.state)

    def closing(self) -> None:
        self.recorder.stop()
        self.stop_server()
        return super().closing()


WaveApp(WaveSender)
