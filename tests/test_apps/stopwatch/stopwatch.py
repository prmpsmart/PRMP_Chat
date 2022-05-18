from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *


class StopWatch(QObject):
    def __init__(self):
        super().__init__()

        self.time = QTime(0, 0, 0, 0)
        self.running = False
        self.runningTime = QElapsedTimer()

    def reset(self):
        self.time = QTime(0, 0, 0, 0)
        self.running = False

    def pause(self):
        if self.running:
            self.time = self.time.addMSecs(self.runningTime.elapsed())
            self.running = False

    def resume(self):
        self.running = True
        self.runningTime.restart()

    def start(self):
        self.running = True
        self.runningTime.start()

    @property
    def timeString(self) -> str:
        time = self.time.addMSecs(self.runningTime.elapsed())
        return time.toString("HH:mm:ss:") + str(time.msec())[:3]


class Frame(QFrame):
    def __init__(self, app: QApplication):
        super().__init__(f=Qt.Tool)
        self.setWindowTitle("StopWatch")

        self.app = app
        self.stopWatch = StopWatch()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

        self.setup()
        self.setMaximumWidth(60)

        self.timer.start(10)
        self.show()

    def setup(self):
        layout = QVBoxLayout(self)

        self.time = QLabel("00:00:00")
        self.time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.time)

        hlay = QHBoxLayout()
        layout.addLayout(hlay)

        self._reset = QPushButton("Reset")
        self._reset.clicked.connect(self.reset)
        hlay.addWidget(self._reset)

        self._startStop = QPushButton("Start")
        self._startStop.clicked.connect(self.startStop)
        hlay.addWidget(self._startStop)

    def update(self):
        super().update()
        if self.stopWatch.running:
            timeString = self.stopWatch.timeString
            self.time.setText(timeString)

    def reset(self):
        self._startStop.setText("Start")
        self.time.setText("00:00:00")
        self.stopWatch.reset()

    def startStop(self):
        if self.stopWatch.running:
            self._startStop.setText("Resume")
            self.stopWatch.pause()

        else:
            self._startStop.setText("Pause")
            self.stopWatch.start()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.app.exit()

    def __del__(self):
        del self.stopWatch


app = QApplication()
f = Frame(app)
app.exec()
