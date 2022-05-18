from .app_qt import *
from .app_qt import _WaveReceiver


class WaveReceiver(WaveWidgetCommon, _WaveReceiver):
    klass = _WaveReceiver

    def __init__(self, app: WaveApp, title="Wave Receiver"):
        _WaveReceiver.__init__(self, app=app, title=title, geo=(1000, 50, 1, 1))
        WaveWidgetCommon.__init__(self)

    def setup(self):
        WaveWidgetCommon.setup(self)

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

        receive_layout.addWidget(self._frames_details, 1, 0)

        receive_layout.addWidget(self._play_recording, 1, 1)

        _WaveReceiver.setup(self)


WaveApp(WaveReceiver)
